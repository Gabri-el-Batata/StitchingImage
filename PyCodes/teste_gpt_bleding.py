# A = image1.copy()
# B = image2.copy()

# print(A.shape, B.shape)

# gpA = [A]
# for i in range(6):
#     A = cv.pyrDown(A)
#     gpA.append(A)

# gpB = [B]
# for i in range(6):
#     B = cv.pyrDown(B)
#     gpB.append(B)

# lpA = [gpA[5]]
# for i in range(5, 0, -1):
#     GE = cv.pyrUp(gpA[i])
#     GE = cv.resize(GE, (gpA[i-1].shape[1], gpA[i-1].shape[0]))  # Redimensiona para garantir o mesmo tamanho
#     LA = cv.subtract(gpA[i-1], GE)
#     lpA.append(LA)

# lpB = [gpB[5]]
# for i in range(5, 0, -1):
#     GE = cv.pyrUp(gpB[i])
#     GE = cv.resize(GE, (gpB[i-1].shape[1], gpB[i-1].shape[0]))  # Redimensiona para garantir o mesmo tamanho
#     LB = cv.subtract(gpB[i-1], GE)
#     lpB.append(LB)


# LS = []

# for la, lb in zip(lpA, lpB):
#     cols, rows, _ = la.shape
#     ls = np.hstack((la[:, :cols//2], lb[:, cols//2:]))
#     LS.append(ls)

# lsc = LS[0]
# for i in range(1, 6):
#     lsc = cv.pyrUp(lsc)
#     lsc = cv.resize(lsc, (LS[i].shape[1], LS[i].shape[0]))
#     lsc = cv.add(lsc, LS[i])

# cv.imshow('piramid', lsc)
# cv.waitKey(0)
