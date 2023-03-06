from matplotlib import pyplot as plt
from functions import *


def plot_data(input_type, input_year):
    # check the input year:
    if not check_date2(input_year):
        console.print(
            f"Input date is invalid: {input_year}. It should be a valid date in this format: YYYY",
            style="error",
        )
        return

    # Declare a dictionary for the revenue per month / profit per month (if needed).
    dict_rev = {
        "01": 0,
        "02": 0,
        "03": 0,
        "04": 0,
        "05": 0,
        "06": 0,
        "07": 0,
        "08": 0,
        "09": 0,
        "10": 0,
        "11": 0,
        "12": 0,
    }
    if input_type == "profit":
        dict_prf = {
            "01": 0,
            "02": 0,
            "03": 0,
            "04": 0,
            "05": 0,
            "06": 0,
            "07": 0,
            "08": 0,
            "09": 0,
            "10": 0,
            "11": 0,
            "12": 0,
        }

    # Revenue: count the revenue per month and store it in the dictionaries based on the month.
    sold_list = read_csvfile("sold.csv")
    for row in sold_list:
        if int(input_year) == datetime.strptime(row[1], "%Y-%m-%d").date().year:
            index = datetime.strptime(row[1], "%Y-%m-%d").strftime("%m")
            dict_rev[index] += float(row[2])
            if input_type == "profit":
                dict_prf[index] += float(row[2])

    # Profit: we subtract all the boughts per month from the revenue per month to get the profit per month.
    if input_type == "profit":
        bought_list = read_csvfile("bought.csv")
        for row in bought_list:
            if int(input_year) == datetime.strptime(row[1], "%Y-%m-%d").date().year:
                index = datetime.strptime(row[1], "%Y-%m-%d").strftime("%m")
                dict_prf[index] -= float(row[2])

    # We take the keys (= month number) of one dictionary and use it to translate into month short-name.
    list_months = []
    for k in dict_rev.keys():
        index = 0
        list_months.append(datetime.strptime(k, "%m").strftime("%b"))

    # The revenues in the dictionary will be put in a list to plot it.
    list_rev = list(dict_rev.values())

    if input_type == "profit":
        list_prf = list(dict_prf.values())
        plt.bar(list_months, list_prf)
        plt.title(f"Profit for the year {input_year}")
    else:
        plt.bar(list_months, list_rev)
        plt.title(f"Revenue for the year {input_year}")

    plt.ylabel("In Euro")
    plt.show()
