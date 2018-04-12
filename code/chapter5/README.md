# Chapter 4

Scripts present here could be used to create and deploy web server to create a REST API.
 Full project with front end integration could be found [here](https://github.com/koshikraj/proof-of-existence).

## Quick Start

- Install dependencies

   `pip install -r requirements.txt`

- Start python webserver

   `python poe_server.py`
   

### HTTP API
##### Publish document
```
curl -X POST -F 'name=user' -F 'email=test@test.com1' -F 'message=some message' -F 'digest=86abfbd5f1a9e928935cdee9b2fd1bc2d43254b40d996e262026e9d668555613' http://localhost:8000/publish 
```

##### Verify document
```
curl http://localhost:8000/verify?digest=86abfbd5f1a9e928935cdee9b2fd1bc2d43254b40d996e262026e9d668555613
``` 

##### Fetch latest document info
```
curl http://localhost:8000/details?count=3
```
