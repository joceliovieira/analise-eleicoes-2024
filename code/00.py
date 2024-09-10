import json
import os
from pathlib import Path

import requests
from tqdm import tqdm


def get_sources():
    data_dir_path = '../data'
    download_path = data_dir_path + '/raw'

    source_path = './data_sources.json'
    sources = json.load(open(source_path, 'r', encoding='utf-8'))

    if not os.path.exists(data_dir_path):
        print(f'Criando o diretório {data_dir_path}')
        try:
            os.mkdir(data_dir_path)
        except FileExistsError:
            print(f'O diretório {data_dir_path} já existe\n')
        except OSError as error:
            raise Warning(
                (
                    f'Não foi possível criar o diretório {data_dir_path}'
                    f'\n{error.strerror}'
                )
            )
    if not os.path.exists(download_path):
        print(f'Criando o diretório {download_path}')
        try:
            os.mkdir(download_path)
        except FileExistsError:
            print(f'O diretório {download_path} já existe\n')
        except OSError as error:
            raise Warning(
                (
                    f'Não foi possível criar o diretório {download_path}'
                    f'\n{error.strerror}\n'
                )
            )

    print('\nIniciando download dos arquivos...\n')
    for key, url in sources.items():
        print(f'Baixando o arquivo {key}')
        file_name = url.split('/')[-1]
        file_name = '../data/raw/' + file_name
        file_name = Path(file_name)
        if file_name.exists():
            print(
                (
                    f'O arquivo {key} já existe.'
                    '\nBaixando o próximo arquivo...\n'
                )
            )
            continue
        try:
            r = requests.get(url, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            block_size = 256
            progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)
            with open(file_name, 'wb') as f:
                for i in r.iter_content(block_size):
                    f.write(i)
                    progress_bar.update(len(i))
            progress_bar.close()
        except Exception as error:
            raise Warning(
                (f'Não foi possível baixar o arquivo {key}' f'\n{error}')
            )
    print('Download dos arquivos finalizado!')


if __name__ == '__main__':
    get_sources()
    print(f'Fim do script {Path(__file__).name}')
