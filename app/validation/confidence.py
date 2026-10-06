import re


def get_query_keywords(query):
    query = query.lower()

    words = re.findall(
        r"[a-zA-Z_]+",
        query
    )

    stop_words = {
        "the",
        "a",
        "an",
        "in",
        "on",
        "of",
        "by",
        "for",
        "to",
        "and",
        "or",
        "is",
        "are",
        "was",
        "were",
        "which",
        "what",
        "how",
        "with",
        "from",
        "each",
        "its",
        "top",
        "bottom"
    }

    keywords = set()

    for word in words:

        if (
            word not in stop_words
            and len(word) > 2
        ):
            keywords.add(word)

    return keywords


def calculate_feedback_adjustment(
    query,
    feedback_manager
):
    if (
        feedback_manager is None
        or not query
    ):
        return 0.0

    feedback = (
        feedback_manager.get_feedback()
    )

    if not feedback:
        return 0.0

    current_keywords = (
        get_query_keywords(query)
    )

    if not current_keywords:
        return 0.0

    positive_score = 0.0
    negative_score = 0.0

    relevant_feedback_count = 0

    for item in feedback:

        stored_query = (
            item.get("query", "")
        )

        stored_keywords = (
            get_query_keywords(
                stored_query
            )
        )

        if not stored_keywords:
            continue

        common_keywords = (
            current_keywords
            & stored_keywords
        )

        union_keywords = (
            current_keywords
            | stored_keywords
        )

        if not union_keywords:
            continue

        similarity = (
            len(common_keywords)
            / len(union_keywords)
        )

        if similarity < 0.5:
            continue

        relevant_feedback_count += 1

        feedback_type = (
            item.get("feedback", "")
            .strip()
            .lower()
        )

        if feedback_type == "positive":

            positive_score += similarity

        elif feedback_type == "negative":

            negative_score += similarity

    if relevant_feedback_count == 0:
        return 0.0

    total_score = (
        positive_score
        + negative_score
    )

    if total_score == 0:
        return 0.0

    positive_rate = (
        positive_score
        / total_score
    )

    if positive_rate >= 0.75:
        return 0.05

    if positive_rate <= 0.25:
        return -0.10

    if positive_rate >= 0.50:
        return 0.02

    return -0.05


def calculate_confidence(
    plan,
    sql,
    result,
    sql_valid=True,
    feedback_manager=None,
    query=None
):
    score = 0.0

    if plan is not None:
        score += 0.25

    if plan.metric:
        score += 0.15

    if plan.aggregation:
        score += 0.10

    if sql:
        score += 0.15

    if sql_valid:
        score += 0.15

    if result is not None:
        score += 0.10

    if plan.group_by:
        score += 0.05

    if (
        plan.ranking
        or plan.percentage
        or plan.target_comparison
        or plan.nested_query
    ):
        score += 0.05

    feedback_adjustment = (
        calculate_feedback_adjustment(
            query=query,
            feedback_manager=feedback_manager
        )
    )

    score += feedback_adjustment

    score = max(
        0.0,
        min(score, 1.0)
    )

    return round(
        score,
        2
    )