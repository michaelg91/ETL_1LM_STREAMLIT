import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np




st.title('1LM Stats Explorer :basketball::flag-pl:')

st.markdown("""
A simple application that uses a dataframe to display statistics from the men's 1 basketball league 
between the 2005/06 and 2022/23 seasons.
Data source: ['https://1lm.pzkosz.pl']
""")


df_p_stats = pd.read_csv('Transformed_files/df_players_statistics.csv')
df_players = pd.read_csv('Transformed_files/df_players.csv')
df_t_stats = pd.read_csv('Transformed_files/df_teams_statistics.csv')
df_opponents = pd.read_csv('Transformed_files/opponents_stats.csv')
df_all_games = pd.read_csv('Transformed_files/df_all_games.csv')

select_df = st.selectbox('Select the dataframe that interests you: ', ['Players', 'Players statistics',
                                                                       'Team statistics', 'Statistics of opponents',
                                                                       'All games from 2005/06 to 2022/23'])


if select_df == 'Players':
    with st.expander("Basic statistics"):
        # Highest player
        max_height = df_players['Height'].max()
        player_with_max_height = str(df_players[df_players['Height'] == max_height][['First_Name', 'Last_name']])
        # Smallest player
        min_height = df_players['Height'].min()
        player_with_min_height = str(df_players[df_players['Height'] == min_height][['First_Name', 'Last_name']])
        # Unique seasons
        count = len(df_players['Year'].unique())
        # Unique country
        u_country = len(df_players['Country'].unique())
        # Avg height
        avg_height = round(df_players['Height'].mean(), 2)
        # Number of unique teams
        u_teams = len(df_players['Team'].unique())
        # Number of unique players
        u_players = len((df_players['First_Name'] + ' ' + df_players['Last_name']).unique())
        # The player who played the most seasons in the first division
        player_seasons = df_players.groupby(['First_Name', 'Last_name'])['Year'].nunique().reset_index(name= 'Seasons_Played')
        most_seasons_player = player_seasons.sort_values(by='Seasons_Played', ascending=False).iloc[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric(':arrow_up: Highest player', max_height, help=player_with_max_height)
        col1.metric(':arrow_down: Smallest player', min_height, help=player_with_min_height)
        col2.metric(':calendar: Seasons', count, delta_color="inverse", help='Numbers of seasons in dataframe')
        col2.metric(':world_map: Nationalities', u_country, delta_color="inverse", help='Different nationalities')
        col3.metric(':1234: Average height', avg_height, help='Average height')
        col3.metric(":basketball: Teams", u_teams, help='Number of unique teams')
        col4.metric(":person_with_ball: Players", u_players, help='Number of unique players')
        col4.metric(":top: Most Season in 1LM by player", most_seasons_player['Seasons_Played'],
                    help=str(most_seasons_player['First_Name'] + ' ' + str(most_seasons_player['Last_name'])))

    st.title('Players')

    with st.container():
        apply_filter = st.sidebar.checkbox(':point_left: Apply Filter', value=False)

        # SIDEBAR
        st.sidebar.header('User Input Features')

        unique_years = df_players['Year'].unique()
        years = st.sidebar.multiselect('Seasons :date:', unique_years, unique_years)

        unique_country = df_players['Country'].unique()
        player_country = st.sidebar.multiselect('Country :earth_americas:', unique_country, unique_country)

        filtered_players = df_players[(df_players['Year'].isin(years)) & (df_players['Country'].isin(player_country))]

        unique_player = (filtered_players['First_Name'] + ' ' + filtered_players['Last_name']).unique()
        player = st.sidebar.selectbox('Players', unique_player)

        if player:
            filtered_players = filtered_players[
                filtered_players['First_Name'] + ' ' + filtered_players['Last_name'] == player]

        if apply_filter:
            st.write(filtered_players)
            st.write('Data dimension: ' + str(filtered_players.shape[0]) + ' rows and ' + str(filtered_players.shape[1])
                     + ' collumns')
        else:
            st.write(df_players)

        df_players = df_players.sort_values(by='Year')
        fig = px.box(df_players, x='Year', y='Height', range_x=False)

        df_players = df_players[df_players['Country'] != 'Polska']
        country_counts = df_players['Country'].value_counts()
        country_percentages = (country_counts / len(df_players)) * 100
        country_data = pd.DataFrame({'Country': country_percentages.index, 'Percentage': country_percentages.values})

        country = px.pie(country_data, values='Percentage', names='Country', title='Participation of foreign players')
        country.update_traces(textposition='inside', textfont_size=12)

        with st.expander("Show charts with stats:"):
            st.plotly_chart(fig)
            st.plotly_chart(country)
elif select_df == 'Players statistics':
    with st.container():
        st.title('Players statistic')

        apply_filter = st.sidebar.checkbox(':point_left: Apply Filter', value=False)

        selected_player = st.sidebar.selectbox('Choose player:', df_p_stats['Name'].unique())

        filtered_data = df_p_stats[df_p_stats['Name'] == selected_player]

        main_stat = ["GP", "PTS", "AST", "TOV", "EVAL"]
        filtered_data = filtered_data.sort_values(by='YEAR', ascending=True)
        if apply_filter:
            st.write(filtered_data)
            fig = px.line(filtered_data, x='YEAR', y=main_stat, markers=True, title='Main statistics')
            fig.update_yaxes(range=[0, 40])
            st.plotly_chart(fig)
        else:
            st.write(df_p_stats)


elif select_df == 'Team statistics':
    with st.container():
        st.title('Team statistics')
        st.write(df_t_stats)
elif select_df == 'Statistics of opponents':
    with st.container():
        st.title('Statistics of opponents')
        st.write(df_opponents)
else:
    with st.container():
        st.title('All games from 2005/06 to 2022/23')
        st.write(df_all_games)

