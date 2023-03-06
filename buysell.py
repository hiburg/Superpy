# from datetime import datetime
import os
from functions import *
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"succes": "green", "error": "bold red"})
console = Console(theme=custom_theme)


def buy(product, price, exp_date):
    # first a check on on the buy-price:
    if price < 0.01:
        console.print("The minimum price is 0.01", style="error")
        return

    # check on exp_date:
    if not check_date1(exp_date):
        console.print(
            f"exp_date is invalid: {exp_date}. It should be a valid date in this format: YYYY-MM-DD.",
            style="error",
        )
        return

    # check if the productname exists in the domain table:
    if not valid_product(product):
        console.print(
            f"Productname {product} is invalid, it does not appear to be a known product",
            style="error",
        )
        return

    # retrieve the processing date to assign to the buy-date:
    buy_date = get_procdate()
    if exp_date < buy_date:
        console.print(
            f"It is not possible to buy an item with an expired date: {exp_date}",
            style="error",
        )
        return

    # Add buy to bought.csv. If the file does not exists, it will be created first (mode append !)
    row_to_add = [product.lower(), buy_date, round(price, 2), exp_date]
    append_csvfile("bought.csv", row_to_add)

    # Add the buy to the inventory or update the quantity in the inventory if the productname and expiry date are already present.
    # If the file inventory.csv is not present it will be created.
    inventory_list = []
    filepath = os.path.join(os.getcwd(), "inventory.csv")
    if os.path.isfile(filepath):
        inventory_list = read_csvfile("inventory.csv")
        inventory_updated = False
        for row in inventory_list:
            if row[0] == product.lower() and row[2] == exp_date:
                quantity_row = int(row[1]) + 1
                row[1] = str(quantity_row)
                inventory_updated = True
                break

        if not inventory_updated:
            inventory_list.append([product.lower(), 1, exp_date])

        write_csvfile("inventory.csv", inventory_list)
    else:
        row_to_add = [product.lower(), 1, exp_date]
        inventory_list.append(row_to_add)
        write_csvfile("inventory.csv", inventory_list)
    console.print("This buy has been added", style="succes")


def sell(product, price):
    # first a check on on the buy-price:
    if price < 0.01:
        console.print("The minimum price is 0.01", style="error")
        return

    # check if the productname exists in the domain table:
    if not valid_product(product):
        console.print(
            f"Productname {product} is invalid, it does not appear to be a known product",
            style="error",
        )
        return

    proc_date = get_procdate()

    # first we check the inventory if a product is present. If it is present, the expiration-date must be
    # now (= processing date !) or in the future:
    inventory_updated = False
    exp_date = ""
    inventory = read_csvfile("inventory.csv")
    for row in inventory:
        if row[0] == product.lower() and row[2] >= proc_date:
            quantity_row = int(row[1]) - 1
            row[1] = str(quantity_row)
            inventory_updated = True
            exp_date = str(row[2])
            break

    # overwrite the updated inventory but without the items with a quantity of 0, they will be removed:
    if inventory_updated:
        inventory_new = []
        for row in inventory:
            if int(row[1]) != 0:  # quantity must be > 0 !
                inventory_new.append(row)
        write_csvfile("inventory.csv", inventory_new)

        # We have updated the inventory.csv, now we can write a record to the sells.csv:
        row_to_add = [product.lower(), proc_date, round(price, 2), exp_date]
        append_csvfile("sold.csv", row_to_add)
        console.print("This item has been sold", style="succes")
    else:
        console.print("This item is not available in the inventory", style="error")
    return
