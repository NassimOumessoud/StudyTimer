from argparse import Action
from cgitb import text
from concurrent.futures import thread
from ipaddress import collapse_addresses
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

import time
import threading
import random
import cProfile


class StudyTimer():
    """ Widget used to time study sessions and provide additional tools during studying.
    """
    def __init__(self):
        main = tk.Tk()
        main.title('StudyTimer')
        main.iconbitmap('icons/read_book_study_icon-icons.com_51077.ico')
        main.geometry('350x200')

        self.main = main
        
        #Styles
        background_color = '#5dade2'
        menu_color = '#DAF7A6'
        self.title_text = Font(family='Times New Roman', size=20, weight='bold')
        self.menu_text = Font(family='Times New Roman', size=10, weight='bold')

        self.main.config(bg=background_color)

        title_style = ttk.Style()
        title_style.theme_use("default")
        title_style.configure('TLabel', background=background_color, font=self.title_text)

        self.menu_style = ttk.Style()
        self.menu_style.configure('Menu.TLabel', background=menu_color, font=self.menu_text)

        spinboxstyle = ttk.Style()
        spinboxstyle.theme_use('default')
        spinboxstyle.configure('My.TSpinbox', arrowsize=20) 
        self.spinfont = Font(family='Times New Roman', size=20, weight="bold")

        self.setup_widget()
        self.create_menu(items={'Exit': self.main.destroy,'Music': None, 'Timer': pass})

        main.mainloop()
        

    def setup_widget(self):
        #Widget setup
        study_default = 25
        break_default = 5
        interval_default = '4'

        self.welcome = self.create_label(text="Welcome to your study timer!", style="TLabel")

        self.setupFrame = ttk.Frame(self.main, style='TLabel', padding=10)
        self.setupFrame.grid(column=0, row=1)
        
        self.create_label(frame=self.setupFrame, text="Study minutes", style='Menu.TLabel', grid=(1,0))
        self.high = ttk.Spinbox(self.setupFrame, from_=0, to=60, width=2, style='My.TSpinbox', font=self.spinfont)
        self.high.grid(column=1, row=1, sticky="W")
        self.high.set(study_default)

        self.create_label(frame=self.setupFrame, text="Break minutes", style='Menu.TLabel', grid=(2,0))
        self.low = ttk.Spinbox(self.setupFrame, from_=0, to=60, width=2, style='My.TSpinbox', font=self.spinfont)
        self.low.grid(column=1, row=2, sticky="W")
        self.low.set(break_default)

        self.create_label(frame=self.setupFrame, text="Amount of intervals", style='Menu.TLabel', grid=(3,0))
        self.intervals = ttk.Entry(self.setupFrame, width=1, font=self.spinfont)
        self.intervals.insert(0, interval_default)
        self.intervals.grid(column=1, row=3, sticky="W")


        ttk.Button(self.setupFrame, text="Start", command=threading.Thread(target=self.init_countdown).start).grid(column=0, row=5)
        ttk.Button(self.setupFrame, text="Exit", command=self.main.destroy).grid(column=1, row=5)


    def create_menu(self, items={}):
        from tkinter import Menu
        menubar = Menu(self.main)
        self.main.config(menu=menubar)

        menu_file = Menu(menubar)

        for item in items:
            menubar.add_command(label=item.key, command=item.value)


    def create_label(self, frame=None, text='', style='TLabel', grid=(0,0), packing=False):

        if frame == None:
            frame = self.main

        label = ttk.Label(frame, text=text, style=style)

        if packing:
            label.pack()
        else: 
            label.grid(row=grid[0], column=grid[1], sticky="W")

        return label

       

    def countdown(self, value, intro_line, study=True):
        
        self.label = self.create_label(frame=self.countdownFrame, text=f"{value} : 59", style='TLabel', grid=(0,2))
        secs = 59
        while True:
            self.label.config(text=f"{value} : {secs}")      
            time.sleep(1)
            secs -= 1

            if secs == 0:
                if value == 0:
                    return
                value -= 1
                secs = 59


    def init_countdown(self):
        self.setupFrame.grid_forget()
        self.welcome.grid_forget()


        intervals = int(self.intervals.get())
        study = int(self.high.get()) - 1
        pause = int(self.low.get()) - 1

        study_lines = ["Let's start!","Let the learning begin."]
        break_lines = ["Good study, have a break!",
                        "Nice job, you deserve a break!",
                        "It's time for a break"]

        study_line = random.choice(study_lines)
        break_line = random.choice(break_lines)

        self.countdownFrame = ttk.Frame(self.main)
        self.countdownFrame.grid(column=1, row=1)

        for interval in range(intervals):
            
            interval += 1
            self.countdown_Label = ttk.Label(self.countdownFrame, text="Study time left -").grid(row=0, column=0)
            self.countdown(study, study_line)

            self.countdown_Label.config(text="Break time left -").grid(row=0, column=0)
            self.countdown(pause, break_line, study=False)


            if interval == intervals:
                print(f"Congratulations! you've studied for {round((study+pause)*intervals/60, 1)} hours!")
                self.countdownFrame.destroy()
                self.welcome.grid()
                self.setupFrame.grid()
                break
        


StudyTimer()

