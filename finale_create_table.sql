CREATE TABLE Date (
    date_id INT PRIMARY KEY,
    day INT,
    month INT,
    quarter INT,
    year INT
);

CREATE TABLE Geography (
    country_code VARCHAR(3) PRIMARY KEY,
    country_name VARCHAR(255),
    continent VARCHAR(255)
);

CREATE TABLE Player (
    player_id VARCHAR(50) PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    player_hand CHAR(1),
    loc_country VARCHAR(3) REFERENCES Geography(country_code)
);

CREATE TABLE Financial (
    financial_id INT PRIMARY KEY,
    match_expenses FLOAT,
    revenue FLOAT,
    profit FLOAT
);

CREATE TABLE Tournament (
    tourney_id VARCHAR(50) PRIMARY KEY,
    tourney_name VARCHAR(255),
    surface VARCHAR(50),
    draw_size VARCHAR(50),
    tourney_level VARCHAR(50),
    date_id INT REFERENCES Date(date_id)
);

CREATE TABLE Match (
    match_id VARCHAR(50) PRIMARY KEY,
    tourney_id VARCHAR(50) REFERENCES Tournament(tourney_id),
    financial_id INT REFERENCES Financial(financial_id),
    winner_id VARCHAR(50) REFERENCES Player(player_id),
    loser_id VARCHAR(50) REFERENCES Player(player_id),
    best_of INT,
    spectator INT,
    score VARCHAR(255),
    round VARCHAR(50),
    match_expenses FLOAT,
    revenue FLOAT,
    profit FLOAT,
    winner_age FLOAT,
    loser_age FLOAT
);
