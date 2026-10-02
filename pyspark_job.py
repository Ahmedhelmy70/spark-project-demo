from pyspark.sql.functions import col

def clean_data(df):
    # Remove rows where amount <= 0 and name is NULL
    filtered_df = df.filter((col("amount") > 0) & col("name").isNotNull())
    
    # Add a column amount_with_tax calculated as amount * 1.20
    final_df = filtered_df.withColumn("amount_with_tax", col("amount") * 1.20)
    
    return final_df
