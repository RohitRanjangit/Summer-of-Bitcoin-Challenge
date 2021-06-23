from functools import cmp_to_key

"""
We can get fully Optimal solution by Bitmasking approach
But it has exponential runtime execution

My approach:
1. Parse Transaction
2.For every node calculate a transaction family(only including ancestors) priority ratio : family_fee/family_weight
3.Find the transaction with maximum priority ratio
4.Include it in the result list
5.Update family_paramaters
again go to step2 while maximum allowed weight is reached or there is no more transactions left to process
"""

t_dict = {}
class MempoolTransaction():
    """
    class to represent a Transaction
    """
    id = 1
    def __init__(self, txid, fee, weight, *parents):
        """
        init method to set the class attributes
        additional attributes: family_fee, family_weight and id
        """
        self.txid = txid
        self.fee = int(fee)
        self.id = MempoolTransaction.id
        self.weight = int(weight)
        self.family_fee = self.fee
        self.family_weight = self.weight
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

t_list = transactions

def get_family_list(txid, has_included):
    """
    return the list of all ancestors of a transaction(including itself)
    approach: using Breadth First Search
    """
    assert txid not in has_included
    
    family_fee = t_dict[txid].fee
    family_weight = t_dict[txid].weight

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
                if p not in has_included:
                    family_list.append(p)
                    family_fee += t_dict[p].fee
                    family_weight += t_dict[p].weight
    family_list.reverse()
    return family_list, family_fee, family_weight

def adjust_family_parameters(family_list):
    """
    set family paramters of included transactions in the result to zero
    """
    for member in family_list:
        t_dict[member].family_fee = 0
        t_dict[member].family_weight = 0

def adjust_t_list(family_list):
    """
    remove all transactions from t_list that has been included in the result
    """
    result = []
    is_family = {}
    for member in family_list:
        is_family[member] = True
    for t in t_list:
        if t.txid in is_family:
            continue
        result.append(t)
    return result



def topological_ordering(tt_list, has_included):
    """
    get a topological ordering
    """
    topological_list = []
    visited = {}
    for t in tt_list:
        if t.txid not in visited:
            result = []
            topological_visit(t.txid, has_included, visited, result)
            topological_list += result
    return topological_list

def topological_visit(txid, has_included, visited, result):
    """
    an utility for topological ordering
    """
    visited[txid] = True
    t_dict[txid].family_weight = t_dict[txid].weight
    t_dict[txid].family_fee = t_dict[txid].fee
    for p in t_dict[txid].parents:
        if (p not in visited) and (p not in has_included):
            topological_visit(p, has_included, visited, result)
            t_dict[txid].family_weight = t_dict[p].weight
            t_dict[txid].family_fee = t_dict[p].fee
    result += [t_dict[txid]]

def process_family_parameter_update(txid, has_included, visited = None):
    """
    get cumulative fee, weight aggregate for all ancestors
    """
    if not visited:
        visited = dict()
    visited[txid] = True
    family_weight = t_dict[txid].weight
    family_fee = t_dict[txid].fee
    for p in t_dict[txid].parents:
        if (p not in visited) and (p not in has_included):
            res = process_family_parameter_update(p, has_included, visited)
            family_weight += res[0]
            family_fee += res[1]
    return family_weight, family_fee
            
    

def update_family_parameter(tt_list, has_included):
    """
    calculate family parameters
    """
    tt_list = topological_ordering(tt_list, has_included)
    for t in tt_list:
        assert t.txid not in has_included
        t.family_weight, t.family_fee = process_family_parameter_update(t.txid, has_included)

def correct_result(result_list):
    """
    check whether if transaction t in result then for every ancestor of t also in list
    and there no duplicate of t in result set
    """
    appeared = {}
    for tid in result_list:
        if tid in appeared:
            return False
        for p in t_dict[tid].parents:
            if p not in appeared:
                return False
        appeared[tid] = True
    return True
    


if __name__ == "__main__":

    result_list = []  #the final result list
    has_included = {}
    remaining_weight = maximum_block_weight
    res_fee = 0
    res_weight = 0

    while len(t_list):
        update_family_parameter(t_list, has_included)
        #sort transactions according to priority ratio
        t_list.sort(key=cmp_to_key(lambda t1, t2:t2.family_fee/t2.family_weight - t1.family_fee/t1.family_weight))
        first = t_list[0]
        t_list.pop(0)

        if first.family_weight > remaining_weight:
            t_list = adjust_t_list([first.txid])
            continue

        res_fee += first.family_fee
        res_weight += first.family_weight

        remaining_weight -= first.family_weight

        family_list, family_fee, family_weight = get_family_list(first.txid, has_included)

        try:
            assert family_fee == first.family_fee
            assert family_weight == first.family_weight
        except:
            #print(first.txid, family_weight, family_fee, family_list)
            pass

        adjust_family_parameters(family_list)

        t_list = adjust_t_list(family_list)
        result_list += family_list

        for mem in family_list:
            has_included[mem] = True
    
    print("No. of blocks in final block:", len(result_list))
    print("Maximum fee can be obtained:", res_fee)
    print("Weight Utilised so far:", res_weight)

    assert correct_result(result_list)

    with open('block.txt', 'w') as result_writer:
        for t in result_list:
            result_writer.write(t)
            result_writer.write('\n')

    
        


