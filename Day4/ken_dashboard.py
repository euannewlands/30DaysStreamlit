"""
Package:        n/a
Module:         ken_dashboard.py
Created By:     Euan Newlands
Created On:     05 Feb 2024

Description:    A streamlit dashboard displaying insights from Ken Jee's YouTube Channel

Classes:        n/a

Methods:        load_data               - loads csv data to pandas dataframes
                engineer_df_agg         - formats columns and data types of one of the datasets
                engineer_df_time        - formats data types in another dataset
                get_vid_stat_trends     - compares video stats to a median baseline
                get_header_stats        - selects a set of metrics to have as Big Numbers
                build_sidebar           - frontend formatting of the streamlit sidebar
                _format_header_metrics  - frontend formatting of the Big Numbers
                _display_df_agg_diff    - frontend formatting of a pandas dataframe
                total_dashboard         - main method for building the entire frontend
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime


@st.cache_data
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
    Euan Newlands       07 Feb 2024     v0.2 - Added os.path.join, which is an operating
                                                system agnostic method of handling paths
    """
    # get file paths
    agg_path = os.path.join(".", "data", "Aggregated_Metrics_By_Video.csv")
    agg_sub_path = os.path.join(
        ".", "data", "Aggregated_Metrics_By_Country_And_Subscriber_Status.csv"
    )
    comments_path = os.path.join(".", "data", "All_Comments_Final.csv")
    time_path = os.path.join(".", "data", "Video_Performance_Over_Time.csv")

    # remove first row from dataframe, which is the YT calculated totals
    df_agg = pd.read_csv(agg_path).iloc[1:, :]
    # load remining files as are
    df_agg_sub = pd.read_csv(agg_sub_path)
    df_comments = pd.read_csv(comments_path)
    df_time = pd.read_csv(time_path)

    dfs = [df_agg, df_agg_sub, df_comments, df_time]

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
    df_agg.sort_values("Video Publish Time", ascending=False, inplace=True)

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
    df_time["Date"] = df_time["Date"].apply(lambda x: x.replace("Sept", "Sep"))
    df_time["Date"] = pd.to_datetime(df_time["Date"], format="%d %b %Y")

    return df_time


def get_vid_stat_trends(df_agg: pd.DataFrame) -> pd.DataFrame:
    """
    DESCR:
        This function calculates median statistics over 12 months, and compares each
        individual video's statistics against this median baseline. The median value is
        subtracted from the video's statistics to calculate how the video perfromed against
        the median baseline. The returned values are used to display which video's performed
        best/worst on the dashboard.
    PARAMS:
        df_agg      - dataframe containing the raw data of video interactions, aggregated
                        by Country and Subscriber status
    RETURNS
        df_agg_diff - a dataframe containing the % difference of video stats compared to
                        the 12-month median values.
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       07 Feb 2024     v0.1 - Initial Script
    """
    # initialise a copy to work with
    df_agg_diff = df_agg.copy()
    # find median on numeric data, only if record within 12 months to latest video
    metric_date_12month = df_agg_diff["Video Publish Time"].max() - pd.DateOffset(
        months=12
    )
    median_12mo_agg = df_agg_diff[
        df_agg_diff["Video Publish Time"] >= metric_date_12month
    ].median(numeric_only=True)

    # compare numeric column records to the 12 month median values
    numeric_cols = np.array(
        (df_agg_diff.dtypes == "int64") | (df_agg_diff.dtypes == "float64")
    )
    df_agg_diff.iloc[:, numeric_cols] = 100*(
        df_agg_diff.iloc[:, numeric_cols] - median_12mo_agg
    ).div(median_12mo_agg)

    return df_agg_diff


def get_header_stats(df_agg: pd.DataFrame) -> tuple[pd.DataFrame,pd.DataFrame]:
    """
    DESCR:
        Extracts the 6 month median for select numeric video performance metrics.
        The trends of these stats are determined by calculating the percentage change
        between the 6 month and 12 month medians. Both the 6 month median metrics and
        their respective trends (compared to 12 month medians) will be included as
        header metrics on the streamlit dashboard.
        The metrics returned are;
        - Video Publish Time
        - Views
        - Likes
        - Subscribers
        - Shares
        - Comments Added
        - RPM(USD)
        - Average % Viewed
        - AVERAGE_DURATION_SEC
        - ENGAGEMENT_RATIO
        - VIEWS / SUBS_GAINED
        
    PARAMS:
        df_agg              - dataframe containing the raw data of video interactions, aggregated
                                by Country and Subscriber status
    RETURNS
        metric_date_6month  - dataframe containing the 6 month median for the select
                                numeric metrics
        metric_trends_df    - dataframe containing the percentage change in the 6 month
                                medians compared to their 12 month median counterparts
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       07 Feb 2024     v0.1 - Initial Script
    """
    header_metrics_df = df_agg[[
        "Video Publish Time",
        "Views",
        "Likes",
        "Subscribers",
        "Shares",
        "Comments Added",
        "RPM(USD)",
        "Average % Viewed",
        "AVG_DURATION_SEC",
        "ENGAGEMENT_RATIO",
        "VIEWS / SUBS_GAINED"
    ]]

    # find median on numeric data, only if record within 6 & 12 months to latest video
    metric_date_12month = header_metrics_df["Video Publish Time"].max() - pd.DateOffset(
        months=12
    )
    metric_date_6month = header_metrics_df["Video Publish Time"].max() - pd.DateOffset(
        months=6
    )
    median_12mo_metrics = header_metrics_df[
        header_metrics_df["Video Publish Time"] >= metric_date_12month
    ].median(numeric_only=True)

    median_6mo_metrics = header_metrics_df[
        header_metrics_df["Video Publish Time"] >= metric_date_6month
    ].median(numeric_only=True)

    metric_trends_df = 100*(median_6mo_metrics - median_12mo_metrics).div(median_12mo_metrics)

    return median_6mo_metrics, metric_trends_df


def build_sidebar() -> str:
    """
    DESCR:
        This function contains all the streamlit code to build out the sidebar on the streamlit
        app. Initially, the siderbar only has a simple select box with 2 options
    PARAMS:
        None
    RETURNS
        page    - the value which represents which content the user wants to display,
                    like a page
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       05 Feb 2024     v0.1 - Initial Script
    """
    page = st.sidebar.selectbox(
        "Individual or Aggregated View",
        ["Aggregate Metrics", "Individual Video Analysis"],
    )

    return page


def _format_header_metrics(header_metrics: pd.DataFrame, header_trends: pd.DataFrame) -> None:
    """
    DESCR:
        This function formats the header statistics to be in 2rows x 5columns
    PARAMS:
        header_metrics  - dataframe containing the 6 month median for select
                                numeric metrics
        header_trends   - dataframe containing the percentage change in the 6 month
                                medians compared to their 12 month median counterparts
    RETURNS
        None
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       07 Feb 2024     v0.1 - Initial Script
    """
    columns = st.columns(5) # creates 5 side by side containers

    for i, met in enumerate(header_metrics.index):
        with columns[i%5]:  # sorts into 2 rows of 5
            st.metric(
                label= met.replace('_',' ').title(),       # make nicer to read
                value = header_metrics[met].round(1),
                delta = f"{header_trends[met].round(2)}%"
            )
        

def _display_df_agg_diff(df_agg_diff: pd.DataFrame) -> None:
    """TODO: add docstring
    """
    df_agg_diff['PUBLISH_DATE'] = df_agg_diff['Video Publish Time'].apply(lambda x: x.date())
    df_agg_diff_final = df_agg_diff.loc[:,[
        'Video Title',
        'PUBLISH_DATE',
        'Views',
        'Likes',
        'Subscribers',
        'AVG_DURATION_SEC',
        'ENGAGEMENT_RATIO',
        'VIEWS / SUBS_GAINED'
    ]]
    st.dataframe(df_agg_diff_final, hide_index = True)


def total_dashboard(
        page: str,
        header_metrics: pd.DataFrame,
        header_trends: pd.DataFrame,
        df_agg_diff: pd.DataFrame
    ) -> None:
    """
    DESCR:
        This function contains all the streamlit code to build out the total streamlit app.
        There are 2 pages; the user can choose a page by interacting with the selectbox in
        the sidebar.
    PARAMS:
        page    - value of page returned by the sidebar select box on the streamlit app
        header_metrics  - dataframe containing the 6 month median for select
                                numeric metrics
        header_trends   - dataframe containing the percentage change in the 6 month
                                medians compared to their 12 month median counterparts
    RETURNS
        None    -
    -----------------------------------------------------------------------------------
    Summary of Changes
    -----------------------------------------------------------------------------------
    Euan Newlands       07 Feb 2024     v0.1 - Initial Script
    """
    if page == 'Aggregate Metrics':
        _format_header_metrics(header_metrics, header_trends)
        _display_df_agg_diff(df_agg_diff)


    if page == 'Individual Video Analysis':
        st.write('Individual Video Analysis')


def run_it():
    # load csvs
    df_agg, df_agg_sub, df_comments, df_time = load_data()

    # engineer dfs
    df_agg = engineer_df_agg(df_agg)
    df_time = engineer_df_time(df_time)

    # find video metric trends
    df_agg_diff = get_vid_stat_trends(df_agg)
    header_metrics, header_trends = get_header_stats(df_agg)

    # build streamlit app
    page = build_sidebar()
    total_dashboard(page, header_metrics, header_trends, df_agg_diff)


if __name__ == "__main__":
    run_it()
