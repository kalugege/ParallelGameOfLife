import numpy as np
import multiprocessing as mp
import queue
import time

N = 4
brojCelija = mp.Value('i',0)
matrica=np.random.randint(2,size=(N,N))
brojCelijaCondition = mp.Condition()
class Celija(mp.Process):
    def __init__(self,stanje,i,j,brojCelija,redPoruka,brojCelijaCondition):
        super().__init__()
        self.stanje=stanje      
        self.i=i
        self.j=j
        self.iteracija=0
        self.brojCelija=brojCelija
        self.stanjeKomsija = mp.Queue()
        self.redPoruka=redPoruka
        self.brojCelijaCondition=brojCelijaCondition
    
    
    def proveraSuseda(self):
        for x in range(self.i - 1, self.i + 2):
            for y in range(self.j - 1, self.j + 2):
                if x == self.i and y == self.j:
                    continue
                
                if x<0 or x>= N:
                    x=x % N
                if y < 0 or y>=N:
                    y = y % N
                self.azurirajQueue(x,y)    

    def azurirajQueue(self,x,y):
        for celija in listaCelija:
            if celija.i == x and celija.j == y:
                celija.stanjeKomsija.put(self.stanje)

    def promenaStanja(self,ziveKomsije):
        global matrica
        
        if ziveKomsije < 2 or ziveKomsije > 3:
            self.stanje = 0
            
        elif self.stanje == 1 and (ziveKomsije == 2 or ziveKomsije == 3):
            self.stanje = 1
           
        elif self.stanje == 0 and ziveKomsije == 3:
            self.stanje = 1
            

        
        
        
        self.iteracija+=1 
        self.redPoruka.put((self.i,self.j,self.iteracija,self.stanje))

    def run(self):
        for _ in range(0,4):
            self.proveraSuseda()
            ziveKomsije=0
            for _ in range(0,8):
                ziveKomsije+=self.stanjeKomsija.get()
            time.sleep(0.1)
            self.promenaStanja(ziveKomsije)

           
            with brojCelija.get_lock():
                self.brojCelija.value+=1
            if self.brojCelija.value == N * N:
                # self.brojCelija.get_lock().acquire()
                # self.brojCelija.value=0
                # self.brojCelija.get_lock().release() 
                with brojCelija.get_lock():
                    self.brojCelija.value=0  
                
                
                self.brojCelijaCondition.acquire()
                self.brojCelijaCondition.notify_all()
                self.brojCelijaCondition.release()

            else:
                
                self.brojCelijaCondition.acquire()
                self.brojCelijaCondition.wait()
                self.brojCelijaCondition.release()    


        
class Servis(mp.Process):
    def __init__(self,matrica,redPoruka,listaMatrica):
        super().__init__()
        self.matrica=matrica
        self.redPoruka=redPoruka
        self.listaMatrica=listaMatrica                    

    def run(self):
        for _ in range(0,4):
            for _ in range(0,N*N):
                poruka = self.redPoruka.get()
                
                self.matrica[poruka[0],poruka[1]]=poruka[3]

            self.listaMatrica.append(matrica.copy())     

        for m in listaMatrica:
           print(m)

redPoruka = mp.Queue()
listaMatrica=[]
servis=Servis(matrica,redPoruka,listaMatrica)
servis.start()

listaCelija=[]         
for i in range(0,N):
    for j in range(0,N):
        celija = Celija(matrica[i,j],i,j,brojCelija,redPoruka,brojCelijaCondition)
        listaCelija.append(celija)     
 
for celija in listaCelija:
    celija.start()
for celija in listaCelija:
    celija.join()


servis.join()                      


