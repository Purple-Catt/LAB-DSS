DROP TABLE IF EXISTS Match;
DROP TABLE IF EXISTS Tournament;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Geography;
DROP TABLE IF EXISTS Date;

-- Creating the 'date' table
CREATE TABLE Date (
    date_id INT PRIMARY KEY,
    day INT,
    month INT,
    year INT,
    quarter INT
);

-- Creating the 'geography' table
CREATE TABLE Geography (
    country_code VARCHAR(10) PRIMARY KEY,
    country_name VARCHAR(100),
    continent VARCHAR(50)
);

-- Creating the 'player' table (Without FK)
CREATE TABLE Player (
    player_id VARCHAR(10) PRIMARY KEY,
    player_name VARCHAR(100),
    player_hand VARCHAR(10),  -- Left/Right-handed
    player_age FLOAT,
    country_code VARCHAR(10)  -- Will add FK later
);

-- Creating the 'tournament' table (Without FK)
CREATE TABLE Tournament (
    tourney_id VARCHAR(50) PRIMARY KEY,
    tourney_name VARCHAR(200),
    surface VARCHAR(50),        -- Type of court (Hard, Clay, Grass)
    draw_size VARCHAR(50),      -- Number of players in the draw
    tourney_level VARCHAR(10),  -- Tournament level (ATP, Grand Slam, etc.)
    date_id INT                 -- Will add FK later
);

-- Creating the 'match' fact table (Without FK)
CREATE TABLE Match (
    match_id INT PRIMARY KEY,
    tourney_id VARCHAR(50),
    winner_id VARCHAR(10),
    loser_id VARCHAR(10),
    best_of INT,  -- Best of 3 or 5 sets
    spectator VARCHAR(10),  -- Number of spectators
    score VARCHAR(50),
    round VARCHAR(50),  -- Match round (Final, Semi, etc.)
    match_expenses DECIMAL(15,2),
    revenue DECIMAL(15,2),
    profit DECIMAL(15,2)
);
-- Adding FK to Player (Linking to Geography)
ALTER TABLE Player 
ADD CONSTRAINT FK_Player_Geography FOREIGN KEY (country_code) 
REFERENCES Geography(country_code);

-- Adding FK to Tournament (Linking to Date)
ALTER TABLE Tournament 
ADD CONSTRAINT FK_Tournament_Date FOREIGN KEY (date_id) 
REFERENCES Date(date_id);

-- Adding FK to Match (Linking to Tournament)
ALTER TABLE Match 
ADD CONSTRAINT FK_Match_Tournament FOREIGN KEY (tourney_id) 
REFERENCES Tournament(tourney_id);

-- Adding FK to Match (Linking to Player - Winner)
ALTER TABLE Match 
ADD CONSTRAINT FK_Match_Winner FOREIGN KEY (winner_id) 
REFERENCES Player(player_id);

-- Adding FK to Match (Linking to Player - Loser)
ALTER TABLE Match 
ADD CONSTRAINT FK_Match_Loser FOREIGN KEY (loser_id) 
REFERENCES Player(player_id);
