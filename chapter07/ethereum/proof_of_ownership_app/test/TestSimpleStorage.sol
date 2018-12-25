pragma solidity ^0.4.24;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";
import "../contracts/SimpleStorage.sol";
import "../contracts/ProofOfOwnership.sol";

contract TestSimpleStorage {

  function testItStoresAValue() public {
    ProofOfOwnership owner = ProofOfOwnership(DeployedAddresses.ProofOfOwnership());

    owner.registerAsset("testasset");


    Assert.equal(address(owner.queryAsset("testasset")), "0x83dbfef1124e2d069d14840d52048dff140ab9f1", "It should store the value 89.");
  }

}
