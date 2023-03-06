import os
import csv
from datetime import datetime, timedelta, date
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"succes": "green", "error": "bold red"})
console = Console(theme=custom_theme)


# This functions reads a .csv file and returns its content as a list.
# If the .csv file is not present or damaged, a message will be given.
def read_csvfile(filename):
    filepath = os.path.join(os.getcwd(), filename)
    list_tmp = []
    try:
        with open(filepath, "r", newline="") as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar="|")
            list_tmp = list(csv_reader)
    except:
        console.print(
            f"A serious problem with csvfile: {filename}, maybe it is not present !",
            style="error",
        )
    finally:
        return list_tmp


# To append a list to a csv file.
def append_csvfile(filename, list_append):
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "a", newline="") as csvfile:
        csv_writer = csv.writer(
            csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerow(list_append)


# To (over)write a list to a csv file.
def write_csvfile(filename, list_write):
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w", newline="") as csvfile:
        csv_writer = csv.writer(
            csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
        )
        csv_writer.writerows(list_write)


# This function retrieves the domain table "products.csv" to check if a given productname is valid
def valid_product(product_name):
    list_products = read_csvfile("products.csv")
    for row in list_products:
        if product_name.lower() == row[0].lower():
            return True
    return False


def init_files(init):
    path = os.getcwd()
    filenames = []
    filename = ""
    # print("In de init")

    # First make a list with the required filenames (filename with extension !)
    if init == "all":
        filenames = ["bought.csv", "sold.csv", "inventory.csv"]
    elif init == "datetime":
        filename = "datetime.txt"
        filenames.append(filename)
    else:
        init = init + ".csv"
        filenames.append(init)

    # Remove the files:
    for filename in filenames:
        if os.path.isfile(os.path.join(path, filename)):
            os.remove(str(os.path.join(path, filename)))

    # If datetime.txt is removed, it will be created with the current date.
    # The other .csv files will be created in the functions buy and sell.
    if init == "all" or init == "datetime":
        file = open(os.path.join(path, "datetime.txt"), "w")
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        file.write(str(current_date))
        file.close()


def advance_time(days):
    if days == 0:
        console.print("Number of days to advance cannot be 0", style="error")
        return
    date_from = get_procdate_as_date()
    time_delta = timedelta(days=days)
    date_to = date_from + time_delta
    date_to_txt = datetime.strftime(date_to, "%Y-%m-%d")
    path = os.getcwd()
    filename = os.path.join(path, "datetime.txt")
    with open(str(filename), "w") as file:
        file.write(date_to_txt)
    console.print(
        f"The processing date has been advanced with {days} days to {date_to_txt}",
        style="succes",
    )


# This function reads the current processing date from file "datetime.txt"
def get_procdate():
    filepath = os.path.join(os.getcwd(), "datetime.txt")
    with open(filepath, "r", newline="") as file:
        proc_date = str(file.readline())
    try:
        type(datetime.strptime(proc_date, "%Y-%m-%d").date() == datetime.date)
    except ValueError:
        console.print(
            f"The date in file <datetime.txt> is invalid: {proc_date}.", style="error"
        )
        console.print(
            "You'd better use the init function to initialize the datetime.txt file",
            style="error",
        )
        console.print(
            "or use --setdate YYYY-MM-DD to change the date to a specific date.",
            style="error",
        )
        return

    return proc_date


# This function retrieves the current processing date from file "datetime.txt" as a date
def get_procdate_as_date():
    proc_date_txt = get_procdate()
    proc_date_dat = datetime.strptime(proc_date_txt, "%Y-%m-%d").date()
    return proc_date_dat


# This function retrieves the current processing date and sets it to another date
def set_procdate(set_date):
    date_is_ok = check_date1(set_date)
    if date_is_ok == False:
        console.print(
            f"The setdate is invalid: {set_date}. You should enter the setdate as YYYY-MM-DD",
            style="error",
        )
        return False

    filepath = os.path.join(os.getcwd(), "datetime.txt")
    with open(filepath, "w", newline="") as file:
        file.writelines(set_date)
    return True


# This function checks if a date (as string YYYY-MM-DD) is a valid date.
def check_date1(input_date):
    try:
        type(datetime.strptime(input_date, "%Y-%m-%d").date() == datetime.date)
        return True
    except ValueError:
        return False


# This function checks if a date (as string YYYY) is a valid date (year).
def check_date2(input_date):
    try:
        type(datetime.strptime(input_date, "%Y").date().year == datetime.year)
        return True
    except ValueError:
        return False


# This function will deliver a report-date-from (YYYY-MM-DD) and a report-date-to (YYYY-MM-DD):
def report_dates(date_temp):
    repdate_from = ""
    repdate_to = ""
    if date_temp == "now":
        repdate_from = date.strftime(get_procdate_as_date(), "%Y-%m-%d")
        repdate_to = date.strftime(get_procdate_as_date(), "%Y-%m-%d")
    elif date_temp == "yesterday":
        repdate = get_procdate_as_date() - timedelta(days=1)
        repdate_from = date.strftime(repdate, "%Y-%m-%d")
        repdate_to = date.strftime(repdate, "%Y-%m-%d")
    else:
        try:
            repdate1 = datetime.strptime(
                date_temp, "%Y-%m"
            ).date()  # 2019-11 => 2019-11-01
            repdate_from = date.strftime(repdate1, "%Y-%m-%d")

            next_month = repdate1.replace(day=28) + timedelta(days=4)  # 2019-12-01
            repdate2 = next_month - timedelta(days=next_month.day)  # 2012-11-30
            repdate_to = date.strftime(repdate2, "%Y-%m-%d")
        except ValueError:
            console.print(
                f"Dateperiod is invalid: {date_temp}. It should be a valid period in this format: YYYY-MM",
                style="error",
            )
        finally:
            return (repdate_from, repdate_to)
    return (repdate_from, repdate_to)
