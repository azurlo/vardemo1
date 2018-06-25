#! /bin/bash
# script that initiates the random walk.
# takes one argument which is the index into the sp500.csv to
# identify which stock to simulate.
#
# June 20, 1018
index=$(($1 + 1))
stockfile=companies.csv
stock=$(awk "NR == ${index} {print; exit}" ${stockfile} | cut -d, -f1)
echo "index = ${index}, stock = ${stock}"
./randomwalk.py -c ${stock}
~                           
