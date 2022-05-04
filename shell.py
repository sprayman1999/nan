#!/bin/python3
# author: Juesheng Wang
# -*- coding: utf-8 -*-
import sys
import os
from lexer import Lexer
from parser import Parser
import subprocess
def usage():
    print("Usage: python3 shell.py <output_path> -o <source_path>")
def main():
    argv_length = len(sys.argv)
    
    if len(sys.argv) == 4 and '-o' == sys.argv[2]:
        output_path = sys.argv[3]
        source_path = sys.argv[1]
        filename = os.path.basename(source_path)
        source = ''
        with open(source_path,"r") as f:
            source = f.read()

        # 词法分析器
        lex = Lexer(source)
        tokens = lex.get_tokens()

        # 语法分析器检查
        parser = Parser()
        programmer_code = Parser.t2s(tokens)
        if parser.check(programmer_code) == False:
            print("存在语法错误")
            exit(-1)
        
        # 翻译代码
        lr_code = parser.get_lr(tokens)
        lr_headers = parser.get_ir_headers(filename)
        lr = lr_headers + lr_code
        output_lr = f"./{filename}.ll"
        with open(output_lr,"w") as f:
            f.write(lr)
        subprocess.call(['clang',output_lr,'-o',output_path],shell=False)
        
    else:
        usage()
		
if __name__ == '__main__':
	main()



