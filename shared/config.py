import sys
from pathlib import Path
import questionary
sys.path.append(str(Path(__file__).resolve().parent.parent))




def server_url():
	url = questionary.text('Enter the server URL:').ask()
	print(f'Server URL set to : {url}')
	return url

