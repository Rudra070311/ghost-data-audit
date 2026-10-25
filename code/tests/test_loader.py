import pytest
from ingestion.loader import CSVreader

def test_csv_reader_valid(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("email,account_id\ntest@test.com,acc_1\n", encoding="utf-8")
    reader = CSVreader(csv_file)
    rows = list(reader.read())
    assert len(rows) == 1
    assert rows[0]["email"] == "test@test.com"

def test_csv_reader_empty(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("", encoding="utf-8")
    reader = CSVreader(csv_file)
    with pytest.raises(ValueError):
        list(reader.read())

def test_csv_reader_duplicate_headers(tmp_path):
    csv_file = tmp_path / "dup.csv"
    csv_file.write_text("email,email\ntest@test.com,test@test.com\n", encoding="utf-8")
    reader = CSVreader(csv_file)
    with pytest.raises(ValueError):
        list(reader.read())