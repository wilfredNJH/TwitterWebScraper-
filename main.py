import customtkinter
import tkinter
from tkinter import ttk

# panels
from panels.scrapingInterface import ScrapingInterface


class MyGUI:
    def __init__(self):
        self.app = customtkinter.CTk()
        
        self.init_customizations()
        self.init_menubar()

        # create a notebook
        notebook = ttk.Notebook(self.app)
        notebook.pack(fill="both", expand=True)

        # panels
        self.frameExcelWorkbook = customtkinter.CTkFrame(master=notebook)
        self.excelWorkook = ScrapingInterface(self.frameExcelWorkbook)

        notebook.add(self.frameExcelWorkbook, text='Twitter Web Scraper')

        self.app.mainloop()

    def init_menubar(self):
        self.menubar = tkinter.Menu(self.app,background="blue")
        self.filemenu = tkinter.Menu(self.menubar, tearoff = 0)
        self.filemenu.add_command(label= "Close", command=quit)
        self.actionmenu = tkinter.Menu(self.menubar,tearoff=0)
        self.actionmenu.add_command(label = "Show Message")
        
        self.menubar.add_cascade(menu=self.filemenu,label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Action")
        
        self.app.config(menu=self.menubar)

    def init_customizations(self):
        # Setting the appearance and theme of the GUI window
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue") 

        # Setting the dimensions and defining the custom tkinter function
        self.app.wm_title("Twitter Web Scraper")
        width= self.app.winfo_screenwidth()               
        height= self.app.winfo_screenheight()               
        self.app.geometry("%dx%d" % (width, height))
        self.app.state('zoomed')



MyGUI()