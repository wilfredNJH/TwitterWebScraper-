import tkinter as tk
import customtkinter
from core.twitterScraper import TwitterScraper

class ScrapingInterface():
    def __init__(self,pMaster):
        # labels
        self.emailLabel = customtkinter.CTkLabel(master = pMaster, text="Email")
        self.emailLabel.place(relx=0.5, rely=0.1,anchor=tk.CENTER)
        self.passwordLabel = customtkinter.CTkLabel(master = pMaster, text="Password")
        self.passwordLabel.place(relx=0.5, rely=0.2,anchor=tk.CENTER)
        self.usernameLabel = customtkinter.CTkLabel(master = pMaster, text="Username")
        self.usernameLabel.place(relx=0.5, rely=0.3,anchor=tk.CENTER)
        self.tagLabel = customtkinter.CTkLabel(master = pMaster, text="#TAG")
        self.tagLabel.place(relx=0.5, rely=0.4,anchor=tk.CENTER)
        self.browserLabel = customtkinter.CTkLabel(master = pMaster, text="Browser Options : 1 - Chrome , 2 - Edge, 3 - Firefox")
        self.browserLabel.place(relx=0.5, rely=0.5,anchor=tk.CENTER)
        self.iterationsLabel = customtkinter.CTkLabel(master = pMaster, text="Number of Iterations")
        self.iterationsLabel.place(relx=0.5, rely=0.6,anchor=tk.CENTER)

        # entrys 
        self.email = tk.StringVar()
        self.emailEntry = tk.Entry(master=pMaster,textvariable=self.email,width=15)
        self.emailEntry.place(relx=0.5, rely=0.15,anchor=tk.CENTER)
        self.password = tk.StringVar()
        self.passwordEntry = tk.Entry(master=pMaster,textvariable=self.password,width=15)
        self.passwordEntry.place(relx=0.5, rely=0.25,anchor=tk.CENTER)
        self.username = tk.StringVar()
        self.usernameEntry = tk.Entry(master=pMaster,textvariable=self.username,width=15)
        self.usernameEntry.place(relx=0.5, rely=0.35,anchor=tk.CENTER)
        self.tag = tk.StringVar()
        self.tagEntry = tk.Entry(master=pMaster,textvariable=self.tag,width=15)
        self.tagEntry.place(relx=0.5, rely=0.45,anchor=tk.CENTER)
        self.browserOption = tk.IntVar()
        self.browserOptionEntry = tk.Entry(master=pMaster,textvariable=self.browserOption,width=15)
        self.browserOptionEntry.place(relx=0.5, rely=0.55,anchor=tk.CENTER)
        self.iterations = tk.IntVar()
        self.iterationsEntry = tk.Entry(master=pMaster,textvariable=self.iterations,width=15)
        self.iterationsEntry.place(relx=0.5, rely=0.65,anchor=tk.CENTER)

        # buttons 
        self.buttonRun = customtkinter.CTkButton(master=pMaster, text="run", command=self.run)
        self.buttonRun.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.buttonClear = customtkinter.CTkButton(master=pMaster, text="Clear", command=self.clear)
        self.buttonClear.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        # Create a BooleanVar to store the state of the checkbox
        self.isUsernameVerChecked = tk.BooleanVar()
        self.isUsernameVerChecked.set(False)
        
        # Create the checkbox with the BooleanVar as the variable parameter
        self.checkBox = tk.Checkbutton(master=pMaster, text="2nd Username Verification?", variable=self.isUsernameVerChecked)
        self.checkBox.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def run(self):
        # input run the web scraper 
        self.twitterScraper = TwitterScraper(self.email.get(),self.password.get(),self.username.get(),self.tag.get(),
                                             self.isUsernameVerChecked.get(),self.browserOption.get())
        self.twitterScraper.scrape_data(self.iterations.get())
        self.twitterScraper.save_data()
        
    def clear(self):
        self.email.set('')
        self.password.set('')
        self.username.set('')
        self.tag.set('')
        self.iterations.set('')
        


