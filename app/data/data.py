import cv2

# Parte 1-A
background_subtractor_original = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=10, detectShadows=True
)
background_subtractor_histogram = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=10, detectShadows=True
)
background_subtractor_clahe = cv2.createBackgroundSubtractorMOG2(
    history=1000, varThreshold=10, detectShadows=True
)

# Parte 1-B
media = 0
deviation = 0
variance = 0

# Parte 2