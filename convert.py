import os
import cloudconvert
import urllib.request
from config import TOKEN_CONVERT

cloudconvert.configure(api_key=TOKEN_CONVERT,
                       sandbox=False)


# создание работы для конвертации одного формата в другой с использование API и преобразуем полученный код с сайта
def convert_BGC(number_college):
    filename = f'zamena{number_college}.xlsx'
    urllib.request.urlretrieve(f'http://www.bgtc.su/wp-content/uploads/raspisanie/zamena{number_college}k.xlsx',
                               filename)
    os.replace(filename, f'сontainer/{filename}')

    name_file = f'zamena{str(number_college)}k.xlsx'  # название файла
    url = 'http://www.bgtc.su/wp-content/uploads/raspisanie/' + name_file  # ссылка на файл + название файла
    data = cloudconvert.Job.create(payload={
        "tasks": {
            'import-1': {
                'operation': 'import/url',
                'url': url,
                'filename': name_file
            },
            'xlsx_to_png': {
                'operation': 'convert',
                'input': 'import-1',
                'output_format': 'png',
                'filename': f'download_{name_file[:-5]}.png'  # удаляем xlsx расширение с помощью среза
            },
            'export-1': {
                'operation': 'export/url',
                'input': 'xlsx_to_png'
            }
        }
    })
    exported_url_task_id = data.get('tasks')[2].get('id')
    res = cloudconvert.Task.wait(id=exported_url_task_id)  # Wait for job completion
    file = res.get("result").get("files")[0]
    filename = file['filename']
    file_url = file['url']
    cloudconvert.download(filename=filename, url=file_url)
    os.replace(filename, f'pictures/download_zamena{number_college}k.png')


convert_BGC(1)
convert_BGC(2)
convert_BGC(3)
convert_BGC(4)