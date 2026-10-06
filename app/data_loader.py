import csv
import json
import duckdb
import pandas as pd


def parse_csv_row(row):
    if len(row) == 1 and "," in row[0]:
        return next(csv.reader([row[0]]))

    return row


def load_csv(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.reader(file)
        rows = list(reader)

    if not rows:
        raise ValueError(f"File is empty: {file_path}")

    headers = parse_csv_row(rows[0])

    data = []

    for row in rows[1:]:
        parsed_row = parse_csv_row(row)

        if len(parsed_row) == len(headers):
            data.append(parsed_row)
        else:
            raise ValueError(
                f"Invalid row in {file_path}. "
                f"Expected {len(headers)} columns but found {len(parsed_row)} columns."
            )

    df = pd.DataFrame(
        data,
        columns=headers
    )

    return df


def load_sales_data(file_path):
    df = load_csv(file_path)

    numeric_columns = [
        "quantity",
        "unit_price",
        "discount",
        "shipping_cost",
        "profit"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    if "order_date" in df.columns:
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

    return df


def load_targets(file_path):
    df = load_csv(file_path)

    if "target_revenue" in df.columns:
        df["target_revenue"] = pd.to_numeric(
            df["target_revenue"],
            errors="coerce"
        )

    if "month" in df.columns:
        df["month"] = df["month"].astype(str)

    return df


def clean_json_text(text):
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:
        line = line.strip()

        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]

        line = line.replace('""', '"')

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def load_json_file(file_path):
    with open(
        file_path,
        "r",
        encoding="utf-8-sig"
    ) as file:
        text = file.read()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        cleaned_text = clean_json_text(text)
        return json.loads(cleaned_text)


def load_data_dictionary(file_path):
    return load_json_file(file_path)


def load_nl_queries(file_path):
    return load_json_file(file_path)


def create_database(sales_data, targets):
    connection = duckdb.connect()

    connection.register(
        "sales_data",
        sales_data
    )

    connection.register(
        "targets",
        targets
    )

    return connection


def load_all_data():
    sales_data = load_sales_data(
        "dataset/sales_data.csv"
    )

    targets = load_targets(
        "dataset/targets.csv"
    )

    data_dictionary = load_data_dictionary(
        "dataset/data_dictionary.json"
    )

    nl_queries = load_nl_queries(
        "dataset/nl_queries.json"
    )

    connection = create_database(
        sales_data,
        targets
    )

    return {
        "sales_data": sales_data,
        "targets": targets,
        "data_dictionary": data_dictionary,
        "nl_queries": nl_queries,
        "connection": connection
    }