#!/bin/bash
echo "show tables"|mysql -upact -ppact pact|sed 1d|awk '{print "drop table "$1 ";"}'|mysql -upact -ppact pact
mysql -upact -ppact pact < mysql.def
