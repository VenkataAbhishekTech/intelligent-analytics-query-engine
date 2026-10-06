class SQLGenerator:

    def __init__(self, schema_manager):
        self.schema_manager = schema_manager

    def get_revenue_expression(self):
        return (
            "quantity * unit_price * (1 - discount)"
        )

    def get_metric_expression(self, metric):
        if metric == "revenue":
            return self.get_revenue_expression()

        if metric == "profit":
            return "profit"

        if metric == "orders":
            return "COUNT(order_id)"

        if metric == "avg_order_value":
            return (
                "SUM("
                "quantity * unit_price * (1 - discount)"
                ") / NULLIF(COUNT(order_id), 0)"
            )

        return metric

    def generate_basic_sql(self, plan):

        if plan.metric == "avg_order_value":

            select_parts = []

            for column in plan.group_by:
                select_parts.append(column)

            select_parts.append(
                "SUM("
                "quantity * unit_price * (1 - discount)"
                ") / NULLIF(COUNT(order_id), 0) "
                "AS avg_order_value"
            )

            select_clause = ", ".join(
                select_parts
            )

        else:

            metric_expression = (
                self.get_metric_expression(
                    plan.metric
                )
            )

            select_parts = []

            for column in plan.group_by:
                select_parts.append(column)

            select_parts.append(
                f"{plan.aggregation}({metric_expression}) "
                f"AS {plan.metric}"
            )

            select_clause = ", ".join(
                select_parts
            )

        sql = (
            f"SELECT {select_clause}\n"
            f"FROM sales_data\n"
        )

        where_conditions = []

        for filter_condition in plan.filters:

            column = filter_condition.column
            operator = filter_condition.operator
            value = filter_condition.value

            if operator == "=":
                where_conditions.append(
                    f"{column} = '{value}'"
                )

            elif operator == "!=":
                where_conditions.append(
                    f"{column} <> '{value}'"
                )

            elif operator == ">":
                where_conditions.append(
                    f"{column} > {value}"
                )

            elif operator == "<":
                where_conditions.append(
                    f"{column} < {value}"
                )

            elif operator == ">=":
                where_conditions.append(
                    f"{column} >= {value}"
                )

            elif operator == "<=":
                where_conditions.append(
                    f"{column} <= {value}"
                )

            elif operator == "LIKE":
                where_conditions.append(
                    f"{column} LIKE '%{value}%'"
                )

            else:
                raise ValueError(
                    f"Invalid operator: {operator}"
                )

        if plan.time_period:

            where_conditions.append(
                "strftime(order_date, '%Y-%m') "
                f"= '{plan.time_period}'"
            )

        if where_conditions:

            sql += (
                "WHERE "
                + " AND ".join(where_conditions)
                + "\n"
            )

        if plan.group_by:

            sql += (
                "GROUP BY "
                + ", ".join(plan.group_by)
                + "\n"
            )

        if plan.order_by:

            direction = (
                plan.order_direction
                or "ASC"
            )

            sql += (
                f"ORDER BY {plan.order_by} "
                f"{direction}\n"
            )

        if plan.limit:

            sql += (
                f"LIMIT {plan.limit}\n"
            )

        sql += ";"

        return sql

    def generate_percentage_sql(self, plan):

        metric_expression = (
            self.get_metric_expression(
                plan.metric
            )
        )

        group_column = plan.group_by[0]

        sql = f"""
SELECT
    {group_column},
    SUM({metric_expression}) AS {plan.metric},
    ROUND(
        100.0 * SUM({metric_expression})
        / NULLIF(
            SUM(
                SUM({metric_expression})
            ) OVER (),
            0
        ),
        2
    ) AS contribution_percentage
FROM sales_data
"""

        where_conditions = []

        for filter_condition in plan.filters:

            column = filter_condition.column
            operator = filter_condition.operator
            value = filter_condition.value

            if operator == "=":
                where_conditions.append(
                    f"{column} = '{value}'"
                )

            elif operator == ">":
                where_conditions.append(
                    f"{column} > {value}"
                )

            elif operator == "<":
                where_conditions.append(
                    f"{column} < {value}"
                )

            elif operator == ">=":
                where_conditions.append(
                    f"{column} >= {value}"
                )

            elif operator == "<=":
                where_conditions.append(
                    f"{column} <= {value}"
                )

            else:
                raise ValueError(
                    f"Invalid operator: {operator}"
                )

        if plan.time_period:

            where_conditions.append(
                "strftime(order_date, '%Y-%m') "
                f"= '{plan.time_period}'"
            )

        if where_conditions:

            sql += (
                "\nWHERE "
                + " AND ".join(where_conditions)
                + "\n"
            )

        sql += f"""
GROUP BY {group_column}
ORDER BY contribution_percentage DESC;
"""

        return sql.strip()

    def generate_ranking_sql(self, plan):

        metric_expression = (
            self.get_metric_expression(
                plan.metric
            )
        )

        group_columns = ", ".join(
            plan.group_by
        )

        partition_column = (
            plan.ranking_partition
        )

        direction = (
            plan.order_direction
            or "DESC"
        )

        sql = f"""
WITH grouped_data AS (

    SELECT
        {group_columns},
        SUM({metric_expression}) AS {plan.metric}

    FROM sales_data

"""

        where_conditions = []

        for filter_condition in plan.filters:

            column = filter_condition.column
            operator = filter_condition.operator
            value = filter_condition.value

            if operator == "=":
                where_conditions.append(
                    f"{column} = '{value}'"
                )

            elif operator == ">":
                where_conditions.append(
                    f"{column} > {value}"
                )

            elif operator == "<":
                where_conditions.append(
                    f"{column} < {value}"
                )

            elif operator == ">=":
                where_conditions.append(
                    f"{column} >= {value}"
                )

            elif operator == "<=":
                where_conditions.append(
                    f"{column} <= {value}"
                )

            else:
                raise ValueError(
                    f"Invalid operator: {operator}"
                )

        if plan.time_period:

            where_conditions.append(
                "strftime(order_date, '%Y-%m') "
                f"= '{plan.time_period}'"
            )

        if where_conditions:

            sql += (
                "    WHERE "
                + " AND ".join(where_conditions)
                + "\n"
            )

        sql += f"""
    GROUP BY {group_columns}

),

ranked_data AS (

    SELECT
        *,
        RANK() OVER (
            PARTITION BY {partition_column}
            ORDER BY {plan.metric} {direction}
        ) AS rank

    FROM grouped_data

)

SELECT *
FROM ranked_data
WHERE rank <= {plan.limit}
ORDER BY rank;
"""

        return sql.strip()

    def generate_nested_customer_sql(self, plan):

        metric_expression = (
            self.get_metric_expression(
                plan.metric
            )
        )

        sql = f"""
WITH customer_revenue AS (

    SELECT
        region,
        customer_id,
        SUM({metric_expression}) AS revenue

    FROM sales_data

    GROUP BY
        region,
        customer_id

),

ranked_customers AS (

    SELECT
        region,
        customer_id,
        revenue,
        RANK() OVER (
            PARTITION BY region
            ORDER BY revenue DESC
        ) AS customer_rank

    FROM customer_revenue

),

top_customers AS (

    SELECT
        region,
        customer_id,
        revenue,
        customer_rank

    FROM ranked_customers

    WHERE customer_rank <= {plan.limit}

)

SELECT
    region,
    SUM(revenue) AS revenue

FROM top_customers

GROUP BY region

ORDER BY revenue DESC;
"""

        return sql.strip()

    def generate_target_comparison_sql(self, plan):

        time_period = (
            plan.time_period
        )

        comparison_operator = "<"

        if plan.comparison_type == "greater_than":
            comparison_operator = ">"

        elif plan.comparison_type == "equal":
            comparison_operator = "="

        sql = f"""
SELECT
    s.region,
    s.revenue,
    t.target_revenue,
    s.revenue - t.target_revenue AS difference,
    CASE
        WHEN s.revenue {comparison_operator}
             t.target_revenue
        THEN 'Missed'
        ELSE 'Met'
    END AS target_status

FROM
(
    SELECT
        region,
        SUM(
            quantity * unit_price * (1 - discount)
        ) AS revenue

    FROM sales_data

    WHERE strftime(
        order_date,
        '%Y-%m'
    ) = '{time_period}'

    GROUP BY region

) s

JOIN targets t
    ON s.region = t.region
    AND t.month = '{time_period}'

WHERE s.revenue {comparison_operator}
      t.target_revenue

ORDER BY difference ASC;
"""

        return sql.strip()

    def generate_yoy_sql(self, plan):

        metric_expression = (
            self.get_metric_expression(
                plan.metric
            )
        )

        sql = f"""
WITH yearly_revenue AS (

    SELECT
        EXTRACT(
            YEAR FROM order_date
        ) AS year,
        SUM(
            {metric_expression}
        ) AS revenue

    FROM sales_data

    GROUP BY
        EXTRACT(
            YEAR FROM order_date
        )

),

yoy_data AS (

    SELECT
        year,
        revenue,
        LAG(revenue) OVER (
            ORDER BY year
        ) AS previous_year_revenue

    FROM yearly_revenue

)

SELECT
    year,
    revenue,
    previous_year_revenue,
    ROUND(
        100.0 *
        (
            revenue - previous_year_revenue
        )
        / NULLIF(
            previous_year_revenue,
            0
        ),
        2
    ) AS yoy_growth_percentage

FROM yoy_data

ORDER BY year;
"""

        return sql.strip()

    def generate_sql(self, plan):

        if (
            plan.comparison_type == "yoy"
        ):

            return self.generate_yoy_sql(
                plan
            )

        if (
            plan.target_comparison
            and plan.join_targets
        ):

            return (
                self.generate_target_comparison_sql(
                    plan
                )
            )

        if (
            plan.nested_query
            and "customer_id" in plan.group_by
            and plan.ranking
            and plan.ranking_partition == "region"
        ):

            return (
                self.generate_nested_customer_sql(
                    plan
                )
            )

        if (
            plan.ranking
            and plan.ranking_partition
        ):

            return (
                self.generate_ranking_sql(
                    plan
                )
            )

        if plan.percentage:

            return (
                self.generate_percentage_sql(
                    plan
                )
            )

        return self.generate_basic_sql(
            plan
        )