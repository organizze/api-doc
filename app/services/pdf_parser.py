import pdfplumber
from typing import List, Optional
from datetime import date
import re
from dataclasses import dataclass


@dataclass
class ParsedIncome:
    """Representa um recebimento extraído do PDF"""

    client_name: str
    description: str
    amount_cents: int
    expected_date: date
    raw_text: str


class PDFParserService:
    """
    Serviço para parsing de PDFs com valores previstos de recebimento.

    Suporta diferentes formatos:
    - Tabelas estruturadas
    - Texto livre com padrões de valor
    - Boletos/faturas
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = ""
        self.tables: List[List[List[str]]] = []

    def extract_content(self) -> None:
        """Extrai texto e tabelas do PDF"""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                # Extrair texto
                page_text = page.extract_text() or ""
                self.text += page_text + "\n"

                # Extrair tabelas
                page_tables = page.extract_tables()
                if page_tables:
                    self.tables.extend(page_tables)

    def parse_income_values(self) -> List[ParsedIncome]:
        """
        Analisa o conteúdo e extrai valores de recebimento previsto.

        Tenta múltiplas estratégias:
        1. Parsing de tabelas estruturadas
        2. Regex para padrões de valor no texto
        """
        results = []

        # Estratégia 1: Parsing de tabelas
        for table in self.tables:
            table_results = self._parse_table(table)
            results.extend(table_results)

        # Estratégia 2: Regex para padrões de valor no texto
        if not results:
            text_results = self._parse_text_patterns()
            results.extend(text_results)

        return results

    def _parse_table(self, table: List[List[str]]) -> List[ParsedIncome]:
        """
        Analisa uma tabela extraída do PDF.
        Tenta identificar colunas de:
        - Cliente/Descrição
        - Valor
        - Data
        """
        results = []

        if not table or len(table) < 2:
            return results

        # Tentar identificar headers
        header = [str(h).lower() if h else "" for h in table[0]]

        value_col = self._find_column_index(
            header, ["valor", "value", "total", "amount", "quantia", "preço", "preco"]
        )
        date_col = self._find_column_index(
            header, ["data", "date", "vencimento", "due", "prazo", "pagamento"]
        )
        desc_col = self._find_column_index(
            header,
            [
                "descricao",
                "descrição",
                "description",
                "cliente",
                "client",
                "nome",
                "name",
                "item",
            ],
        )

        # Se não encontrou headers, tentar inferir pela estrutura
        if value_col < 0:
            # Procurar coluna com valores monetários
            for i, cell in enumerate(table[1] if len(table) > 1 else []):
                if cell and self._parse_currency(str(cell)) > 0:
                    value_col = i
                    break

        # Processar linhas
        for row in table[1:]:
            if not row or all(not cell for cell in row):
                continue

            try:
                # Extrair valor
                amount = 0
                if value_col >= 0 and value_col < len(row):
                    amount = self._parse_currency(str(row[value_col] or ""))

                # Se não encontrou na coluna esperada, procurar em todas
                if amount == 0:
                    for cell in row:
                        if cell:
                            parsed = self._parse_currency(str(cell))
                            if parsed > 0:
                                amount = parsed
                                break

                if amount == 0:
                    continue

                # Extrair data
                parsed_date = date.today()
                if date_col >= 0 and date_col < len(row) and row[date_col]:
                    parsed_date = self._parse_date(str(row[date_col]))
                else:
                    # Procurar data em qualquer célula
                    for cell in row:
                        if cell:
                            try_date = self._parse_date(str(cell))
                            if try_date != date.today():
                                parsed_date = try_date
                                break

                # Extrair descrição
                description = ""
                if desc_col >= 0 and desc_col < len(row) and row[desc_col]:
                    description = str(row[desc_col])
                else:
                    # Usar primeira célula não numérica como descrição
                    for cell in row:
                        if cell and not self._is_numeric(str(cell)):
                            description = str(cell)
                            break

                if not description:
                    description = " | ".join(str(c) for c in row if c)

                results.append(
                    ParsedIncome(
                        client_name=description[:255],
                        description=description,
                        amount_cents=amount,
                        expected_date=parsed_date,
                        raw_text=str(row),
                    )
                )
            except (IndexError, ValueError, TypeError):
                continue

        return results

    def _parse_text_patterns(self) -> List[ParsedIncome]:
        """
        Extrai valores usando regex para padrões comuns:
        - R$ 1.234,56
        - Datas: dd/mm/yyyy, yyyy-mm-dd
        """
        results = []

        # Padrão para valores monetários brasileiros
        # Captura: R$ 1.234,56 ou 1.234,56 ou 1234,56
        currency_pattern = r"R?\$?\s*([\d]{1,3}(?:\.[\d]{3})*,[\d]{2})"

        # Padrão para datas brasileiras
        date_pattern = r"(\d{2}/\d{2}/\d{4})"

        # Encontrar todas as ocorrências
        amounts = re.findall(currency_pattern, self.text)
        dates = re.findall(date_pattern, self.text)

        # Criar um item para cada valor encontrado
        for i, amount_str in enumerate(amounts):
            amount = self._parse_currency(amount_str)
            if amount > 0:
                # Tentar associar com uma data próxima
                expected_date = date.today()
                if i < len(dates):
                    expected_date = self._parse_date(dates[i])

                # Extrair contexto ao redor do valor
                match = re.search(
                    rf".{{0,50}}{re.escape(amount_str)}.{{0,50}}", self.text
                )
                context = match.group(0) if match else f"Valor #{i + 1}"

                results.append(
                    ParsedIncome(
                        client_name="Importado do PDF",
                        description=context.strip(),
                        amount_cents=amount,
                        expected_date=expected_date,
                        raw_text=amount_str,
                    )
                )

        return results

    @staticmethod
    def _find_column_index(header: List[str], keywords: List[str]) -> int:
        """Encontra índice de coluna baseado em keywords"""
        for i, col in enumerate(header):
            if col and any(kw in col.lower() for kw in keywords):
                return i
        return -1

    @staticmethod
    def _parse_currency(value: str) -> int:
        """Converte string de valor para centavos"""
        if not value:
            return 0

        # Remove R$, espaços e caracteres não numéricos (exceto . e ,)
        clean = re.sub(r"[R$\s]", "", str(value))

        # Formato brasileiro: 1.234,56 -> 123456
        # Remove pontos de milhar e troca vírgula por ponto
        clean = clean.replace(".", "").replace(",", ".")

        try:
            return int(float(clean) * 100)
        except ValueError:
            return 0

    @staticmethod
    def _parse_date(value: str) -> date:
        """Converte string de data para date"""
        if not value:
            return date.today()

        value = value.strip()

        # Tentar dd/mm/yyyy
        match = re.match(r"(\d{2})/(\d{2})/(\d{4})", value)
        if match:
            try:
                return date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
            except ValueError:
                pass

        # Tentar dd-mm-yyyy
        match = re.match(r"(\d{2})-(\d{2})-(\d{4})", value)
        if match:
            try:
                return date(int(match.group(3)), int(match.group(2)), int(match.group(1)))
            except ValueError:
                pass

        # Tentar yyyy-mm-dd (ISO)
        match = re.match(r"(\d{4})-(\d{2})-(\d{2})", value)
        if match:
            try:
                return date(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except ValueError:
                pass

        return date.today()

    @staticmethod
    def _is_numeric(value: str) -> bool:
        """Verifica se uma string representa um valor numérico"""
        clean = re.sub(r"[R$\s.,]", "", value)
        return clean.isdigit()
