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

    :return: normalize dataset
    """
    year = []
    tmp_year = []
    title = []
    tmp = []
    tmp_genres = []
    genres = []
    for line in sys.stdin:
        line = line.strip()
        line = line.split(',')
        if len(line) > 3:
            for i in range(2, len(line) - 1):
                line[1] = line[1] + line[i]
        line = "{}, {}, {}".format(line[0], line[1], line[-1])
        line = line.split(",")
        tmp.append(line[1])
        tmp_genres.append(line[2])
    for element in tmp:
        if element.rfind("(") == -1:
            title.append(element)
        else:
            title.append(element[:element.rfind("(")])
        if element.rfind("(") == -1 and element.rfind(")") == -1:
            tmp_year.append(element)
        else:
            tmp_year.append(element[element.rfind("(") + 1:element.rfind(")")])
    for year_str in tmp_year:
        try:
            year.append(int(year_str))
        except ValueError:
            year.append(None)
    for genre in tmp_genres:
        genres.append(genre.strip().split("|"))
    ds = list(zip(title, year, genres))
    return ds


def mapping(ds):
    """

    :param ds: dataset
    :return: genre, (genre, title, year)
    """
    for line in ds:
        for genre in line[2]:
            yield genre, (genre, line[0], line[1])


def genres_helper(ds, genres):
    """

    :param ds: dataset
    :param genres: genres flag
    :return: ds with apply genres
    """
    genre_ds = []
    for line in ds:
        for genre in line[2]:
            if genre == genres:
                genre_ds.append(line)
    return genre_ds


def word_helper(ds, word):
    """

    :param ds: dataset
    :param word: word flag
    :return: dataset with apply word
    """
    word_ds = []
    for line in ds:
        if line[0].find(word) != -1:
            word_ds.append(line)
    return word_ds


def time_helper(ds, year_from, year_to):
    """

    :param ds: dataset
    :param year_from: year_from flag
    :param year_to: year_to flag
    :return: dataset with apply years
    """
    time_ds = []
    for line in ds:
        try:
            if year_from <= line[1] <= year_to:
                time_ds.append(line)
        except TypeError:
            continue
    return time_ds


def search(word, genres, year_from, year_to, ds):
    """

    :param word: word flag
    :param genres: genres flag
    :param year_from: year_from flag
    :param year_to: year_to flag
    :param ds: dataset
    :return: genre (title, year)
    """

    if genres is None and word is None:
        for key, value in mapping(ds):
            print("{}\t{}".format(key, value))
    elif genres is None:
        word_ds = word_helper(ds, word)
        word_time_ds = time_helper(word_ds, year_from, year_to)
        for key, value in mapping(word_time_ds):
            print("{}\t{}".format(key, value))
    elif word is None:
        genre_ds = genres_helper(ds, genres)
        genre_time_ds = time_helper(genre_ds, year_from, year_to)
        for key, value in mapping(genre_time_ds):
            print("{}\t{}".format(key, value))
    else:
        word_ds = word_helper(ds, word)
        genre_ds = genres_helper(word_ds, genres)
        word_genre_time_ds = time_helper(genre_ds, year_from, year_to)
        for key, value in mapping(word_genre_time_ds):
            print("{}\t{}".format(key, value))



def main():
    """

    :return: main func
    """
    word, genres, year_from, year_to = parsing()
    ds = normalize()
    search(word, genres, year_from, year_to, ds)


if __name__ == '__main__':
    main()
