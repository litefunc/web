import redis
import json
import pandas as pd
from controller import mysum
from sanic_cors import CORS, cross_origin
import sanic.response as response
from sanic import Sanic
from sql.pg import select, insert, delete
from common.connection import conn_local_pg
import syspath
import os
import sys
if os.getenv('MY_PYTHON_PKG') not in sys.path:
    sys.path.append(os.getenv('MY_PYTHON_PKG'))


tse = conn_local_pg('tse')
cur = tse.cursor()

r = redis.Redis(host='localhost', port=os.getenv('REDIS_DOCKER_PORT'),
                password=os.getenv('REDIS_DOCKER_PWD'), db=0, decode_responses=True)
ids_len = r.get('ids_len')
if ids_len is None:
    df = select.sd(['證券代號', '證券名稱'], 'mysum').df(tse).dropna()
    ids = list(df['證券代號'] + ' ' + df['證券名稱'])
    r.lpush('ids', *ids)
    r.set('ids_len', len(ids)-1)

ids = r.lrange('ids', 0, int(r.get('ids_len'))-1)

app = Sanic(__name__)
CORS(app, automatic_options=True)

app.static('/static', './fe/dist/static')


@app.route("/test/json", methods=['GET', 'OPTIONS'])
async def test(request):
    print({"hello": "世界"})
    # headers={'Access-Control-Allow-Origin': 'http://localhost:8080'}
    # return text("Hello, cross-origin-world!")
    print(ids)
    return response.json({"hello": "世界"}, status=200, ensure_ascii=False)


@app.route("/ids/list", methods=['GET', 'OPTIONS'])
async def test(request):
    print(ids)
    return response.json({'ids': ids}, status=200, ensure_ascii=False)


@app.route("/cols/list", methods=['GET', 'OPTIONS'])
async def test(request):
    cols = select.columns('mysum', tse)
    cols = [col for col in cols if col not in ['年月日', '證券代號', '證券名稱']]
    print(cols)
    return response.json({'cols': cols}, status=200, ensure_ascii=False)


@app.route("/data/list", methods=['POST', 'OPTIONS'])
async def test(request):
    req = json.loads(request.body)
    print(req)
    cols = ['年月日']+[col.replace('%', '%%') for col in req['cols']]
    df = select.sw(cols, 'mysum', {'證券代號': req['id']}).df(tse)
    df = df.where((pd.notnull(df)), None)  # np.nan can not covert to json
    df['年月日'] = df['年月日'].astype(str)
    d = {'labels': list(df), 'data': df.values.tolist()}
    print(d)
    return response.json(d, status=200, ensure_ascii=False)

# @app.route("/index")
# async def test(request):
#     return await response.file('./fe/dist/index.html')

# @app.route('/view')
# async def handle_request(request):
#     return response.json(mysum())

# @app.route('/json')
# async def handle_request(request):
#     return response.json('./static/index.html')

# @app.route('/file')
# async def handle_request(request):
#     return await response.file('./fe/dist/index.html')


@app.route('/test/text', methods=['GET', 'OPTIONS'])
async def handle_request(request):
    print('text')
    return response.text('hello 世界')


@app.route('/test/raw', methods=['GET', 'OPTIONS'])
async def handle_request(request):
    print('raw')
    return response.raw('./static/index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8088)
