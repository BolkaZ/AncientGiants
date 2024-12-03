import uuid
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.shortcuts import render
from django.db import connection

USER_ID = 1

configuration_elements = [
    {
        'detail_text': "Триасовый период знаменует собой начало мезозойской эры и эпохи динозавров. Этот период начался после того, как худшее в истории вымирание уничтожило жизнь. В раннем триасе климатические условия были чрезвычайно жаркими и засушливыми. В результате это приводит к появлению широко распространенной пустыни и ландшафта. Однако с течением времени погода стала мягкой и влажной. Кроме того, здесь преобладают млекопитающие рептилии, такие как листрозавр."
        ' Около 240 миллионов лет назад в летописи окаменелостей появились первые динозавры. Это Герреразавр и Эораптор. Итак, начинается хронология эволюции динозавров. В этот период они были относительно небольшими и не такими большими, какими станут в более поздние периоды. У них также есть рот, вытянутый от уха до уха, и острые зигзагообразные зубы. Кроме того, некоторые группы рептилий, такие как кодоны и терапсиды, занимают видное место. Хотя архозавры, не относящиеся к динозаврам, продолжали занимать видное место, динозавры быстро диверсифицировались. Вскоре после этого динозавры уже разделились на две основные группы. Это были Saurischia и Ornithoscelida.'
        ' 201,3 миллиона лет назад произошло еще одно массовое вымирание, когда климат изменился. Таким образом, завершился триасовый период.',
        'end': '201 млн лет назад',
        'id': 1,
        'image': 'http://127.0.0.1:9000/paleoproject/png1.webp',
        'name': 'Триасовый период',
        'start': '252 млн лет назад'
    },
    {
        'detail_text': 'Юрский период — второй из трёх периодов мезозойской эры. Это часто ассоциируется с пышной тропической средой. Что еще более важно, именно здесь существовали динозавры, такие как брахиозавр и аллозавр. Животные и растения жили на суше, а моря восстановились после вымирания. Климат в целом был теплее и стабильнее, чем в триасовый период. Есть также обильные леса и мелководные моря.'
        ' Когда начался юрский период, существовало два основных континента. Это Лавразия и Гондвана. 200 миллионов лет назад появились птерозавры. Это первые позвоночные, развившие двигательный полет. У этих рептилий длинные членистые хвосты, нет перьев, и они могут летать, только паря.'
        ' Затем по суше бродили динозавры в юрском периоде. Они обозначили буквально большой путь. Апатозавр, также известный как Бронтозавр, весил до 30 тонн и имел длину шеи до 22 метров. Затем целофизы — хищные динозавры. Они ходят на двух ногах, их длина составляет 2 метра, а вес - 23 килограмма. На землю добрался и первый пернатый динозавр – археоптерикс. Растительноядный брахиозавр имеет рост до 16 метров и вес более 80 тонн. При этом длина Диплодока тоже была 26 метров.',
        'end': '145 млн лет назад',
        'id': 2,
        'image': 'http://127.0.0.1:9000/paleoproject/png2.jpg',
        'name': 'Юрский период',
        'start': '201 млн лет назад'
    },
    {
        'detail_text': 'Произошло незначительное вымирание, завершившее юрский период. В результате этого вымирания погибли многие виды доминирующих рептилий. И это знаменует собой начало третьей эры мезозойской эры, которая произошла около 145 миллионов лет назад. Фактически, это последняя, но самая продолжительная эра из трех периодов, предшествовавших вымиранию динозавров.'
        ' Меловой период стал периодом расцвета знаменитого и крупнейшего вида динозавров. Сюда входят тираннозавр рекс и трицератопс. Тираннозавр рекс — гигантский хищный динозавр, который, возможно, также является падальщиком и может бегать со скоростью до 40 км/ч. А у трицератопса было два рога над глазами и рог поменьше на кончике морды. Климат в то время в целом был теплым, и в нем продолжалось преобладание цветковых растений. Но к концу периода температура начала колебаться.'
        ' Меловой период также закончился одним из самых известных событий массового вымирания. Это мел-палеогеновое (K-Pg) вымирание, уничтожившее большинство динозавров и многие другие виды.',
        'end': '66 млн лет назад',
        'id': 3,
        'image': 'http://127.0.0.1:9000/paleoproject/png3.jpg',
        'name': 'Меловой период',
        'start': '145 млн лет назад'
    }
]

orders = {
    0: [
        {'id': 4, 'name': 'Платеозавр', 'quantity': 3},
        {'id': 5, 'name': 'Целофизис', 'quantity': 2}
    ],
    1: [
        {'id': 5, 'name': 'Тираннозавр', 'quantity': 1},
        {'id': 6, 'name': 'Велоцираптор', 'quantity': 5}
    ],
    2: [
        {'id': 7, 'name': 'Брахиозавр', 'quantity': 2}
    ]
}

def bid_view(request):
    order_id = 0 
    cart_items = orders[order_id] 
    return render(request, 'animal.html', {'cart_items': cart_items, 'order_id': order_id})



def index(request):
    query = request.GET.get('q', '')
    results = [item for item in configuration_elements if query.lower() in item['name'].lower()]


    if not query or not results:
        results = configuration_elements

    return render(request, 'main.html', {'results': results, 'query': query})


def getDetailPage(request, id):
    item = next((el for el in configuration_elements if el['id'] == id), None)
    
    if item is None:
        return redirect('some-error-page')

    return render(request, 'description.html', {'item': item})

