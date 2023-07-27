#! /bin/python
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import sys,os
from colorama import Fore
import atexit
requests.packages.urllib3.disable_warnings()

def read_url(url):
    r=requests.get(url,verify=False)
    data=r.text
    soup = BeautifulSoup(data,"lxml")

    domain = '{uri.netloc}'.format(uri=urlparse(url))
    domain=domain.split(':')[0]
    tmp_file=open(save_dir+domain+'-tmp.txt','a')
    urls_file=open(save_dir+domain+'-urls.txt','a')
    dynamic_file=open(save_dir+domain+'-dynamic.txt','a')
    subdomain_file=open(save_dir+domain+'-subdomains.txt','a')

    for link in soup.find_all('a'):
        parsed_uri=urlparse(link.get('href'))
        link_domain='{uri.netloc}'.format(uri=parsed_uri)
        # subdomain
        if (domain!=link_domain) and (link_domain!="") and (domain in link_domain):
            subdomain_file.write(link_domain+"\n")
            print(Fore.BLUE+link_domain+Fore.RESET)

        if (link.get('href') is not None) and (link.get('href')[:4]=='http'):# or (link.get('href')[:5]=='https')):
            if domain in link.get('href'):
                # dynamic url
                if "?" in link.get('href'):
                    tmp_file.write(link.get('href')+"\n")
                    dynamic_file.write(link.get('href')+"\n")
                    urls_file.write(link.get('href')+"\n")
                    print(Fore.LIGHTRED_EX+'[*] Dynamic : '+link.get('href')+Fore.RESET)
                else:
                    urls_file.write(link.get('href')+"\n")
                    tmp_file.write(link.get('href')+"\n")
                    print(Fore.GREEN+"[+] Normal "+link.get('href')+Fore.RESET)
            elif "?" in link.get('href'):
                # tmp_file.write(link.get('href')+"\n")
                urls_file.write(url+"/"+link.get('href')+"\n")
                dynamic_file.write(url+"/"+link.get('href')+"\n")
                print(Fore.LIGHTRED_EX+"[+] Dynamic : "+link.get('href'))

def read_file():
    file=save_dir+domain+'-urls.txt'
    with open(file) as f:
        urls=f.read().splitlines()
        for url in urls:
            try:
                read_url(url)
            except Exception as e:
                print(e)
def exit_handler():
    os.system('sort -u '+save_dir+domain+'-urls.txt > '+save_dir+domain+"_sorted_urls.txt"+" 2>/dev/null")
    os.system('sort -u '+save_dir+domain+'-subdomains.txt > '+save_dir+domain+"_sorted_sub_domains.txt"+" 2>/dev/null")
    os.system('sort -u '+save_dir+domain+'-dynamic.txt > '+save_dir+domain+"_sorted_dynamic.txt"+" 2>/dev/null")
    os.system('rm -r '+save_dir+domain+'-tmp.txt '+' 2>/dev/null')
    os.system('rm -r '+save_dir+domain+'-urls.txt'+' 2>/dev/null')
    os.system('rm -r '+save_dir+domain+'-subdomains.txt'+' 2>/dev/null')
    os.system('rm -r '+save_dir+domain+'-dynamic.txt'+' 2>/dev/null')

if len(sys.argv)<2:
    print(Fore.CYAN+"Usage : links <url> <verbose>"+Fore.RESET)
    sys.exit()

url = str(sys.argv[1])
verbose=int(sys.argv[2])
parsed_uri=urlparse(url)
domain='{uri.netloc}'.format(uri=parsed_uri)
domain=domain.split(":")[0]
base_path=os.path.dirname(__file__)
save_dir=base_path+'/loot/'+domain+'/'
os.system('mkdir -p '+save_dir)

atexit.register(exit_handler)

tmp_file=save_dir+domain+'-urls.txt'
urls_file=save_dir+domain+'-urls.txt'
subdomain_file=save_dir+domain+'-subdomains.txt'
dynamic_file=save_dir+domain+'-dynamic.txt'
tmp=open(tmp_file,'w+')
tmp.close()
urls=open(urls_file,'w+')
urls.close()
subdomain=open(subdomain_file,'w+')
subdomain.close()
dynamic=open(dynamic_file,'w+')
dynamic.close()
try:
    read_url(url)
except Exception as e:
    print(e)
while (verbose!=0):
    verbose-=1
    try:
        read_file()
    except Exception as e:
        print(e)
    except KeyboardInterrupt as e:
        print("Quitting....")

