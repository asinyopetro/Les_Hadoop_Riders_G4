#!/bin/bash
# Manipulations HDFS — Partie 2.B (à exécuter dans hadoop-master)
set -e

echo "=== 1) Creation arborescence /data/ventes/2026 ==="
hdfs dfs -mkdir -p /data/ventes/2026

echo "=== 2) Upload transactions.csv ==="
hdfs dfs -put -f /data/transactions.csv /data/ventes/2026/

echo "=== 3) Verification blocs / replication (fsck) ==="
hdfs fsck /data/ventes/2026/transactions.csv -files -blocks -locations

echo "=== 4) Stat du fichier ==="
hdfs dfs -stat "%n | taille=%b | replication=%r | block_size=%o" /data/ventes/2026/transactions.csv

echo "=== 5) 5 premieres lignes depuis HDFS ==="
hdfs dfs -cat /data/ventes/2026/transactions.csv | head -n 5

echo "=== 6) Upload part2 + getmerge ==="
hdfs dfs -put -f /data/transactions_part2.csv /data/ventes/2026/
hdfs dfs -getmerge /data/ventes/2026 /tmp/transactions_merged.csv
echo "--- Contenu merge (local /tmp) ---"
cat /tmp/transactions_merged.csv
hdfs dfs -put -f /tmp/transactions_merged.csv /data/ventes/2026/transactions_merged.csv

echo "=== 7) Suppression + corbeille ==="
hdfs dfs -rm /data/ventes/2026/transactions_part2.csv
echo "Contenu .Trash :"
hdfs dfs -ls -R /user/root/.Trash || hdfs dfs -ls -R /.Trash || echo "(corbeille selon config)"

echo "=== 8) setrep a 2 ==="
hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv
hdfs dfs -stat "replication=%r" /data/ventes/2026/transactions.csv

echo "=== Demo HDFS terminee ==="
