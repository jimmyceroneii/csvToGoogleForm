import csv

def parse_csv(file_path):
    data = []

    with open(file_path, mode='r') as csvFile:
        for row in csvFile:
            data.append(row.strip())

    return data