import glob
import os
import datetime
import shutil
from config import conf


def moving(account_path: str):

    account_name = os.path.basename(account_path)

    filelist = glob.glob(os.path.join(account_path, "**/*"), recursive=False)
    for f in filelist:
        if not os.path.isfile(f):
            continue

        img_name = os.path.basename(f)
        if not img_name.startswith(account_name):
            continue
        utm = img_name.replace(account_name + "_", "").split("_")[0]

        dt = datetime.datetime.fromtimestamp(int(utm))
        dt_path = dt.strftime("%Y\\%m")

        target_path = os.path.join(account_path, dt_path)
        if not os.path.isdir(target_path):
            os.makedirs(target_path, exist_ok=True)
        # target_file = os.path.join(target_path, img_name)
        new_path = shutil.move(f, target_path)
        print(new_path)


def main(target_path: str):
    filelist = glob.glob(os.path.join(target_path, "**/*"), recursive=False)
    for f in filelist:
        if os.path.isfile(f):
            continue

        moving(f)


if __name__ == "__main__":
    for path_info in conf:
        main(path_info["dst_path"])
