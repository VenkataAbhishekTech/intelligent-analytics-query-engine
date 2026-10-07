from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from app.data_loader import load_all_data
from app.schema_manager import SchemaManager
from app.engine import AnalyticsEngine


app = FastAPI(
    title="Intelligent Analytics Query Engine",
    description="Natural language analytics API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DASHBOARD_DIR = os.path.join(
    BASE_DIR,
    "dashboard"
)


app.mount(
    "/dashboard",
    StaticFiles(directory=DASHBOARD_DIR),
    name="dashboard"
)


class QueryRequest(BaseModel):
    query: str


print("Loading analytics engine...")

data = load_all_data()

sales_data = data["sales_data"]
targets = data["targets"]
data_dictionary = data["data_dictionary"]
connection = data["connection"]

schema_manager = SchemaManager(
    sales_data=sales_data,
    targets=targets,
    data_dictionary=data_dictionary
)

engine = AnalyticsEngine(
    schema_manager=schema_manager,
    connection=connection
)

print("Analytics engine loaded successfully.")


@app.get("/")
def dashboard():

    dashboard_path = os.path.join(
        DASHBOARD_DIR,
        "index.html"
    )

    return FileResponse(
        dashboard_path
    )


@app.get("/api/health")
def health():

    return {
        "status": "healthy",
        "service": "Intelligent Analytics Query Engine"
    }


@app.post("/api/query")
def process_query(
    request: QueryRequest
):

    query = request.query.strip()

    if not query:

        return {
            "success": False,
            "error": "Please enter a query."
        }

    try:

        result = engine.process_query(
            query
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


@app.get("/api/examples")
def examples():

    return {
        "examples": [
            "Total sales in India for March",
            "Top 2 cities by profit",
            "Average order value by region",
            "Which region missed its target in Feb?",
            "Sales contribution % by category",
            "Top product in each region",
            "YoY growth in revenue",
            "Revenue of top 3 customers per region"
        ]
    }