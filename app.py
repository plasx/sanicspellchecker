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
async def caseChecker(word):
    pass

async def suggestions(partofword):
    with await redis.conn as r:
        await r.set('key', 'value1')
        result = await r.sismember(partofword[0], partofword)
        redis_check = "true" if result == 1 else "false"

@app.route('/')
async def test(request):
    return json({'hello': 'world'})

@app.route('/spellcheck/<word>')
async def spellchecker(request, word):
    with await redis.conn as r:
        result = await r.sismember(word[0], word)
        redis_check = "true" if result == 1 else "false"
        if redis_check == false:
            pass

    return json({"suggestions": [], "correct": redis_check})
    # return json({'hello': f'world{word}', 'redis_results':result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
