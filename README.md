# Intelligent Analytics Query Engine

An AI-powered natural language analytics engine that allows users to ask business questions in plain English and automatically converts them into executable SQL queries.

The system combines natural-language understanding, deterministic fallback parsing, structured query planning, SQL generation, SQL validation, DuckDB execution, confidence scoring, explanations, feedback logging, and a professional web dashboard into a modular analytics pipeline.

---

## 🚀 Overview

Traditional analytics systems often require users to understand SQL or navigate complex dashboards.

This project provides a simpler approach:

```text
Business Question
       ↓
Natural Language
       ↓
Query Understanding
       ↓
Structured Query Plan
       ↓
SQL Generation
       ↓
SQL Validation
       ↓
DuckDB Execution
       ↓
Result
       ↓
Confidence + Explanation

✨ Key Features
- Natural-language business query processing
- LLM-based query understanding using Google Gemini
- Deterministic fallback parser
- Structured query planning
- Automatic SQL generation
- SQL validation before execution
- DuckDB analytical query execution
- Aggregation and filtering
- Grouping analysis
- Top-N analysis
- Ranking within groups
- Contribution percentage analysis
- Target comparison
- Nested analytical queries
- Year-over-Year revenue analysis
- Confidence scoring
- Natural-language explanations
- Feedback logging
- Automatic sample-output generation
- FastAPI backend
- Professional web dashboard
- Automated testing with pytest


🏗️ System Architecture

                    Natural Language Query
                              |
                              v
                  +------------------------+
                  |    Gemini / Fallback   |
                  |         Parser         |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |     Query Planner      |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |      Query Plan        |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |     SQL Generator      |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |     SQL Validator      |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |     DuckDB Engine      |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |   Confidence Score     |
                  +------------------------+
                              |
                              v
                  +------------------------+
                  |      Explanation       |
                  +------------------------+
                              |
                              v
                       Final Result
                              |
                              v
                    FastAPI Dashboard


Technologies Used:
Technology	      Purpose
Python    	      Core application development
Google            Gemini	Natural-language query understanding
DuckDB	          Analytical SQL execution
Pandas	          Data loading and manipulation
Pydantic	        Structured query-plan validation
FastAPI	          API and web application backend
Uvicorn	          ASGI server
HTML	            Dashboard structure
CSS	              Dashboard styling
JavaScript	      Dashboard interaction
pytest	          Automated testing
python-dotenv	    Environment configuration             



Dataset
The project uses sample business-sales data containing information such as:
- Customer
- Product
- Product Category
- Region
- Country
- City
- Quantity
- Unit Price
- Discount
- Profit
- Order Date
The project also contains target data for comparing actual revenue against target revenue.
Dataset files:
dataset/
├── sales_data.csv
├── targets.csv
├── data_dictionary.json
├── nl_queries.json
└── feedback_log.csv


Test Coverage
The automated tests verify:
- Basic revenue aggregation
- Country filtering
- Month filtering
- Top-N city ranking
- Average Order Value
- Target comparison
- Contribution percentage
- Product ranking by region
- Year-over-Year analysis
- Customer ranking by region

Design Principles
The project follows a modular architecture so that individual components can be developed and improved independently.
Separation of Responsibilities
Component	Responsibility
Parser	Natural-language interpretation
Query Plan	Structured analytical representation
SQL Generator	Converts query plans into SQL
SQL Validator	Validates generated SQL
DuckDB	Executes analytical SQL
Confidence Module	Calculates confidence
Explanation Module	Generates explanations
Feedback Module	Records query feedback
FastAPI	Provides API endpoints
Dashboard	Provides the user interface


This separation makes the system easier to:
- Test
- Maintain
- Debug
- Extend
- Integrate with other applications
Project Status
Natural Language Parsing       ✅
Deterministic Fallback         ✅
Query Planning                 ✅
SQL Generation                 ✅
SQL Validation                 ✅
DuckDB Execution               ✅
Aggregation                    ✅
Filtering                      ✅
Grouping                       ✅
Ranking / Top-N                ✅
Contribution Analysis          ✅
Target Comparison              ✅
Nested Queries                 ✅
YoY Analysis                   ✅
Confidence Scoring             ✅
Result Explanation             ✅
Feedback Logging               ✅
Sample Outputs                 ✅
FastAPI Backend                ✅
Web Dashboard                  ✅
Automated Testing              ✅
Supplied Queries               8/8 PASS

Future Improvements
Potential future enhancements include:
- Conversational follow-up queries
- Automatic chart generation
- Query history
- Additional database connectors
- Advanced semantic understanding
- Larger dataset support
- Streaming analytics
- Authentication and authorization
- Advanced feedback-driven learning
- User-specific analytics
- Enterprise analytics integrations
- Advanced visualization capabilities
Project Highlights
This project demonstrates practical implementation of:
- Generative AI
- Natural Language Processing
- Natural Language to SQL
- Query Planning
- SQL Generation
- SQL Validation
- Data Analytics
- Analytical Database Processing
- DuckDB
- FastAPI
- REST API Development
- Web Dashboard Development
- Automated Testing
- Confidence Scoring
- Explainable AI Concepts
- Modular Software Architecture
Portfolio Value
The project demonstrates how AI can be used to make analytical systems easier for non-technical users.
Instead of requiring users to write:
SELECT city, SUM(profit)
FROM sales_data
GROUP BY city
ORDER BY SUM(profit) DESC
LIMIT 2;

the user can simply ask:
Top 2 cities by profit

The engine handles the analytical translation automatically.
This project demonstrates the integration of AI, data analytics, SQL generation, database execution, API development, web interfaces, and automated testing into a single end-to-end system.
