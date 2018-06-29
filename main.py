# -*- coding: utf-8 -*-

import imaplib
import email
import datetime
import scripts

label_save = [u'DBF', u'DBF/RSHB', u'DBF/VSE_PL', u'DBF/POST', u'DBF/KVITOSHA',
                  u'DBF/1_ISSILKUL', u'DBF/2_KALACHINSK', u'DBF/3_LUBINSK', u'DBF/4_MUROMCEVO', u'DBF/5_POLTAVKA',
                  u'DBF/6_RUSSKAYA_POL', u'DBF/7_TAVRICHESKII', u'DBF/8_TARSKII', u'DBF/9_TEVRIZ', u'DBF/10_TUKALINSK']
list_rashireniy = [u'.csv', u'.dbf', u'.7z', u'.zip',u'.rar']

label_save = [] #yours label from get letters
list_rashireniy=[] #yours expansion files which need save

date_now = str(datetime.date.today().strftime("%d.%m.%Y"))

login = u"YOURgmail"
password = u"YOURpassword"
imap = imaplib.IMAP4_SSL(u'imap.gmail.com')
enter = imap.login(login, password)

for label in label_save:
    scripts.get_list_label(imap, label, list_rashireniy)

imap.logout()
