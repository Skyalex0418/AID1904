import getpass # 隐藏输入
import hashlib # 转换加密

# 输入隐藏
pwd = getpass.getpass("PW:")
print(pwd)

# hash对象
# hash = hashlib.md5() # 生成对象

# 算法加盐
hash = hashlib.md5("*#06l_".encode())
hash.update(pwd.encode()) # 算法加密
pwd = hash.hexdigest() # 提取加密后的密码
print(pwd)




