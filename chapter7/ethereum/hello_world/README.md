
# Hello World smart contract

* Initialize an sample contract project

    * Execute: `truffle init`
    
    * Add the following setting to the truffle.js, so that we can communicate with the local blockchain node.
   
        ```
        module.exports = { 
          networks: { 
            development: { 
              host: '127.0.0.1', 
              port: 8545, 
              network_id: '*' } 
          } 
        };
        
        ```

* Compile and deploy the contract  

  * Execute: `truffle compile`
   
  * Execute: `truffle migrate`
  
* Invoking the contract through truffle console
   
  * Execute: `truffle console`
  
  * Execute the command inside the console:
  
       ```          
       truffle(development)>  
       
       Hello.deployed().then((instance) => instance.greetUser("Alice"));
       
       ```
  * This will return a response "Hello Alice" in the hexa decimal format.
