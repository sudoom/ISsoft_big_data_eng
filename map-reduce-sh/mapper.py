import pandas as pd
import sys
import argparse


def parsing():
    """

    :return: parser flags
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-regexp",
                        help="word in title")
    parser.add_argument("-year_from",
                        help="start year",
                        default=1874)
    parser.add_argument("-year_to",
                        help="end year",
                        default=2018)
    parser.add_argument("-genres",
                        help="genres")
    args = parser.parse_args()
    word = args.regexp
    genres = args.genres
    year_from = int(args.year_from)
    year_to = int(args.year_to)
    return word, genres, year_from, year_to


def normalize():
    """

    :return: normalize dataframe
    """
    df = pd.read_csv(sys.stdin)
    title_col = []
    tmp_year_col = []
    for i in df["title"]:
        if i.rfind("(") == -1:
            title_col.append(i)
        else:
            title_col.append(i[:i.rfind("(")])
        if i.rfind("(") == -1 and i.rfind(")") == -1:
            tmp_year_col.append(i)
        else:
            tmp_year_col.append(i[i.rfind("(") + 1:i.rfind(")")])
    year_col = []
    for i in tmp_year_col:
        try:
            year_col.append(int(i))
        except ValueError:
            year_col.append(None)
    df["title"] = title_col
    df["year"] = year_col
    format_genres = df["genres"].str.split("|")
    df["genres"] = format_genres
    df = df.drop(columns="movieId")
    return df


def mapping(df):
    """

    :param df: dataframe
    :return: tuple(genre, [title, year])
    """
    for i in df.index:
        for j in df["genres"][i]:
            map_row = (j, [df["title"][i], df["year"][i]])
            print(map_row)


def search(word, genres, year_from, year_to, df):
    """

    :param word: word flag
    :param genres: genres flag
    :param year_from: year_from flag
    :param year_to: year_to flag
    :param df: dataframe
    :return: tuples(genre, title, year)
    """
    if genres is None and word is None:
        mapping(df)
    elif genres is None:
        word_df = df.loc[
            df["title"].str.contains(word, regex=False)
        ]
        word_year_df = word_df.loc[
            (word_df["year"] > year_from) & (word_df["year"] < year_to)
            ]
        mapping(word_year_df)
    elif word is None:
        genres_df = df.loc[
            df["genres"].str.contains(genres, regex=False)
        ]
        genres_year_df = genres_df.loc[
            (genres_df["year"] > year_from) & (genres_df["year"] < year_to)
            ]
        mapping(genres_year_df)
    else:
        word_df = df.loc[
            df["title"].str.contains(word, regex=False)
        ]
        genres_df = word_df.loc[
            word_df["genres"].str.contains(genres, regex=False)
        ]
        word_genres_year_df = genres_df.loc[
            (genres_df["year"] > year_from) & (genres_df["year"] < year_to)
            ]
        mapping(word_genres_year_df)


def main():
    """

    :return: main func
    """
    word, genres, year_from, year_to = parsing()
    df = normalize()
    search(word, genres, year_from, year_to, df)


if __name__ == '__main__':
    main()
