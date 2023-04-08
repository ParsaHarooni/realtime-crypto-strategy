# https://github.com/gianlucamalato/machinelearning/blob/master/Fibonacci_Retracements.ipynb
import pandas as pd
import modules.strategies.defaults as defaults
df_data = defaults.df_data

def calculate_swings(df: pd.DataFrame = df_data):
    highest_swing = -1
    lowest_swing = -1

    for i in range(1, df.shape[0] - 1):
        if (
            df["High"][i] > df["High"][i - 1]
            and df["High"][i] > df["High"][i + 1]
            and (highest_swing == -1 or df["High"][i] > df["High"][highest_swing])
        ):
            highest_swing = i

        if (
            df["Low"][i] < df["Low"][i - 1]
            and df["Low"][i] < df["Low"][i + 1]
            and (lowest_swing == -1 or df["Low"][i] < df["Low"][lowest_swing])
        ):
            lowest_swing = i

    return {"highest": highest_swing, "lowest": lowest_swing}


    

def ratio_levels(df:pd.DataFrame = df_data, ratios:list[float] = [0,0.236, 0.382, 0.5 , 0.618, 0.786,1]):
    levels = []

    swings = calculate_swings(df=df)

    max_level = df['High'][swings['highest']]
    min_level = df['Low'][swings['lowest']]
    
    for ratio in ratios:
      if swings['highest'] > swings['lowest']: # Uptrend
        levels.append(max_level - (max_level-min_level)*ratio)
      else: # Downtrend
        levels.append(min_level + (max_level-min_level)*ratio)

    return levels
