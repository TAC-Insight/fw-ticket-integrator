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
    header = (
        "[bold blue]================================[/bold blue] \n"
        "[bold blue]=[/bold blue] [bold]Fast-Weigh Ticket Integrator[/bold] [bold blue]=[/bold blue] \n"
        "[bold blue]================================[/bold blue]"
    )
    console.print(header)

    # Open and parse config.json
    try:
        with open("config.json") as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        console.print(
            "[bold red]ERROR:[/bold red] config.json not found. Please create it in the same directory as the exe."
        )
        exit()

    # Set the web services URL based on config.json
    url = config["api_endpoint_url"]

    # Connect to the database
    db = pyodbc.connect(config["dsn"])
    cursor = db.cursor()

    # Open the tickets.sql file
    try:
        with open("tickets.sql", "r") as f:
            sql = f.read()
    except FileNotFoundError:
        console.print(
            "[bold red]ERROR:[/bold red] tickets.sql not found. Please create it in the same directory as the exe."
        )
        exit()

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

    # Write payload to api_payload.json
    with open("api_payload.json", "w") as f:
        f.write(payload)

    # Post tickets to the FW API
    r = requests.post(
        url,
        data=payload,
        headers={"Authorization": "Bearer " + config["api_key"], "content-type": "application/json"},
    )

    # Print the API response
    console.print("Last Sync: " + str(datetime.now()))
    console.print("Tickets Pulled: " + str(len(results)))
    console.print("API Response: " + str(r.status_code) + " " + r.reason)
    results = r.json()
    console.print(results["Message"])

    # Write the results to api_response.json
    with open("api_response.json", "w") as f:
        f.write(json.dumps(results, indent=4, sort_keys=True, default=str))
