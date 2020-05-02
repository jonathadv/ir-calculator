from datetime import datetime
from typing import List, Union


class Cost:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = abs(float(value))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}={self.value})"


class Transaction:
    SELL = "SELL"
    BUY = "BUY"

    def __init__(
        self,
        ticker: str,
        trans_type: Union[SELL, BUY],
        date: str,
        shares: Union[str, int],
        price_per_share: Union[str, float],
        costs: List[Cost],
    ):
        self.ticker = ticker
        self.trans_type = trans_type
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.shares = abs(int(float(shares.replace(",", "."))))
        self.price_per_share = abs(float(price_per_share.replace(",", ".")))
        self.costs: List[Cost] = costs

    def total(self):
        value = self.shares * self.price_per_share
        return value

    def total_with_cost(self):
        total_costs = self.total_cost()

        if self.trans_type == self.SELL:
            total_costs = -self.total_cost()

        return self.total() + total_costs

    def total_cost(self):
        return sum([c.value for c in self.costs])

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ticker={self.ticker}, "
            f"type={self.trans_type}, "
            f"date={self.date}, "
            f"shares={self.shares}, "
            f"price_per_share={self.price_per_share})"
        )

    def __str__(self):
        return (
            f"[{self.date.strftime('%Y-%m-%d')}] | {self.trans_type} | "
            f"{self.shares} x {self.price_per_share} = {self.total()}"
        )


class Stock:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.purchased: List[Transaction] = []
        self.sold: List[Transaction] = []

    def add_operation(self, op: Transaction):
        if op.trans_type == Transaction.BUY:
            self.purchased.append(op)
        elif op.trans_type == Transaction.SELL:
            self.sold.append(op)
        else:
            raise Exception(f"Unable to add Operariont {op}")

    def n_transactions(self):
        return len(self.purchased) + len(self.sold)

    def n_purchased(self):
        return sum([i.shares for i in self.purchased])

    def n_sold(self):
        return sum([i.shares for i in self.sold])

    def total_amount(
        self, transaction_type: Union[Transaction.SELL, Transaction.BUY] = None
    ):
        transactions = self.get_transactions(transaction_type)
        return sum([t.total() for t in transactions])

    def total_amount_with_cost(
        self, transaction_type: Union[Transaction.SELL, Transaction.BUY] = None
    ):
        transactions = self.get_transactions(transaction_type)
        return sum([t.total_with_cost() for t in transactions])

    def total_cost(
        self, transaction_type: Union[Transaction.SELL, Transaction.BUY] = None
    ):
        transactions = self.get_transactions(transaction_type)
        return sum([t.total_cost() for t in transactions])

    def get_transactions(
        self, transaction_type: Union[Transaction.SELL, Transaction.BUY] = None
    ):
        opts = {
            Transaction.SELL: self.sold,
            Transaction.BUY: self.purchased,
        }

        transactions: List[Transaction] = opts.get(
            transaction_type, (self.sold + self.purchased)
        )

        return transactions

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ticker={self.ticker}, "
            f"n_transactions={self.n_transactions()}, "
            f"purchased={self.n_purchased()}, "
            f"sold={self.n_sold()}, "
            f"total_amount={self.total_amount()})"
        )
