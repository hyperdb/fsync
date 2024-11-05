import os
import glob
import shutil
from config import conf


def main(in_path: str, out_path: str):
    filelist = glob.glob(os.path.join(in_path, "**/*"), recursive=True)
    for f in filelist:
        if not os.path.isfile(f):
            continue
        else:
            target_name = f.replace(in_path, out_path)
            dir_name = os.path.dirname(target_name)
            if not os.path.isdir(dir_name):
                os.makedirs(dir_name)
            if not os.path.isfile(target_name):
                shutil.copy2(f, target_name)


if __name__ == "__main__":

    for path_info in conf:
        main(path_info["src_path"], path_info["dst_path"])
