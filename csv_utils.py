import csv

WRITE_TO = "results/result.csv"


# utils for working with csv format
def get_data(filename):
    with open(filename) as f:
        for row in csv.reader(f):
            yield row[0].lower()


def get_dict_data(filename):
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=',')
        return {line["Asin"]: line["Title"] for line in reader}


def get_dict_data_2(filename):
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter=',')
        return {line["Title"]: (line["Asin"], line["Review"]) for line in reader}



