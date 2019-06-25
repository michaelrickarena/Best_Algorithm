import itertools
import csv
from collections import defaultdict
players_by_position = defaultdict(list)

k=10

Target={'SP':2,'C':1,'1B':1,'2B':1,'3B':1,'SS':1,'OF':3}

players={'Fernando Tatis Jr. (12805819)': {'cost': 5700, 'position': 'SS', 'team': 'COL'}, 'Trevor Story (12805822)': {'cost': 5500, 'position': 'SS', 'team': 'SDP'}, 'Francisco Lindor (12805834)': {'cost': 5200, 'position': 'SS', 'team': 'DET'}, 'Jorge Polanco (12805846)': {'cost': 5000, 'position': 'SS', 'team': 'KCR'}, 'Daniel Murphy (12805833)': {'cost': 5400, 'position': '1B', 'team': 'SDP'}, 'Freddie Freeman (12805849)': {'cost': 5000, 'position': '1B', 'team': 'PHI'}, 'Eric Hosmer (12805885)': {'cost': 4700, 'position': '1B', 'team': 'COL'}, 'Carlos Santana (12805875)': {'cost': 4800, 'position': '1B', 'team': 'DET'}, 'Brendan Rodgers (12806073)': {'cost': 3800, 'position': '2B', 'team': 'SDP'}, 'Derek Dietrich (12805893)': {'cost': 4600, 'position': '2B', 'team': 'TEX'}, 'Ryan McMahon (12805938)': {'cost': 4300, 'position': '2B', 'team': 'SDP'}, 'Whit Merrifield (12805918)': {'cost': 4500, 'position': '2B', 'team': 'MIN'}, 'Alex Bregman (12805848)': {'cost': 5100, 'position': '3B', 'team': 'TOR'}, 'Manny Machado (12805934)': {'cost': 4300, 'position': '3B', 'team': 'COL'}, 'Anthony Rendon (12805824)': {'cost': 5400, 'position': '3B', 'team': 'ARI'}, 'Matt Chapman (12805957)': {'cost': 4200, 'position': '3B', 'team': 'SEA'}, 'Mitch Garver (12805825)': {'cost': 5300, 'position': 'C', 'team': 'KCR'}, 'Gary Sanchez (12805880)': {'cost': 4700, 'position': 'C', 'team': 'CHW'}, 'Robinson Chirinos (12805898)': {'cost': 4500, 'position': 'C', 'team': 'TOR'}, 'J.T. Realmuto (12805892)': {'cost': 4600, 'position': 'C', 'team': 'ATL'}, 'Charlie Blackmon (12805818)': {'cost': 5800, 'position': 'OF', 'team': 'SDP'}, 'Franmil Reyes (12805850)': {'cost': 5000, 'position': 'OF', 'team': 'COL'}, 'David Dahl (12805826)': {'cost': 5300, 'position': 'OF', 'team': 'SDP'}, 'J.D. Martinez (12805847)': {'cost': 5000, 'position': 'OF', 'team': 'BAL'}, 'Eddie Rosario (12805874)': {'cost': 4800, 'position': 'OF', 'team': 'KCR'}, 'Ronald Acuna Jr. (12805867)': {'cost': 4900, 'position': 'OF', 'team': 'PHI'}, 'Josh Naylor (12805914)': {'cost': 4500, 'position': 'OF', 'team': 'COL'}, 'Andrew Benintendi (12805838)': {'cost': 5100, 'position': 'OF', 'team': 'BAL'}, 'Max Kepler (12805856)': {'cost': 4900, 'position': 'OF', 'team': 'KCR'}, 'Mike Trout (12805828)': {'cost': 5500, 'position': 'OF', 'team': 'TBR'}, 'Michael Brantley (12805910)': {'cost': 4500, 'position': 'OF', 'team': 'TOR'}, 'Zach Davies (12805805)': {'cost': 6800, 'position': 'SP', 'team': 'MIL'}, 'Blake Snell (12805792)': {'cost': 10000, 'position': 'SP', 'team': 'TB'}, 'Drew Pomeranz (12805808)': {'cost': 6200, 'position': 'SP', 'team': 'SF'}}


## Then loop through the players organizing them into the players_by_position
for name, player in players.items():
    player["name"] = name # Do some data cleanup
    players_by_position[player["position"]].append(player)


def create_all_position_combinations(all_combinations_by_position: dict,positions_remaining: list) -> list:
    # When there is just one position left we don't have to combine them with
    # anything so just get the player combinations and return them.
    if len(positions_remaining) == 1:
        return all_combinations_by_position[positions_remaining[0]]

    all_combinations = []
    # Get the current position we want to work with.
    current_position = positions_remaining[0]
    # Now we will go through all the current position's combinations of
    # players and combine each with all the other combinations.

    for combination in all_combinations_by_position[current_position]:
        # Generate all the other possible combinations then combine them with
        # the current position combination and then add those to our list of
        # all combinations.
        for child_combinations in create_all_position_combinations(
                all_combinations_by_position, positions_remaining[1:]):
            team_part = list(child_combinations)
            team_part.extend(combination)  # Building a possible team
            all_combinations.append(team_part)  # Save the team
    return all_combinations


player_combinations_by_position = {}
for position, total_players in Target.items():
    if total_players == 1:
        player_combinations_by_position[position] = [[player] for player in players_by_position[position]]
    else:
        player_combinations_by_position[position] = list(itertools.combinations(
            players_by_position[position],
            total_players
        ))


all_position_combinations = create_all_position_combinations(player_combinations_by_position, list(Target.keys()))


def my_sort(item): #sort by postition
    ordering = ("SP", "C", "1B", "2B", "3B", "SS", "OF")
    return ordering.index(item["position"])
all_position_combinations = [sorted(list(team), key=my_sort) for team in all_position_combinations]


minimum_cost=49899
maximum_cost=50001

all_position_combinations = [team for team in [sorted(list(team), key=my_sort) for team in all_position_combinations] if minimum_cost < sum(price["cost"] for price in team) < maximum_cost]
print(len(all_position_combinations))

final=[]
 
for c in all_position_combinations:
	elements={}
	for player in c:
		if player['team'] in elements:	
			elements[player['team']] += 1
		else:
			elements[player['team']] =1
	if len(list(elements.keys())) == 8:
		final.append(c)
	else:
		pass


print(len(final))



# Put in Excel

with open('emiko_test2.csv', 'w', newline='') as f:
	thewriter=csv.writer(f)
	thewriter.writerow(['Pitcher 1','Pitcher 2','catcher','First Base','Second Base','Third Base','Shortstop','Outfield 1','Outfield 2','Outfield 3'])
	for person_list in final:
		thewriter.writerow([person["name"] for person in person_list])












#test if works
# total = 1
# for position, combinations in player_combinations_by_position.items():
#     total *= len(list(combinations))
# print(len(all_position_combinations), total)
	