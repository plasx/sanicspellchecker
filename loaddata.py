import redis

redisclient = redis.Redis(host='redis', port=6379, db=0)
filename = "dictionary.txt"

with open(filename, 'r') as f:
    for line in f:
        redisclient.sadd(line[0], line.split('\n')[0])
