user='suhail22' 			#login details to access your favorites and NSFW wallpapers
password='sohul2002'
mode='subscription'			# 3 available modes	(subscription,favorites,search) * search is the default mode and it will work without login. subscription and favorites both require login.
favTag=''					# optional,you can leave empty, this can be used if you have multiple collections/favorites and want to download a particular ,for example (https://alpha.wallhaven.cc/favorites/*favTag*). it will 							download the first collection in your favorites list if favTag left empty.
threads='10'				# the number of wallpapers downloaded simultaneously,each wallpaper is a separate downloading thread. depends on connection speed, more=faster :D ,117 is the limit not the sky
sorting='date_added' 			#sorting options(random,toplist,relevance,date_added(latest),views,favorites).
search='kings' 	 			#search ,you can leave empty.
toprange='3M'				# download toplist(if enabled in sorting) for specific period(last day=1d,last 3 days=3d,last week=1w,last month=1M
							#last 3 months =3M,last 6 months=6M, last year=1y).
numpages='4'  	 			#number of pages to download(24 in each page).
startpage='3'				#start downloading from a certain page(none will be downloaded if page does not exist).
order='desc'				#order(desc or asc).
cat='010'				 	#categories (General=100,Anime=010,People=001) you can add them together or enable a single category only.
purity='110'				#purity (SFW=100,Sketchy=010,NSFW=001) *NSFW is not supported.
resolution='1920x1080' 				#specify the resolution(s) needed ,use (,) to specify more resolutions (or leave empty).
ratio=''					# specify ratio(s) ,use (,) to specify more rations (or leave empty),for example (16x9).
createfolder='True'			#save wallpapers in a new folder, use True or False - the folder will be renamed as (Wallpapers-*date and time*) .
savedir='e:/Wallpapers/'	#save directory ,also if createfolder is True,it will create a new folder inside savedir ,directories can be relative (wallpapers/) or absolute(d:/wallpapers/) *the last backslash is required.
							#leave empty to create the folder in the same directory.
allowduplicates='False'		# Allow the script to download duplicated wallpapers that are already has been downloaded, Check list.of.downloaded.wall.txt .
openfolderafter='True'		# open directory after done downloading wallpapers.