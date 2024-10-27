import boto3
import pickle
from bloom_filter import BloomFilter
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__)) + '/data/'
print(DATA_DIR)

class S3Utils:
    def __init__(self, bucket_name):
        self.s3_resource = boto3.resource('s3')
        self.bucket_name = bucket_name

    def write_pickle(self, key, obj):
        pickle_byte_obj = pickle.dumps(obj)
        self.s3_resource.Object(self.bucket_name, key).put(Body=pickle_byte_obj)

    def read_pickle(self, key):
        obj = self.s3_resource.Object(self.bucket_name, key).get()['Body'].read()
        return pickle.loads(obj)

    def write_txt_file(self, key, data):
        text = "/n".join(data)
        self.s3_resource.Object(self.bucket_name, key).put(Body=text)

    def get_s3_storage_gb(self):
        bucket_name = self.bucket_name
        cloudwatch = boto3.client('cloudwatch')
        response = cloudwatch.get_metric_statistics(
            Namespace="AWS/S3",
            MetricName="BucketSizeBytes",
            Dimensions=[
                {
                    "Name": "BucketName",
                    "Value": bucket_name
                },
                {
                    "Name": "StorageType",
                    "Value": "StandardStorage"
                }
            ],
            StartTime=datetime.now() - timedelta(days=1),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=['Average']
        )

        bucket_size_bytes = response['Datapoints'][-1]['Average']
        return bucket_size_bytes


def pickle_data(data, name):
    file_name = DATA_DIR + name + '.pkl'
    with open(file_name, 'wb') as f:
        pickle.dump(data, f)

def unpickle_data(name):
    file_name = DATA_DIR + name + '.pkl'
    with open(file_name, 'rb') as f:
        data = pickle.load(f)
    return data
