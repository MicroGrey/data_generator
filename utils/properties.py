import cv2
import filter
# Read Image
def circle_point(image, pts):
    for pt in pts:
        print(pt)
        cv2.circle(image, (int(pt[0]), int(pt[1])), 1, (255,255,0), 4)
    
    return image

image = cv2.imread("20250511020232340.png")

# If checked
if image is None:
    print("图像读取失败！请检查路径。")
else:
    height, width = image.shape[:2]
    image = circle_point(image, [(321.51167999999996, 490.043136), (470.51776000000007, 363.709632)])
    cv2.imshow("Image with Circle", image)
    print(f"图像分辨率为：{width} x {height}")
    print(filter.distance((268.76416, 474.17625599999997), (470.51776000000007, 363.709632)))
    print(filter.distance((337.52192, 437.152512), (470.51776000000007, 363.709632)))
    cv2.waitKey(0)