from http.server import HTTPServer, BaseHTTPRequestHandler
from requests import request
from json import JSONEncoder
from sys import exit

json_encoder = JSONEncoder()
home_page: str = open('home.html', 'r').read()
logged_in_page: str = open('logged_in.html', 'r').read()
token: str
httpd: HTTPServer

class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.path = self.path[1:]

        global token
        global httpd
        if self.path == "":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(home_page.encode())
        
        elif self.path.startswith("login"):
            code = self.path.replace("login?code=", "")
            data = f'client_id=22257&client_secret=6u2R8t1zbjA3uLY0Cy8MrjIeF79qFnqPyBqBhHP3&code={code}&grant_type=authorization_code&redirect_uri=http%3A%2F%2Flocalhost%3A6969%2Flogged_in'
            r = request('POST', 'https://osu.ppy.sh/oauth/token',
                        data=data, 
                        headers={
                            'Accept': 'application/json',
                            'Content-Type': 'application/x-www-form-urlencoded'
                        })
            if r.status_code >= 400:
                print(r.text)
                exit()
            resp_obj: dict = r.json()
            token = resp_obj['access_token']
            print(token)
            
            self.send_response(301)
            self.send_header('Location', '/logged_in')
            self.end_headers()
                
        elif self.path.startswith("logged_in"):
            r = request("GET", "https://osu.ppy.sh/api/v2/me", headers={'Authorization': f'Bearer {token}'})
            user_obj: dict = r.json()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write((logged_in_page.replace('${user.name}', user_obj['username'])).encode())

def run_server():
    server_address = ('', 6969)
    httpd = HTTPServer(server_address, MyRequestHandler)
    print('server up')
    httpd.serve_forever()

# Run the server
if __name__ == "__main__":
    run_server()
