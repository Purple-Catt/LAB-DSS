import csv
import pyodbc

match_path ='Data\\DW\\match_ssis.csv'
player_path ='Data\\DW\\player_ssis.csv'
tournament_path ='Data\\DW\\tournament_ssis.csv'
date_path = 'Data\\DW\\date_ssis.csv'
geography_path = 'Data\\DW\\geography_ssis.csv'
params = ('DRIVER={ODBC Driver 17 for SQL Server};'
          'SERVER=tcp:lds.di.unipi.it;'
          'DATABASE=Group_ID_10_DB;'
          'UID=Group_ID_10;'
          'PWD=FRU5YM7A')

with pyodbc.connect(params) as conn:
    with open(date_path, newline='') as date_file:
        cursor = conn.cursor()
        reader = csv.reader(date_file)
        var = True
        for row in reader:
            if var:
                var = False
                continue
            date_id = int(row[0])
            day = int(row[1])
            month = int(row[2])
            year = int(row[3])
            quarter = int(row[4])

            cursor.execute('INSERT INTO Date_SSIS_python VALUES (?, ?, ?, ?, ?)',
                           date_id, day, month, quarter, year)

        cursor.commit()
        cursor.close()

    with open(geography_path, newline='') as geography_file:
        cursor = conn.cursor()
        reader = csv.reader(geography_file)
        var = True
        for row in reader:
            if var:
                var = False
                continue
            country_code = row[0]
            country_name = row[1]
            continent = row[2]

            cursor.execute('INSERT INTO Geography_SSIS_python VALUES (?, ?, ?)',
                           country_code, country_name, continent)

        cursor.commit()
        cursor.close()

    with open(player_path, newline='') as player_file:
        cursor = conn.cursor()
        reader = csv.reader(player_file)
        var = True
        for row in reader:
            if var:
                var = False
                continue
            player_id = int(row[0])
            player_name = row[1]
            player_hand = row[2]
            country_code = row[4]
            cursor.execute('INSERT INTO Player_SSIS_python VALUES (?, ?, ?, ?)',
                           player_id, player_name, player_hand, country_code)

        cursor.commit()
        cursor.close()

    with open(tournament_path, newline='') as tournament_file:
        cursor = conn.cursor()
        reader = csv.reader(tournament_file)
        var = True
        for row in reader:
            if var:
                var = False
                continue
            tourney_id = row[0]
            tourney_name = row[1]
            surface = row[2]
            draw_size = int(row[3])
            tourney_level = row[4]
            date_id = int(row[5])

            cursor.execute('INSERT INTO Tournament_SSIS_python VALUES (?, ?, ?, ?, ?, ?)',
                           tourney_id, tourney_name, surface, draw_size, tourney_level, date_id)

        cursor.commit()
        cursor.close()

    with open(match_path, newline='') as match_file:
        cursor = conn.cursor()
        reader = csv.reader(match_file)
        var = True
        for row in reader:
            if var:
                var = False
                continue
            match_id = int(row[0])
            tournament_id = row[1]
            winner_id = int(row[2])
            loser_id = int(row[3])
            financial_id = int(row[4])
            score = row[5]
            roundd = row[6]
            best_of = int(row[7])
            spectator = int(row[8])
            match_expenses = float(row[9])
            revenue = float(row[10])
            profit = float(row[11])
            winner_age = float(row[12])
            loser_age = float(row[13])

            cursor.execute('INSERT INTO Match_SSIS_python VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                           match_id, tournament_id, financial_id, winner_id, loser_id, best_of,
                           spectator, score, roundd, match_expenses, revenue, profit, winner_age, loser_age)

        cursor.commit()
        cursor.close()
