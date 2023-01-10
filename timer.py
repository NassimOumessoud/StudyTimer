from argparse import Action
from cgitb import text
from concurrent.futures import thread
from ipaddress import collapse_addresses
from msilib.schema import Class
import tkinter as tk
from tkinter import HORIZONTAL, ttk
from tkinter.font import Font
from PIL import Image

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
        main.geometry('420x200')
        self.main = main

        tk.Grid.rowconfigure(self.main,0,weight=1)
        tk.Grid.columnconfigure(self.main,0,weight=1)
    
        #tk.Grid.rowconfigure(self.main,1,weight=1)

        self.style()
        self.timer = False
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
        self.welcome = self.create_label(text="Welcome to your study timer!", style="TLabel")
        #self.image = ImageTK.open('nature.png')
        #self.image.resize((420, 200))
        #self.canvas = tk.Canvas(self.main)
        #self.canvas.grid(row=0, column=0)
        #self.canvas.create_image(0, 0, image=self.image)


    def setup_timer(self):
        if self.timer:
            print('Studytimer is already active.')
            return

        study_default = 25
        break_default = 5
        interval_default = '4'
        self.setupFrame = ttk.Frame(self.main, style='TLabel',  padding=10)
        self.setupFrame.grid(column=0, row=1, sticky='W')

        self.welcome.config(text="How long would you like to study?")
        
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
        
        progressbar = ttk.Progressbar(self.countdownFrame, orient=HORIZONTAL,  length=300, maximum=1, value=0)
        progressbar.grid(row=10, column=0, columnspan=5)

        self.label = self.create_label(frame=self.countdownFrame, text=f"{value} : 59", style='TLabel', grid=(0,2))
        
        
        end_time = (value)*60
        progress = 0

        value = value - 1
        secs = 59
        
        while value >= 0:
            current_time = value*60 + secs
            progress = (end_time - current_time)/end_time
            
            progressbar.config(value=progress)
            self.label.config(text=f"{value} : {secs}")     

            time.sleep(1)
            secs -= 1

            if secs == 0:
                value -= 1
                secs = 59

            if progress == .99:      #if progress at 99 percent sound alarm
                self.play_sound('audio/alarm.mp3')


    def play_sound(self, sound_file):
        playsound.playsound(sound_file, block=False)


    def pause(self):
        self.pause = True
        self.pausebutton.config(text="Resume", command=self.pause==False)
        while self.pause:
            print(1)
        print(0)


    def init_countdown(self):
        
        self.timer = True
        intervals = int(self.intervals.get())
        study = int(self.high.get())
        pause = int(self.low.get())

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
        self.pausebutton = ttk.Button(self.countdownFrame, text="Pause", command=self.pause)
        self.pausebutton.grid(column=0, row=1)

        for interval in range(intervals):
            
            interval += 1
            self.countdown_label = self.create_label(frame=self.countdownFrame, text="Study time left -", style='TLabel', grid=(0,0))
            self.countdown(study, study_line)

            if interval == intervals:
                print(f"Congratulations! you've studied for {round((study+pause+2)*intervals/60, 1)} hours!")
                self.countdownFrame.destroy()
                self.timer = False
                self.setup_widget()
                break

            self.countdown_label.config(text="Break time left -")
            self.countdown(pause, break_line, study=False)
        

import cmath


class Calculator():
    def __init__(self):
        main = tk.Tk()
        main.title('Calculator')
        main.geometry('350x200')
        main.iconbitmap('icons/1486395290-09-calculator_80565.ico')
        self.main = main

        self.functions = {'exp': self.exponential, 'der': self.derivative, 'int': self.integral, 'log': self.log, 'ln': self.naturalLog}
        self.symbols = {'i': complex(0, 1), 'j': complex(0, 1), 'pi': cmath.pi, 'Pi': cmath.pi}
        self.decimals = 3

        self.setup()
        main.mainloop()


    def setup(self):
        StudyTimer.style(self)
        self.frame = ttk.Frame(self.main, style='TFrame', padding=20)
        self.frame.pack()

        self.entry = ttk.Entry(self.frame, style='TEntry', width=13)
        self.entry.bind('<Return>', self.calculate)
        self.entry.grid(row=0, column=0)

        button = ttk.Button(self.frame, text='Calculate', width=13, command=self.calculate).grid(row=3, column=0)


    def calculate(self):
        self.equation = self.entry.get()
        self.entry.delete(0, 'end')
        try:
            self.entry.insert(0, eval(self.equation))

        except NameError or SyntaxError as error:
            error = error.args[0].split("'")[1] 
            if error in self.functions.keys():
                self.functions[error]()


    def integral(self):
        pass


    def derivative(self):
        print('do derivative')
        pass


    def exponential(self):
        self.equation = self.equation.split("(")[1][:-1]
        try:
            self.answer = cmath.exp(float(self.equation))
        except:
            for key in self.equation:
                print(key)
                if key in self.symbols.keys():
                    pass
            
                
            print(self.equation)
            self.answer = cmath.exp(float(self.equation))
            self.entry.insert(0, self.answer)


    def log(self):
        self.equation = self.equation.split("(")[1][:-1]
        self.answer = cmath.log10(float(self.equation))
        self.entry.insert(0, self.answer)

    
    def naturalLog(self):
        self.equation = self.equation.split("(")[1][:-1]
        self.answer = cmath.log(float(self.equation))
        self.entry.insert(0, self.answer)


StudyTimer()

