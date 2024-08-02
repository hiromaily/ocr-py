import re


class JapaneseTextExtractor:
    def __init__(self, text):
        self.text = text

    def search(self, pattern):
        match = re.search(pattern, self.text)
        if match:
            return match.group(1).strip()
        return None

    def name(self):
        pattern = r"氏名\s+(.+?)\s+(?!\S)"
        return self.search(pattern)

    def expiration_date(self):
        pattern = r"有効期限\s+([^\s]+)"
        return self.search(pattern)

    def sign(self):
        pattern = r"記号\s+([^\s]+)\s+番号"
        return self.search(pattern)

    def number(self):
        pattern = r"番号\s+(\d+)"
        return self.search(pattern)
