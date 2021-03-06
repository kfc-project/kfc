import os
from bson import ObjectId
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from datetime import datetime

UPLOAD_FOLDER = './static'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jepg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

client = MongoClient('mongodb+srv://test:sparta@Cluster0.d4msk.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')


@app.route('/battle_create')
def battle_create():
    return render_template('battle_create.html')


@app.route('/battle_zone')
def battle_zone():
    return render_template('battle_zone.html')


# 'battle_zone.html' 관련 코드
# 왼쪽 '선택' 버튼을 눌렀을 시 작동
@app.route('/api/select1', methods=['POST'])
def select_btn1():
    id = request.form['id']
    battle = db.battle.find_one({'_id': ObjectId(id)})

    current_sel1 = battle['sel_cnt1']
    new_sel1 = current_sel1 + 1

    db.battle.update_one({'_id': ObjectId(id)}, {'$set': {'sel_cnt1': new_sel1}})
    return jsonify({'msg': '선택 완료'})


# 오른쪽 '선택' 버튼을 눌렀을 시 작동
@app.route('/api/select2', methods=['POST'])
def select_btn2():
    id = request.form['id']
    battle = db.battle.find_one({'_id': ObjectId(id)})

    current_sel2 = battle['sel_cnt2']
    new_sel2 = current_sel2 + 1

    db.battle.update_one({'_id': ObjectId(id)}, {'$set': {'sel_cnt2': new_sel2}})
    return jsonify({'msg': '선택 완료'})


# Progress Bar 표출
@app.route('/api/showbar', methods=['GET'])
def show_bar():
    id = request.args.get('id')
    bar = db.battle.find_one({'_id': ObjectId(id)}, {'_id': False})
    return jsonify({'show_bars': bar})


# 댓글 DB 보내기
@app.route('/reply', methods=['POST'])
def write_reply():
    Id_receive = request.form['Id_give']
    Password_receive = request.form['Password_give']
    Comment_receive = request.form['Comment_give']
    Check_receive = request.form['Check_give']
    time_receive = datetime.now()
    battleId = request.form['battleId']

    doc = {
        'Id': Id_receive,
        'Password': Password_receive,
        'Comment': Comment_receive,
        'like': 0,
        'Check': Check_receive,
        'time': time_receive,
        'battleId': battleId
    }
    db.reply.insert_one(doc)

    return jsonify({'msg': '댓글 저장 완료!'})

# 배틀 타이틀 가져오기
@app.route('/api/server_create', methods=['GET'])
def show_battles():
    id = request.args.get('id')
    battles = db.battle.find_one({'_id': ObjectId(id)})
    battles['_id'] = str(battles['_id'])
    return jsonify({'show_battles': battles})

# 댓글 DB 가져오기
@app.route('/reply', methods=['GET'])
def read_replies():
    id = request.args.get('id')
    replies = objectIdDecoder(list(db.reply.find({'battleId': id}).sort('like', -1)))
    return jsonify({'all_replies': replies})


# 댓글 삭제하기
@app.route('/api/delete', methods=['POST'])
def delete_reply():
    _id_receive = request.form['_id_give']
    db.reply.delete_one({'_id': ObjectId(_id_receive)})
    return jsonify({'msg': '삭제 완료!'})


# 좋아요 수 늘리기
@app.route('/api/like', methods=['POST'])
def like_comment():
    Id_receive = request.form['Id_give']

    target_id = db.reply.find_one({'Id': Id_receive})
    current_like = target_id['like']

    new_like = current_like + 1

    db.reply.update_one({'Id': Id_receive}, {'$set': {'like': new_like}})

    return jsonify({'msg': '좋아요 완료!'})


# object 값을 str로 바꾸기
def objectIdDecoder(list):
    results = []
    for document in list:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results


# 'main.html' 관련 코드
# main 토론장
@app.route('/api/sub_create', methods=['GET'])
def card_get():
    card_list = object_string(list(db.battle.find({})))
    return jsonify({'cards': card_list})

# 토론장 삭제하기
@app.route('/api/sub_delete', methods=['POST'])
def delete_card():
    id_receive = request.form['id_give']
    db.battle.delete_one({'_id': ObjectId(id_receive)})
    return jsonify({'msg': '주제가 삭제되었습니다.'})


# 'battle_create.html' 관련 코드
# 토론장 생성하기
@app.route('/api/sub_create', methods=['POST'])
def sub_create():
    title_receive = request.form['title_give']
    sub1_receive = request.form['sub1_give']
    sub2_receive = request.form['sub2_give']
    name_receive = request.form['name_give']
    pw_receive = request.form['pw_give']

    file_len = len(request.files)
    # file_len 이 0이면 JS에서 파일을 안보낸준 것!
    # 파일을 안보내줬으면 default 파일이름을 넘겨준다.
    if file_len == 0:
        full_file_name = 'default_img_220315.jpg'  # default 파일이름 설정
    else:
        # 파일을 제대로 전달해줬으면 파일을 꺼내서 저장하고 파일이름을 넘겨준다.
        img_receive = request.files['img_give']

        extension = img_receive.filename.split('.')[-1]

        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        filename = f'challenge-file-{mytime}'
        # save_to = f'static/assets/img/challenge/{filename}.{extension}'
        # image_receive.save(save_to)
        full_file_name = f'{filename}.{extension}'

        # 토론장 이미지 업로드 하기
        path = os.path.join(app.config['UPLOAD_FOLDER'], full_file_name)
        img_receive.save(path)

    doc = {
        'title': title_receive,
        'subject1': sub1_receive,
        'subject2': sub2_receive,
        'name': name_receive,
        'password': pw_receive,
        'img_src': full_file_name,
        'sel_cnt1': 0,
        'sel_cnt2': 0,
        'total_cnt': 0
    }
    db.battle.insert_one(doc)

    return jsonify({'msg': '생성되었습니다.'})


# 조회수 카운트하기
@app.route('/cnt_view', methods=['POST'])
def view_cnt():
    id_receive = request.form['id_give']
    target_id = db.battle.find_one({'_id': ObjectId(id_receive)})

    current_cnt = target_id['total_cnt']
    new_cnt = current_cnt + 1

    db.battle.update_one({'_id': ObjectId(id_receive)}, {'$set': {'total_cnt': new_cnt}})
    return jsonify({'msg': '토론장으로 이동해볼까요?'})


# object 값을 str로 바꾸기
def object_string(list):
    results = []
    for document in list:
        document['_id'] = str(document['_id'])
        results.append(document)
    return results


# 실행코드
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)