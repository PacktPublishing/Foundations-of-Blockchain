import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Neon, {rpc} from '@cityofzion/neon-js'
// import {encode, decode} from 'base-64';
// base58 = require("ba se-58");
import {encode, decode} from 'base-58';
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

console.log('1234'.hexEncode());

class App extends Component {

    getAssetOwner() {
        const props = {
            scriptHash: '60a7ed582c6885addf1f9bec7e413d01abe54f1a',
            operation: 'query',
            args: ['f572f8ce40bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3'.hexEncode(),
                ''
            ]
        };


        const Script = Neon.create.script(props);

        rpc.Query.invokeScript(Script).execute('http://139.59.65.33:30333').then((res) => {

            this.setState({owner: scripthash_to_address(res.result.stack[0].value)});
        });

    }

    constructor(props) {
        super(props);
        this.state = {owner: ''};
        this.getAssetOwner();

    }

  render() {
    return (
      <div className="PooApp">
          Hello: {this.state.owner}

      </div>
    );
  }
}

export default App;
