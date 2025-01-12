# PostgreSQL Database Integration with Python 3
import psycopg2
from psycopg2 import sql
import json

class Database:
    #PosrgeSQL Server Connection Settings
    DB_SERVER_CONFIG = {
        "host": "localhost",
        "database": "postgres",
        "user": "postgres",
        "password": "Faiz256",
        "port": "5432"
    }
    DB_NAME = "playerData"
    # Create Database

    @classmethod
    def createDatabase(cls):
            try:
                # Connect to the PostgreSQL server (not a specific database yet)
                connection = psycopg2.connect(**cls.DB_SERVER_CONFIG)
                connection.autocommit = True  # Enable autocommit to execute CREATE DATABASE

                # Create a cursor
                cursor = connection.cursor()

                # Check if the database already exists
                cursor.execute(
                    "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s;", (cls.DB_NAME,)
                )
                exists = cursor.fetchone()
                if exists:
                    print(f"Database '{cls.DB_NAME}' already exists.")
                else:
                    # Create the new database
                    cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(cls.DB_NAME)))
                    print(f"Database '{cls.DB_NAME}' created successfully.")

            except Exception as e:
                print("Error while creating the database:", e)
            
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("Server connection closed.")
            

    @staticmethod
    def get_postgresql_type(value):
        if isinstance(value, str):
            return "VARCHAR(255)"
        elif isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "REAL"
        elif isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, list):
            return "JSONB"  # Use JSONB for storing lists
        elif isinstance(value, dict):
            return "JSONB"  # Use JSONB for nested dictionaries
        elif hasattr(value, "__dict__"):
            return "JSONB"  # Serialize Python objects as JSONB
        else:
            return "TEXT"  # Default to TEXT for unsupported types
        
    @classmethod
    def createTable(cls, table_name, data):
        """
        Ensures the table exists in the PostgreSQL database.
        If the table does not exist, it is created based on the provided data.
        If the table already exists, the function does nothing.
        
        Args:
        - table_name: Name of the table to check/create.
        - data: Dictionary containing the column names and sample data types for the table.
        """
        # Create a connection to the PostgreSQL database
        try:
            conn = psycopg2.connect(**cls.DB_SERVER_CONFIG)
            print("Connected to the database successfully.")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            return
        
        try:
            with conn.cursor() as cursor:
                # Check if the table already exists
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT 1 
                        FROM information_schema.tables 
                        WHERE table_name = %s
                    );
                """, (table_name,))
                
                # If the table exists, do nothing
                if cursor.fetchone()[0]:
                    print(f"Table '{table_name}' already exists.")
                    return
                
                # Otherwise, create the table
                columns = ", ".join(
                    f"{key} {cls.get_postgresql_type(value)}" for key, value in data.items()
                )
                
                create_table_query = sql.SQL("CREATE TABLE {} ({})").format(
                    sql.Identifier(table_name),
                    sql.SQL(columns)
                )
                
                cursor.execute(create_table_query)
                conn.commit()
                print(f"Table '{table_name}' created successfully.")
        
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            # Close the connection
            conn.close()
            print("Database connection closed.")
    @staticmethod
    def serialize_value(value):
        """
        Serialize Python objects, lists, and dictionaries for insertion into PostgreSQL.
        """
        if isinstance(value, (list, dict)) or hasattr(value, "__dict__"):
            return json.dumps(value, default=lambda o: o.__dict__)  # Convert to JSON
        return value  # Return the original value for simple types
    
    @classmethod
    def insertData(cls, table_name, data):
        try:
            # Ensure the table exists
            cls.createTable(table_name, data)

            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**cls.DB_SERVER_CONFIG)
            cursor = connection.cursor()

            # Serialize complex values in the dictionary
            serialized_data = {key: cls.serialize_value(value) for key, value in data.items()}

            # Build the SQL query dynamically
            columns = serialized_data.keys()
            values = serialized_data.values()

            query = f"""
                INSERT INTO \"{table_name}\" ({', '.join(columns)})
                VALUES ({', '.join(['%s'] * len(values))})
            """

            print(query)
            print(tuple(values))
            newVals = tuple(val[:255] for val in tuple(values))
            # Execute the query with values
            cursor.execute(query, newVals)
            connection.commit()
            print("Data inserted successfully!")

        except Exception as e:
            print("Error:", e)

        finally:
            if connection:
                cursor.close()
                connection.close()

    @classmethod
    def custom_command(cls, query):
        try:
            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**cls.DB_SERVER_CONFIG)
            cursor = connection.cursor()


            # Execute the query with values
            cursor.execute(query)
            connection.commit()

            # Fetch all results
            rows = cursor.fetchall()
            # Print the results
            print(rows)
            for row in rows:
                print(row)

        except Exception as e:
            print("Error:", e)

        finally:
            if connection:
                cursor.close()
                connection.close()
