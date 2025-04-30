# list = [1,1,2,2,3,3,4,4,5,6,6,7,7]
#
# unique_list = []
#
# for i in list:
#     if i not in unique_list:
#         list += [i]
# print(list)
#


# str1 = "hello"
# print(str1[::-1])

# a=5
# b=10
# a,b=b,a
# print(a)
# print(b)


lst = [9, 7, 4, 2, 1]
for i in range(len(lst)):
    # print(lst[i])
    for j in range(i + 1, len(lst)):
        print(lst[i], lst[j])
        if lst[i] > lst[j]:
            lst[i], lst[j] = lst[j], lst[i]

print(lst)
