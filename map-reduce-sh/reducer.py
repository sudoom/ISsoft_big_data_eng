import sys
import os
import json
from numpy import nan
import math
import shutil

# filename can be overwritten
NAME = "output"
# path of directory
DIR = os.getcwd() + "/data/tmp/result"


def check_dir():
    """
    Check directory, if directory exist delete them, and create new.
    :return: Nothing
    """
    while True:
        try:
            os.mkdir(DIR)
            break
        except FileExistsError:
            shutil.rmtree(DIR)


def create_lists():
    """

    :return: list with genres, list with title and year
    """
    genres_list = []
    tuple_list = []
    for line in sys.stdin:
        res = eval(line)
        genres_list.append(res[0])
        tuple_list.append(res)
    return genres_list, tuple_list


def create_tmp_dict(genres_list):
    """

    :param genres_list: list with genres
    :return: temporary dictionary
    """
    tmp_dict = {}
    cnt = 1
    for i in set(genres_list):
        value_tmp_dict = {"genre": f"{i}", "movies": []}
        tmp_dict[cnt] = value_tmp_dict
        cnt += 1
    return tmp_dict


def create_main_dict(tmp_dict, tuple_list):
    """

    :param tmp_dict: temporary dictionary
    :param tuple_list: list with title and year
    :return: main dictionary
    """
    for i in tmp_dict.items():
        for j in i[1].items():
            for k in tuple_list:
                if k[0] == j[1]:
                    i[1]["movies"].append(
                        {"title": f"{k[1][0]}",
                         "year": int(k[1][1]) if not math.isnan(k[1][1]) else None})
    return tmp_dict


def create_json(main_dict):
    """

    :param main_dict: main dictionary
    :return: create json file
    """
    with open(f"{DIR}/{NAME}.json", "w") as wr_file:
        json.dump(main_dict, wr_file)


def main():
    """

    :return: main func
    """
    check_dir()
    genre_list, tuple_list = create_lists()
    tmp_dict = create_tmp_dict(genre_list)
    main_dict = create_main_dict(tmp_dict, tuple_list)
    create_json(main_dict)


if __name__ == '__main__':
    main()
