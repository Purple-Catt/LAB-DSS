import csv
from math import floor

match_path = 'Data\\DW\\match.csv'
player_path = 'Data\\DW\\player.csv'
tournament_path = 'Data\\DW\\tournament.csv'
date_path = 'Data\\DW\\date.csv'
geography_path = 'Data\\DW\\geography.csv'

match_ssis_path = 'Data\\DW\\match_ssis.csv'
player_ssis_path = 'Data\\DW\\player_ssis.csv'
tournament_ssis_path = 'Data\\DW\\tournament_ssis.csv'
date_ssis_path = 'Data\\DW\\date_ssis.csv'
geography_ssis_path = 'Data\\DW\\geography_ssis.csv'

with open(match_path, newline='') as file:
    match_len = len(file.readlines())

with open(match_path, newline='') as match_file:
    tourney_ids = set()
    player_ids = set()
    match_ssis_file = open(match_ssis_path, 'w', newline='')
    match_ssis_writer = csv.writer(match_ssis_file)
    reader = csv.reader(match_file)

    limit = floor(match_len * 0.2)
    row_number = 0
    var = True
    for row in reader:
        if row_number < limit:
            row_number += 1
            match_ssis_writer.writerow(row)
            if not var:
                tourney_ids.add(row[1])
                player_ids.add(row[2])
                player_ids.add(row[3])
            var = False

        else:
            break

    match_ssis_file.close()

with open(tournament_path, newline='') as tournament_file:
    date_ids = set()
    tournament_ssis_file = open(tournament_ssis_path, 'w', newline='')
    tournament_ssis_writer = csv.writer(tournament_ssis_file)
    reader = csv.reader(tournament_file)
    var = True
    for row in reader:
        if var:
            tournament_ssis_writer.writerow(row)
            var = False
            continue

        if row[0] in tourney_ids:
            tournament_ssis_writer.writerow(row)
            date_ids.add(row[5])

    tournament_ssis_file.close()

with open(player_path, newline='') as player_file:
    geography_ids = set()
    player_ssis_file = open(player_ssis_path, 'w', newline='')
    player_ssis_writer = csv.writer(player_ssis_file)
    reader = csv.reader(player_file)
    var = True
    for row in reader:
        if var:
            var = False
            player_ssis_writer.writerow(row)
            continue

        if row[0] in player_ids:
            player_ssis_writer.writerow(row)
            geography_ids.add(row[3])

    player_ssis_file.close()

with open(date_path, newline='') as date_file:
    date_ssis_file = open(date_ssis_path, 'w', newline='')
    date_ssis_writer = csv.writer(date_ssis_file)
    reader = csv.reader(date_file)
    var = True
    for row in reader:
        if var:
            var = False
            date_ssis_writer.writerow(row)
            continue

        if row[0] in date_ids:
            date_ssis_writer.writerow(row)

    date_ssis_file.close()

with open(geography_path, newline='') as geography_file:
    geography_ssis_file = open(geography_ssis_path, 'w', newline='')
    geography_ssis_writer = csv.writer(geography_ssis_file)
    reader = csv.reader(geography_file)
    var = True
    for row in reader:
        if var:
            var = False
            geography_ssis_writer.writerow(row)
            continue

        if row[0] in geography_ids:
            geography_ssis_writer.writerow(row)

    geography_ssis_file.close()
