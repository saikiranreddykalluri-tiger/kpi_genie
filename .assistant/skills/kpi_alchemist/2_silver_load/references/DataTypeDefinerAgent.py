# =============================================================================
# Install Required Libraries
# =============================================================================
!pip install langgraph==0.2.65 langchain==0.3.16 langchain-core==0.3.32 \
pydantic==2.10.6 sqlparse==0.5.3 openai==1.59.7 --quiet

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

# =============================================================================
# Main Execution
# =============================================================================
print("\n🚀 Creating DataType Definer Agent...\n")

datatype_agent = create_datatype_definer_workflow()

initial_state: AgentState = {
    "table_name": "YOUR_BRONZE_TABLE", #example: genie.bronze.retail
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
    

import pandas as pd

# Convert Pydantic model to dictionary, then extract columns list
schema_dict = final_state["schema_output"].dict() if hasattr(final_state["schema_output"], "dict") else final_state["schema_output"].model_dump()

# Create DataFrame from the columns list
summary_df = pd.DataFrame(schema_dict["columns"])

# Convert to Spark DataFrame
summary_df = spark.createDataFrame(summary_df)

summary_df.write.mode("overwrite").saveAsTable("genie.temp.column_type_recommendations")
