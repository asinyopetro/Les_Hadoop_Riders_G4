#!/bin/bash
set -e

ROLE="${HADOOP_ROLE:-master}"
export HADOOP_HOME="${HADOOP_HOME:-/opt/hadoop}"
export HADOOP_CONF_DIR="${HADOOP_CONF_DIR:-/opt/hadoop/etc/hadoop}"
export PATH="$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin"

# JAVA_HOME depuis hadoop-env si besoin
if [ -z "$JAVA_HOME" ]; then
  source "${HADOOP_HOME}/etc/hadoop/hadoop-env.sh" 2>/dev/null || true
fi
if [ -z "$JAVA_HOME" ]; then
  export JAVA_HOME="$(dirname "$(dirname "$(readlink -f "$(command -v java)")")")"
fi

echo "=== Les_Hadoop_Riders G4 | Role: ${ROLE} | Host: $(hostname) ==="

if [ "$ROLE" = "master" ]; then
  if [ ! -d "/opt/hadoop/data/nameNode/current" ]; then
    echo "=== Formatage du NameNode ==="
    hdfs namenode -format -force -nonInteractive
  fi

  echo "=== Demarrage NameNode ==="
  hdfs --daemon start namenode

  echo "=== Demarrage SecondaryNameNode ==="
  hdfs --daemon start secondarynamenode || true

  echo "=== Demarrage ResourceManager ==="
  yarn --daemon start resourcemanager

  echo "=== Master pret (HDFS UI :9870 | YARN UI :8088) ==="
else
  echo "=== Attente du NameNode (hadoop-master:9000) ==="
  for i in $(seq 1 90); do
    if hdfs dfs -ls / >/dev/null 2>&1; then
      echo "=== NameNode joignable ==="
      break
    fi
    sleep 2
  done

  echo "=== Demarrage DataNode ==="
  hdfs --daemon start datanode

  echo "=== Demarrage NodeManager ==="
  yarn --daemon start nodemanager

  echo "=== Worker pret ==="
fi

tail -f /dev/null
