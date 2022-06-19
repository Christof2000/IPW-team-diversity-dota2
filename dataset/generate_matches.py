import json
import secrets
import requests
from time import sleep


def json_to_csv(jObj):
    s = ""
    for val in jObj:
        s += "," + str(jObj[val]) 
    return s[1:] + '\n'


def json_to_csv_columns(jObj):
    s = ""
    for val in jObj:
        s += "," + str(val) 
    return s[1:] + '\n'

#24*3600

epoch_timestamp =1654081668  #1651025933
upper_limit_mmr = 4000 
lower_limit_mmr = 3000

firstTime = True
game_ids = {}
count = 0
for x in range (1600):
    matchesString = "https://api.opendota.com/api/explorer?sql=select%0D%0Apublic_matches.match_id%2C%0D%0Apublic_matches.start_time%2C%0D%0Apublic_matches.avg_mmr%2C%0D%0Apublic_matches.num_mmr%2C%0D%0Apublic_matches.game_mode%2C%0D%0Apublic_matches.lobby_type%2C%0D%0Aplayer_matches.account_id%2C%0D%0Aplayer_matches.hero_id%2C%0D%0A((player_matches.player_slot%20%3C%20128)%20%3D%20public_matches.radiant_win)%20win%0D%0Afrom%20public_matches%20JOIN%20player_matches%20using(match_id)%20%0D%0Awhere%20%0D%0Apublic_matches.start_time%20%3C%3D%20"+ str(epoch_timestamp) +"%20%0D%0Aorder%20by%20start_time%20desc%20LIMIT%2040"
    #matchesString = "https://api.opendota.com/api/explorer?sql=select%0Apublic_matches.match_id%2C%0Apublic_matches.start_time%2C%0Apublic_matches.avg_mmr%2C%0Apublic_matches.num_mmr%2C%0Aplayer_matches.account_id%2C%0Aplayer_matches.hero_id%2C%0A((player_matches.player_slot%20%3C%20128)%20%3D%20public_matches.radiant_win)%20win%0Afrom%20public_matches%20JOIN%20player_matches%20using(match_id)%20%0Awhere%20num_mmr%20%3E%204%0AAND%20public_matches.start_time%20%3E%3D%20"+ str(epoch_timestamp) +"%0AAND%20public_matches.avg_mmr%20%3C%204000%0AAND%20public_matches.avg_mmr%20%3E%203000%0Aorder%20by%20start_time%20asc%20LIMIT%2020"
    #matchesString = "https://api.opendota.com/api/explorer?sql=select%0Apublic_matches.match_id%2C%0Apublic_matches.start_time%2C%0Apublic_matches.avg_mmr%2C%0Apublic_matches.num_mmr%2C%0Aplayer_matches.account_id%2C%0Aplayer_matches.hero_id%2C%0A((player_matches.player_slot%20%3C%20128)%20%3D%20public_matches.radiant_win)%20win%0Afrom%20public_matches%20JOIN%20player_matches%20using(match_id)%20%0Awhere%20num_mmr%20%3E%204%0AAND%20public_matches.start_time%20%3E%3D%20" + str(epoch_timestamp) +"%0AAND%20public_matches.avg_mmr%20%3C%204000%0AAND%20public_matches.avg_mmr%20%3E%203000"
    #if you add 1000 it increases by about 15 min
    epoch_timestamp -= 15000 #24 * 3600 * 2 # days down

    r = requests.get(matchesString)
    if r.status_code == 200:

        obj = r.json()
        rows = obj["rows"]

        count += 1
        print("Succesfull requesttt: " + str(count))
        print("Rows added: " + str(obj["rowCount"]))
        
        rows_csv_format = []
        
        #adding column names
        if firstTime:
            rows_csv_format.append(json_to_csv_columns(rows[0]))
            firstTime = False

        for r in rows: 
            if r["match_id"] not in game_ids:
                game_ids[(r["match_id"])] = 1
                rows_csv_format.append(json_to_csv(r))
            else:
                if game_ids[(r["match_id"])] > 10:
                    print("duplicate")
                    pass
                else:
                    game_ids[(r["match_id"])] += 1
                    rows_csv_format.append(json_to_csv(r))
        print('done')

        with open("data_files/data_" + "matches" + ".csv",'a') as fd:
            for r in rows_csv_format:
                fd.write(r)
        
        sleep(5)
        
    else:
        print(r._content)
        print("Error -> Probably a timeout")
        sleep(5)




# select
# public_matches.match_id,
# public_matches.start_time,
# public_matches.avg_mmr,
# public_matches.num_mmr,
# public_matches.game_mode,
# player_matches.account_id,
# player_matches.hero_id,
# ((player_matches.player_slot < 128) = public_matches.radiant_win) win
# from public_matches JOIN player_matches using(match_id) 
# where public_matches.avg_mmr < 4000
# AND public_matches.avg_mmr > 3000
# AND public_matches.start_time <= 1651025933
# order by start_time desc LIMIT 20


# select
# public_matches.match_id,
# public_matches.start_time,
# public_matches.avg_mmr,
# public_matches.num_mmr,
# public_matches.game_mode,
# player_matches.account_id,
# player_matches.hero_id,
# ((player_matches.player_slot < 128) = public_matches.radiant_win) win
# from public_matches JOIN player_matches using(match_id) 
# where 
# public_matches.start_time <= 1651025933 
# -- AND public_matches.avg_mmr < 4000
# -- AND public_matches.avg_mmr > 3000
# AND public_matches.game_mode = 2
# order by start_time desc LIMIT 20



# select
# public_matches.match_id,
# public_matches.start_time,
# public_matches.avg_mmr,
# public_matches.num_mmr,
# public_matches.game_mode,
# public_matches.lobby_type,
# player_matches.account_id,
# player_matches.hero_id,
# ((player_matches.player_slot < 128) = public_matches.radiant_win) win
# from public_matches JOIN player_matches using(match_id) 
# where 
# public_matches.start_time <= 1651025933 
# AND public_matches.game_mode = 2
# order by start_time desc LIMIT 20



# select
# public_matches.match_id,
# public_matches.start_time,
# public_matches.avg_mmr,
# public_matches.num_mmr,
# public_matches.game_mode,
# public_matches.lobby_type,
# player_matches.account_id,
# player_matches.hero_id,
# ((player_matches.player_slot < 128) = public_matches.radiant_win) win
# from public_matches JOIN player_matches using(match_id) 
# where 
# public_matches.start_time <= 1651793816 
# order by start_time desc LIMIT 40