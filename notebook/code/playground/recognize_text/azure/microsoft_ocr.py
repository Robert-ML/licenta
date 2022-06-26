# import the necessary packages
from config import microsoft_cognitive_services as config
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import argparse
import time
import sys
import cv2
import os
import time

def OCR(file, client):
    imageData = open(file, "rb")

    response = client.read_in_stream(imageData, raw=True)
    operationLocation = response.headers["Operation-Location"]
    operationID = operationLocation.split("/")[-1]

    # continue to poll the Cognitive Services API for a response until
    # we get a response
    while True:
        # get the result
        results = client.get_read_result(operationID)
        # check if the status is not "not started" or "running", if so,
        # stop the polling operation
        if results.status.lower() not in ["notstarted", "running"]:
            break

        # sleep for a bit before we make another request to the API
        time.sleep(10)
    # check to see if the request succeeded
    if results.status == OperationStatusCodes.succeeded:
        # print("[INFO] Microsoft Cognitive Services API request succeeded...")
        pass
    # if the request failed, show an error message and exit
    else:
        print("[INFO] Microsoft Cognitive Services API request failed")
        print("[INFO] Attempting to gracefully exit")
        sys.exit(0)

    text_l = []
    # loop over the results
    for result in results.analyze_result.read_results:
        # loop over the lines
        for line in result.lines:
            # extract the OCR'd line from Microsoft's API and unpack the
            # bounding box coordinates
            text = line.text
            # draw the output OCR line-by-line
            # show the output OCR'd line
            text_l.append(text)
            print(text)
    # show the final output image
    # cv2.imwrite("./out/1.jpg", final)
    # cv2.imshow("Final Output", final)
    # cv2.waitKey(0)
    return text_l

def main():
    path_in = "../evaluate/"
    files = os.listdir(path_in)

    client = ComputerVisionClient(config.ENDPOINT_URL, CognitiveServicesCredentials(config.SUBSCRIPTION_KEY))

    time_total = []

    for file in files:
        # if file end in .png is ok
        if not file.endswith(".png"):
            continue

        print(file)
        time_start = time.time()
        text = OCR(path_in + file, client)
        print("\n")
        time_end = time.time()
        time_total.append(time_end - time_start)

        file_name = file.split(".")[0]
        with open(path_in + file_name + ".txt", "w") as f:
            f.write(str(text))

    with (open("/mnt/HD/School/A4/licenta/notebook/code/playground/detect_text/evaluation/times-stage3.txt", "w")) as f:
        f.write(str(time_total))

if __name__ == "__main__":
    main()
