# KPI Alchemist: Agentic Analytics Accelerator

## Problem Statement

Organizations struggle to rapidly derive business insights from raw client/source data. Manual analytics setup is time-consuming, requires deep technical expertise, and slows down client onboarding. Teams need a scalable, reusable framework that:

* Accelerates proof-of-concept delivery
* Reduces manual scaffolding effort
* Automates data understanding and KPI generation
* Provides metadata-driven development approach
* Enables faster client demos and showcases

## Solution Overview

KPI Alchemist is an Agentic AI-driven analytics accelerator powered by Databricks Genie Code and skill-based orchestration. It transforms source data into production-ready KPI views through intelligent skill coordination.

**Core Capabilities:**

* Automatic source data understanding and ingestion (10+ source types)
* Intelligent data type detection and casting
* Automated KPI view generation with business logic
* SQL/PySpark code generation through skills
* Medallion architecture scaffolding (Bronze → Silver → Gold)
* Extensible skill-based architecture for future agents

**Architecture Philosophy: "Skill is King"**

The framework operates on a fundamental principle: skills define intelligence and execution flow. Agents are skill orchestrators—they collaborate through structured skill files that encode domain expertise, transformation logic, and workflow patterns. Skills are modular, reusable, and the foundation of all system capabilities.

## Tech Stack

* **Databricks Genie Code** — AI-powered workspace assistant
* **Claude Sonnet 4.6** — LLM for skill interpretation and code generation
* **Databricks Unity Catalog** — Governance and metadata management
* **Delta Lake** — ACID-compliant data storage
* **PySpark** — Distributed data processing
* **Databricks SQL** — Analytics and KPI queries
* **Medallion Architecture** — Bronze/Silver/Gold layers
* **Skill-Based Framework** — Modular AI agent orchestration
* **AI Gateway** — Secure LLM access and routing

## Architecture Summary

**Skill-Driven Design Pattern:**

```
User Request → Genie Code → Skill Loader → Skill Orchestrator → Code Generator → Validator → Output
```

**Three-Layer Orchestration:**

1. **Bronze Layer (Ingestion Agent)**
   * Reads 10+ source types (CSV, JSON, Parquet, JDBC, S3, Azure, Auto Loader, Delta, Merge/Upsert)
   * Preserves raw data integrity (STRING types for files, native types for RDBMS)
   * Creates catalog/schema structure
   * Generates ingestion notebooks with validation

2. **Silver Layer (Transformation Agent)**
   * Analyzes bronze data quality and patterns
   * Intelligent data type casting and inference
   * Applies business transformation rules from reference files
   * Null handling and standardization
   * Creates clean, typed datasets

3. **Gold Layer (KPI Generation Agent)**
   * Automated KPI view generation from silver tables
   * Applies null filling strategies (fillna logic)
   * Generates aggregation views (COUNT, SUM, AVG, MIN, MAX, DISTINCT)
   * Time-based rollups (daily, weekly, monthly)
   * Deploys production-ready KPI views to Unity Catalog

**Skill Orchestration Mechanism:**

* Skills stored at: `/Workspace/.assistant/skills/kpi_alchemist/`
* Each layer has dedicated skill files with templates and patterns
* Genie Code interprets skills and generates layer-specific notebooks
* Skills include validation logic, error handling, and execution guidance
* Extensible for future agents (forecasting, anomaly detection, lineage tracking)

**Metadata Interpretation:**

* Skills parse user inputs (table names, paths, source types)
* Extract catalog/schema/table components automatically
* Apply transformation reference files for business logic
* Generate executable notebooks with pre-configured parameters

## Setup Instructions

**Prerequisites:**

* Databricks workspace with Unity Catalog enabled
* Cluster with DBR 13.3+ (Serverless recommended)
* Permissions to create catalogs, schemas, and tables
* Access to source data (files, databases, cloud storage)

**Installation Steps:**

1. **Clone Skill Repository:**
   ```bash
   # Skills should be placed at:
   /Workspace/.assistant/skills/kpi_alchemist/
   ```

2. **Verify Skill Structure:**
   ```
   kpi_alchemist/
   ├── 1_bronze_load/
   │   └── bronze_data_loader.md
   ├── 2_silver_load/
   │   ├── silver_data_loader.md
   │   └── references/
   │       └── Transformations.md
   └── 3_gold_load/
       ├── 03_gold_data_load.md
       └── references/
           └── Automated KPI Generation System (notebook)
   ```

3. **Configure Workspace Instructions:**
   Add to `.assistant_workspace_instructions.md`:
   ```markdown
   If request relates to 'Load Bronze' or 'Ingest to Bronze', load skill:
   /Workspace/.assistant/skills/kpi_alchemist/1_bronze_load/bronze_data_loader.md
   
   If request relates to 'Load Gold' or 'Create KPI Views', load skill:
   /Workspace/.assistant/skills/kpi_alchemist/3_gold_load/03_gold_data_load.md
   ```

4. **Install Dependencies:**
   No additional libraries required—runs on Databricks Runtime.

5. **Set Up Unity Catalog:**
   Create target catalogs (or let skills auto-create):
   ```sql
   CREATE CATALOG IF NOT EXISTS main;
   CREATE SCHEMA IF NOT EXISTS main.bronze;
   CREATE SCHEMA IF NOT EXISTS main.silver;
   CREATE SCHEMA IF NOT EXISTS main.gold;
   ```

## Run Instructions

**End-to-End Workflow:**

### Step 1: Bronze Data Ingestion

1. Open Databricks Genie Code chat
2. Say: **"Load Bronze"** or **"Ingest to Bronze"**
3. Genie loads the bronze skill and asks for:
   * Project folder path
   * Target table name (catalog.schema.table)
   * Source type (CSV, JSON, Parquet, JDBC, S3, Azure, etc.)
   * Source-specific configuration (path, credentials, format options)
4. Confirm inputs
5. Genie creates:
   * Directory structure (DDL, SRC folders)
   * Catalog/schema setup notebook
   * Source-specific ingestion notebook
6. Genie auto-executes notebooks and validates data load

### Step 2: Silver Data Transformation

1. Say: **"Load Silver"** or **"Transform to Silver"**
2. Genie loads the silver skill and asks for:
   * Project folder path
   * Source bronze table (catalog.schema.table)
   * Target silver table (catalog.schema.table)
   * Transformation mode (Auto Type Detection recommended)
3. Genie reads transformation reference file
4. Genie creates:
   * Directory structure
   * Schema setup notebook
   * Data profiling notebook (analyzes types, nulls, patterns)
   * Transformation notebook (applies casting and business logic)
5. Genie executes notebooks and validates clean data

### Step 3: Gold KPI Generation

1. Say: **"Load Gold"** or **"Create KPI Views"**
2. Genie loads the gold skill and asks for:
   * Project folder path
   * Source silver table (catalog.schema.table)
   * Target catalog and schema for KPI views
3. Genie clones KPI generation system notebook
4. Genie configures source/target details
5. Genie adds null handling logic (fillna strategies)
6. Execute the generated notebook to:
   * Analyze silver table schema
   * Identify KPI opportunities
   * Generate aggregation views
   * Deploy views to gold schema

**Quick Start Example:**

```
User: "Load Bronze for CSV files"
Genie: [Loads bronze skill, asks questions]
User: [Provides: path, target table, CSV options]
Genie: [Creates structure, ingests data, validates]

User: "Transform to Silver with auto type detection"
Genie: [Loads silver skill, asks for bronze table]
User: [Confirms bronze table, transformation mode]
Genie: [Profiles data, applies transformations, creates silver table]

User: "Generate KPIs from silver table"
Genie: [Loads gold skill, asks for target schema]
User: [Provides gold schema details]
Genie: [Creates KPI views: sales by region, daily revenue, top products, etc.]
```

**Validate Outputs:**

```sql
-- Check bronze data
SELECT * FROM main.bronze.your_table LIMIT 10;

-- Check silver cleaned data
SELECT * FROM main.silver.your_table_clean LIMIT 10;

-- Check generated KPIs
SHOW VIEWS IN main.gold;
SELECT * FROM main.gold.kpi_sales_by_region;
```

## Key Differentiators

* **Zero-Code User Experience:** Users provide data details; skills generate all code
* **Skill-Centric Intelligence:** All logic encoded in reusable skill files
* **Rapid Prototyping:** From raw data to KPI dashboard in under 15 minutes
* **Metadata-Driven:** Automatic parsing of table names, paths, and data types
* **Extensible Framework:** Easy to add new skills for forecasting, anomaly detection, lineage
* **Production-Ready Outputs:** Generated notebooks follow best practices and include validations
* **Modular Agent Collaboration:** Skills orchestrate multi-agent workflows seamlessly

## Future Enhancements

* **Forecasting Agent:** Time-series prediction KPIs using Prophet/ARIMA
* **Anomaly Detection Agent:** Auto-detect outliers and data quality issues
* **Lineage Tracking Agent:** Visualize data flows across medallion layers
* **Schema Evolution Agent:** Handle schema changes automatically
* **Cost Optimization Agent:** Recommend partitioning and clustering strategies
* **Governance Agent:** Auto-tag PII, apply row-level security, audit access

---

**Team Alchemist** | Theme 1: Agentic AI for Tech | TPL Hackathon 2026

*"Skill is King — Intelligence encoded, agents orchestrated, insights delivered."*
