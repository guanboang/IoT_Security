import difflib

'''
时间 2020年6月17日 Python实现
'''
def circular_shift_left(int_value, k, bit):
    '''
    循环左移
    :param int_value: 数据
    :param k: 移位k位
    :param bit: 数据总位数
    :return: 移位后数据
    '''
    bit_string = '{:0%db}' % bit
    bin_value = bit_string.format(int_value)  # 8 bit binary
    bin_value = bin_value[k:] + bin_value[:k]
    int_value = int(bin_value, 2)
    return int_value
def circular_shift_right(int_value, k, bit):
    '''
    循环右移
    :param int_value: 数据
    :param k: 移位k位
    :param bit: 数据总位数
    :return: 移位后数据
    '''
    bit_string = '{:0%db}' % bit
    bin_value = bit_string.format(int_value)
    bin_value = bin_value[-k:] + bin_value[:-k]
    int_value = int(bin_value, 2)
    return int_value

def strToB(string):
    '''
    将输入输入映射到固定长度的关键字数组中
    :param string: 输入数据
    :return: 关键字数组list
    '''
    # 编码 字符串转字节数组
    string_bytes = string.encode()
    # 计算所有字节的总和
    temp = 0
    for i in string_bytes:
        temp = temp * (256) + i

    # 模运算 限制大小在50bit内
    temp = (temp) % (2 ** 50)
    temp_bin = bin(temp)[2:]

    # 少于50bit的，尾部补充0
    if len(temp_bin) < 50:
        for n in range(50 - len(temp_bin)):
            temp_bin = temp_bin + '0'

    # 每5bit的后面就补充一个1
    new_bin = ''
    for i in range(0,len(temp_bin),5):
        new_bin = new_bin + temp_bin[i:i+5] + '1'

    temp = int('0b'+new_bin,2) # 二进制转十进制
    temp = circular_shift_right(temp,29,60) # 循环右移29bit 总共60bit
    string_bin = bin(temp)[2:]

    # 少于60bit的，首部补充0
    if len(string_bin) < 60:
        for n in range(60 - len(string_bin)):
            string_bin = '0' + string_bin

    # 将01二进制字符串转化为每6bit一个数据（十进制）
    # data 的数组长度就是10，60 / 6 = 10
    data = []
    for i in range(0,len(string_bin),6):
        Sum = 0
        for j in range(6):
            Sum = Sum * 2 + int(string_bin[i+j])
        data.append(Sum)

    return data
def HASH(data):
    '''
    :param data: strToB函数的返回值data数组
    :return: 哈希值
    '''
    M = 13  # 因为data长度是10 所以寻找大于10的一个素数
    # Hash函数用的 除留余数法
    # Hash表的解决冲突机制是 线性探测
    Hash_table = []
    for i in range(M):
        Hash_table.append(0)
    for i in data:
        flag = 0
        for t in Hash_table:
            if i == t:
                flag = 1
                break
        if flag:
            continue
        Index = i % M
        if Hash_table[Index] == 0:
            Hash_table[Index] = i
        else:
            count = 0
            point = Index
            for j in range(M):
                if Hash_table[point] != 0:
                    count += 1
                else:
                    Hash_table[point] = i
                    count = 0
                    break
                point = (point + 1) % M
            if count == M:
                Hash_table[Index] = i

    # 此处可以个性化设计映射的字符，产生不同的hash值 :)
    chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n']
    HashCode = ''
    for i in data:
        temp = chars[Hash_table.index(i)]
        HashCode += temp
    return HashCode

'''首先将字符串转换为byte类型，然后将byte转换位hex（16进制），最后转换为10进制整数'''
def str2int(string):
    str_byte = bytes(string, encoding='utf-8')
    str_hex = str_byte.hex()
    str2int = int(str_hex,16)
    return str2int

'''上述转换的逆运算，将整数转换为字符串'''
def int2str(interger):
    int2hex = hex(interger)
    hex2byte = bytes.fromhex(int2hex[2:])
    byte2str = hex2byte.decode('utf-8')
    return byte2str

'''加密字符串，成为一个整数密文'''
def encryption(string, key):
    string2int = str2int(string)
    key2int = str2int(key)
    '''求字符串转整数后的位数，以便对密码转整数后通过倍数计算得到差不多
    相同的位数进行位运算（否则由于位运算的特性用相近的密码也能进行文本大
    部分还原），同时将这个位数储存在密文中，以便解密时使用相同的数字。'''
    len_str = len(str(string2int))
    len_len_str = len(str(len_str))
    len_key = len(str(key2int))
    key_multy = (len_str - len_key) if len_str >len_key else 0
    key_use = key2int * (10**(key_multy+1))
    encry_int = string2int ^ key_use
    return str(len_len_str)+str(len_str)+str(encry_int)

'''解密整数密文，根据异或与运算得到ASCII序号。然后翻译'''
def decryption(string, key):
    key2int = str2int(key)
    '''
    原字符串转化为整数的位数，以及位数的位数已经写到密文中前面部分了
    （之所以要记录两次信息，因为位数是不定长的，可能1个数字可能2、3个
    或更多）
    '''
    len_len_str = int(string[0])
    len_str = int(string[1:len_len_str+1])
    len_key = len(str(key2int))
    key_multy = (len_str - len_key) if len_str >len_key else 0
    key_use = key2int * (10**(key_multy+1))
    translate_string = string[len_len_str+1:]
    decry_int = int(translate_string) ^ key_use
    decry_str = int2str(decry_int)
    return decry_str

''' 对称加密的密钥 用于hash值的加密 '''
key = '82345678912592345678212592345671812392345678982592345567891682'

while(1):
    print('-------------输入Q退出--------------')
    print('请输入数据一：')
    string = input()
    if string == 'Q':
        break
    HASH_P = (strToB(string))

    print('',''.join(reversed(HASH_P)))
    print('hash值: ', HASH(strToB(string)))
    Mac_string = bin(int(encryption(HASH(strToB(string)), key)))[2:] + '01011'
    print('MAC值: ', Mac_string)
    Mac_string1=Mac_string
    print('长度bit: ', len(Mac_string), '位')

    print('请输入数据二：')
    string = input()
    if string == 'Q':
        break
    print('hash值: ', HASH(strToB(string)))
    Mac_string = bin(int(encryption(HASH(strToB(string)), key)))[2:] + '01011'
    print('MAC值: ', Mac_string)
    print('长度bit: ', len(Mac_string), '位')
    if Mac_string==Mac_string1:
        print('\033[7;31mMAC并未发生改变\033[0m')
    else:
        print('\033[7;31mMAC发生改变\033[0m')
        Mac_string1_lines = Mac_string1.splitlines()
        Mac_string_lines = Mac_string.splitlines()
        d = difflib.Differ()
        diff = d.compare(Mac_string1_lines,Mac_string_lines)
        print('\n'.join(list(diff)))

# '''测试样例'''
# print('--------------------------------------------------------------')
#
# test1 = 'testdata'
# test2 = 'ttstdata'
#
# print('数据: ',test1,'   hash值: ',HASH(strToB(test1)))
# print('数据: ',test2,'   hash值: ',HASH(strToB(test2)))
# print()
#
# Mac_test1 = bin(int(encryption(HASH(strToB(test1)),key)))[2:]+'01011'
# Mac_test2 = bin(int(encryption(HASH(strToB(test2)),key)))[2:]+'01011'
#
# print('数据: ',test1,'   MAC值: ',Mac_test1)
# print('长度bit: ',len(Mac_test1),'位')
# print('数据: ',test1,'   MAC值: ',Mac_test1)
# print('长度bit: ',len(Mac_test1),'位')
# print('\033[7;31mMac值是否相同？\033[0m',Mac_test1 == Mac_test2)
# print('\n--------------------------------------------------------------')
#
#
# test1 = 'Baymax'
# test2 = 'BazMf8'
#
# print('数据: ',test1,'   hash值: ',HASH(strToB(test1)))
# print('数据: ',test2,'   hash值: ',HASH(strToB(test2)))
# print()
# Mac_test1 = bin(int(encryption(HASH(strToB(test1)),key)))[2:]+'01011'
# Mac_test2 = bin(int(encryption(HASH(strToB(test2)),key)))[2:]+'01011'
#
# print('数据: ',test1,'   MAC值: ',Mac_test1)
# print('长度bit: ',len(Mac_test1),'位')
# print('数据: ',test2,'   MAC值: ',Mac_test2)
# print('长度bit: ',len(Mac_test2),'位')
# print('\033[7;31mMac值是否相同？\033[0m',Mac_test1 == Mac_test2)