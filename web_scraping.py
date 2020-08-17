from bs4 import BeautifulSoup
import requests
from tkinter import mainloop, Frame, Tk, Label
import time


class Exchange(Frame):
             
    def __init__(self, parent):
        super().__init__(parent)
        url = 'https://www.doviz.com'
        response = requests.get(url)
        page = response.content

        soup = BeautifulSoup(page, 'html.parser')

        name = soup.find_all("span", {"class":"name"})
        value = soup.find_all("span", {"class":"value"})
        change = soup.find_all("div", {"class":"change"})

        #parent = Tk()
        parent.title('Güncel Döviz Kurları')
        parent.geometry('630x60')
        label11 = Label(parent, text = name[0].get_text())
        label11.place(x = 0, y = 0) 

        label12 = Label(parent, text = value[0].get_text())
        label12.place(x = 0, y = 20)

        label13 = Label(parent, text = change[0].get_text().lstrip())
        label13.place(x = 0, y = 40)

        label21 = Label(parent, text = name[1].get_text())
        label21.place(x = 80, y = 0) 

        label22 = Label(parent, text = value[1].get_text())
        label22.place(x = 80, y = 20)

        label23 = Label(parent, text = change[1].get_text().lstrip())
        label23.place(x = 80, y = 40)

        label31 = Label(parent, text = name[2].get_text())
        label31.place(x = 160, y = 0) 

        label32 = Label(parent, text = value[2].get_text())
        label32.place(x = 160, y = 20)

        label33 = Label(parent, text = change[2].get_text().lstrip())
        label33.place(x = 160, y = 40)

        label41 = Label(parent, text = name[3].get_text())
        label41.place(x = 240, y = 0) 

        label42 = Label(parent, text = value[3].get_text())
        label42.place(x = 240, y = 20)

        label43 = Label(parent, text = change[3].get_text().lstrip())
        label43.place(x = 240, y = 40)

        label51 = Label(parent, text = name[4].get_text())
        label51.place(x = 320, y = 0) 

        label52 = Label(parent, text = value[4].get_text())
        label52.place(x = 320, y = 20)

        label53 = Label(parent, text = change[4].get_text().lstrip())
        label53.place(x = 320, y = 40)

        label61 = Label(parent, text = name[5].get_text())
        label61.place(x = 400, y = 0) 

        label62 = Label(parent, text = value[5].get_text())
        label62.place(x = 400, y = 20)

        label63 = Label(parent, text = change[5].get_text().lstrip())
        label63.place(x = 400, y = 40)

        label71 = Label(parent, text = name[6].get_text())
        label71.place(x = 480, y = 0) 

        label72 = Label(parent, text = value[6].get_text())
        label72.place(x = 480, y = 20)

        label73 = Label(parent, text = change[6].get_text().lstrip())
        label73.place(x = 480, y = 40)

        label81 = Label(parent, text = name[7].get_text())
        label81.place(x = 560, y = 0) 

        label82 = Label(parent, text = value[7].get_text())
        label82.place(x = 560, y = 20)

        label83 = Label(parent, text = change[7].get_text().lstrip())
        label83.place(x = 560, y = 40)

        #time.sleep(10)
        parent.update_idletasks()
        #parent.after(1000, self.get_price)


if __name__ == '__main__':
    window = Tk()
    run = Exchange(window)
    window.mainloop()