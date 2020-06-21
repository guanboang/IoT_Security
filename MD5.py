import math
import time
import hashlib
rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

constants = [int(abs(math.sin(i + 1)) * 2 ** 32) & 0xFFFFFFFF for i in range(64)]

# A B C D
init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
# 非线性函数
functions = 16 * [lambda b, c, d: (b & c) | (~b & d)] + \
            16 * [lambda b, c, d: (d & b) | (~d & c)] + \
            16 * [lambda b, c, d: b ^ c ^ d] + \
            16 * [lambda b, c, d: c ^ (b | ~d)]

index_functions = 16 * [lambda i: i] + \
                  16 * [lambda i: (5 * i + 1) % 16] + \
                  16 * [lambda i: (3 * i + 5) % 16] + \
                  16 * [lambda i: (7 * i) % 16]


# 对x左移amount位
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF


def md5(message):
    message = bytearray(message)  # copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message) % 64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')

    hash_pieces = init_values[:]

    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst + 64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4 * g:4 * g + 4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))


def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))


def my_md5(message):
    return md5_to_hex(md5(message))


T1=time.time()
demo = b"cbjooeah3yel9vzsojx5mudqd94k2xs3sb0h160bcio3z74c5979bk7ldaroe0spn462a8fscoqixeexow5lebwz9o0h2afashc3ejkkfq9phc24bwta1jqv8pbwa9q4alvi18kv79i7995t3o56v2ubp7e0gaikrytzevwt0e16dv8524t40fbssqdkwrcmw94qy7xjg2wwj525ch3yitthy54oxcrjl1rsx1ppx17xs4d9u4grdyfaec326uxe1sww45q81340w1hnc9qgqxnmgzmoewb3gnypidxzghhvgxig16lh2eai1d1j2zfmffysz9y6anjsmeq54q1ygynkggzajtccy7rj8y50xcry7ol3edj14h6vf5gxlqthvg0f433grkfkjac4mc6in2lhuumfrb0ab54fdje2o8y3iib2w2e41hsxeqhxo6s28vmt8ppexzpg1inyeyjwhruv921ltoy17ijymeal45p1knzzvzr7e3yprdsn9l4luej7bf0i2n9y8tcidhmm8jxe0gtsnc75hz50tvzawlzrdr5yax5kbx2yks69oq992wxbmr6q2wev2kdlt9f8yl9yi2aehvtd9k861vis2ak2d3mi6awsbxr5qogz8kxgsy6p83phoha91u5jwgm6qovj02old5mwywg15ubas7jb0pzgah8dwnnk95r7oy6ih7c35e11f3i42xjc2bzwp3th1t68bb3ibi9zzeqfufuydso7b6ccznuxyx7nfuxw"
print('个人实现\t',my_md5(demo))
T2=time.time()
print('时间为',(T2-T1)*1000000,'微秒')
T3=time.time()
print('MD5库\t',hashlib.md5(demo).hexdigest())
T4=time.time()
print('时间为',(T4-T3)*1000000,'微秒')
print('时间差值为：\033[7;31m',-(T4-T3-T2+T1)*1000000,'微秒\033[0m')


