**Summer of Bitcoin Challenge**

Bitcoin miners construct blocks by selecting a set of transactions from their mempool. Each transaction in the mempool:includes a `fee` which is collected by the miner if that transaction is included in a block has a `weight`, which indicates the size of the transactionmay have one or more parent transactions which are also in the mempool.

 The miner selects an ordered list of transactions which have a combined weight below the maximum block weight. Transactions with parent transactions in th emempool may be included in the list, but only if all of their parents appear before them in the list.
 
 Naturally, the miner would like to include the transactions that maximize the total fee.
 
 The task is to write a program which reads a file mempool.csv, with the format:``<txid>,<fee>,<weight>,<parent_txids>``
 
 `txid` is the transaction identifierfee is the transaction fee.
`weight` is the transaction weight.

`parent_txids` is a list of the txids of the transaction’s unconfirmed parent transactions (confirmed parent transactions are not included in this list). It is of the form: ```<txid1>;<txid2>;...```

