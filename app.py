import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = (
    "Motor_Vehicle_Collisions_-_Crashes.csv"
)

n_injured_col = "number of persons injured"

def main():
    st.title("Motor Vehicle Collisions")
    
    df = load_data(100000)
    n_max_injured = int(df[n_injured_col].max())
    n_min_injured = int(df[n_injured_col].min())
            
    st.header("Where are the most people injured in NYC?")
    injured_people = st.slider("No. persons injured", min_value=n_min_injured, max_value=n_max_injured)
    injured_people_df = df.query("`number of persons injured` >= @injured_people")
    injured_people_lonlat_df = injured_people_df[["latitude", "longitude"]]
    injured_people_lonlat_df = injured_people_lonlat_df.dropna(how="any")
    st.map(injured_people_lonlat_df)
    
    widget_show_raw_data(df)


def widget_show_raw_data(df):
    if st.checkbox("Show Raw Data", False):
        st.subheader("Raw Data")
        st.write(df)


@st.cache_resource()
def load_data(nrows: int = None):
    df = pd.read_csv(DATA_URL, nrows=nrows)
    df.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
    lowercase = lambda colname: str(colname).lower()
    df.rename(lowercase, axis='columns', inplace=True)
    df.rename(columns={"crash_date_crash_time": "date_time"}, inplace=True)
    return df
    


if __name__ == "__main__":
    main()
    