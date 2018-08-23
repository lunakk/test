"""基于用户相似度的协同过滤推荐算法

    初始数据：txt文本，一行表示一个用户对一件购买过的商品的评分
    最终结果：作为推荐的商品的编号的列表
        by xiaoyan huang"""
import hxy_recomment
import time
from math import sqrt
from operator import itemgetter


# 1.拿到用户购买的所有商品信息 & 所有商品信息
# 用户购买的所有商品信息：user_goods_info
# {id:[goods_id,...],
# ...}
# 所有商品信息 goods_info
# {goods_id:[name,price,...],
# ...}

# 2.计算用户两两之间共同购买的商品数
# {u:{v:12, vv:15, vvv:25,...}, v:{u:12}}
# 1.倒排
# 商品对用户的倒排
# {goods_id:[u1,u2],...}
# 稀疏矩阵
# 密集矩阵，计算机计算密集矩阵的效率>>稀疏矩阵
def get_goods_num(user_goods_info):
    goods_user = {}
    for user, goods_list in user_goods_info.items():
        for goods_id in goods_list:
            if goods_id not in goods_user:
                goods_user.setdefault(goods_id, [])
            goods_user[goods_id].append(user)
    user_similar = {}
    for goods_id, user_list in goods_user.items():
        for u in user_list:
            for v in user_list:
                if u == v:
                    continue
                if u not in user_similar:
                    user_similar.setdefault(u, {})
                if v not in user_similar[u]:
                    user_similar[u].setdefault(v, 0)
                user_similar[u][v] += 1
    return user_similar


# 3.使用余弦公式计算两两用户之间的相似度
# 余弦公式
# A,B共同购买的商品数/sqrt(A购买的商品数*B购买的商品数)
# A商品数=len(user_goods_info[A])
def get_user_similar(user_goods_info, user_similar):
    for u, uvw in user_similar.items():
        for v, counts in uvw.items():
            u_counts = len(user_goods_info[u])
            v_counts = len(user_goods_info[v])
            # {u:{v:0.751254, vv:0.85452, vvv:0.951245,...}, v:{u:0.12454}}
            user_similar[u][v] = counts / sqrt(u_counts * v_counts)
    return user_similar


# 4.针对指定用户，拿到与他最相似的10个用户
# 排序取top10
def get_similar_user(user_id, user_similar):
    user_similar_dict = user_similar.get(user_id, -1)
    user_similar_dict = sorted(user_similar_dict.items(), key=itemgetter(1), reverse=True)[:10]
    return user_similar_dict


# 5.统计这10个用户购买过的商品，剔除目标用户已购买的商品，商品的推荐指数为用户相似度相加，倒排取top5
# {goods_id:0.454512+0.784512+0.9451245}
def get_similar_goods(user_similar_dict, user_goods, user_id):
    user_goods_top = {}
    goods_number = {}
    exept_goods = user_goods[user_id]
    new_similar_dict = {}
    for i in user_similar_dict:
        user_goods_top.setdefault(i[0], [])
        user_goods_top[i[0]] = user_goods[i[0]]
        new_similar_dict.setdefault(i[0], 0)
        new_similar_dict[i[0]] = i[1]
    for user, goods in user_goods_top.items():
        for goods_id in goods:
            if goods_id in exept_goods:
                continue
            if goods_id not in goods_number:
                goods_number.setdefault(goods_id, 0)
            goods_number[goods_id] += new_similar_dict[user]
    goods_number = sorted(goods_number.items(), key=itemgetter(1), reverse=True)[:5]
    new_goods_number = []
    for j in goods_number:
        new_goods_number.append(j[0])
    return new_goods_number


def sort_out(wacth_data, user_id):
    filename = 'hxy_user_data2.txt'
    user_goods = hxy_recomment.get_data(filename)
    goods_num = get_goods_num(user_goods)
    goods_num = get_user_similar(user_goods, goods_num)
    goods_num = get_similar_user(user_id, goods_num)
    goods_num2 = get_similar_goods(goods_num, user_goods, user_id)
    goods_info = {}
    for i in goods_num2:
        goods_info.setdefault(i, [])
        goods_info[i] = wacth_data[i]
    return goods_info


if __name__ == '__main__':
    user_id = 'user789'


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


    filename = 'hxy_wacth_info2.txt'
    wacth_data, base_data = data(filename)
    j = sort_out(wacth_data, user_id)
    print(j)
