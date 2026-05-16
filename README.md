# KPI Genie - Custom Skills for Databricks

This repository contains custom skills for Genie Code (Databricks AI Assistant) to streamline data engineering workflows.

---

## 📁 Folder Structure

To use custom skills, your folder structure should look like this:

```
/Users/<your_email>/
├── .assistant/
│   ├── skills/
│   │   └── kpi_alchemist/
│   │       └── 1_bronze_load/
│   │           ├── bronze_data_loader.md  # Main skill file
│   │           └── scripts/               # Optional helper scripts
│   └── .assistant_instructions.md         # Global assistant instructions
└── kpi_genie/                             # Your project folder
    └── README.md                          # This file
```

**Important:** The `.assistant` folder must be placed in your **user home directory**:
* Path: `/Users/<your_email>/.assistant/`
* This is where Genie Code looks for custom skills and instructions

---

## 🚀 How to Use Skills

### Method 1: Using @skill_name (Recommended)

In any Genie Code chat, type `@` followed by the skill name to invoke it:

```
@bronze_data_loader
```

This will:
1. Load the skill automatically
2. Guide you through the step-by-step workflow
3. Execute the bronze data ingestion process

### Method 2: Natural Language Trigger

Based on your `.assistant_instructions.md`, you can use natural language:

```
Load Bronze
```

or

```
Ingest to Bronze
```

Genie Code will:
1. Detect the intent
2. Prompt you to use the custom skill
3. Load `bronze_data_loader` skill when you confirm

---

## 📚 Available Skills

### 1. **bronze_data_loader**
**Location:** `.assistant/skills/kpi_alchemist/1_bronze_load/bronze_data_loader.md`

**Purpose:** Automated bronze layer data ingestion with step-by-step guidance

**What it does:**
* Gathers all required inputs (target table, source type, configurations)
* Creates directory structure for your project
* Generates and executes DDL notebook for catalog/schema setup
* Creates and executes data ingestion notebook (10 source patterns supported)
* Creates and executes validation notebook
* Provides complete execution results and quality checks

**Supported Source Types:**
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

**Example Usage:**
```
@bronze_data_loader
```

Then follow the prompts:
1. Provide project location (default: `/Workspace/Users/{username}/ProjectIngestion/Bronze`)
2. Provide target table (format: `catalog_name.schema_name.table_name`)
3. Choose data source type
4. Provide source-specific configurations
5. Confirm and let it create + execute all notebooks

---

## ⚙️ Setup Instructions

### Step 1: Create the .assistant Folder

```bash
# In Databricks workspace, create the folder structure
mkdir -p /Users/<your_email>/.assistant/skills/kpi_alchemist/1_bronze_load/
```

### Step 2: Upload Skill Files

Place your skill files in the appropriate location:
* `bronze_data_loader.md` → `/Users/<your_email>/.assistant/skills/kpi_alchemist/1_bronze_load/`

### Step 3: Create Assistant Instructions (Optional)

Create `/Users/<your_email>/.assistant/.assistant_instructions.md` with:

```markdown
# Major instructions
- Always prompt the user to check if their query relates to custom skills, allowing you to load the appropriate skill file.
- If user says 'Load Bronze' or 'Ingest to Bronze' Then prompt user to continue with custom skill available?
- Skill file: bronze_data_loader
```

### Step 4: Test Your Skill

Open any notebook or chat in Databricks and type:
```
@bronze_data_loader
```

Genie Code should recognize and load your skill!

---

## 🔧 How Skills Work

1. **Skill Discovery:** Genie Code scans `/Users/<your_email>/.assistant/skills/` for available skills
2. **Skill Loading:** When you use `@skill_name`, Genie Code loads the corresponding `.md` file
3. **Guided Workflow:** The skill provides step-by-step instructions to Genie Code
4. **Automation:** Genie Code follows the skill's template to create and execute notebooks
5. **Validation:** Each step includes validation and execution to ensure success

---

## 📝 Skill File Format

Skills are written in Markdown with special sections:

```markdown
# Skill Name

## 🎯 Skill Purpose
Description of what the skill does

## ⚠️ AGENT INSTRUCTIONS
Critical rules for Genie Code to follow

## 📋 STEP-BY-STEP WORKFLOW
Sequential steps with templates and validation

## 📚 APPENDIX
Code patterns and examples
```

---

## 🎯 Best Practices

1. **Always use fully qualified table names:** `catalog_name.schema_name.table_name`
2. **Let skills execute notebooks:** Don't manually run - skills handle execution automatically
3. **Review execution results:** Check the output after each step completes
4. **Follow the workflow:** Skills are designed to be executed sequentially
5. **Provide accurate inputs:** Wrong configurations may cause failures during execution

---

## 🐛 Troubleshooting

### Issue: Skill not found
**Solution:** Verify the folder structure:
```bash
ls -la /Users/<your_email>/.assistant/skills/kpi_alchemist/1_bronze_load/
```

### Issue: Permission errors during execution
**Solution:** Ensure you have:
* CREATE CATALOG permissions
* CREATE SCHEMA permissions
* CREATE TABLE permissions

### Issue: Skill loads but doesn't execute
**Solution:** 
* Check if all required inputs were provided
* Review error messages in notebook execution results
* Verify source paths and connection details are correct

---

## 📖 Example: Complete Bronze Load Workflow

```
User: @bronze_data_loader

Genie: Let me gather the required information for bronze ingestion.
       Where would you like to keep your bronze ingestion code files?

User: /Workspace/Users/myemail/DataPipelines/Bronze

Genie: What is your target table? (format: catalog_name.schema_name.table_name)

User: analytics.bronze.customers

Genie: What storage location for the database/schema? (press Enter to skip)

User: [Enter]

Genie: What type of data source will you ingest from?
       1. CSV Files from Volumes
       2. JSON Files from Volumes
       ...

User: 1

Genie: [Gathers remaining inputs...]
       [Creates directory structure...]
       [Executes DDL notebook...]
       [Executes ingestion notebook...]
       [Executes validation notebook...]
       
       ✅ Bronze Ingestion Setup Complete!
       Records Loaded: 45,678
       All validations passed!
```

---

## 🤝 Contributing

To add new skills:

1. Create a new folder under `.assistant/skills/`
2. Write your skill file in Markdown format
3. Follow the bronze_data_loader.md structure as a template
4. Add skill name to `.assistant_instructions.md`
5. Test thoroughly with different scenarios

---

## 📄 License

This project is part of your personal Databricks workspace configuration.

---

## 📞 Support

For issues or questions:
* Review skill documentation in the `.md` files
* Check Databricks Genie Code documentation
* Test with simpler configurations first

---

**Happy Data Engineering! 🚀**
