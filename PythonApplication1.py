import requests
from bs4 import BeautifulSoup as bs
from lxml import html

def pageget (url):
    lo=login().session_requests
    
    
    page=lo.get(url,headers = dict(referer = url))

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
def login(
    ):
    payload = {
	"username": "suhail22", 
	"password": "sohul22", 
	"_token": "<CSRF_TOKEN>"
    }
    session_requests = requests.session()
    login_url = "https://alpha.wallhaven.cc/auth/login"
    result = session_requests.get(login_url)

    tree = html.fromstring(result.text)
    authenticity_token = list(set(tree.xpath("//input[@name='_token']/@value")))[0]
    print(authenticity_token)
    result = session_requests.post(
	login_url, 
	data = payload, 
	headers = dict(referer=login_url)
    )
    
######Main script######
login()
numberofpages=5
linksTodownload=[]
searchfor='breaking bad'.replace(' ','+')
for run in range(1,numberofpages+1):
    url='https://alpha.wallhaven.cc/search?q=&categories=111&purity=001&sorting=random&order=desc&page='+str(run)
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
for single in linksTodownload:
        try:
            page=pageget(single)
            parsed=parser(page)
            tagfound=tagfind(parsed,'img')
     #       print('found image url,ready to Download')
            downloader(tagfound)
        except:
            print('invalid URL ')
print('done downloading page '+str(run))
    