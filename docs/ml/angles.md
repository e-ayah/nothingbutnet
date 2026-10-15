# Explanation of calculate_angle:

## Summary:
Takes in three points, one being the point where the angle lies and the other two being the endpoints of the vectors to figure out the angle, and uses the dot product formula to return the rounded angle.

## Step by Step:
1. Sets each given point to be an array instead for future calculations
2. Builds the first vector from the midpoint to the first point
3. Builds the second vector from the midpoint to the third point
4. Divides the dot product by the product of the two lengths to get the cosine value (if either length is 0, i.e. two joints are at the same spot, it returns None instead)
5. Clips the cosine value so that it remains between -1 and 1 due to potential floating point rounding errors
6. Changes the radians angle into degrees
7. Rounds the answer to one decimal place

## Worked Example by Hand:
- 90 Degree angle Release Example
Shoulder: (10, 10)
Elbow: (20, 10)
Wrist: (20, 20)

1. a, b, c = np.array([10,10]), np.array([20,10]), np.array([20,20])
2. vector_ba = [10, 10] - [20, 10] 
    # [-10, 0]
3. vector_bc = [20, 20] - [20, 10] 
    # [0, 10]
4. cosine = np.dot([-10,0], [0,10]) / (np.linalg.norm([-10,0]) * np.linalg.norm([0,10]))
    # 0.0
5. cosine = np.clip(0.0, -1.0, 1.0)
    # 0.0
6. angle = np.degrees(np.arccos(0.0))
    # 90.0
7. return round(angle,1)
    # 90.0

## np.clip Explanation:
np.clip exists in order to guarantee that the number given to the arccos function is between -1 and 1 as otherwise rounding can lead to cosine taking in 1.00001 which would lead to returning NaN when trying to do the arccos calculation