Voor de opdracht Superpy CLI maak ik gebruik van drie .csv files. Al deze files bevatten geen headers aangezien het hier om interne data gaat. Bij het exporteren worden er wel headers aan de te exporteren bestanden toegevoegd. De gebruikte .csv files zijn:

1. bought.csv: in deze file zijn alle aankopen aanwezig. Dit bestand bestaat uit deze kolommen: 

   - product-name

   - buy-date

   - price

   - expiration-date

2.  sold.csv: dit bestand bevat alle verkopen. 

   - product-name
   - sell-date
   - price
   - expiration-date

3. inventory.csv: dit bestand bevat de **actuele** voorraad van Superpy. 

   - product-name
   - quantity
   - expiration-date



Alle aankopen worden opgeslagen in bought.csv en na een aankoop wordt de voorraad, inventory.csv,  bijgewerkt (voor een nieuw product wordt er een record aangemaakt met quantity=1 , voor een bestaand product wordt de quantity opgehoogd met 1).  De combinatie product-name en expiration-date zijn uniek in inventory.csv (primary key). D.w.z. als de combinatie product-name en expiration-date al aanwezig is in inventory.csv dan wordt de quantity met 1 opgehoogd bij een aankoop. Om die reden wordt de buy-date dan ook niet apart opgeslagen in inventory.csv, immers de combi productname/expiration-date kan op verschillende momenten zijn aangekocht.

Voor een verkoop geldt dat er gebruik gemaakt wordt van het FIFO principe (first in, first out). Het oudste artikel (oudste expiration date) wordt als eerste verkocht mits de expiration-date nog niet verstreken is. Bij een verkoop wordt de voorraad bijgewerkt: de quantity wordt met 1 verlaagd. Mocht er een quantity van 0 overblijven dan wordt dit record uiteraard verwijderd.



Bij het bouwen en programmeren van deze CLI liep ik tegen een aantal zaken aan en daarvoor heb ik een oplossing bedacht:

1. Sommige functiionaliteit wordt meerdere keren uitgevoerd, zoals bijvoorbeeld het inlezen en wegschrijven van .csv files en het controleren van een ingevoerde datum. Daarom heb ik ervoor gekozen om dit in aparte functies onder te brengen (functions.py) en deze vanuit de overige functies aan te roepen indien nodig. Dit voorkomt dubbele coding en het is eenvoudiger te onderhouden. Ook heb ik de programmatuur van Superpy opgedeeld in meerdere logische files om het overzichtelijk te houden (vb report.py en export.py).

   ```
   # This function checks if a date (as string YYYY-MM-DD) is a valid date.
   
   def check_date1(input_date):
     	try:
   		type(datetime.strptime(input_date, "%Y-%m-%d").date() == datetime.date)
   		return True
   	except ValueError:
   		return False
   ```

   

2. Bij het opvoeren van een aankoop moet er een productname worden opgegeven. Deze wordt dan initieel in de inventory vastgelegd (bij een nieuw product). Aangezien een gebruiker voor een productname iets willekeurigs kan invoeren heb ik ervoor gekozen om de productnames vast te leggen in een domeintabel (products.csv). Bij het opvoeren van een aankoop wordt dan gecontroleerd of de productname voorkomt in de domeintabel. Een productname wordt altijd in lowercase opgeslagen. In de toekomst kan Superpy worden uitgebreid met een aparte beheerfunctie op deze products.csv.

   ```
   Apple,fruit
   Apricot,fruit
   Avocado,fruit
   ...
   ...
   Tomato,vegetable
   Yam,vegetable
   Zucchini,vegetable
   ```

   

3. De interne datum (processing date) die in Superpy wordt gebruikt heb ik opgeslagen in een apart bestand (datetime.txt). Deze datum kan worden aangepast met de functies **get_procdate()** en **advance_time()**. Ook kan worden gecontroleerd welke datum er nu in het bestand staat door middel van de functie **set_procdate().**

   ```
   Datetime.txt:
   2023-03-01
   ```



4. De CLI is gebouwd m.b.v. de library argpase. Aangezien deze CLI diverse commando's en opties bevat heb ik ervoor gekozen om deze onder te brengen in subparsers. Voor elk commando (buy, sell, export etc) is er een aparte subparser bedacht. Voor sommige commando's (report, export en plot) is er daarnaast nog een extra subparser bedacht welke het type (report, export en plot) aangeeft. Een voorbeeld is het plot_type welke bestaat uit een revenu of profit. Deze indeling maakt de structuur van de CLI overzichtelijker.

   ```
   # Command plot
       parser_plot = subparsers.add_parser("plot", help="Plot a graph of the inventory")
       # Subparser plot-type for plot
       parser_plot_type = parser_plot.add_subparsers(
           dest="plot_type", title="choose a plot type", help="", required=True)
       # Plot-type revenue
       parser_plot_type_rev = parser_plot_type.add_parser(
           "revenue", help="Plots the revenue for a specific year."
   
   ```

   

