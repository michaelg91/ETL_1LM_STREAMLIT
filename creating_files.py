import csv


def creating_players_txt_file(file_path: str, players_table: list):
    number, name, last_name, birth_place, birthday, height, position, team, year= players_table

    with open(file_path, 'a') as file:
        file.write(f'{number};{name};{last_name};{birth_place};{birthday};{height};{position};{team};{year}\n')


def creating_players_csv_file(file_path: str, players_table: list):
    number, name, last_name, birth_place, birthday, height, position, team = players_table

    with open(file_path, 'a', newline='') as csvfile:
        header = ['Number', 'Name', 'Last_Name', 'Birth_place', 'Birthday', 'Height', 'Position', 'Team']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writerow({
            'Number': number,
            'Name': name,
            'Last_Name': last_name,
            'Birth_place': birth_place,
            'Birthday': birthday,
            'Height': height,
            'Position': position,
            'Team': team
        })


def creating_players_stats_txt_file(file_path: str, stats_player: list):
    name, games_played, starting_five, points, minutes, two_made, two_attempted, two_percentage, \
        three_made, three_attempted, three_percentage, shot_made, shot_attempted, shot_percentage, \
        fthrows_made, fthrows_attempted, fthrows_percentage, off_reb, def_reb, t_reb, assist, \
        p_foul, f_fouls, tov, stl, blk, r_blk, eval, plus_minus, team, year = stats_player

    with open(file_path, 'a') as file:
        file.write(f'{name};{games_played};{starting_five};{points};{minutes};{two_made};{two_attempted};{two_percentage};{three_made};{three_attempted};{three_percentage};{shot_made};{shot_attempted};{shot_percentage};{fthrows_made};{fthrows_attempted};{fthrows_percentage};{off_reb};{def_reb};{t_reb};{assist};{p_foul};{f_fouls};{tov};{stl};{blk};{r_blk};{eval};{plus_minus};{team};{year}\n')


def creating_games_txt_file(file_path: str, stats_games: list):
    date, opponent, result, points, two_made, two_attempted, two_percentage,\
    three_made, three_attempted, three_percentage, shot_made, shot_attempted, shot_percentage,\
    fthrows_made, fthrows_attempted, fthrows_percentage, off_reb, def_reb, t_reb, assist,\
        p_foul, f_fouls, tov, stl, blk, r_blk, eval, team, year = stats_games

    with open(file_path,'a') as file:
        file.write(f'{date};{opponent};{result};{points};{two_made};{two_attempted};{two_percentage};{three_made};{three_attempted};{three_percentage};{shot_made};{shot_attempted};{shot_percentage};{fthrows_made};{fthrows_attempted};{fthrows_percentage};{off_reb};{def_reb};{t_reb};{assist};{p_foul};{f_fouls};{tov};{stl};{blk};{r_blk};{eval};{team};{year}\n')


def creating_team_stats_txt_file(file_path: str, stats_team: list):
    team_name, games, points, two_made, two_attempted, two_percentage, \
        three_made, three_attempted, three_percentage, shot_made, shot_attempted, shot_percentage, \
        fthrows_made, fthrows_attempted, fthrows_percentage, off_reb, def_reb, t_reb, assist, \
        p_foul, f_fouls, tov, stl, blk, r_blk, eval, plus_minus, year,team = stats_team

    with open(file_path,'a') as file:
        file.write(f'{team_name};{games};{points};{two_made};{two_attempted};{two_percentage};{three_made};{three_attempted};{three_percentage};{shot_made};{shot_attempted};{shot_percentage};{fthrows_made};{fthrows_attempted};{fthrows_percentage};{off_reb};{def_reb};{t_reb};{assist};{p_foul};{f_fouls};{tov};{stl};{blk};{r_blk};{eval};{plus_minus};{year};{team}\n')


def convert_txt_to_csv(txt_file, csv_file):
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in lines:
            data = line.strip().split(';')
            writer.writerow(data)

