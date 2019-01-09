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


## Docker compose installation:

### Mac:

Docker for Mac already includes Compose along with other Docker apps. Mac users need not install this separately.

### Windows:

Docker for Windows already includes Compose along with other Docker apps. Windows users need not install this separately.

### Ubuntu/ other Linux platforms

* Download the latest version of Docker Compose:

    ```
    sudo curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

* Provide permissions to the executables:
    ```
    sudo chmod +x /usr/local/bin/docker-compose

    ``` 
* Create a symbolic link:
    ```
    sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

    ```
 




