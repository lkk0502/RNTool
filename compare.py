import argparse
import os
import sys
from datetime import datetime
from typing import Dict

import pandas as pd

from utils.base import Tools


def userargs():
    """輸入參數定義，使用 -h / --help 查詢."""

    parser = argparse.ArgumentParser(
        description="發版小工具 - 比對新舊版本差異.", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("old", metavar="old", help="Old version.")
    parser.add_argument("new", metavar="new", help="New version.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()


def get_all_filesinfo(path: str) -> Dict[str, Dict[str, str]]:
    """取得路徑下所有檔案的 `名稱` & `大小` & `修改時間`."""

    data = {}
    timeformat = "%Y/%m/%d %H:%M:%S"
    basepath = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            mtime = os.path.getmtime(filepath)
            data[os.path.relpath(filepath, basepath)] = {
                "File Size": os.path.getsize(filepath),
                "File mTime": datetime.fromtimestamp(mtime).strftime(timeformat),
            }

    return data


def main(args):

    # output file path
    outdir = r"./out"
    Tools.checkdir(outdir)
    outpath = os.path.join(outdir, "compare.xlsx")

    data_old = get_all_filesinfo(args.old)
    data_new = get_all_filesinfo(args.new)

    data_out = []
    # status : N:新增 A:修改 R:移除 O:原始
    # Compare old and new file size
    for name in set(data_old.keys()).union(data_new.keys()):
        old = data_old.get(name, None)
        new = data_new.get(name, None)

        if old and new:
            status = "O " if old["File Size"] == new["File Size"] else "A"
        elif old:
            status = "R"
        elif new:
            status = "N"
        else:
            raise SystemError("出現未預期錯誤!")

        data_out.append(
            {
                "Status": status,
                "File Name": name,
                "Content": "",
                "File Size": "" if new is None else new["File Size"],
                "File mTime": "" if new is None else new["File mTime"],
                "Old File Size": "" if old is None else old["File Size"],
                "Old File mTime": "" if old is None else old["File mTime"],
            }
        )

    # 先依照檔案名稱排序
    data_out.sort(key=lambda x: x["File Name"])

    # 依照 status 排序
    df = pd.DataFrame(data_out).sort_values(by="Status", key=lambda x: x.map({"N": 0, "A": 1, "R": 2, "O": 3}))
    # 輸出至 excel
    df.to_excel(outpath, index=False)


if __name__ == "__main__":
    main(userargs())
