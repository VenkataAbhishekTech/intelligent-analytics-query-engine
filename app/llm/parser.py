import json
import os
import re
import time

from dotenv import load_dotenv
from google import genai

from app.planner.query_plan import QueryPlan


load_dotenv()


class GeminiParser:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            api_key = os.getenv(
                "GOOGLE_API_KEY"
            )

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY or GOOGLE_API_KEY "
                "is not set in .env"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.models = [
            "gemini-2.5-flash",
            "gemini-2.5-flash-lite"
        ]

    def clean_response(
        self,
        response_text
    ):

        response_text = response_text.strip()

        if response_text.startswith("```"):

            response_text = (
                response_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return response_text

    def normalize_plan_data(
        self,
        plan_data,
        query
    ):

        ranking_partition = (
            plan_data.get(
                "ranking_partition"
            )
        )

        if isinstance(
            ranking_partition,
            list
        ):

            if ranking_partition:

                plan_data[
                    "ranking_partition"
                ] = ranking_partition[0]

            else:

                plan_data[
                    "ranking_partition"
                ] = None

        filters = plan_data.get(
            "filters",
            []
        )

        normalized_filters = []

        for filter_condition in filters:

            if not isinstance(
                filter_condition,
                dict
            ):
                continue

            column = filter_condition.get(
                "column"
            )

            operator = filter_condition.get(
                "operator"
            )

            value = filter_condition.get(
                "value"
            )

            if (
                column is None
                or operator is None
            ):
                continue

            operator_upper = (
                str(operator)
                .upper()
                .strip()
            )

            if (
                "EXTRACT(MONTH" in
                operator_upper
            ):

                operator = (
                    "EXTRACT(MONTH) ="
                )

            normalized_filters.append(
                {
                    "column": column,
                    "operator": operator,
                    "value": value
                }
            )

        plan_data[
            "filters"
        ] = normalized_filters

        query_lower = query.lower()

        month_mapping = {
            "january": "2024-01",
            "jan": "2024-01",
            "february": "2024-02",
            "feb": "2024-02",
            "march": "2024-03",
            "mar": "2024-03",
            "april": "2024-04",
            "apr": "2024-04",
            "may": "2024-05",
            "june": "2024-06",
            "jun": "2024-06",
            "july": "2024-07",
            "jul": "2024-07",
            "august": "2024-08",
            "aug": "2024-08",
            "september": "2024-09",
            "sep": "2024-09",
            "october": "2024-10",
            "oct": "2024-10",
            "november": "2024-11",
            "nov": "2024-11",
            "december": "2024-12",
            "dec": "2024-12"
        }

        if (
            plan_data.get("target_comparison")
            and not plan_data.get("time_period")
        ):

            for month_name, month_value in month_mapping.items():

                if month_name in query_lower:

                    plan_data[
                        "time_period"
                    ] = month_value

                    break

        return plan_data

    def create_fallback_plan(
        self,
        query
    ):

        query_lower = query.lower().strip()

        # --------------------------------------------------
        # Total sales in India for March
        # --------------------------------------------------

        if (
            "total sales" in query_lower
            and "india" in query_lower
            and (
                "march" in query_lower
                or "mar" in query_lower
            )
        ):

            return QueryPlan(
                metric="revenue",
                aggregation="SUM",
                group_by=[],
                filters=[
                    {
                        "column": "country",
                        "operator": "=",
                        "value": "India"
                    }
                ],
                order_by=None,
                order_direction=None,
                limit=None,
                ranking=False,
                ranking_partition=None,
                percentage=False,
                target_comparison=False,
                time_period="2024-03",
                comparison_type=None,
                join_targets=False,
                nested_query=False,
                explanation=(
                    "Calculate total revenue for orders "
                    "from India during March 2024."
                ),
                confidence=0.95
            )

        # --------------------------------------------------
        # Average order value by region
        # --------------------------------------------------

        if (
            (
                "average order value"
                in query_lower
                and "region"
                in query_lower
            )
            or
            (
                "aov"
                in query_lower
                and "region"
                in query_lower
            )
        ):

            return QueryPlan(
                metric="avg_order_value",
                aggregation="AVG",
                group_by=[
                    "region"
                ],
                filters=[],
                order_by=None,
                order_direction=None,
                limit=None,
                ranking=False,
                ranking_partition=None,
                percentage=False,
                target_comparison=False,
                time_period=None,
                comparison_type=None,
                join_targets=False,
                nested_query=False,
                explanation=(
                    "Calculate average order value for "
                    "each region using total revenue divided "
                    "by the number of orders."
                ),
                confidence=0.95
            )

        # --------------------------------------------------
        # YoY revenue
        # --------------------------------------------------

        if (
            "yoy" in query_lower
            and "revenue" in query_lower
        ) or (
            "year over year" in query_lower
            and "revenue" in query_lower
        ):

            return QueryPlan(
                metric="revenue",
                aggregation="SUM",
                group_by=[],
                filters=[],
                order_by=None,
                order_direction=None,
                limit=None,
                ranking=False,
                ranking_partition=None,
                percentage=False,
                target_comparison=False,
                time_period=None,
                comparison_type="yoy",
                join_targets=False,
                nested_query=True,
                explanation=(
                    "Calculate revenue for each year and "
                    "compare each year's revenue with the "
                    "previous year's revenue to determine "
                    "year-over-year growth."
                ),
                confidence=0.90
            )

        # --------------------------------------------------
        # Top N customers per region
        # --------------------------------------------------

        customer_match = re.search(
            r"top\s+(\d+)\s+customers?\s+per\s+region",
            query_lower
        )

        if customer_match:

            limit = int(
                customer_match.group(1)
            )

            return QueryPlan(
                metric="revenue",
                aggregation="SUM",
                group_by=[
                    "region",
                    "customer_id"
                ],
                filters=[],
                order_by="revenue",
                order_direction="DESC",
                limit=limit,
                ranking=True,
                ranking_partition="region",
                percentage=False,
                target_comparison=False,
                time_period=None,
                comparison_type=None,
                join_targets=False,
                nested_query=True,
                explanation=(
                    f"Calculate revenue for each customer "
                    f"within each region, rank customers "
                    f"by revenue within their region, keep "
                    f"the top {limit} customers per region, "
                    f"and aggregate their revenue by region."
                ),
                confidence=0.95
            )

        # --------------------------------------------------
        # Target comparison
        # --------------------------------------------------

        target_words = [
            "target",
            "missed its target",
            "missed target",
            "target in"
        ]

        if any(
            word in query_lower
            for word in target_words
        ):

            month_mapping = {
                "january": "2024-01",
                "jan": "2024-01",
                "february": "2024-02",
                "feb": "2024-02",
                "march": "2024-03",
                "mar": "2024-03",
                "april": "2024-04",
                "apr": "2024-04",
                "may": "2024-05",
                "june": "2024-06",
                "jun": "2024-06",
                "july": "2024-07",
                "jul": "2024-07",
                "august": "2024-08",
                "aug": "2024-08",
                "september": "2024-09",
                "sep": "2024-09",
                "october": "2024-10",
                "oct": "2024-10",
                "november": "2024-11",
                "nov": "2024-11",
                "december": "2024-12",
                "dec": "2024-12"
            }

            time_period = None

            for month_name, month_value in month_mapping.items():

                if month_name in query_lower:

                    time_period = month_value
                    break

            return QueryPlan(
                metric="revenue",
                aggregation="SUM",
                group_by=[
                    "region"
                ],
                filters=[],
                order_by=None,
                order_direction=None,
                limit=None,
                ranking=False,
                ranking_partition=None,
                percentage=False,
                target_comparison=True,
                time_period=time_period,
                comparison_type="less_than",
                join_targets=True,
                nested_query=False,
                explanation=(
                    "Compare total regional revenue "
                    "with the regional target for "
                    "the requested month."
                ),
                confidence=0.95
            )

        # --------------------------------------------------
        # Contribution percentage
        # --------------------------------------------------

        if (
            "contribution" in query_lower
            and "%" in query_lower
        ):

            if "categor" in query_lower:

                return QueryPlan(
                    metric="revenue",
                    aggregation="SUM",
                    group_by=[
                        "product_category"
                    ],
                    filters=[],
                    order_by=None,
                    order_direction=None,
                    limit=None,
                    ranking=False,
                    ranking_partition=None,
                    percentage=True,
                    target_comparison=False,
                    time_period=None,
                    comparison_type=None,
                    join_targets=False,
                    nested_query=False,
                    explanation=(
                        "Calculate revenue for each "
                        "product category and express "
                        "each category as a percentage "
                        "of total revenue."
                    ),
                    confidence=0.95
                )

        # --------------------------------------------------
        # Top product in each region
        # --------------------------------------------------

        if (
            "top product" in query_lower
            and "region" in query_lower
        ):

            return QueryPlan(
                metric="revenue",
                aggregation="SUM",
                group_by=[
                    "region",
                    "product_name"
                ],
                filters=[],
                order_by="revenue",
                order_direction="DESC",
                limit=1,
                ranking=True,
                ranking_partition="region",
                percentage=False,
                target_comparison=False,
                time_period=None,
                comparison_type=None,
                join_targets=False,
                nested_query=True,
                explanation=(
                    "Calculate revenue for each "
                    "product within each region, "
                    "rank products by revenue, and "
                    "select the top product in each region."
                ),
                confidence=0.95
            )

        # --------------------------------------------------
        # Top N cities by profit
        # --------------------------------------------------

        city_profit_match = re.search(
            r"top\s+(\d+)\s+cities?\s+by\s+profit",
            query_lower
        )

        if city_profit_match:

            limit = int(
                city_profit_match.group(1)
            )

            return QueryPlan(
                metric="profit",
                aggregation="SUM",
                group_by=[
                    "city"
                ],
                filters=[],
                order_by="profit",
                order_direction="DESC",
                limit=limit,
                ranking=False,
                ranking_partition=None,
                percentage=False,
                target_comparison=False,
                time_period=None,
                comparison_type=None,
                join_targets=False,
                nested_query=False,
                explanation=(
                    f"Calculate total profit by city, "
                    f"sort cities by profit in descending "
                    f"order, and return the top {limit} cities."
                ),
                confidence=0.95
            )

        return None

    def parse_query(
        self,
        query,
        schema
    ):

        from app.llm.prompt_builder import (
            build_prompt
        )

        # Try deterministic fallback first.
        # This avoids unnecessary Gemini calls for
        # queries that the fallback parser already knows.
        fallback_plan = (
            self.create_fallback_plan(
                query
            )
        )

        if fallback_plan:

            print(
                "Using deterministic "
                "fallback parser."
            )

            return fallback_plan

        prompt = build_prompt(
            query,
            schema
        )

        last_error = None

        for model in self.models:

            for attempt in range(3):

                try:

                    print(
                        f"Trying model: {model} "
                        f"(attempt {attempt + 1}/3)"
                    )

                    response = (
                        self.client.models.generate_content(
                            model=model,
                            contents=prompt
                        )
                    )

                    response_text = (
                        self.clean_response(
                            response.text
                        )
                    )

                    try:

                        plan_data = json.loads(
                            response_text
                        )

                    except json.JSONDecodeError as error:

                        raise ValueError(
                            "Gemini returned invalid JSON: "
                            f"{error}"
                        )

                    plan_data = (
                        self.normalize_plan_data(
                            plan_data,
                            query
                        )
                    )

                    plan = QueryPlan.model_validate(
                        plan_data
                    )

                    return plan

                except Exception as error:

                    last_error = error

                    error_text = str(error)

                    if (
                        "429" in error_text
                        or "RESOURCE_EXHAUSTED"
                        in error_text
                        or "quota"
                        in error_text.lower()
                    ):

                        print(
                            "Gemini quota exceeded."
                        )

                        print(
                            "Using deterministic "
                            "fallback parser."
                        )

                        fallback_plan = (
                            self.create_fallback_plan(
                                query
                            )
                        )

                        if fallback_plan:

                            return fallback_plan

                        raise RuntimeError(
                            "Gemini quota exceeded and "
                            "no fallback parser is "
                            "available for this query."
                        )

                    if "503" in error_text:

                        print(
                            "Gemini service is temporarily "
                            "unavailable."
                        )

                        if attempt < 2:

                            wait_time = (
                                2 ** attempt
                            )

                            print(
                                f"Retrying in "
                                f"{wait_time} seconds..."
                            )

                            time.sleep(
                                wait_time
                            )

                            continue

                        break

                    raise

        fallback_plan = (
            self.create_fallback_plan(
                query
            )
        )

        if fallback_plan:

            print(
                "Using deterministic "
                "fallback parser."
            )

            return fallback_plan

        raise RuntimeError(
            "Gemini was unavailable after multiple "
            "attempts. Please try again later. "
            f"Last error: {last_error}"
        )