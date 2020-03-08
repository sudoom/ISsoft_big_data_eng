import sys
import pandas as pd
import os


df = pd.read_csv(sys.stdin, names=["movieId", "title", "genres", "year"])
new_df = df.drop(columns=["movieId"])
os.mkdir(os.getcwd()+"/data/tmp/result")
new_df.to_json(os.getcwd()+"/data/tmp/result/"+"output.json", orient="index")
