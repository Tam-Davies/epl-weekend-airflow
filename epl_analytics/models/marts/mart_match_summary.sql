SELECT
    match_id,
    match_date,
    matchday,
    home_team,
    away_team,
    home_score,
    away_score,
    winner,

    home_score + away_score AS total_goals,

    ABS(home_score - away_score) AS goal_difference,

    CASE
        WHEN home_score > away_score THEN home_team
        WHEN away_score > home_score THEN away_team
        ELSE 'DRAW'
    END AS match_outcome,

    CASE
        WHEN home_score + away_score >= 4 THEN 'HIGH_SCORING'
        WHEN home_score + away_score BETWEEN 1 AND 3 THEN 'LOW_SCORING'
        ELSE 'GOALLESS'
    END AS scoring_category

FROM {{ ref('stg_matches') }}

WHERE status = 'FINISHED'