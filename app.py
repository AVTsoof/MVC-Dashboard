import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = (
    "Motor_Vehicle_Collisions_-_Crashes.csv"
)

N_INJURED_COL = "NUMBER OF PERSONS INJURED"

def main():
    st.title("Motor Vehicle Collisions")
    
    df = load_data(100000)
    widget_show_raw_data(df)
    widget_show_2d_map(df)
    widget_show_3d_map(df)
    
    
def widget_show_raw_data(df):
    if st.sidebar.checkbox("Show Raw Data", False):
        st.subheader("Raw Data")
        st.write(df)


def widget_show_2d_map(df):
    n_max_injured = int(df[N_INJURED_COL].max())
    n_min_injured = int(df[N_INJURED_COL].min())
    
    injured_people = st.sidebar.slider("No. persons injured", min_value=n_min_injured, max_value=n_max_injured)
    
    df_subset = df.query(F"`{N_INJURED_COL}` >= @injured_people")
    
    if st.sidebar.checkbox("Specify Hour"):
        hour = st.sidebar.slider("Hour to look at", 0, 23, value=8, step=1)
        df_subset = df_subset[df_subset["CRASH DATE_CRASH TIME"].dt.hour == hour]
    
    st.header("Where are the most people injured in NYC?")
    st.map(df_subset[["LATITUDE", "LONGITUDE"]])
    st.write(f"TOTAL:", len(df_subset))
    st.write(df_subset)


def widget_show_3d_map(df):
    pass
    

@st.cache_resource()
def load_data(nrows: int = None):
    df = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH DATE", "CRASH TIME"]])
    df.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True, how="any")
    return df
    


if __name__ == "__main__":
    main()
    