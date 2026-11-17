import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from shared import config
import requests

server_url = config.server_url() if config.server_url() != None else "https://jsonplaceholder.typicode.com/todos/1"



server_response = requests.get(server_url)
if server_response.status_code == 200:
    welcoming_message = server_response.json()
else:
    print("Issue occured try again please")
"""except:
    print("!!!Bad URL T_T !!!")"""


print(welcoming_message)

