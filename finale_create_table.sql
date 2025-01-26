-- Create the Geography table (Dimension)
CREATE TABLE Geography (
    country_code NVARCHAR(10) PRIMARY KEY, -- Primary Key
    country_name NVARCHAR(100),
    continent NVARCHAR(50)
);

-- Create the Date table (Dimension)
CREATE TABLE Date (
    date_id INT PRIMARY KEY, -- Primary Key
    day INT,
    month INT,
    quarter INT,
    year INT
);

-- Create the Financial table (Dimension)
CREATE TABLE Financial (
    financial_id INT PRIMARY KEY, -- Primary Key
    match_expenses DECIMAL(18, 2),
    revenue DECIMAL(18, 2),
    profit DECIMAL(18, 2)
);

-- Create the Tournament table (Dimension)
CREATE TABLE Tournament (
    tourney_id INT PRIMARY KEY, -- Primary Key
    tourney_name NVARCHAR(100),
    surface NVARCHAR(50),
    draw_size INT,
    tourney_level NVARCHAR(50),
    date_id INT, -- Foreign Key to Date table
    FOREIGN KEY (date_id) REFERENCES Date(date_id)
);

-- Create the Player table (Dimension)
CREATE TABLE Player (
    player_id INT PRIMARY KEY, -- Primary Key
    player_name NVARCHAR(100),
    player_hand NVARCHAR(10),
    country_code NVARCHAR(10), -- Foreign Key to Geography table
    FOREIGN KEY (country_code) REFERENCES Geography(country_code)
);

-- Create the Match table (Fact Table)
CREATE TABLE Match (
    match_id INT PRIMARY KEY, -- Primary Key
    tourney_id NVARCHAR(20),           -- Foreign Key to Tournament table
    financial_id INT,         -- Foreign Key to Financial table
    winner_id INT,            -- Foreign Key to Player table
    loser_id INT,             -- Foreign Key to Player table
    best_of INT,              -- Number of sets in the match
    spectator INT,            -- Number of spectators
    score NVARCHAR(50),       -- Match score
    round NVARCHAR(50),       -- Tournament round
    winner_age DECIMAL(5, 2), -- Winner's age
    loser_age DECIMAL(5, 2),  -- Loser's age
    FOREIGN KEY (tourney_id) REFERENCES Tournament(tourney_id),
    FOREIGN KEY (financial_id) REFERENCES Financial(financial_id),
    FOREIGN KEY (winner_id) REFERENCES Player(player_id),
    FOREIGN KEY (loser_id) REFERENCES Player(player_id)
);
