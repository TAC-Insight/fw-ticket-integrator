# Fast-Weigh Ticket Integrator

The Fast-Weigh Ticket Integrator uses 32-bit ODBC connections to query compatible databases and post tickets to the Fast-Weigh API.

The API will create/update/void any of the tickets posted.

1. [Download the exe from the latest release](https://github.com/TAC-Insight/fw-ticket-integrator/releases)
2. Create `config.json` file in the same directory as the .EXE and set the `api_key` and `dsn` vars
3. Create `tickets.sql` file in the same directory as the .EXE
4. Set FastWeighTicketIntegrator.exe to run at startup
5. Done!

### config.json

```json
{
  "api_key": "your-api-key-goes-here",
  "dsn": "32-bit ODBC connection name goes here"
}
```

### tickets.sql

The `tickets.sql` file should conform to the https://api.fast-weigh.com/swagger/ui/index#!/Tickets/Tickets_Post payload body.

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
