## Data Transformation Steps

1. **Calculate `total_price`:**
   - Compute `total_price` by multiplying `price` with either `units` or `qty` (depending on which column is present).

2. **Standardize Customer Names:**
   - Convert all customer name columns to upper case for consistency.

3. **Handle Multiple Date Formats:**
   - Parse the `Date` column to handle both `MM-DD-YY` and `M/D/YYYY` formats.
   - Once all tranformations are applied, remove the records where it is null

4. **Prefer BIGINTs, DECIMAL(30,2), STRING Data Types:**
   - Where applicable, cast columns to `BIGINT`, `DECIMAL(30,2)`, or `STRING` data types as appropriate. Do not apply to phone number columns. Only apply where necessary.

---

## Silver Layer Must-Have Rules

1. **Data Quality Validation:**
   - Verify source data exists or not

2. **Deduplication:**
   - For now ignore this step

3. **Schema Standardization:**
   - Enforce consistent column naming conventions across all silver tables (e.g., snake_case).
   - Maintain uniform data types for similar columns across different silver tables.

4. **Audit Columns:**
   - Add metadata columns: `load_timestamp`, `source_system`, and `record_hash` for tracking data lineage.
   - Include `is_active` or `is_deleted` flags for soft delete patterns when applicable.

5. **Idempotency:**
   - Design transformations to be replayable without creating duplicates or inconsistent state.
   - Use MERGE operations or write to tables with appropriate unique constraints.

6. **Data Retention:**
   - Define and implement retention policies for historical data in silver tables.
   - Consider partitioning strategies (by date) for efficient querying and maintenance.

7. **String Trimming and Cleansing:**
   - Apply `TRIM()` to all string columns to remove leading and trailing whitespace.
   - Remove special characters, extra spaces, and hidden control characters from text fields.
   - Standardize empty strings to NULL for consistency in downstream processing.

8. **Type Conversion Safety:**
   - Use `TRY_CAST()` instead of `CAST()` to prevent failures on invalid data.
   - Define explicit fallback values for failed conversions (e.g., NULL or default values).
   - Log or quarantine records that fail critical type conversions for investigation.

9. **Date and Timestamp Formatting:**
   - Standardize all date columns to a single format (e.g., `YYYY-MM-DD` or `DATE` type).
   - Convert timestamps to UTC timezone and store with timezone information.
   - Parse multiple date formats using conditional logic or `TRY_TO_TIMESTAMP()` with format patterns.

10. **Numeric Formatting and Precision:**
    - Round or truncate numeric values to appropriate precision (e.g., `DECIMAL(30,2)` for currency).
    - Remove currency symbols, commas, and other formatting characters before conversion.
    - Handle negative values consistently (convert parentheses notation to negative signs).

11. **Case Normalization:**
    - Apply consistent casing rules: `UPPER()` for codes/keys, `LOWER()` for email addresses, `INITCAP()` for names where appropriate.
    - Document casing standards per column type in your data dictionary.
    - Use case-insensitive comparisons for joins and lookups when needed.