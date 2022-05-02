from transaction import Transaction
from block import Block


class BlockChain():
    def __init__(self):
        self.chain = []
        self.tree_blocks = {}

    def get_blockchain(self):
        length_chains = [len(self.chain[i]) for i in range(1, len(self.chain))]
        max_line = max(length_chains)
        for i in range(1, len(self.chain)):
            if len(self.chain[i]) == max_line:
                return i

    @staticmethod
    def in_chain(id_data, list_data):
        all_blocks_in_chain = set()
        for i in range(1, len(list_data)):
            for j in range(len(list_data[i])):
                if list_data[i][j] not in all_blocks_in_chain:
                    all_blocks_in_chain.add(list_data[i][j])
        if id_data not in all_blocks_in_chain:
            return True
        return False

    @staticmethod
    def data_validation(block: Block):
        list_operation = {}
        for i in range(len(block.transactions)):
            if block.transactions[i]['type_transaction'] == Transaction.EMISSION:
                if block.transactions[i]['to_value'] not in list_operation:
                    list_operation[block.transactions[i]['to_value']] = block.transactions[i]['amount']
                else:
                    list_operation[block.transactions[i]['to_value']] += block.transactions[i]['amount']
            elif block.transactions[i]['type_transaction'] == Transaction.TRANSFER:
                if block.transactions[i]['to_value'] not in list_operation:
                    list_operation[block.transactions[i]['to_value']] = block.transactions[i]['amount']
                    list_operation[block.transactions[i]['from_value']] -= block.transactions[i]['amount']
                else:
                    list_operation[block.transactions[i]['to_value']] += block.transactions[i]['amount']
                    list_operation[block.transactions[i]['from_value']] -= block.transactions[i]['amount']
        for value in list_operation.values():
            if value < 0:
                return False
        return True

    def validate_block(self, block: Block):
        if len(block.transactions) > 0:
            return True
        if self.in_chain(block.id_block, self.chain):
            return True

    def add_block(self, parent_block_id: int, block: Block):
        if not self.validate_block(block):
            return False
        if parent_block_id is None and len(self.chain) > 0:
            return False
        if not self.in_chain(parent_block_id, self.chain):
            return False

        if not self.data_validation(block):
            return False

        if parent_block_id is None:
            self.chain.append(block.id_block)

        if parent_block_id is not None:
            if parent_block_id == self.chain[0]:
                self.chain.append([parent_block_id, block.id_block])
            else:
                for i in range(1, len(self.chain)):
                    if parent_block_id in self.chain[i]:
                        if self.chain[i][-1] == parent_block_id:
                            self.chain[i].append(block.id_block)
                        else:
                            segment = self.chain[i][:self.chain[i].index(parent_block_id) + 1]
                            segment.append(block.id_block)
                            self.chain.extend([segment])
                            break
        self.tree_blocks[block.id_block] = block.transactions

    def get_balance(self, account: str) -> str:
        if account is None or len(account) < 2 or len(account) > 100:
            raise ValueError
        long_chain = self.chain[self.get_blockchain()]
        final_settlement_of_transactions = {}
        for id_block, transactions in self.tree_blocks.items():
            if id_block in long_chain:
                for i in range(len(transactions)):
                    if transactions[i]['type_transaction'] == Transaction.EMISSION:
                        if transactions[i]['to_value'] not in final_settlement_of_transactions:
                            final_settlement_of_transactions[transactions[i]['to_value']] = transactions[i]['amount']
                        else:
                            final_settlement_of_transactions[transactions[i]['to_value']] += transactions[i]['amount']
                    elif transactions[i]['type_transaction'] == Transaction.TRANSFER:
                        if transactions[i]['to_value'] not in final_settlement_of_transactions:
                            final_settlement_of_transactions[transactions[i]['to_value']] = transactions[i]['amount']
                            final_settlement_of_transactions[transactions[i]['from_value']] -= transactions[i]['amount']
                        else:
                            final_settlement_of_transactions[transactions[i]['to_value']] += transactions[i]['amount']
                            final_settlement_of_transactions[transactions[i]['from_value']] -= transactions[i]['amount']
        return final_settlement_of_transactions.get(account, 0)
