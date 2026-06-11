import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nfl_team import Nfl_Team

class NflGui:
    """ 
    Initiating constants and lists to place within the GUI
    STATS column will expand as new functions on the dataframe are implemented
    In addition to the CHART_TYPES as more comparisons are added.
    """
    TEAMS = [
        "ARI", "ATL", "BAL", "BUF", "CAR", "CHI", "CIN", "CLE",
        "DAL", "DEN", "DET", "GB",  "HOU", "IND", "JAX", "KC",
        "LAC", "LAR", "LV",  "MIA", "MIN", "NE",  "NO",  "NYG",
        "NYJ", "PHI", "PIT", "SEA", "SF",  "TB",  "TEN", "WAS"
    ]
    YEARS = list(range(2009,2018))
    WEEKS = ["All"] + list(range(1,19)) # NFL weeks 
    STATS = ['total_rushing_yards','total_passing_yards','total_defensive_yards','def_sacks','offensive_sacks_allowed']
    CHART_TYPES = ['Bar','Line']
    
    def __init__(self,root,filepath):
        """
        This allows the initalization of the GUI as the program size 
        and complexity increases. Graphing abilities might be moved to 
        it's own .py structure
        """
        self.root = root
        self.filepath = filepath
        self.root.title('Nfl Stats')
        self.root.geometry("1024x768") # Can be adjusted as needed
        self._build_controls()
        self._build_chart_area()
        
    def _build_controls(self):
        """
        Tkinter initiated to allow for placement of various buttons within the GUI
        each _var corresponds to constants within NFLGui.
        """
        control_frame = tk.Frame(self.root,bg='white',bd =2,padx=10,pady=10)
        control_frame.pack(side='top',fill='both') 
        
        tk.Label(control_frame,text='Teams:').grid(row=0,column=0,padx=5)
        self.team_var = tk.StringVar(value=self.TEAMS[0]) # Teams are indexed in alphabetical order
        ttk.Combobox(control_frame,textvariable=self.team_var,values=self.TEAMS,state='readonly',width=8).grid(row=0,column=1,padx=5)
        
        tk.Label(control_frame,text='Years:').grid(row=0,column=2,padx=5)
        self.year_var= tk.IntVar(value=2009) # Years are only from 2009 to 2017
        ttk.Combobox(control_frame,textvariable=self.year_var,values=self.YEARS,state='readonly',width=8).grid(row=0,column=3,padx=5)
        
        tk.Label(control_frame,text='Weeks:').grid(row=0,column=4,padx=5)
        self.week_var = tk.StringVar(value='All')
        ttk.Combobox(control_frame,textvariable=self.week_var,values=self.WEEKS,state='readonly',width=8).grid(row=0,column=5,padx=5)
        
        tk.Label(control_frame,text='Stats:').grid(row=0,column=6,padx=5)
        self.stat_var = tk.StringVar(value=self.STATS[0]) # Can change placement of STATS if need be. 
        ttk.Combobox(control_frame,textvariable=self.stat_var,values=self.STATS,state='readonly',width=8).grid(row=0,column=7,padx=5)
        
        tk.Label(control_frame,text='Chart:').grid(row=0,column=8,padx=5)
        self.chart_var = tk.StringVar(value='Line') #Default value for graph
        ttk.Combobox(control_frame,textvariable=self.chart_var,values=self.CHART_TYPES,state='readonly',width=8).grid(row=0,column=9,padx=5)
        
        tk.Button(control_frame,text = "Generate", command=self.generate,bg="#1a3a5c", fg="white", padx=10).grid(row=0, column=10, padx=10)
    def _build_chart_area(self):
        self.fig,self.ax= plt.subplots(figsize=(8,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def generate(self):
        team = self.team_var.get() # Example of Abstraction as .get() is value in tkinter
        year = self.year_var.get()
        week = None if self.week_var.get() == "All" else int(self.week_var.get())
        stat = self.stat_var.get()
        chart_type = self.chart_var.get()
    
        nfl = Nfl_Team(team,self.filepath,year,week)
        data = getattr(nfl,stat)() # Instead of using IF/ELSE 
  
        self.ax.clear()
        if data is not None: # Keeps from producing an empty graph
            if chart_type == "Line":
                self.ax.plot(data.index,data.values)
            else:
                self.ax.bar(data.index,data.values)
    
        self.ax.set_title(f"{team} - {stat} ({year}, Week:{week or 'All'})")
        self.ax.set_xlabel("Week")
        self.ax.set_xticks(range(1,19))# Changed ticks to correspond to each week. 
        self.ax.set_ylabel(stat.replace("_"," ").title())
        bars = self.ax.bar(data.index, data.values)
        self.ax.bar_label(bars, fmt='%.0f')
        self.canvas.draw()

    