import urllib.request
import shutil
import os
import time

NAME = "Project"
URL = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
PATH = os.getcwd() + "/" + NAME
FILENAME = URL[URL.rfind("/") + 1:]
FILEPATH = PATH + "/" + FILENAME
FOLDER = URL[URL.rfind("/"):-4]


def make_dir(debug=0):
    """

    :param debug: debug flag
    :return: Make directory named NAME if directory exists named with number
    at the end
    """
    start_time = time.time()
    counter = 1
    global NAME, PATH, FILEPATH
    while True:
        if NAME not in os.listdir(os.getcwd()):
            os.mkdir(NAME)
            if debug == 1:
                print("Make directory {}".format(NAME))
                print("Take {} seconds".format(time.time() - start_time), "\n")
            break
        else:
            NAME = "Project_{}".format(counter)
            PATH = os.getcwd() + "/" + NAME
            FILEPATH = PATH + "/" + FILENAME
            counter += 1
            continue


def download(filepath, url=URL, debug=0):
    """

    :param debug: debug flag
    :param filepath: str, file path relative
    :param url: str, take a file url
    :return: file, download file from url to filepath
    """
    start_time = time.time()
    # print("Start download {}".format(FILENAME))
    urllib.request.urlretrieve(url, filepath)
    if debug == 1:
        print("Download {} complete".format(FILENAME))
        print("Take {} seconds".format(time.time() - start_time), "\n")


def unpack(filepath, path, debug=0):
    """

    :param debug: debug flag
    :param filepath: str, file path relative
    :param path: str, path relative
    :return: directory, unpack a file from file path to path
    """
    start_time = time.time()
    shutil.unpack_archive(filepath, path)
    if debug == 1:
        print("Unpack {} complete".format(FILENAME))
        print("Take {} seconds".format(time.time() - start_time), "\n")


def create(path, debug=0):
    """

    :param debug: debug flag
    :param path: str, path relative
    :return: directories, create directories (ex:
    /Project/tmp/datalake/movies/movies.csv)for all csv files from unpack
    the directory and move csv files to them
    """
    # start_time = time.time()
    os.chdir(path)
    # print("Change directory to {}".format(name))
    for i in os.listdir(os.getcwd() + FOLDER):
        if i[-3:] == "csv":
            os.makedirs("tmp/datalake/{}".format(i[:-4]))
            shutil.move(os.getcwd() + FOLDER + "/" + i,
                        path + "/tmp/datalake/{}".format(i[:-4]))
            if debug == 1:
                print("{} directory create".format(i[:-4]))
    # print("Take {} seconds".format(time.time() - start_time), "\n")


def remove(filepath, debug=0):
    """

    :param debug: debug flag
    :param filepath: str, file path relative
    :return: nothing, remove not used files/directories
    """
    start_time = time.time()
    os.remove(filepath)
    # print("Remove {} complete".format(FILENAME))
    shutil.rmtree(os.getcwd() + FOLDER)
    if debug == 1:
        print("Remove {} complete".format(FOLDER))
        print("Take {} seconds".format(time.time() - start_time), "\n")


def main(debug=0):
    """

    :param debug: debug flag
    :return: main function
    """
    start_time = time.time()
    make_dir()
    download(FILEPATH)
    unpack(FILEPATH, PATH)
    create(PATH)
    remove(FILEPATH)
    if debug == 1:
        print("Script take {} seconds".format(time.time() - start_time))


if __name__ == '__main__':
    main()
