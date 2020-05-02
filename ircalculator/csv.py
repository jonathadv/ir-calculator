import re
import csv
from .stocks import Cost, Transaction, Stock


def process_transaction(transaction):
    costs = []

    headline = transaction.pop(0)

    ticker = headline[2]
    optype = headline[3].upper()
    date = headline[0]
    shares = headline[4]
    price_per_share = headline[5]

    for line in transaction:
        name = line[1]
        value = line[6].replace(",", ".")
        costs.append(Cost(name, value))

    return Transaction(ticker, optype, date, shares, price_per_share, costs)


def is_transaction_header(line):
    date_pattern = r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
    try:
        return bool(re.match(date_pattern, line[0]))
    except IndexError:
        return False


def process_stock_operations(stock_operations, stocks):
    start = -1
    for index, line in enumerate(stock_operations):
        has_start = start > -1
        has_more = index < len(stock_operations) - 1
        is_next_transaction_header = has_more and is_transaction_header(
            stock_operations[index + 1]
        )

        if not has_start and is_transaction_header(line):
            start = index
            continue

        if has_start and (is_next_transaction_header or not has_more):
            end = index + 1
            op = process_transaction(stock_operations[start:end])
            if not op.ticker in stocks:
                stocks[op.ticker] = Stock(op.ticker)
            stocks[op.ticker].add_operation(op)
            start = -1


def sanitize(content):
    new_content = []
    for line in content:
        if (
            line[0].startswith("Total")
            or (len(line) > 1 and line[1].startswith("Transferir") and line[2] == "")
            or any([i == "Dividend" for i in line])
            or any([i == "Rendimento" for i in line])
        ):
            continue
        new_content.append(line)

    return new_content


def process_csv(file):
    stocks = {}

    with open(file, newline="") as csvfile:
        month = csv.reader(csvfile, delimiter=",", quotechar='"')

        content = list(month)
        content = sanitize(content)

        start = -1
        for index, line in enumerate(content):
            has_start = start > -1
            has_more = index < len(content) - 1
            is_next_title = has_more and len(content[index + 1]) == 1

            if not has_start and len(line) == 1:
                start = index
                continue

            if has_start and is_next_title:
                end = index + 1
                process_stock_operations(content[start:end], stocks)
                start = -1

    return stocks
