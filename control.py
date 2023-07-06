

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
        pickle.dump(requests_cookiejar, f)

def load_cookies():
    with open(cookieFile, 'rb') as f:
        return pickle.load(f)

##### Get command line args ####
#username = requote_uri(args.user)
#password = requote_uri(args.password)


url = 'http://192.168.50.{0}'.format(args.unit)

def get_login():
    r = requests.get(url + '/login.html', cookies=load_cookies())
    save_cookies(r.cookies)
    return r

def do_login():
    payload = {'username': args.user, 'password': args.password, 'action': 'LOGIN'}
    r = requests.get(url + '/login.cgi', params=payload, cookies=load_cookies())
    save_cookies(r.cookies)
    return r

def get_outlets():
    r = requests.get(url + '/outlets', cookies=load_cookies())
    save_cookies(r.cookies)
    return r

def do_outlet_action():
    r = requests.get(url + '/outlet_individual.cgi?Out{0}={1}&action=Apply'.format(outlet, action), cookies=load_cookies())
    save_cookies(r.cookies)
    return r

def do_logout():
    r = requests.get(url + '/logout.html', cookies=load_cookies())
    save_cookies(r.cookies)
    return r

def parse_outlet(outlet):
    soup = BeautifulSoup(outlet, 'html.parser')
    for label in soup.find_all('label'):
        if label.get('id') == 'o' + outlet:
            color = label.b.font.get('color')
            status = label.b.font.string
            return color, status

if args.action == 'login':
    resp = get_login()
    if resp.status_code == 200:
        #print(resp.text)
        pass
    login = do_login()
    print(login.url)
    print(login.status_code, login.text)
    logout = do_logout()
    #print(logout.status_code, logout.text)


