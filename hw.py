import csv
import calendar
import os
from datetime import datetime
from dictionaries import category_dict


def main():
    file_path = input('file path: ') or 'data.CSV'
    year = input('year: ') or 2019
    month = input('month: ') or 6
    new_file_path= f'{year}-{month}.csv'
    if not os.path.exists(new_file_path):
        create_new_file(int(year), int(month))
    card_column = input('which card? 1. saving account, 2. checking account, 3. credit card 1, 4. credit card: ') or 3
    handle_file(file_path, new_file_path, int(card_column))


def handle_file(file_path, new_file_path, card_column):
    if file_path == '':
        file_path = 'data.CSV'
    with open(file_path) as data_file:
        data_reader = csv.reader(data_file)
        data_rows = list(data_reader)

    with open(new_file_path) as new_file:
        new_file_reader = csv.reader(new_file)
        new_rows = list(new_file_reader)

    filled_rows = []
    for new_row in new_rows:
        for data_row in data_rows:
            new_row = handle_row(new_row, data_row, card_column)
        filled_rows.append(new_row)

    with open(new_file_path, 'w') as new_file:
        new_file_writer = csv.writer(new_file)
        new_file_writer.writerows(new_rows)

    print(f'file is generated at {new_file_path}')
    print_file(new_file_path)


def handle_row(new_row, data_row, card_column):
    if data_row[0] == 'Transaction Date':
        return new_row

    [_, post_date, _, category, _, amount] = data_row

    data_date = datetime.strftime(datetime.strptime(post_date, '%m/%d/%Y'), '%Y-%m-%d')
    new_date = new_row[0]
    if data_date == new_date:
        # column number depends on data type(credit card 1, 2 , etc)
        new_row = add_to_column(new_row, card_column, amount)
        if category in category_dict:
            new_row = add_to_column(new_row, category_dict[category], amount)
    return new_row


def add_to_column(new_row, column_index, amount):
    real_amount = abs(float(amount))
    if new_row[column_index] is '':
        new_row[column_index] = real_amount
    else:
        new_row[column_index] = float(new_row[column_index]) + real_amount
    return new_row


def create_new_file(year, month):
    cal = calendar.Calendar()
    new_file_name = f'{year}-{month}.csv'
    with open(new_file_name, 'w') as new_file:
        spam_writer = csv.writer(new_file)
        for date in cal.itermonthdates(year, month):
            if date.month == month:
                row = [None] * 21
                row[0] = date
                spam_writer.writerow(row)


def print_file(file_path):
    with open(file_path) as csv_file:
        spam_reader = csv.reader(csv_file)
        for row in spam_reader:
            print(row)


if __name__ == "__main__":
    main()


