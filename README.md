# Date Detection from Images

A system built to extract date information from images of payment bills, and receipts. This was done using python programming, OpenCV and Optical Character Recognition (OCR)

This program was hosted on REST API created in AWS cloud as a lambda function. When this function is triggered, it takes in an image and scans for any available date information. 


### Flowchart

Since most images have different qualities the first step was to convert it to a grayscale format. Various thresholding values are applied continuously in a loop as different images are captured at various exposure levels. 

The characters present are then extracted using OCR and are scanned for date information in various formats  
