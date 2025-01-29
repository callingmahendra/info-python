
import cx_Oracle

class SampleCode:
    def __init__(self, source_conn_str, target_conn_str):
        """
        Initialize with connection strings for source and target Oracle databases.
        :param source_conn_str: Connection string for the source system
        :param target_conn_str: Connection string for the target system
        """
        self.source_conn_str = source_conn_str
        self.target_conn_str = target_conn_str

    def load_source_data(self):
        """
        This method retrieves data from the source (CUSTOMERS table in Oracle).
        """
        try:
            # Establish a connection to the source Oracle database
            source_conn = cx_Oracle.connect(self.source_conn_str)
            
            # Create a cursor object to execute queries
            source_cursor = source_conn.cursor()

            # Define the SQL query to extract data from the CUSTOMERS table
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

            # Fetch all rows from the executed query
            source_data = source_cursor.fetchall()

            # Define column names
            column_names = [desc[0] for desc in source_cursor.description]

            # Close the source database cursor and connection
            source_cursor.close()
            source_conn.close()

            # Return the extracted data and column names
            return source_data, column_names

        except cx_Oracle.DatabaseError as e:
            print(f"Error loading source data: {e}")
            raise

    def load_target_data(self, transformed_data):
        """
        This method loads transformed data into the target (CUST_ORDERS_DIM10 table in Oracle).
        :param transformed_data: List of tuples representing transformed data
        """
        try:
            # Establish a connection to the target Oracle database
            target_conn = cx_Oracle.connect(self.target_conn_str)
            
            # Create a cursor object to execute queries
            target_cursor = target_conn.cursor()

            # Define the SQL query for inserting data into the target table
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

            # Bulk insert transformed data into the target table
            # `executemany` is used for efficient batch inserts
            target_cursor.executemany(insert_query, transformed_data)

            # Commit the transaction to ensure data is saved in the target table
            target_conn.commit()

            # Close the target database cursor and connection
            target_cursor.close()
            target_conn.close()

        except cx_Oracle.DatabaseError as e:
            print(f"Error loading target data: {e}")
            raise
