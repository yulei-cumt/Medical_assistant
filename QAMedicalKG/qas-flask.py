from flask import Flask
from flask import request
from flask_cors import *
from gevent import pywsgi
# import pymysql
import json
# from chatbot_graph import *

from question_classifier import *
from question_parser import *
from answer_search import *


app = Flask(__name__)
CORS(app, supports_credentials=True)


'''问答类'''
class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_main(self, sent):
        answer = '很抱歉没能理解您的问题，我的数据量有限，您可以换一种问法再次尝试。'
        res_classify = self.classifier.classify(sent)
        if not res_classify:
            return answer
        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
            return answer
        else:
            return '\n'.join(final_answers)


@app.route('/ask', methods=["get", "post"])
def search():
    the_question = request.values.get('the_question')
    # 将问题写入test文件中，方便模型调用
    filename = './intentions/THUCNews/data/test.txt'
    with open(filename, 'w', encoding='utf8') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        for i in range(256):
            f.write(the_question+' 0'+"\n")
        f.write(the_question+' 0')
    f.close()
    answer = handler.chat_main(the_question)
    print('客服机器人:', answer)

    data = {}
    data['code'] = 0
    data['msg'] = '成功'
    data['answer'] = answer
    jsonStr = json.dumps(data)
    # print(jsonStr)
    return jsonStr
    # return 'success'


if __name__ == "__main__":
    handler = ChatBotGraph()
    app.run()
    #server = pywsgi.WSGIServer(('0.0.0.0', 12345), app)
    #server.serve_forever()
