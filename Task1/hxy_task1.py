import hxy_recomment
import hxy_user_similar
import hxy_goods_similar
from flask import Flask
from flask import render_template

app = Flask(__name__)


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


# filename = 'wacth_info.txt'
# wacth_data, base_data = data(filename)

filename1 = 'hxy_wacth_info2.txt'
wacth_data1, base_data1 = data(filename1)
user_id = 'user45'
gest_like = hxy_user_similar.sort_out(wacth_data1, user_id)

sorted_wacth_similar = hxy_goods_similar.sort_out_similar(filename1, wacth_data1)


@app.route("/wacth/")
def hello():
    return render_template('hxy_task1.html', wacth_data_html=base_data1, gest_like_html=gest_like,
                           similar_wacthes=sorted_wacth_similar)


@app.route("/wacth/<index>")
def hello_aaa(index):
    recomment_data = hxy_recomment.sortout(index, wacth_data1)
    return render_template('hxy_task2.html', r=recomment_data, i=wacth_data1[index])
