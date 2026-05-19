# KPI Genie - Data Pipeline Runbook

**Version:** 1.0  
**Last Updated:** 2024  
**Owner:** Data Engineering Team

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Quick Start Guide](#quick-start-guide)
4. [Skill Files Overview](#skill-files-overview)
5. [Bronze Layer Details](#bronze-layer-details)
6. [Silver Layer Details](#silver-layer-details)
7. [Gold Layer Details](#gold-layer-details)
8. [Transformation Rules](#transformation-rules)
9. [How to Use Custom Skills](#how-to-use-custom-skills)
10. [Best Practices](#best-practices)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [File Locations](#file-locations)
13. [Additional Resources](#additional-resources)

---

## 🎯 Project Overview

**KPI Genie** (powered by **KPI Alchemist**) is a comprehensive, automated data pipeline system built on Databricks that transforms raw data into actionable KPIs through a three-tier medallion architecture:

* **Bronze Layer**: Raw data ingestion from multiple sources
* **Silver Layer**: Data cleansing, type casting, and quality validation
* **Gold Layer**: Automated KPI view generation and aggregation

This runbook provides complete guidance for using the KPI Alchemist skills to build end-to-end data pipelines with minimal manual coding.

### Key Features

✅ **10+ Data Source Patterns** - CSV, JSON, Parquet, Delta, JDBC, S3, Azure, Auto Loader, Merge/Upsert  
✅ **Intelligent Type Detection** - Auto-analyze and cast data types from string bronze layer  
✅ **Automated KPI Generation** - Analyze silver tables and create aggregated KPI views  
✅ **Best Practice Templates** - Pre-built, tested code patterns following Databricks standards  
✅ **Step-by-Step Workflows** - Guided prompts ensure nothing is missed  
✅ **Auto-Execution** - Notebooks run automatically after creation for immediate validation

---

## 📁 Directory Structure

```
kpi_genie/
├── .assistant/
│   └── skills/
│       └── kpi_alchemist/
│           ├── 1_bronze_load/
│           │   └── bronze_data_loader.md          # Bronze ingestion skill
│           ├── 2_silver_load/
│           │   ├── silver_data_loader.md          # Silver transformation skill
│           │   └── references/
│           │       └── Tranformations.md          # Standard transformation rules
│           └── 3_gold_load/
│               ├── 03_gold_data_load.md           # Gold KPI generation skill
│               └── references/
│                   └── Automated KPI Generation System.ipynb
└── README.md                                      # This file
```

### User Project Structure (Created by Skills)

When you use the skills, they create the following structure in your project folder:

```
/Users/<username>/<project_name>/
├── Bronze/
│   ├── 00_setup_bronze_structure                  # Directory setup notebook
│   ├── DDL/
│   │   └── 01_setup_catalog_schema                # Catalog/schema creation
│   └── SRC/
│       ├── 02_load_<source_type>_<table_name>     # Ingestion notebook
│       └── 03_validate_bronze                     # Validation notebook
├── Silver/
│   ├── 00_setup_silver_structure                  # Directory setup notebook
│   ├── DDL/
│   │   └── 01_setup_silver_catalog_schema         # Catalog/schema creation
│   └── SRC/
│       ├── 02_profile_and_analyze                 # Data profiling notebook
│       ├── 03_transform_and_load                  # Transformation notebook
│       └── 04_validate_silver                     # Validation notebook
└── Gold/
    └── Automated KPI Generation System            # KPI generation notebook
```

---

## 🚀 Quick Start Guide

### Step 1: Bronze Data Ingestion (Raw Data)

**Trigger Phrase:** "Load Bronze" or "Ingest to Bronze"

**What It Does:**
* Creates directory structure (DDL/, SRC/)
* Sets up Unity Catalog and schema
* Creates ingestion notebook based on your source type
* Loads raw data with ALL columns as STRING (file sources) or preserves types (RDBMS)
* Adds bronze metadata columns (ingestion_timestamp, source_file, load_id)
* Creates validation notebook
* **Executes all notebooks automatically**

**What You Need:**
1. Project folder path
2. Target table name (catalog.schema.table)
3. Data source type (CSV, JSON, JDBC, etc.)
4. Source-specific configuration (paths, credentials, etc.)

**Output:** Raw data loaded into bronze table with metadata tracking

---

### Step 2: Silver Data Transformation (Cleaned Data)

**Trigger Phrase:** "Ingest to Silver" or "Transform to Silver"

**What It Does:**
* Creates directory structure for silver layer
* Sets up Unity Catalog and schema
* Profiles bronze data to analyze quality and types
* Applies intelligent type casting (auto or manual)
* Applies standard transformations (date parsing, name standardization, calculations)
* Adds silver audit columns (load_timestamp, source_system, record_hash)
* Validates transformed data
* **Executes all notebooks automatically**

**What You Need:**
1. Project folder path
2. Source bronze table name
3. Target silver table name
4. Transformation mode (Auto, Manual, Schema on Read, or Load from References)

**Output:** Clean, typed data in silver table with quality checks

---

### Step 3: Gold KPI Generation (Aggregated Metrics)

**Trigger Phrase:** "Load Gold" or "Create KPI Views"

**What It Does:**
* Clones the Automated KPI Generation System notebook
* Configures it with your source/target details
* Analyzes silver table schema
* Identifies KPI opportunities (numeric, categorical, time-based)
* Generates and creates KPI views with aggregations (COUNT, SUM, AVG, MIN, MAX)
* Deploys views to your gold schema

**What You Need:**
1. Project folder path for gold notebook
2. Source silver table (catalog.schema.table)
3. Target catalog for KPI views
4. Target schema for KPI views

**Output:** Automated KPI views ready for dashboards and analytics

---

## 📚 Skill Files Overview

### 1. Bronze Data Loader (`bronze_data_loader.md`)

**Purpose:** Ingest raw data from multiple sources into Delta tables

**Supported Patterns:**
1. **CSV Files from Volumes** - With custom delimiters and header options
2. **JSON Files** - Multi-line and single-line support
3. **Parquet Files** - With merge schema support
4. **Delta Table Copy** - Copy existing Delta tables with append/overwrite
5. **JDBC Database (SQL Server)** - Direct database ingestion with secrets
6. **JDBC with Partitioning** - Parallelized reads for large tables
7. **AWS S3** - CSV/Parquet from S3 with IAM or access keys
8. **Azure Blob Storage** - ADLS Gen2 integration
9. **Auto Loader (Streaming)** - Incremental file ingestion with checkpointing
10. **Merge/Upsert Load** - Delta merge operations with composite keys

**Key Features:**
* **All columns as STRING** for file sources (no schema inference errors)
* **Preserves original types** for RDBMS and Delta sources
* Automatic metadata columns added to every record
* Pre-configured validation notebooks
* Error-free templates tested on Databricks

---

### 2. Silver Data Transformer (`silver_data_loader.md`)

**Purpose:** Clean, type-cast, and validate data from bronze layer

**Transformation Modes:**
1. **Auto Type Detection** - Analyzes sample data, detects patterns, recommends best types
2. **Manual Type Specification** - You define exact schema
3. **Schema on Read** - Keep as string, cast in queries
4. **Load from References** - Apply transformations from Tranformations.md

**Key Features:**
* Data profiling with distinct value analysis
* Intelligent type recommendations (BIGINT, DECIMAL(30,2), DATE, TIMESTAMP, STRING)
* Applies standard transformation rules automatically
* TRY_CAST for safety (no pipeline failures)
* Deduplication and data quality checks
* Audit column generation

---

### 3. Gold KPI Generator (`03_gold_data_load.md`)

**Purpose:** Automatically generate aggregated KPI views from silver tables

**Capabilities:**
* Analyzes silver table schema and data
* Identifies aggregation opportunities:
  * **Numeric columns**: COUNT, SUM, AVG, MIN, MAX
  * **Categorical columns**: COUNT, DISTINCT COUNT, top N values
  * **Date columns**: Daily, weekly, monthly aggregations
* Creates views in target gold schema
* Follows naming conventions (e.g., `kpi_<table>_<metric>_by_<dimension>`)

**Key Features:**
* No manual aggregation code needed
* Consistent KPI naming and structure
* Easy to extend with custom logic
* Ready for BI tool connections

---

## 🥉 Bronze Layer Details

### Step-by-Step Workflow

The Bronze skill follows a strict 6-step sequence:

#### **STEP 1: Gather All Required Inputs**
Ask user one by one (not all at once):
1. Project location path
2. Target table (catalog.schema.table)
3. Storage location (optional)
4. Data source type (1-10)
5. Source-specific configuration (paths, credentials, options)
6. Confirm all inputs before proceeding

#### **STEP 2: Create Directory Structure**
* Creates `00_setup_bronze_structure` notebook
* Sets up DDL/ and SRC/ folders
* **Executes notebook automatically** to create directories

#### **STEP 3: Create Catalog and Schema DDL**
* Creates `01_setup_catalog_schema` notebook
* Generates CREATE CATALOG and CREATE SCHEMA statements
* Grants permissions to account users
* **Executes notebook automatically** to provision infrastructure

#### **STEP 4: Create Ingestion Notebook**
* Selects appropriate pattern based on source type
* Creates `02_load_<source_type>_<table_name>` notebook
* Hardcodes all configuration values (no widgets)
* Includes read, metadata addition, write, and validation cells
* **Executes notebook automatically** to load data

#### **STEP 5: Create Validation Notebook**
* Creates `03_validate_bronze` notebook
* Includes record counts, schema display, sample data, load history, Delta history
* **Executes notebook automatically** to validate load

#### **STEP 6: Final Summary and Handoff**
* Displays complete summary with:
  * Project structure created
  * Unity Catalog objects
  * Execution results (record counts)
  * Quick links to notebooks and tables
* Provides guidance for re-running ingestion

### Data Type Strategy

**Critical Rule:** 
* **File-based sources** (CSV, JSON, Parquet, S3, Azure, Auto Loader): Load ALL columns as **STRING**
  * Why? Avoids schema inference errors, preserves raw data integrity
  * Type casting happens in Silver layer with validation
* **RDBMS sources** (JDBC patterns): **Preserve original data types**
  * Why? Database types are already validated and optimized
* **Delta sources**: **Preserve original schema**

### Code Pattern Example (CSV)

```python
# Read CSV - NO schema inference
df = spark.read.format("csv") \
    .option("header", True) \
    .option("inferSchema", "false") \
    .option("delimiter", ",") \
    .load(source_path)

# Add metadata
df = df.withColumn("bronze_ingestion_timestamp", current_timestamp()) \
       .withColumn("bronze_source_file", input_file_name()) \
       .withColumn("bronze_load_id", lit(load_id))

# Write to Delta
df.write.format("delta") \
    .mode("append") \
    .option("mergeSchema", "true") \
    .saveAsTable(target_table)
```

### Metadata Columns Added

Every bronze record includes:
* `bronze_ingestion_timestamp` - When record was loaded
* `bronze_source_file` - Source file path (for file sources)
* `bronze_load_id` - UUID for this load batch

---

## 🥈 Silver Layer Details

### Step-by-Step Workflow

#### **STEP 1: Gather All Required Inputs**
1. Project location path
2. Source bronze table (catalog.schema.table)
3. Target silver table (catalog.schema.table)
4. Storage location (optional)
5. Transformation mode (Auto, Manual, Schema on Read, Load from References)
6. Confirm all inputs

#### **STEP 2: Create Directory Structure**
* Creates `00_setup_silver_structure` notebook
* Sets up DDL/ and SRC/ folders
* **Executes automatically**

#### **STEP 3: Create Catalog and Schema DDL**
* Creates `01_setup_silver_catalog_schema` notebook
* Provisions Unity Catalog infrastructure
* **Executes automatically**

#### **STEP 4: Create Data Profiling Notebook**
* Creates `02_profile_and_analyze` notebook
* **Reads transformation reference file** (Tranformations.md)
* Analyzes bronze data:
  * Record counts
  * Distinct values per column
  * Data type patterns
  * Null percentages
  * Sample value inspection
* Recommends data types and transformations
* **Executes automatically** to generate analysis report

#### **STEP 5: Create Transformation Notebook**
* Creates `03_transform_and_load` notebook
* Applies type casting with TRY_CAST
* Implements standard transformations:
  * Date parsing (multiple formats)
  * Name standardization (UPPER)
  * Calculated fields (total_price)
  * String trimming and cleansing
* Adds audit columns:
  * `silver_load_timestamp`
  * `silver_source_system`
  * `silver_record_hash`
* Handles nulls and removes invalid records
* **Executes automatically** to load silver table

#### **STEP 6: Create Validation Notebook**
* Creates `04_validate_silver` notebook
* Validates:
  * Record counts match expectations
  * Data types are correct
  * No critical nulls
  * Transformation logic applied correctly
* **Executes automatically**

#### **STEP 7: Additional Transformations**
* If needed, creates `05_additional_transformations` notebook
* Applies custom business logic
* Integrates README file rules if provided

### Transformation Reference File

**Location:** `.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformations.md`

**MUST READ** before Step 4 profiling. Contains standard rules for:
* Calculated fields
* String standardization
* Date format handling
* Type preferences
* Data quality requirements

### Auto Type Detection Logic

The skill analyzes sample data to recommend:
* **BIGINT**: Integer patterns without decimals
* **DECIMAL(30,2)**: Numeric values with decimals (currency, measurements)
* **DATE**: Date patterns (YYYY-MM-DD, MM-DD-YY, M/D/YYYY)
* **TIMESTAMP**: Datetime patterns with time component
* **STRING**: Text, mixed formats, or when uncertain

Uses TRY_CAST to safely convert with fallback to NULL on errors.

---

## 🥇 Gold Layer Details

### Step-by-Step Workflow

#### **STEP 1: Gather Project Configuration**
1. Project folder path for gold notebook
2. Source silver table (catalog.schema.table) → Parse into catalog, schema, table
3. Target catalog for KPI views
4. Target schema for KPI views

#### **STEP 2: Clone and Configure Notebook**
* Reads reference notebook: `Automated KPI Generation System.ipynb`
* Clones to user's project folder
* Updates configuration variables:
  * SOURCE_CATALOG, SOURCE_SCHEMA, SOURCE_TABLE
  * TARGET_CATALOG, TARGET_SCHEMA

#### **STEP 3: Guide User Execution**
* Informs user the notebook is ready
* User runs notebook to execute KPI generation

### What the System Does

1. **Analyzes Source Table**
   * Reads silver table schema
   * Identifies column types (numeric, categorical, date/timestamp)
   * Samples data to understand distributions

2. **Identifies KPI Opportunities**
   * **Numeric columns**: Aggregations like SUM, AVG, MIN, MAX
   * **Categorical columns**: COUNT, DISTINCT COUNT, top values
   * **Date columns**: Time-series aggregations (daily, weekly, monthly)
   * **Combinations**: Cross-dimensional KPIs (e.g., sales by region by month)

3. **Generates KPI Views**
   * Creates SQL view definitions
   * Names views consistently: `kpi_<base_table>_<metric>_by_<dimension>`
   * Example: `kpi_sales_total_revenue_by_region`, `kpi_customers_count_by_signup_month`

4. **Deploys to Target Schema**
   * Executes CREATE VIEW statements in target gold schema
   * Views are immediately queryable by BI tools

### Example Generated KPIs

From a `sales_data` silver table:
* `kpi_sales_total_revenue_by_date` - Daily revenue totals
* `kpi_sales_avg_order_value` - Average transaction amount
* `kpi_sales_unique_customers_by_month` - Monthly customer counts
* `kpi_sales_top_10_products` - Best-selling products

---

## ⚙️ Transformation Rules

### Standard Transformations (from Tranformations.md)

#### 1. Calculate `total_price`
```sql
-- Multiply price with quantity (handles both 'units' and 'qty' columns)
CASE 
  WHEN units IS NOT NULL THEN TRY_CAST(price AS DECIMAL(30,2)) * TRY_CAST(units AS BIGINT)
  WHEN qty IS NOT NULL THEN TRY_CAST(price AS DECIMAL(30,2)) * TRY_CAST(qty AS BIGINT)
  ELSE NULL
END AS total_price
```

#### 2. Standardize Customer Names
```sql
-- Convert all customer name columns to upper case
UPPER(TRIM(customer_name)) AS customer_name
```

#### 3. Handle Multiple Date Formats
```sql
-- Parse MM-DD-YY and M/D/YYYY formats
COALESCE(
  TRY_TO_DATE(date_column, 'MM-dd-yy'),
  TRY_TO_DATE(date_column, 'M/d/yyyy'),
  TRY_TO_DATE(date_column, 'yyyy-MM-dd')
) AS parsed_date

-- Remove records where date parsing failed (after all transformations)
WHERE parsed_date IS NOT NULL
```

#### 4. Preferred Data Types
* **BIGINT**: Integer values (quantities, counts, IDs without leading zeros)
* **DECIMAL(30,2)**: Currency, measurements, any numeric with decimals
* **STRING**: Text, codes with leading zeros, mixed formats
* **Do NOT apply to phone numbers** - Keep as STRING

### Silver Layer Must-Have Rules

#### 1. Data Quality Validation
```python
# Verify source data exists
source_count = spark.table(source_bronze_table).count()
if source_count == 0:
    raise Exception(f"Source table {source_bronze_table} is empty")
```

#### 2. Deduplication
```python
# For now, this step is ignored per reference file
# Future: Implement based on composite key
```

#### 3. Schema Standardization
* **Column naming**: snake_case (e.g., `customer_id`, `order_date`)
* **Consistent types**: Same column types across all silver tables
* **Uniform nullability**: Document which columns allow nulls

#### 4. Audit Columns
```python
df = df.withColumn("silver_load_timestamp", current_timestamp()) \
       .withColumn("silver_source_system", lit("bronze_layer")) \
       .withColumn("silver_record_hash", sha2(concat_ws("|", *df.columns), 256))
```

#### 5. Idempotency
* Use MERGE operations for repeatable loads
* Include load_id in writes for tracking
* Design for replay without duplicates

#### 6. Data Retention
* Define retention policies per table
* Partition by date for efficient pruning
* Archive old data to cold storage

#### 7. String Trimming and Cleansing
```python
# Apply TRIM to all string columns
from pyspark.sql.functions import trim, regexp_replace

for col_name, col_type in df.dtypes:
    if col_type == 'string':
        df = df.withColumn(col_name, trim(col(col_name)))
        df = df.withColumn(col_name, regexp_replace(col(col_name), r'\s+', ' '))
```

#### 8. Type Conversion Safety
```python
# Use TRY_CAST instead of CAST
SELECT 
  TRY_CAST(amount AS DECIMAL(30,2)) AS amount,
  TRY_CAST(order_id AS BIGINT) AS order_id,
  COALESCE(TRY_CAST(quantity AS INT), 0) AS quantity  -- Default to 0
FROM bronze_table
```

#### 9. Date and Timestamp Formatting
```python
# Standardize to DATE type and UTC timezone
df = df.withColumn("order_date", to_date(col("order_date_string"))) \
       .withColumn("created_at", to_utc_timestamp(col("created_at_string"), "America/New_York"))
```

#### 10. Numeric Formatting and Precision
```sql
-- Remove currency symbols and cast to DECIMAL
REGEXP_REPLACE(price_column, '[^0-9.-]', '') AS cleaned_price,
TRY_CAST(cleaned_price AS DECIMAL(30,2)) AS price
```

#### 11. Case Normalization
```sql
-- Apply consistent casing
UPPER(product_code) AS product_code,      -- Codes: UPPER
LOWER(email_address) AS email_address,    -- Emails: LOWER
INITCAP(customer_name) AS customer_name   -- Names: Title Case (optional)
```

---

## 🎮 How to Use Custom Skills

### Triggering Skills with Phrases

The assistant recognizes specific trigger phrases to load the appropriate skill:

#### Bronze Data Loader
**Trigger Phrases:**
* "Load Bronze"
* "Ingest to Bronze"
* "Create bronze layer"
* "Ingest raw data"

**What Happens:**
1. Assistant loads `bronze_data_loader.md` skill
2. Prompts you for configuration (project path, target table, source type, etc.)
3. Creates all notebooks with your inputs
4. Executes notebooks automatically
5. Validates data load
6. Provides summary with links

#### Silver Data Transformer
**Trigger Phrases:**
* "Ingest to Silver"
* "Transform to Silver"
* "Create silver layer"
* "Clean bronze data"

**What Happens:**
1. Assistant loads `silver_data_loader.md` skill
2. Prompts you for configuration (bronze table, silver table, transformation mode)
3. Reads transformation reference file
4. Creates profiling, transformation, and validation notebooks
5. Executes notebooks automatically
6. Provides summary with data quality report

#### Gold KPI Generator
**Trigger Phrases:**
* "Load Gold"
* "Create KPI Views"
* "Generate KPIs"
* "Create gold layer"

**What Happens:**
1. Assistant loads `03_gold_data_load.md` skill
2. Prompts you for configuration (silver table, target catalog/schema)
3. Clones KPI generation notebook
4. Updates configuration with your values
5. Guides you to run the notebook
6. KPIs are auto-generated and created

### Example Conversation Flow

```
You: Load Bronze for my sales data