import pandas as pd
from copy import copy
from numpy import nan

def fill_blank_timestamps(dataframe: pd.DataFrame) -> pd.DataFrame:
    # copying as to not modify the dataframe stored in the sensor object from this function, instead taking it as a return
    df = copy(dataframe)
    dr = pd.date_range(start=df["Timestamp"].min(), end=df["Timestamp"].max(), freq="15Min")
    df.set_index('Timestamp').reindex(dr).fillna(0.0).rename_axis("Timestamp").reset_index()
    print(df)
    return df