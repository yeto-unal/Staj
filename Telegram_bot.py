from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.ext.dispatcher import Dispatcher
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
import mysql.connector
from bs4 import BeautifulSoup
import requests

uname = None
passw = None
phone_number = None 

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'p3mb3pant3r',
    database = 'banka'
)

mycursor = mydb.cursor(buffered = True)

def start(update, context):
    user = update.message.from_user
    update.message.reply_text("Merhaba " + user['first_name'])
    update.message.reply_text("Bazı komutları kullanabilmeniz için sisteme giriş yapmanız gerekir")
    update.message.reply_text("Yardım için /help komutunu kullanabilirsiniz")

def help(update, context):
    update.message.reply_text("/send [GÖNDERİLECEK TEL. NO.] [GÖNDERİLECEK TUTAR] (para göndermek için)")
    update.message.reply_text("/show (güncel bakiyeyi gösterir)")
    update.message.reply_text("/set [KULLANICI ADI] [ŞİFRE] [TELEFON NUMARASI] (sisteme giriş yapmak için)")
    update.message.reply_text("/exchange (güncel döviz kurlarını gösterir)")

def b_send(update, context):
    to_text = update.message.text
    splitted = to_text.split()
    
    pno = splitted[1]
    cash = splitted[2]
    
    result = send(pno, cash)
    update.message.reply_text(result)

def send(pno, cash):
    text = "Bakiyeniz kafi değil."
    try:
        mycursor.execute("SELECT Balance FROM bot_sql WHERE Phone_no = {0}".format(phone_number)) 
        curr_balance = mycursor.fetchone()
        curr_balance = float(curr_balance[0])
        cash = float(cash)

        if (curr_balance < cash):
            return text

        elif (cash < 0):
            text = "Hortuma izin yok"
            return text    

        else:
            mycursor.execute("UPDATE bot_sql Set Balance = Balance + {0} WHERE Phone_no = {1} ".format(cash, pno))
            mycursor.fetchone()

            mycursor.execute("UPDATE bot_sql Set Balance = Balance - {0} WHERE Phone_no = {1}".format(cash, phone_number))
            mycursor.fetchone()

            mydb.commit()
            text = ("%s telefon numaralı hesaba %.2f TL gönderilmiştir.") % (pno, cash)
            return text
    except mysql.connector.errors.ProgrammingError:
        text = "/send komutunu kullanabilmeniz için giriş yapmanız gerekiyor.\nNasıl giriş yapıldığını öğrenmek için /help komutunu kullanabilirsiniz."
        return text        

def show(update, context):
    """to_text = update.message.text
    splitted = to_text.split()

    pno = splitted[1]"""

    mycursor.execute("SELECT Name, Balance FROM bot_sql WHERE Phone_no = {0}".format(phone_number))
    text = mycursor.fetchone()
    update.message.reply_text(str("%s : %.2f TL") % (text[0], text[1]))

def set_vars(update, context):
    to_text = update.message.text
    splitted = to_text.split()
    mycursor.execute("SELECT * FROM bot_sql WHERE Username = '{0}' AND Password = '{1}' AND Phone_no = '{2}'".format(splitted[1], splitted[2], splitted[3]))
    test = mycursor.fetchone()

    if (test):
        global uname
        uname = splitted[1]
        global passw
        passw = splitted[2]
        global phone_number
        phone_number = splitted[3]
        update.message.reply_text("Sisteme girişiniz başarılı")
    else:
        update.message.reply_text("Lütfen tekrar deneyiniz")

def exchange(update, context):
    url = 'https://www.doviz.com'
    response = requests.get(url)
    page = response.content
    soup = BeautifulSoup(page, 'html.parser')

    name = soup.find_all("span", {"class":"name"})
    value = soup.find_all("span", {"class":"value"})
    
    for i in range(len(name)):
        update.message.reply_text(name[i].get_text() + ": " + value[i].get_text())

def main():
    TOKEN = '<YOUR TOKEN>'
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set", set_vars))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("send", b_send))
    dp.add_handler(CommandHandler("show", show))
    dp.add_handler(CommandHandler("exchange", exchange))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()