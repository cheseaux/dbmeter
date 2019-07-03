import json

jsonFile = "settings.json"

def load_settings():
  with open(jsonFile) as config_file:
    return json.load(config_file)

def write_settings(settings):
  with open(jsonFile, 'w') as fp:
    json.dump(settings, fp)
    print "Settings saved to %s : %s" % (jsonFile, settings)

def update_settings(key, newval):
  print "Updating data['%s'] to %s" % (key, newval)
  data = load_settings()
  if key not in data:
     raise Exception('No setting \'{}\' found in {}'.format(key, data))
  data[key] = newval
  write_settings(data)

def min_db():
  return int(load_settings()['minDb'])

def max_db():
  return int(load_settings()['maxDb'])

def warn_is_enabled():
  return load_settings()['warnEnabled']

def warn_duration():
  return int(load_settings()['warnDuration'])

def alarm_is_enabled():
  return load_settings()['alarmEnabled']

def alarm_duration():
  return int(load_settings()['alarmDuration'])
