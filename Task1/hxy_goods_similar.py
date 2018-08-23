"""1.拿到所有商品的信息，分为标准集和推荐集
		标准集：你这一页显示的商品（30个）
		推荐集：剩下的所有商品
	2.拿到标准集48个手表的共同重要程度top10的词A
	3.拿到推荐集的每一本书的top5重要程度的词B
	4.对每一个手表计算（A∩B）/（A∪B）
	5.倒排取top10的手表进行推荐
	最后结果依然是一个列表，包含被推荐手表的编号

	初始数据：txt文本，每一行表示一个商品的具体信息
	    编号，名字，作者，。。。
	    by xiaoyan huang"""
import jieba.analyse
from operator import itemgetter


# 1.读到所有的数据，分为标准集和推荐集
# 标准集：你这一页显示的商品（30个）
# 推荐集：剩下的所有商品


def get_data(goods_info_filename):
    goods_info = {}
    base_set = {}
    other_set = {}
    with open(goods_info_filename, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip('\n')
            info_list = line.split('\t')
            index = info_list.pop(0)
            # 剩下的就是手表信息列表
            goods_info.setdefault(index, [])
            goods_info[index] = info_list


    i = 0
    for index, info_list in goods_info.items():
        if i < 48:
            base_set.setdefault(index, [])
            base_set[index] = info_list
        else:
            other_set.setdefault(index, [])
            other_set[index] = info_list
        i += 1

    return base_set, other_set


# 2.拿到标准集48个手表的共同重要程度top10的词A
def get_base_words(base_set):
    base_words = []
    string = ''
    for index, info_list in base_set.items():
        name = info_list[1]
        # 拿到了所有有用信息组成的字符串
        string = string + name
    # 通过TF-IDF来表征重要程度，倒排取top10的词
    base_words = jieba.analyse.extract_tags(string, topK=10)
    return base_words


# 3.拿到推荐集的每一本书的top5重要程度的词B
def get_other_each_book_words(other_set):
    # {'124':['机器学习','深度学习','强化学习','自主学习','好好学习'],'125':[......]}
    other_words = {}
    for index, info_list in other_set.items():
        other_words.setdefault(index, [])
        other_words[index] = jieba.analyse.extract_tags(info_list[1], topK=5)
    return other_words


# 4.对每一本书计算（A∩B）/（A∪B）
# 5.倒排取top10的书进行推荐
# len(set([]) & set([])) / len(set([]) | set([]))
def get_wacth_info(base_words, other_words):
    top_ten = {}
    for key, value in other_words.items():
        top_ten.setdefault(key, 0)
        top_ten[key] = len(set(base_words) & set(value)) / len(set(base_words) | set(value))
    sorted_top = sorted(top_ten.items(), key=itemgetter(1), reverse=True)[:10]
    return sorted_top


def sort_out_similar(goods_info_filename, wacth_data):
    base_set, other_set = get_data(goods_info_filename)
    base_words = get_base_words(base_set)
    other_words = get_other_each_book_words(other_set)
    sorted_top = get_wacth_info(base_words, other_words)
    sorted_wacth = {}
    for i in sorted_top:
        sorted_wacth.setdefault(i[0])
        sorted_wacth[i[0]] = wacth_data[i[0]]
    return sorted_wacth


if __name__ == '__main__':

    # base_set = {'55': ['https://images-cn.ssl-images-amazon.com/images/I/41MCGlFt9lL._SL260_SX200_CR0,0,200,260_.jpg',
    #                    'Daniel Wellington 丹尼尔•惠灵顿 时尚女士手表 腕表 女表 皮质表带 石英手表 0508DW 不同批次包装盒随机发送（瑞典品牌）', '￥879.00', '4.3 星'],
    #             '269': ['https://images-cn.ssl-images-amazon.com/images/I/61wi4NDkU9L._SL200_CR0,0,200,260_.jpg',
    #                     'Tamlee 时尚皮革 男士 多功能数字 手表 运动腕表 Black', '￥191.88', '5 星'],
    #             '520': ['https://images-cn.ssl-images-amazon.com/images/I/51LMTtjphzL._SL200_CR0,0,200,260_.jpg',
    #                     '男式手表奢华 TOURBILLON 手表皮革表带自缠绕机械自动腕表', '￥250.71', '暂无评分'],
    #             '738': ['https://images-cn.ssl-images-amazon.com/images/I/51a16wpxPFL._SL260_SX200_CR0,0,200,260_.jpg',
    #                     '【此表太火了！不抢后悔！手慢无！】agelocer 艾戈勒 瑞士品牌 原装进口 Budapest布达佩斯系列 原装全自动机械商务男表正品手表男皮带时尚防水机械腕表 男士腕表 机械手表 男表 男士手表 (型号：4101A1)',
    #                     '￥3,380.00', '5 星'],
    #             '798': ['https://images-cn.ssl-images-amazon.com/images/I/31X+CeACeDL._SL200_CR0,0,200,260_.jpg',
    #                     '丹尼尔惠灵顿 (DanielWellington) 手表DW女表32mm白盘白皮带女士手表 瑞典品牌 专柜同款 热销爆款 (银色边白盘白色表带)', '￥699.00', '5 星'],
    #             '940': ['https://images-cn.ssl-images-amazon.com/images/I/41d51x6WmrL._SL260_SX200_CR0,0,200,260_.jpg',
    #                     'agelocer 艾戈勒 瑞士品牌 原装正品女士机械手表 琉森系列 超薄机械表 女士表全自动机械表 皮带防水 女士手表时尚简约机械腕表 女士腕表 女士机械表 休闲女士机械手表 (1202A1)',
    #                     '￥2,280.00', '暂无评分'],
    #             '50': ['https://images-cn.ssl-images-amazon.com/images/I/51yPrzByD6L._SL200_CR0,0,200,260_.jpg',
    #                    'Daniel Wellington 丹尼尔惠灵顿 瑞典品牌 石英男士手表 DW00100258', '￥799.00', '5 星'],
    #             '57': ['https://images-cn.ssl-images-amazon.com/images/I/41fd0NWNXcL._SL260_SX200_CR0,0,200,260_.jpg',
    #                    'Daniel Wellington 丹尼尔•惠灵顿 瑞典品牌 Classic系列 石英女士手表 腕表女表 石英女表 0507DW 不同批次包装盒随机发送（瑞典品牌 ）', '￥879.00',
    #                    '4.3 星'],
    #             '63': ['https://images-cn.ssl-images-amazon.com/images/I/4116MOEQb9L._SL200_CR0,0,200,260_.jpg',
    #                    'Daniel Wellington 丹尼尔惠灵顿 瑞典品牌 石英女士手表 DW00100219', '￥699.00', '4.8 星'],
    #             '68': ['https://images-cn.ssl-images-amazon.com/images/I/517t6BvI-BL._SL200_CR0,0,200,260_.jpg',
    #                    'IBSO 男式创意旋转手表 隐藏式表头 石英腕表 运动防水手表', '￥250.71', '3.8 星']}


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
    goods_info_filename = 'wacth_info2.txt'
    base_set1, other_set, stop_words = get_data(goods_info_filename)
    base_words = get_base_words(base_set1)
    other_words = get_other_each_book_words(other_set)
    sorted_top = get_wacth_info(base_words, other_words)
    sorted_wacth = sort_out_similar(goods_info_filename, stop_words_filename)
    print(base_words)
    print(other_words)
    print(sorted_top)
    print(sorted_wacth)
