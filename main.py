import copy
import random

league_matches = [
    {'Home': 'St. Albans City', 'Away': 'Hampton & Richmond Borough'},
    {'Home': 'Taunton Town', 'Away': 'Torquay United'},
    {'Home': 'Truro City', 'Away': 'Dover Athletic'},
    {'Home': 'Weston-super-Mare', 'Away': 'Eastbourne Borough'},
    {'Home': 'Taunton Town', 'Away': 'Weston-super-Mare'},
    {'Home': 'Truro City', 'Away': 'Weymouth'},
    {'Home': 'Aveley', 'Away': 'Bath City'},
    {'Home': 'Braintree Town', 'Away': 'Eastbourne Borough'},
    {'Home': 'Chippenham Town', 'Away': 'Chelmsford City'},
    {'Home': 'Dartford', 'Away': 'Truro City'},
    {'Home': 'Dover Athletic', 'Away': 'Yeovil Town'},
    {'Home': 'Maidstone United', 'Away': 'Hampton & Richmond Borough'},
    {'Home': 'Slough Town', 'Away': 'Welling United'},
    {'Home': 'Taunton Town', 'Away': 'Hemel Hempstead Town'},
    {'Home': 'Tonbridge Angels', 'Away': 'St. Albans City'},
    {'Home': 'Torquay United', 'Away': 'Havant & Waterlooville'},
    {'Home': 'Weymouth', 'Away': 'Farnborough'},
    {'Home': 'Worthing', 'Away': 'Weston-super-Mare'}
]

league_table = {
    'Yeovil Town': 92,
    'Chelmsford City': 83,
    'Worthing': 81,
    'Braintree Town': 81,
    'Maidstone United': 80,
    'Bath City': 73,
    'Hampton & Richmond Borough': 72,
    'Aveley': 70,
    'Farnborough': 69,
    'Slough Town': 64,
    'St. Albans City': 64,
    'Chippenham Town': 61,
    'Tonbridge Angels': 57,
    'Weymouth': 55,
    'Weston-super-Mare': 55,
    'Welling United': 53,
    'Truro City': 51,
    'Hemel Hempstead Town': 49,
    'Torquay United': 48,
    'Eastbourne Borough': 48,
    'Taunton Town': 45,
    'Dartford': 43,
    'Havant & Waterlooville': 37,
    'Dover Athletic': 27
}

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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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
