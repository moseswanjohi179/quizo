import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))



import pyfiglet

#adding graffiti title 

from pyfiglet import Figlet

def quizo_title():
    f = Figlet(font='graffiti')
    print(f.renderText('QUIZO'))

quizo_title()