# BrewBox
Brewbox is an open source cocktail maker. Written with a python backend and scaleability in mind.

##Requirements
- Apache 2
- MariaDB
- Flask-CORS
- Flask-socketio
- gevents
- gevents-webserver

To get started simply make following scheme:

![Fritzing scheme](https://raw.githubusercontent.com/howest-mct/2020-2021-projectone-GordonCedric/master/Finals/1%20Frizing%20schema/Fritzing_schem.png?token=AOQQA3W6T4S36F7UP5BROWDA2CRM6 "Fritzing scheme")

Now that you have build the circuit, we have to set some things up first.  

Since we are going to be running everything on the Raspberry Pi, we need to set up the dependencies, etc...

### Pi setup:

So, to install these packages we first have to do a global update/upgrade.  

To do this, you have to run following commands:

    sudo apt update
    sudo apt upgrade

So now that that's updated, we will also have to enable the correct interfaces, to do this, just run:

    sudo raspi-config 

This will open a new window, here you navigate to Interfaces and enable 1-wire and I2C.

With the interfaces enabled, we can proceed to install Apache2, to do this simply run:

    sudo apt install apache2 -y

When Apache2 is installed, you can do the same for our MariaDB:

    apt install mariadb-server mariadb-client -y

It will ask you to do the secure install, simply follow the steps on screen to set everything up.  

Make sure you remember your credentials since you will need them to set up the database.

Now that your MariaDB is set up, it's time to clone the github repository.  

You can do this by simply typing:

    git clone https://github.com/GordonCedric/BrewBox

This will clone the entire project on your Pi.  

The last step needed for the environment is telling apache2 where the frontend will be.

Simply go to /etc/apache2/sites-available and edit the 000-default.conf file.  

On the line DocumentRoot, fill in the path where you cloned the github directory and in that directory you navigate to Code/Frontend  

This will make the website always show up when the Pi boots.

### Pip Packages:

Now that our Pi is all ready to use, we also need some packages for Python.  

These can be easily installed by using following commands:

    pip3 install flask-cors  
    pip3 install flask-socketio  
    pip3 install mysql-connector-python  
    pip3 install gevent  
    pip3 install gevent-websocket

After this, you can easily upload the database which is located in:

*Code/Database-export/database.sql*

Now you can go to Code/Backend/config.py and setup the database connection.

When this is done, you can start the app.py and it should be running without any issues.

> I want to run it as a service and not manually

No problem!  I have included the file to run it as a service in Code/brewbox.service.

To do this, you can just use following command:

    sudo cp brewbox.service /etc/systemd/system/brewbox.service

After that you need to test that it's **actually** working as a service.

So to test this, we start the service manually using:

	sudo systemctl start brewbox.service

If this boots without an issue, we can stop the service and enable it:

	sudo systemctl stop brewbox.service
	sudo systemctl enable brewbox.service