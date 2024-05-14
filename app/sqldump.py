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
            sed -i 's/CREATE DATABASE [^;]*//g' {self.fullpath};
            sed -i 's/DROP DATABASE [^;]*//g' {self.fullpath};
            sed -i 's/USE [^;]*//g' {self.fullpath};
            sed -i 's/CREATE USER [^;]*//g' {self.fullpath};
            sed -i 's/CREATE LOGIN [^;]*//g' {self.fullpath};
            sed -i 's/GRANT [^;]*//g' "$1";
            sed -i 's/^[\/]*SET [^;]*//g' {self.fullpath};
            """
            subprocess.run(commands, shell=True, check=True)
        except Exception as e:
            print("** FILE DOES NOT EXISTS **")
            return None

    @property
    def dump_data(self):
        rdbms = {
            "mysql+mysqldb": f"""
            echo 'DROP DATABASE IF EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};
            echo 'CREATE DATABASE IF NOT EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};
            cat {self.fullpath} | mysql -p{os.getenv("SECRET_KEY")} {self.db_name};
            rm -r {self.path};
            """,
            "postgresql": f"""
            echo 'DROP DATABASE {self.db_name}' | psql;
            echo 'CREATE DATABASE {self.db_name}' | psql;
            cat {self.fullpath} | psql;
            rm -r {self.path};
            """
        }
        for fmts in rdbms.keys():
            try:
                subprocess.run(rdbms[fmts], shell=True, check=True)
                return fmts
            except Exception as e:
                print(f'** ERROR WHILE USING "{fmts}" ON {self.db_name} DUMP FILE **')
                pass
        return None
