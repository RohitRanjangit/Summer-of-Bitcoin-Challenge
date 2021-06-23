from functools import cmp_to_key

"""
The Selection of ordered list : I mean that we've to choose the transactions in order that they appear
in mempool.csv
if It's not the case then I've to only tweak the line no. 69 in this code
"""

t_dict = {}
class MempoolTransaction():
    id = 1
    def __init__(self, txid, fee, weight, *parents):
        self.txid = txid
        self.fee = int(fee)
        self.id = MempoolTransaction.id
        self.weight = int(weight)
        self.family_fee = self.fee
        self.family_weight = self.weight
        self.family_order = 1
        self.family_size = 1
        self.child_list = list()
        if parents[0]:
            self.parents = parents[0].split(';')
        else:
            self.parents = []
        t_dict[self.txid] = self
        MempoolTransaction.id += 1



def parse_mempool_csv():
    """Parse the CSV file and return a list of MempoolTransactions."""
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()[1:]])


transactions = parse_mempool_csv()

#set maximum block weight here
maximum_block_weight = 4000000

def assert_consistency(t_list):
    appeared = {}
    for transaction in t_list:
        if transaction.txid in appeared:
            return False
        if transaction.txid in transaction.parents:
            return False
        appeared[transaction.txid] = True
    return True

if not assert_consistency(transactions):
    print("Malformed data in mempool.csv")
    exit(-1)

t_list = []
t_pos = {}
for t in transactions:
    include = True
    curr_order = t.family_order
    for p in t.parents:
        t.family_fee += t_dict[p].family_fee
        t.family_weight += t_dict[p].family_weight
        t.family_size += t_dict[p].family_size
        t.family_order = min(t_dict[p].family_order + curr_order,t.family_order)
        t_dict[p].child_list.append(t.txid)
        if t_dict[p].id > t.id:
            include = False
    if include:
        t_list.append(t)
        t_pos[t.txid] = len(t_list)-1


def get_family_list(txid):
    family_list = [txid]
    visited = {}
    visited[txid] = True
    queue = [txid]
    while len(queue):
        first = queue[0]
        queue.pop(0)
        for p in t_dict[first].parents:
            if not p in visited:
                visited[p] = True
                queue.append(p)
                family_list.append(p)
    family_list.reverse()
    return family_list

def adjust_family_parameters(family_list):
    for member in family_list:
        t_dict[member].family_fee = 0
        t_dict[member].family_weight = 0

def adjust_t_list(family_list):
    result = []
    is_family = {}
    for member in family_list:
        is_family[member] = True
    for t in t_list:
        if t.txid in is_family:
            continue
        result.append(t)
    return result

def update_family_parameter(tt_list):
    for t in tt_list:
        t.family_fee = t.fee
        t.family_weight = t.weight
        for p in t.parents:
            t.family_fee += t_dict[p].family_fee
            t.family_weight += t_dict[p].family_weight

if __name__ == "__main__":

    result_list = []
    remaining_weight = maximum_block_weight
    res_fee = 0
    res_weight = 0

    while len(t_list):
        t_list.sort(key=cmp_to_key(lambda t1, t2:t2.family_fee/t2.family_weight - t1.family_fee/t1.family_weight))
        first = t_list[0]
        t_list.pop(0)

        if first.family_weight > remaining_weight:
            t_list = adjust_t_list([first.txid])
            continue

        res_fee += first.family_fee
        res_weight += first.family_weight

        remaining_weight -= first.family_weight

        family_list = get_family_list(first.txid)

        adjust_family_parameters(family_list)

        t_list = adjust_t_list(family_list)

        update_family_parameter(t_list)
        result_list += family_list
    
    print("No. of blocks in final block:", len(result_list))
    print("Maximum fee can be obtained:", res_fee)
    print("Weight Utilised so far:", res_weight)

    with open('block.txt', 'w') as result_writer:
        for t in result_list:
            result_writer.write(t)
            result_writer.write('\n')

    
        


