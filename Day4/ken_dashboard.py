"""
Package:        n/a
Module:         ken_dashboard.py
Created By:     Euan Newlands
Created On:     05 Feb 2024

Description:    A streamlit dashboard displaying insights from Ken Jee's YouTube Channel

Classes:        n/a

Methods:        load_data        - loads csv data to pandas dataframes
                engineer_df_agg  - formats columns and data types of one of the datasets
                engineer_df_time - formats data types in another dataset
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime


def load_data() -> list[pd.DataFrame]:
    """
    DESCR
        This function loads the data, downloaded from Kaggle, from .csv files to
        Pandas DataFrames.
    PARAMS
        None
    RETURNS
        dfs -   a list of dataframes, with each containing data from one of
                the .csv raw data files
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       05 Feb 2024     v0.1 - Initial Script
    """
    # remove first row from dataframe, which is the YT calculated totals
    df_agg = pd.read_csv(".\data\Aggregated_Metrics_By_Video.csv").iloc[1:, :]

    df_agg_sub = pd.read_csv(
        ".\data\Aggregated_Metrics_By_Country_And_Subscriber_Status.csv"
    )
    df_comments = pd.read_csv(".\data\All_Comments_Final.csv")
    df_time = pd.read_csv(".\data\Video_Performance_Over_Time.csv")

    dfs = (df_agg, df_agg_sub, df_comments, df_time)

    return dfs


def engineer_df_agg(df_agg: pd.DataFrame) -> pd.DataFrame:
    """
    DESCR:
        This function modifies the raw df_agg dataframe by renaming columns to be
        more readable and enforcing the following;
            - `Video Publish Time` data type conversion; pd.object -> pd.datetime64ns
            - `Average View Duration` data type conversion; pd.object -> pd.datetime64ns
            - `AVG_DURATION_SEC` column added
            - `ENGAGEMENT_RATIO` column added
            - `VIEWS / SUBS_GAINED` column added
    PARAMS:
        df_agg  - dataframe containing the raw data of video interactions, aggregated
                    by Country and Subscriber status
    RETURNS
        df_agg  - the re-engineered dataframe, with the same raw data values
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       05 Feb 2024     v0.1 - Initial Script
    """
    # column renames due to funny something going on with the raw data
    df_agg.columns = [
        "Video",
        "Video Title",
        "Video Publish Time",
        "Comments Added",
        "Shares",
        "Dislikes",
        "Likes",
        "Subscribers Lost",
        "Subscribers Gained",
        "RPM(USD)",
        "CPM(USD)",
        "Average % Viewed",
        "Average View Duration",
        "Views",
        "Watch Time(hours)",
        "Subscribers",
        "Your Estimated Revenue(USD)",
        "Impressions",
        "Impressions Click-through Rate(%)",
    ]

    # string to datetime conversion
    df_agg["Video Publish Time"] = pd.to_datetime(
        df_agg["Video Publish Time"], format="%b %d, %Y"
    )

    # string to H:M:S timestamp format, to calculate avg watch in seconds
    df_agg["Average View Duration"] = df_agg["Average View Duration"].apply(
        lambda x: datetime.strptime(x, "%H:%M:%S")
    )
    df_agg["AVG_DURATION_SEC"] = df_agg["Average View Duration"].apply(
        lambda x: x.second + x.minute * 60 + x.hour * 3600
    )

    # "Cool data points" from raw data
    df_agg["ENGAGEMENT_RATIO"] = (
        df_agg["Comments Added"]
        + df_agg["Shares"]
        + df_agg["Likes"]
        + df_agg["Dislikes"]
    ) / df_agg["Views"]

    df_agg["VIEWS / SUBS_GAINED"] = df_agg["Views"] / df_agg["Subscribers Gained"]

    # order by video publish date
    df_agg.sort_values('Video Publish Time', ascending = False, inplace = True)

    return df_agg



def engineer_df_time(df_time: pd.DataFrame) -> pd.DataFrame:
    """
    DESCR:
        This function modifies the raw df_time dataframe by formatting the time column
        data type from string to datetime.
    PARAMS:
        df_time - dataframe containing the raw data of video performance over time
    RETURNS
        df_time - the re-engineered dataframe, with the same raw data values
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       05 Feb 2024     v0.1 - Initial Script
    """
    # string to datetime conversion, first formatting Sept -> 3 letter variation
    df_time["Date"] = df_time["Date"].apply(lambda x: x.replace('Sept','Sep'))
    df_time["Date"] = pd.to_datetime(df_time["Date"], format = '%d %b %Y')

    return df_time
    

def run_it():
    # load csvs
    df_agg, df_agg_sub, df_comments, df_time = load_data()

    # engineer dfs
    df_agg = engineer_df_agg(df_agg)
    df_time = engineer_df_time(df_time)


if __name__ == "__main__":
    run_it()
