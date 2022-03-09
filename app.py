from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('mongodb+srv://test:sparta@Cluster0.d4msk.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')

@app.route('/card', methods=["POST"])
def card_post():
    title_receive = request.form['title_give']
    img_receive = request.form['img_give']
    link_receive = request.form['link_give']
    num_receive = request.form['num_give']

    doc = {
        'title': title_receive,
        'img': img_receive,
        'link': link_receive,
        'num': num_receive
    }

    db.cards.insert_one(doc)

    return jsonify({'msg': '저장완료'})

@app.route('/card', methods=["GET"])
def card_get():
    return jsonify({'msg': 'GET 연결 완료!'})

@app.route('/battle_create')
def battle_create():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': 'POST 연결 완료!'})

@app.route('/battle_zone')
def battle_zone():
    return render_template('battle_zone.html')

# API 역할을 하는 부분
@app.route('/api/select1', methods=['POST'])
def select_btn1():
    title_receive = request.form['title_give']
    target_title = db.battle.find_one({'title': title_receive})

    current_sel1 = target_title['sel_cnt1']
    new_sel1 = current_sel1+1

    db.battle.update_one({'title': title_receive}, {'$set': {'sel_cnt1': new_sel1}})
    return jsonify({'msg': '선택 완료'})

@app.route('/api/select2', methods=['POST'])
def select_btn2():
    title_receive = request.form['title_give']
    target_title = db.battle.find_one({'title': title_receive})

    current_sel2 = target_title['sel_cnt2']
    new_sel2 = current_sel2+1

    db.battle.update_one({'title': title_receive}, {'$set': {'sel_cnt2': new_sel2}})
    return jsonify({'msg': '선택 완료'})

@app.route('/reply', methods=['POST'])
def write_reply():
    Id_receive = request.form['Id_give']
    Password_receive = request.form['Password_give']
    Comment_receive = request.form['Comment_give']
    like_receive = request.form['like_give']

    doc = {
        'Id': Id_receive,
        'Password': Password_receive,
        'Comment': Comment_receive,
        'like': like_receive
    }

    db.reply.insert_one(doc)
    return jsonify({'msg': '댓글 저장 완료!'})

@app.route('/api/showbar', methods=['GET'])
def show_bar():
    bar = list(db.battle.find({'title': '깻잎 논쟁!'}, {'_id': False}))
    return jsonify({'show_bars': bar})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)