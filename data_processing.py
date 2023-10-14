from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
from creating_files import creating_players_txt_file,\
    creating_players_stats_txt_file, convert_txt_to_csv, creating_games_txt_file, creating_team_stats_txt_file


URL = 'https://1lm.pzkosz.pl'
PLAYER_STATS = '/2.html'
TEAM_STATS = '/4.html'
GAMES = '/6.html'


def extract():

    def get_teams_website(URL) -> list:
        teams_website = f'{URL}/druzyny.html'
        response = requests.get(teams_website)
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')

        pagi = soup.find('div', id='header')
        root = pagi.find('div', class_='comboBox')
        branches = root.find_all('li')

        season_links = [link['href'] for branch in branches[:-2] for link in branch.find_all('a', href=True)]

        all_teams = []
        for season in season_links:
            teams_website = f'{URL}{season}'
            response = requests.get(teams_website)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')

            box = soup.find('div', class_='teamsList')  # root
            # all_teams = []
            for team in box.find_all('a', href=True):
                all_teams.append(team['href'])

        return all_teams

    def get_players(all_teams: list):
        for i, team in enumerate(all_teams):
            players = requests.get(f'{URL}{team}')
            content = players.text
            soup = BeautifulSoup(content, 'html.parser')

            year = soup.find('div', class_='comboBox').find('span').text
            # print(year)
            team_name = soup.find('h1', itemprop="name").text

            box = soup.find('div', class_="row flex-wrap")
            # for player in box.find_all('span'):
            table_player = box.find_all('div', class_="col-xl-3 col-lg-3 col-md-4 col-sm-6 mycol")

            for player in table_player:
                player_table = []
                for text in player.find_all('span'):
                    text = text.get_text(strip=True)
                    player_table.append(text)
                player_table.append(team_name)
                player_table.append(year)
                creating_players_txt_file('Files_txt/players.txt', player_table)

                convert_txt_to_csv('Files_txt/players.txt', 'Files_csv/players.csv')

    # Players statistic
    def get_player_statistic(all_teams):
        for statistic in all_teams:
            statistic = statistic.replace('.html', PLAYER_STATS)
            ind_stats = requests.get(f'{URL}{statistic}')
            content = ind_stats.text
            soup = BeautifulSoup(content, 'html.parser')

            year = soup.find('div', class_='comboBox').find('span').text
            team_name = soup.find('h1', itemprop="name").text

            table = soup.find_all('table', class_='statystyki')[1]
            trs = table.find_all('tr')

            for tr in trs[2::]:
                stats_player = []
                for stats in tr.find_all('td'):
                    stats = stats.get_text(strip=True)
                    stats_player.append(stats)
                stats_player.append(team_name)
                stats_player.append(year)
                creating_players_stats_txt_file('Files_txt/players_stats.txt', stats_player)
                convert_txt_to_csv('Files_txt/players_stats.txt', 'Files_csv/players_stats.csv')

    # Team statistic
    def get_team_statistic(all_teams):
        for team_statistic in all_teams:
            team_statistic = team_statistic.replace('.html', TEAM_STATS)
            ind_stats = requests.get(f'{URL}{team_statistic}')
            content = ind_stats.text
            soup = BeautifulSoup(content, 'html.parser')

            year = soup.find('div', class_='comboBox').find('span').text
            team = soup.find('h1', itemprop="name").text
            table = soup.find_all('table', class_='statystyki')[1]
            trs = table.find_all('tr')

            for tr in trs[2::]:
                stats_team = []
                for stats in tr.find_all('td'):
                    stats = stats.get_text(strip=True)
                    stats_team.append(stats)
                stats_team.append(year)
                stats_team.append(team)

                creating_team_stats_txt_file('Files_txt/teams_stats.txt', stats_team)
                convert_txt_to_csv('Files_txt/teams_stats.txt', 'Files_csv/teams_stats.csv')

    # Games
    def get_all_games(all_teams):
        for games_per_team in all_teams:
            games_per_team = games_per_team.replace('.html', GAMES)
            ind_stats = requests.get(f'{URL}{games_per_team}')
            content = ind_stats.text
            soup = BeautifulSoup(content, 'html.parser')

            year = soup.find('div', class_='comboBox').find('span').text
            team_name = soup.find('h1', itemprop="name").text
            table = soup.find('table', class_='statystyki')
            trs = table.find_all('tr')

            for tr in trs[2::]:
                stats_games = []
                for stats in tr.find_all('td'):
                    stats = stats.get_text(strip=True)
                    stats_games.append(stats)
                stats_games.append(team_name)
                stats_games.append(year)
                creating_games_txt_file('Files_txt/all_games.txt', stats_games)
                convert_txt_to_csv('Files_txt/all_games.txt', 'Files_csv/all_games.csv')

    all_teams = get_teams_website(URL)
    # get_players(all_teams)
    # get_player_statistic(all_teams)
    # get_team_statistic(all_teams)
    get_all_games(all_teams)


def transform():
    csv_files = []

    def clean_players():

        df_players = pd.read_csv('Files_csv/players.csv', header=None)
        # Create columns name
        df_players.columns = ["Number", "First_Name", "Last_name", "Country", "Birthday", "Height", "Position", "Team",
                              "Year"]
        # removing column Number, because we don't need it for any analysis,inplace= True
        # means operation is performed on an existing object we do not create a copy axis=0 remove rows,
        # axis=1 remove columns
        df_players.drop("Number", inplace=True, axis=1)
        # filling Country feature with Polska
        df_players.Country = df_players.Country.fillna("Polska")
        # Convert string on date type
        df_players['Birthday'] = pd.to_datetime(df_players['Birthday'], format='%d.%m.%Y')
        # Converting the value '---' to NULL
        df_players.iloc[df_players["Height"] == '---', 4] = pd.NA
        # Convert 'Height' column to float (or appropriate) type
        df_players["Height"] = (pd.to_numeric(df_players["Height"], errors='coerce') / 100).round(2)
        df_players["Height"] = df_players["Height"].apply(lambda x: f'{x:.2f}')
        # Remove 'Sezon' from column 'Year'
        df_players["Year"] = df_players["Year"].str.replace('Sezon ', '')
        # Remove whitespace characters before and after '\'
        df_players['Position'] = df_players['Position'].str.replace(r'\s*/\s*', '/', regex=True)
        # Remove whitespace characters at the end of a string
        df_players['Team'] = df_players['Team'].str.rstrip()

        df_players.to_csv('Transformed_files/df_players.csv', index=False)
        csv_files.append('Transformed_files/df_players.csv')

    def clean_players_stats():

        df_pstats = pd.read_csv('Files_csv/players_stats.csv', header=None)
        df_pstats.columns = ["Name", "GP", "S5", "PTS", "MIN", "2PM", "2PA", "2P%", "3PM", "3PA", "3P%", "SM", "SA",
                             "S%", "FTM", "FTA", "FTP", "OREB", "DREB", "TREB", "AST",
                             "PF", "FF", "TOV", "STL", "BLK", "RBLK", "EVAL", "PLUS_MINUS", "TEAM", "YEAR"]

        columns_fill = ["PTS", "2PM", "2PA", "2P%", "3PM", "3PA", "3P%", "SM", "SA", "S%", "FTM", "FTA", "FTP", "OREB",
                        "DREB", "TREB", "AST",
                        "PF", "TOV", "STL", "BLK", "EVAL"]

        # placing the NaN value with 0.0 because statistics were run and the NaN value actually meant 0
        for column in columns_fill:
            print(column)
            df_pstats[column] = df_pstats[column].fillna(0.0)
        # Remove 'Sezon' from column 'Year'
        df_pstats["YEAR"] = df_pstats["YEAR"].str.replace('Sezon ', '')
        # Remove whitespace characters at the end of a string
        df_pstats['TEAM'] = df_pstats['TEAM'].str.rstrip()
        # placing the NaN value with 0.0 because statistics were run and the NaN value actually meant 0, of course,
        # the change applies only to those seasons in which statistics for the column were kept
        seasons_plus_minus = ["2010/2011", "2009/2010", "2008/2009", "2007/2008", "2006/2007", "2005/2006"]
        seasons_s5_ff_rblk = ["2006/2007", "2005/2006"]
        columns_part_two = ["S5", "FF", "RBLK", "PLUS_MINUS"]

        for column in columns_part_two:
            if column == "PLUS_MINUS":
                df_pstats.loc[~df_pstats["YEAR"].isin(seasons_plus_minus), column] = df_pstats[column].fillna(0.0)
            else:
                df_pstats.loc[~df_pstats["YEAR"].isin(seasons_s5_ff_rblk), column] = df_pstats[column].fillna(0.0)

        df_pstats.to_csv('Transformed_files/df_players_statistics.csv', index=False)
        csv_files.append('Transformed_files/df_players_statistics.csv')

    def clean_teams_stats():
        df_teams = pd.read_csv('Files_csv/teams_stats.csv', header=None)
        df_teams.columns = ["TEAM_NAME", "GAMES", "POINTS", "2PM", "2PA", "2P%", "3PM", "3PA", "3P%", "SM", "SA", "S%",
                            "FTM", "FTA", "FTP", "OREB", "DREB", "TREB", "AST",
                            "PF", "FF", "TOV", "STL", "BLK", "RBLK", "EVAL", "PLUS_MINUS", "YEAR",'TEAM']
        # analyzing the data, unfortunately, we have no statistics for teams from Kutno in the 2019/2020 season,
        # we only have the statistics of opponents, so the two records for the team from Kutno are removed
        df_teams.drop(df_teams[(df_teams['YEAR'] == 'Sezon 2019/2020') & (df_teams['TEAM'] == 'Polfarmex Kutno')].index,
                      inplace=True)

        # Remove 'Sezon' from column 'Year'
        df_teams["YEAR"] = df_teams["YEAR"].str.replace('Sezon ', '')
        # # Remove column 'TEAM'
        df_teams.drop('TEAM_NAME', axis=1, inplace=True)

        new_column_order = ["TEAM", "GAMES", "POINTS", "2PM", "2PA", "2P%", "3PM", "3PA", "3P%", "SM", "SA", "S%",
                            "FTM", "FTA", "FTP", "OREB", "DREB", "TREB", "AST",
                            "PF", "FF", "TOV", "STL", "BLK", "RBLK", "EVAL", "PLUS_MINUS", "YEAR"
                            ]

        df_teams = df_teams.loc[:, new_column_order]
        # Create file with opponents stats
        opponents_stats = df_teams.iloc[1::2].copy()
        opponents_stats.to_csv('Transformed_files/opponents_stats.csv', index=False)
        csv_files.append('Transformed_files/opponents_stats.csv')
        # Remove opponents stats from main file
        df_teams.drop(df_teams.index[1::2], inplace=True)

        df_teams.to_csv('Transformed_files/df_teams_statistics.csv', index=False)
        csv_files.append('Transformed_files/df_teams_statistics.csv')

    def clean_all_games():

        df_all_games = pd.read_csv('Files_csv/all_games.csv', header=None)

        df_all_games.columns = ["DATE", "OPPONENT", "RESULT", "PTS", "2PM", "2PA", "2P%",
                                "3PM", "3PA", "3P%", "SM", "SA", "S%",
                                "FTM", "FTA", "FT%", "OREB", "DREB", "TREB", "AST",
                                "PF", "FF", "TOV", "STL", "BLK", "RBLK", "EVAL", "TEAM", "YEAR"]

        pattern_opponent = r'^(.+)\((w|d)\)$'

        df_all_games[['OPPONENT', 'HOME(D)/AWAY(W)']] = df_all_games['OPPONENT'].str.extract(pattern_opponent)

        df_all_games['HOME(D)/AWAY(W)'] = df_all_games['HOME(D)/AWAY(W)'].str.upper()

        pattern_result = r'(\d+\s*:\s*\d+)([W|P])$'

        df_all_games[['RESULT', 'WIN(W)/LOST(P)']] = df_all_games['RESULT'].str.extract(pattern_result)

        df_all_games['WIN(W)/LOST(P)'] = df_all_games['WIN(W)/LOST(P)'].str.upper()

        df_all_games['YEAR'] = df_all_games['YEAR'].str.replace('Sezon ', '')

        df_all_games['TEAM'] = df_all_games['TEAM'].str.rstrip()
        # Remove whitespace characters before and after ':'
        df_all_games['RESULT'] = df_all_games['RESULT'].str.replace(' ', '')

        df_all_games['DATE'] = pd.to_datetime(df_all_games['DATE'], format='%Y-%m-%d %H:%M')

        new_column_order = ['TEAM', 'DATE', 'OPPONENT', 'HOME(D)/AWAY(W)', 'RESULT', 'WIN(W)/LOST(P)', 'PTS', '2PM', '2PA',
                            '2P%',
                            '3PM', '3PA', '3P%', 'SM', 'SA', 'S%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'TREB', 'AST',
                            'PF', 'FF', 'TOV', 'STL', 'BLK', 'RBLK', 'EVAL', 'YEAR']

        df_all_games = df_all_games.loc[:, new_column_order]

        df_all_games.to_csv('Transformed_files/df_all_games.csv', index=False)
        csv_files.append('Transformed_files/df_all_games.csv')

    clean_players()
    clean_players_stats()
    clean_teams_stats()
    clean_all_games()

    return csv_files


def load(csv_files):

    conn = sqlite3.connect('1LM_database.db')
    table_names = ['PLAYERS', 'PLAYERS_STATISTIC', 'OPPONENT_STATISTICS', 'TEAMS_STATISTIC', 'GAMES']

    for csv_file, table_name in zip(csv_files, table_names):
        print(csv_file, table_name)
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, conn, index=False)

    conn.close()
    print("Database created and data imported successfully.")


# extract()
transform = transform()
# load(transform)

