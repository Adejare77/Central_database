#!/usr/bin/env python3
"""Cleaning sqldump files"""
import os
import subprocess
import shutil
from app import sqlite_path


class DumpCleanUp:
    """Clean the SQL dump uploaded for Processing"""
    def __init__(self, filename, db_name, full_path) -> None:
        """Initializes the filenmae, database name and full path

        Args:
            filename (str): Actual database name given by user
            db_name (str): Database name used for storage
            full_path (str): path to the stored uploaded sqldump
        """
        self.filename = filename
        self.db_path = full_path
        self.db_name = db_name
        self.fullpath = self.copy_data
        self.cleanup

    @property
    def copy_data(self):
        """Copies original sqldump file for cleaning purpose"""
        try:
            self.path = os.path.join(self.db_path, "temp")
            # Creates a temp folder in Desktop
            os.makedirs(self.path, exist_ok=True)
            command = f"""
            cp {self.db_path}/{self.filename}.sql {self.path}/{self.db_name}.sql
            """
            subprocess.run(command, shell=True, check=True)
            fullpath = os.path.join(self.path, self.db_name + ".sql")
            return fullpath

        except Exception as e:
            print(f"** ERROR WHILE MAKING A COPY OF \
                  {self.db_name} TO TEMP FOLDER **")

    @property
    def cleanup(self):
        """cleans the copied sqldump file"""
        try:
            # Bash commands for cleaning sqldump files
            commands = f"""
            sed -i 's-\/\*[!]*\*\/--g' {self.fullpath};
            sed -i 's/--.*//g' {self.fullpath};
            sed -i 's/CREATE DATABASE [^;]*[;]*//g' {self.fullpath};
            sed -i 's/DROP [^;]*[;]*//g' {self.fullpath};
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
        """
        Try different DBMS to use for the sqldump file if db_engine is None.
        Else use the DBMS provided by the user.
        """
        rdbms = {
            "MySQL": "mysql+mysqldb",
            "MariaDB": "mysql+mysqldb",
            "PostgreSQL": "postgresql",
            "SQLite": "sqlite"
            }
        if db_engine:
            try:
                output = subprocess.run(
                    self.db_engine(rdbms[db_engine], "Create"), shell=True, check=True,
                    capture_output=True, text=True)
                return rdbms[db_engine]
            except subprocess.CalledProcessError as e:
                error = "** SUBPROCESS ERROR **"
                print("===========", error, "============")
                subprocess.run(self.db_engine(rdbms[db_engine], "Delete"),
                               shell=True, check=True)

            except Exception as e:
                error = "** EXCEPTION ERROR  **"
                print("===========", error, "============")
                subprocess.run(self.db_engine(rdbms[db_engine], "Delete"),
                               shell=True, check=True)


        # rdbms = ["postgresql", "mysql+mysqldb"]
        rdbms = ["mysql+mysqldb", "postgresql"]

        for fmts in rdbms:
            try:
                output = subprocess.run(
                    self.db_engine(fmts, "Create"), shell=True, check=True,
                    capture_output=True, text=True)
                return fmts
            except subprocess.CalledProcessError as e:
                error = "** SUBPROCESS ERROR **"
                print("===========", error, "============")
                subprocess.run(self.db_engine(fmts, "Delete"),
                               shell=True, check=True)

            except Exception as e:
                error = "** EXCEPTION ERROR  **"
                print("===========", error, "============")
                subprocess.run(self.db_engine(fmts, "Delete"),
                               shell=True, check=True)
        return None

    def db_engine(self, fmt, action):
        filename = self.db_name[self.db_name.find("_")+1:]
        username = self.db_name[: self.db_name.find("_")]
        engines = {
              "mysql+mysqldb": {
                  "Create": f"""
                  echo 'DROP DATABASE IF EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};
                  echo 'CREATE DATABASE IF NOT EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};
                  cat {self.fullpath} | mysql -p{os.getenv("SECRET_KEY")} {self.db_name};
                  """,
                  "Delete": f"""
                  echo 'DROP DATABASE IF EXISTS `{self.db_name}`' | mysql -p{os.getenv("SECRET_KEY")};"""
                  },
              "postgresql": {
                  "Create": f"""
                  echo 'CREATE DATABASE {self.db_name}' | psql -U {os.getenv("USER")} -d central_db;
                  psql -U {os.getenv("USER")} -d {self.db_name} -f {self.fullpath};
                  """,
                  "Delete": f"""
                  echo 'DROP DATABASE {self.db_name}' | psql -U {os.getenv("USER")} -d central_db;"""
                  },
              "sqlite": {
                  "Create": f"""
                  mkdir -p {sqlite_path}/{username};
                  sqlite3 {sqlite_path}/{username}/{filename}.db < {self.fullpath};
                  """,
                  "Delete": f"""
                  if [ -e "{sqlite_path}/{username}/{filename}.db" ]; then
                  rm -r {sqlite_path}/{username}/{filename}.db;
                  fi
                """
                  }
        }
        return engines[fmt][action]
