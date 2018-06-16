#!/bin/bash -l

#find /tmp -type f -print | xargs -- rm -f --
rm -f /tmp/*

echo collected files:
gsutil ls -r gs://risk-vardemo1
