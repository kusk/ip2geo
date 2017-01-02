import geoip2.database
import sys
import re
import socket
import os
import magic

try:
	if sys.argv[1]:
		print("Working...")
except:
	print('ip2country.py - [path to parse] - [csv output]')
	exit()

c = 0

reader = geoip2.database.Reader('GeoLite2-Country.mmdb')
response = reader.country('80.62.117.136')
rootdir = sys.argv[1]
save = open(sys.argv[2], 'a')
save.write('IP;Country;File;Line;'+"\n")
for dirName, subdirList, fileList in os.walk(rootdir):
	for fname in fileList:
		if "text" in magic.from_file(dirName+'/'+fname):
			f = open(dirName+'/'+fname, 'r')
			try:
				for l in f.readlines():
					ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', l)
					for i in ip:
						try:
							socket.inet_aton(i)
							r = reader.country(i)
							if len(l) < 300:
								save.write(i+';'+r.country.name+';'+dirName+'/'+fname+';'+l)
								c = c + 1
						except:
							pass
			except:
				pass
			f.close()
save.close()
print('Done!')
print(str(c) +' lines added to '+sys.argv[2])
