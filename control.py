#! /c/Users/BJ/AppData/Local/Microsoft/WindowsApps/python3.11.exe


import requests
from bs4 import BeautifulSoup
import pickle
import argparse
from requests.utils import requote_uri
from requests import get

parser = argparse.ArgumentParser(
                    prog='Middle Atlantic UPS Controller',
                    description='Get and control status of outlets on Middle Atlantic UPS',
                    epilog='')

parser.add_argument('unit')
parser.add_argument('action')
parser.add_argument('-o', '--outlet', default = None)
parser.add_argument('-n', '--user', default = '')
parser.add_argument('-p', '--password', default = '')
args = parser.parse_args()

cookieFile = "C:/Users/BJ/Code/MiddleAtlantic/cookie.pickle"

def save_cookies(requests_cookiejar):
    with open(cookieFile, 'wb') as f:
        #print(requests_cookiejar)
        pickle.dump(requests_cookiejar, f)

def load_cookies():
    with open(cookieFile, 'rb') as f:
        p = pickle.load(f)
        #print(p)
        return p

##### Get command line args ####
#username = requote_uri(args.user)
#password = requote_uri(args.password)


url = 'http://192.168.50.{0}'.format(args.unit)

def do_get(URI, payload=None):
    page = requests.get(url+URI, headers = {
            'accept': '*/*',
            'Content-Type': 'multipart/form-data',
            'User-agent': 'PostmanRuntime/7.32.3'
        }, cookies=load_cookies(), params=payload, allow_redirects=False)
    #print(page.cookies)
    if page.cookies:
        save_cookies(page.cookies)
    return page

def get_outlets():
    return do_get('/outlet_individual.html')
    
def parse_outlet(soup, outlet):
    for label in soup.find_all('label'):
        if label.get('id') == 'o' + str(outlet):
            #color = label.b.font.get('color')
            status = label.b.font.string
            return status

if args.action == 'login':
    resp = do_get('/login.html')
    #if resp.status_code == 200:
    #print(resp.text)
        #pass
    login = do_get('/login.cgi', {'username': 'Hope Church', 'password': "Hopemedia1", 'action': 'LOGIN'})
    location = login.headers['Location'].split('/')
    if location[-1] == 'error3.html':
        print('Other')
    if location[-1] == 'summary.html':
        print('Success')

elif args.action == 'status':
    outlets = get_outlets()
    soup = BeautifulSoup(outlets.text, 'html.parser')
    if not args.outlet:
        for i in [1,2,3,4,5,6,7,8]:
            print(parse_outlet(soup, i))
    else:
        print(parse_outlet(soup, args.outlet))

elif args.action == 'logout':
    try:
        do_get('/logout.html')
    except(requests.exceptions.ConnectionError):
        print('Out')

elif args.action in ['on', 'off'] and args.outlet:
    do_get('/outlet_individual.cgi', {'Out{0}'.format(args.outlet): args.action, 'action': 'Apply'})
