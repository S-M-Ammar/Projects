from nba_api.stats.static import teams
nba_teams = teams.get_teams()
team_ = [team for team in nba_teams if team['full_name'] == "Washington Wizards"][0]
team_id = team_['id']
print(team_id)