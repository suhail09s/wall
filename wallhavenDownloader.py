import requests
from bs4 import BeautifulSoup as bs
import threading
import time
import datetime
import conf
import os
from queue import Queue
q=Queue()

############################
# reads a config file attached (conf.py) with the main .py for a castomizable downloader 
try:
    open("conf.py",'r')
    search=str(conf.search).replace(' ','+') # replace space with plus to mkae the url
    dthread=int (conf.threads)
    cat=conf.cat
    purity=conf.purity
    sorting=conf.sorting    
    order=conf.order
    toprange=conf.toprange
    ratio=str(conf.ratio).replace(',','%2C')# to allow  multiple ratios
    resolution=str(conf.resolution).replace(',','%2C')# to allow multiple resolutions
    numpages=int((conf.numpages))
    startpage=int(conf.startpage)
    savedir=conf.savedir
    createfolder=str(conf.createfolder).upper
    print('all configrations has been read')
except:
    print ('Failed to read config file conf.py, please check conf.py does exist and all variables has valid values.')
##############################


gettime=datetime.datetime.today()
foldertime='{:%d-%m_%H-%M-%S}'.format(gettime)
print(gettime)
print_lock=threading.Lock()
def threader():
    while True:
        single=q.get()
        worker(single)
        q.task_done()

def worker (single):# this thread worker takes each link and try to parse the direct link of the wallpaper.
    page=pageget(single)
    parsed=parser(page)
    tagfound=tagfind(parsed,'img')
    downloader(tagfound)
    

def pageget (url):
    
    page=requests.get(url)

    return page

def parser (page):
   soup=bs(page.text,'html.parser')
   return soup

def tagfind(soup,mode):
    if mode=='catalog':
        tag1=soup.find (id='thumbs')
        tag2=tag1.findAll('a')
        return tag2

    if mode=='img':
        tag1=soup.find (id='wallpaper')
   
        return tag1
    
def listlinks (tags):
    links=[]
    for tag in tags:
        link=tag.get('href')
        splink=link.split('/')[-1]
        
        if str.isdigit(splink):
            links.append(link)
            print('added '+link)
        else:
            pass
        
    return links


def downloader(link):
    image=link.get('src')
    image='https:'+image 
    
    spname=image.split('/')
    name=spname[-1]
    newfolder=''# to avoid creating a new folder if createfolder in conf.py = False
    if createfolder==str('True').upper:
        newfolder='wallpapers-{}/'.format(foldertime)
    if not os.path.exists(savedir+newfolder):
        os.makedirs(savedir+newfolder)
    try:
        open(savedir+newfolder+'/'+name,'r') # the script will try to check if the wallpaper is already exist. 
        print(name+' is already exist.')
        
        
    except:
        r = requests.get(image, allow_redirects=True)
        open(savedir+newfolder+name, 'wb').write(r.content) # saving the wallpaper.
        print(name+' has been downloaded')
        
                              ##############################  Main script  ####################################


linksTodownload=[] # a definition of a simple list of all the wallpapers that are planned for downloading (empty at this point).


for page in range(startpage,startpage+numpages):
    
    url='https://alpha.wallhaven.cc/search?q={}&categories={}&purity={}&resolutions={}&ratios={}&topRange={}&sorting={}&order={}&page={}'\
            .format(search,cat,purity,resolution,ratio,toprange,sorting,order,str(page))  #constructing the link .
    print(url)
    page=pageget(url)
    parsed=parser(page)
    tagfound=tagfind(parsed,'catalog')
    tolist=listlinks(tagfound)

    
    for link in tolist: # simply making a list of all the links to are planned for downloading.
        linksTodownload.append(link)
if len(linksTodownload)==0: # in case there aren't any wallpapers to be downloaded(empty page for example).
    print('nothing to download')
    exit(0)
    
print('getting ready to download :'+str(len(linksTodownload))+' wallpapers')
       

print('downloading...')
start=time.time()
for single in range(dthread):# Starting a thread that processes each link.
        try:
            
             t=threading.Thread(target=threader)
             t.daemon=True
             t.start()
             
            
        except:
            print('invalid URL ')
for link in linksTodownload: #Queue manger/builder - adds all links that are planned for downloading in a queue.
    
    q.put(link)

print('#'*25)

q.join()
print('\n \n \n ######## Done downloading, Enjoy :D ########')
print ("Downloading time was :",time.time()-start)


