import docker
import re
import requests
import os
import urllib
import getpass
import json
from datetime import datetime, timedelta

def pretty_print_POST(req):
  print('{}\n{}\r\n{}\r\n\r\n{}'.format(
      '-----------START-----------',
      req.method + ' ' + req.url,
      '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
      req.body.decode('utf8'),
  ))

def pretty_print_GET(req):
  print('{}\n{}\r\n{}'.format(
      '-----------START-----------',
      req.method + ' ' + req.url,
      '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
  ))

api_key = os.environ.get('PYBOSSA_API_KEY')

if not api_key:
  print('Could not find PYBOSSA_API_KEY environment variable')

client = docker.from_env()
container = client.containers.get('pybossa-app')

if container.short_id:
  print(f'Container found: {container.short_id}')
else:
  print('Container not found...  exiting...')
  exit

pybossa_url = "http://0.0.0.0:80/"

#time_now = datetime.now()
#ten_seconds_from_now = time_now + timedelta(seconds=10)
for line in container.logs(stream=True):
  log_line = line.decode('utf8')
  print(log_line)
  regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
  url = re.findall(regex,log_line) 
  if len(url) > 0:
    pybossa_url = url[0][0].replace("0.0.0.0", "localhost")
    print(f'Found URL: {pybossa_url}')
    break

http_session = requests.session()

print(f'Testing connectivity to {pybossa_url}')
response = http_session.get(pybossa_url)

if response.status_code == 200:
  print('Able to connect to pybossa')

user = input("UserName:")
user_url = urllib.parse.urljoin(pybossa_url, f"account/{user}")
user_response = http_session.get(user_url)

if user_response.status_code == 404:
  new_user_url = urllib.parse.urljoin(pybossa_url, f"account/register")
  new_user_get_response = http_session.get(new_user_url, headers={"Content-Type": "application/json"})
  new_user_get_json = json.loads(new_user_get_response.content.decode('utf8'))

  name = input("Please enter your name:")
  email = input("Please enter your email address:")
  password = getpass.getpass("Please enter your password:")
  
  new_user_post_response = http_session.post(
    new_user_url,
    json={"email_addr": email, "fullname": name, "name": user, "password": password, "confirm": password}, 
    headers={"Content-Type": "application/json", "Accept": "text/plain", "X-CSRFToken": new_user_get_json["form"]["csrf"]})

user_api_url = urllib.parse.urljoin(pybossa_url, f"account/{user}/")
print(f"Navigate to pybossa in your browser to login: {pybossa_url}")
print(f"Once authenticated navigate to your profile: {user_api_url}")
api_key = input(f"Provide the API key on your user profile page:")

new_project_url = urllib.parse.urljoin(pybossa_url, f"project/new?api_key={api_key}")
new_project_get_response = http_session.get(new_project_url, headers={"Content-Type": "application/json"})
new_project_get_json = json.loads(new_project_get_response.content.decode('utf8'))

new_project_post_response = http_session.post(
    new_project_url,
    json={"name": "Healthsites Project", "description": "Healthsites project", "long_description": "A sample HealthSites integration project", "short_name": "sample_healthsites"}, 
    headers={"Content-Type": "application/json", "Accept": "text/plain", "X-CSRFToken": new_project_get_json["form"]["csrf"]})

new_project_post_json = json.loads(new_project_post_response.content.decode('utf8'))
update_project_url = urllib.parse.urljoin(pybossa_url, f"{new_project_post_json['next']}?api_key={api_key}")

print(update_project_url)