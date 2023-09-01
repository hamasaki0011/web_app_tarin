import csv

with open("copyNew_0.csv", 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        print(line)