from flask import Flask, render_template, request
import boto3
from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

app = Flask(__name__)

# Initialize the S3 client and set up a bucket
def initialize_s3():
  s3_client = boto3.client('s3', endpoint_url='http://127.0.0.1:9000', aws_access_key_id='ROOTNAME', aws_secret_access_key='CHANGEME123')
  bucket_name = 'my-bucket'
  return s3_client, bucket_name

s3_client, bucket_name = initialize_s3()
try:
  s3_client.create_bucket(Bucket=bucket_name)
  print('Bucket created')
except Exception as e:
  print(f'Bucket exists or {e}. Line 25.')

# Define the homepage route
@app.route('/')
def index():
	return render_template('index.html')

# Define the file upload route
@app.route('/upload', methods=['POST'])
def upload():
	file = request.files['file']
	s3_client.upload_fileobj(file, bucket_name, file.filename)
	return 'File uploaded successfully!'

# Define the route for file storage
@app.route('/storage')
def storage():
  try:
    s3_client.create_bucket(Bucket=bucket_name)
    print('Bucket created')
  except Exception as e:
    print(f'Bucket exists or {e}')
  objects = s3_client.list_objects(Bucket=bucket_name)
  links = [s3_client.generate_presigned_url(
				'get_object',
				Params={'Bucket': bucket_name, 'Key': obj['Key']},
				ExpiresIn=3600)
			 for obj in objects['Contents']]
  return render_template('storage.html', links=links)

if __name__ == '__main__':
	app.run(debug=True, port=3000)