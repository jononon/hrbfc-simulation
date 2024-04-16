import copy
import random
from football_api import get_standings, get_fixtures

POINTS_FOR_WIN = 3
POINTS_FOR_DRAW = 1
SIMULATION_COUNT = 1_000_000


def simulate_matches(teams, matches):
    if len(matches) == 0:
        return teams
    else:
        current_match = matches.pop()

        outcome = random.choice(['Home', 'Away', 'Draw'])

        if outcome == 'Draw':
            # win for draw
            teams[current_match["Home"]] += POINTS_FOR_DRAW
            teams[current_match["Away"]] += POINTS_FOR_DRAW
            return simulate_matches(teams, matches)
        else:
            # win for home or away
            teams[current_match[outcome]] += POINTS_FOR_WIN
            return simulate_matches(teams, matches)


def generate_position_probability_dict(team):
    team_positions = []

    for outcome in league_outcomes:
        sorted_outcome = sorted(outcome.items(), key=lambda item: item[1], reverse=True)
        for i in range(len(sorted_outcome)):
            if sorted_outcome[i][0] == team:
                team_positions.append(i + 1)
                break

    position_outcome_dict = {}

    for position in team_positions:
        if position in position_outcome_dict:
            position_outcome_dict[position] += 1
        else:
            position_outcome_dict[position] = 1

    position_probability_dict = {}
    for position, num_outcomes in position_outcome_dict.items():
        position_probability_dict[position] = num_outcomes / len(team_positions)

    return position_probability_dict

def get_league_table():
    league_table = {}

    standings = get_standings()

    for team_data in standings['response'][0]['league']['standings'][0]:
        team_name = team_data['team']['name']
        points = team_data['points']
        league_table[team_name] = points

    return league_table

def get_league_matches():
    upcoming_fixtures = []

    fixtures = get_fixtures()

    for fixture in fixtures['response']:
        if fixture['fixture']['status']['long'] == "Not Started":
            home_team = fixture['teams']['home']['name']
            away_team = fixture['teams']['away']['name']
            upcoming_fixtures.append({"Home": home_team, "Away": away_team})

    return upcoming_fixtures

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    league_table = get_league_table()

    league_matches = get_league_matches()

    league_outcomes = []

    for simulation in range(SIMULATION_COUNT):
        simulation_league_table = copy.deepcopy(league_table)
        simulation_matches = copy.deepcopy(league_matches)

        league_outcomes.append(simulate_matches(simulation_league_table, simulation_matches))

    for key, _ in sorted(league_table.items(), key=lambda item: item[1], reverse=True):
        print_string = f"{key} -- "

        position_probability_dict = generate_position_probability_dict(key)

        for position, probability in sorted(position_probability_dict.items(), key=lambda item: item[0]):
            print_string += f"{position}: {round(probability * 100, 2)}%; "

        print(print_string)
