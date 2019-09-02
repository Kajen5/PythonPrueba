import os
from PIL import Image
import re




def lista_guardada(nombre):
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


def otro(titulo):
    lista = lista_guardada(titulo)
    directorio = os.path.join(titulo)
    if not os.path.isdir(directorio):
        os.mkdir(directorio)
    os.chdir(directorio)
    i = 0
    n = 0
    lista2 = []
    new_im = Image.new('RGB', (728, 1035))
    for capitulo in lista:
        (numero, imagenes) = capitulo
        for imagen in imagenes:
            (link_imagen, pag) = imagen
            nombre = titulo + "_" + \
                str(numero) + "_" + str(pag) + ".jpg"
            i += 1
            outfile = titulo + "_" + str(n) + ".pdf"
            lista2 += nombre
            new_im += Image.open(str(nombre))
            new_im.save(outfile, "PDF", Quality=100, save_all=True)
            if i > 500:
                i = 0
                n += 1
                new_im = Image.new('RGB', (728, 1035))
                new_im.save(outfile, "PDF", Quality=100, save_all=True,
                    append_images=[Image.open(nombre) for nombre in lista2])
    new_im.save(outfile, "PDF", Quality=100, save_all=True)
if __name__ == '__main__':
    otro("tate_no_yushaa")