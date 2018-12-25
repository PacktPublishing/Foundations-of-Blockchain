import React, { Component } from 'react';
import crypto from 'crypto';
import Dropzone from 'react-dropzone';
import Web3 from 'web3';
import getWeb3 from "./utils/getWeb3";
import { Button, ProgressBar, ButtonToolbar } from 'react-bootstrap';
import { default as contract } from 'truffle-contract'
import contract_artifacts from './contracts/ProofOfOwnership.json';
import { Line, Circle } from 'rc-progress';


class Main extends Component {
    constructor(props) {
        super(props);
        this.state = {isConnected: false,
                      uploadStatus: 0,
                      hashValue:null,
                      fileOwner: null};


    }
    componentWillMount() {
        if(this.web3 && this.web3.isConnected()) {
            this.setState({isConnected: true});

        }

    }

    async componentDidMount(){
        await this.initWeb3Connection();
        this.poo = contract(contract_artifacts);
        this.poo.setProvider(this.web3.currentProvider);
    }

    async initWeb3Connection() {
        // const web3 = window.web3;
        // Get network provider and web3 instance.
        this.web3 = await getWeb3();

        // Use web3 to get the user's accounts.
        const accounts = await this.web3.eth.getAccounts();
        this.user_address = accounts[0];
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
            this.poo.deployed().then((contractInstance)=>{

                contractInstance.queryAsset(assetID, {gas: 1400000, from: user_address}).then((c)=>{
                    this.setState({fileOwner: c.toLocaleString()})
                });


            });
        } catch (err) {
            console.log(err);
        }
    }

    calculateHash(file){
        this.setState({uploadStatus:25});
        const reader = new FileReader();
        reader.onload = () => {
            const fileAsBinaryString = reader.result;
            const hashValue = crypto.createHash('md5').update(fileAsBinaryString).digest("hex");
            this.setState({hashValue: hashValue,
                           fileOwner: null,
                           uploadStatus:99});

        };
        reader.onabort = () => console.log('file reading was aborted');
        reader.onerror = () => console.log('file reading has failed');

        reader.readAsBinaryString(file[0]);

    }


    render() {
        return (
            <div style={{display: "flex", alignItems: "center",
                justifyContent: "center", flexDirection: "column",
                "padding": 100}}>


                <Dropzone
                    onDrop={this.calculateHash.bind(this)}

                >
                    <p>Try dropping some files here, or click to select files to upload.</p>
                </Dropzone>
                {this.state.uploadStatus > 0 && this.state.uploadStatus < 100?
                    <Line percent={this.state.uploadStatus} strokeWidth="1" style={{margin: "5%", width: "30%"}}/> : null

                }

                {this.state.hashValue ? <div> <b>File hash value</b>: <code>{this.state.hashValue}</code></div> : null

                }
                {this.state.fileOwner ? <div> <b>Current owner</b>: <code>{this.state.fileOwner}</code></div> : null

                }


                <ButtonToolbar  style={{margin: "5%"}}>
                <Button bsStyle="primary" bsSize="large" active
                        disabled={!this.state.hashValue}
                        onClick={(e) => this.registerAsset(Web3.utils.asciiToHex(this.state.hashValue))}>
                    Register file
                </Button>
                    <Button bsStyle="primary" bsSize="large" active
                            disabled={!this.state.hashValue}
                            onClick={(e) => this.queryAsset(Web3.utils.asciiToHex(this.state.hashValue))}>
                        Check owner
                    </Button>
                </ButtonToolbar>






            </div>
    );
    }
}
export default Main;