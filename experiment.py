bool_list = [True, True, False, True, True, False, False, True]
res_true, res_false = [], []
for i in range(0, len(bool_list)):
    if bool_list[i]:
        res_true.append(i)
    else:
        res_false.append(i)
print(f'true  - {res_true}')
print(f'false  - {res_false}')

