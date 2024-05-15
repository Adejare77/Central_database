#!/usr/bin/env bash
sed -i 's/\bCREATE DATABASE [^;]*\b//g' /home/adejare77/Desktop/central_db/test/temp/test_rashisky.sql

sed -i 's/\bUSE [^;]*\b//g' /home/adejare77/Desktop/central_db/test/temp/test_rashisky.sql

sed -i 's/\CREATE USER [^;]*\b//g' /home/adejare77/Desktop/central_db/test/temp/test_rashisky.sql

sed -i 's/\CREATE LOGIN [^;]*\b//g' /home/adejare77/Desktop/central_db/test/temp/test_rashisky.sql

sed -i 's/\GRANT [^;]*\b//g' /home/adejare77/Desktop/central_db/test/temp/test_rashisky.sql

sed -i 's/\SET [^;]*\b//g' /home/adejare77/Desktop/central_db/test/temp/test_rashisky.sql

