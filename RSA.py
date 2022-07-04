import random
                 
def karatsuba(num1,num2):
    global N,phiN

    num1 = str(num1)
    num2 = str(num2)
    len1 = len(num1)
    len2 = len(num2)

    if len1 == 0 or len2 == 0:
        return "0"

    result = [0] * (len1 + len2)

    i_n1 = 0
    i_n2 = 0

    for i in range(len1 - 1, -1, -1):
        carry = 0
        n1 = ord(num1[i]) - 48

        i_n2 = 0

        for j in range(len2 - 1, -1, -1):

            n2 = ord(num2[j]) - 48

            summ = n1 * n2 + result[i_n1 + i_n2] + carry

            carry = summ // 10

            result[i_n1 + i_n2] = summ % 10

            i_n2 += 1

        if (carry > 0):
            result[i_n1 + i_n2] += carry

        i_n1 += 1

    i = len(result) - 1
    while (i >= 0 and result[i] == 0):
        i -= 1

    if (i == -1):
        return "0"

    s = ""
    while (i >= 0):
        s += chr(result[i] + 48)
        i -= 1

    return int(s)


def power(x, y, p):
    res = 1
    x = x % p

    while (y > 0):
        if (y & 1):
            res = (res * x) % p
        y = y >> 1      # y = y/2
        x = (x * x) % p

    return res

def gcd(p, q):
    #euclidean algorithm to determine greatest common divisor of p and q

    while q:
        p, q = q, p % q
    return p

def egcd(a, b):
    
        #euclids extended greatest common divisor algorithm
        #ax + by = gcd(a, b)
    
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient*r
        old_s, s = s, old_s - quotient*s
        old_t, t = t, old_t - quotient*t

    return [old_r, old_s, old_t]

def isCoPrime(p, q):
        #return True if p and q are coPrime
        #if gcd(p, q) == 1
    

    return gcd(p, q) == 1

def generateLargePrime(keysize=1024):
    
        #return a random large prime number of keysize bits in size
    
    while True:
        num = random.randint(2**(keysize-1), 2**(keysize)-1)
        if isPrime(num):
            return num

def rabinMiller(n):
    #return True if n is prime
    s = n - 1
    t = 0
    while s % 2 == 0:
        # count how many times we have to halve n
        s = s // 2
        t += 1

    for trial in range(128): # try to prove not prime 128 times
        a = random.randint(2, n - 1)
        v = power(a, s, n)
        if v != 1: # test doesn't apply if v == 1
            i = 0
            while v != n - 1:
                if i == t - 1:
                    return False
                else:
                    i += 1
                    v = power(v, 2, n)

    return True

def generateKeys(keysize=1024):

    global e ,d,p,q,N
    
    e=d=N= 0

    # get prime numbers
    p = generateLargePrime(keysize)
    q = generateLargePrime(keysize)

    #N = p * q
    N=karatsuba(p,q)

    #phiN = (p - 1) * (q - 1)
    phiN=karatsuba(p-1,q-1)

    while True:
        e = random.randint(2 ** (keysize - 1), 2 ** (keysize)-1)
        if isCoPrime(e, phiN):
            break

    d = modularInverse(e, phiN)


    return e,d,N

def isPrime(n):

    # 0, 1, negetive numbers are not prime
    if n < 2:
        return False

    # low prime numbers (< 1000) to save time
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    if n in lowPrimes:
        return True

    # if low primes divide into n
    for prime in lowPrimes:
        if n % prime == 0:
            return False

    # else do rabin miller algorithm
    return rabinMiller(n)


def modularInverse(a, m):

    # gcd using euclid's algorithm
    gcd, x, y = egcd(a, m)

    if x < 0:
        x += m

    return x

def keystxt():
    global public_keys
    global secret_keys


    public_keys=[]
    secret_keys=[]

    print("loading...")
    generateKeys()
    N=karatsuba(p,q)
    phiN=karatsuba(p-1,q-1)
    
    secret_keys = [d, N]
    with open('secret_keys.txt', 'w') as f:
        f.write('{}\n{}'.format(secret_keys[0], secret_keys[1]))

    public_keys = [e, N]
    with open('public_keys.txt', 'w') as f:
        f.write('{}\n{}'.format(public_keys[0], public_keys[1]))
    
    return public_keys,secret_keys
    
def readkeys():
    global e,N
    public_keys=[]
    print('wait...')
    with open('public_keys.txt', 'r') as f:
        list1=f.readlines()
        if list1!=[]:
            pubilc_keys=[int(list1[0]),int(list1[1])]
    e=pubilc_keys[0]
    N=pubilc_keys[1]
    
    return e,N

def encrypt(msg,e,N,sizebolok=200):
    boloklist=[]
    ciphertext=0
    
    if(len(msg))>0:
        ciphertext=ord(msg[0])

    for i in range(1,len(msg)):
        if (i%sizebolok==0):
            boloklist.append(ciphertext)
            ciphertext=0

        ciphertext=ciphertext*256+ord(msg[i])

    boloklist.append(ciphertext)
    for i in range(len(boloklist)):
        boloklist[i]=str(power(boloklist[i],e,N))

    Encrypted_message=" ".join(boloklist)

    return Encrypted_message

def crt(d,p,q,c):
    dq=power(d,1,q-1)
    dp=power(d,1,p-1)
    m1=power(int(c),dp,p)
    m2=power(int(c),dq,q)

    qinv=int(gcd(1/q,p))
    h=int((qinv*(m1-m2)))
    h2=power(h,1,p)
    m=m2+h2*q
    return m


def decrypt(code,sizebolok=200):  
    message=''
    code2=list(code)
    code2=map(int,code.split())

    for i in code2:
        i=crt(d,p,q,i)

        text=''
        for j in range(sizebolok):
            text+=chr(i%256)
            i=i//256

        message+=text[::-1]

    return message
                        
def main():
    while True:
        print('enter 1 to make or use keys ')
        choose=int(input())
        if choose==1:
            print("1.making keys 2.use the user's keys")
            ke=int(input())
            if ke==1:
                keys=keystxt()
                print('1.decryptnewmsg 2.encrypt')
                po=int(input())
                
                if po==1:
                    print('enter:')
                    msg2=input()
                    print(decrypt(msg2))
                
                if po==2:
                    print('enter your message:')
                    msg=input()
                    
                    
                    print(encrypt(msg,e,N))
                    print("enter 3 if you wanna decrypt the last message, enter 4 to pass")
                    f=int(input())
                    if f==3:
                        print(decrypt(encrypt(msg,e,N)))
                    if f==4:
                        pass
  
            if ke==2:
                keys=readkeys()
                print('enter your message:')
                msg3=input()
                print(encrypt(msg3,int(e),int(N)))
                

main()




