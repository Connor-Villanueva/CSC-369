import polars as pl
import duckdb
import time

CSV_FILE_PATH = "./2022_place_canvas_history.csv"
PARQUET_FILE_PATH = "./2022_place_canvas_history.parquet"

def _create_parquet():
    print("Creating initial parquet...")
    print("Scanning CSV...")
    df = pl.scan_csv(CSV_FILE_PATH).with_columns(
        (
            pl.coalesce(
                pl.col("timestamp").str.strptime(
                    pl.Datetime, "%Y-%m-%d %H:%M:%S%.f %Z", strict=False
                )
            )
            .dt.replace_time_zone(None)
            .alias("timestamp")
        )
    )
    print("Sinking to Parquet...")
    df.sink_parquet(PARQUET_FILE_PATH)
    print("Finished sinking Parquet.\n")

def _edit_uid():
    print("Editing User IDs...")
    print("Scanning Parquet...")
    df = pl.scan_parquet(PARQUET_FILE_PATH).with_columns(
        pl.col("user_id")
            .rank(method="dense")
            .cast(pl.Int32)
            .sub(1)
            .alias("user_id")
    )

    print("Sinking to Parquet...")
    df.sink_parquet(PARQUET_FILE_PATH)
    print("Finished sinking Parquet.\n")

def _edit_coordinates():
    print("Splitting Coordinates...")
    print("Scanning Parquet...")
    df = (pl.scan_parquet(PARQUET_FILE_PATH).with_columns(
        pl.col("coordinate")
            .str.split(",")
            .alias("coords")
        )
        .with_columns(
            x1=pl.col("coords").list.get(0, null_on_oob=True).cast(pl.Int32),
            y1=pl.col("coords").list.get(1, null_on_oob=True).cast(pl.Int32),
            x2=pl.col("coords").list.get(2, null_on_oob=True).cast(pl.Int32),
            y2=pl.col("coords").list.get(3, null_on_oob=True).cast(pl.Int32)
        )
        .drop("coords")
        .drop("coordinate")
    )

    df = df.collect()
    print("Sinking to Parquet...")
    df.write_parquet(PARQUET_FILE_PATH)
    print("Finished sinking Parquet\n")

def _add_time_since_last_placed():
    query = f"""
        SELECT
            *,
            EPOCH(timestamp) - LAG(EPOCH(timestamp)) OVER (PARTITION BY user_id ORDER BY timestamp ASC) AS time_since_last_placed
        FROM
            '{PARQUET_FILE_PATH}'
    """

    df = duckdb.query(query).pl()

    df.write_parquet(PARQUET_FILE_PATH)

def timer_dec(function):
    def enhanced_function(*args, **kwargs):
        start = time.perf_counter_ns()
        function(*args, *kwargs)
        end = time.perf_counter_ns()
        print("### Runtime")
        print((end-start) / 1e6, "ms")

    return enhanced_function

if __name__ == "__main__":
    # _create_parquet()
    # _edit_uid()
    # _edit_coordinates()
    _add_time_since_last_placed()