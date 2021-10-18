import boto3
from moto import mock_s3
from scrape.exporters import JsonS3Exporter

@mock_s3
def test_should_upload_file_to_s3_when_method_finish_to_call():
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='dummy')

    json = JsonS3Exporter('stocks_test')
    json.start_exporting()
    
    json.export_item({"name": "moto"})
    json.finish_exporting()

    body = conn.Object('dummy', 'stocks_test').get()['Body'].read().decode("utf-8")
    assert body == '[{"name": "moto"}]'