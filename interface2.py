import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from search import search_documents
from search import search_unigram
from search import search_bigram

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口大小和标题
        self.result_text = None
        self.setWindowTitle('My Search Engine')
        self.setMinimumSize(800, 600)

        # 创建三个搜索框，和对应的搜索结果文本框
        self.search_box1 = QLineEdit()
        self.search_btn1 = QPushButton('Search')
        self.result_text1 = QTextEdit()
        self.result_text1.setReadOnly(True)

        self.search_box2 = QLineEdit()
        self.search_btn2 = QPushButton('Search')
        self.result_text2 = QTextEdit()
        self.result_text2.setReadOnly(True)

        self.search_box3 = QLineEdit()
        self.search_btn3 = QPushButton('Search')
        self.result_text3 = QTextEdit()
        self.result_text3.setReadOnly(True)

        # 设置搜索按钮的点击事件
        self.search_btn1.clicked.connect(lambda: self.search1())
        self.search_btn2.clicked.connect(lambda: self.search2())
        self.search_btn3.clicked.connect(lambda: self.search3())

        # 创建一个垂直布局，用于容纳搜索框和搜索结果文本框
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.search_box1)
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.search_btn1)
        hbox1.addStretch()
        vbox1.addLayout(hbox1)
        vbox1.addWidget(self.result_text1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.search_box2)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.search_btn2)
        hbox2.addStretch()
        vbox2.addLayout(hbox2)
        vbox2.addWidget(self.result_text2)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.search_box3)
        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.search_btn3)
        hbox3.addStretch()
        vbox3.addLayout(hbox3)
        vbox3.addWidget(self.result_text3)

        # 创建一个水平布局，用于容纳三个垂直布局
        hbox = QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)
        hbox.addLayout(vbox3)

        # 设置布局间距和控件间距
        vbox1.setSpacing(10)
        vbox2.setSpacing(10)
        vbox3.setSpacing(10)
        hbox.setSpacing(20)
        hbox.setContentsMargins(40, 40, 40, 40)

        self.setLayout(hbox)

        # 设置搜索框的样式
        self.search_box1.setObjectName('search_box')
        self.search_box2.setObjectName('search_box')
        self.search_box3.setObjectName('search_box')

        # 设置搜索按钮的样式
        self.search_btn1.setObjectName('search_btn')
        self.search_btn2.setObjectName('search_btn')
        self.search_btn3.setObjectName('search_btn')

        # 设置搜索结果文本框的样式
        self.result_text1.setObjectName('result_text')
        self.result_text2.setObjectName('result_text')
        self.result_text3.setObjectName('result_text')

        # 设置整个窗口的样式
        self.setStyleSheet('''
            QLineEdit#search_box {
                border-radius: 10px;
                border: 2px solid #ccc;
                height: 35px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding-left: 10px;
            }
            QPushButton#search_btn {
                border-radius: 10px;
                background-color: #0099ff;
                color: #fff;
                font-weight: bold;
                font-size: 14px;
                height: 35px;
                width: 70px;
            }
            QTextEdit#result_text {
                border-radius: 10px;
                border: 2px solid #ccc;
                font-family: Arial, sans-serif;
                font-size: 14px;
                padding: 10px;
                background-color: #f5f5f5;
            }
        ''')

    # 搜索函数
    def search(self, result_text, results):

        # results = [
        #     {
        #         'title': 'Python Programming Language - Official Website',
        #         'summary': 'The official home of the Python Programming Language.',
        #         'url': 'https://www.python.org/',
        #         'score': 9.5
        #     },
        #     {
        #         'title': 'Python Programming Language - Official Website',
        #         'summary': 'The official home of the Python Programming Language.',
        #         'url': 'https://www.python.org/',
        #         'score': 9.5
        #     }
        # ]

        # 将之前的内容清除
        result_text.clear()
        if len(results) > 0:
            result_text.insertPlainText('搜索结果：\n\n')
            # 显示搜索结果
            for i, result in enumerate(results):
                if i == 10:  # 遍历前十个元素即可
                    break
                result_text.insertPlainText('{}\n'.format(str(i + 1) + ":"))
                result_text.insertPlainText('[Title]: ')
                result_text.insertPlainText('{}\n'.format(result['title']))
                result_text.insertPlainText('[Summary]: ')
                result_text.insertPlainText('{}\n'.format(result['summary']))
                result_text.insertPlainText('[URL]: ')
                result_text.insertPlainText('{}\n'.format(result['url']))
                result_text.insertPlainText('[Score]: ')
                result_text.insertPlainText('{}\n\n'.format(result['score']))
        else:
            result_text.insertPlainText('无搜索结果')

    # 三个不同的搜索函数
    def search1(self):
        results = search_documents(self.search_box1.text())
        self.search(self.result_text1, results)

    def search2(self):
        results = search_unigram(self.search_box2.text())
        self.search(self.result_text2, results)

    def search3(self):
        results = search_bigram(self.search_box3.text())
        self.search(self.result_text3, results)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
