# code/ingestion/media.py
import json
import pathlib

class UnstructuredReader:
    def __init__(self, file_path: pathlib.Path, file_type: str):
        self.file_path = pathlib.Path(file_path)
        self.file_type = file_type.lower()

    def read_items(self):
        if not self.file_path.is_file():
            raise FileNotFoundError(f"Source file not found: {self.file_path}")
        
        if self.file_type == "json":
            with self.file_path.open("r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            yield item
                    else:
                        raise ValueError(f"Expected a list of items in JSON file: {self.file_path}")
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON format in file {self.file_path}: {e}")
        
        elif self.file_type == "txt" or self.file_type == "log":
            with self.file_path.open("r", encoding="utf-8") as f:
                for line in f:
                    yield line.strip()
            
        elif self.file_type == "csv":
            from ingestion.loader import CSVreader
            csv_reader = CSVreader(self.file_path)
            for row in csv_reader.read():
                yield row
        
        elif self.file_type == "sql":
            with self.file_path.open("r", encoding="utf-8") as f:
                sql_content = f.read()
                yield {"sql": sql_content}
        
        elif self.file_type == "png":
            with self.file_path.open("rb") as f:
                image_data = f.read()
                yield {"image_data": image_data}
                
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}. Only .json, .txt, .log, .csv, and .sql files are supported.")