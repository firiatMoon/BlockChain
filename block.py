from transaction import Transaction
import hashlib


class DataBlock:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)


class Block():
    id_block = DataBlock()
    transactions = DataBlock()

    def __init__(self):
        self.id_block = None
        self.transactions = []

    def set_id(self, id_block: int):
        if isinstance(id_block, int):
            self.id_block = id_block

    def validate_transaction(self, transaction: Transaction):
        string = str(f'{transaction.id_transaction}:{transaction.type_transaction}:{transaction.from_value}:{transaction.to_value}:{transaction.amount}')
        check_signature = hashlib.md5(string.encode("utf-8"))
        if check_signature.hexdigest() == transaction.signature:
            return True
        return False

    def add_transaction(self, transaction: Transaction):
        number = transaction.id_transaction
        if not self.validate_transaction(transaction):
            raise ValueError()
        if len(self.transactions) >= 10:
            raise ValueError()
        for i in range(len(self.transactions)):
            if self.transactions[i]['id_transaction'] == number:
                raise ValueError()
        self.transactions.append(transaction.__dict__)

