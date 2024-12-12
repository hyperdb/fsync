import os
import glob
import sqlite3
from config import conf


def create_list(account_path: str):
    # account = os.path.basename(account_path)

    exprot_db = sqlite3.connect("./sqlite/export.db")

    cur = exprot_db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS image_files (fname TEXT NOT NULL PRIMARY KEY);"
    )

    filelist = glob.glob(os.path.join(account_path, "**/*"), recursive=True)
    for f in filelist:
        if not os.path.isfile(f):
            continue

        img_name = os.path.basename(f)

        cur.execute(
            "INSERT OR IGNORE INTO image_files (fname) VALUES (\"%s\")" % (
                img_name)
        )

    cur.close()
    exprot_db.commit()
    exprot_db.close()


def main(target_path: str):
    filelist = glob.glob(os.path.join(target_path, "**/*"), recursive=True)
    for f in filelist:
        if os.path.isfile(f):
            continue

        create_list(f)


if __name__ == "__main__":
    for path_info in conf:
        main(path_info["dst_path"])
