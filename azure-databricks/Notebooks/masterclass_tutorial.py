# Databricks notebook source
# MAGIC %md
# MAGIC #**DataBricks **

# COMMAND ----------



# COMMAND ----------

#creating dataset
mydata = [(1,'aa',30),(2,'bb',40),(3,'cc',50)]

#creating schema
myschema = "id INT, name STRING, marks INT"

#creating customized dataframe
df = spark.createDataFrame(mydata,schema=myschema)
df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC # Access Data

# COMMAND ----------
# tenant_id="39d764db-8d4d-47c8-9502-898a2aa48ba6"

# COMMAND ----------



spark.conf.set("fs.azure.account.auth.type.storagedatabricksanmo.dfs.core.windows.net", "OAuth")
spark.conf.set("fs.azure.account.oauth.provider.type.storagedatabricksanmo.dfs.core.windows.net", "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider")
spark.conf.set("fs.azure.account.oauth2.client.id.storagedatabricksanmo.dfs.core.windows.net", "3e02fc9f-1999-49f2-86df-7699bc8ebe32")
spark.conf.set("fs.azure.account.oauth2.client.secret.storagedatabricksanmo.dfs.core.windows.net", dbutils.secrets.get(scope="anmoscope", key="app-secret"))
spark.conf.set("fs.azure.account.oauth2.client.endpoint.storagedatabricksanmo.dfs.core.windows.net", "https://login.microsoftonline.com/39d764db-8d4d-47c8-9502-898a2aa48ba6/oauth2/token")

# COMMAND ----------

# MAGIC %md
# MAGIC # DataBricks Utilities

# COMMAND ----------

dbutils.fs.ls("abfss://source@storagedatabricksanmo.dfs.core.windows.net/")

# COMMAND ----------

# MAGIC %md
# MAGIC **dbutils.widgets**

# COMMAND ----------

#user has the ability to provide value by creating a parameter
dbutils.widgets.text("p_name","anmol")

# COMMAND ----------

var = dbutils.widgets.get("p_name")
var

# COMMAND ----------

dbutils.secrets.list(scope='anmoscope')

# COMMAND ----------

#redacted means the secret is pulled securely but not visible
dbutils.secrets.get(scope='anmoscope',key='app-secret')

# COMMAND ----------

# MAGIC %md
# MAGIC #data reading

# COMMAND ----------

df_sales = spark.read.format('csv')\
              .option('header',True)\
              .option('inferSchema',True)\
              .load('abfss://source@storagedatabricksanmo.dfs.core.windows.net/') 




# COMMAND ----------

#display
df_sales.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ### PySpark Transformations

# COMMAND ----------

from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

df_sales.withColumn('Item_Type',split(col('Item_Type'),' ')).display()

# COMMAND ----------

#add yes to every record
df_sales.withColumn('flag',lit('yes')).display()

# COMMAND ----------

#cast the dataype of item_visibility
df_sales.withColumn('Item_Visibility',col('Item_Visibility').cast(StringType())).display()

# COMMAND ----------

