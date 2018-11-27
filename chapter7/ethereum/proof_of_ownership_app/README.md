# Proof of Ownership DApp

We have created the Proof of Ownership DApp using [`react`](https://truffleframework.com/boxes/react) truffle box.


## Executing the Proof of Ownership DApp 

The Proof of Ownership app contains:

* The contract logic in `contract/ProofOfOwnership.sol`

* The frontend logic in  `client/src/Main.js`


### Quick start


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
  
  * Execute the command inside the console to invoke the contract:
  
       ```          
       truffle(development)>  
       
       ProofOfOwnership.deployed().then((instance)=>instance.registerAsset("c9f50a3bdd2efccb7e34fbd8b42e9675", {from: "0xebe41ec4c574fde7a1d13d333d17267ca93df491"}));
       
       ```
  * This will register the asset with the id: `c9f50a3bdd2efccb7e34fbd8b42e9675`
  
* The frontend react app can be launched with npm:

    `npm start`
