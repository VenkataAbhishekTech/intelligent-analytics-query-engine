class SQLValidator:

    FORBIDDEN_KEYWORDS = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "REPLACE"
    ]

    def validate(self, sql):

        if not sql:
            raise ValueError(
                "SQL query is empty."
            )

        sql_upper = sql.upper().strip()

        for keyword in self.FORBIDDEN_KEYWORDS:

            if keyword in sql_upper:
                raise ValueError(
                    f"Forbidden SQL operation: {keyword}"
                )

        valid_start = (
            sql_upper.startswith("SELECT")
            or sql_upper.startswith("WITH")
        )

        if not valid_start:
            raise ValueError(
                "Only SELECT queries are allowed."
            )

        return True