SELECT
  TOP 2
  TicketNum AS TicketNumber,
  Transactions_DateTimeTransaction AS TicketDateTime,
  Customers_Customer_ID AS Customer_CustomerID
FROM Transactions
WHERE Transactions_DateTimeTransaction >= Date()-30