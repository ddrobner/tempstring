import pandas as pd
from copy import copy

def fill_blank_timestamps(dataframe: pd.DataFrame) -> pd.DataFrame:
    # returning the original dataframe now until I get back to this
    return dataframe
    # Not sure if this is right, leaving this for later
    # want to try and output some plots first and see what I get
    """
    df = copy(dataframe)
    for i in range(len(df)):
        timestamp_delta = df["Timestamp"][i+1] - df["Timestamp"][i]
        if timestamp_delta > 1:
            for x in range(timestamp_delta):
                # NOTE: assumes sensor index is the same for the whole dataframe
                # it should really be though, just based on how the whole program is structured
                df = df.append({"Timestamp":df["Timestamp"][i]+x, "Sensor Index":df["Sensor Index"][0], "Temperature": 0}, ignore_index=True)
    return df
    """
