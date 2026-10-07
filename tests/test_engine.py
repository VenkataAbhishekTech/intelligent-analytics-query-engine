from app.data_loader import load_all_data
from app.schema_manager import SchemaManager
from app.engine import AnalyticsEngine


def create_engine():

    data = load_all_data()

    schema_manager = SchemaManager(
        sales_data=data["sales_data"],
        targets=data["targets"],
        data_dictionary=data["data_dictionary"]
    )

    engine = AnalyticsEngine(
        schema_manager=schema_manager,
        connection=data["connection"]
    )

    return engine


def test_total_sales_in_india_for_march():

    engine = create_engine()

    result = engine.process_query(
        "Total sales in India for March"
    )

    assert result["result"][0]["revenue"] == 108


def test_top_2_cities_by_profit():

    engine = create_engine()

    result = engine.process_query(
        "Top 2 cities by profit"
    )

    assert len(result["result"]) == 2

    assert result["result"][0]["city"] == "New York"
    assert result["result"][0]["profit"] == 200

    assert result["result"][1]["city"] == "San Francisco"
    assert result["result"][1]["profit"] == 180


def test_average_order_value_by_region():

    engine = create_engine()

    result = engine.process_query(
        "Average order value by region"
    )

    assert len(result["result"]) == 3


def test_region_missed_target_in_february():

    engine = create_engine()

    result = engine.process_query(
        "Which region missed its target in Feb?"
    )

    assert len(result["result"]) == 3


def test_sales_contribution_by_category():

    engine = create_engine()

    result = engine.process_query(
        "Sales contribution % by category"
    )

    assert len(result["result"]) == 3


def test_top_product_in_each_region():

    engine = create_engine()

    result = engine.process_query(
        "Top product in each region"
    )

    assert len(result["result"]) == 3


def test_yoy_growth():

    engine = create_engine()

    result = engine.process_query(
        "YoY growth in revenue"
    )

    assert len(result["result"]) >= 1


def test_top_3_customers_per_region():

    engine = create_engine()

    result = engine.process_query(
        "Revenue of top 3 customers per region"
    )

    assert len(result["result"]) == 3