import functions_framework
from flask import request, jsonify
import pickle
import json
import base64

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

    return jsonify({"message": "Taurine received and pickled successfully."})
