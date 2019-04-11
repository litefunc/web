import pandas as pd
import numpy as np
import cytoolz.curried
import datetime as dt
import os
import sys
if os.getenv('MY_PYTHON_PKG') not in sys.path:
    sys.path.append(os.getenv('MY_PYTHON_PKG'))
import syspath
from common.env import PG_PWD, PG_PORT, PG_USER
from common.connection import conn_local_pg
import sql.pg as pg
# from sql.pg import select, insert, delete
import web.model as model

tse = conn_local_pg('tse')

def mysum():
    return model.mysum().to_json(orient='records')