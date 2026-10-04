FROM apache/hadoop:3.3.6

LABEL maintainer="Les_Hadoop_Riders G4"
LABEL description="Cluster Hadoop HDFS+YARN multi-noeuds pour UA1 Projet 1"

USER root

ENV JAVA_HOME=/usr/lib/jvm/jre-1.8.0-openjdk
ENV HADOOP_HOME=/opt/hadoop
ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh \
    && echo "export HADOOP_HOME=${HADOOP_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh \
    && echo "export HADOOP_CONF_DIR=${HADOOP_CONF_DIR}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

COPY config/ ${HADOOP_HOME}/etc/hadoop/
COPY entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && mkdir -p /opt/hadoop/data/nameNode \
                /opt/hadoop/data/dataNode \
                /opt/hadoop/logs \
                /opt/hadoop/tmp \
                /data \
    && chown -R hadoop:users /opt/hadoop/data /opt/hadoop/logs /opt/hadoop/tmp /data ${HADOOP_HOME}/etc/hadoop \
    && chown hadoop:users /entrypoint.sh

EXPOSE 9870 8088 9000 9864 8042

USER hadoop
ENTRYPOINT ["/entrypoint.sh"]
