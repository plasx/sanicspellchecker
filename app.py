from sanic import Sanic
from sanic.response import json
from sanic.exceptions import abort
import redis

app = Sanic()

def conforms(word):
    if word == word.upper() or word == word.lower():
        return "compliant"
    else:
        for i in word[1:-1]:
            if i.isupper():
                return "noncompliant"
    if word[-1:].isupper():
        return "suggest"
    return "compliant"


def suggestions(word):
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    recommendedwords = [user for user in r.sscan_iter(word[0], match=f'{word}*')]
    if not recommendedwords and len(word) > 2:
        suggestions(word[:-1])
    else:
        return recommendedwords or []


@app.route('/spellcheck/<word>')
async def spellchecker(request, word):
    # if word == 'car':
    #     import ipdb; ipdb.sset_trace()
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
    if conforms(word) == "compliant":
        word = word.lower()
        result = r.sismember(word[0], word)
        redis_check = "true" if result is True else "false"
        if redis_check == "false":
            recommendedwords = [user for user in r.sscan_iter(word[0], match=f'{word}*')]
            return json({"suggestions": recommendedwords or [], "correct": redis_check})
        else:
            return json({"suggestions": [], "correct": "true"})
    elif conforms(word) == "suggest":
        word = word.lower()
        return json({"suggestions": suggestions(word) or [], "correct": "false"})
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
