# Fast-Weigh Ticket Integrator

![screenshot](/screenshot.png)

The Fast-Weigh Ticket Integrator uses 32-bit ODBC connections to query compatible databases and post tickets to the Fast-Weigh API. It syncs tickets every 3 minutes.

The API will create/update/void any of the tickets posted.

1. [Download the exe from the latest release](https://github.com/TAC-Insight/fw-ticket-integrator/releases)
2. Create `config.json` file in the same directory as the .exe and set the `api_key` and `dsn` vars
3. Create `tickets.sql` file in the same directory as the .exe
4. Set FastWeighTicketIntegrator.exe to run at startup. (Run `shell:startup` via Windows Run. Copy a shortcut to the .exe into the startup directory.)
5. Done!

Your directory should look like:

```
- config.json
- FastWeighTicketIntegrator.exe
- tickets.sql
```

Once the exe runs you'll also have some logs / debug files:

```
- api_payload.json
- api_response.json
```

### config.json

You can write your own ODBC connection string in the "dsn" option, or use a 32-bit system DSN by name (preferred).

```json
{
  "api_key": "your-api-key-goes-here",
  "dsn": "dsn=...",
  "api_endpoint_url": "https://fwticketapi.azurewebsites.net/"
}
```

### tickets.sql

The `tickets.sql` file should conform to the [FW API ticket payload body](https://api.fast-weigh.com/swagger/ui/index#!/Tickets/Tickets_Post).

It is a simple text file with only the sql statement in it.

Field names should be renamed to match the keys in the ticket payload.

Sub-fields like the Region fields, Customer fields, etc... should be formated with underscores. Doing so will allow the program to parse the fields and nest them to match the format expected by the API endpoint.

A shortened example from the Libra dataset:

```sql
SELECT
  TicketNum AS TicketNumber,
  Transactions_DateTimeTransaction AS TicketDateTime,
  Customers_Customer_ID AS Customer_CustomerID
FROM Transactions
WHERE Transactions_DateTimeTransaction >= Date()-3
```

The above results in the following payload object:

```json
{
  "TicketNumber": 1234,
  "TicketDateTime": "2022-04-01 12:00:00",
  "Customer": {
    "CustomerID": "ABC"
  }
}
```

**Note**: In some cases, the nesting will go 2 or 3 levels deep. `Truck_Hauler_HaulerID` for example.

Here's a starter script for a **Libra Access DB**:

```sql
SELECT
  TicketNum AS TicketNumber
  ,FORMAT( DATEADD('h', 5, Transactions_DateTimeTransaction) , 'YYYY-MM-DDThh:mm:ss') AS TicketDateTime
  ,FORMAT( DATEADD('h', 5, Transactions_DateTimeTransaction) , 'YYYY-MM-DDThh:mm:ss') AS PrintDateTime
  ,-5 AS UTCOffset
  ,Weighmaster AS Operator
  ,Transactions_TonsGrossWeight AS GrossWeight
  ,Transactions_TonsTareWeight AS TareWeight
  ,Transactions_TonsNetWeight AS NetWeight
  ,Trucks_Truck_ID AS Truck_TruckID
  ,Mid([Trucks_Description],1,10) AS Truck_Hauler_HaulerID
  ,Trucks_Description AS Truck_Hauler_HaulerName
  ,'External' AS Truck_Hauler_HaulerType
  ,'EXEMPT' AS TaxCode_Code
  ,'DURACAP' AS Region_RegionName
  ,'ASBURY' AS Location_LocationName
  ,'ASBRY' AS Yard_YardName
  ,Customers_Customer_ID AS Customer_CustomerID
  ,Customers_Customer_Name AS Customer_CustomerName
  ,Jobs_Job_ID AS Order_ExternalOrderID
  ,Jobs_Job_Name AS Order_Description
  ,Jobs_PO_Number AS Order_PONumber
  ,'true' AS Order_UsePOD
  ,'U' AS OrderProduct_FreightType
  ,'U' AS OrderProduct_SurchargeType
  ,'EXEMPT' AS OrderProduct_TaxCode_Code
  ,Products_Product_ID AS OrderProduct_Product_ProductID
  ,Products_Product_Name AS OrderProduct_Product_ProductDescription
  ,'Ton' AS OrderProduct_Product_UnitOfMeasure
  ,VoidTkt AS Void
FROM Transactions
WHERE Transactions_DateTimeTransaction >= Date()-3
```

### Development notes

- 32-bit Python. Many of these old databases are only compatible with 32-bit applications/drivers.
- pyodbc requires Microsoft C++ Build Tools. The easiest way to get this is via the Visual Studio Installer.
- Create virtual env: `py -m venv venv` (make sure you activate the env as well)
- Install requirements: `pip install -r requirements.txt`
- Dev command: `py main.py`
- Build command: `py build.py`
