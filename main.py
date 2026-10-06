from app.data_loader import load_all_data
from app.schema_manager import SchemaManager
from app.engine import AnalyticsEngine
import json
import os


def main():

    print("=" * 60)
    print("INTELLIGENT ANALYTICS QUERY ENGINE")
    print("=" * 60)

    data = load_all_data()

    sales_data = data["sales_data"]
    targets = data["targets"]
    data_dictionary = data["data_dictionary"]
    connection = data["connection"]
    nl_queries = data["nl_queries"]

    schema_manager = SchemaManager(
        sales_data=sales_data,
        targets=targets,
        data_dictionary=data_dictionary
    )

    engine = AnalyticsEngine(
        schema_manager=schema_manager,
        connection=connection
    )

    print("\n" + "=" * 60)
    print("RUNNING SUPPLIED NATURAL LANGUAGE QUERIES")
    print("=" * 60)

    results = []
    sample_outputs = []

    for index, item in enumerate(
        nl_queries,
        start=1
    ):

        if isinstance(item, dict):

            query = (
                item.get("query")
                or item.get("question")
                or item.get("natural_language_query")
            )

        else:

            query = str(item)

        if not query:
            continue

        print("\n")
        print("=" * 60)
        print(f"TEST {index}")
        print("=" * 60)

        try:

            result = engine.process_query(
                query
            )

            results.append(
                {
                    "status": "PASSED",
                    "response": result
                }
            )

            sample_output = {
                "query": query,
                "generated_logic": result.get(
                    "generated_logic",
                    result.get("sql", "")
                ),
                "result": result.get(
                    "result",
                    result.get("data", [])
                ),
                "confidence_score": result.get(
                    "confidence_score",
                    0.0
                ),
                "explanation": result.get(
                    "explanation",
                    ""
                )
            }

            sample_outputs.append(
                sample_output
            )

        except Exception as error:

            print("\nQUERY FAILED")
            print("-" * 60)
            print(str(error))

            results.append(
                {
                    "status": "FAILED",
                    "query": query,
                    "error": str(error)
                }
            )

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(
        1
        for item in results
        if item["status"] == "PASSED"
    )

    failed = sum(
        1
        for item in results
        if item["status"] == "FAILED"
    )

    print(f"Total queries : {len(results)}")
    print(f"Passed        : {passed}")
    print(f"Failed        : {failed}")

    print("\n" + "=" * 60)
    print("FINAL TEST RESULTS")
    print("=" * 60)

    print(
        json.dumps(
            results,
            indent=2,
            default=str
        )
    )

    output_directory = "outputs"

    os.makedirs(
        output_directory,
        exist_ok=True
    )

    output_file = os.path.join(
        output_directory,
        "sample_outputs.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            sample_outputs,
            file,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    print("\n" + "=" * 60)
    print("SAMPLE OUTPUT SAVED")
    print("=" * 60)

    print(
        f"File: {output_file}"
    )

    print(
        f"Saved queries: {len(sample_outputs)}"
    )


if __name__ == "__main__":
    main()