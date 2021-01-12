from tkinter import *
from tkinter import filedialog
from naraTest import processID


def str_to_sort_list(event):
    naID = int(naIdInput.get())
    spread = int(spreadInput.get())
    if folder_path.get() == '':
        try:
            processID(naID, spread)
        except NameError:
            dialog.set('Wrong directory, try to delete previous results')
    else:
        try:
            processID(naID, spread, path=folder_path.get())
        except NameError:
            dialog.set('Wrong directory, try to delete previous results')


def browse_button():
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)


root = Tk()

l1 = Label(text="Input naID")
naIdInput = Entry(width=40)
l2 = Label(text="Input spread")
spreadInput = Entry(width=40)
l3 = Label(text="Input directory for download (leave empty to download in current directory")
directoryInput = Entry(width=40)
but = Button(text="Parse")
folder_path = StringVar()
lbl1 = Label(master=root, textvariable=folder_path)
button2 = Button(text="Browse", command=browse_button)
dialog = StringVar()
lblfin = Label(textvariable=dialog)

but.bind('<Button-1>', str_to_sort_list)

l1.pack()
naIdInput.pack()
l2.pack()
spreadInput.pack()
lbl1.pack()
button2.pack()
but.pack()
lblfin.pack()

root.mainloop()
