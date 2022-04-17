from transaction import Transaction
from block import Block


class BlockChain():
    def __init__(self):
        self.list_num_blocks = {}
        self.block_tree_transaction = {}

    def get_blockchain(self):
        '''return the longest chain of Blocks'''
        max_line = {}
        for key, value in self.list_num_blocks.items():
            max_line[key] = len(value)
            return max(max_line, key=max_line.get)

    def validate_block(self, block: Block):
        if len(block.transactions) < 0:
            return False
        for value in self.list_num_blocks.values():
            if block.id_block in value:
                return False
        return True

    def add_block(self, parent_block_id: int, block: Block):
        if self.validate_block(block):
            return False
        if parent_block_id is None and len(self.list_num_blocks) > 0:
            return False
        if parent_block_id not in self.list_num_blocks:
            return False
        for value in self.operations(block).values():
            if value < 0:
                return False
        else:
            if parent_block_id not in self.block_tree_transaction:
                self.block_tree_transaction[parent_block_id] = self.operations(block)
                self.list_num_blocks.setdefault(parent_block_id, []).append(block.id_block)
            else:
                for key, value in self.operations(block).items():
                    if key in self.block_tree_transaction[parent_block_id]:
                        self.block_tree_transaction[parent_block_id][key] += value
                        self.list_num_blocks.setdefault(parent_block_id, []).append(block.id_block)

    def operations(self, block: Block):
        list_operation = {}
        for i in range(len(block.transactions)):
            # return block.transactions[i]['type_transaction']
            if block.transactions[i]['type_transaction'] == 0:
                if block.transactions[i]['to_value'] not in list_operation:
                    list_operation[block.transactions[i]['to_value']] = block.transactions[i]['amount']
                else:
                    list_operation[block.transactions[i]['to_value']] += block.transactions[i]['amount']
            elif block.transactions[i]['type_transaction'] == 1:
                if block.transactions[i]['to_value'] not in list_operation:
                    list_operation[block.transactions[i]['to_value']] = block.transactions[i]['amount']
                    list_operation[block.transactions[i]['from_value']] -= block.transactions[i]['amount']
                else:
                    list_operation[block.transactions[i]['to_value']] += block.transactions[i]['amount']
                    list_operation[block.transactions[i]['from_value']] -= block.transactions[i]['amount']
        return list_operation

    def get_balance(self, account: str) -> str:
        if len(self.block_tree_transaction) > 0:
            max_tree_blocks = self.block_tree_transaction[self.get_blockchain()]
            return max_tree_blocks.get(account, 0)
        return f'0'


trx = Transaction()
trx.set_id(1)
trx.set_to('bob')
trx.set_from('hany')
trx.set_type(0)
trx.set_amount(100)
trx.set_signature('9ed588c209ecf3119d31400ec2bc67a6')

trx1 = Transaction()
trx1.set_id(2)
trx1.set_type(1)
trx1.set_from('bob')
trx1.set_to('alice')
trx1.set_amount(50)
trx1.set_signature('fef42c7324e60257aa4284fd6331c820')

# trx1.set_signature('5f87e75d786d8c50a0cb3b933521fc34')

bl = Block()
bl.set_id(1)
bl.add_transaction(trx)
bl.add_transaction(trx1)

trx3 = Transaction()
trx3.set_id(3)
trx3.set_type(0)
trx3.set_to('alice')
trx3.set_amount(150)
trx3.set_signature('6cdefb6f3b7c02b85cf0ca6f9fa85269')

bl2 = Block()
bl2.set_id(2)
bl2.add_transaction(trx3)

# trx4 = Transaction()
# trx4.set_id(4)
# trx4.set_type(1)
# trx4.set_from('bob')
# trx4.set_to('alice')
# trx4.set_amount(5)
# trx4.set_signature('6cdefb6f3b7c02b85cf0ca6f9fa85269')
# # print(bl.transactions)
# # print(bl2.transactions)
#
blch = BlockChain()
# print(blch.operations(bl))


blch.add_block(1, bl)
blch.add_block(1, bl2)
#
#
print(blch.block_tree_transaction)
print(blch.list_num_blocks)

print(blch.get_balance('bob'))
print(blch.get_balance('alice'))
#
# # check_signature = hashlib.md5()
# # check_signature.update(b'1:0:None:bob:100')
# # print(check_signature.hexdigest())
# # check_signature = hashlib.md5(b'2:1:bob:alice:50')
# # print(check_signature.hexdigest())
# # check_signature = hashlib.md5(b'2:1:bob:alice:50')
# # print(check_signature.hexdigest())
