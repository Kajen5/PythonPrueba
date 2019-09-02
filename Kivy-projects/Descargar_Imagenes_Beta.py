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
        link = re.search(r'://(.*?)/(.+)', base)
        conn = htp.HTTPSConnection(link.group(1))
        print("Conexion exitosa")
        conn.request("GET", "/" + link.group(2))
        print("Pagina encontrada")
        r1 = conn.getresponse()
        data1 = r1.read().decode('utf-8')
        titulo = re.search(r'<TITLE>(.*?) - Read', data1)
        self.titu = titulo.group(1)
        print(self.titu)
        if withFile:
            self.lista = self.lista_guardada(self.titu)
        else:
            pag_padres = re.findall(
                r'(\d+\.*\d*)</a></td>\n<td><a href="(.*?)">', data1)
            print(len(pag_padres))
            print("Links padres encontrados")
            pag_padres.reverse()
            linkBase = "https://" + link.group(1)
            for pag_padre in pag_padres:
                (numero, link_padre) = pag_padre
                if not float(numero) >= start:
                    continue
                tuples = list()
                data2 = self.leyendoPagina(linkBase +
                    link_padre, 10).decode('utf-8')
                print("Pagina padre cargada -->>" + numero)
                link_imagen = re.search(
                    r'Page .*?">\n<meta property="og:image" ' +
                    r'content="(.*?)">', data2)
                tuples.append((link_imagen.group(1), str(1)))
                print((link_imagen.group(1), str(1)))
                otro = re.search(
                    r'id="page" onchange=".*?">\n<option value=".*?" ' +
                    r'selected>1</option>\n(.*?)\n</select>\n<a class="blue',
                    data2, re.DOTALL)
                otros_link = re.findall(
                    r'<option value="(.+)">\d+</option>', otro.group(1))
                hilos = []
                i = 0
                for link in otros_link:
                    hilo = th.Thread(target=self.hilo_busqueda,
                                     args=(link, hilos, tuples))
                    hilo.start()
                    hilos.append(hilo)
                    if i > 6 and i < len(otros_link) - 1:
                        hilos[i - 7].join()
                    i += 1
                    sleep(1)
                hilos[len(hilos) - 1].join()
                print("Link de imagenes cargada -->>" + numero)
                print("\n")
                self.lista.append([numero, tuples])
                self.guardar()
            print("lista de enlaces guardada")
        self.download_carpeta()
        self.comprobar()

    def hilo_busqueda(self, link, hilos, tupla):
        imagen = self.busqueda_secundaria(link)
        if int(imagen[1]) > 2:
            hilos[int(imagen[1]) - 3].join()
        print(imagen)
        tupla.append(imagen)

    def busqueda_secundaria(self, link):
        Data = self.leyendoPagina(link, 10).decode('utf-8')
        link_imagen = re.search(
            r'Page (\d+)\">\n<meta property="og:image" ' +
            'content="(.*?)">', Data)
        pag = link_imagen.group(1)
        imagen = (link_imagen.group(2), pag)
        return imagen

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

    def replace(s):
        str = ""
        for x in s:
            if x == "-5":
                str += ""
            else:
                str += x
        return str


if __name__ == '__main__':
    enlace = "https://www.taadd.com/book/Spirit+Blade+Mountain.html"
    start = 241
    Descargar(enlace, start, withFile=False)
