import boto3
from scrapy.exporters import JsonItemExporter
from scrapy.utils.project import get_project_settings

class JsonS3Exporter(JsonItemExporter):
    
    def __init__(self, name):
        self._file = open(f'/tmp/{name}.json', 'w+b')
        super().__init__(self._file)

        # Get the s3 client
        settings = get_project_settings()

        self._s3 = boto3.client('s3')
        self._bucket = settings.get("AWS_BUCKET")
        self._name = name
    
    def finish_exporting(self):
        super().finish_exporting()
        self._file.close()

        with open(f'/tmp/{self._name}.json', 'r+b') as body:
            return self._s3.put_object(
                Bucket = self._bucket,
                Key = self._name,
                Body = body
            )