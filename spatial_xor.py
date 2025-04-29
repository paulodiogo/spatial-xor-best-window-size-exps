import random, mmh3
from ctypes import c_uint32


class SpatialXor:    
    
    ARRAY_SIZE = 0
    WINDOW = 0
    HASHES = 3
    BITS_PER_FINGERPRINT = 8                    

    def __init__(self, arraySize, window, hashes = 3, max_iterations=1, fingerprint_size = 8):
      self.ARRAY_SIZE = arraySize
      self.WINDOW = window
      self.HASHES = hashes
      self.BITS_PER_FINGERPRINT = fingerprint_size      
      self.MAX_ITERATIONS = max_iterations      

    def fingerprint(self, x):
        return int(hash(x) & ((1 << self.BITS_PER_FINGERPRINT) - 1))    
    
    def murmur64(self, x):
        key = x.to_bytes((x.bit_length() + 7) // 8, 'big')
        return mmh3.hash64(key, seed = self.seed, signed=False)[0]    

    def independentHash(self, key, seed):
        return c_uint32(self.murmur64(key + c_uint32(seed).value)).value
    
    def hn(self, x, n, delta):
        return self.independentHash(x, self.seed + n) % delta

    def build(self, S):

        iterations = 0

        while True:

            self.seed = random.getrandbits(64)    

            success, stack = self.map(S)

            if success:
              break

            iterations += 1

            if iterations == self.MAX_ITERATIONS:
              raise Exception("Max iterations!")

        self.assign(S, stack)

        return True



    def map(self, S):                      

        t = []

        H = [t[:] for _ in range(self.ARRAY_SIZE)]           

        for x in S:
            values = self.hns(x)            
            for ind in values:
              H[ind].append(x)

        Q = []

        for i in range(len(H)):
          if len(H[i]) == 1:
            Q.append(i)                

        sigma = []

        while len(Q) > 0:
          i = Q.pop()          

          if len(H[i]) == 1:
            x = H[i][0]
            sigma.append((x, i))                       

            values = self.hns(x)

            for ind in values:              

              if(x in H[ind]):
                H[ind].remove(x)

              if len(H[ind]) == 1:
                Q.append(ind)        

        if len(sigma) == len(S):                    
          return True, sigma
        else:
          return False, []
      
    def assign(self, S, sigma):
      self.B = [0] * self.ARRAY_SIZE

      while len(sigma) > 0:
        x, i = sigma.pop()
        values = self.hns(x)

        res = 0

        for item in values:
          res ^= self.B[item]

        self.B[i] = 0        
        self.B[i] = self.fingerprint(x) ^ res           

    def contain(self, x):
        values = self.hns(x)

        res = 0

        for item in values:
          res ^= self.B[item]

        return self.fingerprint(x) == res

    def hns(self, x):

        values = []

        start = self.hn(x, 0, self.ARRAY_SIZE - self.WINDOW) 
        block = self.WINDOW // self.HASHES        

        for i in range(self.HASHES):
          values.append(start + self.hn(x, i, block) + (i * block))        

        return values