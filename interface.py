import os
from importlib import reload
from flask import Flask, request
from flask import render_template,redirect,url_for,jsonify
from flask import flash, make_response
import conf
import json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import wallhavenDownloader
app=Flask(__name__)



app.secret_key = 'ss'
class Edit(FlaskForm):
    user = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Update')

def writetofile(dic):
    
    confString=(f"""user='{dic["user"]}' 			#login details to access your favorites and NSFW wallpapers
password='{dic["password"]}'
mode='{dic["mode"]}'			# 3 available modes	(subscription,favorites,search) * search is the default mode and it will work without login. subscription and favorites both require login.
favTag='{dic["favTag"]}'					# optional,you can leave empty, this can be used if you have multiple collections/favorites and want to download a particular ,for example (https://alpha.wallhaven.cc/favorites/*favTag*). it will 							download the first collection in your favorites list if favTag left empty.
threads='{dic["threads"]}'				# the number of wallpapers downloaded simultaneously,each wallpaper is a separate downloading thread. depends on connection speed, more=faster :D ,117 is the limit not the sky
sorting='{dic["sorting"]}' 			#sorting options(random,toplist,relevance,date_added(latest),views,favorites).
search='{dic["search"]}' 	 			#search ,you can leave empty.
toprange='{dic["toprange"]}'				# download toplist(if enabled in sorting) for specific period(last day=1d,last 3 days=3d,last week=1w,last month=1M
							#last 3 months =3M,last 6 months=6M, last year=1y).
numpages='{dic["numpages"]}'  	 			#number of pages to download(24 in each page).
startpage='{dic["startpage"]}'				#start downloading from a certain page(none will be downloaded if page does not exist).
order='{dic["order"]}'				#order(desc or asc).
cat='{dic["cat"]}'				 	#categories (General=100,Anime=010,People=001) you can add them together or enable a single category only.
purity='{dic["purity"]}'				#purity (SFW=100,Sketchy=010,NSFW=001) *NSFW is not supported.
resolution='{dic["resolution"]}' 				#specify the resolution(s) needed ,use (,) to specify more resolutions (or leave empty).
ratio='{dic["ratio"]}'					# specify ratio(s) ,use (,) to specify more rations (or leave empty),for example (16x9).
createfolder='{dic["createfolder"]}'			#save wallpapers in a new folder, use True or False - the folder will be renamed as (Wallpapers-*date and time*) .
savedir='{dic["savedir"]}'	#save directory ,also if createfolder is True,it will create a new folder inside savedir ,directories can be relative (wallpapers/) or absolute(d:/wallpapers/) *the last backslash is required.
							#leave empty to create the folder in the same directory.
allowduplicates='{dic["allowduplicates"]}'		# Allow the script to download duplicated wallpapers that are already has been downloaded, Check list.of.downloaded.wall.txt .
openfolderafter='{dic["openfolderafter"]}'		# open directory after done downloading wallpapers.""")

    with open('conf.py','w') as file:
        file.write(confString)
        file.close()

@app.route('/edit',methods=['GET','POST'])
def edit():
    return jsonify({'page':'1'})
@app.route('/',methods=['GET','POST'])
def frontPage():
    dic={}
    reloadconf()    
    for item in dir(conf):
        if item.startswith("__"):
            continue
        
        d=f'conf.{item}'
        
        dic[item]=eval(d)
    
    c=json.dumps(dic)
    loaded_c=json.loads(c)
    form=Edit()
    if form.validate_on_submit():
        con=json.dumps(request.form)
        
        loaded_d=json.loads(con)
        loaded_d.pop('csrf_token')
        loaded_d.pop('submit')
        writetofile(loaded_d)
        print ('update conf.py')
            
        return render_template('front.html',loaded_c=loaded_d,form=form)
    return render_template('front.html',loaded_c=loaded_c,form=form)

@app.route('/run')
def rundownloader():
    wallhavenDownloader.main()
    return ('will init downloader')
def reloadconf():
    reload(conf)


if __name__=='__main__':

    host=os.getenv('IP','0.0.0.0')
    port= int(os.getenv('PORT',8085))
    app.debug=True
    app.secret_key = 'ss'

   



    app.run(host=host,port=port)