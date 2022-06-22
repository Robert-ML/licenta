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

def draw_ocr_results(image, text, pts, color=(0, 255, 0)):
	# unpack the points list
	topLeft = pts[0]
	topRight = pts[1]
	bottomRight = pts[2]
	bottomLeft = pts[3]
	# draw the bounding box of the detected text
	cv2.line(image, topLeft, topRight, color, 2)
	cv2.line(image, topRight, bottomRight, color, 2)
	cv2.line(image, bottomRight, bottomLeft, color, 2)
	cv2.line(image, bottomLeft, topLeft, color, 2)
	# draw the text itself
	cv2.putText(image, text, (topLeft[0], topLeft[1] - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
	# return the output image
	return image

def OCR(file):
    imageData = open(file, "rb")
    image = cv2.imread(file)
    # initialize the client with endpoint URL and subscription key

    client = ComputerVisionClient(config.ENDPOINT_URL, CognitiveServicesCredentials(config.SUBSCRIPTION_KEY))
    # call the API with the image and get the raw data, grab the operation
    # location from the response, and grab the operation ID from the
    # operation location
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

    # make a copy of the input image for final output
    final = image.copy()
    # loop over the results
    for result in results.analyze_result.read_results:
        # loop over the lines
        for line in result.lines:
            # extract the OCR'd line from Microsoft's API and unpack the
            # bounding box coordinates
            text = line.text
            box = list(map(int, line.bounding_box))
            (tlX, tlY, trX, trY, brX, brY, blX, blY) = box
            pts = ((tlX, tlY), (trX, trY), (brX, brY), (blX, blY))
            # draw the output OCR line-by-line
            output = image.copy()
            output = draw_ocr_results(output, text, pts)
            final = draw_ocr_results(final, text, pts)
            # show the output OCR'd line
            print(text)
    # show the final output image
    # cv2.imwrite("./out/1.jpg", final)
    # cv2.imshow("Final Output", final)
    # cv2.waitKey(0)

def main():
    path_in = "../selected/"
    files = os.listdir(path_in)
    for file in files:
        print(file)
        OCR(path_in + file)
        print("\n")

if __name__ == "__main__":
    main()
