class Position(object):
    def __init__(self,idx,line,col,text):
        '''
        idx: 索引
        line: 行号
        col: 列号
        text: 文本内容
        '''
        self.idx = idx
        self.line = line
        self.col = col
        self.text = text
        self.prev_line_length = 0

    def next(self,current_char):
        self.idx += 1
        if current_char == '\n' or current_char == '\r':
            self.pre_line_length = self.col
            self.col = 0
            self.line += 1
        else:
            self.col += 1

    def back(self):
        self.idx -= 1
        if self.col <= 0:
            self.line -= 1
            self.col = self.pre_line_length
        else:
            self.col -= 1

    def __str__(self):
        return f"({self.line},{self.col})"
