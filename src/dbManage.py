# PostgreSQL Database Integration with Python 3
from dataclasses import asdict, fields
import psycopg2
from psycopg2 import sql
import json

from dataFormat import Effect, Item, DEFAULT_DATA_SNAP


# TODO SPEED OPTIMIZATION -- DO THIS ONCE DB ISSUES ARE FULLY RESOLVED
"""
    TODO KEEP CONNECTION LIVE
    TODO BATCH DATABASE WRITES TO SAVE ON LATENCY

"""
class Database:

    DB_NAME = "playerData"
    #PosrgeSQL Server Connection Settings
    APP_DB_CONFIG = {
        "host": "localhost",
        "database":  DB_NAME,
        "user": "postgres",
        "password": "Faiz256",
        "port": "5432"
    }

    MASTER_DB_CONFIG = {
        "host": "localhost",
        "database":  "postgres",
        "user": "postgres",
        "password": "Faiz256",
        "port": "5432"
    }

    DEFAULT_DDATAFRAME = None # convert_dataframe_to_ddataframe(DEFAULT_DATA_SNAP)
    
    # Create Database

    @classmethod
    def create_database(cls):
        connection = None
        try:
            # Connect to the PostgreSQL server (not a specific database yet)
            connection = psycopg2.connect(**cls.MASTER_DB_CONFIG)
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

            cursor.execute( f"GRANT ALL PRIVILEGES ON DATABASE \"{cls.DB_NAME}\" TO { (cls.APP_DB_CONFIG.get('user')) };" )

        except Exception as e:
            print("Error while creating the database:", e)
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
        
    # change data is a dict with key:value pairs
    @classmethod
    def create_table(cls, table_name, data):
        """
        Ensures the table exists in the PostgreSQL database.
        If the table does not exist, it is created based on the provided data (dict).
        If the table already exists, the function does nothing.
        
        Args:
        - table_name: Name of the table to check/create.
        - data: Dictionary containing the column names and sample data types for the table.
        """
        conn = None
        # Create a connection to the PostgreSQL database
        try:
            conn = psycopg2.connect(**cls.APP_DB_CONFIG)
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
                """, (table_name, ))
                
                # If the table exists, do nothing
                if cursor.fetchone()[0]:
                    print(f"Table '{table_name}' already exists.")
                    return
                
                # Otherwise, create the table
                columns = ", ".join(
                    f"{key} {cls.get_postgresql_type(value)}" for key, value in data.items()
                )

                columns = "id SERIAL PRIMARY KEY, " + columns
                
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
        if isinstance(value, (list, dict, tuple)) or hasattr(value, "__dict__"):
            return json.dumps(value, default=lambda o: o.__dict__)  # Convert to JSON
        return value  # Return the original value for simple types
    
    @classmethod
    def serialize_multiple_values(cls, values):
        return [cls.serialize_value(val) for val in values]
    
    # creates  ddataframe (database dataframe) => tuple(DATA, [EFFECT], [ITEM]) from a Dataframe Object
    @classmethod
    def convert_dataframe_to_ddataframe(cls, dataframe):
        #assume dataframe is a Dataframe Object
        #print("start")
        datadict = asdict(dataframe)
        itemList = []# list of dicts
        effectList = []


        for idx, invItem in enumerate(dataframe.plyrInventory):
            #print(invItem)
            itemDict: dict = asdict(invItem)
            #itemDict["idx"] = idx ##TODO
            itemList.append(itemDict)
        else:
            datadict.pop("plyrInventory")
        #do same for armor and offhand, can either continue incrementing idx, or we can create a "source" column for which type of inv this is from
        datadict.pop("plyrArmor") # just discard for now
        datadict.pop("plyrOffhand")
        
        for effect in dataframe.plyrStatus:
            effectDict: dict = asdict(effect)
            #effectDict["data_id"] = idx
            effectList.append(effectDict)
        else:
            datadict.pop("plyrStatus")
        return (datadict, itemList, effectList)
    

    #assumes dataframe
    # separate out schema creation
    # accepts ddataframe (database dataframe) => tuple(DATA, [EFFECT], [ITEM])
    @classmethod
    def save_ddataframe(cls, data):
        #table_name = ""
        connection = None
        try:
            #split dataframe into three separate dicts
            #print("Happens Here 1")
            # Ensure the table exists
            if cls.DEFAULT_DDATAFRAME is None: #only runs once
                cls.DEFAULT_DDATAFRAME = cls.convert_dataframe_to_ddataframe(DEFAULT_DATA_SNAP)
                cls.create_table("DATA", cls.DEFAULT_DDATAFRAME[0]) #really silly to create every single time, but i digress
                itemtabledata = cls.DEFAULT_DDATAFRAME[1][0]
                itemtabledata["data_id"] = 0
                effecttabledata = cls.DEFAULT_DDATAFRAME[2][0].copy()
                effecttabledata["data_id"] = 0
                cls.create_table("ITEMS", itemtabledata) #really silly to create every single time, but i digress
                cls.create_table("EFFECTS", effecttabledata) #really silly to create every single time, but i digress


            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**cls.APP_DB_CONFIG)
            cursor = connection.cursor()

            # Serialize complex values in the dictionary
            serialized_data = {key: cls.serialize_value(value) for key, value in data[0].items()}

            # Build the SQL query dynamically
            columnsData, valuesData = (serialized_data.keys(), serialized_data.values())
            columnsItems = [field.name for field in fields(Item)] + ["data_id"]
            columnsEffects = [field.name for field in fields(Effect)]+ ["data_id"]

            queryDATA = f"""
                INSERT INTO \"{"DATA"}\" ({', '.join(columnsData)})
                VALUES ({', '.join(['%s'] * len(valuesData))})
                RETURNING id
            """

            queryITEMS = f"""
                INSERT INTO \"{"ITEMS"}\" ({', '.join(columnsItems)})
                VALUES ({', '.join(['%s'] * len(columnsItems))})
            """

            queryEFFECTS = f"""
                INSERT INTO \"{"EFFECTS"}\" ({', '.join(columnsEffects)})
                VALUES ({', '.join(['%s'] * len(columnsEffects))})
            """

            #print(query)
            #print(tuple(values))
            #newVals = tuple( val[:255]   for val in tuple(values))

            # Execute the query with values
            print("start")
            print(valuesData)
            print(cls.serialize_multiple_values(valuesData))
            cursor.execute(queryDATA, cls.serialize_multiple_values(valuesData))
            connection.commit()
            print("stop")

            # get data table id with sql query
            #print("Happens Here 3")
            inserted_data_id = str(cursor.fetchone()[0])
            #print("initdone", inserted_data_id)

            for item in data[1]:
                #print(queryITEMS)
                #print(tuple(item.values()) + tuple(inserted_data_id, ))
                l = cls.serialize_multiple_values(item.values())
                l.append(inserted_data_id)
                cursor.execute(queryITEMS, l)
            #print("Happens Here 4")
            for effect in data[2]:
                l = cls.serialize_multiple_values(effect.values())
                l.append(inserted_data_id)
                cursor.execute(queryEFFECTS, l)
            connection.commit()
            #print("Data inserted successfully!")

        except Exception as e:
            print("Error:", e)

        finally:
            if connection:
                cursor.close()
                connection.close()

    @classmethod
    def custom_command(cls, query):
        connection = None
        try:
            # Connect to the PostgreSQL database
            connection = psycopg2.connect(**cls.APP_DB_CONFIG)
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
