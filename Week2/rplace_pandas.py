import pandas as pd
from datetime import datetime
import sys
from helper import timer_dec

PARQUET_FILE_PATH = "../2022_place_canvas_history.parquet"

@timer_dec
def getResults(start_time, end_time):
    df = pd.read_parquet(PARQUET_FILE_PATH)
    color = (
            df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
            ).groupby("pixel_color").count().sort_values(by="timestamp", ascending=False)
    
    coord = (
            df[(df["timestamp"] >= start_time) & (df["timestamp"] <= end_time)]
            ).groupby("coordinate").count().sort_values(by="timestamp", ascending=False)
    
    print("\n-=-=-=-=-=-=-=-\n")
    print("Most Placed Color:", color.iloc[0].name)
    print(f"Most Placed Pixel Location: ({coord.iloc[0].name})")
    print("\n-=-=-=-=-=-=-=-\n")

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

    
    print("\nTimeframe:", start_time, "to", end_time)
    getResults(start_time, end_time)

if __name__ == "__main__":
    main()