import os
from datetime import datetime
import json
import pyodbc
from rich.console import Console
import requests
from flatten_dict import unflatten


def run_query():
    # Init rich console
    console = Console()

    # Clear the console
    os.system("cls")

    # Print the header
    header = ("[bold blue]================================[/bold blue] \n"
              "[bold blue]=[/bold blue] [bold]Fast-Weigh Ticket Integrator[/bold] [bold blue]=[/bold blue] \n"
              "[bold blue]================================[/bold blue]"
              )
    console.print(header)

    # Open and parse config.json
    with open("config.json") as config_file:
        config = json.load(config_file)

    # Connect to the database
    db = pyodbc.connect("DSN="+config["dsn"])
    cursor = db.cursor()

    # Open the tickets.sql file
    with open("tickets.sql", "r") as f:
        sql = f.read()

    # Execute the query
    cursor.execute(sql)
    rows = cursor.fetchall()
    results = []

    # Loop through the results and build a list of dictionaries
    column_names = [column[0] for column in cursor.description]
    for row in rows:
        flatDict = dict(zip(column_names, row))
        dictToAppend = unflatten(flatDict, splitter="underscore")
        results.append(dictToAppend)

    # Parse the results to JSON
    payload = json.dumps(results, indent=4, sort_keys=True, default=str)

    # Post tickets to the FW API
    r = requests.post("https://api.fast-weigh.com/v2/tickets",
                      data=payload,
                      headers={
                          "x-api-key": config["api_key"],
                          "content-type": "application/json"
                      })

    # Print the API response
    console.print("Last Sync: " + str(datetime.now()))
    console.print("API Response: " + str(r.status_code) + " " + r.reason)
    console.print(r.json())
    console.print(payload)
