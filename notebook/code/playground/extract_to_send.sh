#!/bin/bash

FILE=20211021_131724

mkdir -p ./to_send/0in/
mkdir -p ./to_send/1sobel_on_original/
mkdir -p ./to_send/2canny_on_original/
mkdir -p ./to_send/3clahe_on_original/
mkdir -p ./to_send/4threshold_on_original/
mkdir -p ./to_send/5canny-n-sobel_on_clahe/
mkdir -p ./to_send/6threshold_on_clahe/
mkdir -p ./to_send/7hats/

cp ./in/prepared/${FILE}* ./to_send/0in/
cp ./out/sobel_on_original/test_${FILE}* ./to_send/1sobel_on_original/
cp ./out/canny_on_original/test_${FILE}* ./to_send/2canny_on_original/
cp ./out/clahe_on_original/test_${FILE}* ./to_send/3clahe_on_original/
cp ./out/threshold_on_original/test_${FILE}* ./to_send/4threshold_on_original/
cp ./out/canny-n-sobel_on_clahe/test_${FILE}* ./to_send/5canny-n-sobel_on_clahe/
cp ./out/threshold_on_clahe/test_${FILE}* ./to_send/6threshold_on_clahe/
cp ./out/hats/test_${FILE}* ./to_send/7hats/

