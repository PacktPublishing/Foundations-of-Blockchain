import React, { Component } from 'react';
import Web3 from 'web3';
import { default as contract } from 'truffle-contract'
import contract_artifacts from './contracts/ProofOfOwnership.json'
class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {isConnected: false};


    }
    componentWillMount() {
        if(this.web3 && this.web3.isConnected()) {
            this.setState({isConnected: true});

        }

    }

    componentDidMount(){
        this.initWeb3Connection();
        this.poo = contract(contract_artifacts);
        this.poo.setProvider(this.web3.currentProvider);
    }

    initWeb3Connection()
    {
        const web3 = window.web3;
        if (typeof web3 !== 'undefined') {
            // Use Mist/MetaMask's provider

            this.web3 = new Web3(web3.currentProvider);
            this.user_address = this.web3.eth.accounts[0]

        } else {
            console.log('No web3? You should consider trying MetaMask!')
            // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
            this.web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
        }
    }


    registerAsset(assetID)
    {

        try {
            let user_address = this.user_address;
            this.poo.deployed().then(function(contractInstance) {

                contractInstance.registerAsset(assetID, {gas: 1400000, from: user_address}).then(function(c) {
                    console.log(c.toLocaleString());
                });
            });
        }

        catch (err) {
            console.log(err);
        }

    }


    queryAsset(assetID)
    {


        try {
            let user_address = this.user_address;
            this.poo.deployed().then(function(contractInstance) {

                contractInstance.queryAsset(assetID, {gas: 1400000, from: user_address}).then(function(c) {
                    console.log(c.toLocaleString());
                });


            });
        } catch (err) {
            console.log(err);
        }
    }


    render() {
        return (
            <div>


                <button onClick={(e) => this.registerAsset("123")}> Register  </button>

                <button onClick={(e) => this.queryAsset("123")}> Query </button>



    </div>
    );
    }
}
export default Main;