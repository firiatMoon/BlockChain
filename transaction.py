class DataTransaction:
    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)


class Transaction:
    EMISSION = 0
    TRANSFER = 1

    id_transaction = DataTransaction()
    type_transaction = DataTransaction()
    from_value = DataTransaction()
    to_value = DataTransaction()
    amount = DataTransaction()
    signature = DataTransaction()

    def __init__(self):
        self.id_transaction = None
        self.type_transaction = None
        self.from_value = None
        self.to_value = None
        self.amount = None
        self.signature = None

    def set_id(self, id_trans: int):
        if isinstance(id_trans, int) and id_trans > 0:
            self.id_transaction = id_trans

    def set_type(self, type_trans: int):
        if type_trans not in (self.EMISSION, self.TRANSFER):
            raise ValueError
        if type_trans == self.EMISSION:
            self.from_value = None
            self.type_transaction = type_trans
        else:
            self.type_transaction = type_trans

    def set_from(self, from_name: str):
        if len(from_name) < 2 or len(from_name) > 10:
            raise ValueError
        if self.type_transaction == self.EMISSION:
            self.from_value = None
        else:
            self.from_value = from_name

    def set_to(self, to_name: str):
        if len(to_name) < 2 or len(to_name) > 10:
            raise ValueError()
        if self.from_value is not None and self.to_value == self.from_value:
            raise ValueError()
        else:
            self.to_value = to_name

    def set_amount(self, sum_transaction: int):
        if not isinstance(sum_transaction, int) or sum_transaction < 0:
            raise ValueError
        else:
            self.amount = sum_transaction

    def set_signature(self, hash_value: str):
        if len(hash_value) != 32:
            raise ValueError
        else:
            self.signature = hash_value

