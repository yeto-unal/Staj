from tkinter import * 


names = ['deneme', 'test', 'programlama']
values = ['10', '20', '30']
change = ['%3', '%5', '%6']

window = Tk()
window.title('Güncel Döviz Kurları')
window.geometry('470x320')
label1 = Label(window, text = names[0])
label1.place(x = 0, y = 0) 

label2 = Label(window, text = values[0])
label2.place(x = 0, y = 20)

label3 = Label(window, text = change[0])
label3.place(x = 0, y = 40)
window.mainloop()