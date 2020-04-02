from . import *
from .Utils import *
from .DataClasses import *
import time
import threading
from threading import Thread

from .user import bp as ubp
from .countries import bp as cbp

from html_table_extractor.extractor import Extractor
import mechanize as mc

br = mc.Browser()

app.blueprint(ubp) 
app.blueprint(cbp)

clear = 1

async def refresh() :
    global WList

    a = br.open("file:///D:/Files/Projects/Corona/Temp.html")
    b = ['<table'+i for i in a.get_data().decode().split('<table')][1:3]
    b_ = [i.split('</table>')[0]+'</table>' for i in b]
    extT,extY = map(Extractor,b_)
    extT.parse()
    extY.parse()
    tToday = extT.return_list()
    tToday.remove(tToday[0])

    db.drop_collection(WList)

    for i in tToday :
        x = Country(i)
        WList.insert_one(x._dict())

async def reset_db(db, client):
    await client.drop_database(db)
    print("DB Reset")

async def init() :
    global mClient
    global UserList
    global clear
    global WList
    global db
    global br

    br.set_handle_robots(False)
    br.addheaders = [('User-agent','Mozilla/5.0 (X11; U; Linux i686; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3')]

    loop = asyncio.get_event_loop()
    mClient = AsyncIOMotorClient(io_loop=loop)
    db = mClient["CORONA_BACK"]
    WList = db['WorldList']
    UserList = db['UserList']

    print("[+] Initialization Done")
    clear = 0

async def reFun() :
    t = 0
    while 1 :
        if t%43200 == 0 :
            print("[+] Running refresh")
            await refresh()
            t = 0
        time.sleep(1)
        t += 1

async def main():
    try :
        x = sys.argv[1]
    except IndexError :
        x = None

    if x == "reset_db":
        await reset_db(db, mClient)
        return

    await init()

    try :
        port_ = int(sys.argv[1])
    except IndexError :
        port_ = 10000
    except ValueError :
        print("[!] Invalid Port")
        print("[!] Defaulting To Port 10000")
        port_ = 10000

    sanic_server = await app.create_server(
        host="0.0.0.0", port=port_, return_asyncio_server=True
    )
    sanic_server.after_start()
    try:
        asyncio_server = sanic_server.server
        await asyncio_server.serve_forever()
    finally:
        sanic_server.before_stop()

    await sanic_server.close()

    for connection in sanic_server.connections:
        connection.close_if_idle()
    sanic_server.after_stop()

def mainFun() :
    mainCo = main()
    try:
        asyncio.run(mainCo)
    except KeyboardInterrupt:
        print("Keyboard Interrupt Main")
        exit(0)
    
def refFun() :
    refCo = reFun()
    try :
        asyncio.run(refCo)
    except KeyboardInterrupt :
        print("Keyboard Interrupt Refresh")

if __name__ == '__main__' :

    mainT = Thread(target=mainFun)
    refT = Thread(target=refFun)

    mainT.start()
    while clear :
        print(clear)
        time.sleep(2)
    refT.start() 
