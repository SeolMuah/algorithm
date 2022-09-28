from collections import Counter

in_str = 'ABCDEFGHIJKLMNOP'
in_str = 'aaabrbacard'
in_str = 'AAAAAAABBCCCDEEEEFFFFFFG'
str_list = list(in_str)
str_count = Counter(str_list)
str_count = [[v,k] for k, v in str_count.items()]
str_count.sort(key=lambda x: x[0],reverse=True)
encode_dic = {v:[] for k, v in str_count}

import numpy as np
total = sum([e[0] for e in str_count])
prob = {e[1] : e[0]/total  for e in str_count}
entropy = sum([-np.log2(e[0]/total) *e[0]/total  for e in str_count])


def encode_func(n_list, num) :
    if type(n_list[1]) == list :
        for e in n_list[1] :
            encode_func(e, num)
    else :
        encode_dic[n_list[1]] = [num] + encode_dic[n_list[1]]

def get_child_node_num(node) :
    num = 0
    if type(node[1]) == list :
        for e in node[1] :
            num += get_child_node_num(e)
        return num
    else :
        return 1
        

while len(str_count) != 1 :
    n1 = str_count.pop() #1 
    n2 = str_count.pop() #0

    num = n1[0] + n2[0]

    encode_func(n2, 0)
    encode_func(n1, 1)

    new_node = [num, [n2, n1]]
    str_count.append(new_node)

    #노드 값이 같다면, 하위 노드가 작은 것이 뒤로
    str_count.sort(key=lambda x: (x[0], get_child_node_num(x)), reverse=True)
    print(str_count)

print(encode_dic, f"총 비트 길이 {sum([len(e) for e in encode_dic.values()])}, 평균 길이 : {sum([len(v)*prob[k] for k,v in encode_dic.items()])}, 엔트로피 : {entropy}")
encode_dic = {k : ''.join([str(i) for i in v]) for k,v in encode_dic.items()}
print(encode_dic)

out_str = ''.join([encode_dic[ch] for ch in in_str])
print(out_str)


encode_list = [(k,v) for k,v in encode_dic.items()]
encode_list.sort(key=lambda x: (x[0]))

#decoding
decoded_str = ""
word = ""
for ch in out_str:
    word += ch
    for conv_ch in encode_list :
        if word == conv_ch[1] :
            decoded_str += conv_ch[0]
            word = ""
            break
print(decoded_str)
