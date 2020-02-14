# Customized Search Engine for Darknet Analysis
## Kerala Police Cyberdome
## Ramachandran A




## Packages required

PySocks
pika
Werkzeug
Flask
xlrd
elasticsearch
BeautifulSoup
pymongo


## Dependencies

Linux
Python 3.x
pip3
Tor CLI
Elasticsearch
Mongodb

[Note: Install these packages seperately. They are not included in requirements.txt]

### Install the packages ###

    sudo pip3 install -r install requirements.txt
    
### Start the services ###
    
    
    sudo service mongod start
    
    sudo service elasticsearch start
    
    sudo service tor start
    
    
### Execute the program ###

    sudo python3 tor.py
    
    sudo python3 elas.py



