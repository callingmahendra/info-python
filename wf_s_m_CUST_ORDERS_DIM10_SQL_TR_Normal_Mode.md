# Informatica PowerCenter to Python Migration Project: Workflow Documentation

**Workflow Name:** wf_s_m_CUST_ORDERS_DIM10_SQL_TR_Normal_Mode

**1. Workflow Description:**

*   This workflow extracts customer order data from the Oracle database, performs data transformations, and loads the transformed data into the target Oracle table.

**2. Source and Target Definitions:**

*   **Source:**
    *   System: Oracle Database
    *   Tables/Files: CUSTOMERS
    *   Data Fields: 
        *   CUSTOMER_ID (number, 15)
        *   NAME (nvarchar2, 255)
        *   ADDRESS (nvarchar2, 255)
        *   WEBSITE (nvarchar2, 255)
        *   CREDIT_LIMIT (number(p,s), 8, 2)
*   **Target:**
    *   System: Oracle Database
    *   Tables/Files: CUST_ORDERS_DIM10
    *   Data Fields: 
        *   CUSTOMER_ID (number, 15)
        *   NAME (nvarchar2, 255)
        *   ADDRESS (nvarchar2, 255)
        *   WEBSITE (nvarchar2, 255)
        *   CREDIT_LIMIT (number(p,s), 8, 2)
        *   CUST_ORDER_ID (number, 15)
        *   STATUS (nvarchar2, 20)
        *   SALESMAN_ID (number, 15)
        *   ORDER_DATE (date, 19)

**3. Mapping Details:**

| Source Field | Target Field | Transformation Logic |
|---|---|---|
| CUSTOMER_ID | CUSTOMER_ID | Direct Map |
| NAME | NAME | Direct Map |
| ADDRESS | ADDRESS | Direct Map |
| WEBSITE | WEBSITE | Direct Map |
| CREDIT_LIMIT | CREDIT_LIMIT | Direct Map |
| CUSTOMER_ID | CUST_ORDER_ID | SQL Query |
| STATUS | STATUS | SQL Query |
| SALESMAN_ID | SALESMAN_ID | SQL Query |
| ORDER_DATE | ORDER_DATE | SQL Query |

**4. SQL Queries and Stored Procedures:**

*   SQL Query used in the workflow:
    ```sql
    SELECT ORDER_ID, STATUS, SALESMAN_ID, ORDER_DATE
    FROM ORDERS
    WHERE CUSTOMER_ID = ?CUSTOMER_ID?
    ```

**5. Business Rules and Logic:**

*   Data validation rules:
    *   Ensure CUSTOMER_ID is not null.
    *   Ensure NAME is not null.
*   Data quality checks:
    *   Verify CREDIT_LIMIT is a positive number.
*   Conditional logic for data routing:
    *   None
*   Error handling mechanisms:
    *   Log errors and continue processing.

**6. Notes and Observations:**

*   Known limitations or constraints:
    *   None
*   Performance considerations:
    *   Ensure efficient indexing on CUSTOMER_ID in the ORDERS table.
*   Potential challenges for Python implementation:
    *   Handling large data volumes efficiently.

**7. Migration Considerations:**

*   Required Python libraries:
    *   pandas
    *   SQLAlchemy
*   Data access methods:
    *   Oracle database connectors
*   Data transformation libraries:
    *   pandas
*   Testing and validation strategies:
    *   Unit tests for data transformations
    *   Integration tests for end-to-end workflow
