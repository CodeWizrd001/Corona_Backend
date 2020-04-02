from sanic import Blueprint
from sanic.response import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from .DataClasses import Country

from . import *

bp = Blueprint("Countries",url_prefix="/countries")

async def Listify(List) :
    a = []
    for i in List :
        temp = Country(i)
        a.append(temp._dict())
    return a 

@bp.route('/init',methods=['GET'])
async def init(request) :
    global mClient
    global WList
    global db

    loop = asyncio.get_event_loop()
    mClient = AsyncIOMotorClient(io_loop=loop)
    db = mClient["CORONA_BACK"]
    WList = db['WorldList']

    return json({'status':'done'})

@bp.route('/list',methods=['GET','POST'])
async def handleResp(request) :
    print("Request Received")
    print(request)
    c = WList.find({"CountryName":{"$gt":''}})
    c = await c.to_list(length=100000)
    c = await Listify(c)
    return json({'data':c})

@bp.route('/get',methods=['POST'])
async def Add(request) :
    print("Request Received") 
    print(request)
    a = request.json
    b = type(a)
    print("Body :",a,b) 

    n = a['cName']
    n.capitalize()
    n = '^'+n
    z = WList.find({'CountryName':{'$regex':n}})
    z = await z.to_list(length=10000)

    y = await Listify(z)

    return json({'data':y})