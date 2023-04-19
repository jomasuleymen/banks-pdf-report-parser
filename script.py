import datetime
import json

import pdfplumber

from kk_transliterate import translit


def write_to_file(data, file_name):
    with open(f'./reports/{file_name}', 'w', encoding="utf-8") as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


def get_date(date_str):
    try:
        date = datetime.datetime.strptime(date_str, '%d.%m.%y')
        return date
    except Exception:
        return None


def parse_sum(str_data):
    currency_index = str_data.find('₸')

    if currency_index != -1:
        str_data = str_data[:currency_index]
    else:
        return None

    str_data = str_data.replace(' ', '')
    str_data = str_data.replace(',', '.')
    return float(str_data)


def parse_name_to_eng(name):
    return translit(name)


def get_data_from_pdf(path_pdf):
    data = []

    with pdfplumber.open(path_pdf) as pdf:
        for page_data in pdf.pages:
            table = page_data.extract_table()
            for row in table:

                if len(row) != 4:
                    continue

                date = get_date(row[0])
                if not date:
                    continue

                sum = parse_sum(row[1])

                if not sum:
                    print('sum is None', row)
                    continue

                name_contragent = row[3]

                data.append({
                    'date': date,
                    'sum': sum,
                    'name': parse_name_to_eng(name_contragent)
                })

    return data


def parse_by_deposit_withdrawal(data):
    parsed_data = {
        'deposit': {},
        'withdrawal': {}
    }

    for row in data:
        end_point = 'deposit' if row['sum'] > 0 else 'withdrawal'

        end_point_obj = parsed_data[end_point]

        if row['name'] not in end_point_obj:
            end_point_obj[row['name']] = 0

        end_point_obj[row['name']] += row['sum']

    # sort parsed_data with value of sum
    for key in parsed_data:
        parsed_data[key] = dict(
            sorted(parsed_data[key].items(), key=lambda item: item[1], reverse=True))

    # prin sum of deposit and withdrawal
    print('deposit', sum(parsed_data['deposit'].values()))
    print('withdrawal', sum(parsed_data['withdrawal'].values()))

    write_to_file(parsed_data, 'report_by_deposit_withdrawal.json')


def parse_by_name(data):
    # make another parsed_data, but wit grouped by name and each name have grouped with deposit and withdrawal sum
    parsed_data = {}

    for row in data:
        end_point = 'deposit' if row['sum'] > 0 else 'withdrawal'
        name = row['name']

        if name not in parsed_data:
            parsed_data[name] = {
                'withdrawal': 0,
                'deposit': 0,
                'difference': 0,
                'count': 0
            }

        parsed_data[name][end_point] += row['sum']
        parsed_data[name]['difference'] = parsed_data[name]['deposit'] + \
            parsed_data[name]['withdrawal']
        parsed_data[name]['count'] += 1

    # sort parsed_data_2 with value of difference
    parsed_data = dict(sorted(parsed_data.items(),
                              key=lambda item: item[1]['difference'], reverse=True))

    write_to_file(parsed_data, 'report_by_name.json')


path_pdf = './data.pdf'

data = get_data_from_pdf(path_pdf)

parse_by_deposit_withdrawal(data)
parse_by_name(data)
