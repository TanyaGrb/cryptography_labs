from itertools import product


def poly_to_str(*p):
    """
        красивый вывод полинома со степенями
    :param p: list - содержит только 0 и 1
    :return: str
    """
    str_p = ""
    l = len(p)
    if not p:
        return "0"
    for i in range(len(p)):
        if p[i] == 1:
            if l - i - 1 == 0:
                str_p += "1 + "
            elif l - i - 1 == 1:
                str_p += "x + "
            else:
                str_p += f"x^{l - i - 1} + "
    return str_p[:-2]


def poly_sum(a, b):
    """
        суммирует полиномы a и b
    :param a, b: list - содержит только 0 и 1
    :return: list - содержит только 0 и 1
    """
    if len(a) > len(b):
        while len(a) != len(b):
            b = [0] + b
    else:
        while len(a) != len(b):
            a = [0] + a
    result = []
    for i in range(len(a)):
        if a[i] == b[i]:
            result.append(0)
        else:
            result.append(1)
    while len(result) > 1 and result[0] == 0:
        result.pop(0)
    return result


def poly_div(a, b):
    """
        делит полином a на b
    :param a, b: list - содержит только 0 и 1
    :return: tuple(div(a, b), mod(a, b)), где div и mod это list - содержит только 0 и 1
    """
    if len(a) >= len(b):
        num_of_iter = len(a) - len(b) + 1
        dividend = a[0: len(b)]
        a = a[len(b):]
        result = []
        for i in range(num_of_iter):
            if len(dividend) >= len(b):
                result.append(1)
                dividend = poly_sum(dividend, b)
            else:
                result.append(0)
            if len(a) > 0:
                dividend.append(a.pop(0))
            while len(dividend) > 1 and dividend[0] == 0:
                dividend.pop(0)
        return result, dividend
    return [0], a


def get_polynomials_by_power(power: int):
    """
        находит все возможные полиномы степени power
    :param power: int - степень
    :return: list of lists
    """
    return [[1] + list(item) for item in list(product([0, 1], repeat=power))]


def get_irreducible_by_power(power: int):
    """
        находит все возможные неприводимые полиномы степени power
    :param power: int
    :return: list of lists
    """
    possible = get_polynomials_by_power(power)
    polynomials = [[1, 0]]
    for pwr in range(1, power):
        temp = get_polynomials_by_power(pwr)
        if temp == [1, 0]:
            polynomials.append(temp)
        else:
            polynomials.extend(temp)
    result = []
    for psble in possible:
        isIrreducible = True
        for poly in polynomials:
            _, mod = poly_div(psble, poly)
            if not mod[0]:
                isIrreducible = False
                break
        if isIrreducible:
            result.append(psble)
    return result


def get_cyclomatic_classes(power):
    """
        находит все возможные цикломатические классы поле GF(2^power)
    :param power: int
    :return: list of lists
    """
    powers = [i for i in range(1, 2 ** power)]
    classes = []
    while powers:
        current_class = []
        c = powers.pop(0)
        while c not in current_class and c != 0:
            current_class.append(c)
            if c in powers:
                powers.remove(c)
            c = c * 2 % (2 ** power - 1)
        classes.append(current_class)
    return classes


def find_minimum_poly(poly):
    """
        находит цикломатические классы в поле полинома poly и соответствующие им минимальные многочлены
    :param poly: list
    """
    power = len(poly) - 1
    c_classes = get_cyclomatic_classes(power)
    polynomials = []
    for i in range(1, power + 1):
        if power % i == 0:
            polynomials.extend(get_irreducible_by_power(i))
    for cl in c_classes:
        for p in polynomials:
            new_poly = [0 for _ in range((len(p) - 1) * cl[0] + 1)]
            for index, value in enumerate(p):
                if value == 1:
                    new_poly[index * cl[0]] = 1
            if poly_div(new_poly, poly)[1] == [0]:
                print(f"Цикломатический класс {cl}; многочлен: {poly_to_str(*p)}")


find_minimum_poly([1, 0, 1, 0, 0, 1])
# print(get_irreducible_by_power(5))
# print(get_irreducible_by_power(1))
