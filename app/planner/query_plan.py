from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class FilterCondition(BaseModel):
    column: str
    operator: str
    value: Any


class QueryPlan(BaseModel):
    metric: Optional[str] = None
    aggregation: Optional[str] = None

    group_by: List[str] = Field(
        default_factory=list
    )

    filters: List[FilterCondition] = Field(
        default_factory=list
    )

    order_by: Optional[str] = None
    order_direction: Optional[str] = None

    limit: Optional[int] = None

    ranking: bool = False
    ranking_partition: Optional[str] = None

    percentage: bool = False

    target_comparison: bool = False

    time_period: Optional[str] = None

    comparison_type: Optional[str] = None

    join_targets: bool = False

    nested_query: bool = False

    explanation: Optional[str] = None

    confidence: Optional[float] = None


def create_query_plan(
    metric=None,
    aggregation=None,
    group_by=None,
    filters=None,
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
    explanation=None,
    confidence=None
):
    plan = QueryPlan(
        metric=metric,
        aggregation=aggregation,
        group_by=group_by or [],
        filters=filters or [],
        order_by=order_by,
        order_direction=order_direction,
        limit=limit,
        ranking=ranking,
        ranking_partition=ranking_partition,
        percentage=percentage,
        target_comparison=target_comparison,
        time_period=time_period,
        comparison_type=comparison_type,
        join_targets=join_targets,
        nested_query=nested_query,
        explanation=explanation,
        confidence=confidence
    )

    return plan


def plan_to_dict(plan):
    return plan.model_dump()


def print_query_plan(plan):
    print("\n" + "=" * 60)
    print("QUERY PLAN")
    print("=" * 60)

    plan_data = plan_to_dict(plan)

    for key, value in plan_data.items():
        print(f"{key}: {value}")