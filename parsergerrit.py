import argparse
import json
import os
import sys
from typing import Dict

import pandas as pd
import requests

from utils.base import Tools


def userargs():
    """輸入參數定義，使用 -h / --help 查詢."""

    parser = argparse.ArgumentParser(
        description="發版小工具 - 抓取 Gerrit Change 內容， 若無法抓取請先使用瀏覽器登入 Gerrit.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-n", metavar="number", dest="number", required=True, help="Gerrit change number.")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return parser.parse_args()


def main(args):

    # gerrit REST API search command
    gerrit_search_text = r"&o=CURRENT_REVISION&o=CURRENT_COMMIT&o=CURRENT_FILES&o=DOWNLOAD_COMMANDS"
    url = rf"http://gerrit.kway.com.tw:8082/changes/?q={args.number}{gerrit_search_text}"

    # output file path
    outdir = r"./out"
    Tools.checkdir(outdir)
    outpath = os.path.join(outdir, f"gerrit-{args.number}.xlsx")

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve the page. Status code: {response.status_code}")

    data_all = json.loads(response.text[5:])[0]

    # 取得所有變更項目資料
    data_change: Dict[str, Dict[str, str]] = (
        data_all.get("revisions", {}).get(data_all["current_revision"], {}).get("files", {})
    )

    data_out = []
    # 轉換為 pandas 格式
    for name, info in data_change.items():
        data_out.append(
            {
                "File Name": name,
                "Lines Inserted": info.get("Lines Inserted", 0),
                "Lines Deleted": info.get("lines_deleted", 0),
                "Size Delta": info.get("size_delta", 0),
                "Size": info.get("size", 0),
            }
        )

    # 輸出至 excel
    df = pd.DataFrame(data_out)
    df.to_excel(outpath, index=False)


if __name__ == "__main__":
    main(userargs())
