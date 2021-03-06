# Приложение для проведения опросов

Разработано по тестовому заданию

Тестовое задание – дополнительный способ для нас убедиться в вашей квалификации и понять, какого рода задачи вы выполняете эффективнее всего.
Расчётное время на выполнение тестового задания: 3-4 часа, время засекается нестрого. Приступить к выполнению тестового задания можно в любое удобное для вас время.

У текущего тестового задания есть только общее описание требований, конкретные детали реализации остаются на усмотрение разработчика.

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

## Документация

Разработано на: 
- django 2.2.10
- django-rest-framework

Разворачивание на локальной машине:
- создать виртуальное окружени и активировать его
- скачать проект командой: **git clone https://github.com/SalikovMikhail/Survey_app.git** 
- установить виртуальное окружение зависимости командой: **pip install -r requirements.txt**
- зайти в директорию survey
- ввести команду в консоль для запуска сервера: **python manage.py runserver**

### Документация к api

    
- Запрос по URL /survey/ (запрос GET) возвращает JSON, который содержит список активных опросов
, в списке элементы вида:

        {
            "id": 1,
            "date_start": "2020-11-14",
            "date_end": "2020-11-17",
            "description": "Данный опрос поможет нам анализировать состояние автомобилей у наших покупателей."
        }

- Когда получили список активных, вы можете посмотреть вопросы и ответы к ним по
URL /survey/<<int:pk>>/ (запрос GET) возвращает JSON вида:


    {
        "id": 3,
        "date_start": "2020-11-15",
        "date_end": "2020-11-25",
        "description": "Опрос владельцев животных: собак, кошек и так далее.",
        "question": [
            {
                "id": 3,
                "text": "У вас кошка или собака?",
                "type_answer": "One",
                "answer": [
                    {
                        "id": 3,
                        "text": "Кошка"
                    },
                    {
                        "id": 4,
                        "text": "Собака"
                    }
                ]
            }]
    }
    
- Вы можете начать проходить опрос анонимно или не анонимно
- Анонимно '/survey/startanonym/<<int:pk>>/', где pk - id опроса(запрос GET)
- не анонимно '/survey/start/<<int:pk>>/',  где pk - id опроса(запрос POST)
также JSON, который содержит { "id": int }. Придет JSON объект вида:

        {
             "survey": {
                "id": 3,
                "date_start": "2020-11-15",
                "date_end": "2020-11-25",
                "description": "Опрос владельцев животных: собак, кошек и так далее.",
                "question": [
                    {
                        "id": 3,
                        "text": "У вас кошка или собака?",
                        "type_answer": "One",
                        "answer": [
                            {
                                "id": 3,
                                "text": "Кошка"
                            },
                            {
                                "id": 4,
                                "text": "Собака"
                            }
                        ]
                    },
                ]
            },
            "user_id": 20
        }
 Где "user_id" - ваш id для прохожения опросов, как анонимно, так и нет.
 
 Отсюда выбираете вопрос и его тип.
 
- Чтобы отправить ответ на вопрос, нужно сделать POST запрос на URL  
'/question/answer/<<int:pk>>/', где pk - id вопроса, с объектом JSON вида:

        {       
            "user_id": 18,
            "survey_id": 3,
            "type_answer": "Text",
            "text": "Martin"
        } 
        
или если у вас тип ответа не текст:

        {
        "user_id": 18,
        "survey_id": 3,
        "type_answer": "One",
        "answer_id": 1
        }

- user_id - id пользователя, который отвечает на вопрос
- survey_id - id опроса, в котором участвует пользователей
- type_answer - тип ответа. Бывают 3 типа ответа: One - 1 вариант ответа
, Many - можно выбрать несколько вариантов, Text - ответ текстом.


- данный URL возвращает JSON объект таких видов:

        {"message": "на этот вопрос Вы уже отвечали"}
        
        {"message": "Ваш ответ записан. Вы ответили на все вопросы. Большое спасибо за участие!"}
        
        {"message": "Ваш ответ записан"}
        
        {"message": "тип ответа указан неверный"}
        
- Если вы хотите увидеть ответы пользователя на вопросы, что нужно обратиться к URL
'/user/survey-answer/' (POST запрос) в котором нужно передать JSON объект:

        {
            "user_id": int,
            "survey_id: int
        }

Где

- user_id - id пользователя для получения именно его ответов
- survey_id - id опроса, из которого нужны ответы пользователя

приходит JSON объект вида:

            {
                "Answer user": [
                    {
                        "id": 11,
                        "id_question": [
                            {
                                "id": 4,
                                "text": "Укажите животных которые у вас есть"
                            }
                        ],
                        "id_answer": [
                            {
                                "id": 5,
                                "text": "Рыбы"
                            },
                            {
                                "id": 6,
                                "text": "Птицы"
                            }
                        ],
                        "text": ""
                    },
                    {
                        "id": 10,
                        "id_question": [
                            {
                                "id": 5,
                                "text": "Напишите кличку вашего питомца"
                            }
                        ],
                        "id_answer": [],
                        "text": "Martin"
                    },
                    {
                        "id": 6,
                        "id_question": [
                            {
                                "id": 3,
                                "text": "У вас кошка или собака?"
                            }
                        ],
                        "id_answer": [
                            {
                                "id": 4,
                                "text": "Собака"
                            }
                        ],
                        "text": ""
                    }
                ],
                "survey": {
                    "id": 3,
                    "date_start": "2020-11-15",
                    "date_end": "2020-11-25",
                    "description": "Опрос владельцев животных: собак, кошек и так далее.",
                    "question": [
                        {
                            "id": 3,
                            "text": "У вас кошка или собака?",
                            "type_answer": "One",
                            "answer": [
                                {
                                    "id": 3,
                                    "text": "Кошка"
                                },
                                {
                                    "id": 4,
                                    "text": "Собака"
                                }
                            ]
                        },
                        {
                            "id": 4,
                            "text": "Укажите животных которые у вас есть",
                            "type_answer": "Many",
                            "answer": [
                                {
                                    "id": 5,
                                    "text": "Рыбы"
                                },
                                {
                                    "id": 6,
                                    "text": "Птицы"
                                },
                                {
                                    "id": 7,
                                    "text": "Хомяки"
                                }
                            ]
                        },
                        {
                            "id": 5,
                            "text": "Напишите кличку вашего питомца",
                            "type_answer": "Text",
                            "answer": []
                        }
                    ]
                }
            }
        
Исходя из данных этого JSON объекта, вы можете увидеть, какие ответы выбрал пользователь.

## Создание опросов, вопрос и ответов
Реализовал с помощью админки джанго. Создается админ, и он может создавать,
редактировать, удалять опросы, вопросы, ответы.

Django==2.2.10

djangorestframework==3.12.2

pytz==2020.4

sqlparse==0.4.1

Разработал: **Михаил Саликов**

почта: **misha.salikov@yandex.ru**

telegram: **@MikhailSalikov**