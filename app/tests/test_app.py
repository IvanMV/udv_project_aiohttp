from api import utils
from api.utils import show_news_by_id, edit_news


# Тест главной страницы
async def test_index_view(client):
    resp = await client.get('/')
    assert resp.status == 200
    
    
# Тест страницы новости
async def test_detail_view(client):
    resp = await client.get('/news/2')
    assert resp.status == 200
    
    
# Тест ошибки 404 страницы несуцществующей новости 
async def test_detail_view_error(client):
    resp = await client.get('/news/x834a7')
    assert resp.status == 404
    

# Тест функции вывода страницы новости с несуществующими id
async def test_show_news_by_id():
    id_1 = 10009754211120123445545514445
    id_2 = 'hwteicbskfgrjvbxfshgdsjvnjdbhvcgsjc5545'
    id_3 = ''
    id_4 = None
    result_1 = await show_news_by_id(id_1)
    result_2 = await show_news_by_id(id_2)
    result_3 = await show_news_by_id(id_3)
    result_4 = await show_news_by_id(id_4)
    assert result_1 == None
    assert result_2 == None
    assert result_3 == None
    assert result_4 == None
    

# Тест функции вывода страницы новости c ненаступившей датой новости
async def test_show_news_by_id_year_1000(monkeypatch):
    def mock_get(*args, **kwargs):
        return '1000-03-26T02:24:32' # установим текущую дату 1000-03-26T02:24:32
    monkeypatch.setattr(utils, "current_date", mock_get)
    result = await show_news_by_id(2)
    assert result == None
    
    
# Тест функции вывода всех новостей c ненаступившей датой
async def test_edit_news_year_1000(monkeypatch):
    def mock_get(*args, **kwargs):
        return '1000-03-26T02:24:32' # установим текущую дату 1000-03-26T02:24:32
    monkeypatch.setattr(utils, "current_date", mock_get)
    result = await edit_news()
    assert result == {'news': [], 'news_count': 0}
