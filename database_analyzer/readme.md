## Database Analyzer

This script analyzes two database files and compares their database structures. Then, it prints the difference between database.db and database_correct.db.

To use just put the database_correct.db and database.db at the project folder.

# Output examples:

:right Databases are structurally equals:
'''
- Database automacao.db is struturally correct!
'''

:error Databases aren't structurally equals:
'''
- Database automacao.db has structural issues:
[TABLE MISSING] table [teste_4] exists in correct db but not in the other db file
[COLUMN MISMATCH] table [sensors] column [address] differs:
  correct db: {'type': 'INT', 'notnull': 0, 'default': '0', 'primary_key': 0}
  automacao.db: {'type': 'INT', 'notnull': 1, 'default': '0', 'primary_key': 0}
'''