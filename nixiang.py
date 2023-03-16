class rightMax(object):
    def __init__(self, dict_path):
        self.dictionary = set()  # 定义字典
        self.maximum = 0  # 最大匹配长度

        with open(dict_path, 'r', encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                self.dictionary.add(line)
                if len(line) > self.maximum:
                    self.maximum = len(line)

    def cut(self, text):
        result = []
        index = len(text)
        while index > 0:
            word = None
            for size in range(self.maximum, 0, -1):
                if index - size < 0:
                    continue
                piece = text[(index - size):index]
                if piece in self.dictionary:
                    word = piece
                    result.append(word)
                    index -= size
                    break
            if word is None:
                result.append(text[(index - 1):index])
                index -= 1
        return result[::-1]  # 由于append为添加至末尾，故需反向打印


def main():
    text = "南京省长江大桥"
    tokenizer = rightMax('ChineseDic.txt')
    print(tokenizer.cut(text))


#main()

