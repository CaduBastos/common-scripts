import sqlite3

def get_tables(db_path):                    # db path as parameter
   
    with sqlite3.connect(db_path) as conn:  # guarantees closing the connection
        cursor = conn.cursor()              # create a cursor object    
        cursor.execute("""
            SELECT name 
            FROM sqlite_master 
            WHERE type='table' 
            AND name NOT LIKE 'sqlite_%';
            """)
        return {row[0] for row in cursor.fetchall()}  # fetch all results
    
def get_columns(db_path, table_name):       # db path and table name as parameters
    
    with sqlite3.connect(db_path) as conn:  # guarantees closing the connection
        cursor = conn.cursor()              # create a cursor object    
        cursor.execute(f"PRAGMA table_info({table_name});")
        return {                            # get content of table_info and sort it
              row[1]: { # column name
                  "type": row[2],
                  "notnull": row[3],
                  "default": row[4],
                  "primary_key": row[5]
              }
              for row in cursor.fetchall()  # fetch all results
        }
    
def compare_schemas(db_ri, db_an):
   
    report = []

    tables_ri = get_tables(db_ri)
    tables_an = get_tables(db_an)

    # check tables missing or extra
    for table in tables_ri - tables_an: 
        report.append(f"[TABLE MISSING] table [{table}] exists in correct db but not in the other db file")
        
    for table in tables_an - tables_ri: 
        report.append(f"[EXTRA TABLE] table [{table}] exists in the other db file but not in correct db")

    # check columns in common
    for table in tables_ri & tables_an:
        columns_ri = get_columns(db_ri, table)
        columns_an = get_columns(db_an, table)

        # check columns missing or extra
        for col in columns_ri.keys() - columns_an.keys():
            report.append(f"[COLUMN MISSING] table [{table}] column [{col}] exists in correct db but not in automacao.db")

        for col in columns_an.keys() - columns_ri.keys():
            report.append(f"[EXTRA COLUMN] table [{table}] column [{col}] exists in automacao.db but not in correct db")

        # check columns
        for col in columns_ri.keys() & columns_an.keys():
            ri = columns_ri[col]
            an = columns_an[col]

            if ri != an:
                report.append(
                    f"[COLUMN MISMATCH] table [{table}] column [{col}] differs:\n"
                    f"  correct db: {ri}\n"
                    f"  automacao.db: {an}"
                ) 
             
    return report

#######################################################################

if __name__ == "__main__":
    try:
        db_analyze = compare_schemas('database_correct.db', 'database.db')
    except Exception as err:
        print(f"Error analyzing database: {err}")
        db_analyze = ["Error during analysis."]

    if not db_analyze:
        print("Database database.db is struturally correct!")
    else:
        print("Database database.db has structural issues:")
        for issue in db_analyze:
            print(issue)
    input("\nPress Enter to exit...")