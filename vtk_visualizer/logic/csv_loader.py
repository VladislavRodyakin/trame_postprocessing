import csv, io

def load_csv_content(content):
    reader = csv.DictReader(io.StringIO(content), delimiter=';')
    data = [row for row in reader]
    headers = [{"text": k, "value": k} for k in data[0].keys()] if data else []
    return data, headers
