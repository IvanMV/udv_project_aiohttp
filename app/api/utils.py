import aiofiles
import asyncio
import json
from pathlib import Path 
from operator import itemgetter
from datetime import datetime
from api.settings import BASE_DIR


# Открытие файлов 
async def open_file(filename):
    path = Path(BASE_DIR, "files", filename) 
    async with aiofiles.open(path, 'r') as f:
        contents = await f.read()
    data = json.loads(contents)
    return data


# Асинхронное получение данных из файлов
async def get_data():
    filenames = ['news.json', 'comments.json']
    tasks = []
    for file in filenames:
        tasks.append(asyncio.create_task(open_file(file)))
    results = await asyncio.gather(*tasks)
    news = results[0] # Словарь всех новостей
    comments = results[1] # Словарь всех комментариев
    return news, comments


# Подсчет количества комментариев по news_id
def count_comments(comments):
    temp = {}
    comments_list = comments.get("comments")
    for i in comments_list:
        news_id = i.get("news_id")
        if temp.get(news_id):
            temp[news_id] += 1
        else:
            temp[news_id] = 1
    return temp


# Получение текущей даты в формате ISO 8601
def current_date():
    return datetime.now().replace(microsecond=0).isoformat()


# Обработка полученного словаря новостей для вывода
async def edit_news():
    # Загрузка новостей и комментариев из файлов 
    news, comments = await get_data()
    
    # Создание словаря {"news_id": число комментариев}
    number_of_comments = count_comments(comments)
    
    # Получение текущей даты в формате ISO 8601
    iso_date = current_date()
    
    # Временный список для хранения новостей после фильтрации
    news_new_list = []
    
    # Фильтрация новостей по дате и удалению, добавление числа комментариев
    list_of_news = news.get("news")
    for i in list_of_news:
        if not i.get("deleted") and i.get("date") <= iso_date:
            id = i.get("id")
            comments_count = number_of_comments.get(id)
            if comments_count:
                i["comments_count"] = comments_count
            else:
                i["comments_count"] = 0
            news_new_list.append(i)
            
    # Сортируем отфильтрованные записи новостей по дате
    news_new_list.sort(key=itemgetter('date'))
    
    # Собираем итоговый словарь новостей
    news_final = {}
    news_final["news"] = news_new_list
    news_final["news_count"] = len(news_new_list)
    return news_final


# Отображение новости по id
async def show_news_by_id(id):
    # Проверка id новости
    try:
        id = int(id)
    except:
        return None
    
    # Загрузка новостей и комментариев из файлов 
    news, comments = await get_data()
    list_of_news = news.get("news")
    
    # Получение новости по ее id
    current_news = next((i for i in list_of_news if i.get("id") == id), None)
    if not current_news:
        return None
        
    # Получение текущей даты в формате ISO 8601
    iso_date = current_date()
        
    # Применение фильтров по дате и удаленной новости
    if current_news.get("deleted") == True or current_news.get("date") >= iso_date:
        return None
    
    # Создание списка комментариев к новости по id новости
    news_comments = []
    for i in comments.get("comments"):
        if i.get("news_id") == id:
            news_comments.append(i)
    
    # Сортируем комментарии к новости по дате
    news_comments.sort(key=itemgetter('date'))
    
    # Добавить список комментариев к новости
    current_news["comments"] = news_comments
    
    # Добавить число комментариев к новости
    current_news["comments_count"] = len(news_comments)
    return current_news


    