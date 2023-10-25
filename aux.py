import re
from datetime import datetime

class Aux:
    @staticmethod
    def formatar_data(data):
        # Verifique o formato "23/10/2023"
        if re.match(r"\d{2}/\d{2}/\d{4}", data):
            # Use o formato "DD/MM/YYYY"
            return datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d")
        else:
            # Use o formato "Tue, 01 Jul 1997 00:00:00 GMT"
            return datetime.strptime(data, "%a, %d %b %Y %H:%M:%S GMT").strftime("%Y-%m-%d")
