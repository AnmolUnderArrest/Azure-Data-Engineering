# Databricks notebook source
# MAGIC %run "/DataBricksMasterClass/masterclass_tutorial"

# COMMAND ----------

# MAGIC %md
# MAGIC # Delta Lake

# COMMAND ----------

#write df_sales data from source to destination container
df_sales.write.format('parquet')\
        .mode('append')\
        .option('path','abfss://destination@storagedatabricksanmo.dfs.core.windows.net/sales')\
        .save()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Managed Table vs External Table

# COMMAND ----------

# MAGIC %sql
# MAGIC create database salesDB;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Managed table

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE salesDB.mantable  
# MAGIC (
# MAGIC   id INT,
# MAGIC   name STRING,
# MAGIC   marks INT
# MAGIC )
# MAGIC USING DELTA  

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO salesDB.mantable 
# MAGIC VALUES
# MAGIC (1,'sam',50),
# MAGIC (2,'bob',63),
# MAGIC (3,'connie',45),
# MAGIC (4,'Derick',40)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesDB.mantable

# COMMAND ----------

# MAGIC %sql
# MAGIC drop table salesDB.mantable

# COMMAND ----------

# MAGIC %md
# MAGIC ### External Table
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE salesDB.exttable  
# MAGIC (
# MAGIC   id INT,
# MAGIC   name STRING,
# MAGIC   marks INT 
# MAGIC )
# MAGIC USING DELTA    
# MAGIC LOCATION 'abfss://destination@storagedatabricksanmo.dfs.core.windows.net/salesDB/exttable'

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO salesDB.exttable 
# MAGIC VALUES
# MAGIC (1,'aa',30),
# MAGIC (2,'bb',33),
# MAGIC (3,'cc',35),
# MAGIC (4,'DD',40)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesDb.exttable

# COMMAND ----------

# MAGIC %md
# MAGIC ### Delta Table Functionalities

# COMMAND ----------

# MAGIC %md
# MAGIC ### insert

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO salesDB.exttable 
# MAGIC VALUES
# MAGIC (5,'aloo',30),
# MAGIC (6,'baigan',33),
# MAGIC (7,'cauliflower',35),
# MAGIC (8,'dry chana',40)

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesdb.exttable order by id asc

# COMMAND ----------

# MAGIC %md
# MAGIC ### Delete

# COMMAND ----------

# DBTITLE 1,Cell 20
# MAGIC %sql
# MAGIC delete from salesdb.exttable   where id=8

# COMMAND ----------

# MAGIC %md
# MAGIC ### Data Versioning

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY salesdb.exttable;  

# COMMAND ----------

# MAGIC %md
# MAGIC ### Time Travel

# COMMAND ----------

# MAGIC %sql
# MAGIC RESTORE TABLE salesdb.exttable TO VERSION AS OF 2;

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesDB.exttable order by id asc

# COMMAND ----------

# MAGIC %md
# MAGIC ## Delta Table Optimization

# COMMAND ----------

# MAGIC %md
# MAGIC **Optimize**

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE salesDB.exttable

# COMMAND ----------

# MAGIC %sql
# MAGIC select * from salesdb.exttable

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE salesdb.exttable ZORDER BY (id)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Auto Loader

# COMMAND ----------

# MAGIC %md
# MAGIC **Streaming dataframe**

# COMMAND ----------

df = spark.readStream.format('cloudFiles')\
        .option('cloudFiles.format','parquet')\
        .option('cloudFiles.schemaLocation','abfss://autoloader-destination@storagedatabricksanmo.dfs.core.windows.net/checkpoint')\
        .load('abfss://autoloader-source@storagedatabricksanmo.dfs.core.windows.net')  

# COMMAND ----------

spark.conf.unset("fs.azure.account.key.storagedatabricksanmo.dfs.core.windows.net")

# COMMAND ----------

df.writeStream.format('delta')\
               .option('checkpointLocation','abfss://autoloader-destination@storagedatabricksanmo.dfs.core.windows.net/checkpoint')\
               .option('mergeSchema','True')\
               .trigger(processingTime='10 seconds')\
               .start('abfss://autoloader-destination@storagedatabricksanmo.dfs.core.windows.net/data')

# COMMAND ----------

