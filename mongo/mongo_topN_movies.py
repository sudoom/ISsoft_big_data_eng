import subprocess

from pymongo import MongoClient

client = MongoClient()
N = 5
db = client["topNmovies"]


def import_csv():
    subprocess.run("chmod +x scripts/*.sh", shell=True)
    subprocess.run("scripts/import.sh", shell=True)


def export_csv():
    subprocess.run("scripts/export.sh", shell=True)


def normalize_movies():
    db.movies_raw.aggregate([
        {
            "$project": {
                "temp_title": {
                    "$regexFind": {
                        "input": "$title",
                        "regex": "(.*)[ ]*\((\d{4})\)[ ]*$"
                    }
                },
                "genre": {"$split": ["$genres", "|"]},
                "movieId": 1
            }
        },
        {
            "$project": {
                "_id": 0,
                "year":
                    {"$toInt": {"$arrayElemAt": ["$temp_title.captures", 1]}},
                "title": {"$arrayElemAt": ["$temp_title.captures", 0]},
                "genre": 1,
                "movieId": 1
            }
        },
        {
            "$match": {
                "title": {"$ne": None},
                "year": {"$ne": None}
            }
        },
        {"$unwind": "$genre"},
        {"$out": "movies_normalized"}
    ])


def normalize_ratings():
    db.ratings_raw.aggregate(
        [
            {
                "$group": {
                    "_id": "$movieId",
                    "avg_rate": {"$avg": "$rating"}
                }
            },
            {
                "$project": {
                    "_id": 1,
                    "avg_rating": {"$round": ["$avg_rate", 2]}
                }
            },
            {"$out": "ratings_normalized"}
        ]
    )


def joined():
    db.movies_normalized.aggregate([
        {
            "$lookup": {
                "from": "ratings_normalized",
                "localField": "movieId",
                "foreignField": "_id",
                "as": "tests"
            }
        },
        {
            "$replaceRoot": {
                "newRoot": {
                    "$mergeObjects": [
                        {"$arrayElemAt": ["$tests", 0]},
                        "$$ROOT"]
                }
            }
        },
        {
            "$project": {
                "tests": 0,
                "movieId": 0
            }
        },
        {
            "$sort": {
                "genre": 1,
                "avg_rating": -1
            }
        },
        {"$out": "joined"}
    ])


def to_csv():
    db.joined.aggregate([
        {
            "$group": {
                "_id": "$genre",
                "temp_movies": {
                    "$push": {
                        "avg_rating": "$avg_rating",
                        "title": "$title",
                        "year": "$year"}}
            }
        },
        {
            "$project": {
                "genre": "$_id",
                "_id": 0,
                "topN": {"$slice": ["$temp_movies", N]}
            }
        },
        {"$unwind": "$topN"},
        {
            "$project": {
                "_id": 1,
                "genre": 1,
                "avg_rating": "$topN.avg_rating",
                "title": "$topN.title",
                "year": "$topN.year"
            }
        },
        {
            "$sort": {
                "genre": 1,
                "avg_rating": -1
            }
        },
        {"$out": "to_csv"}
    ])


def main():
    import_csv()
    normalize_movies()
    normalize_ratings()
    joined()
    to_csv()
    export_csv()


if __name__ == "__main__":
    main()
