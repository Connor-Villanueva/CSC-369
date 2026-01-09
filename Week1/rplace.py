import sqlite3
import time
import sys
import csv
from datetime import datetime

CSV_FILE = "../2022_place_canvas_history.csv"
DB_FILE = "./2022_place_canvas.db"
TABLE_NAME = "canvas_history"

def createDB():
    # Start the connection
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Creating the table
    query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            timestamp TEXT,
            user_id TEXT,
            pixel_color TEXT,
            coordinate TEXT
        )
    """
    cursor.execute(query)

    # Insert the csv content into the database
    with open(CSV_FILE, "rt") as f:
        reader = csv.reader(f)

        next(reader)

        query = f"""
            INSERT INTO {TABLE_NAME}
            VALUES (?, ?, ?, ?)
        """

        cursor.executemany(query, reader)

    # Update timestamps to DATETIME objects
    query = f"""
        UPDATE {TABLE_NAME}
        SET timestamp = DATETIME(SUBSTR(timestamp, 1, LENGTH(timestamp) - 4))
    """
    cursor.execute(query)

    # Create Indices For Performance

    # (Timestamp, pixel_color) idx
    query = f"""
        CREATE INDEX
            date_color
        ON
            {TABLE_NAME}
        (timestamp, pixel_color)
    """
    cursor.execute(query)

    # (Timestamp, coordinate) idx
    query = f"""
        CREATE INDEX
            date_coord
        ON
            {TABLE_NAME}
        (timestamp, coordinate)
    """
    cursor.execute(query)

    # (Timestamp) idx
    query = f"""
        CREATE INDEX
            date_idx
        ON
            {TABLE_NAME}
        (timestamp)
    """
    cursor.execute(query)

    conn.commit()
    conn.close()


def timer_dec(func):
    def enhanced_func(*args, **kwargs):
        start = time.perf_counter_ns()
        func(*args, *kwargs)
        end = time.perf_counter_ns()
        print("Execution time:", (end - start) / 1e6, "ms")
    
    return enhanced_func

@timer_dec
def getResults(conn : sqlite3.Connection, start_time, end_time):
    query = f"""
        SELECT
            pixel_color,
            COUNT(*) AS frequency
        FROM {TABLE_NAME}
        WHERE timestamp >= DATETIME('{start_time}') AND timestamp <= DATETIME('{end_time}')
        GROUP BY pixel_color
        ORDER BY frequency DESC
        LIMIT 3
    """
    color = conn.execute(query).fetchone()

    query = f"""
        SELECT
            coordinate,
            COUNT(*) AS frequency
        FROM {TABLE_NAME}
        WHERE timestamp >= DATETIME('{start_time}') AND timestamp <= DATETIME('{end_time}')
        GROUP BY coordinate
        ORDER BY frequency DESC
        LIMIT 3
    """
    coord = conn.execute(query).fetchone()

    print("\n-=-=-=-=-=-=-=-\n")
    print("Most Placed Color:", color[0])
    print(f"Most Placed Pixel Location: ({coord[0]})")
    print("\n-=-=-=-=-=-=-=-\n")

def printUsage():
    print("Usage: [YYYY-MM-DD HH] [YYYY-MM-DD HH]")

def main():
    # createDB()

    conn = sqlite3.connect(DB_FILE)

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

    print("\nTimeframe:", start_time, "to", end_time)
    getResults(conn, start_time, end_time)

    conn.close()

if __name__ == "__main__":
    main()