import pandas as pd

NAME = input("Print name for a file:", )
DF = pd.DataFrame(
    {"col_1": [True, False, False, True, True],
     "col_2": [i for i in range(5)],
     "col_3": list("abghj"),
     "col_4": pd.date_range(start="20100101", end="20200202",
                            periods=5),
     "col_5": pd.date_range(start="1/1/2007", periods=5),
     "col_6": pd.date_range(end="2016-05-13", periods=5,
                            tz="Europe/Minsk"),
     "col_7": [0.1, 0.5, 6.5, 6.1, 5],
     "col_8": ["Data", 1, True, 0.5, None]
     }
)


def create_csv(df, debug=0):
    """

    :param debug: debug flag
    :param df: take pandas dataframe
    :return: format pandas dataframe to csv file and write it on disk
    """
    df.to_csv("{}.csv".format(NAME), index=False)
    CSV_file = pd.read_csv("{}.csv".format(NAME))
    if debug == 1:
        print(("{}.csv created".format(NAME)), "\n")
    return CSV_file


def csv_to_parquet_to_csv(csv, debug=0):
    """

    :param debug: debug flag
    :param csv: csv file
    :return: format csv to parquet and backward,
    write 2 files with parquet and csv extension
    """
    csv.to_parquet("{}.parquet".format(NAME), compression=None,
                   engine="pyarrow")
    PARQUET_file = pd.read_parquet("{}.parquet".format(NAME), engine="pyarrow")
    if debug == 1:
        print("{}.csv convert to {}.parquet completed".format(NAME, NAME))
        print("{}.parquet created".format(NAME), "\n")
    PARQUET_file.to_csv("{}_1.csv".format(NAME), index=False)
    if debug == 1:
        print("{}.parquet convert to {}_1.csv completed".format(NAME, NAME))
        print("{}_1.csv  created".format(NAME), "\n")
    return PARQUET_file


def parquet_scheme(parquet, debug=0):
    """

    :param debug: debug flag
    :param parquet: parquet file
    :return: scheme of parquet file
    """
    if debug == 1:
        print("{}.parquet scheme".format(NAME), "\n")
    return parquet.info(memory_usage="deep")


def main():
    parquet_scheme(csv_to_parquet_to_csv(create_csv(DF)))


if __name__ == "__main__":
    main()
