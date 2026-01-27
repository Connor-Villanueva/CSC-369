import duckdb
import polars as pl

from datetime import datetime
from helper import timer_dec
import colornames
import sys

PARQUET_PATH = "../2022_place_canvas_history_uid.parquet"
MAX_INACTIVITY = 900

"""
Ranks colors by the number of distinct users who placed
those colors during the specified timeframe.
"""
def rankColors(filtered_df: pl.DataFrame) -> None:
    query = f"""
        SELECT
            pixel_color,
            COUNT(DISTINCT user_id) AS user_count
        FROM
            filtered_df
        GROUP BY
            pixel_color
        ORDER BY
            user_count DESC
    """

    res = duckdb.query(query)

    print("- **Top**")
    for i, tup in enumerate(res.fetchall()):
        color_hex = tup[0]
        freq = tup[1]
        color_name = colornames.find(color_hex)

        print(f"{i+1}. {color_name}: {freq} users")

    print()

"""
Calculates the average session length in seconds during the specified
timeframe.
"""
def averageSessionLength(filtered_df: pl.DataFrame):
    query = f"""
        WITH
            time_diff AS (
                SELECT
                    *,
                    EPOCH(timestamp) - LAG(EPOCH(timestamp)) OVER (PARTITION BY user_id ORDER BY timestamp ASC) AS inactivity_time
                FROM
                    filtered_df
                ORDER BY
                    user_id, timestamp ASC
            ),
            sessions AS (
                SELECT
                    SUM(
                        CASE WHEN 
                            inactivity_time > {MAX_INACTIVITY} OR inactivity_time IS NULL 
                        THEN 1 
                        ELSE 0 END
                    ) OVER (PARTITION BY user_id ORDER BY timestamp ASC) AS session_id,
                    user_id,
                    timestamp
                FROM
                    time_diff
            ),
            session_lengths AS (
                SELECT
                    user_id,
                    session_id,
                    EPOCH(MAX(timestamp)) - EPOCH(MIN(timestamp)) AS session_length
                FROM
                    sessions
                GROUP BY
                    user_id, session_id
                HAVING
                    COUNT(*) > 1
            )
        SELECT
            ROUND(AVG(session_length), 2) AS avg_session_length_seconds
        FROM
            session_lengths
    """

    res = duckdb.query(query).fetchone()[0]

    print(f"- **Output:** {res} seconds\n")

"""
Calculates the 50th, 75th, 90th, and 99th percentile
of the numbers of pixels placed by users during the specified
timeframe.
"""
def pixelPlacementPercentiles(filtered_df: pl.DataFrame):
    query = f"""
        WITH
            dist AS (
                SELECT
                    user_id,
                    COUNT(*) AS freq
                FROM
                    filtered_df
                GROUP BY
                    user_id
            )
        SELECT
            quantile_cont(freq, 0.50 ORDER BY freq ASC) AS '50_percentile',
            quantile_cont(freq, 0.75 ORDER BY freq ASC) AS '75_percentile',
            quantile_cont(freq, 0.90 ORDER BY freq ASC) AS '90_percentile',
            quantile_cont(freq, 0.99 ORDER BY freq ASC) AS '99_percentile'
        FROM
            dist
    """

    p50, p75, p90, p99 = duckdb.query(query).fetchone()

    print(f"- **Output:**")
    print(f"  - 50th Percentile: {p50} pixels")
    print(f"  - 75th Percentile: {p75} pixels")
    print(f"  - 90th Percentile: {p90} pixels")
    print(f"  - 99th Percentile: {p99} pixels\n")
    

"""
Counts how many users placed their first pixel ever
within the specified timeframe.
"""
def firstTimeUsers(filtered_df: pl.DataFrame, start_time: datetime):
    query = f"""
        WITH
            during_timeframe AS (
                SELECT
                    DISTINCT user_id
                FROM
                    filtered_df
            ),
            before_timeframe AS (
                SELECT
                    DISTINCT user_id
                FROM
                    '{PARQUET_PATH}'
                WHERE
                    timestamp < '{start_time}'
            )
        SELECT
            count(*) AS new_users
        FROM
            before_timeframe AS btf
        RIGHT JOIN during_timeframe AS dtf ON
            btf.user_id = dtf.user_id
        WHERE
            btf.user_id IS NULL
    """

    res = duckdb.query(query).fetchone()[0]

    print(f"- **Output:** {res} users\n")


def filter_df(start_time: datetime, end_time: datetime) -> pl.DataFrame:
    query = f"""
        SELECT *
        FROM '{PARQUET_PATH}'
        WHERE
            timestamp BETWEEN '{start_time}' AND '{end_time}'
    """

    return duckdb.query(query).df()

@timer_dec
def getResults(start_time: datetime, end_time: datetime):
    print("\n**Timeframe:**", start_time, "to", end_time, "\n")
    
    filtered_df: pl.DataFrame = filter_df(start_time, end_time)

    print("### Ranking of Colors by Distinct Users")
    rankColors(filtered_df)

    print("### Average Session Length")
    averageSessionLength(filtered_df)

    print("### Percentiles of Pixels Placed")
    pixelPlacementPercentiles(filtered_df)

    print("### Count of First-Time Users")
    firstTimeUsers(filtered_df, start_time)

def printUsage():
    print("Usage: [YYYY-MM-DD HH] [YYYY-MM-DD HH]")

def main():
    if (len(sys.argv) != 5):
        printUsage()
        sys.exit(1)

    try:
        year, month, day = sys.argv[1].split("-")
        start_time = datetime(int(year), int(month), int(day), int(sys.argv[2]))

        year, month, day = sys.argv[3].split("-")
        end_time = datetime(int(year), int(month), int(day), int(sys.argv[4]))

    except Exception as e:
        printUsage()
        sys.exit(1)

    if (start_time > end_time):
        print("Ending date must be after the starting date.")
        sys.exit(1)

    getResults(start_time, end_time)

    
if __name__ == "__main__":
    main()