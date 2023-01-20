import random
from flask import Flask, abort, request, jsonify

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
ret = ["*","**", "***","****","*****"]
quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает."
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках."
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили."
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так."
    },
]


# Сериализация: list --> str
@app.route("/quotes")
def get_all_quotes():
    return quotes


@app.route("/quotes/count")
def quote_counts():
    return {
        "count": len(quotes)
    }


# dict --> str
@app.route("/quotes/random")
def random_quote(sp=quotes):
    return random.choice(sp)


@app.route("/quotes/<int:id>")
def get_quote(id):
    for quote in quotes:
        if quote["id"] == id:
            return quote

    abort(404, f"Quote with id={id} not found")

# добавление новой цитаты + одну *
@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    # print(type(new_quote))
    last_id = quotes[-1]["id"]
    new_quote["id"] = last_id + 1
    new_quote["rating"] = ret[0]

    quotes.append(new_quote)
    return new_quote, 201

#изменение цитаты
@app.route("/quotes/<int:id>", methods=['PUT'])
def edit_quote(id):
    new_data = request.json
    quote = get_quote(id)
    for key, val in new_data.items():
        quote[key] = val
    return quote, 200

#добавление рейтинга для иимеющихся цитат
@app.route("/quotes/rating", methods=['PUT'])
def rating():
    for quote in quotes:
        quote['rating']=random.choice(ret)
    return quotes

# не совсем поняла почему работает и как GET и как POST,
# и как считывать данные при использовании
# /quotes/filter?param=value
@app.route("/quotes/filter")
def filter():
    res=[]
    k=list((request.json).items())
    for quote in quotes :
        if quote[k[0][0]]==k[0][1]:
            res.append(quote['text'])
    return res, 200

# удаление элемента
@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    quote = get_quote(id)
    for i in range(len(quotes)):
        if quotes[i]==quote:
            quotes.remove(quotes[i])
        # return quotes
        return f"Quote with id {id} is deleted.", 200




if __name__ == "__main__":
    app.run(debug=True)
