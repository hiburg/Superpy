from datetime import datetime, date
from functions import *
from rich.console import Console
from rich.theme import Theme
from rich.table import Table
from rich.progress import track
from time import sleep

custom_theme = Theme({"succes": "green", "error": "bold red"})
console = Console(theme=custom_theme)


def process_data():
    sleep(0.02)


def report_inventory():
    console.print("")
    table = Table(title="Current inventory for SuperPy:", style="green")
    table.add_column("product", style="blue")
    table.add_column("expiration-date", style="blue")
    table.add_column("quantity", justify="right", style="blue")
    inventory = read_csvfile("inventory.csv")
    for row in inventory:
        table.add_row(row[0], row[2], row[1])
    console.print(table)


def report_revenue(date_temp):
    date_from, date_to = report_dates(date_temp)
    # If there is a problem with the date (YYYY-MM), stop further processing:
    if date_from == "" or date_to == "":
        return

    for _ in track(range(100), description="[green]Processing data"):
        process_data()

    list_sold = read_csvfile("sold.csv")
    revenue = 0
    for row in list_sold:
        if row[1] >= date_from and row[1] <= date_to:
            revenue += float(row[2])
    console.print(
        "=================== Revenue Report ====================", style="succes"
    )
    console.print(f"For this period     : {date_from} / {date_to}", style="succes")
    console.print(f"The total revenue is: {round(revenue,2)}", style="succes")


def report_profit(date_temp):
    date_from, date_to = report_dates(date_temp)
    # If there is a problem with the date (YYYY-MM), stop further processing:
    if date_from == "" or date_to == "":
        return

    for _ in track(range(100), description="[green]Processing data"):
        process_data()

    list_bought = read_csvfile("bought.csv")
    costs = 0
    for row in list_bought:
        if row[1] >= date_from and row[1] <= date_to:
            costs += float(row[2])
    list_sold = read_csvfile("sold.csv")
    revenue = 0
    for row in list_sold:
        if row[1] >= date_from and row[1] <= date_to:
            revenue += float(row[2])
    profit = revenue - costs
    console.print(
        "=================== Profit Report =====================", style="succes"
    )
    console.print(f"For this period     : {date_from} / {date_to}", style="succes")
    console.print(f"The total profit is : {round(profit,2)}", style="succes")
