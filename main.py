import time
from info_manager import execute

def main(city,date):
    return execute(city,date)

if __name__ == '__main__':
    t0 = time.time()
    print(main('трускавець','2021.09.17'))
    delta = time.time() - t0
    print(delta)
