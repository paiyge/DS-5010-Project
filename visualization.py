"""
This module contains functions that create the graphs from the data frame
generated by calculate.py
"""

from calculate import *
from plotly.offline import plot
import plotly.express as px

def draw_scatterplot(ppdfd_df, x='Date', y='DLI'):
    '''
    Draws a scatterplot of DLI vs Date by default.

    Parameters
    ----------
    ppdfd_df : pandas DataFrame
        Data frame containing dates, PAR, and PPFD
    x : pandas Series, optional
        The data for the x-axis of the scatterplot. The default is 'Date'.
    y : pandas Series, optional
        The data for the y-axis of the scatterplot. The default is 'DLI'.

    Returns
    -------
    None.

    '''
    fig = px.scatter(ppfd_df, x, y)
    plot(fig, auto_open=True)


def weekly_dli(ppfd_df):
    '''
    Creates a data frame with the week number and the year as indices and
    the week's average DLI as a column

    Parameters
    ----------
    ppfd_df : pandas DataFrame
        Data frame containing dates, PAR, and PPFD

    Returns
    -------
    week_df : pandas DataFrame
        Data frame with the week number the year, and the week's average DLI

    '''
    ppfd_df['Week'] = (pd.to_datetime
                       (ppfd_df['UnixTime'], unit='s').dt.isocalendar().week)
    ppfd_df['Year'] = (pd.to_datetime
                       (ppfd_df['UnixTime'], unit='s').dt.year)
    week_df = pd.DataFrame(ppfd_df.groupby(['Year','Week'])['DLI'].mean())
    return week_df


def monthly_dli(ppfd_df):
    '''
    Creates a data frame with the month number and the year as indices and
    the month's average DLI as a column

    Parameters
    ----------
    ppfd_df : pandas DataFrame
        Data frame containing dates, PAR, and PPFD

    Returns
    -------
    month_df : pandas DataFrame
        Data frame with the month number and the year as indices and
        the month's average DLI as a column

    '''
    ppfd_df['Month'] = (pd.to_datetime
                       (ppfd_df['UnixTime'], unit='s').dt.month)
    ppfd_df['Year'] = (pd.to_datetime
                       (ppfd_df['UnixTime'], unit='s').dt.year)
    month_df = pd.DataFrame(ppfd_df.groupby(['Year','Month'])['DLI'].mean())
    return month_df


def draw_weekbar(ppfd_df):
    '''
    Draws a bar graph of DLI vs the week number

    Parameters
    ----------
    ppfd_df : pandas DataFrame
        Data frame containing dates, PAR, and PPFD

    Returns
    -------
    None.

    '''
    week_df = weekly_dli(ppfd_df)
    week_df = week_df.reset_index()
    week_df['Year'] = week_df['Year'].astype(str)
    fig1 = px.bar(week_df, y='DLI', x='Week', color="Year", barmode='group')
    plot(fig1, auto_open=True)

def draw_monthbar(ppfd_df):
    '''
    Draws a bar graph of DLI vs month

    Parameters
    ----------
    ppfd_df : pandas DataFrame
        Data frame containing dates, PAR, and PPFD

    Returns
    -------
    None.

    '''
    month_df = monthly_dli(ppfd_df)
    month_df = month_df.reset_index()
    month_df['Year'] = month_df['Year'].astype(str)
    fig2 = px.bar(month_df, y='DLI', x='Month', color="Year", barmode='group')
    plot(fig2, auto_open=True)


if __name__ =="__main__":
    ppfd_df = calculate_ppfd(create_df(4,5,2010,5,17,2010))
    draw_weekbar(ppfd_df)
    draw_scatterplot(ppfd_df)
    draw_monthbar(ppfd_df)
