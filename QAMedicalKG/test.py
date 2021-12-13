# coding: UTF-8
from callModel import callModelCNN


if __name__ == '__main__':
    handler = callModelCNN()
    while 1:
        the_input = input('请输入：')
        ans = handler.callCNN()

        print(ans)

