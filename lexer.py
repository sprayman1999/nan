# void int char byte list #不知道是否可以实现自动推导
# func return let is for while in foreach
# { } [ ] < > |
# + - * % & | = == += -= *= ^= ^|= (三元运算符)
# + - * / % 算术运算符
# ^ | & ^~ &~ |~ 位运算符
from common import *
from position.position import Position
DIGITS = "0123456789"
ARITHMETIC_OPERATORS = ["+","-","*","/","%","**","++","--"]
RELATIONAL_OPERATORS = [">","<","<=",">=","!=","=="]
LOGICAL_OPERATORS = ["&&","||","!","^~","|~","&~"]
BITWISE_OPERATORS = ['&',"|","^","~"]
ASSIGNMENT_OPERATORS = ["=","+=","-=","*=","%=","/=","&~=","^~=","|~=","^=","|=","&=","~=","<<=",">>="]
MISC_OPERATORS = ["?",":",",","."]
POSTFIX_OPERATORS = ["(",")","[","]"]
SHIFT_OPERATORS = ["<<",">>"]
OPERATORS = ARITHMETIC_OPERATORS + RELATIONAL_OPERATORS + LOGICAL_OPERATORS + BITWISE_OPERATORS + ASSIGNMENT_OPERATORS + MISC_OPERATORS + POSTFIX_OPERATORS + SHIFT_OPERATORS

BRACE = '{}'

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

KEYWORDS = ['if','while','foreach','else','func',"int","char","byte","long","float","auto","or","and","not","is","in","do","except",'const','string','import','package',"return","struct","class","asyn","as","sizeof","break","continue","static","switch","case","void"]

SINGLE_QUOTATION_MARK = "\'"
DOUBLE_QUOTATION_MARK = "\""
END_MARK = ";"


# TT: Token Type


TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_CHAR = "CHAR"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_SHIFT_OPERATORS = "SHIFT_OPERATORS"
TT_POSTFIX_OPERATORS = "POSTFIX_OPERATORS"
TT_MISC_OPERATORS = "MISC_OPERATORS"
TT_ASSIGNMENT_OPERATORS = "ASSIGNMENT_OPERATORS"
TT_BITWISE_OPERATORS = "BITWISE_OPERATORS"
TT_LOGICAL_OPERATORS = "LOGICAL_OPERATORS"
TT_RELATIONAL_OPERATORS = "RELATIONAL_OPERATORS"
TT_ARITHMETIC_OPERATORS = "ARITHMETIC_OPERATORS"
TT_LEFT_BRACE = "LEFT_BRACE"
TT_RIGHT_BRACE = "RIGHT_BRACE"
TT_END_MARK = "END_MARK"



class Token(object):
    def __init__(self,type,value):
        self.type = type
        self.value = value
    def __str__(self):
        return f"<{self.type},{self.value}>"
        
class Lexer(object):
    def __init__(self,text):
        self.text = text
        self.pos = Position(-1,0,-1,text)
        self.current_char = None
        self.tokens = self.__make_tokens()
    def next(self):
        self.pos.next(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None
    def get_tokens(self):
        return self.tokens
    def __make_tokens(self):
        tokens = []
        self.next()
        while self.current_char != None:
            if self.current_char in (' ','\t',"\n","\r"):
                self.next()
            elif self.current_char in BRACE:
                tokens.append(self.get_brace())
            elif self.current_char in DIGITS:
                tokens.append(self.get_number())
            elif self.current_char in OPERATORS:
                tokens.append(self.get_operator())
            elif self.current_char in ALPHABET:
                word = self.get_word()
                if word in KEYWORDS:
                    tokens.append(self.get_keyword(word))
                else:
                    tokens.append(self.get_identifier(word))
            elif self.current_char in SINGLE_QUOTATION_MARK:
                tokens.append(self.get_char())
            elif self.current_char in DOUBLE_QUOTATION_MARK:
                tokens.append(self.get_string())
            elif self.current_char in END_MARK:
                tokens.append(self.get_end_mark())
            else:
                print(f"{str(self.pos)} IllegalChar Error!")
                exit(-1)
        return tokens
        
        
    def get_char(self):
        char_str = self.current_char
        self.next()
        while self.current_char != None and self.current_char != SINGLE_QUOTATION_MARK:
            char_str += self.current_char
            self.next()
        if self.current_char == None:
            self.error("wrong \"char\" type.[0]")
        char_str += SINGLE_QUOTATION_MARK
        self.next()
        if is_hex_char(char_str[1:-1]) == True or len(char_str) == 3: #去除头尾的单引号
            return Token(TT_CHAR,char_str)
        else:
            self.error("wrong \"char\" type.[1]")
        
    def get_string(self):
        string_str = self.current_char
        self.next()
        while self.current_char != None and self.current_char != DOUBLE_QUOTATION_MARK:
            string_str += self.current_char
            self.next()
        if self.current_char == None:
            self.error("wrong \"string\" type.[0]")
        string_str += DOUBLE_QUOTATION_MARK
        self.next()
        return Token(TT_STRING,string_str)

    def get_end_mark(self):
        self.next()
        return Token(TT_END_MARK,END_MARK)
        

    def get_word(self):
        word = ''
        while self.current_char != None and self.current_char in (ALPHABET + DIGITS + "_"):
            word += self.current_char
            self.next()
        return word
    
    def get_identifier(self,word):
        return Token(TT_IDENTIFIER,word)

    def get_keyword(self,word):
        
        return Token(TT_KEYWORD,word)
    def error(self,text):
        if self.current_char != None:
            print("<{self.pos.line},{self.pos.col}>\"{self.current_char}\" Something cause a error. {text}");
        else:
            print("<{self.pos.line},{self.pos.col}> Something cause a error. {text}");
        exit(-1)

    def get_brace(self):
        if self.current_char == "{":
            self.next()
            return Token(TT_LEFT_BRACE,"{")
        elif self.current_char == "}":
            self.next()
            return Token(TT_RIGHT_BRACE,"}")
        
    def get_operator(self):
        operator_str = ''
        token_type = ''
        token = None
        if self.current_char in POSTFIX_OPERATORS:
            operator_str += self.current_char
            self.next()
        else:
            while self.current_char != None and self.current_char not in (ALPHABET + DIGITS + "_" + " \n\r\t" + "{}"):
                operator_str += self.current_char
                self.next()
        if operator_str not in OPERATORS:
            self.error("The operator is not found.")
        token_type = self.get_operator_token_type(operator_str)
        return Token(token_type,operator_str)

    def get_operator_token_type(self,operator_str):
        if operator_str in ARITHMETIC_OPERATORS:
            return TT_ARITHMETIC_OPERATORS
        elif operator_str in RELATIONAL_OPERATORS:
            return TT_RELATIONAL_OPERATORS
        elif operator_str in LOGICAL_OPERATORS:
            return TT_LOGICAL_OPERATORS
        elif operator_str in BITWISE_OPERATORS:
            return TT_BITWISE_OPERATORS
        elif operator_str in ASSIGNMENT_OPERATORS:
            return TT_ASSIGNMENT_OPERATORS
        elif operator_str in MISC_OPERATORS:
            return TT_MISC_OPERATORS
        elif operator_str in POSTFIX_OPERATORS:
            return TT_POSTFIX_OPERATORS
        elif operator_str in SHIFT_OPERATORS:
            return TT_SHIFT_OPERATORS

    def get_number(self):
        '''
        小数 整数
        '''
        num_str = ''
        dot_count = 0 # 小数点的个数
        while self.current_char != None and self.current_char in (DIGITS + '.' + "_"):
            if self.current_char == '.':
                if dot_count >= 1:
                    break
                else:
                    dot_count += 1
                    num_str += self.current_char
            else:
                num_str += self.current_char
            self.next()
        if dot_count == 0:
            return Token(TT_INT,num_str.replace("_",""))
        else:
            return Token(TT_INT,num_str.replace("_",""))

    def __str__(self):
        str = ''
        for item in self.tokens:
            str += f"<{item.type},{item.value}>\n"
        return str
def main():
    source = '''
func main(): void{
    printf("Hello Nan!");
}
    '''.strip()
    lex = Lexer(source)
    tokens = lex.get_tokens()
    print(lex)
if __name__ == "__main__":
    main()





