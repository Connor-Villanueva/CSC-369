# Week 2 Analysis

This week, we performed the same task as in week 1, but now with 3 new libraries:

1. `DuckDB` in `rplace_duckdb.py`
2. `Polars` in `rplace_polars.py`
3. `Pandas` in `rplace_pandas.py`

Some preprocessing of the data was performed prior to running any of these scripts. This preprocessing is done in `helper.py`. 

Note: This script also contains a decorater that is used for timing purposes.

The preprocessing that was performed was migrating the data from a `csv` file to a `parquet` file. In this process, timestamps were correctly converted to `datetime` data types and user ids were removed.

# Reflection

Overall, we see that DuckDB and Polars perform significantly better than my SQLite appraoch from week 1. Had I taken the more traditional approach in week 1, we would have seen the improvement with Pandas as well.

Personally, the easiest script to write, and my favorite, was `rplace_duckdb.py` because of my familarity with DuckDB from CSC 466, and SQL. This also ran the fastest, compared to the other two.

Though that's not to say that Polars and Pandas were very difficult either. I got some experience with these in CSC 466, but mainly had to lookup some syntax. Polars and Pandas are also similar enough that it was easy to translate from one to the other.