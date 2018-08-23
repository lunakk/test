import random

with open('hxy_user_data2.txt', 'w', encoding='utf-8') as f:
    user_data = {}
    for i in range(50000):
        user_id = random.randint(1, 5000)
        goods_id = random.randint(0, 1000)
        score = random.randint(1, 5)
        string = 'user' + str(user_id) + '\t' + str(goods_id)
        if string not in user_data:
            user_data.setdefault(string, -1)
            user_data[string] = score
    for key, value in user_data.items():
        f.write(key + '\t' + str(value) + '\n')
