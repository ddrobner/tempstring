import pandas as pd
from copy import copy
from numpy import nan

def fill_blank_timestamps(dataframe: pd.DataFrame) -> pd.DataFrame:
    #return dataframe
    # TODO only fill in when > 1D is missing
    # copying as to not modify the dataframe stored in the sensor object from this function, instead taking it as a return
    df = copy(dataframe)
    df = df.set_index("Timestamp").sort_index().asfreq(freq="Min").reset_index()
    return df