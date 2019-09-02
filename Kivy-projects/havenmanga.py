import http.client as htp
import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep


class Descargar():
    """docstring for ClassName"""
    titu = None
    lista = list()

    def __init__(self, base, start=0, withFile=False):
        data1 = self.leyendoPagina(base, timeout=25).decode('utf-8')
        print("Conexion exitosa")
        titulo = re.search(r'<h1 class="name bigger">(.*?)</h1>', data1)
        self.titu = self.replace(titulo.group(1))
        print("Pagina encontrada")
        print(self.titu)
        if withFile:
            self.lista = self.lista_guardada(self.titu)
        else:
            pag_padres = re.findall(
                r'2 class="chap"><a href="(.*?)">.*? (\d+\.*\d*) <span', data1)
            print("Links padres encontrados")
            pag_padres.reverse()
            hilos = []
            i = 0
            for pag_padre in pag_padres:
                (link_padre, numero) = pag_padre
                if not float(numero) >= start:
                    continue
                '''
                tuples = list()
                data2 = self.leyendoPagina(link_padre, 10).decode('utf-8')
                print("Pagina padre cargada -->>" + numero)
                link_imagen = re.search(
                    r'<center>(.*?)</center', data2, re.DOTALL)
                pag_padres = re.findall(r'src="(.*?)"', link_imagen.group(1))
                pag = 1
                for link in pag_padres:
                    imagen = (link, str(pag))
                    print(imagen)
                    tuples.append(imagen)
                    pag += 1
                print("Link de imagenes cargada -->>" + numero)
                print("\n")
                '''
                hilo = th.Thread(target=self.hilo_busqueda_all,
                                 args=(pag_padre, hilos, self.lista, i))
                hilo.start()
                hilos.append(hilo)
                if i > 6 and i < len(pag_padres) - 1:
                    hilos[i - 7].join()
                i += 1
                sleep(0.5)
            hilos[len(hilos) - 1].join()
            '''
                self.lista.append([numero, tuples])
                self.guardar()
            '''
            print("lista de enlaces guardada")
        self.download_carpeta()
        self.comprobar()

    def hilo_busqueda_all(self, Padre, hilos, tupla, i):
        link, numero = Padre
        imagen_list = self.busqueda_secundaria_all(link)
        if i > 1:
            hilos[i - 1].join()
        print("Pagina padre cargada -->>" + numero)
        for pagina in imagen_list:
            print(pagina)
        print("Link de imagenes cargada -->>" + numero)
        print("\n")
        tupla.append([numero, imagen_list])
        self.guardar()

    def busqueda_secundaria_all(self, link):
        imagen_list = list()
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        link_imagen = re.search(
            r'<center>(.*?)</center', Data, re.DOTALL)
        pag_padres = re.findall(r'src=["\'](.*?)["\']', link_imagen.group(1))
        pag = 1
        for link in pag_padres:
            imagen = (link, str(pag))
            imagen_list.append(imagen)
            pag += 1
        return imagen_list

    def leyendoPagina(self, link, timeout):
        try:
            Pagina = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            Data = urlopen(Pagina, timeout=timeout).read()
        except Exception as e:
            print("Reintentando... " + str(e))
            sleep(2)
            Data = self.leyendoPagina(link, timeout)
        return Data

    def download_carpeta(self):
        print("<<--- Comenzando descargas --->>\n")
        directorio = os.path.join(self.titu)
        if not os.path.isdir(directorio):
            os.mkdir(directorio)
        os.chdir(directorio)
        hilos = []
        cola = []
        for i in range(8):
            h = th.Thread(target=self.otro, args=(cola, ))
            hilos.append(h)
            hilos[i].start()
            sleep(3)
        for i in range(8):
            hilos[i].join()

    def otro(self, cola):
        for capitulo in self.lista:
            (numero, imagenes) = capitulo
            for imagen in imagenes:
                (link_imagen, pag) = imagen
                if link_imagen in cola:
                    continue
                cola.append(link_imagen)
                nombre = self.titu + "_" + \
                    str(numero) + "_" + str(pag) + ".jpg"
                if not os.path.isfile(nombre):
                    self.download_archivo(link_imagen, str(nombre))
                cola.remove(link_imagen)

    def download_archivo(self, url, NOMBRE):
        print("Descarga iniciada -->>\t" + NOMBRE)
        data1 = self.leyendoPagina(url, 30)
        f = open(NOMBRE, 'wb')
        f.write(data1)
        print("\t Descarga completada -->>\t" + NOMBRE)

    def guardar(self):
        f = open(self.titu + "-enlaces.txt", 'w')
        for capitulo in self.lista:
            (numero, imagenes) = capitulo
            f.write("Pagina padre cargada -->>" + numero + "\n")
            for imagen in imagenes:
                f.write(str(imagen) + "\n")
            f.write("Link de imagenes cargada -->>" + numero + "\n\n")
        f.close()
        pass

    def lista_guardada(self, nombre):
        lista = list()
        try:
            f = open(nombre + "-enlaces.txt", "r")
            text = f.read()
            pag_padres = re.findall(
                r"padre cargada -->>(\d+\.*\d*)\n(.*?)\nLink", text, re.DOTALL)
            for pag_padre in pag_padres:
                (numero, link_padres) = pag_padre
                print("Pagina padre cargada -->>" + numero)
                tuples = re.findall(r"\('(.*?)', '(\d+)'\)", link_padres)
                lista.append((numero, tuples))
                for row in tuples:
                    print(row)
                print("Link de imagenes cargada -->>" + numero)
                print("\n")
            f.close()
        except Exception as e:
            pass
        return lista

    def comprobar(self):
        i = len(os.listdir("."))
        h = sum(len(x[1]) for x in self.lista)
        print(i, h)

    def replace(self, s):
        cadena = ""
        for x in s:
            if x == ":":
                cadena += ""
            else:
                cadena += x
        return cadena


if __name__ == '__main__':
    enlace = "http://heavenmanga.org/silver-gravekeeper/page-1"
    start = 97
    Descargar(enlace, start, withFile=False)
