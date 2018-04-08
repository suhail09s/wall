login =dict(login='suhail',password='pass')# not working YET
threads='5'					# the number of wallpapers downloaded simultaneously,each wallpaper is a separate downloading thread. depends on connection speed, more=faster :D 
sorting='date_added' 			 #sorting options(random,toplist,relevance,date_added,views,favorites)
search='' 	 				#search ,you can leave empty.
toprange='1y'				# download toplist(if enabled in sorting) for specific period(last day=1d,last 3 days=3d,last week=1w,last month=1M
							#last 3 months =3M,last 6 months=6M, last year=1y)
numpages='1'  	 			#number of pages to download(24 in each page).
startpage='10'				#start downloading from a certain page(none will be downloaded if page does not exist)
order='asc'				 #order(desc or asc).
cat='100'				 	#categories (General=100,Anime=010,People=001) you can add them together or enable a single category only
purity='100'				 #purity (SFW=100,Sketchy=010,NSFW=001) *NSFW is not supported.
resolution='' #specify the resolution(s) needed ,use (,) to specify more resolutions (or leave empty).
ratio=''						# specify ratio(s) ,use (,) to specify more rations (or leave empty),for example (16x9)
createfolder='False'				#save wallpapers in a new folder, use True or False - the folder will be renamed as (Wallpapers-*date and time*) 
savedir='Wallpapers/'				#save directory ,also if createfolder is True,it will create a new folder inside savedir ,directories can be relative (wallpapers/) or absolute(d:/wallpapers/) *the last backslash is required.
							#leave empty to create the folder in the same directory.