import requests
import json
import Items

all_skins_url = "https://bymykel.github.io/CSGO-API/api/en/skins.json"
steam_api_key = ""


skins = []

i = 0

data = requests.get(all_skins_url).json()

json_object = json.dumps(data, indent=4)

# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)

while True:
    try:
        name = data[i]['name']
        min_float = data[i]['min_float']
        max_float = data[i]['max_float']
        rarity = data[i]['rarity']['name']
        collection = data[i]['collections'][0]['name']

        skin = Items.Skin(name, rarity, collection, min_float, max_float)
        skins.append(skin)
        i += 1
        #print(i)
    except:
        i += 1
        if (i > len(data)):
            break

manager = Items.TradeUpManager(skins)


calc = Items.TradeUpCalculator(manager.CreateRandomInputSkins())

average_float = calc.CalculateAverageFloat()
print("Average float is :" + str(average_float))
calc.CalculateOutcomeProbabilities(skins, average_float)
