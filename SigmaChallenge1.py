import random
import requests
from multiprocessing.pool import ThreadPool as Pool
import time

def miller_rabin(n, k):
    #referencia:https://gist.github.com/Ayrx/5884790
    if n == 2:return True
    if n % 2 == 0:return False
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def palimdome(x):
  return x == x[::-1]

def Compute(aux, i, n, chunk):
  c=0
  while c<len(i)-n:
    if palimdome(aux):
      print('Found a palimdrom  -> '+aux+' chunk -> '+str(chunk))
      if miller_rabin(int(aux),40):
        print('Found a PalPrime -> '+aux+' chunk -> '+str(chunk))
        break
    c+=1
    n+=1
    aux=i[c:n]

def Search_PalPrime(n,start):
  num_digits = 1000
  chunk = start
  end = start+10000000
  while start<end:
    time.sleep(1)
    r = requests.get('https://api.pi.delivery/v1/pi?start={}&numberOfDigits={}'.format(start, num_digits))
    PI = r.json()['content'][1:]
    aux1 = PI[0:n]
    Compute(aux1,PI,n,chunk)
    start +=num_digits


def worker(n,item):
    try:
        Search_PalPrime(n,item)
    except:
        print('error with chunk ->', item)

n = 21#palindrome size

pool_size = 10
pool = Pool(pool_size)
intervalo = 100000000

l = [i*intervalo  for i in range(pool_size*254,pool_size*254+pool_size)]
print(l)
for item in l:
    pool.apply_async(worker, (n,item))
pool.close()
pool.join()


