WITH home_results AS (

    SELECT
        match_id,
        match_date,
        home_team AS team,
        away_team AS opponent,
        'HOME' AS venue,
        home_score AS goals_for,
        away_score AS goals_against,
        CASE
            WHEN home_score > away_score THEN 'WIN'
            WHEN home_score < away_score THEN 'LOSS'
            ELSE 'DRAW'
        END AS result,
        CASE
            WHEN home_score > away_score THEN 3
            WHEN home_score = away_score THEN 1
            ELSE 0
        END AS points

    FROM {{ ref('stg_matches') }}
    WHERE status = 'FINISHED'

),

away_results AS (

    SELECT
        match_id,
        match_date,
        away_team AS team,
        home_team AS opponent,
        'AWAY' AS venue,
        away_score AS goals_for,
        home_score AS goals_against,
        CASE
            WHEN away_score > home_score THEN 'WIN'
            WHEN away_score < home_score THEN 'LOSS'
            ELSE 'DRAW'
        END AS result,
        CASE
            WHEN away_score > home_score THEN 3
            WHEN away_score = home_score THEN 1
            ELSE 0
        END AS points

    FROM {{ ref('stg_matches') }}
    WHERE status = 'FINISHED'

)

SELECT * FROM home_results

UNION ALL

SELECT * FROM away_results