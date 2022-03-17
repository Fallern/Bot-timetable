import Vk_bot
import update_logic
from threading import Thread
from time import sleep


def main():
    thread_message_processing = Thread(target=Vk_bot.message_processing, args=())
    thread_data_from_timetable = Thread(target=update_logic.timetable_logic, args=())
    thread_data_from_timetable.start()
    # после включение период ожидания, для выполнения первым потоком всех начальных заданий, что бы не возникли
    # конфликты
    sleep(120)
    thread_message_processing.start()


if __name__ == '__main__':
    main()
