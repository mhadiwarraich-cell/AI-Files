import cv2


image = cv2.imread('Ronaldo.jpeg')


cv2.nameWindow('Load Image', cv2.WINDOW_NORMAL)

cv2.resizeWindow('Load Image', 800,500)

cv2.imshow('Load Image', image)

cv2.waitKey(0)

cv2.destroyAllWindows()

print(f"Image Dimensiona: {image.shape}")
