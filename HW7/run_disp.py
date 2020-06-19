import cgi
from wsgiref.simple_server import make_server
from functools import partial
from resttest import hello_world, localtime, notfound_404,image


routes = [
    ('get', '/hello', hello_world),
    ('get', '/localtime', localtime),
    ('get', '/image', image)  # add for our server can open images    
    ]


def dispatch(routes, default_route, environ, start_response):
    path = environ['PATH_INFO']
    params = cgi.FieldStorage(environ['wsgi.input'],
                              environ=environ)
    method = environ['REQUEST_METHOD'].lower()
    environ['params'] = params
    handler = routes.get((method, path), default_route)
    return handler(environ, start_response)


def compile_routes(routes_list):
    return dict([
                ((method, path), handler)
                for method, path, handler in routes_list]
                )


if __name__ == '__main__':
    # Создаем диспетчер и регистрируем функции
    dispatcher = partial(
        dispatch,
        compile_routes(routes),
        notfound_404)

    # Запускаем базовый сервер
    httpd = make_server('', 8080, dispatcher)
    print('Serving on port 8080...')
    httpd.serve_forever()
# http://localhost:8080/hello&
