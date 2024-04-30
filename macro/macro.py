import fileinput
import sys
import copy
#메크로 부분 빼내기
add_call_list = []
list_macro = []

add_call_list_2 = []
add_call_list_3 = []


lines = []
def file_read():
    global lines
    with open("source.txt", 'r') as in_file, open("object.txt", 'w') as out_file:
        for line in in_file:
            out_file.write(line)

    f = open("source.txt", 'r')
    lines = f.readlines()
    lines = list(map(lambda s: s.strip(), lines))
    f.close()
    check = False
    count = 0
    for i in lines:
        if( "macro" in i):
            check = True
        if("loop" in i):
            count+=1
    return lines , check ,count
def macro_extraction(lines,check,count):
    global add_call_list
    global list_macro
    if(check):
        idx = 1
        i = lines[1]
        add_call_list.append(i)
        while i != "endm":
            i = lines[idx+1]
            add_call_list.append(i)
            idx += 1
        
        del add_call_list[len(add_call_list)-1]
        add_call_list.append("\n")
        for i in range(count):
            list_macro.append(add_call_list.copy())
    else:
        return 0
def conversion():
    for i in range(len(list_macro)):
        k = (list_macro[i])[0].replace("Lab","loop"+str(i+1))
        (list_macro[i])[0] = k
    return conversion_object(list_macro)
def conversion_2(inza,list_macro):
    inza_count = len(inza[0])
    for i in range(len(list_macro)):
        for j in range(len(list_macro[i])):
            for q in range(1,inza_count+1,1):
                if("avg"+str(q) in list_macro[i][j]):
                    k = (list_macro[i])[j].replace("avg"+str(q),(inza[i])[q-1])
                    (list_macro[i])[j] = k
    #return conversion_object_2(list_macro)
    return list_macro
#줄 관리
def k(a):
    re = ""
    count = 0
    for i in a:
        if(count == 0):
            re += "\t"+i+"\n"
            count += 1
        else:
            re += "\t\t\t   "+i + "\n"
    return re

def conversion_object(kk):
    count = 0
    number = []
    for line in fileinput.input("object.txt",inplace=True):
        if 'addcall loop' in line:
            number.append(line)
        sys.stdout.write(line)
    inza = inza_d(number)
    kk = conversion_2(inza,kk)
    for line in fileinput.input("object.txt",inplace=True):
        if 'addcall loop' in line:
            number.append(line)
            line = line.replace(line, k(kk[count]))
            count += 1
        sys.stdout.write(line)
    #last_d(inza)

#인자 관리
def inza_d(number):
    last_list = []
    inza = []
    for i in number:
        q = ""
        number_2 = list(map(lambda s: s.strip("\n"), i))
        number_3 = []
        for k in number_2:
            if(k == " "):
                pass
            else:
                number_3.append(k)
        last_list.append(number_3)

    for i in last_list:
        ppp = ""
        for j in i:
            ppp += j
        inza.append(ppp.split(","))
    for i in range(len(inza)):
        del inza[i][0]
    return inza
if __name__ == '__main__':
    
    lines, check, count = file_read()
    macro_extraction(lines,check,count)
    conversion()

