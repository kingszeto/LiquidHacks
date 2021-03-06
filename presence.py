from pypresence import Client
import time
import config
import pymongo
from pymongo import MongoClient
import webbrowser
import signal

def signal_handler(signum, frame):
    raise Exception("TO")

cluster = MongoClient(f"mongodb+srv://kingszeto:{config.mongo_password}@cluster0.zfror.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["rootwitch"]
collection = db["teams"]
party = collection.find({"_id": "tlwin2020"})[0]
print(party)
client_id = config.client_id
client = Client(client_id)

client.start()
client.subscribe("ACTIVITY_JOIN")

a = client.set_activity(pid=0, state=f"Watching {party['match']}",\
     details= f"Rooting for {party['team']}",\
     small_image=party['small'], small_text=party['match'],\
     large_image=party['big'], large_text=party['team'], start = time.time(),\
     party_size=[1,10000], party_id=party['_id']+'A', join=party['_id'])

print(a)
print("Begin Loop")
while True:
    time.sleep(1)
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(1)
    try:
        a = client.read_output()
        a = client.loop.run_until_complete(a)
    except:
        print("No event calls")
    if a['evt'] == 'ACTIVITY_JOIN':
        party=collection.find({"_id": a['data']['secret']})[0]
        client.set_activity(pid=0, state=f"Watching {party['match']}",\
            details= f"Rooting for {party['team']}",\
            small_image=party['small'], small_text=party['match'],\
            large_image=party['big'], large_text=party['team'], start = time.time(),\
            party_size=[1,10000], party_id=party['_id']+'A', join=party['_id'])
        # webbrowser.open('http://kingsleyszeto.me/') 
    # print(client.sock_reader.feed_data)

