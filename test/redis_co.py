from redis import Redis
import json

connect=Redis(host='10.2.10.134')
data=connect.lrange('u_24', 0, 499)
for item in data:
    print '*'*80
    
    di=json.loads(item)
    print di['username']
    print di['contents']