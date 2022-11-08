from argparse import Action
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
    def __init__(self, main):
        self.main = main
        
        background_color = '#5dade2'
        menu_color = '#DAF7A6'
        self.title_text = Font(family='Times New Roman', size=20, weight='bold')
        self.menu_text = Font(family='Times New Roman', size=10, weight='bold')
        
        study_default = 25
        break_default = 5
        interval_default = '4'
        
        #Styles
        self.main.config(bg=background_color)

        title_style = ttk.Style()
        title_style.theme_use("default")
        title_style.configure('TLabel', background=background_color, font=self.title_text)

        self.menu_style = ttk.Style()
        self.menu_style.configure('Menu.TLabel', background=menu_color, font=self.menu_text)

        spinboxstyle = ttk.Style()
        spinboxstyle.theme_use('default')
        spinboxstyle.configure('My.TSpinbox', arrowsize=20) 
        
        #Widget
        self.welcome = ttk.Label(self.main, text="Welcome to your study timer!", style="TLabel")
        self.welcome.grid(column=0, row=0)

        self.setupFrame = ttk.Frame(self.main, style='TLabel', padding=10)
        self.setupFrame.grid(column=0, row=1)
        
        self.spinfont = Font(family='Times New Roman', size=20, weight="bold")

        ttk.Label(self.setupFrame, text="Study minutes", style='Menu.TLabel').grid(column=0, row=1, sticky="W")
        self.high = ttk.Spinbox(self.setupFrame, from_=0, to=60, width=2, style='My.TSpinbox', font=self.spinfont)
        self.high.grid(column=1, row=1, sticky="W")
        self.high.set(study_default)

        ttk.Label(self.setupFrame, text="Break minutes", style='Menu.TLabel').grid(column=0, row=2, sticky="W")
        self.low = ttk.Spinbox(self.setupFrame, from_=0, to=60, width=2, style='My.TSpinbox', font=self.spinfont)
        self.low.grid(column=1, row=2, sticky="W")
        self.low.set(break_default)

        ttk.Label(self.setupFrame, text="Amount of intervals", style='Menu.TLabel').grid(column=0, row=3, sticky="W")
        self.intervals = ttk.Entry(self.setupFrame, width=1, font=self.spinfont)
        self.intervals.insert(0, interval_default)
        self.intervals.grid(column=1, row=3, sticky="W")

        print('done')
        ttk.Button(self.setupFrame, text="Start", command=self.init_countdown()).grid(column=0, row=5)
        ttk.Button(self.setupFrame, text="Exit", command=main.destroy).grid(column=1, row=5)
        
       
    def countdown(self, value, intro_line, study=True):
        secs = 59
        
        while value >= 0:
            self.label['text'] = f"{value} : {secs}"      

            time.sleep(1)
            secs -= 1
            if secs == 0:
                value -= 1
                secs = 59


    def init_countdown(self):
        self.setupFrame.grid_forget()
        self.welcome.grid_forget()

        self.countdownFrame = ttk.Frame(self.main)
        self.countdownFrame.grid(column=1, row=1)

        self.study_label = ttk.Label(self.countdownFrame, text="Study time left -")
        self.break_label = ttk.Label(self.countdownFrame, text="Break time left -")


        intervals = int(self.intervals.get())
        study_lines = ["Let's start!","Let the learning begin."]

        break_lines = ["Good study, have a break!",
                        "Nice job, you deserve a break!",
                        "It's time for a break"]

        
        study = int(self.high.get()) - 1
        pause = int(self.low.get()) - 1
        study_line = random.choice(study_lines)
        break_line = random.choice(break_lines)
            
        for interval in range(intervals):
            interval += 1

            self.study_label.grid(column=0, row=0)
            self.study_label.grid_forget()
            self.label = ttk.Label(self.countdownFrame, text=f"{study} : 59", style='TLabel')
            self.label.grid(column=2, row=0) 
            count = threading.Thread(target=self.countdown, args=(study, study_line))
            count.start()
            

            self.break_label.grid(column=0, row=0)
            self.countdown(pause, break_line, study=False)
            self.break_label.grid_forget()

            if interval == intervals:
                study = int(self.high.get())
                pauze = int(self.low.get())
                print(f"Congratulations! you've studied for {round((study+pauze)*intervals/60, 1)} hours!")
                self.countdownFrame.destroy()
                self.welcome.grid()
                self.setupFrame.grid()
                break
        


root = tk.Tk()
root.title('StudyTimer')
root.iconbitmap('icons/read_book_study_icon-icons.com_51077.ico')
root.geometry('350x200')
Timer = StudyTimer(root)
#cProfile.run(Timer.timer())
root.mainloop()