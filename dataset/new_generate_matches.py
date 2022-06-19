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


# 65953076
def create_api_string(match_id):
    return "https://api.opendota.com/api/publicMatches?less_than_match_id=" +  str(match_id) 

def match_api_string(match_id):
    return "https://api.opendota.com/api/matches/" +  str(match_id) 


new_match_id = 6595307508
firstTime = True
for i in range(400):
    r = requests.get(create_api_string(match_id=new_match_id))
    if r.status_code == 200:
        
        obj = r.json()
        print(create_api_string(match_id=new_match_id))
        print(obj)
        rows_csv_format = []

        #adding column names
        # if firstTime:
        #     rows_csv_format.append(json_to_csv_columns(obj[0]))
        #     firstTime = False

        for r in obj: 
            g = r['match_id']
            match = requests.get(create_api_string(match_id=new_match_id))
            
            if match.status_code == 200:
                match_json = match.json()
                players = match_json['players']
                for p in players:
                    if p[]
            else:
                print(r._content)
                sleep(65)

            #rows_csv_format.append(json_to_csv(r))
        print('done')    

        with open("data_files/data_" + "matches" + ".csv",'a') as fd:
            for r in rows_csv_format:
                fd.write(r)

        new_match_id = int(obj[-1]['match_id'])

        sleep(1)
        if os.path.isfile("PAUSEFILE"):
            input('Remove ' + "PAUSEFILE" + ' and hit ENTER to continue')
        

    else:
        print(r._content)
        sleep(65)
    
