* **Source:**
  * System: Oracle  
  * Tables/Files: CUSTOMERS  
  * Data Fields:  
    - CUSTOMER_ID (number, Precision: 15, Scale: 0, not null)  
    - NAME (nvarchar2, Precision: 255, Scale: 0, not null)  
    - ADDRESS (nvarchar2, Precision: 255, Scale: 0, nullable)  
    - WEBSITE (nvarchar2, Precision: 255, Scale: 0, nullable)  
    - CREDIT_LIMIT (number(p,s), Precision: 8, Scale: 2, nullable)  

* **Target:**
  * System: Oracle  
  * Tables/Files: CUST_ORDERS_DIM10  
  * Data Fields:  
    - CUSTOMER_ID (number, Precision: 15, Scale: 0, nullable)  
    - NAME (nvarchar2, Precision: 255, Scale: 0, nullable)  
    - ADDRESS (nvarchar2, Precision: 255, Scale: 0, nullable)  
    - WEBSITE (nvarchar2, Precision: 255, Scale: 0, nullable)  
    - CREDIT_LIMIT (number(p,s), Precision: 8, Scale: 2, nullable)  
    - CUST_ORDER_ID (number, Precision: 15, Scale: 0, nullable)  
    - STATUS (nvarchar2, Precision: 20, Scale: 0, nullable)  
    - SALESMAN_ID (number, Precision: 15, Scale: 0, nullable)  
    - ORDER_DATE (date, Precision: 19, Scale: 0, nullable)  