#!/bin/bash
# Job YARN — calcul de pi (Monte Carlo)
set -e

echo "=== Soumission du job pi (4 maps, 1000 samples/map) ==="
yarn jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.3.6.jar pi 4 1000

echo "=== Applications YARN recentes ==="
yarn application -list -appStates ALL | head -n 20

echo "=== Demo YARN pi terminee — verifier http://localhost:8088 ==="
