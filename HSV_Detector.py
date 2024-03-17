import cv2 as cv
import numpy as np


def change_brightness(img, brightness):  # 修改图像的亮度，brightness取值0～2 <1表示变暗 >1表示变亮
    [averB, averG, averR] = np.array(cv.mean(img))[:-1] / 3
    k = np.ones((img.shape))
    k[:, :, 0] *= averB
    k[:, :, 1] *= averG
    k[:, :, 2] *= averR
    img = img + (brightness - 1) * k
    img[img > 255] = 255
    img[img < 0] = 0
    return img.astype(np.uint8)


def reshape_image_scan(image):  # 归一化图片尺寸：短边400，长边不超过800，短边400，长边超过800以长边800为主
    width, height = image.shape[1], image.shape[0]
    scale = width * 1.0 / 600
    new_width = 600

    new_height = int(height / scale)
    if new_height > 600:
        new_height = 600
        scale = height * 1.0 / 600
        new_width = int(width / scale)
    out = cv.resize(image, (new_width, new_height))
    return out, new_width, new_height

# # 遍历文件夹函数
# def getFileList(dir, Filelist, ext=None):
#     """
#     获取文件夹及其子文件夹中文件列表
#     输入 dir：文件夹根目录
#     输入 ext: 扩展名
#     返回： 文件路径列表
#     """
#     newDir = dir
#     if os.path.isfile(dir):
#         if ext is None:
#             Filelist.append(dir)
#         else:
#             if ext in dir[-3:]:
#                 Filelist.append(dir)
#
#     elif os.path.isdir(dir):
#         for s in os.listdir(dir):
#             newDir = os.path.join(dir, s)
#             getFileList(newDir, Filelist, ext)
#
#     return Filelist


# 鼠标响应事件
def onmouse(event, x, y, flags, param):
    cv.imshow("Original_image", img)
    # 双击
    if event == cv.EVENT_LBUTTONDBLCLK:
        print("(" + str(x) + "," + str(y) + ")的HSV为" + str(img_hsv[y, x]))


# 存放图片的文件夹路径,获取文件夹中所有图片
# path = "./images/"
# imglist = getFileList(path, [])
# for imgpath in imglist:

img = cv.imread("./Test.jpg")  # 读取图片
img = reshape_image_scan(img)[0]  # 归一化图片尺寸
img = change_brightness(img, 1.5)  # 修改图像的亮度，brightness取值0～2；<1表示变暗；>1表示变亮
cv.imshow("Original_image", img)
cv.namedWindow("Original_image")
cv.setMouseCallback("Original_image", onmouse)  # 设置鼠标响应事件,点击图片显示HSV值

img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # 将图片转化为HSV空间
mask = cv.inRange(img_hsv, np.array([63, 32, 70]), np.array([80, 255, 255]))  # 通过HSV空间的阈值分割得到蒙版
div = np.array(img)  # 复制图片
div[mask == 255] = [0, 0, 255]  # 将蒙版阈值区域涂为红色
cv.imshow("Masked", div)
cv.waitKey(0)
cv.destroyAllWindows()