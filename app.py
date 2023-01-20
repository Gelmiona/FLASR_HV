import random
from flask import Flask, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
ret = [1, 2, 3, 4, 5]
quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
        'rating': '*****'
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
        'rating': '*'
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
        'rating': '**'
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так.",
        'rating': '***'
    },
]

@app.route("/")
def get_all():
    return 'HELLO WORLD'

# @app.route("/about")
# def about():
#     return about_me

@app.route("/quotes/count", methods=["GET"])
def quote_counts():
    return f'"count": {len(quotes)}'

@app.route("/quotes")
def get_quotes():
    return quotes, 200

# @app.route("/quotes/random")
# def random_quote():
#     return random.choice(quotes)

@app.route("/quotes/random")
def random_quote():
    return random.choice(quotes)


@app.route("/quotes_numbers")
def get_quote_by_numbers():
    last_id = quotes[-1]["id"]
    return str(last_id+1)


@app.route("/quotes/<int:quote_id>", methods=['GET'])
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote, 200
    return f"Quote with id={quote_id} not found", 404

#изменение цитаты, код с урока
@app.route("/quotes/<int:quote_id>", methods=['PUT'])
def edit_quote(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            new_data = request.json
            if 'text' in new_data:
                quote['text'] = new_data['text']
            if 'author' in new_data:
                quote['author'] = new_data['author']
            return quote, 200
    return f"Quote with id={quote_id} not found", 404

# добавление новой цитаты + одну *
@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    #last_id = quotes[-1]["id"]
    new_quote["id"] = int(get_quote_by_numbers())
    if 'rating' not in new_quote or len(new_quote['rating'])> 5:
        new_quote['rating'] = ret[0]*'*'
    quotes.append(new_quote)
    return new_quote, 201


#фильтр по заданному рейтингу или автору в одной функции
@app.route("/quotes/filter", methods=['GET'])
def filter():
    res = []
    args = request.args
    for i in quotes:
        for k,v in args.items():
            if k =='author':
                if i['author'] == v:
                    res.append(i['text'])
            elif k == 'rating':
                if i['rating'] == v:
                    res.append(i['text'])
    if res:
        return res
    return f"Quote parametrs not find.", 200

#поиск по заданному диапазану рейтинга
@app.route("/quotes/filter2", methods=['GET'])
def filter2():
    args = request.args
    res=[]
    for i in quotes:
        for k,v in i.items():
            for v1 in args.values():
                if v==v1:
                    res.append(i)
    if res:
        return res
    return f"Quote parametrs not find.", 200

# удаление элемента
@app.route("/quotes/<int:id>", methods=['DELETE'])
def delete(id):
    for quote in quotes:
        if quote['id'] == id:
            quotes.remove(quote)
        # return quotes
        return f"Quote with id {id} is deleted.", 200




if __name__ == "__main__":
    app.run(debug=True)

