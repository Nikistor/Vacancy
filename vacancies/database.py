import psycopg2

from prettytable import PrettyTable

class Database():
    # Подключение к БД
    def connect(self):
        try:
            # Подключение к базе данных
            self.connection = psycopg2.connect(
                host='127.0.0.1',
                port=5432,
                user='postgres',
                password='postgres',
                database='vacancy_city',
            )

            print("Успешное подключение к базе данных")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Удаление таблиц из БД
    def drop_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                DROP TABLE city CASCADE;
                DROP TABLE vacancy CASCADE;
                DROP TABLE vacancycity CASCADE;
                DROP TABLE users CASCADE;
                """)

            # Подтверждение изменений
            self.connection.commit()
            print("Успешно удалены таблицы в БД")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Создание таблицы БД и связывание таблицы
    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    -- Создание таблицы ГОРОД
                    CREATE TABLE city (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        foundation_date INT NULL,
                        grp FLOAT NULL,
                        climate VARCHAR NOT NULL,
                        square INT NULL,
                        -- Доступен/недоступен
                        status BOOLEAN NOT NULL,
                        description VARCHAR NOT NULL
                    );

                    -- Создание таблицы ВАКАНСИЯ
                    CREATE TABLE vacancy (
                      id SERIAL PRIMARY KEY,
                      name_vacancy VARCHAR NOT NULL,
                      date_create DATE NOT NULL,
                      date_form DATE NOT NULL,
                      date_close DATE NOT NULL,
                      status_vacancy VARCHAR NOT NULL,
                      id_employer INT NOT NULL,
                      id_moderator INT NOT NULL
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
            """)

            # Подтверждение изменений
            self.connection.commit()
            print("Успешно созданы таблицы в БД")

        except Exception as ex:
            print("Ошибка при работе с PostgreSQL:", ex)

    # Заполнение записи в таблицу в БД
    def insert_default_value(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    -- ПОЛЬЗОВАТЕЛЬ (Авторизация)
                    INSERT INTO users (email, password, admin) VALUES
                        ('user1@user.com', '1234', false),
                        ('user2@user.com', '1234', false),
                        ('user3@user.com', '1234', false),
                        ('user4@user.com', '1234', false),
                        ('user5@user.com', '1234', false),
                        ('root@root.com', '1234', true);

                    -- ГОРОД (Услуга)
                    INSERT INTO city (name, foundation_date, grp, climate, square, status, description) VALUES
                        ('Москва', 1147, 13.1, 'умеренный', 2561, true, 'Москва — столица и крупнейший город России. Сюда ведут многие пути и человеческие судьбы, с этим городом связано множество роковых и знаменательных событий истории, людских радостей и надежд, несчастий и разочарований, разумеется, легенд, мифов и преданий. Москва — блистательный город, во всех отношениях достойный называться столицей. Здесь великолепные памятники архитектуры и живописные парки, самые лучшие магазины и высокие небоскребы, длинное метро и заполненные вокзалы. Москва никогда не спит, здесь трудятся с утра до поздней ночи, а затем веселятся до утра.'),
                        ('Санкт-Петербург', 1703, 5.6, 'умеренный', 1439, true, 'Санкт-Петербург – один из красивейших мегаполисов мира, посмотреть на который приезжают путешественники из разных уголков планеты. Раскинувшийся на побережье Финского залива, в устье реки Невы, Санкт-Петербург является вторым по величине городом России (в статусе самостоятельного субъекта федерации) и одновременно административным центром Ленинградской области и Северо-Западного федерального округа.'),
                        ('Екатеринбург', 1723, 1.5, 'умеренный', 495, true, 'Екатеринбург – административный центр Свердловской области, четвёртый по численности город России. Город расположен на Среднем Урале, на восточном склоне Уральских гор. Благодаря тому, что Уральские горы в этом месте представляют собой холмы были проложены дороги из Центральной России в Сибирь. Здесь проходят железные дороги, крупные автодороги, действует международный аэропорт «Кольцово».'),
                        ('Киров', 1374, 1.1, 'умеренный', 169, true, 'Киров – город и областной центр на реке Вятке, известный как родина традиционного народного промысла – дымковской игрушки, вкусного вятского кваса, легкого кукарского кружева и самобытного праздника «Свистопляска». Киров находится в Предуралье, 896 км к северо-востоку от Москвы. Город вошел в историю в роли места ссылок, где издавна отбывали заключение бунтари, не угодные власти. В середине XIX века в вятской ссылке провел семь лет знаменитый русский писатель М. Е. Салтыков-Щедрин.'),
                        ('Волгоград', 1589, 1.3, 'умеренный', 859, true, 'Волгоград - город, один из крупнейших на Юге страны. Его называют портом пяти морей, Волго-Донской канал соединяет теплые южные моря – Черное, Азовское, Каспийское – с холодными Балтийским и Северным. Благодаря этому в городе интенсивно развивается торговля и кипит деловая жизнь. В городе-герое Волгограде находится множество памятников, посвященных героям Великой Отечественной войны.');

                    -- ВАКАНСИЯ (Заявки)
                    INSERT INTO vacancy (name_vacancy, date_create, date_form, date_close, status_vacancy, id_employer, id_moderator) VALUES
                        ('Вакансия №1', '01-01-2023', '10-01-2023', '01-03-2023', 'Введён', 1, 6),
                        ('Вакансия №2', '20-05-2023', '01-06-2023', '01-08-2023', 'В работе', 2, 6),
                        ('Вакансия №3', '24-09-2023', '05-10-2023', '30-11-2023', 'Завершён', 3, 6),
                        ('Вакансия №4', '20-09-2023', '30-09-2023', '30-11-2023', 'Отменен', 4, 6),
                        ('Вакансия №5', '20-09-2023', '30-09-2023', '30-11-2023', 'Удалён', 5, 6);

                    -- ВАКАНСИИГОРОДА (вспомогательная таблица М-М услуга-заявка)
                    INSERT INTO vacancycity (id_city, id_vacancy) VALUES
                        (1, 1),
                        (2, 2),
                        (3, 3),
                        (4, 4),
                        (5, 5);
                    """)

                # Подтверждение изменений
                self.connection.commit()
                print("[vacancycity, city, vacancy, users]: Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[vacancycity, city, vacancy, users]: Ошибка при заполнение данных:", ex)

    # Обновление статуса в таблице Город
    def update_status_delete_city(self, status, id_city):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE city SET status = %s WHERE id = %s;""",
                    (status, id_city)
                )
                # Подтверждение изменений
                self.connection.commit()
                print("[Status] Данные успешно обновлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[Status] Ошибка при обновление данных:", ex)

    # Закрытие БД
    def close(self):
        # Закрытие соединения
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")


# Вызов функции
db = Database()
# Вызов функции для подключения к БД
db.connect()
# Вызов функции для закрытия БД
db.close()