from datetime import datetime
from typing import List


class Cost:
    def __init__(self, name, value):
        self.name = name
        self.value = abs(float(value))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}={self.value})"


class Transaction:
    SELL = "SELL"
    BUY = "BUY"

    def __init__(
        self, ticker, optype, date, shares, price_per_share, costs: List[Cost]
    ):
        self.ticker = ticker
        self.optype = optype
        self.date = datetime.strptime(date, "%Y-%m-%d")
        self.shares = abs(int(float(shares.replace(",", "."))))
        self.price_per_share = abs(float(price_per_share.replace(",", ".")))
        self.costs: List[Cost] = costs

    def total(self):
        value = self.shares * self.price_per_share
        return value

    def total_with_cost(self):
        total_costs = self.total_cost()

        if self.optype == self.SELL:
            total_costs = -self.total_cost()

        return self.total() + total_costs

    def total_cost(self):
        return sum([c.value for c in self.costs])

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ticker={self.ticker}, "
            f"type={self.optype}, "
            f"date={self.date}, "
            f"shares={self.shares}, "
            f"price_per_share={self.price_per_share})"
        )

    def __str__(self):
        return f"[{self.date.strftime('%Y-%m-%d')}] | {self.optype} | {self.shares} x {self.price_per_share} = {self.total()}"


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self.purchased: List[Transaction] = []
        self.sold: List[Transaction] = []

    def add_operation(self, op: Transaction):
        if op.optype == Transaction.BUY:
            self.purchased.append(op)
        elif op.optype == Transaction.SELL:
            self.sold.append(op)
        else:
            raise Exception(f"Unable to add Operariont {op}")

    def n_transactions(self):
        return len(self.purchased) + len(self.sold)

    def n_purchased(self):
        return sum([i.shares for i in self.purchased])

    def n_sold(self):
        return sum([i.shares for i in self.sold])

    def total_amount(self):
        transactions = self.sold + self.purchased
        return sum([t.total() for t in transactions])

    def total_amount_with_cost(self):
        transactions = self.sold + self.purchased
        return sum([t.total_with_cost() for t in transactions])

    def total_cost(self):
        transactions: Transaction = self.sold + self.purchased
        return sum([t.total_cost() for t in transactions])

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"ticker={self.ticker}, "
            f"n_transactions={self.n_transactions()}, "
            f"purchased={self.n_purchased()}, "
            f"sold={self.n_sold()}, "
            f"total_amount={self.total_amount()})"
        )
