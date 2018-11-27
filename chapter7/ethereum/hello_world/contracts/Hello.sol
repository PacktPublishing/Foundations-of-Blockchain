pragma solidity ^0.4.23;

contract Hello {

  function greetUser(bytes user) view public returns (bytes) {
      return abi.encodePacked("Hello ", user);

}
}
