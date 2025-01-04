# Book assistant (prototype)

## Идея проекта

Ассистент, который может отвечать на вопросы по книге. Это может быть художественная книга, это может быть учебник. Помощник может служить интерактивным конспектом или поможет найти нужную информацию в книге

__Целевая аудитория__ - студенты, школьники и все-все, кто работает с книгами.

```
Главная цель проекта для меня - сделать прототип ассистента по какой-то базе знаний. В данном случае база знаний - книга. Но технически может быть заменена на любую wiki, confluence и др.
```

## Как это работает (видео)

[![Book assistant demo](https://img.youtube.com/vi/9ZdERW4Ermo/0.jpg)](https://www.youtube.com/watch?v=9ZdERW4Ermo)

## Работающий прототип

[http://89.169.166.100:8080](http://89.169.166.100:8080)

если не работает, проверьте, что в браузере указано `http`



## Особенности реализации

1. Можно добавлять новые книги, они автоматически векторизуются в RAG
2. Книги могут быть на разных языках, общаться с ассистентом тоже можно на разных языках
3. Ассистент плохо отвечает на вопросы, на которые нет прямого ответа в тексте (точка для улучшения)
4. Поддерживает загрузку книг в txt и pdf форматах.

## Необходимые библиотеки

```
langchain==0.3.13
langchain_openai==0.2.14
langchain_community==0.3.13
faiss-cpu==1.9.0.post1
Flask==2.3.2
Werkzeug==2.3.6
pypdf==5.1.0
transliterate==1.10.2
```

## Технические особенности:

1. Модель `gpt-4o-mini` через прокси
2. `FAISS` в качестве векторного хранилища
3. `LangChain` в качестве основного фреймворка
4. `Flask` в качестве UI
5. Промтинг с добавлением релеватного контеста из RAG
6. Память в промтинге не испольуется, сходу не получилось нормально настроить

### Почему Flask вместо StreamLit

Познакомился с сервисами `V0` и `Cursor`. Захотелось сделать  более интересный визуально интерфейс чем позволяет `Streamlit`, даже если сам не умею. Вроде получилось.

Но позже столкнулся, что его чуть сложнее деплоить. Нельзя использовать бесплатный `Streamlit` сервис, надо самому думать об организации различных сессий для разных пользователей и т.д.


## Деплой

Развернул в `yandex.cloud`. Просто запустил на linux виртуальной машине. Без дocker, k8s и др. Единственное приобрел прокси, для обращения к openai.

## Что можно улучшить

1. Помощник плохо отвечает на вопросы, где нет прямых ответов в книге. Например, "О чем эта книга?" или "В чем основная мысль книги?". Поэтому надо составить большой чек-лист вопросов о книге, получить на них ответы использую "умную модель" с большим контекстом и сложить ответы в RAG. Или, как альтернативу, использовать техники промтинга с доступом к `wikipedia` и интернет, где скорее всего есть ответы на эти вопросы.

2. Добавить память при работе с ассистентом.

3. Добавить сессии, чтобы каждый пользователь работал со своими книгами и своей историей общения.

4. Добавить более умный split по книгам. Сейчас используется простой `TextSplitter`.

4. Расширить формат поддерживаемых книг

5. Настроить https для сервиса

