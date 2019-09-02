import threading
import time
import http.client
import re
from urllib.request import urlopen, Request
'''
condition = threading.Condition()
ready = False

class Person(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global ready
        condition.acquire()
  
        print("[%s] I'm waiting" % time.strftime("%H:%M:%S"))
        condition.wait()
        print("[%s] Go CiberByte!" % time.strftime("%H:%M:%S"))
        condition.release()
class Car(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global ready
        condition.acquire()
        for i in range(1):
            time.sleep(3)
        print("[%s] Car ready" % time.strftime("%H:%M:%S"))
        ready = True
        condition.notify()
        condition.release()
    
        
person = Person()
car = Car()
person.start()
car.start()
person.join()


size = 156545
fragmentos = 15
tamF = size//fragmentos
print(tamF)
ranges = [[i, i+tamF-1] for i in range (0, size, tamF)]
ranges[-1][-1]=size
pi

#Vamos a usar un diccionario compartido por los procesos, la clave será el orden que cada fragmento de bytes tiene en el archivo final.

#Lanzamos los procesos
workers = [[i,r] for i, r in enumerate(ranges)]
print (workers)




def busqueda_secundaria(link, hilos, tupla):
    Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    Data = urlopen(Pagina).read().decode('utf-8')
    link_imagen = re.search(
        r'Page (\d+)\">\n<meta property="og:image" content="(.*?)">', Data)
    pag = link_imagen.group(1)
    imagen = (link_imagen.group(2), pag)
    if int(pag) > 2:
        hilos[int(pag) - 3].join()
    print(imagen)
    tupla.append(imagen)


conn = http.client.HTTPSConnection(
        "www.taadd.com")
print("conexion establecida")
pag_padre = ("154","/chapter/TatenoYuushanoNariagari2/464661/")
(numero, link_padre) = pag_padre
tuples = list()
conn.request("GET", link_padre)
r2 = conn.getresponse()
data2 = r2.read().decode('utf-8')
print("Pagina padre cargada -->>" + numero)
link_imagen = re.search(
    r'Page .*?">\n<meta property="og:image" content="(.*?)">', data2)
tuples.append((link_imagen.group(1), str(1)))
print((link_imagen.group(1), str(1)))
otro = re.search(
    r'id="page" onchange=".*?">\n<option value=".*?" selected>1</option>\n(.*?)\n</select>\n<a class="blue', data2, re.DOTALL)
otros_link = re.findall(
        r'<option value="(.+)">\d+</option>', otro.group(1))
hilos = []
for link in otros_link:
    print(link)
    hilo = threading.Thread(target=holas, args=(link,hilos,tuples))
    hilo.start()
    hilos.append(hilo)
    time.sleep(1)
hilos[len(otros_link)-1].join()
print("Link de imagenes cargada -->>" + numero)






for i in range(h):
    print("hola",i, ranges)
    hilo = threading.Thread(target=holas, args=(i,hilos))
    hilos.append(hilo)
    hilos[i].start()




hilos[h-1].join()
print("hola")
'''
hola = [i for i in range(100)]
for h in hola:
    hola.remove(h)
print(hola)
