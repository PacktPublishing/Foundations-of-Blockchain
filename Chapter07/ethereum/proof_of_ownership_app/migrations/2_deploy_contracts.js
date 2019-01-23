var ProofOfOwnership = artifacts.require("./ProofOfOwnership.sol");

module.exports = function(deployer) {
    deployer.deploy(ProofOfOwnership);
};
