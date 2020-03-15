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
    for i in tmp:
        if i.rfind("(") == -1:
            title.append(i)
        else:
            title.append(i[:i.rfind("(")])
        if i.rfind("(") == -1 and i.rfind(")") == -1:
            tmp_year.append(i)
        else:
            tmp_year.append(i[i.rfind("(") + 1:i.rfind(")")])
    for i in tmp_year:
        try:
            year.append(int(i))
        except ValueError:
            year.append(None)
    for i in tmp_genres:
        genres.append(i.strip().split("|"))
    main = list(zip(title, year, genres))
    return main


def mapping(ds):
    """

    :param ds: dataset
    :return: genre, [title, year]
    """
    for i in ds:
        for j in i[2]:
            yield j, (i[0], i[1])


def genres_helper(ds, genres):
    """

    :param ds: dataset
    :param genres: genres flag
    :return: ds with apply genres
    """
    genre_ds = []
    for i in ds:
        for j in i[2]:
            if j == genres:
                genre_ds.append(i)
    return genre_ds


def word_helper(ds, word):
    """

    :param ds: dataset
    :param word: word flag
    :return: dataset with apply word
    """
    word_ds = []
    for i in ds:
        if i[0].find(word) != -1:
            word_ds.append(i)
    return word_ds


def time_helper(ds, year_from, year_to):
    """

    :param ds: dataset
    :param year_from: year_from flag
    :param year_to: year_to flag
    :return: dataset with apply years
    """
    time_ds = []
    for i in ds:
        try:
            if year_from <= i[1] <= year_to:
                time_ds.append(i)
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
