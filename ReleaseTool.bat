@REM 建置檔案
python -m PyInstaller --distpath ./out --onefile .\compare.py

python -m PyInstaller --distpath ./out --onefile .\parsergerrit.py

@REM 複製 Readme
mkdir .\out\sample\out
copy .\Readme.md .\out /Y
copy .\sample\out\* .\out\sample\out