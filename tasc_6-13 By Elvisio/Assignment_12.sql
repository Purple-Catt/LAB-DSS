-- Create a temporary CTE (Common Table Expression) to compute rank points
WITH Match_Points AS (
    SELECT 
        m.match_id,
        m.winner_id,
        m.loser_id,
        m.round,

        -- Assigning Winner Rank Points
        CASE 
            WHEN m.round IN ('Final', 'F') THEN 2000
            WHEN m.round = 'SF' THEN 720
            WHEN m.round = 'QF' THEN 360
            WHEN m.round = 'R16' THEN 180
            WHEN m.round = 'R32' THEN 90
            WHEN m.round = 'R64' THEN 45
            WHEN m.round = 'R128' THEN 10
            WHEN m.round = 'Q1' THEN 30
            WHEN m.round = 'Q2' THEN 20
            WHEN m.round = 'Q3' THEN 15
            WHEN m.round = 'Q4' THEN 10
            WHEN m.round = 'RR' THEN 50
            WHEN m.round = 'PR' THEN 25
            WHEN m.round = 'BR' THEN 5
            WHEN m.round = 'ER' THEN 5
            WHEN m.round = 'CR' THEN 5
            ELSE 0
        END AS Winner_Points,

        -- Assigning Loser Rank Points
        CASE 
            WHEN m.round IN ('Final', 'F') THEN 1200
            WHEN m.round = 'SF' THEN 360
            WHEN m.round = 'QF' THEN 180
            WHEN m.round = 'R16' THEN 90
            WHEN m.round = 'R32' THEN 45
            WHEN m.round = 'R64' THEN 10
            WHEN m.round = 'R128' THEN 5
            WHEN m.round = 'Q1' THEN 15
            WHEN m.round = 'Q2' THEN 10
            WHEN m.round = 'Q3' THEN 7
            WHEN m.round = 'Q4' THEN 5
            WHEN m.round = 'RR' THEN 25
            WHEN m.round = 'PR' THEN 12
            WHEN m.round = 'BR' THEN 2
            WHEN m.round = 'ER' THEN 2
            WHEN m.round = 'CR' THEN 2
            ELSE 0
        END AS Loser_Points

    FROM Group_ID_10.Match m
)

-- Create the table and insert aggregated values in one step
SELECT 
    p.player_id AS Player_ID, 
    p.player_name AS Player_Name, 
    p.country_code AS Country_Code, -- Changed from loc_country to country_code
    SUM(mp.Winner_Points) AS Winner_Rank_Points,
    SUM(mp.Loser_Points) AS Loser_Rank_Points
INTO Group_ID_10.Assignment_12_Rank_Points  -- This creates the table automatically
FROM Match_Points mp
LEFT JOIN Group_ID_10.Player p ON mp.winner_id = p.player_id OR mp.loser_id = p.player_id
GROUP BY p.player_id, p.player_name, p.country_code;  -- Changed loc_country to country_code
