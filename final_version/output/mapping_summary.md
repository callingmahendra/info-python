### **3. Mapping Details:**

| **Source Field**   | **Target Field**  | **Transformation Logic**                  |
|---------------------|-------------------|-------------------------------------------|
| `CUSTOMER_ID`      | `CUSTOMER_ID`     | Direct Map                               |
| `NAME`             | `NAME`            | Direct Map                               |
| `ADDRESS`          | `ADDRESS`         | Direct Map                               |
| `WEBSITE`          | `WEBSITE`         | Direct Map                               |
| `CREDIT_LIMIT`     | `CREDIT_LIMIT`    | Direct Map                               |
| `CUSTOMER_ID`      | `CUSTOMER_ID_output` | Direct Map into SQL Custom Transformation |
| `CUSTOMER_ID_output` | `CUSTOMER_ID`   | Direct Map from SQL Transformation        |
| `ORDER_ID`         | `CUST_ORDER_ID`   | Output from SQL Query in SQL Custom Transformation |
| `STATUS`           | `STATUS`          | Output from SQL Query in SQL Custom Transformation |
| `SALESMAN_ID`      | `SALESMAN_ID`     | Output from SQL Query in SQL Custom Transformation |
| `ORDER_DATE`       | `ORDER_DATE`      | Output from SQL Query in SQL Custom Transformation |

---

### **4. SQL Queries and Stored Procedures:**

#### **SQL Queries Used:**

**Source Qualifier Queries:**

- No explicit SQL query mentioned in the Source Qualifier (`SQ_CUSTOMERS`). It indicates that the transformation retrieves all fields directly.

**SQL Query Used in SQL Transformation:**
```sql
SELECT 
    ORDER_ID, 
    STATUS, 
    SALESMAN_ID, 
    ORDER_DATE
FROM 
    ORDERS
WHERE 
    CUSTOMER_ID = ?CUSTOMER_ID?
```

- **Purpose:** The query fetches order-related details (`ORDER_ID`, `STATUS`, `SALESMAN_ID`, `ORDER_DATE`) from the `ORDERS` table based on the `CUSTOMER_ID`.

#### **Stored Procedures Used:**

- **Name of Stored Procedures:** None specified explicitly within the workflow configuration.
- **Input Parameters:** N/A
- **Output Parameters:** N/A
- **Description:** No stored procedure is used in this mapping.

---

### **5. Business Rules and Logic:**

#### **Data Validation Rules:**
- The output of the SQL Transformation is mapped only if the records from the `CUSTOMERS` and the associated query (`ORDERS` table) satisfy the relationship based on `CUSTOMER_ID`.

#### **Data Quality Checks:**
- No explicit checks or rules for data cleansing or deduplication are mentioned, except the filter applied in the SQL transformation query (`WHERE CUSTOMER_ID = ?CUSTOMER_ID?`).

#### **Conditional Logic for Data Routing:**
- Conditional filtering is implemented in the SQL transformation to fetch only orders corresponding to the provided `CUSTOMER_ID`.

#### **Error Handling Mechanisms:**
- SQL Transformation generates an additional field called `SQLError`, which might be used to track or log SQL errors encountered during processing.
- The `CUSTOMER_ID` field's mapping through transformations ensures that all downstream logic aligns with this unique identifier as a reference key.

