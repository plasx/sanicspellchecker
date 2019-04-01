from sanic import Sanic
from sanic.response import json
from sanic_redis import SanicRedis

app = Sanic()
app.config.update(
    {
        'REDIS': {
            'address': ('redis', 6379),
            'db': 0
        }
    }
)

redis = SanicRedis(app)


def conforms(word):
    if word == word.upper() or word == word.lower():
        return True
    else:
        for i in range(1, len(word)):
            if word[i].isupper():
                return False
    return True


def suggestions(word):
    with await redis.conn as r:
        result = await r.sismember(word[0], word)
        if result == 0:
            recommendedwords = [user for user in r.sscan_iter(word[0], match=f'{word}*')]
        if not recommendedwords and len(word) > 3:
            await suggestions(word[:-1])
        else:
            return recommendedwords

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.route('/spellcheck/<word>')
async def spellchecker(request, word):
    if conforms(word):
        with await redis.conn as r:
            result = await r.sismember(word[0], word)
            redis_check = "true" if result == 1 else "false"
            if redis_check == "false":
                import ipdb; ipdb.sset_trace()
                recommendedwords = [user for user in r.sscan_iter(word[0], match=f'{word}*')]
                print(recommendedwords)
                return json({"suggestions": [], "correct": redis_check})
        return json({"suggestions": [], "correct": redis_check})
    else:
        return json({"suggestions": [], "correct": redis_check})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
