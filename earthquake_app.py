def cities():
    all_cities = DB.cities()
    body = ['<h1>West Coast City Earthquake Data</h1>', '<ul>']
    item_template = ('<li><strong><a href="/city/{id}">{city}</a></strong>'
                     '(Average Intensity: {avg_int})</li>')
    for city in all_cities:
        body.append(item_template.format(**city))
    body.append('</ul>')
    return '\n'.join(body)


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

def city(city):
    page = """
<h1>{city}</h1>
<table>
    <tr><th>Distance from {city}:</th><td>{epi_d}</td></tr>
    <tr><th>Depth Distance from {city}:</th><td>{depth_d}</td></tr>
    <tr><th>Magnitude:</th><td>{mag}</td></tr>
    <tr><th>Intensity:</th><td>{intensity}</td></tr>
</table>
<a href="/">Back to the list</a>
"""
    city = DB.title_info(city)
    if book is None:
        raise NameError
    return page.format(**book)


class EQdb():
    def cities(self):
        cities = [dict(id=id, title=database[id]['city']) for id in
                  database.keys]

    def average_intensity(self):
        intensity = [dict(id=id, title=database[id]['avg_int']) for id in
                     database.keys]