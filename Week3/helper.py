import polars as pl
import time

CSV_FILE_PATH = "../2022_place_canvas_history.csv"
PARQUET_FILE_PATH = "../2022_place_canvas_history_uid.parquet"

def _create_parquet():
    df = pl.scan_csv(CSV_FILE_PATH).with_columns(
        (
            pl.coalesce(
                pl.col("timestamp").str.strptime(
                    pl.Datetime, "%Y-%m-%d %H:%M:%S.%f %Z", strict=False
                ),
                pl.col("timestamp").str.strptime(
                    pl.Datetime, "%Y-%m-%d %H:%M:%S %Z", strict=False
                )
            )
            .dt.replace_time_zone(None)
            .alias("timestamp")
        ),
        (
            pl.col("user_id")
                .rank(method="dense")
                .cast(pl.Int32)
                .sub(1)
                .alias("user_id")
        )
    )

    df = df.with_columns(
        pl.col("user_id")
            .rank(method="dense")
            .cast(pl.Int32)
            .sub(1)
            .alias("user_id")
    )

    df = df.with_columns()

    df.sink_parquet(PARQUET_FILE_PATH)

def _edit_uid():
    df = pl.scan_parquet(PARQUET_FILE_PATH).with_columns(
        pl.col("user_id")
            .rank(method="dense")
            .cast(pl.Int32)
            .sub(1)
            .alias("user_id")
    )

    df.sink_parquet(PARQUET_FILE_PATH)

def timer_dec(function):
    def enhanced_function(*args, **kwargs):
        start = time.perf_counter_ns()
        function(*args, *kwargs)
        end = time.perf_counter_ns()
        print("Execution time:", (end-start) / 1e6, "ms")

    return enhanced_function

if __name__ == "__main__":
    # _create_parquet()
    _edit_uid()