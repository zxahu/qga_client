import re


class MatrixFilter:

    instance = None

    def __init__(self, reg):
        self.instance = re.compile(reg)

    def do(self, content, group=1):

        return self.instance.search(content).group(group)


class ColumnMatrixFilter(MatrixFilter):

    def __init__(self, option, column=1):

        reg = r'%s\W+' % option
        for i in range(1, column):
            reg += r'\w+\W+'
        reg += r'(\w+)'
        MatrixFilter.__init__(self, reg)
