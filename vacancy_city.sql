-- Для подключения к БД
--\conn vacancy_city

-- Удаление таблицы
--DROP TABLE city CASCADE;
--DROP TABLE vacancy CASCADE;
--DROP TABLE vacancycity CASCADE;
--DROP TABLE users CASCADE;

-- Создание таблицы ГОРОД
CREATE TABLE city (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    foundation_date INT NULL,
    grp FLOAT NULL,
    climate VARCHAR NOT NULL,
    square INT NULL,
    status BOOLEAN NOT NULL,
    description VARCHAR NOT NULL,
    url_photo  VARCHAR NULL
);

-- Создание таблицы ВАКАНСИЯ
CREATE TABLE vacancy (
  id SERIAL PRIMARY KEY,
  name_vacancy VARCHAR NOT NULL,
  date_create DATE NOT NULL,
  date_form DATE NULL,
  date_close DATE NULL,
  status_vacancy VARCHAR NOT NULL,
  id_employer INT NULL,
  id_moderator INT NULL
);

-- Создание таблицы ПОЛЬЗОВАТЕЛЬ
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    admin BOOLEAN NOT NULL
);

-- Создание таблицы ВАКАНСИИГОРОДА
CREATE TABLE vacancycity (
  id SERIAL PRIMARY KEY,
  id_city INT NOT NULL,
  id_vacancy INT NOT NULL
);

-- Связывание БД внешними ключами
ALTER TABLE vacancycity
ADD CONSTRAINT FR_vacancycity_of_city
    FOREIGN KEY (id_city) REFERENCES city (id);

ALTER TABLE vacancycity
ADD CONSTRAINT FR_vacancycity_of_vacancy
    FOREIGN KEY (id_vacancy) REFERENCES vacancy (id);

ALTER TABLE vacancy
ADD CONSTRAINT FR_vacancy_of_employer
    FOREIGN KEY (id_employer) REFERENCES users (id);

ALTER TABLE vacancy
ADD CONSTRAINT FR_vacancy_of_moderator
    FOREIGN KEY (id_moderator) REFERENCES users (id);

-- ПОЛЬЗОВАТЕЛЬ (Авторизация)
INSERT INTO users (email, password, admin) VALUES
    ('user1@user.com', '1234', false),
    ('user2@user.com', '1234', false),
    ('user3@user.com', '1234', false),
    ('root@root.com', '1234', true);
-- Вывод таблицы пользователя
SELECT * FROM users;

-- ГОРОД (Услуга)
INSERT INTO city (name, foundation_date, grp, climate, square, status, description) VALUES
    ('Москва', 1147, 13.1, 'умеренный', 2561, true, 'Москва — столица и крупнейший город России. Сюда ведут многие пути и человеческие судьбы, с этим городом связано множество роковых и знаменательных событий истории, людских радостей и надежд, несчастий и разочарований, разумеется, легенд, мифов и преданий. Москва — блистательный город, во всех отношениях достойный называться столицей. Здесь великолепные памятники архитектуры и живописные парки, самые лучшие магазины и высокие небоскребы, длинное метро и заполненные вокзалы. Москва никогда не спит, здесь трудятся с утра до поздней ночи, а затем веселятся до утра.'),
    ('Санкт-Петербург', 1703, 5.6, 'умеренный', 1439, true, 'Санкт-Петербург – один из красивейших мегаполисов мира, посмотреть на который приезжают путешественники из разных уголков планеты. Раскинувшийся на побережье Финского залива, в устье реки Невы, Санкт-Петербург является вторым по величине городом России (в статусе самостоятельного субъекта федерации) и одновременно административным центром Ленинградской области и Северо-Западного федерального округа.'),
    ('Екатеринбург', 1723, 1.5, 'умеренный', 495, true, 'Екатеринбург – административный центр Свердловской области, четвёртый по численности город России. Город расположен на Среднем Урале, на восточном склоне Уральских гор. Благодаря тому, что Уральские горы в этом месте представляют собой холмы были проложены дороги из Центральной России в Сибирь. Здесь проходят железные дороги, крупные автодороги, действует международный аэропорт «Кольцово».'),
    ('Киров', 1374, 1.1, 'умеренный', 169, true, 'Киров – город и областной центр на реке Вятке, известный как родина традиционного народного промысла – дымковской игрушки, вкусного вятского кваса, легкого кукарского кружева и самобытного праздника «Свистопляска». Киров находится в Предуралье, 896 км к северо-востоку от Москвы. Город вошел в историю в роли места ссылок, где издавна отбывали заключение бунтари, не угодные власти. В середине XIX века в вятской ссылке провел семь лет знаменитый русский писатель М. Е. Салтыков-Щедрин.'),
    ('Волгоград', 1589, 1.3, 'умеренный', 859, true, 'Волгоград - город, один из крупнейших на Юге страны. Его называют портом пяти морей, Волго-Донской канал соединяет теплые южные моря – Черное, Азовское, Каспийское – с холодными Балтийским и Северным. Благодаря этому в городе интенсивно развивается торговля и кипит деловая жизнь. В городе-герое Волгограде находится множество памятников, посвященных героям Великой Отечественной войны.');
-- Вывод таблицы город
SELECT * FROM city;

-- ВАКАНСИЯ (Заявки)
INSERT INTO vacancy (name_vacancy, date_create, date_form, date_close, status_vacancy, id_employer, id_moderator) VALUES
    ('Вакансия №1', '01-01-2023', '10-01-2023', '01-03-2023', 'Введён', 1, 4),
    ('Вакансия №2', '20-05-2023', '01-06-2023', '01-08-2023', 'В работе', 2, 4),
    ('Вакансия №3', '24-09-2023', '05-10-2023', '30-11-2023', 'Завершён', 3, 4),
    ('Вакансия №4', '20-09-2023', '30-09-2023', '30-11-2023', 'Отменен', 1, 4),
    ('Вакансия №5', '20-09-2023', '30-09-2023', '30-11-2023', 'Удалён', 2, 4);
-- Вывод таблицы вакансия
SELECT * FROM vacancy;

-- ВАКАНСИИГОРОДА (вспомогательная таблица М-М услуга-заявка)
INSERT INTO vacancycity (id_city, id_vacancy) VALUES
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5);
-- Вывод таблицы ВакансииГорода
SELECT * FROM vacancycity;

-- Отображение городов, в котором статус "Закрыта"
SELECT
    c.name
FROM vacancycity as vc
INNER JOIN city as c ON vc.id_city = c.id
INNER JOIN vacancy v ON vc.id_vacancy = v.id
WHERE v.status_vacancy = 'Закрыта';

-- Отображение городов, в котором статус "Доступен"
SELECT * FROM city as C
WHERE C.status = true;

-- Отображение городов, в котором город "Киров"
SELECT
    c.name,
    c.foundation_date,
    c.square,
    c.description
FROM vacancycity as vc
INNER JOIN city as c ON vc.id_city = c.id
INNER JOIN vacancy v ON vc.id_vacancy = v.id
WHERE c.name = 'Киров';

-- Отображение всех вакансий, в котором была создана после 20.05.2023
SELECT * FROM vacancy as v
WHERE v.date_create > '19-09-2023';

-- Отображение всех городов
SELECT * FROM users;
SELECT * FROM city;
SELECT * FROM vacancy;
SELECT * FROM vacancycity;

-- Отображение индекса и статуса города
SELECT id, status FROM city;

-- Отображение города в котором статус доступен
SELECT * FROM city as C
    WHERE C.status = true;

-- Отображение города в котором индекс равен 1
SELECT * FROM city as C
WHERE C.id = 1;

-- Удаление записи в таблице город
--DELETE FROM city WHERE name = 'Москва';

-- Проверка существует ли таблица по названию города
SELECT * FROM city as C WHERE C.name = 'Сочи';