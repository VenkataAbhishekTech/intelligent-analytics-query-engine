from app.llm.parser import GeminiParser
from app.sql.generator import SQLGenerator
from app.sql.validator import SQLValidator
from app.validation.confidence import calculate_confidence
from app.explanation.explainer import generate_explanation
from app.feedback.feedback_manager import FeedbackManager


class AnalyticsEngine:

    def __init__(
        self,
        schema_manager,
        connection
    ):
        self.schema_manager = schema_manager
        self.connection = connection

        self.parser = GeminiParser()

        self.sql_generator = SQLGenerator(
            schema_manager
        )

        self.sql_validator = SQLValidator()

        self.feedback_manager = (
            FeedbackManager()
        )

    def process_query(self, query):

        print("\n" + "=" * 60)
        print("QUERY")
        print("=" * 60)

        print(query)

        print("\nGENERATING QUERY PLAN...")
        print("-" * 60)

        schema = (
            self.schema_manager
            .get_schema_for_llm()
        )

        plan = self.parser.parse_query(
            query,
            schema
        )

        print(
            plan.model_dump_json(
                indent=2
            )
        )

        print("\nGENERATING SQL...")
        print("-" * 60)

        sql = self.sql_generator.generate_sql(
            plan
        )

        print(sql)

        print("\nVALIDATING SQL...")
        print("-" * 60)

        validation_result = (
            self.sql_validator.validate(
                sql
            )
        )

        if not validation_result:
            raise ValueError(
                "SQL validation failed."
            )

        print(
            "SQL validation: PASSED"
        )

        print("\nEXECUTING SQL...")
        print("-" * 60)

        result = self.connection.execute(
            sql
        ).fetchdf()

        print(
            result.to_string(
                index=False
            )
        )

        confidence = calculate_confidence(
            plan=plan,
            sql=sql,
            result=result,
            sql_valid=True,
            feedback_manager=(
                self.feedback_manager
            ),
            query=query
        )

        explanation = generate_explanation(
            query=query,
            plan=plan,
            sql=sql,
            result=result
        )

        response = {
            "query": query,
            "generated_logic": sql,
            "result": result.to_dict(
                orient="records"
            ),
            "confidence_score": confidence,
            "explanation": explanation
        }

        return response

    def save_feedback(
        self,
        response,
        feedback
    ):

        self.feedback_manager.save_feedback(
            query=response["query"],
            feedback=feedback,
            confidence_score=(
                response["confidence_score"]
            ),
            generated_logic=(
                response["generated_logic"]
            )
        )

    def get_feedback_summary(self):

        return (
            self.feedback_manager
            .get_feedback_summary()
        )

    def print_feedback_summary(self):

        self.feedback_manager.print_feedback_summary()
