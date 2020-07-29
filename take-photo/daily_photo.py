import os
from os import path
from datetime import datetime

# this file runs by the sudo crontab for the permissions involving public Apache folder for making the folder
# for the photos/moving the photos into that folder

date_today = datetime.today().strftime('%Y-%m-%d')

# check if directory exists
if (not path.isdir('/home/pi/plant-photos')):
    try:
        os.mkdir('/home/pi/plant-photos', 0o775) # 0o is octal prefix
    except:
        print ("Failed to create plant-photos directory in /home/pi/")
        os._exit(1)

# take picture
os.system('cd /home/pi/plant-photos && raspistill -o ' + date_today + '.jpg -w 1280 -h 960')

# move picture into public folder if it exists and update photo permissions
# this is kind of nasty, should write functions
if (path.isfile('/home/pi/plant-photos/' + date_today + '.jpg')):
    photo_file_path = '/home/pi/plant-photos/' + date_today + '.jpg'
    os.system('chown www-data:pi ' + photo_file_path)
    if (path.isdir('/var/www/html')):
        if (not path.isdir('/var/www/html/plant-photos')):
            try:
                os.mkdir('/var/www/html/plant-photos', 0o775)
                os.system('chown www-data:root /var/www/html/plant-photos')
            except:
                print ("Failed to make public folder /var/www/html/plant-photos")
                os._exit(1)
        
        os.system('mv ' + photo_file_path + ' /var/www/html/plant-photos/' + date_today + '.jpg')
            
    else:
        print ("Please install Apache") # ha

# referenced
# https://stackabuse.com/creating-and-deleting-directories-with-python/
# https://www.guru99.com/python-check-if-file-exists.html
