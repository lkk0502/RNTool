# KWAY 發版小工具

![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![OS: Windows 10](https://img.shields.io/badge/OS-Windows%20-blue.svg)

發版小工具

| 版本  | 日期         | 變更者   | 說明 |
| :---- | :----------- | :------- | :--- |
| `1.0` | `2024/12/19` | `zhewei` | 初版 |

## 前言

因為發版過程要貼 gerrit 變更 + 產出檔案大小 / 前次檔案大小 / 新增修改移除 ...等等，過程耗日曠時，故建立下列工具來快速產生相關清單。

其中包含:

- [`compare`](#compare) : 比對當前版本與前一個版本的檔案內容大小差異輸出為 Excel。
- [`parsergerrit`](#parsergerrit) : 抓取 gerrit change number 輸出為 Excel。

## compare

用於比對相同產品，不同版本號之差異，輸出 Excel 格式，並依照 N ( 新增 ) / A ( 修改 ) / R ( 移除 ) / O ( 原始 ) 格式順序排列。

Usage:

```shell
# usage: compare.exe [-h] old new

python compare oldpath newpath
```

參數說明:

- `-h` / `--help` : Show usage。
- `oldpath` : 舊的版本檔案路徑，請指定 folder。***必填***。
- `newpath` : 新的版本檔案路徑，請指定 folder。***必填***。

檔案輸出至當前目錄下 `.\out\compare.xlsx`

範例:

```shell
python compare .\source\NPC-DT3-19 .\source\NPC-DT3-28
```

輸出檔案可參考 `./samlpe/out/compare.xlsx`

將資料複製到 `RN.docs` 時須注意 : 必須依照 `docs` 中的行數複製 `xlsx` 再進行貼上，否則會有欄位跑掉的問題。
ex. `docs` 中預設為 2 行，則在 `xlsx` 複製時也需要複製 2 行資料格，貼上後才可確保格式正常。

## parsergerrit

用於快速輸出 gerrit 變更項目清單至 Excel，使用前請先透過瀏覽器登入 gerrit，避免無法正確抓取資料。

Usage:

```shell
# usage: parsergerrit.exe [-h] -n number

python parsergerrit -n gerrit_number
```

參數說明:

- `-h` / `--help` : Show usage。
- `-n` : 要抓取的 Gerrit change number。***必填***。

檔案輸出至當前目錄下 `.\out\gerrit-{number}.xlsx`

範例:

```shell
python parsergerrit -n 29743
```

輸出檔案可參考 `./samlpe/out/gerrit-29743.xlsx`

將資料複製到 `RN.docs` 時須注意 : 必須依照 `docs` 中的行數複製 `xlsx` 再進行貼上，否則會有欄位跑掉的問題。
ex. `docs` 中預設為 2 行，則在 `xlsx` 複製時也需要複製 2 行資料格，貼上後才可確保格式正常。
