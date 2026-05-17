# Databricks Genie AI Skill File: Bronze Data Ingestion
    
## 🎯 Skill Purpose
This skill guides you through a structured, step-by-step bronze data ingestion setup. Follow the steps sequentially - gather ALL inputs first, then create assets.

---

## ⚠️ AGENT INSTRUCTIONS - READ FIRST

**CRITICAL RULES:**
1. **Always follow the step sequence** - Do NOT skip or reorder steps
2. **Gather ALL inputs in Step 1** before proceeding to Step 2
3. **Create ONLY the assets specified** in each step - no additional files
4. **Use EXACT templates** provided - no modifications unless user explicitly requests
5. **Validate completion** of each step before moving to next
6. **Do NOT hallucinate** - if information is missing, ask the user
7. **One step at a time** - Complete current step fully before suggesting next
8. **No widgets** - All configuration values are hardcoded from Step 1 inputs
9. **EXECUTE ALL CELLS** - After creating each notebook, immediately navigate to it and execute all cells to load data and run validations

---

## 📋 STEP-BY-STEP WORKFLOW

### STEP 1: GATHER ALL REQUIRED INPUTS

**Before creating anything, ask the user these questions and collect ALL answers:**

**Ask it one by one not all at once. Follow like 1.1 then 1.2 then 1.3 ... .. ..**

#### 1.1 Project Location
- **Question:** "Where would you like to keep your bronze ingestion code files?"
- **Default:** `/Workspace/Users/{current_username}/ProjectIngestion/Bronze`
- **Store as:** `base_path`

#### 1.2 Target Table Information
- **Question:** "What is your target table? (Provide full name in format: catalog_name.schema_name.table_name)"
- **Example:** `main.bronze.customers`
- **Default:** `main.bronze.{table_name}`
- **Store as:** `target_table`
- **Parse and extract:**
  - `catalog_name` = first part (e.g., "main")
  - `schema_name` = second part (e.g., "bronze")
  - `table_name` = third part (e.g., "customers")

- **Question:** "What storage location for the database/schema? (Optional - press Enter to skip for Unity Catalog default)"
- **Default:** Empty (Unity Catalog default)
- **Store as:** `storage_location`

#### 1.3 Data Source Information
- **Question:** "What type of data source will you ingest from?"
- **Options:** 
  1. CSV Files from Volumes
  2. JSON Files from Volumes
  3. Parquet Files from Volumes
  4. Delta Table Copy
  5. JDBC Database (SQL Server)
  6. JDBC with Partitioning (Large Tables)
  7. AWS S3
  8. Azure Blob Storage
  9. Auto Loader (Streaming)
  10. Merge/Upsert Load
- **Store as:** `source_type` (the number or name)

#### 1.4 Source-Specific Configuration
Based on the `source_type`, ask for:

**For File-Based Sources (CSV, JSON, Parquet, S3, Azure):**
- Source path/location
- File format specific options (delimiter for CSV, multiline for JSON, etc.)

**For Database Sources (JDBC):**
- JDBC URL
- Source table name
- Secret scope name
- Username key in secrets
- Password key in secrets
- (For partitioned) Partition column, lower bound, upper bound, num partitions

**For Auto Loader:**
- Source path
- Checkpoint location
- File format (csv, json, parquet, avro)

**For Merge/Upsert:**
- Source path
- Merge key columns (comma-separated)

**Store all collected values in a structured format**

#### 1.5 Confirmation
- **Action:** Display all collected inputs to user
- **Question:** "Please confirm these details are correct. Type 'yes' to proceed with creation, or provide corrections."
- **Wait for confirmation before proceeding to Step 2**

---

### STEP 2: CREATE DIRECTORY STRUCTURE

**Only execute after Step 1 is confirmed**

#### 2.1 Create Setup Notebook
- **Action:** Create a Python notebook named `00_setup_bronze_structure`
- **Location:** `{base_path}/00_setup_bronze_structure`
- **Content:** Use template below

**Template for Setup Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Project Setup
# MAGIC Run this notebook first to create the directory structure

# COMMAND ----------
# Get current username
username = spark.sql("SELECT current_user() as user").collect()[0]["user"]

# Base path from Step 1
base_path = "{base_path}"

# Create directory structure
ddl_path = f"{base_path}/DDL"
src_path = f"{base_path}/SRC"

# Create directories using dbutils
dbutils.fs.mkdirs(base_path)
dbutils.fs.mkdirs(ddl_path)
dbutils.fs.mkdirs(src_path)

print(f"✅ Created Bronze structure at: {base_path}")
print(f"  📂 DDL: {ddl_path}")
print(f"  📂 SRC: {src_path}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Directory Structure Created:
# MAGIC ```
# MAGIC {base_path}/
# MAGIC ├── DDL/          # Catalog & Database creation scripts
# MAGIC └── SRC/          # Source code for data ingestion
# MAGIC ```
```

#### 2.2 Execute Setup Notebook
- **Action:** Navigate to the created notebook using `openAsset` with `continueMessage: "Execute all cells in this setup notebook to create the directory structure"`
- **Agent on notebook page will:** Execute all cells using `runNotebookCells`
- **Validation:** Confirm directories were created successfully by checking execution results
- **Return:** Navigate back to complete Step 2
- **Output:** "✅ Step 2 Complete: Directory structure created"

---

### STEP 3: CREATE CATALOG AND DATABASE DDL NOTEBOOK

**Only execute after Step 2 is complete**

#### 3.1 Create DDL Notebook
- **Action:** Create a Python notebook named `01_setup_catalog_schema`
- **Location:** `{base_path}/DDL/01_setup_catalog_schema`
- **Content:** Use template below with user-provided values

**Template for DDL Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Layer: Catalog and Schema Setup
# MAGIC 
# MAGIC **Target Table:** {target_table}
# MAGIC **Catalog:** {catalog_name}
# MAGIC **Schema:** {schema_name}

# COMMAND ----------
# Configuration from Step 1
catalog_name = "{catalog_name}"
schema_name = "{schema_name}"
storage_location = "{storage_location}"  # Empty string if not specified

# COMMAND ----------
# MAGIC %md
# MAGIC ## Create Catalog

# COMMAND ----------
# Create catalog if not exists
spark.sql(f"""
    CREATE CATALOG IF NOT EXISTS {catalog_name}
    COMMENT 'Catalog for bronze layer data ingestion'
""")

print(f"✅ Catalog '{catalog_name}' created or already exists")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Create Schema/Database

# COMMAND ----------
# Build schema creation SQL with optional storage location
if storage_location and storage_location.strip():
    schema_sql = f"""
        CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}
        COMMENT 'Bronze layer - raw ingested data'
        LOCATION '{storage_location}'
    """
else:
    schema_sql = f"""
        CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}
        COMMENT 'Bronze layer - raw ingested data'
    """

spark.sql(schema_sql)
print(f"✅ Schema '{catalog_name}.{schema_name}' created or already exists")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Grant Permissions

# COMMAND ----------
# Grant permissions (adjust as needed)
try:
    spark.sql(f"GRANT USE CATALOG ON CATALOG {catalog_name} TO `account users`")
    spark.sql(f"GRANT USE SCHEMA ON SCHEMA {catalog_name}.{schema_name} TO `account users`")
    spark.sql(f"GRANT CREATE TABLE ON SCHEMA {catalog_name}.{schema_name} TO `account users`")
    print("✅ Permissions granted successfully")
except Exception as e:
    print(f"⚠️ Note: Permission grants may require admin privileges: {e}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Verify Creation

# COMMAND ----------
# Verify catalog and schema exist
display(spark.sql(f"SHOW SCHEMAS IN {catalog_name}"))
print(f"\n✅ Verification complete: {catalog_name}.{schema_name} is ready for use")
```

#### 3.2 Execute DDL Notebook
- **Action:** Navigate to the created notebook using `openAsset` with `continueMessage: "Execute all cells in this DDL notebook to create the catalog and schema"`
- **Agent on notebook page will:** Execute all cells sequentially using `runNotebookCells`
- **Validation:** Verify catalog and schema exist by checking execution results
- **Return:** Navigate back after successful execution
- **Output:** "✅ Step 3 Complete: Catalog '{catalog_name}' and schema '{schema_name}' created"

---

### STEP 4: CREATE INGESTION NOTEBOOK

**Only execute after Step 3 is complete**

#### 4.1 Determine Ingestion Pattern
- **Action:** Based on `source_type` from Step 1, select the correct pattern
- **Map:** 
  - Type 1 → Pattern 1 (CSV)
  - Type 2 → Pattern 2 (JSON)
  - Type 3 → Pattern 3 (Parquet)
  - Type 4 → Pattern 4 (Delta Copy)
  - Type 5 → Pattern 5 (JDBC)
  - Type 6 → Pattern 6 (JDBC Partitioned)
  - Type 7 → Pattern 7 (S3)
  - Type 8 → Pattern 8 (Azure)
  - Type 9 → Pattern 9 (Auto Loader)
  - Type 10 → Pattern 10 (Merge/Upsert)

#### 4.2 Create Ingestion Notebook
- **Action:** Create a Python notebook with descriptive name
- **Naming:** `02_load_{source_type_name}_{table_name}`
  - Example: `02_load_csv_customers`
- **Location:** `{base_path}/SRC/02_load_{source_type_name}_{table_name}`
- **Content:** Use the corresponding pattern template with hardcoded values from Step 1

#### 4.3 Notebook Structure
Every ingestion notebook must have this structure:

```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Ingestion: {Description}
# MAGIC 
# MAGIC **Source:** {source_description}
# MAGIC **Target:** {target_table}
# MAGIC **Ingestion Type:** {source_type}

# COMMAND ----------
# Import required libraries
from pyspark.sql.functions import current_timestamp, input_file_name, lit
import uuid

# COMMAND ----------
# MAGIC %md
# MAGIC ## Configuration

# COMMAND ----------
# Configuration values from Step 1
{configuration_code_with_hardcoded_values}
load_id = str(uuid.uuid4())

# COMMAND ----------
# MAGIC %md
# MAGIC ## Read Source Data

# COMMAND ----------
# Read from source
{read_code_based_on_pattern}

# COMMAND ----------
# MAGIC %md
# MAGIC ## Add Metadata Columns

# COMMAND ----------
# Add bronze metadata
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Write to Bronze Table

# COMMAND ----------
# Write to bronze
{write_code_based_on_pattern}

print(f"✅ Loaded {df.count()} records to {target_table}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Validation

# COMMAND ----------
# Verify load
record_count = spark.table(target_table).count()
print(f"Total records in table: {record_count}")

# Check latest load
display(spark.sql(f"""
    SELECT 
        bronze_load_id,
        MAX(bronze_ingestion_timestamp) as latest_timestamp,
        COUNT(*) as records_in_batch
    FROM {target_table}
    GROUP BY bronze_load_id
    ORDER BY latest_timestamp DESC
    LIMIT 5
"""))
```

#### 4.4 Hardcode Configuration Values
- **Critical:** All configuration values MUST be hardcoded from Step 1 inputs
- **Example:** If user provided target_table as `main.bronze.customers`, the code should be:
```python
target_table = "main.bronze.customers"
source_path = "/Volumes/main/default/data/customers.csv"
delimiter = ","
has_header = True
```

#### 4.5 Execute Ingestion Notebook
- **Action:** After creating the ingestion notebook, navigate to it using `openAsset` with `continueMessage: "Execute all cells in this ingestion notebook to load data into the bronze table"`
- **Agent on notebook page will:** Execute all cells sequentially using `runNotebookCells`
- **Validation:** Check execution results to confirm data was loaded successfully
- **Error Handling:** If any cell fails, diagnose and fix the issue before proceeding
- **Return:** Navigate back after successful execution
- **Output:** "✅ Step 4 Complete: Data ingestion completed - {record_count} records loaded to {target_table}"

---

### STEP 5: CREATE VALIDATION NOTEBOOK

**Only execute after Step 4 is complete**

#### 5.1 Create Validation Notebook
- **Action:** Create a Python notebook named `03_validate_bronze`
- **Location:** `{base_path}/SRC/03_validate_bronze`
- **Content:** Use template below

**Template for Validation Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Data Quality Validation

# COMMAND ----------
# Configuration
target_table = "{target_table}"

# COMMAND ----------
# MAGIC %md
# MAGIC ## Record Count

# COMMAND ----------
# Record count
record_count = spark.table(target_table).count()
print(f"Total records: {record_count}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Schema Information

# COMMAND ----------
# Display schema
display(spark.sql(f"DESCRIBE TABLE {target_table}"))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Sample Data

# COMMAND ----------
# Show sample records
display(spark.table(target_table).limit(100))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Load History

# COMMAND ----------
# Check latest loads
display(spark.sql(f"""
    SELECT 
        bronze_load_id,
        MIN(bronze_ingestion_timestamp) as load_start,
        MAX(bronze_ingestion_timestamp) as load_end,
        COUNT(*) as records_in_batch,
        COUNT(DISTINCT bronze_source_file) as num_source_files
    FROM {target_table}
    GROUP BY bronze_load_id
    ORDER BY load_start DESC
    LIMIT 10
"""))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Table History (Delta)

# COMMAND ----------
# Check Delta history
display(spark.sql(f"DESCRIBE HISTORY {target_table} LIMIT 10"))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Data Quality Checks

# COMMAND ----------
# Basic quality checks
display(spark.sql(f"""
    SELECT 
        COUNT(*) as total_records,
        COUNT(DISTINCT bronze_load_id) as num_loads,
        MIN(bronze_ingestion_timestamp) as first_load,
        MAX(bronze_ingestion_timestamp) as latest_load
    FROM {target_table}
"""))
```

#### 5.2 Execute Validation Notebook
- **Action:** After creating the validation notebook, navigate to it using `openAsset` with `continueMessage: "Execute all cells in this validation notebook to verify data quality and completeness"`
- **Agent on notebook page will:** Execute all cells sequentially using `runNotebookCells`
- **Validation:** Review validation results to ensure data quality meets expectations
- **Return:** Navigate back after successful execution
- **Output:** "✅ Step 5 Complete: Validation completed - all quality checks passed"

---

### STEP 6: FINAL SUMMARY AND HANDOFF

**Only execute after Step 5 is complete**

#### 6.1 Create Summary
- **Action:** Display a complete summary of what was created and executed

**Summary Template:**
```
✅ Bronze Ingestion Setup Complete!

📁 Project Structure:
   Base Path: {base_path}
   ├── DDL/
   │   └── 01_setup_catalog_schema ✅ EXECUTED
   └── SRC/
       ├── 02_load_{source_type}_{table_name} ✅ EXECUTED
       └── 03_validate_bronze ✅ EXECUTED

📊 Unity Catalog:
   Target Table: {target_table}
   Catalog: {catalog_name}
   Schema: {schema_name}

📈 Execution Results:
   Records Loaded: {record_count}
   Load Status: SUCCESS
   Validation Status: PASSED

📝 What Was Done:
   1. ✅ Created directory structure
   2. ✅ Set up catalog and schema
   3. ✅ Created ingestion notebook
   4. ✅ Executed data load - {record_count} records loaded
   5. ✅ Created validation notebook
   6. ✅ Executed validation checks - all passed

🔗 Quick Links:
   [DDL Notebook](#notebook-{ddl_notebook_id})
   [Ingestion Notebook](#notebook-{ingestion_notebook_id})
   [Validation Notebook](#notebook-{validation_notebook_id})
   [Target Table](#table/{target_table})
```

#### 6.2 Next Steps Guidance
Provide the user with:
1. Summary of completed work with execution results
2. Links to review the notebooks and table
3. Instructions for re-running ingestion if needed:
   - "To load additional data, open the ingestion notebook and click 'Run All'"
   - "To validate data after new loads, open the validation notebook and click 'Run All'"

---

## 📚 APPENDIX: CODE PATTERNS

### Pattern 1: CSV Files from Volumes
```python
# Configuration
source_path = "{user_provided_source_path}"
target_table = "{user_provided_target_table}"
delimiter = "{user_provided_delimiter}"  # default: ","
has_header = {user_provided_has_header}  # True or False
load_id = str(uuid.uuid4())

# Read CSV
df = spark.read.format("csv") \
    .option("header", has_header) \
    .option("inferSchema", "true") \
    .option("delimiter", delimiter) \
    .option("encoding", "UTF-8") \
    .load(source_path)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 2: JSON Files (Multi-line)
```python
# Configuration
source_path = "{user_provided_source_path}"
target_table = "{user_provided_target_table}"
multiline = {user_provided_multiline}  # True or False
load_id = str(uuid.uuid4())

# Read JSON
df = spark.read.format("json") \
    .option("multiLine", multiline) \
    .load(source_path)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 3: Parquet Files
```python
# Configuration
source_path = "{user_provided_source_path}"
target_table = "{user_provided_target_table}"
load_id = str(uuid.uuid4())

# Read Parquet
df = spark.read.format("parquet") \
    .option("mergeSchema", "true") \
    .load(source_path)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 4: Delta Table Copy
```python
# Configuration
source_table = "{user_provided_source_table}"
target_table = "{user_provided_target_table}"
load_mode = "{user_provided_load_mode}"  # "overwrite" or "append"
load_id = str(uuid.uuid4())

# Read Delta table
df = spark.read.format("delta").table(source_table)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode(load_mode) \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 5: JDBC Database (SQL Server)
```python
# Configuration
jdbc_url = "{user_provided_jdbc_url}"
source_table = "{user_provided_source_table}"
target_table = "{user_provided_target_table}"
secret_scope = "{user_provided_secret_scope}"
username_key = "{user_provided_username_key}"
password_key = "{user_provided_password_key}"
load_id = str(uuid.uuid4())

# Get credentials from secrets
username = dbutils.secrets.get(scope=secret_scope, key=username_key)
password = dbutils.secrets.get(scope=secret_scope, key=password_key)

# JDBC properties
jdbc_properties = {
    "user": username,
    "password": password,
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Read from JDBC
df = spark.read.jdbc(
    url=jdbc_url,
    table=source_table,
    properties=jdbc_properties
)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 6: JDBC with Partitioned Read
```python
# Configuration
jdbc_url = "{user_provided_jdbc_url}"
source_table = "{user_provided_source_table}"
target_table = "{user_provided_target_table}"
partition_column = "{user_provided_partition_column}"
lower_bound = {user_provided_lower_bound}
upper_bound = {user_provided_upper_bound}
num_partitions = {user_provided_num_partitions}
secret_scope = "{user_provided_secret_scope}"
load_id = str(uuid.uuid4())

# Get credentials
username = dbutils.secrets.get(scope=secret_scope, key="sql_username")
password = dbutils.secrets.get(scope=secret_scope, key="sql_password")

jdbc_properties = {
    "user": username,
    "password": password,
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Read with partitioning
df = spark.read.jdbc(
    url=jdbc_url,
    table=source_table,
    column=partition_column,
    lowerBound=lower_bound,
    upperBound=upper_bound,
    numPartitions=num_partitions,
    properties=jdbc_properties
)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 7: AWS S3 (CSV)
```python
# Configuration
s3_bucket = "{user_provided_s3_bucket}"
s3_path = "{user_provided_s3_path}"
s3_full_path = f"s3a://{s3_bucket}/{s3_path}"
target_table = "{user_provided_target_table}"
use_iam_role = {user_provided_use_iam_role}  # True or False
load_id = str(uuid.uuid4())

# AWS credentials (if not using IAM role)
if not use_iam_role:
    aws_access_key = dbutils.secrets.get(scope="aws_scope", key="access_key")
    aws_secret_key = dbutils.secrets.get(scope="aws_scope", key="secret_key")
    spark.conf.set("fs.s3a.access.key", aws_access_key)
    spark.conf.set("fs.s3a.secret.key", aws_secret_key)

# Read CSV from S3
df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(s3_full_path)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 8: Azure Blob Storage
```python
# Configuration
storage_account = "{user_provided_storage_account}"
container = "{user_provided_container}"
file_path = "{user_provided_file_path}"
target_table = "{user_provided_target_table}"
secret_scope = "{user_provided_secret_scope}"
load_id = str(uuid.uuid4())

# Set up Azure authentication
account_key = dbutils.secrets.get(scope=secret_scope, key="storage_key")
spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    account_key
)

# Azure path
azure_path = f"abfss://{container}@{storage_account}.dfs.core.windows.net/{file_path}"

# Read from Azure
df = spark.read.format("parquet").load(azure_path)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to bronze
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Pattern 9: Auto Loader (Incremental Streaming)
```python
# Configuration
source_path = "{user_provided_source_path}"
checkpoint_location = "{user_provided_checkpoint_location}"
target_table = "{user_provided_target_table}"
file_format = "{user_provided_file_format}"  # csv, json, parquet, avro

# Read with Auto Loader
df = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", file_format) \
    .option("cloudFiles.schemaLocation", checkpoint_location + "/schema") \
    .option("cloudFiles.inferColumnTypes", "true") \
    .option("header", "true") \
    .load(source_path)

# Add metadata columns
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name())

# Write stream to bronze
query = df.writeStream \
    .format("delta") \
    .option("checkpointLocation", checkpoint_location) \
    .option("mergeSchema", "true") \
    .trigger(availableNow=True) \
    .toTable(target_table)

query.awaitTermination()
print(f"✅ Auto Loader completed for {target_table}")
```

### Pattern 10: Merge (Upsert) Load
```python
from delta.tables import DeltaTable

# Configuration
source_path = "{user_provided_source_path}"
target_table = "{user_provided_target_table}"
merge_keys = {user_provided_merge_keys_list}  # ["key1", "key2"]
load_id = str(uuid.uuid4())

# Read source data
source_df = spark.read.format("csv") \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .load(source_path)

# Add metadata columns
source_df = source_df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
                     .withColumn("bronze_load_id", lit(load_id))

# Check if table exists
if spark.catalog.tableExists(target_table):
    # Perform merge
    delta_table = DeltaTable.forName(spark, target_table)
    
    # Build merge condition
    merge_condition = " AND ".join([f"target.{key} = source.{key}" for key in merge_keys])
    
    delta_table.alias("target").merge(
        source_df.alias("source"),
        merge_condition
    ).whenMatchedUpdateAll() \
     .whenNotMatchedInsertAll() \
     .execute()
    
    print(f"✅ Merged data into {target_table}")
else:
    # First load - create table
    source_df.write.format("delta") \
        .mode("overwrite") \
        .saveAsTable(target_table)
    
    print(f"✅ Created and loaded {target_table}")
```

---

## 💡 IMPORTANT REMINDERS FOR AGENT

1. **Never skip Step 1** - Always gather ALL inputs before creating anything
2. **Follow the sequence** - Steps must be completed in order (1 → 2 → 3 → 4 → 5 → 6)
3. **Use exact templates** - Do not modify patterns unless explicitly requested
4. **Hardcode all values** - Use values from Step 1, not placeholder text or widgets
5. **Validate each step** - Confirm completion before moving to next step
6. **No hallucination** - Only create assets specified in the steps
7. **Provide links** - Always provide notebook/table links in the final summary
8. **No widgets** - All configuration is hardcoded from Step 1 inputs
9. **Execute immediately** - After creating each notebook, navigate to it and execute all cells using `openAsset` and `runNotebookCells`
10. **Verify execution** - Check execution results to ensure data loaded successfully and validations passed before moving to next step
