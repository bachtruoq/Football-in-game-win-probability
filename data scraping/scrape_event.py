import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import json

IDlist = {
    '2022-2023' : range(1640674, 1641054),
    '2021-2022' : range(1549539, 1549919),
    '2020-2021' : range(1485184, 1485564),
    '2019-2020' : range(1375927, 1376307),
    '2018-2019' : range(1284741, 1285121)
}

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
        driver.quit()

        start_index = data.find('matchCentreData')
        end_index = data.find('matchCentreEventTypeJson')

        data = data[start_index+17:end_index-14]

        data = json.loads(data)

        event_data = data['events']
        df = pd.DataFrame(event_data)
        df.to_csv('D:/hust/20231/ds/project/raw_data/'+season+'/'+matchID+'.csv', index=False)