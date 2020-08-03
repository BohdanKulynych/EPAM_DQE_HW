import csv

with open('datasets_645767_1144553_HRR Scorecard_ 20 _ 40 _ 60 - 20 Population.csv', 'r') as file:
    data_list = []
    reader = csv.reader(file)
    header = next(reader)
    description = next(reader)
    # append data to list
    for data in reader:
        data_list.append(data)
    # calculate hrr
    free_beds = [f"{'%.1f' % (int(data_list[i][3].replace(',', '')) / int(data_list[i][1].replace(',', '')) * 100)}%"
                 for i in range(len(data_list))]
    # get locations
    locations = [data_list[i][0] for i in range(len(data_list))]
    # create dict location - hrr
    beds_hrr = dict(zip(locations, free_beds))
    # sort it
    beds_hrr = sorted(beds_hrr.items(), key=lambda x: float(x[-1].strip('%')), reverse=True)
    
