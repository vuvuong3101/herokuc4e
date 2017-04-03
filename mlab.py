
# mongodb://<dbuser>:<dbpassword>@ds147080.mlab.com:47080/web-db
#mongodb://<dbuser>:<dbpassword>@ds141410.mlab.com:41410/web_db
import mongoengine

host = "ds141410.mlab.com"
port = 41410
db_name = "web_db"
username = "admin"
password = "admin"
def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)
def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]
def item2json(item):
    import json
    return json.loads(item.to_json())