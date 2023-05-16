import pandas as pd
from copy import copy
from numpy import zeros

def fill_blank_timestamps(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Fills missing timestamps for when the detector is online

    Args:
        dataframe (pd.DataFrame): The dataframe to fill 

    Returns:
        pd.DataFrame: The filled dataframe 
    """

    # copying as to not modify the dataframe stored in the sensor object from this function, instead taking it as a return
    df = copy(dataframe)
    # going to generate a dataframe at the missing dates with all 0's for temperature data and merge the dataframes
    for t in range(len(df["Timestamp"])-1):
        # so great that pandas lets you just subtract dates, love how lazy python lets you be
        if df["Timestamp"][t+1].tz_localize(None) - df["Timestamp"][t].tz_localize(None) > pd.Timedelta(1, "day"):
            missing_dates = pd.date_range(df["Timestamp"][t].tz_convert("America/Toronto"), df["Timestamp"][t+1].tz_convert("America/Toronto"), freq="10T")
            zeros_df = pd.DataFrame({"Timestamp":missing_dates, "Sensor Index":df["Sensor Index"][:len(missing_dates)], "Temperature":zeros(len(missing_dates))})
            df = pd.concat([df, zeros_df]).sort_values(by="Timestamp")
    return df

def offset_sensor_indices(timestamp: pd.Timestamp, dataframe: pd.DataFrame) -> pd.DataFrame:
    # copying for the same reason as above
    df = copy(dataframe)
    for t in range(len(df["Sensor Index"])):
        if df["Timestamp"][t].tz_convert("America/Toronto") > timestamp.tz_localize("America/Toronto"):
            df["Sensor Index"][t] = df["Sensor Index"][t] + 1
    return df

def discard_outliers(data: pd.DataFrame, ceiling) -> pd.DataFrame:
    return data[data["Temperature"] < ceiling].reset_index()