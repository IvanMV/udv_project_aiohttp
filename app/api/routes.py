from api.views import news_list, news_detail


def setup_routes(app):
    app.router.add_get('/', news_list, name='news_list')
    app.router.add_get('/news/{id}', news_detail, name='news_detail')