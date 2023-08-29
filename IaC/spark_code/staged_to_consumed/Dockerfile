FROM python:3.8 
ARG HADOOP_VERSION=3.2.2 
ARG AWS_SDK_VERSION=1.11.563 

RUN apt install tar gzip

RUN curl -LO https://corretto.aws/downloads/latest/amazon-corretto-11-x64-linux-jdk.tar.gz 
RUN mkdir /usr/java 
RUN tar -xvzf amazon-corretto-11-x64-linux-jdk.tar.gz 
RUN mv amazon-corretto-*.1-linux-x64 /usr/java/ 
RUN ln -s /usr/java/amazon-corretto-*.1-linux-x64/bin/java /usr/bin/java #configs env vars java

ENV JAVA_HOME="/usr/java/amazon-corretto-*.1-linux-x64/bin/"
ENV PATH=${PATH}:${JAVA_HOME}/bin 

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone 

RUN pip3 install pyspark 

#configs env vars spark
ENV SPARK_HOME="/usr/local/lib/python3.8/site-packages/pyspark"
ENV PATH=$PATH:$SPARK_HOME/bin 
ENV PATH=$PATH:$SPARK_HOME/sbin 
ENV PYTHONPATH=$SPARK_HOME/python:$SPARK_HOME/python/lib/*:$PYTHONPATH 
ENV PATH=$SPARK_HOME/python:/home/ubuntu/*:$PATH 
ENV SPARK_LOCAL_IP='127.0.0.1'

RUN mkdir $SPARK_HOME/conf 

RUN echo "SPARK_DIST_CLASSPATH=/opt/spark/jars:/opt/hadoop/etc/hadoop:/opt/hadoop/share/hadoop/common/lib/*:/opt/hadoop/share/hadoop/common/*:/opt/hadoop/share/hadoop/hdfs:/opt/hadoop/share/hadoop/hdfs/lib/*:/opt/hadoop/share/hadoop/hdfs/*:/opt/hadoop/share/hadoop/yarn/lib/*:/opt/hadoop/share/hadoop/yarn/*:/opt/hadoop/share/hadoop/mapreduce/lib/*:/opt/hadoop/share/hadoop/mapreduce/*:/opt/hadoop/contrib/capacity-scheduler/*.jar:/opt/hadoop/share/hadoop/tools/lib/*" > $SPARK_HOME/conf/spark-env.sh 

# copy hadoop-aws and aws-sdk
RUN wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/${HADOOP_VERSION}/hadoop-aws-${HADOOP_VERSION}.jar -P ${SPARK_HOME}/jars/ && \ 
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/${AWS_SDK_VERSION}/aws-java-sdk-bundle-${AWS_SDK_VERSION}.jar -P ${SPARK_HOME}jars/ 

RUN touch $SPARK_HOME/bin/spark-class 
RUN echo "#!/usr/bin/env bash" > $SPARK_HOME/bin/spark-class 
RUN echo 'exec /usr/java/amazon-corretto-*.1-linux-x64/bin/java -cp /usr/local/lib/python3.8/site-packages/pyspark/conf/:/usr/local/lib/python3.8/site-packages/pyspark/jars/* -Xmx10g "$@"' >> $SPARK_HOME/bin/spark-class 
RUN chmod -R 777 $SPARK_HOME/bin/spark-class 

COPY jars/* ${SPARK_HOME}/jars/ 
COPY requirements.txt /opt/requirements.txt

################################################################################################
COPY . /opt/app

RUN pip3 install -r /opt/requirements.txt
ENV PATH="/opt/program:${PATH}"

WORKDIR /opt/app
ENTRYPOINT ["python", "stage-consumed.py"] 