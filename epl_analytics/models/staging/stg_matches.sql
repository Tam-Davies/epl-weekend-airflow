SELECT
    match_id,
    match_date,
    status,
    matchday,
    home_team,
    away_team,
    home_score,
    away_score,
    winner,
    home_score + away_score AS total_goals

FROM {{ source('raw', 'matches') }}