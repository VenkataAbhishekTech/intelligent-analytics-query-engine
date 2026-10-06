class SchemaManager:

    def __init__(
        self,
        sales_data,
        targets,
        data_dictionary
    ):
        self.sales_data = sales_data
        self.targets = targets
        self.data_dictionary = data_dictionary

    def get_sales_columns(self):
        return self.sales_data.columns.tolist()

    def get_target_columns(self):
        return self.targets.columns.tolist()

    def get_metrics(self):
        return self.data_dictionary.get(
            "metrics",
            {}
        )

    def get_dimensions(self):
        return self.data_dictionary.get(
            "dimensions",
            []
        )

    def get_synonyms(self):
        return self.data_dictionary.get(
            "synonyms",
            {}
        )

    def get_time_mappings(self):
        return self.data_dictionary.get(
            "time_mappings",
            {}
        )

    def resolve_term(self, term):
        term = term.lower().strip()

        synonyms = self.get_synonyms()

        if term in synonyms:
            return synonyms[term]

        if term in self.get_metrics():
            return term

        if term in self.get_dimensions():
            return term

        if term in self.get_sales_columns():
            return term

        if term in self.get_target_columns():
            return term

        return None

    def get_schema(self):
        return {
            "sales_data": {
                "columns": self.get_sales_columns()
            },
            "targets": {
                "columns": self.get_target_columns()
            },
            "metrics": self.get_metrics(),
            "dimensions": self.get_dimensions(),
            "synonyms": self.get_synonyms(),
            "time_mappings": self.get_time_mappings()
        }

    def get_schema_for_llm(self):
        schema = self.get_schema()

        return schema

    def print_schema(self):
        print("\n" + "=" * 60)
        print("SCHEMA MANAGER")
        print("=" * 60)

        print("\nSALES DATA COLUMNS")
        print("-" * 60)

        for column in self.get_sales_columns():
            print("-", column)

        print("\nTARGET DATA COLUMNS")
        print("-" * 60)

        for column in self.get_target_columns():
            print("-", column)

        print("\nMETRICS")
        print("-" * 60)

        for name, formula in self.get_metrics().items():
            print(f"- {name}: {formula}")

        print("\nDIMENSIONS")
        print("-" * 60)

        for dimension in self.get_dimensions():
            print("-", dimension)

        print("\nSYNONYMS")
        print("-" * 60)

        for synonym, meaning in self.get_synonyms().items():
            print(f"- {synonym} -> {meaning}")

        print("\nTIME MAPPINGS")
        print("-" * 60)

        for term, meaning in self.get_time_mappings().items():
            print(f"- {term} -> {meaning}")