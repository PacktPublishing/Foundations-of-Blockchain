# Docker Engine and Docker compose: 

Most of the setup and execution steps mentioned in the book in performed on Linux machine (Ubuntu 16.04.5 LTS). Although similar steps
can be reproduced on Mac OS and Windows based systems, you can alternatively use Linux bases docker container to run all the commands as it is.

Few applications in this book needs [docker compose](https://docs.docker.com/compose). 

## Docker CE installtion:

Following set of commands installs latest stable version of of docker CE along with all the dependencies: 

### Ubuntu:

``` 
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common 

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - 

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" 

sudo apt-get update 

sudo apt-get install docker-ce
```

### Mac:

Docker CE for Mac can be downloaded from 
https://store.docker.com/editions/community/docker-ce-desktop-mac.

Use the downloaded dmg file to install the docker.

This installation includes  Docker Engine, Docker CLI client, Docker Compose, Docker Machine, and Kitematic.

### Windows:

Docker CE fro Windows can be downloaded from 
https://store.docker.com/editions/community/docker-ce-desktop-windows.

Run the downloaded exe file.

### Quick start

## Docker compose installtion:

### Ubuntu:




