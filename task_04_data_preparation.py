import csv

fact_path = 'Data\\fact_cleaned.csv'
tourney_path = 'Data\\tourney_cleaned.csv'
countries_path = 'Data\\countries.csv'

match_path = 'Data\\DW\\match.csv'
player_path = 'Data\\DW\\player.csv'
tournament_path = 'Data\\DW\\tournament.csv'
date_path = 'Data\\DW\\date.csv'

# Create match, player and financial tables
with open(fact_path, newline='') as fact_file:
    reader = csv.reader(fact_file)
    tourney_file = open(tourney_path, newline='')
    tourney_reader = csv.reader(tourney_file)
    tourney_id_dict = dict()
    var = True
    for row in tourney_reader:
        if var:
            var = False
            continue
        tourney_id_dict[row[0]] = row[1]

    match_file = open(match_path, newline='', mode='w')
    player_file = open(player_path, newline='', mode='w')

    match_writer = csv.writer(match_file)
    player_writer = csv.writer(player_file)
    var = True
    match_id = 1
    unique_players = set()
    for row in reader:
        match_row = list()
        player_row = list()
        if var:
            var = False
            col_idx_fact = dict()
            for k, v in enumerate(row):
                col_idx_fact[v] = k

            match_writer.writerow(['match_id', 'tourney_id', 'winner_id', 'loser_id', 'score', 'round',
                                   'best_of', 'spectator', 'match_expenses', 'revenue',
                                   'profit', 'winner_age', 'loser_age'])
            player_writer.writerow(['player_id', 'player_name', 'player_hand', 'country_code'])
            continue

        match_row.append(str(match_id))
        match_row.append(tourney_id_dict[row[col_idx_fact['tourney']]])
        match_row.append(row[col_idx_fact['winner_id']])
        match_row.append(row[col_idx_fact['loser_id']])
        match_row.append(row[col_idx_fact['score']])
        match_row.append(row[col_idx_fact['round']])
        match_row.append(row[col_idx_fact['best_of']])
        match_row.append(row[col_idx_fact['spectator']].removesuffix('.0'))
        match_row.append(row[col_idx_fact['match_expenses']])
        revenue = float(row[col_idx_fact['avg_ticket_price']]) * float(row[col_idx_fact['spectator']])
        profit = revenue - float(row[col_idx_fact['match_expenses']])
        match_row.append(str(round(revenue, 2)))
        match_row.append(str(round(profit, 2)))
        match_row.append(row[col_idx_fact['winner_age']])
        match_row.append(row[col_idx_fact['loser_age']])
        match_writer.writerow(match_row)
        match_id += 1

        if row[col_idx_fact['winner_id']] not in unique_players:
            unique_players.add(row[col_idx_fact['winner_id']])
            player_row.append(row[col_idx_fact['winner_id']])
            player_row.append(row[col_idx_fact['winner_name']])
            player_row.append(row[col_idx_fact['winner_hand']])
            player_row.append(row[col_idx_fact['winner_ioc']])
            player_writer.writerow(player_row)
            player_row = list()

        if row[col_idx_fact['loser_id']] not in unique_players:
            unique_players.add(row[col_idx_fact['loser_id']])
            player_row.append(row[col_idx_fact['loser_id']])
            player_row.append(row[col_idx_fact['loser_name']])
            player_row.append(row[col_idx_fact['loser_hand']])
            player_row.append(row[col_idx_fact['loser_ioc']])
            player_writer.writerow(player_row)

    tourney_file.close()
    match_file.close()
    player_file.close()

# Create tournament and date tables
with open(tourney_path, newline='') as tourney_file:
    reader = csv.reader(tourney_file)
    tournament_file = open(tournament_path, newline='', mode='w')
    date_file = open(date_path, newline='', mode='w')

    tournament_writer = csv.writer(tournament_file)
    date_writer = csv.writer(date_file)
    var = True
    date_id = 1
    unique_dates = dict()
    for row in reader:
        tournament_row = list()
        date_row = list()
        if var:
            var = False
            col_idx_tourney = dict()
            for k, v in enumerate(row):
                col_idx_tourney[v] = k

            tournament_writer.writerow(['tourney_id', 'tourney_name', 'surface',
                                        'draw_size', 'tourney_level', 'date_id'])
            date_writer.writerow(['date_id', 'day', 'month', 'year', 'quarter'])
            continue

        date = row[col_idx_tourney['day']:]
        if ''.join(date) not in unique_dates.keys():
            unique_dates[''.join(date)] = str(date_id)
            date_row.append(str(date_id))
            date_row.extend(date)
            date_id += 1
            date_writer.writerow(date_row)

        tournament_row.append(row[col_idx_tourney['tourney_id']])
        tournament_row.append(row[col_idx_tourney['tourney_name']])
        tournament_row.append(row[col_idx_tourney['surface']])
        tournament_row.append(row[col_idx_tourney['draw_size']])
        tournament_row.append(row[col_idx_tourney['tourney_level']])
        tournament_row.append(unique_dates[''.join(date)])
        tournament_writer.writerow(tournament_row)

    tournament_file.close()
    date_file.close()
