import requests
from bs4 import BeautifulSoup as bs
import threading
import time
import datetime
import conf
import os
from queue import Queue
import subprocess
import random

from colorama import init
from termcolor import colored

# use Colorama to make Termcolor work on Windows too
init()

# then use Termcolor for all colored text output

q=Queue()
############################
# reads a config file attached (conf.py) with the main .py for a castomizable downloader 

try:
    co=open("conf.py",'r')
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
    allowduplicates=conf.allowduplicates
    createfolder=str(conf.createfolder).upper
    openfolderafter=conf.openfolderafter
    favTag=conf.favTag
    print('all configrations has been read')
    print('Downloading all wallpapers about ({}) based on {} sorting from page number {} to page number {} \nthat are {} old to folder under {} with {} thread/s'\
                                                    .format(search,sorting,startpage,(startpage+numpages-1),toprange,savedir,dthread))
    co.close()
    
except:
    print ('****Failed to read config file conf.py, please check conf.py does exist and all variables has valid values.****')
    exit(1)
##############################

downloadedwalls=[]
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
        print('Logging in....')
        url_login='https://alpha.wallhaven.cc/auth/login'
        getcsrf=c.get(url_login)
        parsedcsrf =parser(getcsrf)
        global csrf
        csrf=tagfind(parsedcsrf,'csrf')
        login_data=dict(csrfmiddlewaretoken=csrf, username=us,password=ps)
        c.post(url_login,data=login_data)
        checklogin=str(c.get('https://alpha.wallhaven.cc').content)
        if (checklogin.find('Welcome back')) == -1: # check if logged in or not, by simply reading the welcome msg.
            print('****Failed to login,Check username and password. ****\n****All features that require login will be disabled.**** \n')
        else:
            print ('logged in :D')
        
        return csrf
def pageget (url):
    
    page=c.get(url)

    return page

def parser (page):
   soup=bs(page.text,'html.parser')
   return soup

def tagfind(soup,mode):
    try:
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
    except:
        print ('error finding tag,empty page')

def listlinks (tags):
    links=[]
    dup=0

    for tag in tags:
        link=tag.get('href')
        splink=link.split('/')
        if (str.isdigit(splink[-1])) and ((splink)[-2] != 'quickFavForm'):
            if (any(splink[-1] in l for l in downloadedwalls)) and allowduplicates=='False':
               dup=dup+1
            elif (any(splink[-1] in l for l in downloadedwalls)) and allowduplicates=='True':
                dup=dup+1
                links.append(link)
                print('added '+link)
            else:
                links.append(link)
                print('added '+link)
        else:
            pass
    print('found {} duplicated/already existed wallpapers'.format(str(dup)))
    return links


def downloader(link):
    image=''
    
    image=link.get('src')
    image='https:'+image 
    
    spname=image.split('/')
    name=spname[-1]
    
    global newfolder
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
        with open("list.of.downloaded.wall.txt", "a") as myfile: # add the name of the downloaded wallpapers to a txt file to check for duplicates.
            myfile.write(name+'\n') 
        
def openfolder(): # function to open the directory after done downloading, it's optional can be turned off from conf.py.

    try: # open savedir when path is relative.
        if createfolder==str('True').upper:
            print (str(workingpath)+savedir+str(newfolder).replace('/','\\'))
            path='explorer "{}"'.format(str(savedir).replace('/','\\')+str(newfolder).replace('/','\\'))
            subprocess.Popen(path)
        else:
            print (str(workingpath))
            path='explorer "{}"'.format(str(savedir).replace('/','\\'))
            subprocess.Popen(path)
        
    except:       # open savedir when path is absolute.
        try:
            if createfolder==str('True').upper:
                print (workingpath+str(newfolder).replace('/','\\'))
                path='explorer "{}"'.format(workingpath+str(newfolder).replace('/','\\'))
                subprocess.Popen(path) 
            else:
                print (workingpath)
                path='explorer "{}"'.format(workingpath)
                subprocess.Popen(path)
        except:
            print ('Error opening folder or none was downloaded,sorry')

def readDownloadedWalls():
    global downloadedwalls
    try:
        with open('list.of.downloaded.wall.txt', 'r') as f:
         downloadedwalls = [str(str(str(line.strip()).replace('.jpg',"")).replace('.png','')).replace('wallhaven-','') for line in f]
       
        print('Downloaded wallpapers list has been read.',len(downloadedwalls))
    except:
        pass
                            ##############################  Main script  ####################################



readDownloadedWalls()

linksTodownload=[] # a definition of a simple list of all the wallpapers that are planned for downloading (empty at this point).
ss=0
with requests.Session() as c: # running the the whole script under a session to avoid logging in everytime and access all pages quicker.
    
    if dthread>118: # threading is buggy when using more than 118 threads, this will force the script to not exceed 117.
        dthread=117
        print('excedded the maximum number of threads allowed,117')
    if ss<1: #to avoid multiple logging in
        login(1,1)# 1 is just a placeholder, the function will get username and password from conf.py
        
    ss=+1
    for page in range(startpage,startpage+numpages): # looping through the selected pages.
        if mode=='subscription':
            url='https://alpha.wallhaven.cc/subscription?purity=111&page={}'.format(str(page)) #constructing the link for subscription mode.
        elif mode=='search':
            url='https://alpha.wallhaven.cc/search?q={}&={}&purity={}&resolutions={}&ratios={}&topRange={}&sorting={}&order={}&page={}'\
            .format(search,cat,purity,resolution,ratio,toprange,sorting,order,str(page))  #constructing the link for searching mode.
        elif mode=='favorites':
             url='https://alpha.wallhaven.cc/favorites/{}?purity={}&page={}'.format(favTag,purity,str(page))  #constructing the link for favorites mode.
        print('reading page number: '+str(page))
        page=pageget(url)
        parsed=parser(page)

        tagfound=tagfind(parsed,'catalog')
        tolist=listlinks(tagfound)

        #print('Error finding wallpapers,it could be an empty page.')
    
        for link in tolist: # simply making a list of all the links to are planned for downloading.
             if any(link in l for l in linksTodownload):
                 continue
             else:
                linksTodownload.append(link)
    
    
        if len(linksTodownload)==0: # in case there aren't any wallpapers to be downloaded(empty page for example).
                print('nothing to download')
       
    
    print('getting ready to download :'+str(len(linksTodownload))+' new wallpapers')
   

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
    print ("Downloading time was :",time.time()-start) # calculate the time spent downloading wallpapers.
    workingpath = (os.path.dirname(os.path.realpath(__file__))+'\\'+str(savedir).replace('/','\\'))
    if openfolderafter=='True':
        openfolder()
    

