#!/bin/bash

for i in a b c d e f; do
    python3 problem.py ../data/$i.in &
done
wait
