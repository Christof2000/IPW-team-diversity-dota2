# /players/{account_id}/rankings





from time import sleep
import pandas as pd
import requests
import os


def json_to_csv(jObj):
    s = ""
    ls = jObj.keys()
    ls = sorted(ls)
    for val in ls:
        s += "," + str(jObj[val]) 
    return s[1:] + '\n'


def json_to_csv_columns(jObj):
    s = ""
    ls = jObj.keys()
    ls = sorted(ls)
    for val in ls:
        s += "," + str(val) 
    return s[1:] + '\n'


matches_df = pd.read_csv("data_files/data_matches.csv")

#there might be duplicate players
player_accounts_and_heros = []
for index, row in matches_df[["account_id", "hero_id"]].iterrows():
    player_accounts_and_heros.append(row)

def create_api_string(account_id):
    return "https://api.opendota.com/api/players/" +  str(account_id) + "/rankings"


firstTime = True
for row in player_accounts_and_heros:
    r = requests.get(create_api_string(account_id=row['account_id']))
    if r.status_code == 200:
        obj = r.json()
        res = None
        for item in obj:
            if item['hero_id'] == row['hero_id']:
                res = item
                res["account_id"] = row["account_id"]
                break        
        if res != None:
            with open("data_files/data_" + "hero_rankings" + ".csv",'a') as fd:            
                #adding column names
                if firstTime:
                    fd.write(json_to_csv_columns(res))
                    firstTime = False
                
                entry = json_to_csv(res)
                print(entry)
                #adding entry
                fd.write(entry)
        else:
            print("None")

        sleep(1.5)

        if os.path.isfile("PAUSEFILE"):
            input('Remove ' + "PAUSEFILE" + ' and hit ENTER to continue')

    else:
        print(r._content)
        print("Error -> Probably a timeout,waiting 60 seconds")
        player_accounts_and_heros.append(row)
        sleep(60)

    
