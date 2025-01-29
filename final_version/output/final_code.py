```python
import pandas as pd
import cx_Oracle

class ETLPipeline:
    def __init__(self, source_conn_str, target_conn_str):
        """
        Initialize the ETL pipeline with source and target database connection strings.
        :param source_conn_str: Connection string for the source Oracle database
        :param target_conn_str: Connection string for the target Oracle database
        """
        self.source_conn_str = source_conn_str
        self.target_conn_str = target_conn_str

    def load_source_data(self):
        """
        Extract data from the source Oracle database (CUSTOMERS table).
        :return: DataFrame containing the retrieved data from the CUSTOMERS table.
        """
        print("Extracting source data...")
        try:
            # Establish a connection to the source Oracle database
            source_conn = cx_Oracle.connect(self.source_conn_str)

            # Create a cursor object to execute queries
            source_cursor = source_conn.cursor()

            # SQL query to retrieve data from the CUSTOMERS table
            query = """
                SELECT
                    CUSTOMER_ID,
                    NAME,
                    ADDRESS,
                    WEBSITE,
                    CREDIT_LIMIT
                FROM
                    CUSTOMERS
            """
            # Execute the query
            source_cursor.execute(query)

            # Fetch all rows returned by the query
            source_data = source_cursor.fetchall()

            # Extract column names from the cursor description
            column_names = [col[0] for col in source_cursor.description]

            # Create a pandas DataFrame with the retrieved data
            source_df = pd.DataFrame(source_data, columns=column_names)

            # Close the cursor and connection
            source_cursor.close()
            source_conn.close()

            print("Source data extraction complete.")
            return source_df

        except cx_Oracle.DatabaseError as e:
            print(f"Error loading source data: {e}")
            raise

    def transform_source_data(self, source_data):
        """
        Transform the source data by joining it with ORDERS table data.
        :param source_data: DataFrame containing source data from the CUSTOMERS table.
        :return: DataFrame containing the transformed data.
        """
        print("Transforming source data...")
        try:
            # Establish a connection to the source Oracle database
            source_conn = cx_Oracle.connect(self.source_conn_str)
            source_cursor = source_conn.cursor()

            # Placeholder for transformed data
            transformed_data = []

            # Iterate over each row in the source DataFrame
            for index, row in source_data.iterrows():
                customer_id = row["CUSTOMER_ID"]

                # SQL query to retrieve related data from ORDERS table for the current CUSTOMER_ID
                query = """
                    SELECT 
                        :1 AS CUSTOMER_ID_output,
                        ORDER_ID,
                        STATUS,
                        SALESMAN_ID,
                        ORDER_DATE
                    FROM
                        ORDERS
                    WHERE 
                        CUSTOMER_ID = :1
                """
                # Execute the query
                source_cursor.execute(query, [customer_id])

                # Fetch the results from the ORDERS table
                order_data = source_cursor.fetchall()

                # For each order, combine data from CUSTOMERS and ORDERS
                for order_row in order_data:
                    transformed_row = {
                        "CUSTOMER_ID": row["CUSTOMER_ID"],
                        "NAME": row["NAME"],
                        "ADDRESS": row["ADDRESS"],
                        "WEBSITE": row["WEBSITE"],
                        "CREDIT_LIMIT": row["CREDIT_LIMIT"],
                        "CUST_ORDER_ID": order_row[1],  # ORDER_ID
                        "STATUS": order_row[2],         # STATUS
                        "SALESMAN_ID": order_row[3],    # SALESMAN_ID
                        "ORDER_DATE": order_row[4],     # ORDER_DATE
                    }
                    transformed_data.append(transformed_row)

            # Convert the transformed data into a pandas DataFrame
            transformed_df = pd.DataFrame(transformed_data)

            # Close the cursor and connection
            source_cursor.close()
            source_conn.close()

            print("Transformation complete.")
            return transformed_df

        except cx_Oracle.DatabaseError as e:
            print(f"Error transforming source data: {e}")
            raise

    def load_target_data(self, transformed_data):
        """
        Load the transformed data into the target Oracle database (CUST_ORDERS_DIM10 table).
        :param transformed_data: DataFrame containing transformed data.
        """
        print("Loading data into the target table...")
        try:
            # Establish a connection to the target Oracle database
            target_conn = cx_Oracle.connect(self.target_conn_str)
            target_cursor = target_conn.cursor()

            # SQL query to insert data into the target table
            insert_query = """
                INSERT INTO CUST_ORDERS_DIM10 (
                    CUSTOMER_ID,
                    NAME,
                    ADDRESS,
                    WEBSITE,
                    CREDIT_LIMIT,
                    CUST_ORDER_ID,
                    STATUS,
                    SALESMAN_ID,
                    ORDER_DATE
                ) VALUES (
                    :1, :2, :3, :4, :5, :6, :7, :8, :9
                )
            """

            # Convert the DataFrame rows to a list of tuples for efficient bulk inserts
            transformed_tuples = list(transformed_data.itertuples(index=False, name=None))

            # Perform batch insert into the target table
            target_cursor.executemany(insert_query, transformed_tuples)

            # Commit the transaction
            target_conn.commit()

            # Close the cursor and connection
            target_cursor.close()
            target_conn.close()

            print("Data load complete.")

        except cx_Oracle.DatabaseError as e:
            print(f"Error loading target data: {e}")
            raise

    def execute_pipeline(self):
        """
        Execute the entire ETL process: Extract, Transform, and Load.
        """
        try:
            # Step 1: Extract data from the source system
            source_data = self.load_source_data()

            # Step 2: Transform the extracted data
            transformed_data = self.transform_source_data(source_data)

            # Step 3: Load the transformed data into the target system
            self.load_target_data(transformed_data)

            print("ETL pipeline executed successfully.")

        except Exception as e:
            print(f"An error occurred during the ETL process: {e}")


if __name__ == "__main__":
    # Define source and target database connection strings
    source_conn_str = "source_user/source_password@source_host:1521/source_service"
    target_conn_str = "target_user/target_password@target_host:1521/target_service"

    # Initialize and execute the ETL pipeline
    etl_pipeline = ETLPipeline(source_conn_str, target_conn_str)
    etl_pipeline.execute_pipeline()
```