# search_engine_darknet is the project developed by Ramachandran A for Kerala Police Cyberdome for Darknet Monitoring and Analysis.
# requires python3 .....  pip3
# required packages and dependencies .... mongodb,tor,elasticsearch,flask
# runs on linux




######################## Usage #############################

    sudo pip3 install -r install requirements.txt
    
    
    xargs -rxa dependencies.txt -- sudo apt-get install --
    
    
    
    
    clone the repository and save in the directory /usr/bin
    
    
    sudo service mongod start
    
    sudo service elasticsearch start
    
    sudo service tor start
    
    sudo python3 tor.py
    
    sudo python3 elas.py



