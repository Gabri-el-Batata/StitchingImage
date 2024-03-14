import cv2 as cv
import numpy as np

GRAYCOLOR = cv.COLOR_BGR2GRAY

PINKCOLOR = (255, 0, 255)

img1 = cv.imread('foto0.png')
img2 = cv.imread('foto1.png')

img1_gray = cv.cvtColor(img1, GRAYCOLOR)
img2_gray = cv.cvtColor(img2, GRAYCOLOR)

orb = cv.ORB.create(nfeatures=2000)

kp1, dc1 = orb.detectAndCompute(img1, None)
kp2, dc2 = orb.detectAndCompute(img2, None)

bf = cv.BFMatcher(cv.NORM_HAMMING)

matches = bf.knnMatch(dc1, dc2, k=2)

good = []
for m,n in matches:
    if m.distance < 0.6 * n.distance:
        good.append(m)

# Draw matches
img_matches = cv.drawMatches(img1, kp1, img2, kp2, good, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

# Display matches (optional)
cv.imshow("Matches", img_matches)
cv.waitKey(0)
cv.destroyAllWindows()
        
def warpImages(img1, img2, H):

  rows1, cols1 = img1.shape[:2]
  rows2, cols2 = img2.shape[:2]

  list_of_points_1 = np.float32([[0,0], [0, rows1],[cols1, rows1], [cols1, 0]]).reshape(-1, 1, 2)
  temp_points = np.float32([[0,0], [0,rows2], [cols2,rows2], [cols2,0]]).reshape(-1,1,2)

  # When we have established a homography we need to warp perspective
  # Change field of view
  list_of_points_2 = cv.perspectiveTransform(temp_points, H)

  list_of_points = np.concatenate((list_of_points_1,list_of_points_2), axis=0)

  [x_min, y_min] = np.int32(list_of_points.min(axis=0).ravel() - 0.5)
  [x_max, y_max] = np.int32(list_of_points.max(axis=0).ravel() + 0.5)
  
  translation_dist = [-x_min,-y_min]
  
  H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

  output_img = cv.warpPerspective(img2, H_translation.dot(H), (x_max-x_min, y_max-y_min))
  output_img[translation_dist[1]:rows1+translation_dist[1], translation_dist[0]:cols1+translation_dist[0]] = img1

  return output_img

MIN_MATCH_COUNT = 10

if len(good) > MIN_MATCH_COUNT:
    # Convert keypoints to an argument for findHomography
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good]).reshape(-1,1,2)

    # Establish a homography
    M, _ = cv.findHomography(src_pts, dst_pts, cv.RANSAC,4)
    
    result = warpImages(img2, img1, M)

    cv.imshow('', result)
    cv.waitKey(0)
    cv.destroyAllWindows()
