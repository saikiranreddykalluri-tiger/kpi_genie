# Gold Data Load - Automated KPI Generation Skill

## Overview
This skill automates the creation of Gold-layer KPI views from Silver tables. It analyzes source tables, generates aggregated KPI views, and creates them in your target catalog/schema.

## Prerequisites
- Silver table(s) loaded and ready
- Target catalog and schema created in Unity Catalog
- Access to the Automated KPI Generation System notebook

## Workflow

### Step 1: Project Folder Setup
**First, ask the user for their project folder path where gold notebooks should be created.**

Example prompt:
```
"What is your project folder path where you'd like to set up the Gold layer notebooks?"
```

Expected format: `/<path>/<to>/<project>/gold` or `/Users/<username>/<project_name>/gold`

### Step 2: Import Reference Notebook
Once the project folder is confirmed, import the Automated KPI Generation System notebook:

**Source notebook location:**
```
./references/Automated KPI Generation System
```

**Import to:**
```
<user_project_folder>/Automated KPI Generation System
```

Use the following approach:
1. Read the reference notebook using `readAssetById`
2. Create a new notebook in the user's project folder
3. Copy the cell content from reference to the new notebook

### Step 3: Create Trigger Notebook
**Create a separate trigger notebook that imports and executes the KPI generation:**

**Trigger notebook name:**
```
<user_project_folder>/Run_KPI_Generation
```

**Trigger notebook structure:**

**Cell 1: Import the main notebook**
```python
%run "./Automated KPI Generation System"
```

**Cell 2: Configuration and Execution**
```python
# ⚠️ IMPORTANT: Update the configuration below before running
# Set these to your actual source and target details

SOURCE_TABLE_FULL = "catalog.schema.table_name"  # e.g., "main.silver.sales_data"
TARGET_CATALOG = "main"  # Target catalog for KPI views
TARGET_SCHEMA = "gold_kpis"  # Target schema for KPI views

# Run KPI generation
result = run_kpi_generation(
    source_table=SOURCE_TABLE_FULL,
    target_catalog=TARGET_CATALOG,
    target_schema=TARGET_SCHEMA
)

# Display results
final_df = spark.createDataFrame(result['kpis'])
display(final_df)

print("✅ KPI Generation Complete!")
```

### Step 4: Guide User Execution
**Inform the user to:**

1. **Update the configuration in Cell 2** of the trigger notebook:
   * `SOURCE_TABLE_FULL` - Full path to source silver table (catalog.schema.table)
   * `TARGET_CATALOG` - Target catalog for KPI views
   * `TARGET_SCHEMA` - Target schema for KPI views

2. **Run the trigger notebook** to execute KPI generation

3. **Review the results** displayed in the output

Example configuration:
```python
SOURCE_TABLE_FULL = "main.silver.sales_data"
TARGET_CATALOG = "main"
TARGET_SCHEMA = "gold_kpis"
```

## What This System Does

1. **Analyzes Source Table**: Reads the silver table schema and data
2. **Identifies KPI Opportunities**: Determines which columns can be aggregated (numeric, categorical, date-based)
3. **Generates KPI Views**: Creates views with aggregations like:
   - COUNT, SUM, AVG, MIN, MAX for numeric columns
   - COUNT, DISTINCT COUNT for categorical columns
   - Time-based aggregations (daily, weekly, monthly)
4. **Creates Views in Target Schema**: Deploys the KPI views to your specified gold layer

## Assistant Workflow

When a user requests "Load Gold" or "Create KPI Views":

1. **Ask for project folder**: "Where would you like to set up your Gold layer notebooks?"
2. **Ask for source and target details**:
   - Source silver table (catalog.schema.table)
   - Target catalog and schema for gold views
3. **Import the reference notebook**: Copy from references to their project folder
4. **Create the trigger notebook**: Set up the %run import and configuration template
5. **Guide execution**: Provide clear instructions for updating configuration and running
6. **Verify results**: Help interpret the generated KPI views

## Common Patterns

### Multiple Source Tables
If user has multiple silver tables, they can:
- Create separate trigger notebooks for each table
- Or create a loop in the trigger notebook to process multiple tables
- Update configuration for each table run

### Custom KPI Logic
If user needs custom KPIs beyond auto-generated ones:
- Start with auto-generation for baseline views
- Add custom KPI definitions manually after
- Explain which views were auto-created vs custom

## Error Handling

Common issues:
* **Table not found**: Verify SOURCE_TABLE_FULL is correct and accessible
* **Permission denied**: Check user has CREATE VIEW permission on target schema
* **Schema not found**: Ensure target catalog and schema exist before running
* **Function not found**: Ensure %run successfully imported the main notebook

## Best Practices

1. **Use separate trigger notebook** for clean separation of logic and execution
2. **Document configuration** in the trigger notebook for team reference
3. **Test with small tables first** before running on large datasets
4. **Review generated KPIs** in the output before proceeding
5. **Use descriptive target schema names** like `gold_sales_kpis` or `gold_metrics`

## Example Full Interaction

```
User: "Load Gold for my sales data"