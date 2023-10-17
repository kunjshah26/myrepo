from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("abc").getOrCreate()

class InvalidObjectError(Exception):
  def __init__(self,message = 'Invalid object name entered, suggestion: HierarchyFusionLocalProduct, HierarchyCordilleraLocalProduct, HierarchySiriusLocalProduct, HierarchyU2K2LocalProduct'):
    self.message = message
    super().__init__(self.message)

df_bdl_global = spark.read.format("delta").load("/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/GlobalProductHierarchyLatest/Processed_Parquet/Global/")
df_bdl_global.createOrReplaceTempView('vw_bdl_hgpl')

def query(dataset):
  
  if dataset.casefold() == 'HierarchySiriusLocalProduct'.casefold():
    regionID = "E"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchySiriusLocalProduct/Processed_Parquet/Sirius"

  elif dataset.casefold() == 'HierarchyU2K2LocalProduct'.casefold():
    regionID = "R"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchyU2K2LocalProduct/Processed_Parquet/U2K2"
  
  elif dataset.casefold() == 'HierarchyCordilleraLocalProduct'.casefold():
    regionID = "A"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchyCordilleraLocalProduct/Processed_Parquet/"

  elif dataset.casefold() == 'HierarchyFusionLocalProduct'.casefold():
    regionID = "I"
    path = "dbfs:/mnt/adls/centrallakePROD/BusinessDataLake/SC/Hierarchies/HierarchyFusionLocalProduct/Processed_Parquet/Fusion"
  
  else:
    raise InvalidObjectError()
  
  data_local = spark.read.format("delta").load(path)
  data_local.createOrReplaceTempView('vw_udl_local')
    
  df = spark.sql(f"""Select REPLACE(LTRIM(REPLACE(A.SKUCODE,'0',' ')),' ','0') as GlobalSKUs, REPLACE(LTRIM(REPLACE(B.MaterialNumber,'0',' ')),' ','0') as LocalMNCodes, B.*
                  from vw_bdl_hgpl as A inner join vw_udl_local as B  
                  ON REPLACE(LTRIM(REPLACE(A.SKUCODE,'0',' ')),' ','0') = REPLACE(LTRIM(REPLACE(B.MaterialNumber,'0',' ')),' ','0') 
                  Where A.SKURegionID = '{regionID}'""")
    
  return df
