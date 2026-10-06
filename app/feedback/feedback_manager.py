import csv
import os
from datetime import datetime


class FeedbackManager:

    def __init__(
        self,
        file_path="dataset/feedback_log.csv"
    ):
        self.file_path = file_path

        self._create_file_if_needed()

    def _create_file_if_needed(self):

        directory = os.path.dirname(
            self.file_path
        )

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        if not os.path.exists(
            self.file_path
        ):

            with open(
                self.file_path,
                "w",
                newline="",
                encoding="utf-8"
            ) as file:

                writer = csv.writer(file)

                writer.writerow(
                    [
                        "timestamp",
                        "query",
                        "feedback",
                        "confidence_score",
                        "generated_logic"
                    ]
                )

    def save_feedback(
        self,
        query,
        feedback,
        confidence_score,
        generated_logic
    ):

        feedback = str(
            feedback
        ).strip().lower()

        if feedback not in [
            "positive",
            "negative"
        ]:

            raise ValueError(
                "Feedback must be "
                "'positive' or 'negative'."
            )

        with open(
            self.file_path,
            "a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow(
                [
                    datetime.now().isoformat(),
                    query,
                    feedback,
                    confidence_score,
                    generated_logic
                ]
            )

    def get_feedback(self):

        if not os.path.exists(
            self.file_path
        ):

            return []

        with open(
            self.file_path,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            return list(reader)

    def get_feedback_count(self):

        feedback = self.get_feedback()

        return len(feedback)

    def get_positive_count(self):

        feedback = self.get_feedback()

        return sum(
            1
            for item in feedback
            if item.get("feedback") == "positive"
        )

    def get_negative_count(self):

        feedback = self.get_feedback()

        return sum(
            1
            for item in feedback
            if item.get("feedback") == "negative"
        )

    def get_feedback_summary(self):

        total = self.get_feedback_count()
        positive = self.get_positive_count()
        negative = self.get_negative_count()

        if total == 0:
            positive_rate = 0.0

        else:
            positive_rate = (
                positive / total
            )

        return {
            "total_feedback": total,
            "positive_feedback": positive,
            "negative_feedback": negative,
            "positive_rate": round(
                positive_rate,
                2
            )
        }

    def print_feedback_summary(self):

        summary = (
            self.get_feedback_summary()
        )

        print("\n" + "=" * 60)
        print("FEEDBACK SUMMARY")
        print("=" * 60)

        print(
            f"Total feedback     : "
            f"{summary['total_feedback']}"
        )

        print(
            f"Positive feedback  : "
            f"{summary['positive_feedback']}"
        )

        print(
            f"Negative feedback  : "
            f"{summary['negative_feedback']}"
        )

        print(
            f"Positive rate      : "
            f"{summary['positive_rate']}"
        )
