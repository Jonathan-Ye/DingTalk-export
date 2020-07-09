#针对4.7日后钉钉更新
import os

def getfilename():
    path = os.getcwd()#获取当前路径
    print("当前文件路径：{}".format(path))
    all_files = [f for f in os.listdir(path )]#输出根path下的所有文件名到一个列表中
    #对各个文件进行处理
    print("当前路径所有文件：{}".format(all_files))
    return(all_files)



def processfile(filename):
    name=[]             #学生姓名
    bm=[]               #部门
    livetime=[]         #直播观看时长
    reviewtime=[]       #回看观看时长
    looksumtime=[]      #观看总时长
    sumtime=''          #直播总时长
    percentage=0
    s=[]
    file=open('%s'%filename,encoding='utf-16')
    for line in file:
        line=line.replace("\n","")
        line=line.replace("\t",",")
        s.append(line)
    for i in range(len(s)):
        s[i]=s[i].split("\t")
    s[3]=s[3][0].split(",")
    sumtime=s[3][2]         #获取直播总时长
    sumtime=sumtime.split(":")
    sumtime=sumtime[1]      #单位分钟

    #删除前7行无用数据
    for i in range(7):
        del(s[0])
    
    for i in range(len(s)):
        s[i]=s[i][0].split(",")
    
    #导入各项数据，提取学生，关键字为“家校通讯录”
    #时间单位为分
    for i in range(len(s)):
        if "家校通讯录" in s[i][4]:
            name.append(s[i][2])
            bm.append(s[i][4])
            if s[i][5]=="未参与":
                print("名单中直播时长不合法！")
                os.system("pause")
                exit()
            s[i][5]=s[i][5].split(":")
            livetime.append(s[i][5][1])
            if s[i][6]=="未参与":
                reviewtime.append('未参与')
            else:
                s[i][6]=s[i][6].split(":")
                reviewtime.append(s[i][6][1])
            s[i][7]=s[i][7].split(":")
            looksumtime.append(s[i][7][1])
    
    addalldata(name,livetime,reviewtime,looksumtime,sumtime,filename)


    latedata=[]
    lateline=''
    latenum=getlatenum(sumtime,looksumtime)
    for i in latenum:
        percentage=int(looksumtime[i])/int(sumtime)*100
        percentage=str(percentage)
        lateline=name[i]+","+livetime[i]+","+reviewtime[i]+","+looksumtime[i]+","+percentage[0:4]
        latedata.append(lateline)
    for i in range(len(latedata)):
        latedata[i]=latedata[i].split(",")

    return(sumtime,latedata)



#获得时长不足学生的位次
def getlatenum(sumtime,looksumtime):
    latenum=[]
    for i in range(len(looksumtime)):
        if int(looksumtime[i])<int(sumtime)*0.75:
            latenum.append(i)
    return(latenum)


def creatfile(classname,latedata,sumtime):

    print("正在创建新文件...")

    newfile=open("时长不足学生名单.csv",'a')
    newfile.write(classname +'\n')
    newfile.write("课程直播总时长：%s            单位：分钟"%sumtime+"\n")
    info="姓名,直播时长,回看时长,观看总时长,百分比"
    newfile.write(info +"\n")
    for item in latedata:
        newfile.write(",".join(item)+"\n")
    newfile.write("\n")
    newfile.write("\n")
    newfile.write("\n")
    print("已添加！")



def addalldata(name,livetime,reviewtime,looksumtime,sumtime,filename):
    global datalist
    global num
    global classlist
    classlist.append(filename+"，课程直播时长："+sumtime+"分")
    percent=0
    if num==0:
        for i in range(len(name)):
            percent=str(int(looksumtime[i])/int(sumtime)*100)
            dataline=name[i]+","+livetime[i]+","+reviewtime[i]+","+looksumtime[i]+","+percent[0:4]+","
            datalist.append(dataline)
    else:
        for i in range(len(name)):
            for j in range(len(datalist)):
                temp=datalist[j].split(",")
                if name[i]==temp[0]:
                    percent=str(int(looksumtime[i])/int(sumtime)*100)
                    dataline=datalist[j]+","+livetime[i]+","+reviewtime[i]+","+looksumtime[i]+","+percent[0:4]+","
                    datalist[j]=dataline




def creatsumfile(classlist,datalist):
    sumfile=open("汇总表格.csv",'w')
    info="直播时长,回看时长,观看总时长,百分比,,"
    for i in range(len(classlist)):
        sumfile.write(","+classlist[i]+",,,,")
    sumfile.write("\n")
    for i in range(len(classlist)):
        if i==0:
            sumfile.write("姓名,直播时长,回看时长,观看总时长,百分比,,")
        else:
            sumfile.write(info)
    sumfile.write("\n")

    #写入数据
    for item in datalist:
        sumfile.write(item)
        sumfile.write("\n")




#主程序！！！
latedata=[]
num=0
allfilename=getfilename()
sumtime=0
datalist=[]
classlist=[]


#判断文件中是否已存在该文件
if "时长不足学生名单.csv" and "汇总表格.csv" in allfilename:
    print("{:=^65}".format(""))
    print("{}".format("请手动删除“时长不足学生名单.csv”和“汇总表格.csv”，再尝试运行程序！"))
    print("{:=^65}".format(""))
    print("{:=^58}".format("程序即将退出！"))
    os.system("pause")
    exit()

for i in allfilename:
    if i=="main.py":
        continue
    else:
        sumtime,latedata=processfile(i)
        creatfile(i,latedata,sumtime)
        num=num+1
        print("“{}”已导出成功！".format(i))
creatsumfile(classlist,datalist)
print("\n")
if num==len(allfilename)-1:
    print("全部导出成功！")
    print('汇总名单已导出至“汇总表格.csv”。时长不足学生名单已导出至“时长不足学生名单.csv”。共计{}门课程。'.format(num))
else:
    print("可能导出失败，请检查后重试。")
print("如要再次运行此程序，请删除“时长不足学生名单.csv”和“汇总表格.csv”")
print("{:=^43}".format(""))
print("{0:=^40}".format('by:叶乔楠'))
print("{:=^43}".format(""))
os.system("pause")
