import numpy as np
import pickle

def create_image(x, y, d, val):
    tmp = np.full((x, y, d), val)
    return np.array(tmp, dtype=np.float)


def alter_image(a, b, c, d, img, val):
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if c >= i >= a and d >= j >= b:
                for k in range(0, img.shape[2]):
                    img[i][j][k] = val



def main():
    val0 = 0
    val1 = 0.5

    image = create_image(32, 32, 3, val0)
    image0 = image.copy()
    alter_image(0, 16, 31, 31, image0, val1)
    image = image.reshape((1, 32, 32, 3))
    image0 = image0.reshape((1, 32, 32, 3))

    f0 = open("dump_test0.pkl", 'wb')
    pickle.dump(image, f0)
    f1 = open('dump_test1_0_1.pkl', 'wb')
    pickle.dump(image0, f1)

main()