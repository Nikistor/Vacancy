# views - обработчик приложения
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from datetime import date

"""Шаблонизация"""
def hello(request):
    # Возврат функции без вложенных полей
    # return render(request, 'index.html', {
    #     'current_date': date.today()
    # })
    # С вложенным полями
    # return render(request, 'index.html', {'data': {'current_date': date.today()}})
    return render(request, 'index.html', {'data': {
        'current_date': date.today(),
        'list': ['python', 'django', 'html']
    }})

"""Наследование шаблонов"""
database = [
    {'id': 1, 'name': 'Москва', 'foundation_date': 1147, 'GRP': 20_450_000_000_000, 'climate': 'умеренный', 'square': 2561, 'status': 'доступен', 'description': 'Москва — столица и крупнейший город России. Сюда ведут многие пути и человеческие судьбы, с этим городом связано множество роковых и знаменательных событий истории, людских радостей и надежд, несчастий и разочарований и, разумеется, легенд, мифов и преданий. Москва — блистательный город, во всех отношениях достойный называться столицей. Здесь великолепные памятники архитектуры и живописные парки, самые лучшие магазины и высокие небоскребы, длинное метро и заполненные вокзалы. Москва никогда не спит, здесь трудятся с утра до поздней ночи, а затем веселятся до утра.'},
    {'id': 2, 'name': 'Санкт-Петербург', 'foundation_date': 1703, 'GRP': 2_600_520_000_000, 'climate': 'умеренный', 'square': 1439, 'status': 'доступен', 'description': 'Санкт-Петербург – один из красивейших мегаполисов мира, посмотреть на который приезжают путешественники из разных уголков планеты. Раскинувшийся на побережье Финского залива, в устье реки Невы, Санкт-Петербург является вторым по величине городом России (в статусе самостоятельного субъекта федерации) и одновременно административным центром Ленинградской области и Северо-Западного федерального округа.'},
    {'id': 3, 'name': 'Екатеринбург', 'foundation_date': 1723, 'GRP': 3_190_000_000_000, 'climate': 'умеренный', 'square': 495, 'status': 'доступен', 'description': 'Екатеринбург – административный центр Свердловской области, четвёртый по численности город России. Город расположен на Среднем Урале, на восточном склоне Уральских гор. Рядом проходит условная граница Европы и Азии. Благодаря тому, что Уральские горы в этом месте представляют собой холмы были проложены дороги из Центральной России в Сибирь. Здесь проходят железные дороги, крупные автодороги, действует международный аэропорт «Кольцово».'},
    {'id': 4, 'name': 'Киров', 'foundation_date': 1374, 'GRP': 332_600_000, 'climate': 'умеренный', 'square': 169, 'status': 'доступен', 'description': 'Киров – город и областной центр на реке Вятке, известный как родина традиционного народного промысла – дымковской игрушки, вкусного вятского кваса, легкого кукарского кружева и самобытного праздника «Свистопляска». Киров находится в Предуралье, 896 км к северо-востоку от Москвы. Город вошел в историю в роли места ссылок, где издавна отбывали заключение бунтари, не угодные власти. В середине XIX века в вятской ссылке провел семь лет знаменитый русский писатель М. Е. Салтыков-Щедрин.'},
    {'id': 5, 'name': 'Волгоград', 'foundation_date': 1589, 'GRP': 1_051_500_000, 'climate': 'умеренный', 'square': 859, 'status': 'доступен', 'description': 'Волгоград - город, один из крупнейших на Юге страны. Его называют портом пяти морей, Волго-Донской канал соединяет теплые южные моря – Черное, Азовское, Каспийское – с холодными Балтийским и Северным. Благодаря этому в городе интенсивно развивается торговля и кипит деловая жизнь. В городе-герое Волгограде находится множество памятников, посвященных героям Великой Отечественной войны. '},
    # {'id': 5, 'name': 'Волгоград', 'foundation_date': 1589, 'GRP': '{0:,}'.format(1_051_500_000).replace(',', ' '), 'climate': 'умеренный', 'square': 859, 'status': 'доступен', 'description': 'Волгоград - город, один из крупнейших на Юге страны. Его называют портом пяти морей, Волго-Донской канал соединяет теплые южные моря – Черное, Азовское, Каспийское – с холодными Балтийским и Северным. Благодаря этому в городе интенсивно развивается торговля и кипит деловая жизнь. В городе-герое Волгограде находится множество памятников, посвященных героям Великой Отечественной войны. '},
]
def GetCities(request):
    return render(request, 'cities.html', {'data': {
        'current_date': date.today(),
        'cities': database
    }})

def GetCity(request, id):
    # Найдем вакансию в списке по 'id'
    city = None
    for obj in database:
        if obj['id'] == id:
            city = obj
            break

    if city is None:
        raise Http404("Вакансия не найдена")

    return render(request, 'city.html', {'data': {
        'current_date': date.today(),
        'city': city
    }})

def sendText(request):
    # input_text = request.POST['text']
    if request.method == 'POST':
        # Получить значение передаваемого параметра 'text' из POST-запроса
        input_text = request.POST.get('text', '')

        # Выполнить нужные действия с полученными данными
        # Например, можно сохранить их в базу данных или выполнить какую-то логику
        # В данном случае, мы просто вернем полученный текст в ответе
        response_text = f"Вы ввели: {input_text}"

        # Вернуть ответ с результатом
        return HttpResponse(response_text)
    else:
        # Если это не POST-запрос, можно выполнить другую логику, если это необходимо
        # Например, можно вернуть страницу с формой для ввода текста
        return render(request, 'base.html')

def filter(request):
    filter_keyword = request.GET.get('filter_keyword')
    filter_field = request.GET.get('filter_field')

    if not filter_keyword:
    # if not filter_keyword or not filter_field:
        return HttpResponseBadRequest("Необходимо указать ключевое слово и поле для фильтрации")

    # if not filter_keyword or not filter_field:
        # messages.error(request, 'Необходимо указать ключевое слово и поле для фильтрации')
        # return redirect('filter')  # Ссылка на URL, на который мы хотим перенаправить пользователя

    # Преобразовать ключевое слово в строку для поиска в базе данных
    filter_keyword = str(filter_keyword)

    # Получить список услуг из базы данных
    filtered_services = []

    # if filter_field == 'name':
    filtered_services = [service for service in database if filter_keyword.lower() in service['name'].lower()]
    # elif filter_field == 'name_organize':
    #     filtered_services = [service for service in database if filter_keyword.lower() in service['name_organize']]
    # elif filter_field == 'description':
    #     filtered_services = [service for service in database if filter_keyword.lower() in service['description']]
    # elif filter_field == 'income_level':
    #     filtered_services = [service for service in database if service['income_level'] == int(filter_keyword)]
    # elif filter_field == 'ID_work_experience':
    #     filtered_services = [service for service in database if service['ID_work_experience'] == int(filter_keyword)]
    # elif filter_field == 'ID_skills':
    #     filtered_services = [service for service in database if service['ID_skills'] == int(filter_keyword)]
    # elif filter_field == 'ID_work_schedule':
    #     filtered_services = [service for service in database if service['ID_work_schedule'] == int(filter_keyword)]
    # elif filter_field == 'ID_specialization':
    #     filtered_services = [service for service in database if service['ID_specialization'] == int(filter_keyword)]

    # else:
    #     pass

    return render(request, 'filters.html', {'database': filtered_services})