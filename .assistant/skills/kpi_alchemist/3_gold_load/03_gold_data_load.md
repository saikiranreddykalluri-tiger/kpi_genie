# Gold Data Load - Automated KPI Generation Skill

## Overview
This skill automates the creation of Gold-layer KPI views from Silver tables. It analyzes source tables, generates aggregated KPI views, and creates them in your target catalog/schema.

## Prerequisites
- Silver table(s) loaded and ready
- Target catalog and schema created in Unity Catalog
- Access to the Automated KPI Generation System notebook

## Workflow

### Step 1: Gather Project Configuration
**Ask the user for the following information:**

1. **Project folder path** where the Gold notebook should be created
   - Example: `/Users/<username>/<project_name>/gold`
   - Example: `/<path>/<to>/<project>/gold`

2. **Source silver table** (full path: catalog.schema.table)
   - Example: `main.silver.sales_data`
   - This will be parsed into:
     - `SOURCE_CATALOG`: The catalog name
     - `SOURCE_SCHEMA`: The schema name
     - `SOURCE_TABLE`: The table name

3. **Target catalog** for KPI views
   - Example: `main`

4. **Target schema** for KPI views
   - Example: `gold_kpis`

### Step 2: Clone and Configure Notebook
Once all configuration details are collected:

**Source notebook location:**
```
./references/Automated KPI Generation System
```

**Clone to:**
```
<user_project_folder>/Automated KPI Generation System
```

**Configuration replacement:**
Replace the configuration variables in the cloned notebook with user inputs:

```python
# Original placeholders:
SOURCE_CATALOG = "your_catalog_name"
SOURCE_SCHEMA = "your_schema_name"
SOURCE_TABLE = "your_table_name"
TARGET_CATALOG = "your_target_catalog"
TARGET_SCHEMA = "your_target_schema"

# Replace with user-provided values:
SOURCE_CATALOG = "<parsed_from_source_table>"
SOURCE_SCHEMA = "<parsed_from_source_table>"
SOURCE_TABLE = "<parsed_from_source_table>"
TARGET_CATALOG = "<user_target_catalog>"
TARGET_SCHEMA = "<user_target_schema>"
```

### Step 3: Clone Process
Use the following approach:
1. Read the reference notebook using `readAssetById`
2. Parse the source table path to extract catalog, schema, and table name
3. Create a new notebook in the user's project folder
4. Copy all cells from reference to the new notebook
5. Update the configuration cell with actual values

### Step 4: Guide User Execution
**Inform the user:**

1. **Review the configuration** in the cloned notebook to ensure it's correct
2. **Run the notebook** to execute KPI generation
3. **Review the results** displayed in the output

The notebook will automatically:
- Analyze the source silver table
- Identify KPI opportunities
- Generate and create KPI views in the target schema

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

1. **Ask for project folder**: "Where would you like to set up your Gold layer notebook?"
2. **Ask for source silver table**: "What is the full path to your source silver table? (format: catalog.schema.table)"
3. **Ask for target details**:
   - "Which catalog should I create the KPI views in?"
   - "Which schema should I create the KPI views in?"
4. **Parse the source table path**: Split catalog.schema.table into individual components
5. **Clone the reference notebook**: Copy to user's project folder
6. **Update configuration**: Replace placeholder variables with actual values
7. **Confirm setup**: Inform user the notebook is ready to run
8. **Guide execution**: Provide clear instructions for running the notebook

## Configuration Parsing Example

If user provides: `main.silver.sales_data`

Parse into:
- `SOURCE_CATALOG = "main"`
- `SOURCE_SCHEMA = "silver"`
- `SOURCE_TABLE = "sales_data"`

If user provides:
- Target catalog: `main`
- Target schema: `gold_kpis`

Set:
- `TARGET_CATALOG = "main"`
- `TARGET_SCHEMA = "gold_kpis"`

## Common Patterns

### Multiple Source Tables
If user has multiple silver tables, they can:
- Clone the notebook multiple times, one for each table
- Or run the notebook multiple times with different configurations
- Create separate notebooks with descriptive names (e.g., "KPI Gen - Sales", "KPI Gen - Inventory")

### Custom KPI Logic
If user needs custom KPIs beyond auto-generated ones:
- Start with auto-generation for baseline views
- Add custom KPI definitions manually after
- Modify the cloned notebook to include additional logic

## Error Handling

Common issues:
* **Table not found**: Verify source table path is correct and accessible
* **Permission denied**: Check user has CREATE VIEW permission on target schema
* **Schema not found**: Ensure target catalog and schema exist before running
* **Invalid table path**: Ensure source table follows catalog.schema.table format

## Best Practices

1. **Validate inputs** before cloning the notebook
2. **Use descriptive target schema names** like `gold_sales_kpis` or `gold_metrics`
3. **Test with small tables first** before running on large datasets
4. **Review generated KPIs** in the output before proceeding
5. **Keep the reference notebook unchanged** for future use

## Example Full Interaction

```
User: "Load Gold for my sales data"
Assistant: "I'll help you set up automated KPI generation. I need a few details:

1. Where would you like to set up your Gold layer notebook?
2. What is the full path to your source silver table? (format: catalog.schema.table)
3. Which catalog should I create the KPI views in?
4. Which schema should I create the KPI views in?"

User: "Project folder: /Users/myname/sales_project/gold
Source table: main.silver.sales_data
Target: main catalog, gold_kpis schema"