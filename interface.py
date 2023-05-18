from PyQt5.QtGui import QIcon, QColor, QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, \
    QTextEdit
from PyQt5.QtCore import Qt
from search import search_documents


class SearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置窗口的标题、图标和大小
        self.setWindowTitle('信息检索系统')
        self.setWindowIcon(QIcon('search_icon.png'))
        self.setMinimumSize(1000, 700)

        # 设置搜索框和搜索按钮
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText('输入关键词')
        self.search_edit.setStyleSheet(
            'QLineEdit {color: black; border: 2px solid #7EBF5E; border-radius: 50px; padding-left: 30px; '
            'padding-right: 30px; font-size: 24px; height: 60px;}')

        self.search_btn = QPushButton('搜索')
        self.search_btn.setStyleSheet(
            'QPushButton {background-color: #7EBF5E; color: white; font-size: 28px; font-weight: bold; border: 2px '
            'solid #7EBF5E; border-radius: 50px; padding-left: 30px; padding-right: 30px; height: 60px;} '
            'QPushButton:hover {background-color: white; color: #7EBF5E; border: 2px solid #7EBF5E;}')
        self.search_btn.clicked.connect(self.search)

        # 设置搜索框和搜索按钮所在的水平盒子布局
        self.search_hbox = QHBoxLayout()
        self.search_hbox.addStretch(1)
        self.search_hbox.addWidget(self.search_edit)
        self.search_hbox.addWidget(self.search_btn)
        self.search_hbox.addStretch(1)

        # 设置搜索结果框
        self.result_text = QTextEdit()
        self.result_text.setTextColor(QColor('#383838'))
        self.result_text.setReadOnly(True)
        self.result_text.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.result_text.setPlaceholderText('暂无搜索结果')
        self.result_text.setStyleSheet(
            'QTextEdit {color: #383838; background-color: white; border: 2px solid #7EBF5E; border-radius: 10px; '
            'padding: 20px; font-size: 20px;}')

        # 将搜索框和搜索结果框添加到垂直盒子布局中
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.search_hbox)
        self.vbox.addWidget(self.result_text)

        # 设置容器窗口，将垂直盒子布局添加到容器窗口上
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.vbox)
        self.setCentralWidget(self.main_widget)

    def search(self):
        query = self.search_edit.text()  # 获取查询词

        # 执行检索
        results = search_documents(query)

        if len(results) > 0:
            # 显示检索结果
            self.result_text.clear()
            self.result_text.setTextColor(QColor('#383838'))
            self.result_text.setFontWeight(75)
            self.result_text.setFontPointSize(14)
            self.result_text.insertPlainText('搜索结果：\n\n')
            i = 0
            for result in results:
                i = i + 1
                self.result_text.setTextColor(QColor('#7EBF5E'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(75)
                self.result_text.setFontPointSize(14)
                self.result_text.insertPlainText('{}\n'.format(str(i) + ":"))

                self.result_text.setTextColor(QColor('#7EBF5E'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('[Title]: ')
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(75)
                self.result_text.setFontPointSize(14)
                self.result_text.insertPlainText('{}\n'.format(result['title']))

                self.result_text.setTextColor(QColor('#7EBF5E'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('[Summary]: ')
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('{}\n'.format(result['summary']))

                self.result_text.setTextColor(QColor('#7EBF5E'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('[URL]: ')
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(75)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('{}\n'.format(result['url']))
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)

                self.result_text.setTextColor(QColor('#7EBF5E'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('[Score]: ')
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(75)
                self.result_text.setFontPointSize(12)
                self.result_text.insertPlainText('{}\n\n'.format(result['score']))
                self.result_text.setTextColor(QColor('#383838'))
                self.result_text.setFontWeight(50)
                self.result_text.setFontPointSize(12)
                title = result['title']
                summary = result['summary']
        else:
            # 显示检索结果
            self.result_text.clear()
            self.result_text.setTextColor(QColor('#383838'))
            self.result_text.setFontWeight(75)
            self.result_text.setFontPointSize(14)
            self.result_text.insertPlainText('无搜索结果')


if __name__ == '__main__':
    app = QApplication([])
    search_window = SearchWindow()
    search_window.show()
    app.exec_()
