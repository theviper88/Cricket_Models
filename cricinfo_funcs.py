import pandas as pd

filter = 'filter=advanced'
size = 'size=50'
start = 'spanmin1=01+Jan+2016'
end = 'spanval1=span'
template = 'template=results'

od_inningss = ['innings_number=1', 'innings_number=2']
test_inningss = ['innings_number=1;innings_number=2', 'innings_number=3;innings_number=4']
innings_names = ['1st Inns', '2nd Inns']


def get_batting_stats(format, team_names, teams, players):
    batting_data = pd.DataFrame(columns=['Innings', 'Team', 'Player', 'Span', 'Mat', 'Inns', 'NO', 'Runs', 'HS', 'Ave', 'BF', 'SR', '100', '50', '0', '4s', '6s', 'Unnamed: 15'])
    for tm in range(len(teams)):
        team = teams[tm]
        if format == 'class=1':
            for inns in range(len(test_inningss)): #+ ';host=2;'
                batting_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?' + format + ';' + filter + test_inningss[inns] + ';orderby=runs;' + size + ';' + start + ';' + end + ';' + team + ';' + template + ';type=batting'
                batting_table = pd.read_html(batting_url)[2]
                batting_table.insert(loc=0, column='Team', value=team_names[tm])
                batting_table.insert(loc=0, column='Innings', value=innings_names[inns])
                batting_data = batting_data.append(batting_table, ignore_index=True, sort=True)
        else:
            for inns in range(len(od_inningss)):
                batting_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?'+format+';'+filter+';'+od_inningss[inns]+';orderby=runs;'+size+';'+start+';'+end+';'+team+';'+template+';type=batting'
                batting_table = pd.read_html(batting_url)[2]
                batting_table.insert(loc=0, column='Team', value=team_names[tm])
                batting_table.insert(loc=0, column='Innings', value=innings_names[inns])
                batting_data = batting_data.append(batting_table, ignore_index=True, sort=True)
    batting_data = batting_data[batting_data['Player'].isin(players)]
    return batting_data

def get_bowling_stats(format, team_names, teams, players):
    bowling_data = pd.DataFrame(columns=['Innings', 'Team', 'Player', 'Span', 'Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'BBI', 'Ave', 'Econ', 'SR', '4', '5', 'Unnamed: 14'])
    for tm in range(len(teams)):
        team = teams[tm]
        if format == 'class=1':
            for inns in range(len(test_inningss)):
                bowling_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?' + format + ';' + filter + ';' + test_inningss[inns] + ';orderby=wickets;' + size + ';' + start + ';' + end + ';' + team + ';' + template + ';type=bowling'
                bowling_table = pd.read_html(bowling_url)[2]
                bowling_table.insert(loc=0, column='Team', value=team_names[tm])
                bowling_table.insert(loc=0, column='Innings', value=innings_names[inns])
                bowling_data = bowling_data.append(bowling_table, ignore_index=True, sort=True)
        else:
            for inns in range(len(od_inningss)):
                bowling_url = 'http://stats.espncricinfo.com/ci/engine/stats/index.html?' + format + ';' + filter + ';' + od_inningss[inns] + ';orderby=wickets;' + size + ';' + start + ';' + end + ';' + team + ';' + template + ';type=bowling'
                bowling_table = pd.read_html(bowling_url)[2]
                bowling_table.insert(loc=0, column='Team', value=team_names[tm])
                bowling_table.insert(loc=0, column='Innings', value=innings_names[inns])
                bowling_data = bowling_data.append(bowling_table, ignore_index=True, sort=True)
    bowling_data = bowling_data[bowling_data['Player'].isin(players)]
    return bowling_data
