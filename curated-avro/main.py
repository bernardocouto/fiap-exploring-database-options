import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Data Catalog table
DataCatalogtable_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="fiap", table_name="parquet", transformation_ctx="DataCatalogtable_node1"
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=DataCatalogtable_node1,
    mappings=[
        ("vendor_id", "long", "vendor_id", "long"),
        ("tpep_pickup_datetime", "string", "tpep_pickup_datetime", "string"),
        ("tpep_dropoff_datetime", "string", "tpep_dropoff_datetime", "string"),
        ("passenger_count", "long", "passenger_count", "long"),
        ("trip_distance", "decimal", "trip_distance", "decimal"),
        ("pickup_longitude", "decimal", "pickup_longitude", "decimal"),
        ("pickup_latitude", "decimal", "pickup_latitude", "decimal"),
        ("rate_code_id", "long", "rate_code_id", "long"),
        ("store_and_fwd_flag", "string", "store_and_fwd_flag", "string"),
        ("dropoff_longitude", "decimal", "dropoff_longitude", "decimal"),
        ("dropoff_latitude", "decimal", "dropoff_latitude", "decimal"),
        ("payment_type", "long", "payment_type", "long"),
        ("fare_amount", "decimal", "fare_amount", "decimal"),
        ("extra", "decimal", "extra", "decimal"),
        ("mta_tax", "decimal", "mta_tax", "decimal"),
        ("tip_amount", "decimal", "tip_amount", "decimal"),
        ("tolls_amount", "decimal", "tolls_amount", "decimal"),
        ("improvement_surcharge", "decimal", "improvement_surcharge", "decimal"),
        ("total_amount", "decimal", "total_amount", "decimal"),
        ("partition_0", "string", "partition_0", "string"),
        ("partition_1", "string", "partition_1", "string"),
        ("partition_2", "string", "partition_2", "string"),
        ("partition_3", "string", "partition_3", "string"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.getSink(
    path="s3://fiap-exploring-database-options-curated-avro/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="S3bucket_node3",
)
S3bucket_node3.setCatalogInfo(catalogDatabase="fiap", catalogTableName="avro")
S3bucket_node3.setFormat("avro")
S3bucket_node3.writeFrame(ApplyMapping_node2)
job.commit()
