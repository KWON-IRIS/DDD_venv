import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

# 플라스크 웹 서버 생성하기
from pymongo import MongoClient

app = Flask(__name__)

# mongodb 추가
client = MongoClient('localhost', 27017)
db = client.get_database('sparta')


# api 추가
# {{렌더링 영역}} : flask 문법
@app.route('/', methods=['GET'])  # 데코레이터 문법
def index():  # 함수이름은 고유해야함
    memos = list(db.articles.find({},{'_id':False}))
    return render_template('index.html', test='테스트', memos = memos)


# 아티클 추가 api
# 프론트에서 받아줄 루트 설정 필요! >> index의 memo 에서 불러옴.

@app.route('/memo', methods=['POST'])
def save_memo():
    # alt+enter > flask.request 추가
    form = request.form
    url_receive = form['url_give']
    comment_receive = form['comment_give']

    # print(url_receive, comment_receive)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    response = requests.get(
        url_receive,
        headers=headers
    )
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')
    url = soup.select_one('meta[property="og:url"]')
    description = soup.select_one('meta[property="og:description"]')
    img = soup.select_one('meta[property="og:image"]')

    print(title['content'])

    document = {
        'title': title['content'],
        'image': img['content'],
        'url': url['content'],
        'description': description['content'],
        'comment': comment_receive,
    }
    db.articles.insert_one(document)

    return jsonify(
        {'result': 'success', 'msg': '잘 저장되었습니다'}
    )


@app.route('/memo', methods=['GET'])
def list_memo():
    memos = list(db.articles.find({}, {'_id': False}))
    result = {
        'result': 'success',
        'articles': memos,
    }
    return jsonify(result)


# app.py 파일을 직접 실행시킬떄 동작시킴
# 항상 가장 아래 있어야함
# localhost: 7000 >> 브라우저 내에서 수정해야함.
if __name__ == '__main__':
    app.run(
        '0.0.0.0',  # 모든 IP에서 오는 요청을 허용
        7000,  # 플라스크 웹 서버는 7000번 포트 사용
        debug=True  # 에러 발생 시 에러 로그 보여줌
    )
