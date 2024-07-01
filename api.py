import requests
import hashlib
import time
import math

from exceptions import FailedRequestException

f = open('rand')
rand = f.readline().strip() 
f.close()

f = open('key')
apiKey = f.read().strip()
f.close()

f = open('secret')
apiSecret = f.read().strip()
f.close()


def requestURL(methodname:str, params:dict = {}) -> str:
    '''
    @param methodname: string. Name of the API endpoint 
    @param params: JSON object. Additional request parameters.
    '''
    # Request string
    base_url = "https://codeforces.com/api/"

    rqparams = []

    for i in params:
        rqparams.append( [i,params[i]] )

    rqparams.append( ["apiKey", apiKey] )

    tm = str(math.floor(time.time())) 

    rqparams.append(["time",  tm])

    rqparams.sort(key=lambda e:e[0])
    rqparams = [i[0] + "=" + i[1] for i in rqparams]
    
    joined_params = methodname + "?" + '&'.join(rqparams)
    unhashed_params = rand + "/" + joined_params + "#" + apiSecret 
    hsh = hashlib.sha512(unhashed_params.encode('utf-8')).hexdigest()

    joined_params += "&apiSig=" + rand + hsh 

    return base_url + joined_params

def apiResponse(methodname:str, params:dict = {}):
    '''
    @param methodname: name of the API endpoint being called
    @param params: parameters for the API call as a dictionary
    '''
    st = requestURL(methodname, params)
    resp = requests.get(st).json()
    time.sleep(1) # dont wanna ddos mikey's laptop! xD
    if resp["status"] != "OK":
        raise FailedRequestException("Request status was \"FAILED\"")
    else:
        return resp["result"]

