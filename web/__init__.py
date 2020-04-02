import asyncio
import sanic
import random
from sanic import Sanic
from sanic.response import json
import pymongo
import sys
from motor.motor_asyncio import AsyncIOMotorClient

app = Sanic("Corona")