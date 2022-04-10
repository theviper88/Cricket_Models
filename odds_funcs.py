import pandas as pd
from scipy import stats
import simulation_funcs as sim

def top_batsman_odds(batting_data, team_names):
    odds = []
    top_batsman_data = batting_data[['Team', 'Player', 'Innings', 'Mat', 'Runs']].fillna(0).replace('-',0)
    top_batsman_data['mean'] = [int(i)/int(j) if j >=5 else 0 for i,j in zip(top_batsman_data['Runs'],top_batsman_data['Mat'])]
    for team in team_names:
        for inns in ['1st Inns', '2nd Inns']:
            simulation_data = top_batsman_data[(top_batsman_data['Team']==team)&(top_batsman_data['Innings']==inns)][['Player', 'mean']]
            simulation_data = simulation_data.reset_index().drop(columns=['index'])
            team_odds = sim.batting_simulation(simulation_data, 10000)
            team_odds = pd.DataFrame(team_odds).reset_index().rename(columns={'index': 'Player', 0: 'Odds'})
            stats = top_batsman_data[(top_batsman_data['Team']==team)&(top_batsman_data['Innings']==inns)][['Player', 'Mat', 'mean']]
            team_odds = pd.merge(team_odds, stats, on='Player', how='left').sort_values(by='Odds')
            odds.append(team_odds.round(2))
    return odds

def top_bowler_odds(bowling_data, team_names):
    odds = []
    top_bowler_data = bowling_data[['Team', 'Player', 'Innings', 'Mat', 'Wkts']].fillna(0).replace('-',0)
    top_bowler_data['mean'] = [int(i)/int(j) if j >=5 else 0  for i,j in zip(top_bowler_data['Wkts'],top_bowler_data['Mat'])]
    for team in team_names:
        for inns in ['1st Inns', '2nd Inns']:
            simulation_data = top_bowler_data[(top_bowler_data['Team']==team)&(top_bowler_data['Innings']==inns)][['Player', 'mean']]
            simulation_data['mean'] = 10 * simulation_data['mean'] / sum(simulation_data['mean'])
            simulation_data = simulation_data[simulation_data['mean']>0].reset_index().drop(columns=['index'])
            team_odds = sim.bowling_simulation(simulation_data, 10000)
            team_odds = pd.DataFrame(team_odds).reset_index().rename(columns={'index': 'Player', 0: 'Odds'})
            stats = top_bowler_data[(top_bowler_data['Team']==team)&(top_bowler_data['Innings']==inns)][['Player', 'Mat', 'mean']]
            team_odds = pd.merge(team_odds, stats, on='Player', how='left').sort_values(by='Odds')
            odds.append(team_odds.round(2))
    return odds

def most_sixes_odds(batting_data, team_names):
    odds = []
    most_sixes_data = batting_data[['Team', 'Player', 'Innings', 'Mat', '6s']].fillna(0).replace('-', 0)
    most_sixes_data['mean'] = [int(i) / int(j) if j >=5 else 0 for i, j in zip(most_sixes_data['6s'], most_sixes_data['Mat'])]
    most_sixes_data['batting_first'] = [team_names[0] if ((i=='1st Inns')&(j==team_names[0])|(i=='2nd Inns')&(j==team_names[1])) else team_names[1] for i,j in zip(most_sixes_data['Innings'],most_sixes_data['Team'])]
    for team in team_names:
        simulation_data = most_sixes_data[most_sixes_data['batting_first'] == team][['Team', 'mean']]
        simulation_data = simulation_data.groupby('Team').agg('sum').reset_index()
        stats = simulation_data.copy()
        team_odds = sim.sixes_simulation(simulation_data, 10000)
        team_odds = pd.merge(team_odds, stats, on='Team', how='left').sort_values(by='Odds')
        odds.append(team_odds.round(2))
    return odds




def player_runs_odds(batting_data, team_names):
    odds = []
    batting_lines = [10.5, 15.5, 20.5, 25.5, 30.5, 35.5, 40.5, 45.5, 50.5]
    player_runs_data = batting_data[['Team', 'Player', 'Innings', 'Inns', 'Runs']].fillna(0).replace('-', 0)
    player_runs_data = player_runs_data[pd.to_numeric(player_runs_data['Inns']) >= 10]
    player_runs_data = player_runs_data[pd.to_numeric(player_runs_data['Runs']) > 0]
    player_runs_data['mean'] = [int(i) / int(j) for i, j in zip(player_runs_data['Runs'], player_runs_data['Inns'])]
    for team in team_names:
        for inns in ['1st Inns', '2nd Inns']:
            team_odds = player_runs_data[(player_runs_data['Team'] == team) & (player_runs_data['Innings'] == inns)][['Player', 'mean']]
            for line in batting_lines:
                team_odds['Under '+str(line)] = [1 / stats.distributions.expon.cdf(int(line - 0.5), scale=i, loc=0) for i in team_odds['mean']]
                team_odds['Over '+str(line)] = [1 / (1-stats.distributions.expon.cdf(int(line - 0.5), scale=i, loc=0)) for i in team_odds['mean']]
            odds.append(team_odds.round(2))
    return odds

def player_wickets_odds(bowling_data, team_names):
    odds = []
    bowling_lines = [0.5, 1.5, 2.5, 3.5, 4.5]
    player_wickets_data = bowling_data[['Team', 'Player', 'Innings', 'Inns', 'Wkts']].fillna(0).replace('-', 0)
    player_wickets_data = player_wickets_data[pd.to_numeric(player_wickets_data['Inns']) >= 10]
    player_wickets_data = player_wickets_data[pd.to_numeric(player_wickets_data['Wkts']) > 0]
    player_wickets_data['mean'] = [int(i) / int(j) for i, j in zip(player_wickets_data['Wkts'], player_wickets_data['Inns'])]
    for team in team_names:
        for inns in ['1st Inns', '2nd Inns']:
            team_odds = player_wickets_data[(player_wickets_data['Team'] == team) & (player_wickets_data['Innings'] == inns)][['Player', 'mean']]
            for line in bowling_lines:
                team_odds['Under ' + str(line)] = [1 / stats.distributions.poisson.cdf(int(line - 0.5), i, loc=0) for i in team_odds['mean']]
                team_odds['Over ' + str(line)] = [1 / (1 - stats.distributions.poisson.cdf(int(line - 0.5), i, loc=0)) for i in team_odds['mean']]
            odds.append(team_odds.round(2))
    return odds