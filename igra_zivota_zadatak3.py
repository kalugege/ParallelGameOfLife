import numpy as np
import multiprocessing as mp

N = 4
matrica=np.random.randint(2,size=(N,N))

def igra_zivota(task,matrica,N):
    
    koordinate = {}
    for x , y in task:
        ziveKomsije=0
        for i in range(x - 1, x + 2):
            for j in range(y - 1,y + 2):
                if x == i and y == j:
                    continue
                if i<0 or i>= N:
                    i=i % N
                if j < 0 or j>=N:
                    j = j % N
                ziveKomsije += matrica[i,j]
        # print(ziveKomsije)
        if ziveKomsije < 2 or ziveKomsije > 3:
            koordinate[(x,y)]=0
        elif matrica[x,y] == 1 and (ziveKomsije == 2 or ziveKomsije == 3):
            koordinate[(x,y)]=1
        elif matrica[x,y] == 0 and ziveKomsije == 3:
           koordinate[(x,y)]=1
        else: koordinate[(x,y)]=0          

    return koordinate
if __name__ == '__main__':
    lista_matrica=[matrica.copy()]
    tasks=[]
    rezultati=[]
    # print(matrica)

    for i in range(N):
        red = []
        for j in range(N):
            red.append((i,j))
        tasks.append(red)

    pool = mp.Pool(mp.cpu_count())

    for i in range(0,100):
        rezultati = [pool.apply(igra_zivota,args=(task,matrica,N)) for task in tasks]

        for rezultat in rezultati:
            for kljuc,vrednost in rezultat.items():
                matrica[kljuc[0],kljuc[1]]=vrednost
                # print(kljuc , ':' , vrednost)

        lista_matrica.append(matrica.copy()) 
    # print(rezultati)
    pool.close()
    pool.join()
count=0
for m in lista_matrica:

    print(count,m)
    count=count+1


                    
                
                

