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
  ,'KNOXTN' AS TaxCode_Code
  ,'APIRG' AS Region_RegionName
  ,'APILC' AS Location_LocationName
  ,'APIYD' AS Yard_YardName
  ,Customers_Customer_ID AS Customer_CustomerID
  ,Customers_Customer_Name AS Customer_CustomerName
  ,Jobs_Job_ID AS Order_ExternalOrderID
  ,Jobs_Job_Name AS Order_Description
  ,'U' AS OrderProduct_FreightType
  ,'U' AS OrderProduct_SurchargeType
  ,'KNOXTN' AS OrderProduct_TaxCode_Code
  ,Products_Product_ID AS OrderProduct_Product_ProductID
  ,Products_Product_Name AS OrderProduct_Product_ProductDescription
  ,'Ton' AS OrderProduct_Product_UnitOfMeasure
FROM Transactions
WHERE Transactions_DateTimeTransaction >= Date()-12