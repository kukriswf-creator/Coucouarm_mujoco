# coucouarm/utils/csv_logger.py

import os
import csv


class CsvLogger:
    def __init__(self, log_path, header):
        self.log_path = log_path
        self.header = header
        self.rows = []

    def append(self, row):
        self.rows.append(row)

    def save(self):
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

        with open(self.log_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(self.header)
            writer.writerows(self.rows)

        print("Log saved to:", self.log_path)