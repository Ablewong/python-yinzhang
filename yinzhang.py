import cv2 as cv

#设置 Y, X值
yzY=410
yzY1=yzY+124
yzX=480
yzX1=yzX+130

def alpha2black_opencv2(img):
    width, height, channels = img.shape

    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]
            if(color_d[3] == 0):
                img[xw, yh] = [0, 0, 0, 0]

    return cv.cvtColor(img, cv.COLOR_BGRA2BGR)

# 读取图片
def read_img(path):
    img = cv.imread(path, -1)

    dst = cv.resize(img, (130, 124))
    # cv.imshow("img", dst)
    # 接下来将 png 透明部分处理成黑色
    ret = alpha2black_opencv2(dst)
    # cv.imshow("ret", ret)

    # 加载背景图
    bg = cv.imread("./test.png")
    print(bg)
    # 获取目标 roi
    roi = bg[yzY:yzY1, yzX:yzX1]
    #cv.imshow("roi",roi)
    # 将印章与roi进行叠加
    mask = cv.cvtColor(ret, cv.COLOR_BGR2GRAY)

    # 想要得到红色印章和背景融合的图
    # 获取印章的二值化图像，红色印章为纯白色
    thresh, new_mask = cv.threshold(mask, 10, 255, cv.THRESH_BINARY)

    # 获取反向图
    mask_inv = cv.bitwise_not(new_mask)
    # cv.imshow("mask_inv",mask_inv)
    # 第一步：在原图中抠出印章区域，即印章区域为黑色
    new_img = cv.add(roi, 1, mask = mask_inv)
    # cv.imshow("new_img", new_img)
    # 第二步，将抠出印章区域得到的图片与印章相加，获取到合成图
    replace_img = cv.add(new_img,ret)
    print(replace_img.shape)
    # cv.imshow("bg", bg)
    # 第三步，将合成好的图片，送回到原图
    bg[yzY:yzY1, yzX:yzX1] = replace_img
    cv.imshow("bg",bg)
    #cv.imwrite("./bg.png",bg) #将合成图片另存为bg.png


if __name__ == "__main__":
    # png 透明图片路径
    path = r"./123.png"
    read_img(path)

    cv.waitKey()
    cv.destroyAllWindows()