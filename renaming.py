import os
import PyPDF2
import enchant
d = enchant.Dict("en_US")

def split_word(word):
    if(len(word)<30):
        for e in d.suggest(word):
            z = list(word)
            y = list(e)
            if ' ' in y:
                y.remove(' ')
            if (y == z and y!='' and z!=''):
                return e
            else:
                return word
                break

for folder in sorted(os.listdir("/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/")):
    if(not(folder.isdigit()) or not(int(folder)==1978)):
        continue
    print("Looking in year:" + folder)
    f_no = int(folder)
    for filename in sorted(os.listdir("/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/"+folder+"/")):
        try:
            if filename.endswith(".pdf"):
                print("Old PDF Name:",filename)
                pdf_file = open("/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/"+folder+"/"+filename, 'rb')
                read_pdf = PyPDF2.PdfFileReader(pdf_file)
                number_of_pages = read_pdf.getNumPages()

                page = read_pdf.getPage(0)

                page_content = page.extractText()
                words=page_content.split(" ")
                #print(words)
                title=[]
                z=[]
                a=[]
                title.append(str(f_no))
                g = -1


                for i in range(0,len(words)):
                    a = list(words[i])
                    a = [" " if not(m.isalnum()) else m for m in a ]
                    words[i] = ''.join(e for e in a if e.isalnum())
                if '' in words:
                    words.remove('')
                special_words=['METHODS','THEORY','ISSUES','SPECIAL','EDITORS','ERRATA','EDITORIAL','RESEARCH']
                '''for i in range(0, len(words)):
                    for j in special_words:
                        if (j.lower() in words[i].lower()):
                            g = i;
                            break
                    if(g>=0):
                        break'''
                if(g<0):
                    g=0


                z=[]
                y=[]
                #print(words)
                #l=len(words)
                for i in range(0,len(words)):
                    #print(words[i])
                    if(words[i]==''):
                        continue
                    if("By" in words[i]):
                        break
                    if(not(d.check(words[i]))):
                        #print(words[i]," can be ",d.suggest(words[i]))
                        y = split_word(words[i])
                        #print(y)
                        if(y!=None):
                            words[i]=y
                #print(words)
                for i in range(0,len(words)):
                    if " " in words[i]:
                        y,z=words[i].split(' ')
                        words[i]=z
                        words.insert(i,y)
                #print(words)






                title.append(words[g])


                if(title[1].upper()=='METHODS'):
                    title.append("ARTICLE")
                    title.append(words[g+1][7:])
                    g+=1
                elif(title[1].upper()=='THEORY'):
                    title.append("AND")
                    title.append("ARTICLE")
                    title.append(words[g+2][7:])
                    g += 1
                elif(title[1].upper()=='ISSUES'):
                    title.append("AND")
                    title.append("OPINIONS")
                    title.append(words[g+2][8:])
                    g += 1
                elif (title[1].upper() == 'SPECIAL'):
                    title.append("ISSUE")
                    title.append(words[g+1][5:])
                    g += 1
                elif(title[1].upper()=='EDITORS'):
                    title.append("COMMENTS")
                    title.append(words[g+1][8:])
                    g += 1
                elif (title[1].upper() == 'ERRATA'):
                    title.append("NOTES")
                    title.append(words[g+1][5:])
                    g += 1
                elif (title[1].upper() == 'EDITORIAL'):
                    title.append("INTRODUCTION")
                    title.append(words[g+1][12:])
                    g += 1
                elif (title[1].upper() == 'RESEARCH'):
                    if(words[g+1][0].upper()=="A"):
                        title.append("ARTICLE")
                        title.append(words[g+1][7:])
                        g += 1
                    if (words[g+1][0].upper() == "E"):
                        title.append("ESSAY")
                        title.append(words[g+1][5:])
                        g += 1
                    if (words[g+1][0].upper()== "N"):
                        title.append("NOTE")
                        title.append(words[g+1][4:])
                        g += 1
                for i in range(len(title)+g-1,len(words)):
                    if(words[i]==''):
                        continue
                    if ("1" in words[i] or i>15 or "By" in words[i]):
                        break
                    title.append(words[i])


                if(("By" in words[i] and words[i]!='By') or ("1" in words[i])):
                    z=[]
                    w=words[i]
                    w = list(w)
                    for j in range(0,len(w)):
                        if(not(w[j].isalpha()) or (w[j]=="B" and w[j+1]=="y") or w[j]=="1"):
                            break
                        z.append(w[j])
                    z=''.join(z)
                    if(d.check(z)):
                        z=split_word(z)
                        w = list(z)
                        for i in range(0,len(w)):
                            if(w[i]==" "):
                                w[i]="_"
                        z = ''.join(w)

                    title.append(z)

                if (title[0] == "ERRATA" or title[0] == "EDITORS"):
                    title = title[0:2]
                if (len(title)>20):
                    title = title[0:20]
                title='_'.join(f for f in title if f!='')
                print("New PDF name: ",title,".pdf")



                os.rename("/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/"+folder+"/"+filename, "/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/"+folder+"/"+title+".pdf")

        except IndexError:
            print("IndexError")
            continue
        except ValueError:
            print("ValueError")
            title[0]=folder
            title='_'.join(title)
            os.rename("/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/" + folder + "/" + filename,
                      "/Users/vijayvishwakarma/Desktop/MIS Quarterly Renamed copy/" + folder + "/" + title + ".pdf")
            continue
        except TypeError:
            print("TypeError")
            continue
        except OSError:
            print("OSError")
            continue

