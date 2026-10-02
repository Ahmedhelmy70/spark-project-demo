import pytest
from pyspark.sql import SparkSession
from pyspark_job import clean_data

@pytest.fixture(scope="session")
def spark():
    # Initialize a local Spark session for testing
    return SparkSession.builder.master("local[1]").appName("PySparkCI").getOrCreate()

def test_clean_data(spark):
    # Mock data covering all valid and invalid test cases
    data = [
        ("Alice", 100.0),    # Valid record
        ("Bob", -50.0),      # Invalid: amount < 0
        ("Charlie", 0.0),    # Invalid: amount == 0
        (None, 200.0)        # Invalid: name is NULL
    ]
    columns = ["name", "amount"]
    df = spark.createDataFrame(data, columns)

    # Execute the transformation function
    result_df = clean_data(df)
    results = result_df.collect()

    # 1. Verify valid records are kept and invalid records are removed
    assert len(results) == 1
    
    # 2. Verify records with amount <= 0 and NULL names are removed
    assert results[0]["name"] == "Alice"
    
    # 3. Verify amount_with_tax is calculated correctly (100 * 1.20 = 120.0)
    assert results[0]["amount_with_tax"] == 120.0
