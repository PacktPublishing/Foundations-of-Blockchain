# Crowdfunding


## Quick start

* Clone the neo-python [ICO template](https://github.com/neonexchange/neo-ico-template) (https://github.com/neonexchange/neo-ico-template)

* Setup a neo private blockchain network. Navigate to the root of the project and launch the neo-python shell.

    `np-prompt -p [private-network-node]`
    

* Open the default wallet that is loaded with NEO and GAS.

  `open wallet neo-privnet.sample.wallet` (password: coz)
    
    
* Configure the token details in `nex/toke.py` file (We have named coin name as PCKT). Build and deploy the ICO smart contract.

    ```
    build ico_template.py test 0710 05 True False name [] 
       
         
    import contract ico_template.avm 0710 05 True False

    ```

* Initiate the ICO by calling deploy method. Replace the hash value with the hash value returned by your import command.

    `testinvoke 0xce4a9966dfd3c7c02b48646a6aac281e4c914c2d deploy []` 
    
* Check the total supply and circulation of the tokens.

    ```
        testinvoke 0xce4a9966dfd3c7c02b48646a6aac281e4c914c2d circulation []
        
        testinvoke 0xce4a9966dfd3c7c02b48646a6aac281e4c914c2d totalSupply []

    ```
    
* Register a crowdsale participant.

    `testinvoke 0xce4a9966dfd3c7c02b48646a6aac281e4c914c2d crowdsale_register ["AXoZMHm7bxCF5oCkudRjJerJy5AvuRDxp2"]`
    
* The registered participant can open the wallet and mint new tokens.

    `testinvoke 0xce4a9966dfd3c7c02b48646a6aac281e4c914c2d mintTokens --attach-neo=50`
    
* The participant needs to import the token inorder view the new tokens in the wallet.

    `import token 0xce4a9966dfd3c7c02b48646a6aac281e4c914c2d `
    
* The `wallet` command will show the newly added tokens.

    ```
    Wallet { 
    
        "addresses": [ 
    
            { 
    
                ... 
    
                "balances": { 
    
                    "0xc56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b": "99993495.0", 
    
                    "0x602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7": "14033.9996" 
    
                }, 
    
                "tokens": [ 
    
                    "[ce4a9966dfd3c7c02b48646a6aac281e4c914c2d] PCKT : 2000.00000000" 
    
                ] 
    
            } 
    
        ], 
    
        ... 
    
        "synced_balances": [ 
    
            "[NEO]: 99993495.0 ", 
    
            "[NEOGas]: 14033.9996 ", 
    
            "[PCKT]: 2000 " 
    
        ], 
    
    … } 
    ``` 
    
  


