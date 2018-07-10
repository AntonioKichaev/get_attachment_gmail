# -*- coding: utf-8 -*-
from email.header import decode_header
import os
from pathlib import Path
import datetime
import sys
import email
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def save_attachment(msg, list_raz, label_when_save, get_imap, msg_id, download_folder="tmp", ):
    date_now = str(datetime.date.today().strftime("%d.%m.%Y"))  # #текущая дата

    try:
        download_folder = download_folder + "/" + date_now + "/" + label_when_save + "/"  # каждый день новая папка
        os.makedirs(download_folder)  # пытаюсь ее сделать если нет

    except:
        # папка есть
        # download_folder = download_folder + "/" + date_now + "/" + label_when_save + "/"
        pass

    """
    Given a message, save its attachments to the specified
    download folder (default is /tmp)

    return: file path to attachment
    """

    msg_date_give = msg['Date']  # дата когда пришло письмо

    msg_from_give_list = msg['From']  # кто прислал
    msg_title_give = msg['Subject']  # заголовок письма

    att_path = "No attachment found."
    for part in msg.walk():
        count_file = 0
        if part.get('Content-Disposition') is None:
            continue
        if part.get_filename():
            filename = decode_header(part.get_filename())[0][0]
        try:
            filename = filename.decode("utf-8")

        except:

            pass

        att_path = os.path.join(download_folder)
        file_logs = u'logs.txt'
        file_logs_brak = u'logs_BRAK.txt'
        dir_save_logs = u'tmp/' + date_now + u"/"

        if os.path.exists(dir_save_logs + file_logs):
            open(dir_save_logs + file_logs, u'a').close()

        # if not os.path.isfile(att_path):

        file_name_get_part = decode_header(part.get_filename())[0][0]
        msg_from_give = msg_from_give_list.split(u"?")
        who_from = msg_from_give[-1].replace("=", '').replace(" ", "").replace("<", "").replace(">", "").replace(
            "\r\n\t", "")  # кто отправил
        get_title_list = decode_header(msg_title_give)
        get_title = get_title_list[0][0]  # .decode(text[0][1])

        try:
            get_title = get_title.decode(str(get_title_list[0][1]))
            # get_title = get_title.encode('cp1251')
            filename = filename.decode(get_title_list[0][1])
        except:
            pass
        write_text = u"Date_download:\t{}\tLabel:\t{}\tFrom:\t{}\tDate_email:\t{}\tTitel:\t{}\t".format(datetime.datetime.now(), label_when_save,who_from, msg_date_give,
                                                                                            get_title)
        # print filename.decode(get_title_list[0][1])
        try:
            filename = filename.encode("utf-8")
        except:
            filename = filename.decode(decode_header(part.get_filename())[0][1])

        if (Path(filename.encode("utf-8")).suffix.lower() in list_raz) == True:
            filename = file_exists(filename, att_path, count_file)

            write_to_file_txt(file_logs, dir_save_logs, 'a', write_text + "\tFiels_is:\t" + filename)
            fp = open(att_path + filename, u'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            get_imap.store(msg_id, '+FLAGS.SILENT', '\SEEN')
            print att_path + filename
        else:
            filename = file_exists(filename, att_path + u"brak/", count_file)
            write_to_file_txt(file_logs_brak, dir_save_logs, 'a',
                              write_text + "\tFiels is: BRAK\t" + filename)
            try:
                os.makedirs(att_path + u"brak/")
            except:
                pass
            fp = open(att_path + u"brak/" + filename, u'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
            print att_path + filename

    return att_path + filename


def get_list_label(this_imap, label_select, list_rashireniy):  # лист не прочитанных писем
    this_imap.select(label_select)

    status = this_imap.search(None, 'ALL', '(UNSEEN)')[1]
    for msg in status:
        all_number_messages = msg.split()
    for number in all_number_messages:

        st, msg_data = this_imap.fetch(number, '(RFC822)')  # загружаю письмо для обработки

        who_is_content_type = type_email(msg_data)  # Записываю Counter-type
        raw_email = msg_data[0][1]  # беру чистое письмо
        email_msg = email.message_from_string(raw_email)  # превратил в строки
        if who_is_content_type == "multipart/mixed":
            # пришел с вложениями
            save_attachment(email_msg, list_rashireniy, label_select, this_imap, number)
        else:
            this_imap.store(number, '-FLAGS.SILENT', '\SEEN')


def write_to_file_txt(file_name, dir_path, mode, text):
    fp = open(dir_path + file_name, mode)  # запись в файл
    fp.write(str(text + u"\r"))
    fp.close()


def type_email(message_date):
    email_msg = email.message_from_string(message_date[0][1])  # raw_msg_str)
    who_is_content_type = email_msg['Content-Type'].split(";")
    return who_is_content_type[0]


def file_exists(file_name, folder, count_file):
    if os.path.exists(folder + file_name):
        if count_file == 0:
            file_name = file_name.replace(Path(file_name.encode('utf-8')).suffix,
                                          '(' + str(count_file + 1) + ')' + Path(file_name.encode('utf-8')).suffix)

        file_name = file_name.replace('(' + str(count_file - 1) + ')', '(' + str(count_file) + ')')
        count_file += 1
        # file_name = file_name.replace("(\w)", "(" + str(count_file) + ")" + Path(file_name.encode("utf-8")).suffix)
        file_name = file_exists(file_name, folder, count_file)

    return file_name
