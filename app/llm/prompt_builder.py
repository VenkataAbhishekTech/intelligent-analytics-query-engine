def build_prompt(
    query,
    schema
):
    prompt = f"""
You are an analytics query planner.

Your task is to convert a natural language business query
into a structured JSON query plan.

You must use only the schema, metrics, dimensions,
synonyms, and time mappings provided below.

SCHEMA:
{schema}

USER QUERY:
{query}

Return ONLY valid JSON.

The JSON must contain these fields:

{{
    "metric": null,
    "aggregation": null,
    "group_by": [],
    "filters": [],
    "order_by": null,
    "order_direction": null,
    "limit": null,
    "ranking": false,
    "ranking_partition": null,
    "percentage": false,
    "target_comparison": false,
    "time_period": null,
    "comparison_type": null,
    "join_targets": false,
    "nested_query": false,
    "explanation": null,
    "confidence": null
}}

Rules:

1. Use "revenue" for sales or income.
2. Use "profit" for earnings.
3. Use "count(order_id)" for orders.
4. Use "avg_order_value" for AOV.
5. Use only valid columns from the provided schema.
6. Use SUM, AVG, COUNT, MIN, or MAX when aggregation is required.
7. Use DESC for "top", "highest", or "largest".
8. Use ASC for "bottom", "lowest", or "smallest".
9. Set limit when the query asks for top N or bottom N.
10. Set ranking=true when ranking is required.
11. Set percentage=true for contribution percentage queries.
12. Set target_comparison=true when comparing actual revenue with targets.
13. Set join_targets=true when target data is required.
14. Set nested_query=true when the query requires multiple analytical stages.
15. Do not invent columns.
16. Keep confidence between 0 and 1.
17. Return JSON only.
"""

    return prompt