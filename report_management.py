import boto3
import pandas as pd
import mariadb
import sys

aws_access_key_id = 'access_key_id'
aws_secret_access_key = 'secret_access_key'
region = 'aws_region'
s3_bucket_name = 's3_bucket_name'

db_host = 'database_host'
db_port = 3306
db_user = 'database_user'
db_password = 'database_password'
db_name = 'database_name'

def fetch_and_store_data():
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region)

    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
        files = [obj['Key'] for obj in response.get('Contents', [])]

        for file in files:
            csv_data = s3_client.get_object(Bucket=s3_bucket_name, Key=file)['Body'].read().decode('utf-8')

            df = pd.read_csv(pd.compat.StringIO(csv_data))

            with mariadb.connect(
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port,
                    database=db_name
            ) as conn:
                with conn.cursor() as cursor:
                    for index, row in df.iterrows():
                        sql = "query"
                        cursor.execute(sql)

                conn.commit()

            print(f"Data from {file} inserted into MariaDB.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_and_store_data()