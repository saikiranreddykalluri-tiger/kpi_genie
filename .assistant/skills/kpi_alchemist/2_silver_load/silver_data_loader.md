# Databricks Genie AI Skill File: Silver Data Transformation & Type Casting
    
## 🎯 Skill Purpose
This skill guides you through a structured, step-by-step silver data transformation setup. It reads bronze tables, analyzes data quality, intelligently casts data types, and loads clean data into silver layer. Follow the steps sequentially - gather ALL inputs first, then create assets.

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
9. **EXECUTE ALL CELLS** - After creating each notebook, immediately navigate to it and execute all cells to analyze data and perform transformations
10. **Data Type Intelligence** - Always analyze sample data and distinct values before choosing data types
11. **ALWAYS CHECK REFERENCE FILE** - Before applying transformations, read the reference file at `/Workspace/.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformations.md` for standard transformation rules and examples
12. **STEP 4 READS TRANSFORMATIONS** - The data profiling notebook (Step 4) must read the transformations.md reference file to understand what calculated fields and transformations are needed

---

## 📚 TRANSFORMATION REFERENCE FILE

**MANDATORY:** Before proceeding with Step 4 (Data Profiling) and Step 6 (Additional Transformations), always read and apply rules from:

**File Path:** `/Workspace/.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformstions.md`

This reference file contains:
* Standard calculated field logic (e.g., total_price calculations)
* String standardization rules (e.g., customer name formatting)
* Common transformation patterns
* Business logic conventions

**Action Required:**
1. Read the reference file using `readFile` tool
2. Parse transformation rules from the reference
3. Apply these rules as default transformations in Step 4 analysis and Step 6 execution
4. If user provides additional README file, merge both sets of rules

---

## 📋 STEP-BY-STEP WORKFLOW

### STEP 1: GATHER ALL REQUIRED INPUTS

**Before creating anything, ask the user these questions and collect ALL answers:**

**Ask it one by one not all at once. Follow like 1.1 then 1.2 then 1.3 ... .. ..**

#### 1.1 Project Location
- **Question:** "Where would you like to keep your silver transformation code files?"
- **Default:** `/Workspace/Users/{current_username}/ProjectIngestion/Silver`
- **Store as:** `base_path`

#### 1.2 Source Bronze Table Information
- **Question:** "What is your source bronze table? (Provide full name in format: catalog_name.schema_name.table_name)"
- **Example:** `main.bronze.customers`
- **Alternative:** "If you completed bronze ingestion, provide the target table name from that process"
- **Store as:** `source_bronze_table`
- **Parse and extract:**
  - `source_catalog` = first part (e.g., "main")
  - `source_schema` = second part (e.g., "bronze")
  - `source_table_name` = third part (e.g., "customers")

#### 1.3 Target Silver Table Information
- **Question:** "What is your target silver table? (Provide full name in format: catalog_name.schema_name.table_name)"
- **Example:** `main.silver.customers_clean`
- **Default:** `main.silver.{source_table_name}_clean`
- **Store as:** `target_silver_table`
- **Parse and extract:**
  - `target_catalog` = first part (e.g., "main")
  - `target_schema` = second part (e.g., "silver")
  - `target_table_name` = third part (e.g., "customers_clean")

- **Question:** "What storage location for the silver schema? (Optional - press Enter to skip for Unity Catalog default)"
- **Default:** Empty (Unity Catalog default)
- **Store as:** `storage_location`

#### 1.4 Transformation Configuration
- **Question:** "What transformation mode do you want to use?"
- **Options:** 
  1. Auto Type Detection (Analyze sample data and automatically choose best data types)
  2. Manual Type Specification (You specify exact types for each column)
  3. Schema on Read (Keep all as string, let downstream queries cast)
  4. Load from ./references (transformation_reference_path)
- **Store as:** `transformation_mode`

#### 1.5 Confirmation
- **Action:** Display all collected inputs to user in a structured format
- **Question:** "Please confirm these details are correct. Type 'yes' to proceed with creation, or provide corrections."
- **Wait for confirmation before proceeding to Step 2**

---

### STEP 2: CREATE DIRECTORY STRUCTURE

**Only execute after Step 1 is confirmed**

#### 2.1 Create Setup Notebook
- **Action:** Create a Python notebook named `00_setup_silver_structure`
- **Location:** `{base_path}/00_setup_silver_structure`
- **Content:** Use template below

**Template for Setup Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Silver Project Setup
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

print(f"✅ Created Silver structure at: {base_path}")
print(f"  📂 DDL: {ddl_path}")
print(f"  📂 SRC: {src_path}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Directory Structure Created:
# MAGIC ```
# MAGIC {base_path}/
# MAGIC ├── DDL/          # Catalog & Schema creation scripts
# MAGIC └── SRC/          # Source code for data transformation
# MAGIC ```
```

#### 2.2 Execute Setup Notebook
- **Action:** Navigate to the created notebook using `openAsset` with `continueMessage: "Execute all cells in this setup notebook to create the directory structure"`
- **Agent on notebook page will:** Execute all cells using `runNotebookCells`
- **Validation:** Confirm directories were created successfully by checking execution results
- **Return:** Navigate back to complete Step 2
- **Output:** "✅ Step 2 Complete: Directory structure created"

---

### STEP 3: CREATE CATALOG AND SCHEMA DDL NOTEBOOK

**Only execute after Step 2 is complete**

#### 3.1 Create DDL Notebook
- **Action:** Create a Python notebook named `01_setup_silver_catalog_schema`
- **Location:** `{base_path}/DDL/01_setup_silver_catalog_schema`
- **Content:** Use template below with user-provided values

**Template for DDL Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Silver Layer: Catalog and Schema Setup
# MAGIC 
# MAGIC **Source Bronze Table:** {source_bronze_table}
# MAGIC **Target Silver Table:** {target_silver_table}
# MAGIC **Catalog:** {target_catalog}
# MAGIC **Schema:** {target_schema}

# COMMAND ----------
# Configuration from Step 1
catalog_name = "{target_catalog}"
schema_name = "{target_schema}"
storage_location = "{storage_location}"  # Empty string if not specified

# COMMAND ----------
# MAGIC %md
# MAGIC ## Create Catalog

# COMMAND ----------
# Create catalog if not exists
spark.sql(f"""
    CREATE CATALOG IF NOT EXISTS {catalog_name}
    COMMENT 'Catalog for silver layer clean data'
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
        COMMENT 'Silver layer - cleaned and type-cast data'
        LOCATION '{storage_location}'
    """
else:
    schema_sql = f"""
        CREATE SCHEMA IF NOT EXISTS {catalog_name}.{schema_name}
        COMMENT 'Silver layer - cleaned and type-cast data'
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
- **Output:** "✅ Step 3 Complete: Catalog '{target_catalog}' and schema '{target_schema}' created"

---

### STEP 4: CREATE DATA PROFILING & ANALYSIS NOTEBOOK

**Only execute after Step 3 is complete**

**IMPORTANT:** This step uses an AI-powered DataType Definer Agent that leverages Claude Opus 4.6 to intelligently analyze bronze data and recommend optimal data types for the silver layer. The agent profiles columns, analyzes sample data, and uses LLM-based inference to make smart type recommendations.

#### 4.1 Create Data Profiling Notebook
- **Action:** Create a Python notebook named `02_analyze_bronze_data`
- **Location:** `{base_path}/SRC/02_analyze_bronze_data`
- **Content:** Use template below with user-provided values
- **Key Feature:** AI-powered type inference using Claude Opus 4.6 for intelligent data type recommendations
- **Reference File:** Code is also available at `./references/DataTypeDefinerAgent.py`

**Template for Data Profiling Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze Data Analysis & Type Recommendation with AI Agent
# MAGIC 
# MAGIC **Source Table:** {source_bronze_table}
# MAGIC **Target Table:** {target_silver_table}
# MAGIC **Reference:** ./references/DataTypeDefinerAgent.py
# MAGIC 
# MAGIC This notebook uses an AI-powered agent (DataType Definer Agent) to analyze bronze data and intelligently recommend optimal data types for silver layer using Claude Opus 4.6.

# COMMAND ----------
# =============================================================================
# Install Required Libraries
# =============================================================================
!pip install langgraph==0.2.65 langchain==0.3.16 langchain-core==0.3.32 \
pydantic==2.10.6 sqlparse==0.5.3 openai==1.59.7 --quiet

# COMMAND ----------
# =============================================================================
# Imports
# =============================================================================
import json
import re
from typing import List, Optional, Dict, Any, TypedDict
from pydantic import BaseModel, Field, field_validator
from langgraph.graph import StateGraph, END
from pyspark.sql.functions import (
    col, min as spark_min, max as spark_max,
    count, countDistinct
)
import openai

print("✅ Libraries imported successfully")

# COMMAND ----------
# =============================================================================
# Configuration
# =============================================================================
API_KEY = "sk-YFxU38F33HyLN_P-KexwPw"
BASE_URL = "https://api.ai-gateway.tigeranalytics.com"
MODEL_NAME = "claude-opus-4.6"

client = openai.OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)

# COMMAND ----------
# =============================================================================
# Pydantic Models
# =============================================================================
class ColumnSchema(BaseModel):
    column_name: str
    recommended_data_type: str
    reasoning: str

    @field_validator("recommended_data_type")
    @classmethod
    def uppercase_dtype(cls, v):
        return v.upper()


class TableSchemaOutput(BaseModel):
    table_name: str
    columns: List[ColumnSchema]
    total_columns_analyzed: int


class AgentState(TypedDict):
    table_name: str
    columns_to_analyze: List[str]
    profiling_data: Dict[str, Any]
    schema_output: Optional[TableSchemaOutput]
    error: Optional[str]

# COMMAND ----------
# =============================================================================
# Profiling Function
# =============================================================================
def profile_columns(df, columns, table_name):
    profiling_data = {
        "table_name": table_name,
        "columns": {}
    }

    for column in columns:
        try:
            stats = df.select(
                count(col(column)).alias("count"),
                countDistinct(col(column)).alias("distinct_count"),
                spark_min(col(column)).alias("min_value"),
                spark_max(col(column)).alias("max_value")
            ).collect()[0]

            profiling_data["columns"][column] = {
                "spark_type": next(
                    field.dataType.simpleString()
                    for field in df.schema.fields
                    if field.name == column
                ),
                "count": stats["count"],
                "distinct_count": stats["distinct_count"],
                "min_value": str(stats["min_value"]),
                "max_value": str(stats["max_value"]),
                "sample_values": [
                    str(r[column])
                    for r in df.select(column).limit(5).collect()
                ],
                "null_count": df.filter(col(column).isNull()).count()
            }

        except Exception as e:
            profiling_data["columns"][column] = {
                "spark_type": "unknown",
                "error": str(e)
            }

    return profiling_data

# COMMAND ----------
# =============================================================================
# LangGraph Nodes
# =============================================================================
def data_profiling_node(state: AgentState):
    try:
        print(f"📊 Profiling table: {state['table_name']}")

        df = spark.table(state["table_name"])

        if not state["columns_to_analyze"]:
            state["columns_to_analyze"] = df.columns

        state["profiling_data"] = profile_columns(
            df,
            state["columns_to_analyze"],
            state["table_name"]
        )

        print(f"✅ Profiled {len(state['columns_to_analyze'])} columns")

    except Exception as e:
        state["error"] = f"Profiling Error: {str(e)}"

    return state


def llm_type_inference_node(state: AgentState):
    if state.get("error"):
        return state

    try:
        print("🤖 Running Claude Opus 4.6 Type Inference...")

        prompt = f"""
You are a SQL datatype expert.

Rules:
- Decimal values → DECIMAL(30,2)
- Text values → STRING
- Large integers → BIGINT
- Date values → DATE
- Timestamp values → TIMESTAMP

Profiling Data:
{json.dumps(state['profiling_data'], indent=2)}

Return JSON only:
{{
  "table_name": "",
  "columns": [
    {{
      "column_name": "",
      "recommended_data_type": "",
      "reasoning": ""
    }}
  ],
  "total_columns_analyzed": 0
}}
"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a data engineering expert."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        llm_response = response.choices[0].message.content

        json_match = re.search(
            r'```json\s*(.*?)\s*```',
            llm_response,
            re.DOTALL
        )

        json_str = (
            json_match.group(1)
            if json_match
            else re.search(r'\{.*\}', llm_response, re.DOTALL).group(0)
        )

        state["schema_output"] = TableSchemaOutput(
            **json.loads(json_str)
        )

        print("✅ Type inference completed")

    except Exception as e:
        state["error"] = f"LLM Error: {str(e)}"

    return state


def output_node(state: AgentState):
    print("\n" + "=" * 80)
    print("📋 DATA TYPE RECOMMENDATIONS")
    print("=" * 80)

    if state.get("error"):
        print(f"\n❌ {state['error']}")
        return state

    schema = state["schema_output"]

    print(f"\nTable: {schema.table_name}")
    print(f"Columns Analyzed: {schema.total_columns_analyzed}\n")

    for column in schema.columns:
        print(f"Column: {column.column_name}")
        print(f"Recommended Type: {column.recommended_data_type}")
        print(f"Reasoning: {column.reasoning}\n")

    return state

# COMMAND ----------
# =============================================================================
# LangGraph Workflow
# =============================================================================
def create_datatype_definer_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("profile_data", data_profiling_node)
    workflow.add_node("infer_types", llm_type_inference_node)
    workflow.add_node("output_results", output_node)

    workflow.set_entry_point("profile_data")

    workflow.add_edge("profile_data", "infer_types")
    workflow.add_edge("infer_types", "output_results")
    workflow.add_edge("output_results", END)

    return workflow.compile()

# COMMAND ----------
# =============================================================================
# Main Execution
# =============================================================================
print("\n🚀 Creating DataType Definer Agent...\n")

datatype_agent = create_datatype_definer_workflow()

initial_state: AgentState = {
    "table_name": "{source_bronze_table}",  # Bronze table from Step 1
    "columns_to_analyze": [],
    "profiling_data": {},
    "schema_output": None,
    "error": None
}

print("🔄 Running Agent...\n")

final_state = datatype_agent.invoke(initial_state)

if final_state.get("schema_output"):
    print("\n✅ Agent execution completed successfully!")
else:
    print("\n❌ Agent execution failed")

# COMMAND ----------
# =============================================================================
# Save Results to Temp Table
# =============================================================================
import pandas as pd

# Convert Pydantic model to dictionary
schema_dict = final_state["schema_output"].dict() if hasattr(final_state["schema_output"], "dict") else final_state["schema_output"].model_dump()

# Create DataFrame from the columns list
summary_df = pd.DataFrame(schema_dict["columns"])

# Convert to Spark DataFrame
summary_spark_df = spark.createDataFrame(summary_df)

# Display recommendations
print("\n📊 Type Recommendations:")
display(summary_spark_df)

# Save to temp table for use in transformation notebook
summary_spark_df.write.mode("overwrite").saveAsTable("genie.temp.column_type_recommendations")

print("\n✅ Recommendations saved to: genie.temp.column_type_recommendations")
print("\n📋 Next Step: Review recommendations and proceed to create transformation notebook")
```

#### 4.2 Execute Data Profiling Notebook
- **Action:** Navigate to the created notebook using `openAsset` with `continueMessage: "Execute all cells in this data profiling notebook to run the AI agent, analyze bronze data, and generate intelligent type recommendations"`
- **Agent on notebook page will:** Execute all cells sequentially using `runNotebookCells`
- **Validation:** Review the AI-generated analysis results and type recommendations
- **Output Table:** Results are saved to `genie.temp.column_type_recommendations`
- **Return:** Navigate back after successful analysis
- **Output:** "✅ Step 4 Complete: Bronze data analyzed by AI agent, intelligent type recommendations generated and saved to genie.temp.column_type_recommendations"

---

### STEP 5: CREATE SILVER TRANSFORMATION NOTEBOOK

**Only execute after Step 4 is complete**

#### 5.1 Create Transformation Notebook
- **Action:** Create a Python notebook named `03_bronze_to_silver_transform`
- **Location:** `{base_path}/SRC/03_bronze_to_silver_transform`
- **Content:** Use template below with user-provided values and recommendations from Step 4

**Template for Transformation Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Bronze to Silver Transformation
# MAGIC 
# MAGIC **Source:** {source_bronze_table}
# MAGIC **Target:** {target_silver_table}
# MAGIC **Transformation Mode:** {transformation_mode}
# MAGIC 
# MAGIC This notebook performs type casting and data cleaning from bronze to silver

# COMMAND ----------
# Configuration
source_table = "{source_bronze_table}"
target_table = "{target_silver_table}"
transformation_mode = "{transformation_mode}"

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 1: Read Bronze Data

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Read bronze table
bronze_df = spark.table(source_table)

print(f"📊 Bronze table loaded: {bronze_df.count():,} rows")
print(f"📊 Columns: {len(bronze_df.columns)}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 2: Load Type Recommendations (if available)

# COMMAND ----------
try:
    recommendations_df = spark.table("temp.column_type_recommendations")
    print("✅ Using recommendations from analysis notebook")
    display(recommendations_df)
except:
    print("ℹ️ No recommendations table found - will use bronze schema as-is")
    recommendations_df = None

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 3: Apply Type Casting

# COMMAND ----------
# Create transformation based on recommendations
if recommendations_df and transformation_mode == "1":
    # Auto Type Detection mode
    print("🔄 Applying automatic type casting...")
    
    # Collect recommendations
    recs = recommendations_df.collect()
    
    # Build select expression
    select_exprs = []
    for rec in recs:
        col_name = rec['column_name']
        current_type = rec['current_type']
        recommended_type = rec['recommended_type']
        
        if current_type != recommended_type:
            # Apply casting with error handling
            if "DECIMAL" in recommended_type or "BIGINT" in recommended_type or "DOUBLE" in recommended_type:
                # Numeric casting with null on error
                select_exprs.append(
                    F.when(F.col(col_name).cast(recommended_type).isNotNull(), 
                           F.col(col_name).cast(recommended_type))
                    .otherwise(None)
                    .alias(col_name)
                )
            elif "TIMESTAMP" in recommended_type or "DATE" in recommended_type:
                # Temporal casting
                select_exprs.append(
                    F.to_timestamp(F.col(col_name)).alias(col_name)
                )
            else:
                # Keep as-is
                select_exprs.append(F.col(col_name))
        else:
            select_exprs.append(F.col(col_name))
    
    # Apply transformations
    silver_df = bronze_df.select(*select_exprs)
    
else:
    # Schema on Read or Manual mode - keep bronze schema
    print("ℹ️ Keeping bronze schema (no automatic casting)")
    silver_df = bronze_df

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 4: Check for Additional Transformation Logic

# COMMAND ----------
# Placeholder for README-based transformations
# This will be populated if user provides a README file with transformation logic
print("ℹ️ No additional transformation logic file provided")
print("ℹ️ If you have transformation rules in a README/markdown file, provide the path")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 5: Add Metadata Columns

# COMMAND ----------
# Add standard silver metadata columns
silver_df = silver_df.withColumn("silver_insert_timestamp", F.current_timestamp())
silver_df = silver_df.withColumn("silver_insert_date", F.current_date())

print("✅ Added metadata columns: silver_insert_timestamp, silver_insert_date")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 6: Preview Transformed Data

# COMMAND ----------
print("🔍 Transformed Silver Data Preview:")
display(silver_df.limit(100))

print("\n📊 Final Schema:")
silver_df.printSchema()

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 7: Write to Silver Table

# COMMAND ----------
print(f"💾 Writing to silver table: {target_table}")

# Write to silver table (overwrite mode for initial load)
silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(target_table)

final_count = spark.table(target_table).count()
print(f"\n✅ Silver table created successfully!")
print(f"📊 Final row count: {final_count:,}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 8: Validation & Statistics

# COMMAND ----------
# Read back and validate
validation_df = spark.table(target_table)

print("📊 Silver Table Statistics:")
print(f"  - Total Rows: {validation_df.count():,}")
print(f"  - Total Columns: {len(validation_df.columns)}")

# Show column statistics
print("\n📊 Column Statistics:")
display(validation_df.summary())

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 9: Compare Bronze vs Silver

# COMMAND ----------
# Compare row counts
bronze_count = spark.table(source_table).count()
silver_count = validation_df.count()

print("📊 Bronze vs Silver Comparison:")
print(f"  - Bronze rows: {bronze_count:,}")
print(f"  - Silver rows: {silver_count:,}")
print(f"  - Difference: {bronze_count - silver_count:,}")
print(f"  - Retention rate: {(silver_count/bronze_count)*100:.2f}%")

# COMMAND ----------
# MAGIC %md
# MAGIC ## ✅ Transformation Complete!
# MAGIC 
# MAGIC **Next Steps:**
# MAGIC - Review the silver table quality
# MAGIC - Set up incremental loads if needed
# MAGIC - Create gold layer aggregations
```

#### 5.2 Execute Transformation Notebook
- **Action:** Navigate to the created notebook using `openAsset` with `continueMessage: "Execute all cells in this transformation notebook to transform bronze data and load into silver"`
- **Agent on notebook page will:** Execute all cells sequentially using `runNotebookCells`
- **Validation:** Verify silver table was created and data was loaded successfully
- **Return:** Navigate back after successful transformation
- **Output:** "✅ Step 5 Complete: Bronze data transformed and loaded to silver table '{target_silver_table}'"

---

### STEP 6: APPLY ADDITIONAL TRANSFORMATIONS (OPTIONAL)

**MANDATORY: Step 4 already read reference file, now apply the transformations and ask about user's README file**

#### 6.1 Confirm Transformation Rules Already Loaded
- **Note:** The transformation reference file was already read and parsed in Step 4
- **Available as:** `standard_transformation_rules` (from Step 4 analysis)
- **Action:** Retrieve the transformation rules identified in Step 4

#### 6.2 Ask User for Additional README File
- **Action:** Ask the user:
- **Question:** "In Step 4, I already loaded the standard transformation rules from the reference file. Do you have an additional README or markdown file with custom transformation logic? If yes, please provide the file path. If no, I'll proceed with the standard transformations only."
- **Store as:** `readme_file_path`
- **If user provides path, proceed to 6.3**
- **If no additional file, proceed to 6.4 with standard rules only**

#### 6.3 Read and Merge User's README File (if provided)
- **Action:** Read the user's README file content
- **Parse for:** 
  - Column transformations
  - Business logic rules
  - Calculated fields
  - Filters or conditions
  - Aggregations
- **Store as:** `custom_transformation_rules`
- **Merge:** Combine `standard_transformation_rules` with `custom_transformation_rules`

#### 6.4 Create Additional Transformation Notebook
- **Action:** Create a Python notebook named `04_apply_transformations`
- **Location:** `{base_path}/SRC/04_apply_transformations`
- **Content:** Use template below

**Template for Transformation Notebook:**
```python
# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # Apply Additional Transformations
# MAGIC 
# MAGIC **Source:** {target_silver_table}
# MAGIC **Standard Reference:** /Workspace/.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformstions.md
# MAGIC **Custom README:** {readme_file_path if provided else "None"}
# MAGIC 
# MAGIC This notebook applies business logic transformations defined in reference files

# COMMAND ----------
# Configuration
source_table = "{target_silver_table}"
reference_path = "/Workspace/.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformstions.md"
readme_path = "{readme_file_path}"  # Empty if not provided

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 1: Read Current Silver Table

# COMMAND ----------
from pyspark.sql import functions as F
from pyspark.sql.types import *

# Read current silver table
silver_df = spark.table(source_table)

print(f"📊 Current silver table loaded: {silver_df.count():,} rows")
print(f"📊 Available columns: {silver_df.columns}")
silver_df.printSchema()

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 2: Display Reference Transformation Rules

# COMMAND ----------
print("📄 Standard Transformation Reference:")
print("=" * 80)
print("""
{standard_transformation_rules}
""")
print("=" * 80)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 3: Apply Standard Transformations

# COMMAND ----------
# AI Agent will parse the reference file and generate specific transformation code here
# Example transformations based on the reference file:

# 1. Calculate total_price (check if price and units/qty exist)
if "price" in silver_df.columns:
    if "units" in silver_df.columns:
        silver_df = silver_df.withColumn("total_price", F.col("price") * F.col("units"))
        print("✅ Created total_price = price * units")
    elif "qty" in silver_df.columns:
        silver_df = silver_df.withColumn("total_price", F.col("price") * F.col("qty"))
        print("✅ Created total_price = price * qty")
    else:
        print("ℹ️ Skipping total_price calculation - no units or qty column found")
else:
    print("ℹ️ Skipping total_price calculation - no price column found")

# 2. Standardize customer names to uppercase
customer_name_columns = [col for col in silver_df.columns if "customer" in col.lower() and "name" in col.lower()]
for col_name in customer_name_columns:
    silver_df = silver_df.withColumn(col_name, F.upper(F.col(col_name)))
    print(f"✅ Converted {col_name} to uppercase")

if not customer_name_columns:
    print("ℹ️ No customer name columns found for uppercase conversion")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 4: Apply Custom Transformations (if README provided)

# COMMAND ----------
# If user provided additional README file, custom transformations will be added here
# AI Agent will parse the custom README and generate additional transformation code

{custom_transformation_code}

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 5: Preview Transformed Data

# COMMAND ----------
print("🔍 Preview after all transformations:")
display(silver_df.limit(100))

print("\n📊 Final Schema:")
silver_df.printSchema()

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 6: Update Silver Table

# COMMAND ----------
print(f"💾 Updating silver table: {source_table}")

# Write back to silver table
silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(source_table)

final_count = spark.table(source_table).count()
print(f"\n✅ Silver table updated with all transformations!")
print(f"📊 Final row count: {final_count:,}")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Step 7: Verify Transformations

# COMMAND ----------
# Verify new columns were created
result_df = spark.table(source_table)
print("📊 Final Column List:")
for col in result_df.columns:
    print(f"  - {col}")

print("\n✅ All transformations applied successfully!")

# COMMAND ----------
# MAGIC %md
# MAGIC ## ✅ Transformations Complete!
```

#### 6.5 AI Agent Processes Transformation Files
- **Action:** AI agent uses transformation rules already identified in Step 4
- **Analyzes:** Transformation logic described in markdown format
- **Generates:** Python/PySpark code to implement all transformations
- **Updates:** The notebook cells with actual transformation code
- **Standard Reference Examples:**
  - "Calculate total_price as quantity * unit_price" → `silver_df.withColumn("total_price", F.col("quantity") * F.col("unit_price"))`
  - "Convert customer_name to uppercase" → `silver_df.withColumn("customer_name", F.upper(F.col("customer_name")))`
- **Custom README Examples:**
  - "Filter out records where status is 'cancelled'" → `silver_df.filter(F.col("status") != "cancelled")`
  - "Create age_category based on age ranges" → Conditional logic with F.when()

#### 6.6 Execute Transformation Notebook
- **Action:** Navigate to the created notebook using `openAsset` with `continueMessage: "Execute all cells to apply standard and custom transformations"`
- **Agent on notebook page will:** Execute all cells sequentially using `runNotebookCells`
- **Validation:** Verify transformations were applied successfully
- **Return:** Navigate back after successful transformation
- **Output:** "✅ Step 6 Complete: All transformations (standard + custom) applied to silver table"

---

## 🎉 COMPLETION CHECKLIST

After completing all steps, verify:

- ✅ Directory structure created (`{base_path}/DDL` and `{base_path}/SRC`)
- ✅ Silver catalog and schema created (`{target_catalog}.{target_schema}`)
- ✅ Transformation reference file read in Step 4
- ✅ Bronze data analyzed and type recommendations generated
- ✅ Calculated fields identified from transformation rules
- ✅ Silver table created with proper data types
- ✅ Metadata columns added to silver table
- ✅ Standard transformations applied from reference file
- ✅ Custom transformations applied (if README provided)
- ✅ All notebooks executed successfully

**Final Output Message:**
```
🎉 Silver Layer Setup Complete!

📊 Summary:
  - Source Bronze: {source_bronze_table}
  - Target Silver: {target_silver_table}
  - Transformation Mode: {transformation_mode}
  - Standard Transformations: Applied from reference file
  - Custom Transformations: {readme_file_path if provided else "None"}

📂 Created Notebooks:
  1. {base_path}/00_setup_silver_structure
  2. {base_path}/DDL/01_setup_silver_catalog_schema
  3. {base_path}/SRC/02_analyze_bronze_data
  4. {base_path}/SRC/03_bronze_to_silver_transform
  5. {base_path}/SRC/04_apply_transformations

✅ Your silver layer is ready for use!

📋 Next Steps:
  - Review data quality in silver table
  - Set up incremental refresh if needed
  - Create gold layer aggregations for reporting
```

---

## 🔧 TROUBLESHOOTING

### Issue: Type casting fails for certain columns
**Solution:** Check the data profiling results - some columns may need custom casting logic. Modify the transformation notebook to handle edge cases.

### Issue: Bronze table not found
**Solution:** Verify the bronze table name is correct and accessible. Run `DESCRIBE TABLE {source_bronze_table}` to check permissions.

### Issue: Decimal precision loss
**Solution:** Increase DECIMAL precision in the transformation notebook. Default is DECIMAL(30,2) - adjust based on your data.

### Issue: Reference file not found
**Solution:** Verify the reference file exists at `/Workspace/.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformstions.md`. If missing, create it with standard transformation rules.

### Issue: README file not accessible
**Solution:** Verify the file path is correct and the file exists in the workspace. Use absolute paths starting with `/Workspace/`.

### Issue: Transformations not working as expected
**Solution:** Review the generated code in Step 3 of the transformation notebook. Check if source columns exist with correct names. You may need to manually adjust the logic based on your specific schema.

### Issue: Column not found during transformation
**Solution:** The transformation logic checks for column existence before applying transformations. If a column is missing, the transformation is skipped. Review your bronze schema to ensure expected columns are present.

### Issue: Cannot read transformation reference file in Step 4
**Solution:** The file path may be incorrect. Verify the file exists at `/Workspace/.assistant/skills/kpi_alchemist/2_silver_load/references/Tranformstions.md`. The notebook uses Python's `open()` function, so ensure the path is accessible.

---

## 📚 ADDITIONAL NOTES

**Data Type Mapping Guidelines:**
- String with only numbers → BIGINT or DECIMAL
- String with dates → TIMESTAMP or DATE
- String with true/false → BOOLEAN
- String with mixed content → STRING
- Large numbers → BIGINT (for integers) or DOUBLE (for floats)
- Financial data → DECIMAL(30,2) or appropriate precision

**Reference File Format (Tranformstions.md):**
The standard reference file should follow this format:
```markdown
## Data Transformation Steps

1. **Calculate `field_name`:**
   - Description of calculation logic

2. **Standardize field_name:**
   - Description of standardization logic
```

**Custom README File Format Guidelines:**
For custom transformations, structure your README as:
```markdown
# Custom Transformation Rules

## Calculated Fields
- field_name = calculation logic
- another_field = another calculation

## String Transformations
- field_name: conversion logic
- email: lowercase and trim

## Conditional Logic
- status_field: if condition then value, else other_value

## Date Calculations
- days_field = current_date - other_date

## Filters
- Remove records where condition
- Keep only records where condition
```

**Best Practices:**
1. Always profile bronze data before transformation
2. Read transformation reference file in Step 4 to understand calculated field requirements
3. Review type recommendations before applying - ensure source columns for calculations are properly typed
4. Test transformations on a sample first
5. Document any custom casting logic
6. Keep reference file updated with standard transformations
7. Use custom README files for project-specific business logic
8. Keep transformation notebooks versioned
9. Validate results after each transformation step
10. Check column existence before applying transformations
11. Log all transformation steps for audit trail
12. Verify source columns for calculated fields are cast to appropriate numeric types
