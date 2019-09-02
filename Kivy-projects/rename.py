import os
import re


def rename(titulo):
    directorio = os.path.join(titulo)
    if not os.path.isdir(directorio):
        os.mkdir(directorio)
    os.chdir(directorio)

    for filename in os.listdir("."):
        oldname = re.search(r"tate_no_yushaa_(\d+)-(.*?)_(\d+)-jpg", filename)
        if oldname:
            if oldname.group(2) == "5-5":
                print(filename)

                os.rename(filename, "tate_no_yushaa_" + oldname.group(1) + "-5_" +oldname.group(3) + ".jpg")
            elif oldname.group(2) == "5":
                os.rename(filename, "tate_no_yushaa_" + oldname.group(1) + "_" +oldname.group(3) + ".jpg")
            else:
                print("--->>>>>" + filename)
                os.rename(filename, "tate_no_yushaa_" + oldname.group(1) + "-1_" +oldname.group(3) + ".jpg")
        


def replace(s):
    str = ""
    for x in s:
        if x == "-5":
            str += ""
        else:
            str += x
    return str

def replace2(s):
    str = ""
    for x in s:
        if x == ".":
            str += "-"
        else:
            str += x
    return str

if __name__ == '__main__':
    rename("tate_no_yushaa")
