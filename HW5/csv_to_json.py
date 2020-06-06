import argparse
import os
import csv
import json
from typing import List
from pprint import pprint


# in cmd execute by this expression: python csv_to_json.py -csv "path"

# parser for execute script in command line
def get_args():
    parser = argparse.ArgumentParser(description='Add filepath to file to read from.')  # add arguments
    parser.add_argument('-csv', type=str, help='path to file needed to read')
    return parser.parse_args()


# find csv file into directory and return path to it
def find_file(putdir: str) -> str:
    for dirroot, dirname, filenames in os.walk(putdir):
        for file in filenames:
            if '.csv' == os.path.splitext(file)[1]:
                return os.path.join(dirroot, file)
        else:
            print("CSV file wasn't found at this directory.")
            quit()


def get_data(csv_file: str) -> List:
    '''

    :param csv_file: path to csv from find_file()
    :return: list of dicts without password column
    '''
    users_data: List = []
    with open(csv_file) as file:
        reader = csv.DictReader(file)
        for line in reader:
            del (line['password'])
            users_data.append(line)
        return users_data


def write_json(data: List) -> str:
    '''

    :param data: data for writing into json
    :return: path to created json file with user data
    '''
    filename = 'user_details.json'
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        path = (str(os.path.dirname(os.path.abspath(filename)))) + "/" + filename
    return path


# print data from json
def read_json(path_to_json: str):
    with open(path_to_json, 'r') as json_file:
        pprint(json.load(json_file))


if __name__ == "__main__":

    path_to_csv = find_file(get_args().csv)

    data = get_data(path_to_csv)

    read_json(write_json(data))
