from bs4 import BeautifulSoup
import pandas as pd
import requests 
import time

all_teams = [] ## list to store all teams

html = requests.get('https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats#all_league_summary').text ##getting the html from the website
soup = BeautifulSoup(html, 'lxml')
table = soup.find_all('table', class_ = 'stats_table')[0] ##only want the first table, therefore the first index

links = table.find_all('a') ## finding all links in the table 
links = [l.get("href") for l in links] ##parsing through links
links = [l for l in links if '/squads/' in l] ##filtering through links to only get squads

team_urls = [f"https://fbref.com{l}" for l in links] ## formatting back to links

for team_url in team_urls: 
    team_name = team_url.split("/")[-1].replace("-Stats", "") 
    data = requests.get(team_url).text
    soup = BeautifulSoup(data, 'lxml')
    stats = soup.find_all('table', class_ = "stats_table")[0] 

    if stats and stats.columns: stats.columns = stats.columns.droplevel() ##formatting the stats

    team_data = pd.read_html(str(stats))[0]
    team_data["Team"]= team_name
    all_teams.append(team_data)
    time.sleep(5)

stat_df = pd.concat(all_teams) ## concatenating all of the stats
stat_df.to_csv("stats.csv") ## importing to csv