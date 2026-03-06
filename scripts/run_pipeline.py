import os
import shutil


def clean_old_files():

    folders = [
        "data/processed",
        "data/feature_store"
    ]

    for folder in folders:

        if os.path.exists(folder):

            for file in os.listdir(folder):

                path = os.path.join(folder, file)

                if os.path.isfile(path):

                    os.remove(path)

    print("Old files removed")


def run_pipeline():

    print("Running preprocessing...")
    os.system("python src/preprocessing.py")

    print("Running feature engineering...")
    os.system("python src/feature_engineering.py")

    print("Running user profiling...")
    os.system("python src/user_profile.py")

    print("Running item similarity...")
    os.system("python src/item_similarity.py")

    print("Running candidate generation...")
    os.system("python src/candidate_generation.py")

    print("Running ranking...")
    os.system("python src/ranking.py")

    print("Pipeline completed")


if __name__ == "__main__":

    clean_old_files()

    run_pipeline()