def logger(func):
    def wraped(*args, **qwargs):
        origin = func(*args, **qwargs)
        args_list = list(map(str, args))
        qwargs_list = list(map(str, qwargs.values()))
        join_all = ", ".join(args_list + qwargs_list)
        print(f'Executing of function {func.__name__} with arguments {join_all}...')
        return origin
    return wraped


@logger
def concat(*args, **qwargs):
    args_join = ''.join(list(map(str, args)))
    qwargs_join = ''.join(list(map(str, qwargs.values())))
    return args_join + qwargs_join


@logger
def sum(a, b):
    return a + b


@logger
def print_arg(arg):
    print(arg)

print(concat(2, 3))
#print(concat('hello', 2))
#print(concat (first = 'one', second = 'two'))
#print(concat('first string', second = 2, third = 'second string'))
print_arg(2)