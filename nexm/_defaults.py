import os

DB_PATH = "./store/"
if not os.path.isdir(DB_PATH):
    os.makedirs(DB_PATH)
