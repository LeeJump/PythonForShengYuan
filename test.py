def power(x, ct):
    # 定义次幂函数
    i = ct
    res = 1
    while i:
        res *= x
        i -= 1
    return res

def fun(x):
    # 1, 定义题目函数f(x)=2*x^3+5, 传入x,返回f(x)
    return 2 * (power(x, 3)) + 5

def differentQuotient(func, x_list):
    # 2, 定义求差商方法,func 为函数名, x_list为自变量x
    if len(x_list) == 2:
        numerate = func(x_list[0]) - func(x_list[1])
        denominator = x_list[0] - x_list[1]
        return numerate / denominator
    elif len(x_list) >= 3:
        numerate = differentQuotient(func, x_list=x_list[0:-1]) - differentQuotient(func, x_list=x_list[1:])
        denominator = x_list[-1] - x_list[0]
        return numerate / denominator


# 当x=[1,2,3,4] 时, 计算差值
x_list = list(range(1, 5))
print('差商', 'f', x_list, '=', differentQuotient(fun, x_list))
# 当x=[1,2,3,4,5] 时, 计算差值
x_list = list(range(1, 6))
print('差商', 'f', x_list, '=', differentQuotient(fun, x_list))
