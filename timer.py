from argparse import Action
from cgitb import text
from concurrent.futures import thread
from ipaddress import collapse_addresses
from msilib.schema import Class
import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter.font import Font

import time
import threading
import random
import cProfile
from turtle import bgcolor, width
import playsound


class StudyTimer():
    """ Widget used to time study sessions and provide additional tools during studying.
    """
    def __init__(self):
        main = tk.Tk()
        main.title('StudyTimer')
        main.iconbitmap('icons/read_book_study_icon-icons.com_51077.ico')
        main.geometry('350x200')
        self.main = main

        self.style()
        self.setup_widget()
        self.create_menu(items={"Exit": self.main.destroy, "Calculator": Calculator, "Music": None, "Timer": self.setup_timer, "Notes": None, "Help": None})
        
        main.mainloop()
        

    def style(self):
        #Styles
        self.background_color = '#5dade2'
        menu_color = '#DAF7A6'
        self.title_text = Font(family='Times New Roman', size=20, weight='bold')
        self.menu_text = Font(family='Times New Roman', size=10, weight='bold')

        self.main.config(bg=self.background_color)

        title_style = ttk.Style()
        title_style.theme_use("default")
        title_style.configure('TLabel', background=self.background_color, font=self.title_text)

        frame_style = ttk.Style()
        frame_style.configure(style='TFrame', background=self.background_color)
        self.menu_style = ttk.Style()
        self.menu_style.configure('Menu.TLabel', background=menu_color, font=self.menu_text)

        entry_style = ttk.Style()
        entry_style.configure(style='TEntry', background=self.background_color)

        spinboxstyle = ttk.Style()
        spinboxstyle.theme_use('default')
        spinboxstyle.configure('My.TSpinbox', arrowsize=20) 
        self.spinfont = Font(family='Times New Roman', size=20, weight="bold")


    def setup_widget(self):
        #Widget setup
        self.welcome = self.create_label(text="Welcome to your study timer!", style="TLabel")


    def setup_timer(self):
        study_default = 25
        break_default = 5
        interval_default = '4'
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
        self.intervals = ttk.Entry(self.setupFrame, width=2, font=self.spinfont)
        self.intervals.insert(0, interval_default)
        self.intervals.grid(column=1, row=3, sticky="W")
        
        ttk.Button(self.setupFrame, text="Start", command=threading.Thread(target=self.init_countdown).start).grid(column=0, row=5)


    def create_menu(self, items={}):
        from tkinter import Menu
        menubar = Menu(self.main)
        self.main.config(menu=menubar)

        menu_file = Menu(menubar)

        for item in items:
            menubar.add_command(label=item, command=items[item])


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
        end_time = (value+1)*60
        progressbar = ttk.Progressbar(self.countdownFrame, orient=HORIZONTAL,  length=300, maximum=end_time, value=0)
        progressbar.grid(row=10, column=0, columnspan=5)

        self.label = self.create_label(frame=self.countdownFrame, text=f"{value} : 59", style='TLabel', grid=(0,2))
        secs = 59

        while True:
            current_time = value*60 + secs
            progressbar.config(value=end_time - current_time)
            self.label.config(text=f"{value} : {secs}")      
            time.sleep(1)
            secs -= 1


            if secs == 0:
                if value == 0:
                    self.play_sound('alarm.mp3')
                    return
                value -= 1
                secs = 59


    def play_sound(self, sound_file):
        playsound.playsound(sound_file)


    def init_countdown(self):

        intervals = int(self.intervals.get())
        study = int(self.high.get()) - 1
        pause = int(self.low.get()) - 1

        self.setupFrame.destroy()
        self.welcome.destroy()

        study_lines = ["Let's start!","Let the learning begin."]
        break_lines = ["Good study, have a break!",
                        "Nice job, you deserve a break!",
                        "It's time for a break"]

        study_line = random.choice(study_lines)
        break_line = random.choice(break_lines)

        self.countdownFrame = ttk.Frame(self.main, style='TLabel', padding=10)
        self.countdownFrame.grid(column=1, row=1)

        for interval in range(intervals):
            
            interval += 1
            self.countdown_label = self.create_label(frame=self.countdownFrame, text="Study time left -", style='TLabel', grid=(0,0))
            self.countdown(study, study_line)

            self.countdown_label.config(text="Break time left -")
            self.countdown(pause, break_line, study=False)


            if interval == intervals:
                print(f"Congratulations! you've studied for {round((study+pause)*intervals/60, 1)} hours!")
                self.countdownFrame.destroy()
                self.setup_timer()
                break
        


class Calculator():
    def __init__(self):
        main = tk.Tk()
        main.title('Calculator')
        main.geometry('350x200')
        self.main = main

        StudyTimer.style(self)
        self.frame = ttk.Frame(self.main, style='TFrame', padding=20)
        self.frame.pack()

        self.equation = ttk.Entry(self.frame, style='TEntry', width=13)
        self.equation.bind('<Return>', self.calculate)
        self.equation.grid(row=0, column=0)

        button = ttk.Button(self.frame, text='Calculate', width=13, command=self.calculate).grid(row=3, column=0)
        main.mainloop()


    def calculate(self):
        equation = self.equation.get()
        self.equation.delete(0, 'end')
        self.equation.insert(0, eval(equation))



StudyTimer()

