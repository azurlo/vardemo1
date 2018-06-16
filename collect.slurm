#!/usr/bin/env bash
echo collec -r gs://risk-vardemo1
#find /tmp -type f -print | xargs -- rm -f --
rm -f /tmp/*
gsutil ls -r gs://risk-vardemo1
