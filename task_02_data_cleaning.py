import csv
from datetime import datetime, timedelta
from ioc_countries import ioc_countries

columns_to_drop = ['winner_seed', 'winner_entry', 'winner_ht', 'loser_seed', 'loser_entry', 'loser_ht', 'minutes',
                   'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpSaved', 'w_bpFaced',
                   'l_ace', 'l_df', 'l_svpt', 'l_1stIn', 'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced',
                   'winner_rank', 'winner_rank_points', 'loser_rank', 'loser_rank_points']
'''
winner_age, winner_hand, loser_age, loser_hand will be substituted with the median
Drop winner and loser ioc, score
'''
fact_dict_stats = {'winner_age': [], 'winner_hand': {'A': 0, 'U': 0, 'L': 0, 'R': 0},
                   'loser_age': [], 'loser_hand': {'A': 0, 'U': 0, 'L': 0, 'R': 0}}
ioc_set = set()

with open('Data\\fact.csv', newline='') as file:
    reader = csv.reader(file)
    var = True
    for row in reader:
        if var:
            var = False
            col_idx_fact = dict()
            col_idx_to_drop = list()
            for k, v in enumerate(row):
                col_idx_fact[v] = k
                if v in columns_to_drop:
                    col_idx_to_drop.append(k)
            continue

        for k in fact_dict_stats.keys():
            if k in ['winner_age', 'loser_age']:
                try:
                    fact_dict_stats[k].append(float(row[col_idx_fact[k]]))
                except ValueError:
                    pass

            else:
                value = row[col_idx_fact[k]]
                if value != '':
                    fact_dict_stats[k][value] += 1

# Compute the average for numerical values, mode for categorical ones
for k in fact_dict_stats.keys():
    if k in ['winner_age', 'loser_age']:
        fact_dict_stats[k] = round(sum(fact_dict_stats[k]) / len(fact_dict_stats[k]), 1)

    else:
        fact_dict_stats[k] = sorted(fact_dict_stats[k].items(), key=lambda x: x[1], reverse=True)[0][0]


with open('Data\\fact.csv', newline='') as r_file:
    with open('Data\\fact_cleaned.csv', newline='', mode='w') as w_file:
        reader = csv.reader(r_file)
        writer = csv.writer(w_file)
        var = True
        for row in reader:
            if var:
                var = False
                for idx in reversed(col_idx_to_drop):
                    row.pop(idx)
                writer.writerow(row)
                continue

            for k in fact_dict_stats.keys():
                if row[col_idx_fact[k]] == '':
                    row[col_idx_fact[k]] = fact_dict_stats[k]

            if (row[col_idx_fact['loser_ioc']] == '' or
                    row[col_idx_fact['score']] == '' or
                    row[col_idx_fact['winner_ioc']] == ''):
                continue

            ioc_set.add(row[col_idx_fact['winner_ioc']])
            ioc_set.add(row[col_idx_fact['loser_ioc']])
            for idx in reversed(col_idx_to_drop):
                row.pop(idx)

            writer.writerow(row)

with open('Data\\tourney.csv', newline='') as r_file:
    with open('Data\\tourney_cleaned.csv', newline='', mode='w') as w_file:
        reader = csv.reader(r_file)
        writer = csv.writer(w_file)
        var = True
        unique_set = set()
        for row in reader:
            if var:
                var = False
                col_idx_tourney = dict()
                for k, v in enumerate(row):
                    col_idx_tourney[v] = k

                row.pop(-1)
                row.append('day')
                row.append('month')
                row.append('year')
                row.append('quarter')
                writer.writerow(row)
                continue

            if tuple(row) not in unique_set:
                unique_set.add(tuple(row))

            else:
                continue

            if row[col_idx_tourney['surface']] == '':
                row[col_idx_tourney['surface']] = 'Clay'

            if row[col_idx_tourney['draw_size']] == '':
                row[col_idx_tourney['draw_size']] = 32

            else:
                row[col_idx_tourney['draw_size']] = row[col_idx_tourney['draw_size']].removesuffix('.0')

            dt = datetime(1970, 1, 1) + timedelta(
                seconds=int(row.pop(col_idx_tourney['tourney_timestamp'])))
            row.append(str(dt.day))
            row.append(str(dt.month))
            row.append(str(dt.year))
            if dt.month <= 4:
                quarter = '1'
            elif dt.month <= 8:
                quarter = '2'
            else:
                quarter = '3'
            row.append(quarter)

            writer.writerow(row)

with (open('Data\\countries.csv', newline='') as r_file,
      open('Data\\countries_cleaned.csv', newline='', mode='w') as w_file,
      open('alpha3countries.csv', newline='') as alpha3_file):
    reader = csv.reader(r_file)
    writer = csv.writer(w_file)
    alpha3_reader = csv.reader(alpha3_file)
    alpha3_countries = dict()
    var = True
    for row in reader:
        if var:
            var = False
            writer.writerow(row)

        if row[0] in ioc_set:
            ioc_set.remove(row[0])

        writer.writerow(row)

    for row in alpha3_reader:
        alpha3_countries[row[1]] = {'name': row[0], 'continent': row[2]}

    for c in ioc_set:
        try:
            code = ioc_countries[c]['alpha_3']
        except KeyError:
            code = c
        new_row = [c, alpha3_countries[code]['name'], alpha3_countries[code]['continent']]
        writer.writerow(new_row)
