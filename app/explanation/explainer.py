def generate_explanation(
    query,
    plan,
    sql,
    result
):
    parts = []

    # What the system understood
    if plan.metric == "revenue":
        metric_text = "revenue"
    elif plan.metric == "profit":
        metric_text = "profit"
    elif plan.metric:
        metric_text = plan.metric
    else:
        metric_text = "the requested metric"

    understanding = (
        f"The system understood the query as calculating "
        f"{metric_text}"
    )

    if plan.group_by:
        group_text = ", ".join(plan.group_by)

        understanding += (
            f", grouped by {group_text}"
        )

    if plan.filters:
        understanding += (
            ", with the requested filters"
        )

    if plan.ranking:
        understanding += (
            ", including ranking within the requested groups"
        )

    if plan.limit:
        understanding += (
            f", limited to the top {plan.limit} results"
        )

    if plan.percentage:
        understanding += (
            ", with each group expressed as a percentage "
            "of the overall total"
        )

    if plan.target_comparison:
        understanding += (
            ", comparing actual revenue against target revenue"
        )

    understanding += "."

    parts.append(understanding)

    # How the result was generated
    generation = (
        "The system converted the query plan into executable "
        "SQL and executed it using DuckDB."
    )

    if plan.nested_query:
        generation = (
            "The system used multiple analytical stages in SQL "
            "to calculate the intermediate values, apply the "
            "required ranking or filtering logic, and then "
            "produce the final result."
        )

    if plan.target_comparison:
        generation = (
            "The system calculated actual revenue from the sales "
            "data, joined it with the target data, and compared "
            "actual revenue with the corresponding target."
        )

    parts.append(generation)

    # Result information
    if result is not None:

        try:
            row_count = len(result)
        except TypeError:
            row_count = 0

        parts.append(
            f"The query returned {row_count} result row(s)."
        )

    return " ".join(parts)