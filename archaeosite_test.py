import json
import csv

def lambda_handler():

    with open('as.csv', 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        # print(data)
        for row in data:
            print(row)

if __name__ == '__main__':
    lambda_handler()
