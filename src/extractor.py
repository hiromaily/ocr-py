import re

# implement extract and validate


class JapaneseTextExtractor:
    def __init__(self, text):
        self.text = text

    def search(self, pattern):
        match = re.search(pattern, self.text)
        if match:
            return match.group(1).strip()
        return None

    def search_two_words(self, pattern):
        match = re.search(pattern, self.text)
        if match:
            address_part1 = match.group(1).strip()
            address_part2 = match.group(2).strip()
            return address_part1 + address_part2
        return None

    def name(self):
        pattern = r"氏名\s+(.+?)\s+(?!\S)"
        result = self.search(pattern)
        if result is None:
            pattern = r"氏名\s+(.+)"
            return self.search(pattern)
        return result

    def expiration_date(self):
        pattern = r"有効期限\s+([^\s]+)"
        return self.search(pattern)

    def sign(self):
        pattern = r"記号\s+([^\s]+)\s+番号"
        result = self.search(pattern)
        if result is None:
            pattern = r"記号\s+(\d+一\d+)"
            return self.search(pattern)
        return result

    def number(self):
        pattern = r"番号\s+(\d+)"
        return self.search(pattern)

    def birth_day(self):
        pattern = r"生年月日\s+(.+?)\s+[^\s]"
        return self.search(pattern)

    def sex(self):
        pattern = r"性別\s+([男女])\s+"
        return self.search(pattern)

    def qualified_day(self):
        pattern = r"資格取得年月日\s+(.+?)\s+[^\s]"
        return self.search(pattern)

    def issued_day(self):
        pattern = r"交付年月日\s*[。]?\s*(令和\d+年\d+月\d+日)"
        return self.search(pattern)

    def address(self):
        pattern = r"住所\s+(.+?)\s*\n\s*(.+)"
        return self.search_two_words(pattern)

    def insurer_number(self):
        pattern = r"保険者番号\s+(\d+)"
        return self.search(pattern)
