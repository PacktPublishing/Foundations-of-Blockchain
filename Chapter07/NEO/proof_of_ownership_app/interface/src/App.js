import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Neon, {rpc, wallet, api, sc} from '@cityofzion/neon-js'
import {encode, decode} from 'base-58';
import crypto from 'crypto';
import Dropzone from 'react-dropzone';
import { Button, ProgressBar, ButtonToolbar } from 'react-bootstrap';
import { Line, Circle } from 'rc-progress';
import hexEncoding from 'crypto-js/enc-hex';
import SHA256 from 'crypto-js/sha256';

const ADDR_VERSION = '17';

function hash256(hex) {
    if (typeof hex !== 'string') throw new Error('reverseHex expects a string');
    if (hex.
            length % 2 !== 0) throw new Error('Incorrect Length:');
    var hexEncoded = hexEncoding.parse(hex);
    var ProgramSha256 = SHA256(hexEncoded);
    return SHA256(ProgramSha256).toString()
}

function reverseHex(hex) {

    var out = ''
    for (var i = hex.length - 2; i >= 0; i -= 2) {
        out += hex.substr(i, 2)
    }
    return out
}

function scripthash_to_address(scriptHash)
{

    // scriptHash = reverseHex(scriptHash)
    const shaChecksum = hash256(ADDR_VERSION + scriptHash).substr(0, 8);
    return encode(Buffer.from(ADDR_VERSION + scriptHash + shaChecksum, 'hex'))
}
String.prototype.hexEncode = function(){
    let hex, i;

    let result = "";
    for (i=0; i<this.length; i++) {
        hex = this.charCodeAt(i).toString(16);
        result += (hex).slice(-4);
    }

    return result
};

String.prototype.hexDecode = function(){
    let j;
    let hexes = this.match(/.{1,2}/g) || [];
    let back = "";
    for(j = 0; j<hexes.length; j++) {
        back += String.fromCharCode(parseInt(hexes[j], 16));
    }

    return back;
};


class App extends Component {



    constructor(props) {
        super(props);
        this.state = {isConnected: false,
            uploadStatus: 0,
            hashValue:null,
            fileOwner: null};



    }

    registerAsset(assetID)
    {

        try {
            let account = new wallet.Account('KxDgvEKzgSBPPfuVfw67oPQBSjidEiqTHURKSDL1R7yGaGYAeYnr');

            let intents = [{

                assetId: Neon.CONST.ASSET_ID.GAS,

                value: new Neon.u.Fixed8(1),  // I gueesed this :)

                scriptHash: '60a7ed582c6885addf1f9bec7e413d01abe54f1a'

            }];

            // the interesting part: what do we want to do :)

            let invoke = {

                scriptHash: '60a7ed582c6885addf1f9bec7e413d01abe54f1a',

                operation: 'register',

                args: [

                    'asdsd'.hexEncode(),
                    'AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y'.hexEncode()

                ]

            }

            let sb = Neon.create.scriptBuilder();

            sb.emitAppCall(invoke.scriptHash, invoke.operation, invoke.args, false);
            let script = sb.str;
            let unsignedTx = Neon.create.invocationTx();


            let signedTx = unsignedTx.addIntent(intents).sign(account.privateKey);
            console.log(signedTx)

            // send the transaction to our net

            rpc.queryRPC('http://139.59.25.30:30333', {

                method: 'sendrawtransaction',

                params: [signedTx],

                id: 1

            }); // here we could listen to the response with then/catch

        }

        catch (err) {
            console.log(err);
        }

    }

    async componentDidMount(){

        const mainNetNeoscan = new api.neoscan.instance("TestNet");
        const neoscanBalance = await mainNetNeoscan.getBalance('AH4dqfuyaT1tGthQiQQ2RQ8c7Xksuphb7k');
        console.log(neoscanBalance)

    }


    queryAsset(assetID) {


        console.log(assetID.hexEncode());
        try {
            const props = {
                scriptHash: '60a7ed582c6885addf1f9bec7e413d01abe54f1a',
                operation: 'query',
                args: [assetID.hexEncode(),
                    ''
                ]
            };


            const Script = Neon.create.script(props);

            rpc.Query.invokeScript(Script).execute('http://139.59.25.30:30333').then((res) => {

                this.setState({fileOwner: scripthash_to_address(res.result.stack[0].value)});
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
            const hashValue = crypto.createHash('sha256').update(fileAsBinaryString).digest("hex");
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
                            onClick={(e) => this.registerAsset(this.state.hashValue)}
                        >
                        Register file
                    </Button>
                    <Button bsStyle="primary" bsSize="large" active
                            disabled={!this.state.hashValue}
                            onClick={(e) => this.queryAsset(this.state.hashValue)}>
                        Check owner
                    </Button>
                </ButtonToolbar>






            </div>
        );
    }
}

export default App;
