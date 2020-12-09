import csv


# utils for working with csv format


def load_from_csv(filename):
    with open(filename) as f:
        for element in csv.DictReader(f, delimiter=','):
            yield element
