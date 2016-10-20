import tokenize
from collections import OrderedDict
from io import BytesIO

from coalib.results.SourcePosition import SourcePosition


class Tokenizer:
    def __init__(self, file, file_contents):
        self.file = file
        self.file_contents = file_contents
        self.tokenListWithPos = OrderedDict()
        self.tokenList = {}

    def FullTokenListWithPos(self):
        if not self.tokenListWithPos:
            linenum = 1
            for line in self.file_contents:
                tokens = tokenize.tokenize(
                    BytesIO(line.encode('utf-8')).readline)
                for toknum, tokval, startpos, _, _ in tokens:
                    if Tokenizer.ShouldAdd(toknum):
                        self.tokenListWithPos[
                            SourcePosition(self.file,
                                           linenum,
                                           startpos[1])] = (toknum, tokval)
                linenum += 1
        return self.tokenListWithPos

    def FullTokenList(self):
        if not self.tokenList:
            for line in self.file_contents:
                tokens = tokenize.tokenize(
                    BytesIO(line.strip().encode('utf-8')).readline)
                for toknum, tokval, _, _, _ in tokens:
                    if Tokenizer.ShouldAdd(toknum):
                        self.tokenList[toknum] = tokval
        return self.tokenList

    @staticmethod
    def TokensFromString(string):
        tokens = tokenize.tokenize(BytesIO(string.encode('utf-8')).readline)
        tokenDict = {}
        for toknum, tokval, _, _, _ in tokens:
            if Tokenizer.ShouldAdd(toknum):
                tokenDict[toknum] = tokval
        return tokenDict


    @staticmethod
    def ShouldAdd(toknum):
        DropTokens = [tokenize.INDENT,
                      tokenize.DEDENT,
                      tokenize.COMMENT,
                      tokenize.NEWLINE]
        if toknum in DropTokens:
            return False
        return True
