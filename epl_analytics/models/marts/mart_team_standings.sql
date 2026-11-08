SELECT
    team,

    COUNT(*) AS played,

    SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) AS won,

    SUM(CASE WHEN result = 'DRAW' THEN 1 ELSE 0 END) AS drawn,

    SUM(CASE WHEN result = 'LOSS' THEN 1 ELSE 0 END) AS lost,

    SUM(goals_for) AS goals_for,

    SUM(goals_against) AS goals_against,

    SUM(goals_for) - SUM(goals_against) AS goal_difference,

    SUM(points) AS points

FROM {{ ref('int_team_match_results') }}

GROUP BY team