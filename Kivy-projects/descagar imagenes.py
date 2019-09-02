
import http.client
import re
import os
from urllib.request import urlopen, Request
import threading as th
from time import sleep
'''
from StringIO import StringIO


   Se descarga la imagen y se almacena en una cadena

URL = 'http://www.url.com/img/imagen.jpg'
data = urlopen(URL).read()

   Se convierte a fichero con StringIO y luego se convierte en imagen

file = StringIO(data)
img = Image.open(file)

   Se almacena en disco

img.save('/home/img/imagen.jpg')

    conn.request("GET", "/manga/Tales%20of%20demons%20and%20gods.html")
    r1 = conn.getresponse()
    data1 = r1.read().decode('utf-8')
    tuples = re.findall(
        r'(\d+)\.5</a>\n.+\n.+\n.+\n.+\n<a href="(.+)" target="_blank">10</a>', data1)
    print(len(tuples))
    titulo = re.search(
        r'<div class="ttline"><h1>(.+) chapter</h1>', data1).group(1)
    for capitulo in tuples:
        (numero, link_pag, ) = capitulo
        conn.request(
        "GET", link_pag)
        r2 = conn.getresponse()
        data2 = r2.read().decode('utf-8')
        link_imagenes = re.findall(r'" alt="(.+) Page (\d+)">', data2)
        otra = re.search(
        r'" selected>1/\d+</option>\n(.*?)\n</select>\n</div>\n<div class="share">', data2, re.DOTALL   )
        print(otra.group(1))

        lista.append(numero,link_imagenes)

    otro = re.search(
        r'" selected>1/\d+</option>\n(.*?)\n</select>\n</div>\n<div class="share">', data2, re.DOTALL   )
    for  otra:
        conn.request(
            "GET", otra.group(1))
        r2 = conn.getresponse()
        data2 = r2.read().decode('utf-8')
        tuples += re.findall(r'" alt="(.+) Page (\d+)">', data2)
    for imagen in imagenes:
        for
        (link, pag )= imagen

 '''


def hola(nombre):
    lista = []
    #f = open(nombre + "-enlaces.txt", "r")
    pag_padres = re.findall(
        r"Pagina padre cargada -->>(\d+\.*\d*)\n(.*?)\nLink", text, re.DOTALL)
    for pag_padre in pag_padres:
        (numero, link_padres) = pag_padre
        print("Pagina padre cargada -->>" + numero)
        tuples = re.findall(r"\('(.*?)', '(\d+)'\)", link_padres)
        lista.append((numero, tuples))
        for row in tuples:
            print(row)
        print("Link de imagenes cargada -->>" + numero)
        print("\n")
    # f.close()
    return lista


def revisar():
    titulo = "Star Martial God Technique"
    lista = hola(titulo)
    
    conn = http.client.HTTPSConnection(
        "www.taadd.com")
    print("Conexion exitosa")
    '''
    conn.request("GET", "/book/TATE+NO+YUUSHA+NO+NARIAGARI.html")
    print("Pagina encontrada")
    r1 = conn.getresponse()
    data1 = r1.read().decode('utf-8')
    print("Pagina cargada")
    pag_padres = re.findall(
        r'(\d+\.*\d*)</a></td>\n<td><a href="(.*?)">', data1)
    print(len(pag_padres))
    print("Links padres encontrados")
    pag_padres.reverse()
    for pag_padre in pag_padres:
        (numero, link_padre) = pag_padre
        print(numero)
        if not float(numero) == 9:
            continue
        
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
        if otro:
            i = 2
            otros_link = re.findall(
                r'<option value="(.+)">\d+</option>', otro.group(1))
            print(len(otros_link))
            for link in otros_link:
                conn.request("GET", link)
                r2 = conn.getresponse()
                data2 = r2.read().decode('utf-8')
                link_imagen = re.search(
                    r"pic' name='comicpic' src=\"(.*?)\" onerror=", data2)
                tuples.append((link_imagen.group(1), str(i)))
                print((link_imagen.group(1), str(i)))
                i += 1
        print("Link de imagenes cargada -->>" + numero)
        print("\n")
        lista.append([numero, tuples])
    print(lista)
    '''
    guardar(titulo, lista)
    
    print("lista de enlaces guardada")
    #download_carpeta(titulo, lista)
  


def replace(s):
    str = ""
    for x in s:
        if x == ".":
            str += "-"
        else:
            str += x
    return str


def download_carpeta(titulo, lista):
    print("<<--- Comenzando descargas --->>\n")
    directorio = os.path.join(titulo)
    if not os.path.isdir(directorio):
        os.mkdir(directorio)
    os.chdir(directorio)
    hilos = []
    cantidad = 10
    for i in range(cantidad):
        h = th.Thread(target=otro, args=(titulo, lista))
        hilos.append(h)
        hilos[i].start()
        sleep(3)
    for i in range(cantidad):
        hilos[i].join()
    print("-->> Descargas Terminadas <<--")


def otro(titulo, lista):
    for capitulo in lista:
        (numero, imagenes) = capitulo
        for imagen in imagenes:
            (link_imagen, pag) = imagen
            imagenes.remove(imagen)
            nombre = titulo + "_" + str(numero) + \
                "_" + str(pag)
            nombre = replace(nombre) + ".jpg"
            if not os.path.isfile(nombre):
                # download_archivo(link_imagen, str(nombre))
                download_archivo(link_imagen, str(nombre))


def download_archivo(url, NOMBRE):
    # link = re.search(r'://(.*?)/(.*?)', url)
    # conn = http.client.HTTPSConnection(link.group(1))
    # conn.request("GET", "/" + link.group(2))
    # r2 = conn.getresponse()
    ''' furl.set_proxy('localhost:1234', 'http')'''
    try:
        print("Descarga iniciada -->>\t" + NOMBRE)
        furl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        data1 = urlopen(furl).read()
        f = open(NOMBRE, 'wb')
        f.write(data1)
        print("\t Descarga completada -->>\t" + NOMBRE)
    except:
        print("Reintentando...")
        download_archivo(url, NOMBRE)
    # f.write(r2.read())


def guardar(titulo, lista):
    f = open(titulo + "-enlaces.txt", 'w')
    for capitulo in lista:
        (numero, imagenes) = capitulo
        f.write("Pagina padre cargada -->>" + numero + "\n")
        for imagen in imagenes:
            f.write(str(imagen) + "\n")
        f.write("Link de imagenes cargada -->>" + numero + "\n\n")
    f.close()
    pass


if __name__ == '__main__':
    revisar()
