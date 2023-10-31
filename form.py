import wsgiref.simple_server


def application(environ, start_response):
    page = '''<!DOCTYPE html>
<html>
<head><title>Simple Form</title></head>
<body>
<h1>Multiplication</h1>
<form>
    Username <input type="text" name="username"><br>
    Password <input type="password" name="password"><br>
    <input type="button" onclick="location.href='http://localhost:8000/login/';" value="submit">
    <button class="btn success">Register</button>
</form>
<hr>
</body></html>'''

    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

    return [page.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()