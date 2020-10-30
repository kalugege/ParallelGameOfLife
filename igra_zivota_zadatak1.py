import numpy as np
import random
import threading 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
N = 4
matrica=np.random.randint(2,size=(N,N))
#matrica =   [[0,0,0,0],
           # [0,1,0,0],
          #  [0,0,1,1],
          #  [1,0,0,1]]
listaMatrica = []
brojacCelija = 0

print(matrica) 

brojacCelijaLock = threading.Lock()
procitanOdLock = threading.Lock()
sledecaIteracija=threading.Condition()

class Celija(threading.Thread):
    def __init__(self,stanje,i,j):
        super().__init__()
        self.iteracija=0
        self.procitanOd = [0,0,0,0,0,0,0,0]
        self.stanje=stanje
        self.i=i
        self.j=j
        self.semaforCelije = threading.Semaphore(0)    

    
    
    def proveraSuseda(self):
        #lista = []
        
        ziveKomsije=0
        pozicija=0
        for x in range(self.i - 1, self.i + 2):
            for y in range(self.j - 1, self.j + 2):
                if x == self.i and y == self.j:
                    continue
                
                if x<0 or x>= N:
                    x=x % N
                if y < 0 or y>=N:
                    y = y % N
                self.azurirajListu(x,y,pozicija)
                pozicija+=1
                ziveKomsije+=matrica[x,y]    
               #lista.append((x,y))
                
        return ziveKomsije

   
    def azurirajListu(self,x,y,pozicija):
        procitanOdLock.acquire()
        for celija in listaCelija:
            if celija.i == x and celija.j == y:
                celija.procitanOd[pozicija]+=1
                if all(celija.procitanOd):
                    celija.semaforCelije.release()
        procitanOdLock.release()         

        


            
                


    def promenaStanja(self,ziveKomsije):
        global matrica
        global brojacCelija

        if ziveKomsije < 2 or ziveKomsije > 3:
            self.stanje = 0
            matrica[self.i,self.j]=0
        elif self.stanje == 1 and (ziveKomsije == 2 or ziveKomsije == 3):
            self.stanje = 1
            matrica[self.i,self.j]=1
        elif self.stanje == 0 and ziveKomsije == 3:
            self.stanje = 1
            matrica[self.i,self.j]=1

        brojacCelijaLock.acquire()

        brojacCelija +=1

        brojacCelijaLock.release()

        self.iteracija+=1

    def run(self):
        global brojacCelija
        
        for _ in range(0,100):
         
            ziveKomsije = self.proveraSuseda()
            self.semaforCelije.acquire()
            procitanOdLock.acquire()
            for i in range(0,8):
                self.procitanOd[i]=0
            procitanOdLock.release()
            time.sleep(0.01)
            #print(self.procitanOd)
           
            self.promenaStanja(ziveKomsije)
            #sys.stdout.write(f'{self.stanje}')
            brojacCelijaLock.acquire()
            if brojacCelija == N * N:
                brojacCelija=0
                listaMatrica.append(matrica.copy())
                brojacCelijaLock.release()
                sledecaIteracija.acquire()
                sledecaIteracija.notify_all()
                sledecaIteracija.release()

            else:
                brojacCelijaLock.release()
                sledecaIteracija.acquire()
                sledecaIteracija.wait()
                sledecaIteracija.release()    


                           
listaCelija=[]         
for i in range(0,N):
    for j in range(0,N):
        celija = Celija(matrica[i][j],i,j)
        listaCelija.append(celija)
for celija in listaCelija:
    celija.start()
for celija in listaCelija:
    celija.join()


for matrica in listaMatrica:
   print(matrica)


#for celija in listaCelija:
  #  celija.proveraSuseda()

#for celija in listaCelija:
 #   print(celija.procitanOd)
 #   print(celija.semaforCelije._value) 

   




           

