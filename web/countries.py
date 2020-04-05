from sanic import Blueprint
from sanic.response import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from .DataClasses import Country
from .Utils import *

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
    c = sorted(c,key = lambda i: i['ActiveCases'],reverse=True)
    d = sorted(c,key = lambda i: i['CasesPM'],reverse=False)
    e = sorted(c,key = lambda i: i['CasesPM'],reverse=True)
    print("Length",len(c))
    print(e[10])
    return json({'data':c,'min':float(d[0]['CasesPM']),'max':float(e[10]['CasesPM'])})

@bp.route('/get',methods=['GET','POST'])
async def Add(request) :
    print("Request Received") 
    print(request)
    a = request.json
    b = type(a)
    print("Body :",a,b) 

    n = a['cName']
    n = n.capitalize()
    n = '^'+n
    z = WList.find({'CountryName':{'$regex':n}})
    z = await z.to_list(length=10000)

    y = await Listify(z)
    y = sorted(y,key = lambda i: i['CountryName'])
    return json({'data':y})