## Building the smart contract

`build poo.py test 0710 05 True False query ["f572f8ce40bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3"] `

## Importing the smart contract

`import poo.avm 0710 05 True False `

## Invoking the smart contract

* Register an asset

    `testinvoke 0x60a7ed582c6885addf1f9bec7e413d01abe54f1a register ["f572f8ce40
bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3","AK2nJJpJr6o664CWJKi1QRXj
qeic2zRp8y"]`

* Transfer an asset

    `testinvoke 0x60a7ed582c6885addf1f9bec7e413d01abe54f1a transfer ["f572f8ce40
bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3","AZ81H31DMWzbSnFDLFkzh9v
HwaDLayV7fU"]`

* Query an asset

    `testinvoke 0x60a7ed582c6885addf1f9bec7e413d01abe54f1a query ["f572f8ce40
bf97b56bad1c6f8d62552b8b066039a9835f294ea4826629278df3"]`