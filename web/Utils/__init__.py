from functools import wraps

client_id = "818861716713-g68oa4jvgdhhf9omtc4cjpdimil8jjas.apps.googleusercontent.com"
client_secret = "IaEK5i3mWfJuS-By0-Qy5mXp"

alph = [
    'A','B','C','D','E','F','G','H','I','J','K','L','M',
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
]

def isalpha(ch) :
    return ch in alph 

def hash(s) :
    s = ''.join([chr(ord(i)+1) for i in s])
    return s 

def Numeric(x) :
    if x == '' or x == ' ' or 'N/A' in x:
        return 0

    if type(x) is int or type(x) is float :
        return x 

    y = list(x) 
    while ',' in y :
        y.remove(',')
    x = ''.join(y)
    try :
        x = int(x)
    except ValueError :
        x = float(x)

    return x 

async def check_logged_in(user) :
    async def check_logged(func) :
        @wraps(func)
        async def check(*args,**kwargs) :
            print(func.__name__,user,type(user))
            return await func(args,kwargs)
        return check
    return check_logged