import numpy

sbox = [9, 11, 12, 4, 10, 1, 2, 6, 13, 7, 3, 8, 15, 14, 0, 5]
xobs = [14, 5, 6, 10, 3, 15, 7, 9, 11, 0, 4, 1, 2, 8, 13, 12]

key = (9, 2)

def enc (m, key):
    t = sbox[m ^ key[0]]
    c = sbox[t ^ key[1]]
    return c


def tc1r(m, key):
    return sbox[m ^ key[0]]

def tc1rs(m, key):
    return xobs[tc1r(m, key)]

def dec (c, key):
    t = xobs[c] ^ key[1]
    m = xobs[t] ^ key[0]
    return m

def dec_round1 (c, key):
    t = xobs[c] ^ key[0]
    return t

import random 

cleartex = random.randint(0, 15)

cleartex

secret = random.randint(0,15), random.randint(0,15)

chiphertext = tc1rs(cleartex, secret)
chiphertext


text = enc(cleartex, secret)
text

def brute_enc(msg, c):
    for i in range(16):
        for j in range(16):
            msg_t = enc(msg, (i, j))
            if(msg_t == c):
                print(f"The key is : {(i, j)}")
                return (i, j)
            
def brute_enc_v2(msg, c):
    for i in range(16):
        for j in range(16):
            msg_t = enc(msg, (i, j))
            if(msg_t == c):
                print(f"The key is : {(i, j)}")
            

print(f"The keys: {secret}")
print(f"The text: {cleartex}")
print(f"The crypted texte: {text}")
keys_find = brute_enc(cleartex, text)
print(keys_find)
new_text = dec(text, keys_find)
print(f"The decrypted texte: {new_text}\n\n")

print("Test de la deuxième version de brute_enc")

brute_enc_v2(cleartex, text)

def kpa(key, n):
    l = []
    for i in range(n):
        msg = random.randint(0, 15)
        l.append((msg, enc(msg, key)))
    return l

print("\n", kpa((10, 7), 10), "\n")

def parity(nmb):
    return bin(nmb).count("1")

def getCouple():
    return [(i, sbox[i]) for i in range(16)]

def linearCount():
    matrix = [[0 for maskI in range(16)] for maskO in range(16)]
    msgList = getCouple()
    for maskI in range(16):
        for maskO in range(16):
            for msg in msgList:
                if (parity(msg[0]&maskI)+parity(msg[1]&maskO))%2 == 0:
                    matrix[maskI][maskO] += 1
    return matrix

print(numpy.matrix(linearCount()), "\n")


def bestPaire(tab): 
    maxCount = 0 
    countBit_max=0 
    bestMaskI = 0 
    bestMaskO = 0
    for maski in range(16): 
        for mask0 in range(16): 
            if maski or mask0:   
                compteur_parite = tab[maski][mask0]
                countBit = parity(mask0) +  parity(maski)
                if compteur_parite >= maxCount and countBit > countBit_max:
                    maxCount, countBit_max, bestMaskI, bestMaskO = compteur_parite, countBit, maski, mask0
    return bestMaskI, bestMaskO

print(bestPaire(linearCount()), "\n")

paires = kpa((10, 9), 16)
print(paires)

#Exo 4 question 2,3

def matrixMax(matrix):
    max = 0
    for maskI in range(16):
        for maskO in range(16):
            if matrix[maskI][maskO] > max and maskO+maskI !=0:
                max = matrix[maskI][maskO]
    return max

def candidatsKey0(msgCouples, maskI, maskO):
    candidats = []
    max_score = 0

    for key0 in range(16):
        score = sum(1 for msg, msgC in msgCouples if (parity(sbox[msg ^ key0] & maskI) + parity(msgC & maskO)) % 2 == 0)

        if abs(score - 8) > max_score:
            max_score = abs(score - 8)
            candidats = [key0]
        elif abs(score - 8) == max_score:
            candidats.append(key0)

    return candidats


k0, k1 = random.randint(0, 15), random.randint(0, 15)
data = kpa((k0, k1), 16)

candidats = candidatsKey0(data, bestPaire(linearCount())[0], bestPaire(linearCount())[1])
print(candidats)
        
def findKey(candidats, msgCouples):
    for key0 in candidats:
        t0 = sbox[key0 ^ msgCouples[0][0]]
        t1 = xobs[msgCouples[0][1]]
        key1 = t0 ^ t1

        valid = all(msgC == enc(msg, [key0, key1]) and msg == dec(msgC, [key0, key1]) for msg, msgC in msgCouples)
        if valid:
            return [key0, key1]


print(f"Clés utilisé : ({k0}, {k1})")
print(f"Résultat à obtenir : {findKey(candidats, data)}\n")


def substitute(x):
    return (5 * x + 3) % 16

# Génération de la boîte S
def generate_SBox():
    SBox = numpy.arange(16, dtype=numpy.uint8)
    numpy.random.shuffle(SBox)  # Permutation aléatoire
    return SBox

SBox = generate_SBox()
for i in range(16):
    SBox[i] = substitute(SBox[i]) 

SBox = SBox.tolist()

print(SBox)

XBox = [SBox.index(i) for i in range(len(SBox))]

compteur = 0
approxLinear = bestPaire(linearCount())
for i in range(1000):
    k0, k1 = random.randint(0, 15), random.randint(0, 15)
    data = kpa((k0, k1), 16)
    candidats = candidatsKey0(data, approxLinear[0], approxLinear[1])
    if findKey(candidats, data) != None: # si clé trouvé
        compteur += 1

print(f"Pourcentage d'attaque réussite avec boiteS : {compteur/10}%")

sbox = SBox
xobs = XBox

compteur = 0
approxLinear = bestPaire(linearCount())
for i in range(1000):
    k0, k1 = random.randint(0, 15), random.randint(0, 15)
    data = kpa((k0, k1), 16)
    candidats = candidatsKey0(data, approxLinear[0], approxLinear[1])
    if findKey(candidats, data) != None: # si clé trouvé
        compteur += 1

print(f"Pourcentage d'attaque réussite avec boiteS modifier: {compteur/10}%")