# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 19:35:06 2026

@author: gregg
"""
from nfl_gui import NflGui
import tkinter as tk

if __name__ == '__main__':
    FILEPATH = r'C:\Users\gregg\nfl\Nfl_2009_2018.csv'
    root = tk.Tk()
    app = NflGui(root, FILEPATH)
    root.mainloop()