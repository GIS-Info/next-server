import csv

def parse_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader if row['Modification'] == '1']