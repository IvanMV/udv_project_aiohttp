from aiohttp import web
from api.utils import edit_news, show_news_by_id


async def news_list(request):
    data = await edit_news()
    return web.json_response(data)
    
    
async def news_detail(request):
    id = request.match_info['id']
    data = await show_news_by_id(id)
    if not data:
        raise web.HTTPNotFound()
    return web.json_response(data)
