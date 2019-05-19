import pickle
import numpy
import matplotlib.pyplot as plt
import statistics
import random


def upack_pickle(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data

def get_selected_indexes_from_name(path):
    indexes = list()
    file_names = path.split(".")
    for file_name in file_names:
        strs = file_name.split("_")

        leng = len(strs)
        i = 0
        if leng < 2:
            break

        while i < leng:
            if strs[i].isdigit():
                if i + 1 < leng and strs[i+1].isdigit():
                    indexes.append((int(strs[i]), int(strs[i+1])))
                else:
                    indexes.clear()
            i += 2

        if indexes is not None and len(indexes) != 0:
            break

    if len(indexes) == 0:
        return None

    return indexes


def get_amount_modified(pic0, pic1, diff):
    if len(pic0.shape) != 3 or len(pic1.shape) != 3:
        raise ValueError()
    shape0 = pic0.shape
    shape1 = pic1.shape
    if shape0[0] != shape1[0] or shape0[1] != shape1[1] or shape0[2] != shape1[2]:
        raise ValueError()
    count = 0
    for i in range(0, shape0[0]):
        for j in range(0, shape0[1]):
            if points_are_different(pic0[i][j], pic1[i][j], diff):
                count += 1
    return count


def get_amount_modified_in_random(pic0, pic1, diff, random_points):
    if len(pic0.shape) != 3 or len(pic1.shape) != 3:
        raise ValueError()
    shape0 = pic0.shape
    shape1 = pic1.shape
    if shape0[0] != shape1[0] or shape0[1] != shape1[1] or shape0[2] != shape1[2]:
        raise ValueError()
    count = 0
    n_count = 0
    for i in range(0, shape0[0]):
        for j in range(0, shape0[1]):
            # flag indicates if i, j is modified
            if (i, j) in random_points:
                if points_are_different(pic0[i][j], pic1[i][j], diff):
                    count += 1
                elif neighbor_has_modified(i, j, pic0, pic1, diff):
                    n_count += 1

    return count, n_count


def neighbor_has_modified(i, j, pic0, pic1, diff):
    steps = [(0, 1), (0, -1), (1, 0), (-1, 0), (1 , 1), (1, -1), (-1, 1), (-1, -1)]
    for step in steps:
        f, g = i + step[0], j + step[1]
        if f < 0 or f >= pic0.shape[0] or g < 0 or g >= pic1.shape[0]:
            continue
        if points_are_different(pic0[f][g], pic1[f][g], diff):
            return True
    return False


def points_are_different(p0, p1, diff):
    if len(p0.shape) != 1 or len(p1.shape) != 1 or p0.shape[0] != p1.shape[0]:
        raise ValueError
    for k in range(0, p0.shape[0]):
        if is_modified(p0[k], p1[k], diff):
            return True
    return False


def is_modified(val0, val1, diff):
    return abs(val0 - val1) >= diff


def plot_image(pic):
    for i in range(0, pic.shape[0]):
        for j in range(0, pic.shape[1]):
            for k in range(0, pic.shape[2]):
                pic[i][j][k] = pic[i][j][k] + 0.5

    plt.imshow(pic)
    plt.show()

def gen_random_set(start, end, num):
    se = set()

    while len(se) < num:
        nextInt_x = random.randint(start, end)
        nextInt_y = random.randint(start, end)
        if (nextInt_x, nextInt_y) not in se:
            se.add( (nextInt_x, nextInt_y))
    debug = len(se)
    return se

def main0():
    lst = list()
    file_config = open("config", "r")
    configs = file_config.readlines()

    file_name_origin = configs[0]
    file_name_adv = configs[1]

    diff = float(configs[2])
    sampling_strs = configs[3].split()
    sampling_nums = [int(st) for st in sampling_strs]

    indexes = get_selected_indexes_from_name(file_name_adv)

    pics0 = upack_pickle(file_name_origin.strip())
    pics1 = upack_pickle(file_name_adv.strip())

    # get the width of the input picture
    # pictures are guranteed to be square
    width = pics0.shape[1]

    print("searching for modified points...")
    j = 0
    for indices in indexes:
        for i in range(indices[0], indices[1]):
            pic0 = pics0[i]
            pic1 = pics1[j]
            amount = get_amount_modified(pic0, pic1, diff)

            lst.append(amount)

            j += 1

    lst.append(statistics.mean(lst))
    print("writing results...")
    fo = open("how_many_are_modified_with_diff_" + str(diff) + '.txt', 'a')
    for num in lst:
        line = str(num) + r"," + "\n"
        fo.write(line)

    print("random sampling in figures and search for different points...")
    mp = dict()
    mp0 = dict()
    for num in sampling_nums:
        lst = list()
        lst0 = list()
        j = 0
        for indices in indexes:
            for i in range(indices[0], indices[1]):
                pic0 = pics0[i]
                pic1 = pics1[j]
                #generate random list

                random_points = gen_random_set(0, width, num)

                amount, amount0 = get_amount_modified_in_random(pic0, pic1, diff, random_points)

                lst.append(amount)
                lst0.append(amount0)

                j += 1

        lst.append(statistics.mean(lst))
        lst0.append(statistics.mean(lst0))
        mp[num] = lst
        mp0[num] = lst0
    print("writing results" + "...")
    fo = open("how_many_are_modified_in_random_points_with_diff_" + str(diff) + '.txt', 'a')
    for num, lst in mp.items():
        line = str(num) + r":" + str(lst) + "\n"
        fo.write(line)

    print("writing results" + "...")
    fo = open("how_many_not_modified_has_neighbor_modified_with_diff_" + str(diff) + '.txt', 'a')
    for num, lst0 in mp0.items():
        line = str(num) + r":" + str(lst0) + "\n"
        fo.write(line)

main0()



