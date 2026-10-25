import csv
import pathlib

class CSVreader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        if not self.file_path.is_file():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        with self.file_path.open(mode="r", newline="", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            if reader.fieldnames:
                raise ValueError(f"CSV file is empty or does not contain headers: {self.file_path}")
            if len(reader.fieldnames) != len(set(reader.fieldnames)):
                raise ValueError(f"CSV file contains duplicate column names: {self.file_path}")
            
            for row in reader:
                if None in row:
                    raise ValueError(f"Too many fields: {self.line_number}")
                yield row
                
if __name__ == "__main__":
    root_dir = pathlib.Path(__file__).resolve().parents[2]
    csv_path = root_dir / "dataset" / "deletion_requests.csv"

    for row in CSVreader(csv_path).read():
        print(row)