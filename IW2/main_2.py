from math import gcd
from random import randint, choice

task = """6. Реализовать алгоритм построения ПСП методом Фиббоначи с
запаздываниями. Обосновать выбор коэффициентов алгоритма. Для
начального заполнения использовать стандартную линейную конгруэнтную
ПСП с выбранным периодом. Реализовать возможность для пользователя
вводить коэффициенты заранее."""


def factor(n):
    result = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            result.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        result.append(n)
    return result


def get_coeff(period):
    c = randint(0, period)
    while gcd(c, period) != 1:
        c += 1
    b = 2
    a = None
    factor_result = factor(period)
    while b <= period:
        if all([b % p == 0 for p in factor_result]):
            if period % 4 == 0:
                if b % 4 == 0:
                    a = b + 1
                    break
            else:
                a = b + 1
                break
        b += 1
    return a, c, randint(2, period)


def gen_linear_congruential(period):
    coeff_a, coeff_c, x0 = get_coeff(period)
    result = [x0]
    for i in range(1, period):
        result.append((coeff_a * result[i - 1] + coeff_c) % period)
    return result


def LFG(init, lst, m, count):
    result = init.copy()
    for i in range(len(init), count):
        result.append(sum([result[len(result) - j] for j in lst]) % (2 ** m))
    return result


delays = input("Параметры запаздывания: ")
if not delays:
    # y = x^k + x^j + 1 must be primitive
    delays = choice([[7, 10], [5, 17], [24, 55], [65, 71], [128, 159]])
    k = delays[1] + 10
    m = 8
    print(f"delays = {delays}, k = {k}, m = {m}")
else:
    delays = [int(item) for item in delays.split()]
    k = int(input("Длина начального заполнения: "))
    m = int(input("Модуль: "))
initial_filling = gen_linear_congruential(k)
print(LFG(initial_filling, delays, m, 1000))
