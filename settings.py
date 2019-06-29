import json

with open('settings.json') as config_file:
    data = json.load(config_file)
    print data['warn']['enabled']
