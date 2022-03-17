import os.path
import urllib.request
import datetime
import convert
import BD
from datetime import datetime
from pytz import timezone
from time import sleep
from Vk_bot import send_message, upload_photo, uppload_doc

TIME_ZONE = timezone("Asia/Krasnoyarsk")
timetable_old_size1 = os.path.getsize('сontainer/zamena1.xlsx')
timetable_old_size2 = os.path.getsize('сontainer/zamena2.xlsx')
timetable_old_size3 = os.path.getsize('сontainer/zamena3.xlsx')
timetable_old_size4 = os.path.getsize('сontainer/zamena4.xlsx')


def comparison_size_bgc(college_number, timetable_old_size, start_program):
    """Проверяем размер исходного(старого файла с расписанием)
     с новым, если они не равны - отсылаем запрос"""
    timetable_new_size = \
        int(urllib.request.urlopen(
            f'http://www.bgtc.su/wp-content/uploads/raspisanie/zamena{college_number}k.xlsx').info()[
                'Content-Length'])
    if timetable_new_size != timetable_old_size:
        convert.convert_BGC(college_number)
        if not start_program:
            users = BD.user_show_college(f'{college_number} корпус')
            url = f'pictures/download_zamena{college_number}k.png'
            url_photo = upload_photo(url)
            for user in users:
                send_message(user, f'Обновление расписания {college_number} корпус', url_photo)
    return timetable_new_size


def timetable_logic():
    global timetable_old_size3, timetable_old_size1, timetable_old_size2, timetable_old_size4
    start_program = True
    while True:
        hour_biysk = datetime.now(TIME_ZONE).strftime('%H%M%S')
        if int(hour_biysk) in range(100000, 200000) or start_program:
            timetable_old_size1 = comparison_size_bgc(1, timetable_old_size1, start_program)
            timetable_old_size2 = comparison_size_bgc(2, timetable_old_size2, start_program)
            timetable_old_size3 = comparison_size_bgc(3, timetable_old_size3, start_program)
            timetable_old_size4 = comparison_size_bgc(4, timetable_old_size4, start_program)
            sleep(180)
        start_program = False
