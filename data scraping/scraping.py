from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import requests
import csv
from io import StringIO
import pandas as pd
from datetime import datetime, timedelta

IDlist = {
    '2018-2019' : range(1284741, 1285121),
    '2019-2020' : range(1375927, 1376307),
    '2020-2021' : range(1485184, 1485564),
    '2021-2022' : range(1549539, 1549919),
    '2022-2023' : range(1640674, 1641054)
}

csv_file = 'pregame_data/pregame_data.csv'

keylist = ['match_id', 'date', 'home_team', 'away_team', 'home_team_id', 'away_team_id', 'home_team_elo', 'away_team_elo']

with open(csv_file, 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=keylist)

    if file.tell() == 0:
        writer.writeheader()

    for season, urls in IDlist.items():
        for matchID in urls:
            matchID = str(matchID)
            url = 'https://1xbet.whoscored.com/Matches/'+matchID+'/Live'
            driver = webdriver.Chrome()
            driver.get(url)

            data_xpath = '/html/body/div[4]/script[1]'
            wait = WebDriverWait(driver, 300)
            data_element = wait.until(EC.presence_of_element_located((By.XPATH, data_xpath)))
            data = data_element.get_attribute('innerHTML')
            start_index = data.find('matchCentreData')
            end_index = data.find('matchCentreEventTypeJson')

            data = data[start_index+17:end_index-14]
            data = json.loads(data)

            event_data = data['events']
            df = pd.DataFrame(event_data)
            df.to_csv('event_data/'+matchID+'.csv', index=False)

            date = data['startTime'][:-9]
            ddate = datetime.strptime(date, '%Y-%m-%d')

            previous_day = ddate - timedelta(days=1)
            predate = previous_day.strftime('%Y-%m-%d')

            r = requests.get('http://api.clubelo.com/'+predate)
            elo_data = StringIO(r.text)
            elo = pd.read_csv(elo_data, sep=",")
            
            name_xpath = '/html/body/div[4]/div[3]/div[1]/div[2]/table/tbody/tr[1]'
            wait = WebDriverWait(driver, 300)
            name_element = wait.until(EC.presence_of_element_located((By.XPATH, name_xpath)))
            name = name_element.get_attribute('innerHTML')
            driver.quit()

            end_index = name.find('</a>')
            start_index = name[:end_index].rfind('>')
            home_team_name = name[start_index+1:end_index]
            if home_team_name == 'Man Utd': home_team_name = 'Man United'
            if home_team_name == 'WBA': home_team_name = 'West Brom'
            if home_team_name == 'Sheff Utd': home_team_name = 'Sheffield United'
            if home_team_name == 'Nottingham Forest': home_team_name = 'Forest'
            end_index = name.rfind('</a>')
            start_index = name[:end_index].rfind('>')
            away_team_name = name[start_index+1:end_index]
            if away_team_name == 'Man Utd': away_team_name = 'Man United'
            if away_team_name == 'WBA': away_team_name = 'West Brom'
            if away_team_name == 'Sheff Utd': away_team_name = 'Sheffield United'
            if away_team_name == 'Nottingham Forest': away_team_name = 'Forest'

            home_team_elo = elo.loc[elo['Club'] == home_team_name, 'Elo'].values[0]
            away_team_elo = elo.loc[elo['Club'] == away_team_name, 'Elo'].values[0]

            instance_data = {
                'match_id' : matchID,
                'date' : date,
                'home_team' : home_team_name,
                'away_team' : away_team_name,
                'home_team_id' : data['home']['teamId'],
                'away_team_id' : data['away']['teamId'],
                'home_team_elo' : home_team_elo,
                'away_team_elo' : away_team_elo
            }

            writer.writerow(instance_data)