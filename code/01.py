from pathlib import Path
from zipfile import ZipFile


def get_files(folder: str):
    path = Path(folder)
    files = [i for i in path.glob('*.zip')]
    return files


def extract_csvs(zip_file: str | Path):
    path = Path(zip_file)
    zf = ZipFile(path)
    for file in zf.namelist():
        if '.csv' in file:
            zf.extract(file, 'data/bronze')


print(f'início do processamento - script: {__file__}')
files = get_files('data/raw')
for file in files:
    print(file)
    extract_csvs(file)
print(f'fim do script {__file__}')