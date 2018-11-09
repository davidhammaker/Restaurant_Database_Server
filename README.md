# Restaurant Database Server
A practice repository for "Servers, Authorization, and CRUD"

## Purpose
This repository contains many resources and practice files that follow Udacity's "Servers, Authorizatin, and CRUD" course. Many files in this repository work well as template files for working with databases. The course originally employed Python 2 for its server file, but this repository includes a server file that has been ported to Python 3.

## Dependencies
These files are being used from within a Linux virtual machine. To install a virtual machine on your computer, you will need access to a shell prompt (E.g. [Git Bash](https://git-scm.com/downloads) for Windows). You will also need to download [VirtualBox](https://www.virtualbox.org/) and [Vagrant](https://www.vagrantup.com/downloads.html). Once you have access to a shell prompt and have downloaded Vagrant and VirtualBox, create a new directory and install the virtual machine by running the following commands inside any directory of your choice:
```
$ mkdir [NAME-OF-YOUR-NEW-DIRECTORY]
$ vagrant init ubuntu/trusty64
$ vagrant up
```
To log into the virtual machine, run `$ vagrant ssh`. You may need to update the machine. Do this by running:
```
$ sudo apt-get update && sudo apt-get upgrade
```
Once your virtual machine is running and updated, you can clone this repository. Log out of the virtual machine with `$ exit` and run:
```
$ git clone https://github.com/davidhammaker/Restaurant_Database_Server.git
```

## Usage
After you have cloned the repository, you can log back into the virtual machine with `$ vagrant ssh`. From there, you should be able to run the server with `$ python3 webserver.py`.

* If you experience any errors, check that you have SQLAlchemy installed. Running `$ pip3 install SQLAlchemy` will either install the module or inform you that the module is already installed. (If `$ pip3` fails, you may need to install that, too. Try `$ sudo apt-get install pip3`, and then proceed to `$ pip3 install SQLAlchemy`.)

Once the server is up and running (your shell should say `Web server running on port 8080`), you can access the webpage by typing `localhost:8080/restaurants` into your web browser.

## Work-in-progress
I am still continuing my work on this course, so this repository is not yet complete. Check back for updates.
