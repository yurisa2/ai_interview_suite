import functions_framework
from flask import request, jsonify
import json
import base64
from google.cloud import storage
import dotenv
import os

dotenv.load_dotenv()
BUCKET = os.getenv("BUCKET")


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


@functions_framework.http
def receive_video(request):
    video_data = request.get_data()

    # with open("received_video.pkl", "wb") as f:
    #     pickle.dump(video_data, f)

    data_decoded = video_data.decode("utf-8")
    data_dict = json.loads(data_decoded)

    with open("imageToSave.webm", "wb") as fh:
        data = data_dict["data"].split(",")[-1]
        fh.write(base64.b64decode(data))

        upload_to_gcs(BUCKET, "imageToSave.webm", "imageToSave.webm")

    return jsonify({"message": "Taurine received and pickled successfully."})
