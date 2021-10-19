import boto3
from scrapy.exporters import JsonItemExporter
from scrapy.utils.project import get_project_settings

class JsonS3Exporter(JsonItemExporter):
    
    def __init__(self, name):
        self._name = name
        self._file = open(self.where_is, 'w+b')
        super().__init__(self._file)

        # Get the s3 client
        settings = get_project_settings()
        self._to_up = settings.get("AWS_UPLOAD_TO_BUCKET")

        if self._to_up:
            self._s3 = boto3.client('s3')
            self._bucket = settings.get("AWS_BUCKET")
    
    def finish_exporting(self):
        super().finish_exporting()
        self._file.close()

        if self._to_up:
            with open(self.where_is, 'r+b') as body:
                return self._s3.put_object(
                    Bucket = self._bucket,
                    Key = self._name,
                    Body = body
                )
    
    @property
    def where_is(self):
        return f'/tmp/{self._name}.json'