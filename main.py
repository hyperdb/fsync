import os
import glob
import shutil
import sys
import sqlite3
from config import conf


def main(in_path: str, out_path: str):
    skip_cnt = 0
    copy_cnt = 0

    exprot_db = sqlite3.connect("./sqlite/export.db")

    cur = exprot_db.cursor()

    filelist = glob.glob(os.path.join(in_path, "**/*"), recursive=True)
    for f in filelist:
        if not os.path.isfile(f):
            continue
        else:
            img_name = os.path.basename(f)

            cur.execute('SELECT fname FROM image_files WHERE fname="%s"' % (img_name))
            if cur.fetchone() is not None:
                sys.stdout.write("\r\033[K" + "skip")
                sys.stdout.flush()
                skip_cnt += 1
                continue

            cur.execute(
                'INSERT OR IGNORE INTO image_files (fname) VALUES ("%s")' % (img_name)
            )

            target_name = f.replace(in_path, out_path)
            dir_name = os.path.dirname(target_name)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            if not os.path.isfile(target_name):
                shutil.copy2(f, target_name)
                sys.stdout.write("\r\033[K" + target_name)
                sys.stdout.flush()
                copy_cnt += 1
            else:
                sys.stdout.write("\r\033[K" + "skip")
                sys.stdout.flush()
                skip_cnt += 1

    sys.stdout.write("\r\033[K")
    sys.stdout.write(f"{copy_cnt} file(s) copy\n")
    sys.stdout.write(f"{skip_cnt} file(s) skip\n")
    sys.stdout.flush()

    cur.close()
    exprot_db.commit()
    exprot_db.close()


if __name__ == "__main__":

    for path_info in conf:
        main(path_info["src_path"], path_info["dst_path"])
