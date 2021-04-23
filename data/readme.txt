Data Loading:
    Step1: Install MySql
    TODO: Step2: Set up password - encrypt the passoword and feed it to the backend server (/website/flaskapp.py)
    Step3: Load the data using the following commands:
        Creacte Backup (if not created earlier): mysqldump -u root -p movies > movies_dump_20170530.sql
        Create DB: create database movies;
        Load Backup: mysql -u root -p movies < movies_dump_20170530.sql
