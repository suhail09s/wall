import requests
from bs4 import BeautifulSoup as bs
import threading
import time
import datetime
import conf
import os
#def confread():# reads a config file attached (conf.py) with the main .py for a castomizable downloader 
search=str(conf.search).replace(' ','+') # replace space with plus to mkae the url
cat=conf.cat
purity=conf.purity
sorting=conf.sorting
order=conf.order
toprange=conf.toprange
ratio=str(conf.ratio).replace(',','%2C')
resolution=str(conf.resolution).replace(',','%2C')
numpages=int((conf.numpages))
savedir=conf.savedir
createfolder=str(conf.createfolder).upper
print('all configrations has been read')
gettime=datetime.datetime.today()
foldertime='{:%d-%m_%H-%M-%S}'.format(gettime)
print(gettime)
def worker (single,i):
    #print('thread number {} started'.format(str(i)))
    page=pageget(single)
    
    parsed=parser(page)
    tagfound=tagfind(parsed,'img')

    #print('Thread-found image url,ready to Download')
    downloader(tagfound)
    
    return exit()

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
       # print(tag1)
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
def imgDownloader(links):
    url = links
    for single in links:
        spname=single.split('/')
        name=spname[-1]
        if str.isdigit(name):
            imgUrl='https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-'+name+'.jpg'
            try:
                 
                r = requests.get(imgUrl, allow_redirects=True)
                open(name+'.jpg', 'wb').write(r.content)
                print(name+'.jpg has been downloaded')
            except:
                print('failed to download'+name)
    return None

def downloader(link):
    image=link.get('src')
    image='https:'+image
    #print(image)
    spname=image.split('/')
    name=spname[-1]
    newfolder=''# to avoid creating a new folder if createfolder in conf.py = False
    if createfolder==str('True').upper:
        newfolder='wallpapers-{}/'.format(foldertime)
        if not os.path.exists(savedir+newfolder):
            os.makedirs(savedir+newfolder)
    try:
        open(savedir+newfolder+'/'+name,'r')
        print(name+' is already exist.')
        
        
    except:
        r = requests.get(image, allow_redirects=True)
        open(savedir+newfolder+name, 'wb').write(r.content)
        print(name+' has been downloaded\n')
        #print('failed to download '+name)
######Main script######


linksTodownload=[]
threads = []

for page in range(1,numpages+1):
    
    url='https://alpha.wallhaven.cc/search?q={}&categories={}&purity={}&resolutions={}&ratios={}&topRange={}&sorting={}&order={}&page={}'\
            .format(search,cat,purity,resolution,ratio,toprange,sorting,order,str(page))   
    print(url)
    page=pageget(url)
    parsed=parser(page)
    #print(parsed)
    tagfound=tagfind(parsed,'catalog')
    #print(tagfound)
    tolist=listlinks(tagfound)
    #print(tolist)
    #print(len(tolist))
    
    for list in tolist:
        linksTodownload.append(list)
        

    
print('getting ready to download :'+str(len(linksTodownload))+' wallpapers')
        # imgDownloader(linksTodownload)
i=1
print('downloading...')
for single in linksTodownload:
        try:
            
            t = threading.Thread(target=worker,args=(single,i,))
            threads.append(t)
            t.setDaemon(True)
            t.start()
            
            i=i+1
            
        except:
            print('invalid URL ')
t.join()
print('#'*25)
time.sleep(1)

print('done downloading page '+str(page))
print(threading.enumerate())

