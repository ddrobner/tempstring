import pandas as pd
from numpy import zeros
from debugtools import memoryprofile

@memoryprofile
def fill_blank_timestamps(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Fills missing timestamps for when the detector is online

    Args:
        dataframe (pd.DataFrame): The dataframe to fill 

    Returns:
        pd.DataFrame: The filled dataframe 
    """

    # copying as to not modify the dataframe stored in the sensor object from this function, instead taking it as a return
    df = dataframe
    dt_series = pd.DatetimeIndex(dataframe["Timestamp"]).tz_localize(None)
    # going to generate a dataframe at the missing dates with all 0's for temperature data and merge the dataframes
    for t in range(len(df["Timestamp"])-1):
        # so great that pandas lets you just subtract dates, love how lazy python lets you be
        if dt_series[t+1] - dt_series[t] > pd.Timedelta(1, "day"):
            missing_dates = pd.date_range(dt_series[t].tz_localize("America/Toronto"), dt_series[t+1].tz_localize("America/Toronto"), freq="10T")
            zeros_df = pd.DataFrame({"Timestamp":missing_dates, "Sensor Index":df["Sensor Index"][:len(missing_dates)], "Temperature":zeros(len(missing_dates))})
            df = pd.concat([df, zeros_df]).sort_values(by="Timestamp")
    return df

@memoryprofile
def offset_sensor_indices(ts_start: pd.Timestamp, ts_end: pd.Timestamp, dataframe: pd.DataFrame) -> pd.DataFrame:
    """Sensor index offset for the cavity string

    Args:
        ts_start (pd.Timestamp): Start of the time range to offset
        ts_end (pd.Timestamp): End of the time range to offset 
        dataframe (pd.DataFrame): The data we are working with

    Returns:
        pd.DataFrame: Original data with offset indices
    """
    # copying for the same reason as above
    df = dataframe
    for t in range(len(df["Sensor Index"])):
        if df["Timestamp"][t].tz_convert("America/Toronto") > ts_start.tz_localize("America/Toronto") and df["Timestamp"][t].tz_convert("America/Toronto")<ts_end.tz_localize("America/Toronto"):
            df["Sensor Index"][t] = df["Sensor Index"][t] + 1
    return df

@memoryprofile
def discard_outliers(data: pd.DataFrame, ceiling: float) -> pd.DataFrame:
    """Discards outlying points

    Args:
        data (pd.DataFrame): The data to be processed`
        ceiling (float): The maximum value to not be filtered 

    Returns:
        pd.DataFrame: The Filtered data 
    """
    return data[data["Temperature"] <= ceiling].reset_index()