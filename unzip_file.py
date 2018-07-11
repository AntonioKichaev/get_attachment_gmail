# -*- coding: utf-8 -*-
import zipfile
import os
import glob
import datetime
import rarfile

date_now = str(datetime.date.today().strftime("%d.%m.%Y"))


def main():
    unzin_from_label(writeYourlabel)


def unzin_from_label(label):
    path_default = u"tmp/" + date_now + label
    pwd = u'YOURpwd'

    get_unzip(path_default, pwd)



def get_unzip(path_default, pwd):
    list_file = glob.glob(path_default + u"*.zip")

    if list_file:
        for file_name in list_file:
            unzipper = zipfile.ZipFile(file_name)
            unzipper.extractall(path_default, pwd=pwd)
            unzipper.close()
            os.remove(file_name)
