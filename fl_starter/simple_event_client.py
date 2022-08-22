import sseclient

url = "http://34.83.215.154:4000/local-model/event"
headers = {"Accept": "text/event-stream"}
client = sseclient.SSEClient(url, headers=headers)
counter = 0
for msg in client:
    if msg.data != "":
        print(msg.data)
        print(counter)
        counter = counter + 1
