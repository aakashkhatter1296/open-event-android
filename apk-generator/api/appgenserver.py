#! /usr/bin/env python
import os
import re
import json,sys
from firebase import firebase
import requests
from tempfile import mkstemp
import subprocess
from tempfile import mkstemp
from shutil import move
from os import remove, close
import zipfile
from shutil import copyfile

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

email = sys.argv[1]
# Path to be created
directory = "/var/www/html/api/files/"+str(email)
print directory
if not os.path.exists(directory):
    os.makedirs(directory)


app_name = sys.argv[2]
app_name = re.sub(r'[^a-zA-Z0-9]', ' ', app_name)
print app_name
print email


print directory

jsonData = " { \n"+'"Email"'+": " + '"' + sys.argv[1] + '",\n'+'"App_Name"'+": "+'"' +sys.argv[2]+'",\n'+'"Api_Link"'+": " + '"' + sys.argv[3] + '"\n }'

subprocess.call(['/var/www/html/clone.sh', directory])
# subprocess.call(['/var/www/html/setPerm.sh', directory])
with open(directory+"/open-event-android/android/app/src/main/assets/config.json", "wb") as fo:
    fo.write(jsonData)

absDirectory = directory + "/open-event-android/android/"
# subprocess.call(['./setPerm.sh', directory])
replace(directory+"/open-event-android/android/app/build.gradle", '"org.fossasia.openevent"', '"org.fossasia.openevent.'+app_name.split()[0]+'"')
replace(directory+"/open-event-android/android/app/src/main/res/values/strings.xml", 'OpenEvent', app_name)

#TODO: Add zip path
#zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
#zip_ref.extractall(directory)
#zip_ref.close()
#TODO: Change path here
#for f in os.listdir(directory+ "/zip"):
#	if f.endswith('.json'):
#		copyfile(f, directoy + "open-event-android/android/app/src/main/assets/"+f)
#	elif f.endswith('.png'):
#		copyfile(f, directory + "open-event-android/android/app/src/main/res/drawable"+f)
#replace(directory+"/open-event-android/android/app/src/main/res/values/strings.xml", 'mipmap/ic_launcher', 'drawable/' + f)
subprocess.call(['/var/www/html/buildApk.sh', directory])
subprocess.call(['/var/www/html/email.sh', directory, email])
#subprocess.call(['/var/www/html/copyApk.sh', absDirectory])
subprocess.call(['/var/www/html/api/delete.sh', email])
print "Script End"
