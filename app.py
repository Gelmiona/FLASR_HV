import random
from flask import Flask, request

# TODO: добавьте .gitignore в проект
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
ret = [1, 2, 3, 4, 5]
quotes = [
    {
        "id": 1,
        "author": "Rick Cook",
        "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
        'rating': '5'
    },
    {
        "id": 2,
        "author": "Waldi Ravens",
        "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
        'rating': '1'
    },
    {
        "id": 3,
        "author": "Mosher’s Law of Software Engineering",
        "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
        'rating': '2'
    },
    {
        "id": 4,
        "author": "Yoggi Berra",
        "text": "В теории, теория и практика неразделимы. На практике это не так.",
        'rating': '3'
        # TODO: Хранить рейтинг в виде звездочек не рационально
        #  "Звездочки" - это отображение рейтинга, храните в виде целого числа.
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
    # TODO: формат возвращаемого значения поправлен в соответствии с заданием
    {
        "count": len(quotes)
    }

@app.route("/quotes")
def get_quotes():
    return quotes, 200

# @app.route("/quotes/random")
# def random_quote():
#     return random.choice(quotes)

@app.route("/quotes/random")
def random_quote():
    return random.choice(quotes)


# TODO: функция к 1 практике по данной рекомендации:
#Реализуйте отдельную функцию, возвращающую новый уникальный id для цитаты. Логика работы простая: берем id последней цитаты в списке и +1
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
    # TODO: если цитаты с указанными параметрами не найдены, принято возвращать пустой список, а не 404
    
    return res, 200
   

#поиск по заданному диапазану рейтинга
@app.route("/quotes/filter2", methods=['GET'])
def filter2():
    args = request.args
    res=[]
    # TODO: переменные(i, v, v1...) переименованы.
    for quote in quotes:
        for key,value in quote.items():
            for value_args in args.values():
                if value==value_args:
                    res.append(quote)
    # TODO: возвращаем пустой список, если нет подходящих  под фильтр цитат
 
    return res, 200

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

