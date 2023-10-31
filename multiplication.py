import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random


connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if not r:
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]
    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        start_response('200 OK', headers)
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            return ['Username created successfully.  <a href="/">Login</a>'.encode()]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        # This is where the game begins. This section of is code only executed if the login form works, and if the
        # user is successfully logged in
        if user:
            correct = 0
            wrong = 0

            cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies.load(environ['HTTP_COOKIE'])
                [correct_str, wrong_str] = cookies['score'].value.split(':')
                correct = int(correct_str)
                wrong = int(wrong_str)

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                factor1 = int(params['factor1'][0])
                factor2 = int(params['factor2'][0])
                answer = int(params['answer'][0])
                if answer == factor1*factor2:
                    correct += 1
                    page += '<p style="background-color: lightgreen">Correct, {} X {} = {}</p>'.format(factor1, factor2,
                                                                                                      answer)
                else:
                    wrong += 1
                    page += '<p style="background-color: red">Wrong, {} X {} = {}</p>'.format(factor1, factor2, answer)
                headers.append(('Set-Cookie', 'score={}:{}'.format(correct, wrong)))

            elif 'reset' in params:
                correct = 0
                wrong = 0

            headers.append(('Set-Cookie', 'score={}:{}'.format(correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page = page + '<h1>What is {} x {}</h1>'.format(f1, f2)

            # Create a list that stores f1*f2 (the right answer) and 3 other random answers]
            answer_choices = [f1*f2, f1-f2, f1+f2, 2*f1 + 2*f2]
            random.shuffle(answer_choices)

            index = 0
            option = ''
            for choice in answer_choices:
                if index == 0:
                    option = 'A'
                elif index == 1:
                    option = 'B'
                elif index == 2:
                    option = 'C'
                elif index == 3:
                    option = 'D'
                index += 1
                hyperlink = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}: {}</a><br>'.format(un, pw, f1, f2, choice, option, choice)
                page = page + '<br>'
                page = page + hyperlink

            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        login_url = "http://localhost:8000/login/username={}&password={}".format(un, pw)
        page = '''<!DOCTYPE html>
            <html>
            <head><title>Simple Form</title></head>
            <body>
            <h1>Multiplication</h1>
            <form>
                Username <input type="text" name="username"><br>
                Password <input type="password" name="password"><br>
                <button type="submit" formaction="/login">Submit</button>
                <button type="submit" formaction="/register">Register</button>
            </form>
            <hr>
            </body></html>'''
        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]



httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()