import urllib.request
import urllib.parse


def sendSMS(apikey, numbers, sender, message):
    data = urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                                   'message': message, 'sender': sender})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return (fr)


resp = sendSMS('vV4ixMZmyok-YTys5TMHMljOCzBrfZDYc6aQzUED2B', '919035857418',
               'TXTLCL', 'Hi')
print(resp)