import functions_framework
from flask import request, jsonify
import json
import base64
from google.cloud import storage
import dotenv
import os
import time
import re
import vertexai
from vertexai.generative_models import GenerativeModel, Part

vertexai.init(project="petrosa-data", location="us-central1")

# ORIGINAL URL https://us-central1-petrosa-data.cloudfunctions.net/video_interivewer_be

def to_snake_case(text):
    words = re.split(r"\s+", text)
    snake_case_text = "_".join(word.lower() for word in words)
    return snake_case_text


dotenv.load_dotenv()
PREFIX = os.getenv("PREFIX")
BUCKET = os.getenv("BUCKET")
SUFFIX = os.getenv("SUFFIX")


def generate_prompt(jd):

    prompt = f"""This is the video of a candidate. 

    {jd}

    Answer the following questions based on the video, and repeat the questions in the answer.

    Describe the candidate in the video and his appeareance. 
    Quality of the english of the candidate. (1-10, where 1 is the worst and 10 is the best)
    Is the candidate a good fit for the job? 
    Is the candidate good and articulate in describing his career?
    Should the candidate proceed to the next steps like deep technical interview and client-side interview?
    Was there any signs of cheating in the video (using AI, other screen, reading answers)?
    Was there any red flags in the video?
    Post the full transcription.
    """
    
    return prompt

vision_model = GenerativeModel("gemini-1.5-flash-002")


def upload_to_gcs(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


@functions_framework.http
def receive_video(request):
    post_json = request.get_json()

    video_name = f"{to_snake_case(post_json['name'])}-{post_json['stack']}-{int(time.time())}.webm"

    data_dict = post_json

    with open(video_name, "wb") as fh:
        data = data_dict["data"].split(",")[-1]
        fh.write(base64.b64decode(data))

        upload_to_gcs(BUCKET, video_name, video_name)

    response = vision_model.generate_content(
        [
            Part.from_uri(
                f"{PREFIX}{BUCKET}/{video_name}",
                mime_type="video/webm",
            ),
            generate_prompt(post_json["jd"]),
        ]
    )

    response_text_file = f"{video_name}.txt"
    with open(response_text_file, "w") as file:
        file.write(response.text)

    upload_to_gcs(BUCKET, response_text_file, response_text_file)

    return jsonify({"message": response.text})
