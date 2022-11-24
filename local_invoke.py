from multiprocessing import Process, Pipe

from handler import multi


if __name__ == '__main__':
    x = multi(1.1,1)
    print(x)
        

