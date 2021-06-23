# Summer of Bitcoin Challenge

Bitcoin miners construct blocks by selecting a set of transactions from their mempool. Each transaction in the mempool:includes a `fee` which is collected by the miner if that transaction is included in a block has a `weight`, which indicates the size of the transactionmay have one or more parent transactions which are also in the mempool.

 The miner selects an ordered list of transactions which have a combined weight below the maximum block weight. Transactions with parent transactions in th emempool may be included in the list, but only if all of their parents appear before them in the list.
 
 Naturally, the miner would like to include the transactions that maximize the total fee.
 
 The task is to write a program which reads a file mempool.csv, with the format:``<txid>,<fee>,<weight>,<parent_txids>``
 
 `txid` is the transaction identifierfee is the transaction fee.
`weight` is the transaction weight.

`parent_txids` is a list of the txids of the transaction’s unconfirmed parent transactions (confirmed parent transactions are not included in this list). It is of the form: ```<txid1>;<txid2>;...```

## Optimal Approach:

We can get fully Optimal solution by **Bitmasking approach** using dynammic programming
But it has exponential runtime execution

## My approach:
1. Parse Transaction
1. For every node calculate a transaction family(only including ancestors) priority ratio : family_fee/family_weight
1. Find the transaction with maximum priority ratio
1. Include it in the result list
1. Update family_paramaters
again go to step-2 while maximum allowed weight is reached or there is no more transactions left to process

**`solution.py`** contains the python code for above described approach

#### Execution time:
| env    |  time     |
| ---    |  ---      |
| real   | 0m40.486s |
| user   | 0m40.356s |
| sys    |0m0.130s   |

### My Result:
No. of blocks in final block: `3269` \
Maximum fee can be obtained: `5801809` \
Weight Utilised so far: `3999924`

