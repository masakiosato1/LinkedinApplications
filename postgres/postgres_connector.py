import psycopg2

class postgres_connector:
    def __init__(self):
        pass





    #database functions
    def connect_to_db(self, database_dictionary):
        self.conn = psycopg2.connect(
            host=database_dictionary['host'],
            database=database_dictionary['database'],
            user=database_dictionary['user'],
            password=database_dictionary['password']
            )


    #table reading functions
    def get_columns(self, table_name):
        with self.conn.cursor() as curs:
            try:
                curs.execute(f"Select * FROM {table_name} LIMIT 0")
                colnames = [desc[0] for desc in curs.description]
                print("done")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            curs.close()
        return colnames



    #table writing functinos
    def create_table_command(self, table_dictionary):
        table_name = table_dictionary['table_name']
        column_names = table_dictionary['column_names']
        column_types = table_dictionary['column_types']
        column_conditions = table_dictionary['column_conditions']
        
        if len(column_names) != len(column_types):
            print("column_names and column_types are not of equal length")
            return ""
        command = f'''
        CREATE TABLE {table_name} ( '''
        for i in range(len(column_names)):
            if i > 0:
                command += ", "
            command += f"{column_names[i]} {column_types[i]} {column_conditions[i]}"
        command += " )"
        
        return command


    def insert_table_command(self, table_dictionary):
        table_name = table_dictionary['table_name']
        column_names = table_dictionary['column_names']
        #column_types = table_dictionary['column_types']
        
        command = f'''INSERT INTO {table_name} ('''
        for i in range(len(column_names)):
            if i > 0:
                command += ", "
            command += column_names[i]
        command += ") VALUES ("
        for i in range(len(column_names)):
            if i > 0:
                command += ", "
            command += "%s"
        command += ")"
        return command
        

    def insert_data(self, output_db_dict, output_table_dict, data):
        self.connect_to_db(output_db_dict)
        #create table
        with self.conn.cursor() as curs:
            try:
                curs.execute(self.create_table_command(output_table_dict))
                print("Created Table")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            self.conn.commit()
            curs.close()

        self.connect_to_db(output_db_dict)
        with self.conn.cursor() as curs:
            #insert data into table
            try:
                curs.executemany(self.insert_table_command(output_table_dict), data)
                print("Inserted Data")
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
            self.conn.commit()
            curs.close()

    def get_data(self, db_dict, query):
        self.connect_to_db(db_dict)
        with self.conn.cursor() as curs:
            try:
                curs.execute(query)
                data = curs.fetchall()
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                return []
            self.conn.commit()
            curs.close()
        return data