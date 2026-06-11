import pandas as pd
import re
from functools import lru_cache

RUN_DIRECTIONS = [
    'up the middle',
    'left end', 'right end',
    'left tackle', 'right tackle',
    'left guard', 'right guard',
    'scrambles right end', 'scrambles left end']
pattern = '|'.join(RUN_DIRECTIONS)
@lru_cache(maxsize=None)
def load_raw_data(filepath):
    """
    On first pass through it was reloading CSV each time, caching allows for a quicker response
    This is the first iteration through this project as it expands and its functionality is increased
    several functions call for Series, which will be replaced with Dataframes to expand functionality
    """
    return pd.read_csv(filepath)
    
    
class Nfl_Team:
    """
    Used to initialize NFL teams from a CSV file from years 2009-2017
    filepath is initialized to determine where the file is located, week currently is
    an optional but seeing as most of the file relies on week being in, may become required
    """
    def __init__(self,team,filepath,year,week=None):
        self.team = team
        
        df = load_raw_data(filepath).copy() # calling for .copy() keeps lru_cache from crashing due to mutable objects.
        self.df_home = df[df["home_team"] == self.team]
        self.df_away = df[df["away_team"] == self.team]
        self.combined_df = pd.concat([self.df_home,self.df_away],ignore_index = True).copy()
        nfl_week = pd.to_datetime(self.combined_df['game_date'])
        self.combined_df['year'] = nfl_week.dt.year
        self.combined_df['week'] = self.combined_df.groupby('year')['game_date'].rank(method='dense').astype(int)
        self.combined_df = self.combined_df[self.combined_df['year']==year]
        if week is not None:
            self.combined_df = self.combined_df[self.combined_df['week'] == week]
    def total_rushing_yards(self):
        filtered = self.combined_df[self.combined_df['desc'].apply(self.is_run_play)].copy()
        filtered['rush_yards'] = filtered['desc'].apply(self.extract_run_yards)
        run_team = filtered['posteam'] == self.team
        return filtered[run_team].groupby('week')['rush_yards'].sum()
        
        
        
    def is_run_play(self,desc):
        """
        Allows a boolean mask to iterate over based upon constants initiated before the class
        """
        if pd.isna(desc):
            return False
        return bool(re.search(pattern,desc, re.IGNORECASE))
        
    def extract_run_yards(self,desc):
        """
        iterates over the 'desc' column within the CSV to pull out
        actual numbers. There is a run column, this was used to help
        understand regex.
        """
        if re.search(r'no gain', desc, re.IGNORECASE):
            return 0
        match = re.search(r'for (-?\d+) yard', desc, re.IGNORECASE)
        return int(match.group(1)) if match else None
            
            
    
    def total_passing_yards(self):
        """
        pos_team is initiated to remove intercepted balls or incomplete passes. Column completed pass is == 1
        may be replaced with a constant to keep DRY code from duplication
        """
        self.combined_df["total_passing_yards"] = self.combined_df[["air_yards","yards_after_catch"]].sum(axis=1)
        pos_team = (self.combined_df['posteam'] == self.team) & (self.combined_df["complete_pass"] == 1)
        return self.combined_df[pos_team].groupby('week')["total_passing_yards"].sum()
       
    
    def def_sacks(self):
        """
        Grouping by week allows the series to plot with the index,values in NFLGui
        """
        return self.combined_df[self.combined_df["defteam"]==self.team].groupby('week')['sack'].sum()
    def offensive_sacks_allowed(self):
        return self.combined_df[self.combined_df["posteam"]==self.team].groupby('week')['sack'].sum()
    
    def total_defensive_yards(self):
        """
        isin utilized as the column has 10 different variations on play_type
        """
        play_type = self.combined_df[self.combined_df['play_type'].isin(['pass', 'run', 'qb_kneel'])]
        return play_type[play_type["defteam"]==self.team].groupby('week')['yards_gained'].sum()
  
        
    
        
        
        