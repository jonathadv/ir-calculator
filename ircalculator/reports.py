from ircalculator.stocks import Stock, Transaction
from typing import List


def display(report):
    print("-" * 60)
    print("\n".join(report))
    print("-" * 60)


def build_sold_only(stocks: List[Stock]) -> List[str]:
    report = []

    for stock in stocks:
        result = stock.total_amount_with_cost(Transaction.SELL)
        if result:
            report.append(f"{stock.ticker}: {result}")
    return report


def build_overall_results(stocks: List[Stock]) -> List[str]:
    report = []

    for stock in stocks:
        result = stock.overall_result()
        report.append(f"{stock.ticker}: {result}")
    return report


def build_transactions(stock: Stock):
    report = []
    report.append("----------------------- Transaction -----------------------")

    for p in stock.get_transactions():
        report.append(str(p))
        report.append(f"\tpurchased: {p.total()}")
        for c in p.costs:
            report.append(f"\t\t{c}")

    report.append("-" * 60)

    return "\n".join(report)


def build_details(stocks: List[Stock]) -> List[str]:
    report = []
    for stock in stocks:
        transactions = build_transactions(stock)
        sell = stock.total_amount_with_cost(Transaction.SELL)
        buy = stock.total_amount_with_cost(Transaction.BUY)
        total_amount = buy if not sell else sell - buy

        content = f"""
# {stock.ticker}

Total Sold:         {stock.n_sold()}
Total Purchased:    {stock.n_purchased()}
Total Amount (RS):  {stock.total_amount()}
Total Cost (RS):    {stock.total_cost()}

Amount + Cost (RS): {total_amount}

{transactions}
"""
        report.append(content)
    return report
