from sanic import Sanic
from sanic.response import json, file, text, raw
from sanic_cors import CORS, cross_origin
from controller import mysum

app = Sanic(__name__)
CORS(app)

app.static('/static', './fe/dist/static')

@app.route("/test", methods=['GET', 'OPTIONS'])
async def test(request):
    print({"hello": "世界"})
    return json({"hello": "世界"}, status=200, headers={'Access-Control-Allow-Origin': 'http://localhost:8080'})

@app.route("/index")
async def test(request):
    return await file('./fe/dist/index.html')

@app.route('/view')
async def handle_request(request):
    return json(mysum())

@app.route('/json')
async def handle_request(request):
    return json('./static/index.html')

@app.route('/file')
async def handle_request(request):
    return await file('./fe/dist/index.html')

@app.route('/text')
async def handle_request(request):
    return text('./fe/dist/index.html')

@app.route('/raw')
async def handle_request(request):
    return raw('./static/index.html')

if __name__ == "__main__":
    app.run(host="localhost", port=8088)