from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/test')
def battle_create():
    return render_template('test.html')

@app.route('/battle_zone')
def battle_zone():
    return render_template('battle_zone.html')

# 왼쪽 '선택' 버튼을 눌렀을 시 작동
@app.route('/api/select1', methods=['POST'])
def select_btn1():
    title_receive = request.form['title_give']
    target_title = db.battle.find_one({'title': title_receive})

    current_sel1 = target_title['sel_cnt1']
    new_sel1 = current_sel1+1

    db.battle.update_one({'title': title_receive}, {'$set': {'sel_cnt1': new_sel1}})
    return jsonify({'msg': '선택 완료'})

# 오른쪽 '선택' 버튼을 눌렀을 시 작동
@app.route('/api/select2', methods=['POST'])
def select_btn2():
    title_receive = request.form['title_give']
    target_title = db.battle.find_one({'title': title_receive})

    current_sel2 = target_title['sel_cnt2']
    new_sel2 = current_sel2+1

    db.battle.update_one({'title': title_receive}, {'$set': {'sel_cnt2': new_sel2}})
    return jsonify({'msg': '선택 완료'})

# Progress Bar 표출
@app.route('/api/showbar', methods=['GET'])
def show_bar():
    bar = list(db.battle.find({'title': '깻잎 논쟁!'}, {'_id': False}))
    return jsonify({'show_bars': bar})

# 토론장 생성하기
@app.route('/api/sub_create', methods=['POST'])
def sub_create():
    title_receive = request.form['title_give']
    sub1_receive = request.form['sub1_give']
    sub2_receive = request.form['sub2_give']
    img_receive = request.form['img_give']

    target_title = db.battle.find_one({'title': title_receive})

    current_seq = target_title['seq'];
    new_seq = current_seq +1;

    doc = {
        'title': title_receive,
        'subject1': sub1_receive,
        'subject2': sub2_receive,
        'img_src': img_receive,
        'seq': new_seq
    }
    db.battle.insert_one(doc)

    return jsonify({'msg': '생성되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)