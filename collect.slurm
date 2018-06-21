#!/bin/bash -l

#find /tmp -type f -print | xargs -- rm -f --
rm -f /tmp/${USER}/*

echo collected files:
gsutil ls -l gs://risk-vardemo1
