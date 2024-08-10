import os

ENVIROMENT = os.getenv('ENVIROMENTOS_PATH', 'base')

from .base import *

if ENVIROMENT == 'producao':
    from .producao import *
elif ENVIROMENT == 'teste':
    from .teste import *