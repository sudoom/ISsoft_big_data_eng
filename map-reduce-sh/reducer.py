import sys


def create_lists():
    """

    :return: list with genres, list with title and year
    """
    genres_list = []
    tmp_list = []
    tuple_list = []
    for line in sys.stdin:
        line = line.strip().split("\t")
        genres_list.append(line[0])
        tmp_list.append(line[1])
    for i in tmp_list:
        i = i.strip("()").split(",")
        tmp = []
        for j in i:
            j = j.strip(" '")
            tmp.append(j)
        tuple_list.append(tmp)
    return genres_list, tuple_list


def create_tmp_dict(genres_list):
    """

    :param genres_list: list with genres
    :return: temporary dictionary
    """
    tmp_dict = {}
    cnt = 1
    for i in set(genres_list):
        value_tmp_dict = {"genre": "{}".format(i), "movies": []}
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
                        {"title": "{}".format(k[1]),
                         "year": int(k[2]) if k[2] != 'None' else None})
        print(i[1])


def main():
    """

    :return: main func
    """
    genre_list, tuple_list = create_lists()
    tmp_dict = create_tmp_dict(genre_list)
    create_main_dict(tmp_dict, tuple_list)


if __name__ == '__main__':
    main()
