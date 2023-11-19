import requests
import pandas as pd
import json
from apify import Actor



def get_data(domain):
    url = "https://mxtoolbox.com/api/v1/Lookup"

    querystring = {"command":"blacklist","argument":f"{domain}","resultIndex":"1","disableRhsbl":"true","format":"2"}

    headers = {
        "authority": "mxtoolbox.com",
        "accept": "json",
        "cache-control": "no-cache",
        "content-type": "application/json; charset=utf-8",
        "pragma": "no-cache",
        "referer": "https://mxtoolbox.com/SuperTool.aspx?action=blacklist%3aaol.com&run=toolpage",
        "tempauthorization": "27eea1cd-e644-4b7b-bebe-38010f55dab3",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_data = response.json()

    html = json_data['HTML_Value']

    df=pd.read_html(html)

    status = df[0]['Unnamed: 0'].values.tolist()
    blacklist = df[0]['Blacklist'].values.tolist()

    result = dict(zip(blacklist,status))
    for name, stat in result.items():
        print(name,stat)
        if stat == 'OK':
            result[name] = True
        elif stat == 'LISTED':
            result[name] =  False
        
    json_object = json.dumps(result,indent=2)
    return json_object


async def main():
    async with Actor:
        input = await Actor.get_input()
        #response = requests.get(input['url'])
        #soup = BeautifulSoup(response.content, 'html.parser')
        data = get_data(input)
        await Actor.push_data(data)

# with open('sample.json','w') as fp:
#     json.dump(result, indent=2,fp=fp)