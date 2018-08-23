"""by xiaoyan huang"""

import time
from operator import itemgetter


# 从txt文件中拿到数据
def get_data(filename):
    user_goods = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            user_id, goods_id, score = line.split('\t')
            if user_id not in user_goods:
                user_goods.setdefault(user_id, [])
            user_goods[user_id].append(goods_id)
    return user_goods


def sortout(index, wacth_data):
    top_goods = get_user(index)
    base_info = {}
    if top_goods != None:
        for key in top_goods:
            k = str(key[0])
            # print(k)
            base_info.setdefault(k, [])
            base_info[k] = wacth_data[k]
    return base_info


# 找出购买过对应商品的用户
# 把所有符合条件的用户购买记录统计，(剔除指定商品)以商品出现的频次倒叙排列取top6
def get_user(goods_id):
    user_goods = get_data('hxy_user_data2.txt')
    goods_number = {}
    for user, goods in user_goods.items():
        if goods_id in goods:
            for i in user_goods[user]:
                if i != goods_id:
                    if i not in goods_number:
                        goods_number.setdefault(i, 1)
                    else:
                        number = int(goods_number[i]) + 1
                        goods_number[i] = number
    sorted_goods = sorted(goods_number.items(), key=itemgetter(1), reverse=True)[0:6]
    return sorted_goods


if __name__ == '__main__':
    # filename = 'user_data.txt'
    # user_goods = get_data(filename)

    def data(filename):
        wacth_data = {}
        base_data = {}
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip('\n')
                line = line.split('\t')
                wacth_id = line.pop(0)
                wacth_data.setdefault(wacth_id, [])
                wacth_data[wacth_id] = line
        for i in range(48):
            base_data.setdefault(str(i), [])
            base_data[str(i)] = wacth_data[str(i)]
        return wacth_data, base_data
    filename = 'hxy_wacth_info.txt'
    wacth_data, base_data = data(filename)

    t1 = time.time()
    print(get_user('0'))
    t2 = time.time()
    print(sortout('0', wacth_data))
    t3 = time.time()
    print(str(t2-t1))
    print(str(t3-t2))
