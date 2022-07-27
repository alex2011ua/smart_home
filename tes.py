# put your python code here
s1 = input().lower()

dict1 = {x: s1.count(x) for x in s1 if x not in ".,!?:;-"}
del dict1[" "]
s2 = input().lower()
dict2 = {x: s2.count(x) for x in s2 if x not in ".,!?:;-"}
del dict2[" "]
print("YES" if dict1 == dict2 else "NO")