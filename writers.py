import json
import os
from datetime import datetime


class DataTypeNotSuportedForIngestionException(Exception):
    def __init__(self, data):
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion!"
        super().__init__(self.message)


class DataWriter:
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.file_name = f'{self.api}/{self.coin}/{datetime.datetime.now()}.json'.replace(':', '-')

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
        with open(self.file_name, 'a') as f:
            f.write(row)

    def write(self, data: [list, dict]):
        if isinstance(data, dict):  # Se o "Data" for do tipo Dicionário
            self._write_row(f'{json.dumps(data)},\n')
        elif isinstance(data, list):
            for item in data:
                self._write_row(f'{item},\n')
        else:
            raise DataTypeNotSuportedForIngestionException(data)
