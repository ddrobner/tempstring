import pandas as pd
from copy import copy
from numpy import zeros

def fill_blank_timestamps(dataframe: pd.DataFrame) -> pd.DataFrame:
    #return dataframe
    # TODO only fill in when > 1D is missing
    # copying as to not modify the dataframe stored in the sensor object from this function, instead taking it as a return
    df = copy(dataframe)
    # this is a clever solution but I only want to fill in missing dates
    #df = df.set_index("Timestamp").sort_index().asfreq(freq="Min").reset_index()
    # so here, I'm going to generate a dataframe at the missing dates with all 0's for temperature data and merge the dataframes
    for t in range(len(df["Timestamp"])-1):
        # so great that pandas lets you just subtract dates, love how lazy python lets you be
        if df["Timestamp"][t+1] - df["Timestamp"][t] > pd.Timedelta(1, "day"):
            missing_dates = pd.date_range(df["Timestamp"][t], df["Timestamp"][t+1], freq="D")
            zeros_df = pd.DataFrame({"Timestamp":missing_dates, "Sensor Index":df["Sensor Index"][:len(missing_dates)], "Temperature":zeros(len(missing_dates))})
            df = pd.concat([df, zeros_df]).sort_values(by="Timestamp")
    return df