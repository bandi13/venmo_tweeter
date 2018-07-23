import requests, tweepy, time, urllib

def get_venmos():
    vens = requests.get("https://venmo.com/api/v5/public")
    return vens.json()['data']

def summarize(json):
    actor = json['actor']['firstname']
    if isinstance(json['transactions'][0]['target'], str):
        target = json['transactions'][0]['target']
    elif 'firstname' in json['transactions'][0]['target'].keys():
        target = json['transactions'][0]['target']['firstname']
    else:
        target = json['transactions'][0]['target']['name']
    method = json['type']
    message = json['message']
    if method == 'payment':
        method = 'paid'
    elif method == 'charge':
        method = 'charged'
    return actor + ' ' + method + ' ' + target + ' for "' + message + '"'

def check_for(json, items):
    if any(x in json['message'].lower() for x in items):
        return json['message']
    else: 
        return False

def check_for_drugs(json):
    items = ['heroin', 'marijuana', 'drug', 'cocaine', 'meth', 'weed', 'pills', 'sherm', 'pcp', 'kush', '420', 'baked', 'high']
    return check_for(json,items)

def check_for_sex(json):
    items = ['sex', 'hooker', 'booty', 'tit', 'boob']
    return check_for(json,items)

def check_for_alcohol(json):
    items = ['alcohol', 'drank', 'beer', 'drink', 'liquor', 'wine']
    return check_for(json,items)

def main():
    while True:
      vens = get_venmos()
      for ven in vens:
          if check_for_drugs(ven):
              print("IsDrug: " + summarize(ven))
          elif check_for_sex(ven):
              print("IsSex: " + summarize(ven))
          elif check_for_alcohol(ven):
              print("IsAlc: " + summarize(ven))
#          else:
#              print("Boring: " + summarize(ven))
      time.sleep(5)

if __name__ == '__main__':
  main()
