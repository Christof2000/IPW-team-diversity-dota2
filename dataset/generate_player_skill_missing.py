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

players_df_duplicates = pd.read_csv("data_files/data_players.csv")

player_dup = {}
for item in players_df_duplicates["account_id"]:
    player_dup[item] = True


#there might be duplicate players
player_accounts = []
for item in matches_df["account_id"]:
    if item not in player_dup: 
        player_accounts.append(item)

print(str(len(player_accounts)))

def create_api_string(account_id):
    return "https://api.opendota.com/api/players/" +  str(account_id) 


firstTime = True
for account_id in player_accounts:
    r = requests.get(create_api_string(account_id=account_id))
    if r.status_code == 200:
        obj = r.json()
        del obj["profile"]

        #add account id field
        obj["account_id"] = account_id

        with open("data_files/data_" + "players" + ".csv",'a') as fd:
            
            #adding column names
            if firstTime:
                fd.write(json_to_csv_columns(obj))
                firstTime = False
            
            entry = json_to_csv(obj)
            print(entry)
            #adding entry
            fd.write(entry)

        sleep(1.5)
        if os.path.isfile("PAUSEFILE"):
            input('Remove ' + "PAUSEFILE" + ' and hit ENTER to continue')
        

    else:
        print(r._content)
        player_accounts.append(account_id)
        sleep(65)
    
