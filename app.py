from flask import Flask
from minio import Minio
from minio.error import S3Error
import os
app = Flask(__name__)

# Initialize MinIO client
minio_client = Minio(
    'localhost:9000',
    access_key='minioadmin',
    secret_key='console123',
    secure=False
)

# Create a bucket if it doesn't exist
bucket_name = "testbucketpoc"
if not minio_client.bucket_exists(bucket_name):
    minio_client.make_bucket(bucket_name)

@app.route('/push-data')
def push_data():
    try:
        file_path = "bmc_hosts_template.yaml"

        # Get the length of the file
        stat_info = os.stat(file_path)
        file_size = stat_info.st_size
        file_size
        with open("bmc_hosts_template.yaml", 'rb') as file_data:
            minio_client.put_object(
                bucket_name=bucket_name,
                object_name="bmc_hosts_template.yaml",
                data=file_data,
                length=file_size,
            )

    except S3Error as e:
        print(f"Error: {e}")

    return 'Hello\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
