import os
import boto3
from moto import mock_s3
from scrape.exporters import JsonS3Exporter

@mock_s3
def test_should_upload_file_to_s3_when_method_finish_to_call(mocker):
    mocker.patch('scrape.exporters.get_project_settings', return_value={
        'AWS_BUCKET': 'drummy',
        'AWS_ACCESS_KEY_ID': '11111',
        'AWS_SECRET_ACCESS_KEY': '********',
        'AWS_UPLOAD_TO_BUCKET': True
    })

    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket='drummy')

    json = JsonS3Exporter('stocks_test')
    json.start_exporting()
    
    json.export_item({"name": "moto"})
    json.finish_exporting()

    body = conn.Object('drummy', 'stocks_test').get()['Body'].read().decode("utf-8")
    assert body == '[{"name": "moto"}]'

def test_should_not_upload_when_to_bucket_is_False(mocker):
    mocker.patch('scrape.exporters.get_project_settings', return_value={
        'AWS_UPLOAD_TO_BUCKET': False
    })

    json = JsonS3Exporter('stocks_test')
    json.start_exporting()
    
    json.export_item({"name": "moto"})
    json.finish_exporting()

    assert hasattr(json, '_s3') is False
    assert json._to_up is False

def test_should_create_a_file_in_temp(mocker):
    mocker.patch('scrape.exporters.get_project_settings', return_value={
        'AWS_UPLOAD_TO_BUCKET': False
    })

    json = JsonS3Exporter('stocks_test')
    json.start_exporting()
    
    json.export_item({"name": "moto"})
    json.finish_exporting()

    assert os.path.isfile(json.where_is)