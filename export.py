from functions import read_csvfile, write_csvfile, get_procdate, check_date1
from datetime import datetime
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"succes": "green", "error": "bold red"})
console = Console(theme=custom_theme)


def export_expired():
    date_now = get_procdate()
    inventory = read_csvfile("inventory.csv")
    expired = []
    header = ["productname", "buydate", "expirationdate"]
    expired.append(header)
    for row in inventory:
        if row[2] < date_now:
            expired.append(row)
    if len(expired) == 1:  # Header is already present in list expired
        console.print(f"No expired products were found in the inventory", style="error")
        return

    filename = (
        "export_inventory_"
        + datetime.strftime(datetime.now(), "%Y-%m-%d_%H%M%S")
        + ".csv"
    )
    write_csvfile(filename, expired)
    console.print(f"The expired items have been exported", style="succes")


def export_bought_sold(type_export, datefrom, dateto):
    # check  datefrom and dateto::
    if not check_date1(datefrom):
        console.print(
            f"Datefrom is invalid: {datefrom}. It should be a valid date in format: YYYY-MM-DD.",
            style="error",
        )
        return
    if not check_date1(dateto):
        console.print(
            f"Dateto is invalid: {dateto}. It should be a valid date in format: YYYY-MM-DD.",
            style="error",
        )
        return

    if type_export == "bought":
        list_temp = read_csvfile("bought.csv")
        header = ["productname", "buydate", "price", "expirationdate"]
    else:
        list_temp = read_csvfile("sold.csv")
        header = ["productname", "selldate", "price", "expirationdate"]

    if len(list_temp) == 0:
        console.print(
            f"No products are found in {type_export}.csv, no records to export",
            style="error",
        )
        return

    list_export = []
    list_export.append(header)
    for row in list_temp:
        if row[1] >= datefrom and row[1] <= dateto:
            list_export.append(row)

    if len(list_export) == 1:  # Only the header !
        console.print(f"No products to export for this period", style="error")
        return

    filename = (
        f"export_{type_export}_"
        + datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
        + ".csv"
    )
    write_csvfile(filename, list_export)
    console.print(
        f"The requested export has been done, see file: {filename}", style="succes"
    )
