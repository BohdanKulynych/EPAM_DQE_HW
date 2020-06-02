import argparse
import csv
import os
from typing import List


def find_file(putdir: str) -> str:
    '''
    param putdir: path to directory with csv
    return: path to csv ,else program ends
    '''
    for dirroot, dirname, filenames in os.walk(putdir):
        for file in filenames:
            if '.csv' == os.path.splitext(file)[1]:
                return os.path.join(dirroot, file)

    print("CSV file wasn't found at this directory.")
    os._exit(0)


if __name__ == "__main__":
    # define our parsers (for compile out script in terminal
    parser = argparse.ArgumentParser(
        description='Enter path to directory where desire file is located after -path parameter')
    parser.add_argument('-path', type=str, help='Enter a path to the directory', required=True)
    parser.add_argument('-bed', type=int, help='Enter a number of beds ', default=1)
    args = parser.parse_args()
    # open csv file in read mode
    with open(find_file(args.path), 'r') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader)  # row 1 of input file
        description = next(reader)  # row 2 of input file ,do it for no trouble reading necessary data
        detailed_rows: List[str] = []  # will contain old rows + free beds percent and written to new file
        for row in reader:
            # calculate free_beds metric,use headers.index(row[name]) because it's more readable
            free_beds: List[float] = [(int((row[headers.index('Available Hospital Beds')].replace(',', ''))) /
                                       int((row[headers.index('Total Hospital Beds')].replace(',', ''))) * 100)]
            # append percent to old rows and deleting 1st element of free_beds element after every itteration
            for i in range(len(free_beds)):
                detailed_rows.append(row + ["%.1f" % free_beds[i] + '%'])
            del free_beds[:i + 1]

    # write detailed_rows to new csv and add to headers the name of new col
    with open('output.csv', 'w', newline='') as file1:
        writer = csv.writer(file1, delimiter=',')
        writer.writerow(headers + ['Free beds'])
        writer.writerow(description)
        writer.writerows(detailed_rows)
    # read this csv
    with open('output.csv', 'r') as output_file:
        reader = csv.reader(output_file)
        headers = next(reader)
        description = next(reader)
        # sort csv by Free beds
        sorted_list: List[str] = sorted(reader, key=lambda row: row[headers.index('Free beds')], reverse=True)
        # check not correct values
        if args.bed > len(detailed_rows) or args.bed < 1:
            print("Incorrect quantity of bed.Try to enter a digit in range(1,"f'{len(detailed_rows)}')
            os._exit(0)
        # print user defined quantity of HRR's and free bed percent
        [print(f'{sorted_list[i][0], sorted_list[i][-1]}') for i in range(args.bed)]
