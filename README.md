# dbf_to_sql

## Script to Migrate DBF DataBases to SQL DataBases


The principal file is "migrate_dbf.py". You just need to change the files name in the code and then run it, this will make a txt file where will be the log (in Spanish) detailing the time for each table dbf. We tested the script with a dbf file with 2GB of size and the time was of 30 minutes around.

If you need to run the script in second plan, you can configure the file_watcher.py script as task in second plan (In case of Windows, in linux as Demon). This script runs automatic each 5 minutes but you can change the time like you need.

If you need to make changes in the database after to upload the tables, you can use edit_table.py to specify the change you need to do in the table SQL.

The migrations won't be saved in your computer, or in a local file, this script upload in automatic way the tables to the database SQL, so, you need to change the parameter in migrate_dbf.py and in edit_table.py:
### Configure MySQL
```
    mysql_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'laravel11crud'
    }
```
