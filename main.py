import time
import threading
import subprocess
import os


#Run mongodb
def mongo_runner():
    subprocess.Popen([r'E:\MongoDB\Server\5.0\bin\mongod.exe', '--dbpath=c:\data\db'], stdout=subprocess.DEVNULL)

#Scrape_main.py every 5 minutes
def data_thread():
    scrape_file = os.path.join(os.path.dirname(__file__), 'scrape_main.py')
    while True:
        subprocess.run(['py', '-3.9', scrape_file])
        time.sleep(5*60)

#Lastly, run flask
def flask_runner():
    os.chdir(os.path.join(os.path.dirname(__file__), 'webserver'))
    subprocess.Popen(['waitress-serve', '--listen=127.0.0.1:5000', 'app:flask_client'])


threading.Thread(target=mongo_runner).start()
threading.Thread(target=data_thread).start()
threading.Thread(target=flask_runner).start()
