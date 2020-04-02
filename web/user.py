from sanic import Blueprint
from sanic.response import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


from .DataClasses import User
from . import *

bp = Blueprint("User",url_prefix="/user")

@bp.route('/init',methods=['GET'])
async def init(request) :
    global mClient
    global UserList
    global db

    loop = asyncio.get_event_loop()
    mClient = AsyncIOMotorClient(io_loop=loop)
    db = mClient["CORONA_BACK"]
    UserList = db['UserList']

    return json({'status':'done'})