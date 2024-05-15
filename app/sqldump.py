#!/usr/bin/env python3

import os
import subprocess

class DumpCleanUp:

    def __init__(self, filename, db_name, full_path) -> None:
        self.filename = filename
        self.db_path = full_path
        self.db_name = db_name
        self.copy_data
        self.cleanup

    @property
    def copy_data(self):
        try:
            self.path = os.path.join(self.db_path, "temp")
            os.makedirs(self.path, exist_ok=True) # Creates a temp folder in Desktop
            command = f'cp {self.db_path}/{self.filename} {self.path}/{self.db_name}.sql'
            subprocess.run(command, shell=True, check=True)
            self.fullpath = os.path.join(self.path, self.db_name + ".sql")
        except Exception as e:
            print(f"** ERROR WHILE MAKING A COPY OF {self.db_name} TO TEMP FOLDER **")

    @property
    def cleanup(self):
        try:
            commands = f"""
            sed -i 's-\/\*[!]*\*\/--g' {self.fullpath};
            sed -i 's/--.*//g' {self.fullpath};
            sed -i 's/CREATE DATABASE [^;]*[;]*//g' {self.fullpath};
            sed -i 's/DROP DATABASE [^;]*[;]*//g' {self.fullpath};
            sed -i 's/USE [^;]*[;]*//g' {self.fullpath};
            sed -i 's/CREATE USER [^;]*[;]*//g' {self.fullpath};
            sed -i 's/CREATE LOGIN [^;]*[;]*//g' {self.fullpath};
            sed -i 's/GRANT [^;]*[;]*//g' {self.fullpath};
            perl -pi -e 's/\\\\c [^;]*[;]*//g' {self.fullpath};
            sed -i 's/^[\/]*SET [^;]*[;]*//g' {self.fullpath};
            sed -i 's/BEGIN [^;]*[;]*//g' {self.fullpath};
            sed -i 's/COMMIT[^;]*[;]*//g' {self.fullpath};
            """
            subprocess.run(commands, shell=True, check=True)
        except Exception as e:
            print("** FILE DOES NOT EXISTS **")
            return None

    def dump_data(self, db_engine):
        rdbms = {
            "mysql+mysqldb": f"""
            echo 'DROP DATABASE IF EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};
            echo 'CREATE DATABASE IF NOT EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};
            cat {self.fullpath} | mysql -p{os.getenv("SECRET_KEY")} {self.db_name};
            """,
            "postgresql": f"""
            echo 'DROP DATABASE {self.db_name}' | psql;
            echo 'CREATE DATABASE {self.db_name}' | psql;
            cat {self.fullpath} | psql -d {self.db_name};
            """
            # rm -r {self.path};
        }
        if db_engine:
            database = {
                "MySQL": "mysql+mysqldb",
                "MariaDB": "mysql+mysqldb",
                "PostgreSQL": "postgresql",
                "Microsoft SQL Server": "microsoft"
            }
            fmts = database[db_engine]
            try:
                subprocess.check_output(rdbms[fmts], shell=True, stderr=subprocess.STDOUT)
                return fmts
            except subprocess.CalledProcessError as e:
                print("--------EXCEPT CALLED-------------")
                print("The formats Given is: ", fmts)
                print("--------EXCEPT CALLED-------------")
                pass

        for fmts in rdbms.keys():
            try:
                subprocess.check_output(rdbms[fmts], shell=True, stderr=subprocess.STDOUT)
                return fmts
            except subprocess.CalledProcessError as e:
                print("--------EXCEPT CALLED-------------")
                print("The formats Called is: ", fmts)
                print("--------EXCEPT CALLED-------------")
                pass

        return None
