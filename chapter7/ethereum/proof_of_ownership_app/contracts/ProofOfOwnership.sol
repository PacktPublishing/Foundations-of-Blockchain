pragma solidity ^0.4.23;

contract ProofOfOwnership {

    mapping (bytes32 => address) public assetOwners;

    function queryAsset(bytes32 asset) view public returns (address) {

        return assetOwners[asset];
  }

    function registerAsset(bytes32 asset) public {

            assetOwners[asset] = msg.sender;

  }

    function transferAsset(bytes32 asset, address owner) public {

        if (assetOwners[asset] == msg.sender)
        {
            assetOwners[asset] = owner;
        }
    }

    function deleteAsset(bytes32 asset) public {

        if (assetOwners[asset] == msg.sender)
        {
            assetOwners[asset] = 0x0000000000000000000000000000000000000000;
        }
    }


}

