import cv2

# |----------| | Parte 1-A | |----------|
operationMask = "0"
equalizeOption = ""

class EqualizeSelectOptions:
    original="Original"
    histogram="Histograma"
    clahe="CLAHE"

background_subtractor_original = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=10, detectShadows=True
)
background_subtractor_histogram = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=10, detectShadows=True
)
background_subtractor_clahe = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=10, detectShadows=True
)

# |----------| | Parte 1-B | |----------|
media = 0.0
deviation = 0.0
variance = 0.0

widthMask = 0
heightMask = 0
border = ""
filterSelected = ""
kernel=0

class TypeBordersOptions:
    sobel="Sobel"
    candy="Candy"

class TypeFilters:
    median="median"
    blur="blur"
    gaussian="gaussian"
    noOne="noOne"

# |----------| | Parte 2 | |----------|