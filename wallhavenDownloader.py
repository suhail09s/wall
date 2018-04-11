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
    us=conf.user
    ps=conf.password
    cat=conf.cat
    mode=conf.mode
    purity=conf.purity
    sorting=conf.sorting    
    order=conf.order
    toprange=conf.toprange
    ratio=str(conf.ratio).replace(',','%2C')# to allow  multiple ratios
    resolution=str(conf.resolution).replace(',','%2C')# to allow multiple resolutions
    numpages=int((conf.numpages))
    startpage=int(conf.startpage)
    savedir=conf.savedir
    allowdublicates=conf.allowdublicates
    createfolder=str(conf.createfolder).upper
    print('all configrations has been read')
except:
    print ('Failed to read config file conf.py, please check conf.py does exist and all variables has valid values.')
    exit(1)
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
    
def login(uname,pas):
        
        url_login='https://alpha.wallhaven.cc/auth/login'
        getcsrf=c.get(url_login)
        parsedcsrf =parser(getcsrf)
        csrf=tagfind(parsedcsrf,'csrf')
        login_data=dict(csrfmiddlewaretoken=csrf, username=us,password=ps)
        c.post(url_login,data=login_data)
        checklogin=str(c.get('https://alpha.wallhaven.cc').content)
        if (checklogin.find('Welcome back')) == -1: # check if logged in or not, by simply reading the welcome msg.
            print('Failed to login,Check username and password. \nAll features that require login will be disabled.\n')
        else:
            print ('logged in')
        
        return csrf
def pageget (url):
    
    page=c.get(url)

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
    if mode=='csrf':
        tag1=soup.find (id='login')
        tag2=tag1.findAll ('input')
        csrftag=str(tag2).split('"')[5]
        return csrftag

def listlinks (tags):
    links=[]
    for tag in tags:
        link=tag.get('href')
        splink=link.split('/')
        
        if (str.isdigit(splink[-1])) and ((splink)[-2] != 'quickFavForm'):
            if (any(splink[-1] in l for l in downloadedwalls)) and allowdublicates=='True':
               print ('found dublicate')
            else:
                links.append(link)
                print('added '+link)
        else:
            pass
        
    return links


def downloader(link):
    image=''
    
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
        exit(1)
        
    except:
        r = requests.get(image, allow_redirects=True)
        open(savedir+newfolder+name, 'wb').write(r.content) # saving the wallpaper.
        print(name+' has been downloaded')
        with open("list.of.downloaded.wall.txt", "a") as myfile:
            myfile.write(name+'\n') 
        
                              ##############################  Main script  ####################################

downloadedwalls=[]
try:
    with open('list.of.downloaded.wall.txt', 'r') as f:
        downloadedwalls = [str(str(str(line.strip()).replace('.jpg',"")).replace('.png','')).replace('wallhaven-','') for line in f]
       
        print('Downloaded wallpapers list has been read.')
except:
    pass
linksTodownload=[] # a definition of a simple list of all the wallpapers that are planned for downloading (empty at this point).
ss=0
with requests.Session() as c:
    if dthread>118:
        dthread=117
        print('excedded the maximum number of threads allowed,117')
    if ss<1:
        login(1,1)
    ss=+1
    for page in range(startpage,startpage+numpages):
     if mode=='subscription':
        url='https://alpha.wallhaven.cc/subscription?purity=111&page={}'.format(str(page))
     elif mode=='search':
        url='https://alpha.wallhaven.cc/search?q={}&={}&purity={}&resolutions={}&ratios={}&topRange={}&sorting={}&order={}&page={}'\
            .format(search,cat,purity,resolution,ratio,toprange,sorting,order,str(page))  #constructing the link .
     elif mode=='favorites':
         url='https://alpha.wallhaven.cc/favorites?purity={}&page={}'.format(purity,str(page))
     print('reading page number: '+str(page))
     page=pageget(url)
     parsed=parser(page)
     tagfound=tagfind(parsed,'catalog')
     tolist=listlinks(tagfound)

    
     for link in tolist: # simply making a list of all the links to are planned for downloading.
         if any(link in l for l in linksTodownload):
             continue
         else:
            linksTodownload.append(link)
     if len(linksTodownload)==0: # in case there aren't any wallpapers to be downloaded(empty page for example).
                print('nothing to download')
       
    
    print('getting ready to download :'+str(len(linksTodownload))+' wallpapers')
   

    print('downloading...')
    start=time.time()
    for single in range(dthread):# Starting a thread that processes each link.
       try:
             
             t=threading.Thread(target=threader)
             t.daemon=True
             t.start()
             time.sleep(0.005)
            
       except:
                print('invalid URL ')
    for link in linksTodownload: #Queue manger/builder - adds all links that are planned for downloading in a queue.
    
            q.put(link)

    print('#'*25)

    q.join()
    print('\n \n \n ######## Done downloading, Enjoy :D ########')
    print ("Downloading time was :",time.time()-start)


