# Intelligent Analytics Query Engine

An AI-powered natural language analytics engine that allows users to ask business questions in plain English and automatically converts them into executable SQL queries.

The system combines natural-language understanding, query planning, SQL generation, SQL validation, DuckDB execution, result validation, confidence scoring, explanations, and feedback logging into a modular analytics pipeline.

---

## Features

- Natural-language business query processing
- LLM-based query parsing
- Deterministic fallback parser
- Structured query planning
- Automatic SQL generation
- SQL validation
- DuckDB query execution
- Aggregation and grouping
- Top-N analysis
- Ranking within groups
- Contribution percentage analysis
- Target comparison
- Nested analytical queries
- Year-over-Year revenue analysis
- Confidence scoring
- Result validation
- Natural-language explanations
- Feedback logging
- Automatic sample-output generation

---

## System Architecture

```text
                    Natural Language Query
                              |
                              v
                  +------------------------+
                  |   LLM / Fallback       |
                  |       Parser           |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |    Query Planner       |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |     Query Plan         |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |    SQL Generator       |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |    SQL Validator      |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |   DuckDB Executor      |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |  Result Validation    |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |   Confidence Score     |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |     Explanation       |
                  +------------------------+
                              |
                              v
                       Final Result
```

---

## Project Structure

```text
intelligent-analytics-query-engine/
│
├── main.py
├── requirements.txt
├── .env
├── __init__.py
├── README.md
│
├── app/
│   ├── config.py
│   ├── data_loader.py
│   ├── engine.py
│   ├── schema_manager.py
│   │
│   ├── execution/
│   │   └── executor.py
│   │
│   ├── explanation/
│   │   └── explainer.py
│   │
│   ├── feedback/
│   │   ├── feedback_manager.py
│   │   └── __init__.py
│   │
│   ├── llm/
│   │   ├── parser.py
│   │   ├── prompt_builder.py
│   │   └── __init__.py
│   │
│   ├── planner/
│   │   ├── planner.py
│   │   ├── query_plan.py
│   │   └── __init__.py
│   │
│   ├── sql/
│   │   ├── generator.py
│   │   ├── validator.py
│   │   └── __init__.py
│   │
│   └── validation/
│       ├── confidence.py
│       └── result_validator.py
│
├── dataset/
│   ├── data_dictionary.json
│   ├── feedback_log.csv
│   ├── nl_queries.json
│   ├── sales_data.csv
│   └── targets.csv
│
├── outputs/
│   └── sample_outputs.json
│
└── tests/
    ├── test_basic.py
    ├── test_complex.py
    ├── test_ranking.py
    └── test_targets.py
```

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application development |
| Google Gemini | Natural-language query understanding |
| DuckDB | Analytical SQL execution |
| Pandas | Data loading and manipulation |
| Pydantic | Structured data and query-plan validation |
| FastAPI | API-ready application support |
| Uvicorn | ASGI server support |
| python-dotenv | Environment configuration |

---

## Dataset

The project uses sample business-sales data containing information such as:

- Customer
- Product
- Product category
- Region
- Country
- City
- Quantity
- Unit price
- Discount
- Profit
- Order date

The project also contains target data for comparing actual revenue against target revenue.

### Revenue Calculation

Revenue is calculated using:

```text
Revenue = Quantity × Unit Price × (1 - Discount)
```

---

## Natural Language Queries

The engine supports analytical questions such as:

```text
Total sales in India for March
```

```text
Top 2 cities by profit
```

```text
Average order value by region
```

```text
Which region missed its target in Feb?
```

```text
Sales contribution % by category
```

```text
Top product in each region
```

```text
YoY growth in revenue
```

```text
Revenue of top 3 customers per region
```

---

## Query Processing Flow

A natural-language query passes through several stages.

### 1. Query Input

The user provides a question in natural language.

Example:

```text
Top 2 cities by profit
```

### 2. Query Parsing

The system identifies the required analytical intent, dimensions, metrics, filters, grouping, ranking, and other operations.

### 3. Query Planning

The parsed information is converted into a structured query plan.

### 4. SQL Generation

The query plan is converted into executable SQL.

Example:

```sql
SELECT city, SUM(profit) AS profit
FROM sales_data
GROUP BY city
ORDER BY profit DESC
LIMIT 2;
```

### 5. SQL Validation

The generated SQL is checked before execution.

### 6. DuckDB Execution

The validated SQL query is executed using DuckDB.

### 7. Result Validation

The returned result is checked by the validation layer.

### 8. Confidence Scoring

The system calculates a confidence score based on the interpretation and execution.

### 9. Explanation

A natural-language explanation is generated describing what the system understood and how the result was produced.

---

## Running the Project

### Step 1: Clone or download the project

Open the project directory:

```powershell
cd intelligent-analytics-query-engine
```

### Step 2: Create a virtual environment

```powershell
python -m venv venv
```

### Step 3: Activate the environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 5: Configure the API key

Create a `.env` file in the project root.

```text
GOOGLE_API_KEY=your_api_key_here
```

Do not commit the actual API key to GitHub.

### Step 6: Run the application

```powershell
python main.py
```

---

## Sample Output

After running the application, the system automatically generates:

```text
outputs/sample_outputs.json
```

Each sample output contains:

```json
{
  "query": "Top 2 cities by profit",
  "generated_logic": "SELECT city, SUM(profit) AS profit ...",
  "result": [
    {
      "city": "New York",
      "profit": 200.0
    },
    {
      "city": "San Francisco",
      "profit": 180.0
    }
  ],
  "confidence_score": 0.85,
  "explanation": "The system understood the query as calculating profit..."
}
```

---

## Testing

The project contains separate test modules for different analytical capabilities:

```text
tests/
├── test_basic.py
├── test_complex.py
├── test_ranking.py
└── test_targets.py
```

The supplied natural-language query suite currently passes:

```text
Total queries : 8
Passed        : 8
Failed        : 0
```

### Test Coverage

The supplied queries verify:

- Basic aggregation
- Filtering
- Grouping
- Ranking
- Top-N analysis
- Contribution percentage
- Target comparison
- Nested queries
- YoY analysis
- Customer ranking by region

---

## Example Result

For the query:

```text
Top 2 cities by profit
```

the engine generates SQL that performs:

```text
GROUP BY city
        ↓
SUM(profit)
        ↓
ORDER BY profit DESC
        ↓
LIMIT 2
```

Result:

```text
New York       200.0
San Francisco  180.0
```

---

## Confidence Scoring

The engine provides a confidence score with each result.

Example:

```json
"confidence_score": 1.0
```

The score provides an indication of how confidently the system interpreted and executed the requested analytical operation.

---

## Feedback System

The project includes a feedback component that can record query-related feedback.

```text
app/
└── feedback/
    └── feedback_manager.py
```

Feedback information is stored in:

```text
dataset/feedback_log.csv
```

This provides a foundation for improving query interpretation and system behavior over time.

---

## Design Principles

The project follows a modular architecture so that individual components can be developed and improved independently.

### Separation of Responsibilities

- Parser handles natural-language interpretation.
- Planner handles analytical planning.
- SQL generator creates SQL.
- SQL validator validates generated SQL.
- Executor runs SQL.
- Result validator checks results.
- Confidence module evaluates confidence.
- Explanation module generates explanations.
- Feedback module records feedback.

This makes the system easier to test, maintain, and extend.

---

## Future Improvements

Potential future enhancements include:

- Web-based analytics interface
- Conversational follow-up queries
- Support for additional databases
- More advanced semantic understanding
- Automatic chart generation
- Dashboard generation
- Query history
- User-specific analytics
- More advanced feedback-driven learning
- Streaming and large-scale dataset support
- Authentication and authorization
- REST API endpoints for external applications

---

## Project Status

```text
Natural Language Parsing       ✅
Deterministic Fallback        ✅
Query Planning                ✅
SQL Generation                ✅
SQL Validation                ✅
DuckDB Execution              ✅
Aggregation                   ✅
Grouping                      ✅
Ranking / Top-N               ✅
Contribution Analysis         ✅
Target Comparison             ✅
Nested Queries                ✅
YoY Analysis                  ✅
Confidence Scoring            ✅
Result Explanation            ✅
Feedback Logging              ✅
Sample Outputs                ✅
Supplied Queries              8/8 PASS
```

---

## Author

**Abhishek**

B.Tech (Hons.) Computer Science Engineering

GLA University

---

## License

This project is developed for academic and educational purposes.