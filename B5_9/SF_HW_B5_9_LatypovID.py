# -*- coding: utf-8 -*-
import time

class Time_it:
    def __init__(self, num_runs=10):
        self.num_runs = num_runs
        self.avg_time = 0
        self.t0 = 0
        self.t1 = 0

    def __call__(self,func):       
        def wrap(*args, **kwargs):
            avg_t = 0            
            for i in range(self.num_runs):
                t0 = time.time()
                func(*args, **kwargs)
                t1 = time.time()
                avg_t += (t1 - t0)

            self.avg_time = avg_t/self.num_runs
            print("Среднее время выполнения 1 запуска из", self.num_runs,"заняло %.5f секунд" % self.avg_time)            
        return wrap
    
    def __enter__(self):
        self.t0 = time.time()
        return self
    
    def __exit__(self, type, value, traceback):
        self.t1 = time.time()
        print("Время выполнения 1 запуска заняло %.5f секунд" % (self.t1 - self.t0))
        return self


def time_this(num_runs = 10):       
    def decorator(func):
        def wrap(*args, **kwargs):
            avg_t = 0            
            for i in range(num_runs):
                t0 = time.time()
                func(*args, **kwargs)
                t1 = time.time()
                avg_t += (t1 - t0)

            avg_time = avg_t/num_runs
            print("Среднее время выполнения 1 запуска из", num_runs,"заняло %.5f секунд" % avg_time)            
        return wrap
    return decorator    
    
print("--------------------------------функция декоратор--------------------------------------------")   

@time_this(num_runs=15)
def f(iters = 1000000):
    for j in range(iters):
        pass

f()

print("\n---------------------------------класс декоратор---------------------------------------------")
@Time_it(num_runs = 20)
def ff(iters = 1000000):
    for j in range(iters):
        pass
    
ff()   

print("\n-------------------------класс контекстный менеджер декоратор--------------------------------")
def fff(iters = 1000000):
    for j in range(iters):
        pass
    
with Time_it() as tf:
    fff()