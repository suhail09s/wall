import requests
from bs4 import BeautifulSoup as bs
import threading

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
    
    try:
        open(name,'r')
        print('checking :'+name)
        
        
    except:
        r = requests.get(image, allow_redirects=True)
        open(name, 'wb').write(r.content)
        print(name+' has been downloaded')
        #print('failed to download '+name)
######Main script######

numberofpages=10
linksTodownload=[]
threads = []
searchfor='joker'.replace(' ','+')
for run in range(1,numberofpages+1):
    #url='https://alpha.wallhaven.cc/search?q={}&categories=111&purity=110&sorting=random&order=desc&page={}'.format(searchfor,str(run))
    url='https://alpha.wallhaven.cc/random?page={}'.format(str(run)) #url for random page
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
        

    #print(len(linksTodownload))
   # imgDownloader(linksTodownload)
i=1
for single in linksTodownload:
        try:
            
            t = threading.Thread(target=worker,args=(single,i,))
            threads.append(t)
            t.setDaemon(False)
            t.start()
            
            i=i+1
            
        except:
            print('invalid URL ')
t.join()
print('#'*25)

print('done downloading page '+str(run))
print(threading.enumerate())