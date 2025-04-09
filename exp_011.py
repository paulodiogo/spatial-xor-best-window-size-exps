import datetime, itertools, time
import spatial_xor
from multiprocessing import Pool

def buildXOR(X, i, n):

    data = list(range(n))

    try:
        X.build(data)
        return True
    except:
        return False

def getBestAlfaZ(T, k, Z, fileName, addText):
    FRAC_ALFA = 1000

    MIN_ALFA = 0
    MAX_ALFA = FRAC_ALFA
    ULTIMO = None

    while True:            

        alfa = (MAX_ALFA - ((MAX_ALFA - MIN_ALFA) / 2))/FRAC_ALFA

        start = time.time()

        N = int(T * alfa)

        X = spatial_xor.SpatialXor(T, Z, k)

        iteracoes = list(range(11))

        RESULT = int(len(iteracoes) / 2) + 1

        assert(RESULT == 6)

        res = []

        with Pool(processes=11) as pool:
            res = pool.starmap(buildXOR, zip(itertools.repeat(X), iteracoes, itertools.repeat(N)))                
        
        TOTAL = res.count(True)

        end = time.time()
        totalTime = (end - start)

        with open(fileName, "a") as text_file:
            text_file.write(f'{k};{alfa:.15f};{Z};{TOTAL};{totalTime:.2f};{addText};\n')
        
        if TOTAL >= RESULT:
            MIN_ALFA = (MAX_ALFA - ((MAX_ALFA - MIN_ALFA) / 2))
            ULTIMO = alfa
        else:
            MAX_ALFA = (MAX_ALFA - ((MAX_ALFA - MIN_ALFA) / 2))
        
        if (MAX_ALFA - MIN_ALFA) < (10 ** -3):            
            break

    return ULTIMO

def getQuartersT(MIN_WIN, MAX_WIN):

  QUARTER = int((MAX_WIN-MIN_WIN) / 4)

  return (MIN_WIN + QUARTER), MIN_WIN + (2*QUARTER), (MIN_WIN + (3*QUARTER))

def run(T, k):    

    data_file = datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    fileName = f"data/exp_011_{T}_{data_file}.exp"

    MIN_WIN = 0
    MAX_WIN = T

    RES = {}

    while True:    

        WIN_1Q, WIN_MID, WIN_2Q = getQuartersT(MIN_WIN, MAX_WIN)

        valoresTexto = ((MIN_WIN, MAX_WIN), (WIN_1Q, WIN_MID, WIN_2Q))

        if WIN_1Q not in RES:
            ALFA_1Q = getBestAlfaZ(T, k, WIN_1Q, fileName, valoresTexto)
            RES[WIN_1Q] = ALFA_1Q

        if WIN_MID not in RES:
            ALFA_MID = getBestAlfaZ(T, k, WIN_MID, fileName, valoresTexto)
            RES[WIN_MID] = ALFA_MID

        if WIN_2Q not in RES:
            ALFA_2Q = getBestAlfaZ(T, k, WIN_2Q, fileName, valoresTexto)
            RES[WIN_2Q] = ALFA_2Q

        if RES[WIN_1Q] > RES[WIN_MID] > RES[WIN_2Q]: #/
            MAX_WIN = WIN_MID            
        elif RES[WIN_1Q] < RES[WIN_MID] < RES[WIN_2Q]: #\'
            MIN_WIN = WIN_MID
        elif RES[WIN_1Q] < RES[WIN_MID] > RES[WIN_2Q]: #/\
            MIN_WIN = WIN_1Q
            MAX_WIN = WIN_2Q
        elif RES[WIN_1Q] > RES[WIN_MID] < RES[WIN_2Q]: #\/

            if RES[WIN_1Q] >= RES[WIN_2Q]:                       
                MAX_WIN = WIN_MID
            else:
                MIN_WIN = WIN_MID           

        elif RES[WIN_1Q] == RES[WIN_MID] > RES[WIN_2Q]:#-\            
            MAX_WIN = WIN_MID
        elif RES[WIN_1Q] < RES[WIN_MID] == RES[WIN_2Q]:#/-
            MIN_WIN = WIN_MID
        elif RES[WIN_1Q] == RES[WIN_MID] == RES[WIN_2Q]:#--
            MIN_WIN = WIN_1Q
            MAX_WIN = WIN_2Q
        elif RES[WIN_1Q] == RES[WIN_MID] < RES[WIN_2Q]:#_/
            MIN_WIN = WIN_MID        
        elif RES[WIN_1Q] > RES[WIN_MID] == RES[WIN_2Q]:#\_            
            MAX_WIN = WIN_MID
        else:
            print("ERRO!",MAX_WIN, MIN_WIN, MAX_WIN - MIN_WIN, RES)
            break        

        if (MAX_WIN - MIN_WIN) < 50:
            break