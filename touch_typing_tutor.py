# source for the stopwatch: https://stackoverflow.com/questions/31995804/stopwatch-on-tkinter-creating-a-class
import tkinter as tk
from tkinter import messagebox
import numpy as np
import os
import natsort
import shutil
import random
import sys
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

class TypingTutor(tk.Frame):

    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.load_words()
        self.grid()
        self.widgets()
        self.running = False
        self.timer = [60]    # [minutes ,seconds, centiseconds]
        self.timeString = str(self.timer[0])
        self.update_time()


    def load_words(self,type="csv"):
        if type=="csv":
            df = pd.read_csv("words.csv")
            self.words = list(df["word"])
        else:
            with open("words.txt") as words:
                words_dataset = words.readlines()
            self.words = words_dataset


    def widgets(self):
        self.timeFrame = tk.LabelFrame(root, text='Timer')
        self.timeFrame.grid(row=0,column=0)

        self.show_label = tk.Label(self.timeFrame, text='60', font=('Helvetica', 30))
        self.show_label.grid(row=0, column=0)

        self.start_timer_btn = tk.Button(self.timeFrame, text='Start', command=self.start)
        self.start_timer_btn.grid(row=0,column=1)

        self.reset_timer_btn = tk.Button(self.timeFrame, text='Reset', command=self.resetTime)
        self.reset_timer_btn.grid(row=0,column=2)

        self.view_stats_btn = tk.Button(self.timeFrame, text='View Stats', command=self.plot_stats)
        self.view_stats_btn.grid(row=0,column=3)


        self.label_words1 = tk.StringVar()
        self.word_label1 = tk.Label(self.timeFrame, textvariable=self.label_words1,font=("Helvetica", 30))
        self.word_label1.grid(row=1,column=1)

        self.label_words2 = tk.StringVar()
        self.word_label2 = tk.Label(self.timeFrame, textvariable=self.label_words2, font=("Helvetica", 30))
        self.word_label2.grid(row=2,column=1)

        self.evalue = tk.StringVar()
        self.input_text = tk.Entry(self.timeFrame,textvariable=self.evalue, font=("Helvetica", 20))
        self.input_text.grid(row=1,column=3)
        self.timeFrame.bind_all("<space>", self.next_word)

        self.correct_word = tk.StringVar()
        self.correct_label = tk.Label(self.timeFrame, textvariable=self.correct_word, font=("Helvetica", 20),fg="green") 
        self.correct_label.grid(row=2,column=3)

        self.wrong_word = tk.StringVar()
        self.wrong_word_label = tk.Label(self.timeFrame, textvariable=self.wrong_word, font=("Helvetica", 20),fg="red") 
        self.wrong_word_label.grid(row=3,column=3)

        
    def next_word(self, master=None):
        words_compare = []
        self.display_words = self.current_words        
        if str(self.evalue.get()).strip(" ") == self.label_words1.get().split()[0]:
            self.correct_words+=1
            self.correct_word.set("Correct")
            self.wrong_word.set("")
        else:
            self.wrong_word.set("Wrong")
            self.correct_word.set("")

        self.evalue.set("")
        self.display_words.pop(0)
        self.display_words1 = " ".join(self.display_words[0:2])
        self.display_words2 = " ".join(self.display_words[2:])
        if len(self.display_words)>0:
            self.label_words1.set(self.display_words1)
            self.label_words2.set(self.display_words2)
        else:
            self.counter+=6
            self.current_words = self.session_words[self.counter:self.counter+6]
            self.display_words1 = " ".join(self.current_words[0:3])
            self.display_words2 = " ".join(self.current_words[3:])
            self.label_words1.set(self.display_words1)
            self.label_words2.set(self.display_words2)


    def update_time(self):

        if (self.running == True):      #Clock is running

            self.timer[0] -= 1          #Count Down a second

            if (self.timer[0] == 0):     #if seconds is negative
                self.timer[0] = 60      #reset to 60 seconds
                messagebox.showinfo('Message', 'Your score was: {}WPM'.format(self.correct_words))
                save = messagebox.askquestion("Would you like to save your progress?")
                if save=="yes":
                    print("Saving file")
                    if os.path.isfile("scores.csv"):
                        df1 = pd.read_csv("scores.csv",index_col=0)
                        today = self.get_date()
                        df2 = pd.DataFrame({"Score": [self.correct_words], "Date": ["{}".format(today)]})
                        df = df1.append(df2, ignore_index = True) 
                        df.to_csv("scores.csv")
                    else:
                        today = self.get_date()
                        df = pd.DataFrame({"Score": [self.correct_words], "Date": ["{}".format(today)]})
                        df.to_csv("scores.csv")

            self.timeString = str(self.timer[0])
            self.show_label.config(text=self.timeString)
        root.after(1000, self.update_time)


    def start(self):
        self.correct_words = 0
        self.session_words = random.sample(self.words[0:2000], 500)
        self.running = True
        self.counter = 0
        self.current_words = self.session_words[self.counter:self.counter+6]
        self.display_words1 = " ".join(self.current_words[0:2])
        self.display_words2 = " ".join(self.current_words[2:])
        self.label_words1.set(self.display_words1)
        self.label_words2.set(self.display_words2)

    def resetTime(self):        
        self.running = False
        self.timer = [60]
        print('Clock is Reset')
        self.show_label.config(text='60')
        self.correct_words=0

    def get_date(self):
        today = datetime.now()
        year = today.year
        month = today.month
        day = today.day
        date = "{}/{}/{}".format(year, month, day)

        return

    def plot_stats(self):
        if os.path.isfile("scores.csv"):
            df = pd.read_csv("scores.csv")
            x = list(df["Score"])
            plt.plot(x)
            plt.title("WPM Scores")
            plt.ylabel("WPM")
            plt.show()
        else:
            messagebox.showinfo("You do not have the .csv file on this folder")


#CHANGE the path to whatever path is needed
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Welcome to Typing Tutor!")
    start_session = TypingTutor(root)
    root.mainloop()

