import argparse
from report import *
from buysell import *
from export import *
from plot import *
from functions import get_procdate, set_procdate
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({"succes": "green", "error": "bold red"})
console = Console(theme=custom_theme)

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.


def main():
    parser = argparse.ArgumentParser(
        description="This is the Superpy CLI",
        epilog="Version 1.0 - Herman Iburg - Februari 2023",
    )
    # Optional arguments:
    parser.add_argument(
        "--init",
        dest="init",
        type=str,
        help="This will initialze all files or a specific file",
        choices=["all", "inventory", "buys", "sells", "datetime"],
        metavar="[all, inventory, buys, sells, datetime]",
    )
    parser.add_argument(
        "--advance",
        dest="days",
        type=int,
        help="Add N days to the processing date",
        metavar="N",
    )
    parser.add_argument(
        "--getdate", action="store_true", help="Retrieves the current processing date"
    )
    parser.add_argument(
        "--setdate",
        dest="set_date",
        help="Sets the processing date to a specific date",
        metavar="YYYY-MM-DD",
    )

    # Subparser commands
    # Command buy
    subparsers = parser.add_subparsers(
        title="Commands for Superpy",
        help="Choose one of these commands:",
        dest="command",
    )
    parser_buy = subparsers.add_parser("buy", help="Add a buy to bought.csv")
    parser_buy.add_argument(
        "--prodname",
        dest="product",
        type=str,
        required=True,
        help="Enter a product name (e.g. 'orange')",
        metavar="",
    )
    parser_buy.add_argument(
        "--price",
        dest="price",
        type=float,
        required=True,
        help="Enter a price (e.g. 1.59)",
        metavar="",
    )
    parser_buy.add_argument(
        "--expdate",
        dest="exp_date",
        type=str,
        required=True,
        help="Enter a date in format YYYY-MM-DD",
        metavar="",
    )
    # Command sell
    parser_sell = subparsers.add_parser("sell", help="Add a sell to sold.csv")
    parser_sell.add_argument(
        "--prodname",
        dest="product",
        type=str,
        required=True,
        help="Enter a product name (e.g. 'orange')",
        metavar="",
    )
    parser_sell.add_argument(
        "--price",
        dest="price",
        type=float,
        required=True,
        help="Enter a price (e.g. 1.59)",
        metavar="",
    )
    # Command report
    parser_report = subparsers.add_parser("report", help="Request a report")
    # Subparser report-type for report
    parser_report_type = parser_report.add_subparsers(
        dest="report_type", title="choose a report type", help="", required=True
    )
    # Report-type inventory
    parser_inventory = parser_report_type.add_parser(
        "inventory", help="Reports the current inventory"
    )
    parser_inventory.add_argument(
        "--now",
        action="store_true",
        help="reports inventory for the current date",
        required=True,
    )
    # Report-type revenue
    parser_revenue = parser_report_type.add_parser(
        "revenue", help="Reports the revenue"
    )
    parser_revenue.add_argument(
        "--now", action="store_true", help="reports revenue for the current date"
    )
    parser_revenue.add_argument(
        "--yesterday", action="store_true", help="reports revenue for yesterday"
    )
    parser_revenue.add_argument(
        "--date",
        type=str,
        help="reports revenue for a specific year/month e.g. 2019-12",
        metavar="2019-12",
    )
    # Report-type profit
    parser_profit = parser_report_type.add_parser("profit", help="Reports the profit")
    parser_profit.add_argument(
        "--now", action="store_true", help="reports profit for the current date"
    )
    parser_profit.add_argument(
        "--yesterday", action="store_true", help="reports profit for yesterday"
    )
    parser_profit.add_argument(
        "--date",
        type=str,
        help="reports profit for a specific year/month e.g. 2019-12",
        metavar="2019-12",
    )

    # Command export
    parser_export = subparsers.add_parser("export", help="Export to a csvfile")
    # Subparser export-type for export
    parser_export_type = parser_export.add_subparsers(
        dest="export_type", title="choose an export type", help="", required=True
    )
    # Export-type expired
    parser_export_type_exp = parser_export_type.add_parser(
        "expired", help="Exports the expired products in the inventory"
    )
    parser_export_type_exp.add_argument(
        "--now", action="store_true", required=True, help=""
    )
    # Export-type bought
    parser_export_type_buy = parser_export_type.add_parser(
        "bought", help="Exports the bought products for a period"
    )
    parser_export_type_buy.add_argument(
        "--datefrom", type=str, required=True, help="Startdate YYYY-MM-DD", metavar=""
    )
    parser_export_type_buy.add_argument(
        "--dateto", type=str, required=True, help="Enddate YYYY-MM-DD", metavar=""
    )
    # Export-type sold
    parser_export_type_sold = parser_export_type.add_parser(
        "sold", help="Exports the sold products for a period"
    )
    parser_export_type_sold.add_argument(
        "--datefrom", type=str, required=True, help="Startdate YYYY-MM-DD", metavar=""
    )
    parser_export_type_sold.add_argument(
        "--dateto", type=str, required=True, help="Enddate YYYY-MM-DD", metavar=""
    )

    # Command plot
    parser_plot = subparsers.add_parser("plot", help="Plot a graph of the inventory")
    # Subparser plot-type for plot
    parser_plot_type = parser_plot.add_subparsers(
        dest="plot_type", title="choose a plot type", help="", required=True
    )
    # Plot-type revenue
    parser_plot_type_rev = parser_plot_type.add_parser(
        "revenue", help="Plots the revenue for a specific year."
    )
    parser_plot_type_rev.add_argument(
        "--year",
        type=str,
        required=True,
        help="For example: --year 2023",
        metavar="YYYY",
    )
    # Plot-type profit
    parser_plot_type_prf = parser_plot_type.add_parser(
        "profit", help="Plots the profit for a specific year."
    )
    parser_plot_type_prf.add_argument(
        "--year",
        type=str,
        required=True,
        help="For example: --year 2023",
        metavar="YYYY",
    )

    args = parser.parse_args()
    
    
    # Handle the args:
    if args.command == None:
        if args.init != None:
            init_files(args.init)
        elif args.days != None:
            advance_time(args.days)
        elif args.getdate == True:
            proc_date = get_procdate()
            if proc_date != None:
                console.print(
                    f"The current processing date is: {proc_date}", style="succes"
                )
        elif args.set_date != None:
            if set_procdate(args.set_date) == True:
                console.print(
                    f"The processing date has been set to: {args.set_date}",
                    style="succes",
                )
        else:
            console.print(
                "No arguments were given, use -h instead to get some help",
                style="error",
            )

    elif args.command == "buy":
        buy(args.product, args.price, args.exp_date)

    elif args.command == "sell":
        sell(args.product, args.price)

    elif args.command == "report":
        if args.report_type == "inventory":
            report_inventory()
        elif args.now == False and args.yesterday == False and args.date == None:
            console.print(
                "You should use one of these options: --now , --yesterday or --date YYYY-MM",
                style="error",
            )
        elif args.report_type == "revenue":
            if args.now:
                report_revenue("now")
            elif args.yesterday:
                report_revenue("yesterday")
            else:
                report_revenue(args.date)
        elif args.report_type == "profit":
            if args.now:
                report_profit("now")
            elif args.yesterday:
                report_profit("yesterday")
            else:
                report_profit(args.date)

    elif args.command == "export":
        if args.export_type == "expired":
            export_expired()
        elif args.export_type == "bought":
            export_bought_sold("bought", args.datefrom, args.dateto)
        else:
            export_bought_sold("sold", args.datefrom, args.dateto)

    elif args.command == "plot":
        if args.plot_type == "revenue":
            plot_data("revenue", args.year)
        else:
            plot_data("profit", args.year)


if __name__ == "__main__":
    main()
