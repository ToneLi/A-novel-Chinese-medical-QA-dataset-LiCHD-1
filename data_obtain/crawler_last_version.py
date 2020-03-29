#encoding=utf-8
from bs4 import BeautifulSoup
import requests
import  re
"""----------爬取丁香医生上的问答数据---------"""

def get_diease_and_id(url):
    """
    获取疾病和它对应的id, 这个id是为了url进入下一级。eg:  https://dxy.com/faq/11230,   id为11230
    :param url:
    :return:
    """
    fw = open("disease_id.txt", "w", encoding="utf-8")  # 由于是循环写入所以属性不再是w了，改为a.
    r = requests.get(url)

    demo = r.text  # 服务器返回响应
    soup = BeautifulSoup(demo, "html.parser")
    # print(soup)
    trs = soup.find_all('tr')
    # print(trs)
    for tr in trs:
        tds = tr.find_all('td')
        if len(tds)!=0:
            for td in tds:
                id=td.find_all("a")
                diease_id=(id[0].get("href")) # 每个病的id
                diease=id[0].string
                print(diease)
                fw.write(diease+"\t"+diease_id+"\n")
    fw.close()
def diease_id_dic():

    with open("disease_id_quchong.txt","r",encoding="utf-8") as fr:
        DIS=[]
        ID=[]
        for line in fr.readlines():
            line=line.strip().split("\t")
            DIS.append(line[0])
            ID.append(line[1])

        dic_=dict(zip(DIS,ID))

        return dic_


def make_zifu_dic():
    s = []
    with open("zifu.txt", "r", encoding="utf-8") as fr:
        for line in fr.readlines():
            line = line.strip()
            s.append(line)
    return s


def make_chinesefigure_dic():
    s = []
    with open("chinese_figure.txt", "r", encoding="utf-8") as fr:
        for line in fr.readlines():
            line = line.strip()
            s.append(line)
    return s


def is_chinese(uchar):
 """判断一个unicode是否是汉字"""
 dic=make_zifu_dic()
 fuhao=[]
 if uchar >= u'\u4e00' and uchar <= u'\u9fa5' or uchar in dic:
  return True
 else:
  return False

def last_write(fw,question_id, QA):
    """
    给question QA的组合大段   返回 每行 对应一个问题  一个答案
    :param question_id: # 问题在QA中的id
    :param QA:
    :return:
    """


    for j in range(len(question_id)):
        if j + 1 < len(question_id):
            fw.write(key + "\t")
            QA_sentence = QA[question_id[j]:question_id[j + 1]]
            # print(QA_sentence)
            if len(QA_sentence)!=0:
                fw.write(QA_sentence[0] + "\t")
                for sen in QA_sentence[1:]:
                    fw.write(sen)
                fw.write("\n")
        else:
            # print(QA[question_id[-1]:])
            fw.write(key + "\t")
            fw.write(QA[question_id[-1]:][0] + "\t")
            for sen in QA[question_id[-1]:][1:]:
                fw.write(sen)
            fw.write("\n")
        fw.flush()



def replace_QA(fw,QA):
    QA=QA.replace("?","？")
    QA = QA.replace("？", "？||")
    chinese_figures=make_chinesefigure_dic()
    for ch in chinese_figures:

        QA = QA.replace(ch, "|")

    """-------去尾：去除尾部多余汉字说明 eg: 图片来源。。。"""
    id1 = [i for i, x in enumerate(QA) if x == "。"]
    QA=QA[:id1[-1]+1].split("|")

    """-------去头：去除尾部多余汉字说明 eg: 图片来源。。。"""
    wehao_index=[]

    for line in QA:
        if "？" in line:
            wehao_index.append(QA.index(line))
    QA=QA[wehao_index[0]:]
    QA_new=[]
    for sen in QA:
        if len(sen)==0:
            continue
        else:
            QA_new.append(sen)

    wehao_index_new = []
    for line in QA_new:
        if "？" in line:
            wehao_index_new.append(QA_new.index(line))
    last_write(fw,wehao_index_new,QA_new)



def obtain_quetion_answer(url,value):
    fw=open("Chinese_media_QA_2019927.txt","a",encoding="utf-8")

    url=url+value
    r = requests.get(url)
    demo = r.text  # 服务器返回响应
    # print(demo)
    soup = BeautifulSoup(demo, "html.parser")

    all_content=(soup.find_all("div",attrs="editor-style"))
    all_content=(all_content[0])
    QA=""

    for char in str(all_content):
        if is_chinese(char)==True:
            QA=QA+char
        else:
            continue

    # for char in str(all_content):
    #
    #     QA=QA+char
    replace_QA(fw,QA)
    fw.close()


if __name__=="__main__":
    url = "https://dxy.com/"
    # dics = {"避孕失败": "/faq/3340",'白带异常': '/faq/3867', "白月牙": "faq/3064","抽动":"/faq/4572"}#, '白带异常': '/faq/3867', "避孕失败": "/faq/3340"
    # dics = {"蛔虫病": "/faq/3317"}  # , '白带异常': '/faq/3867', "避孕失败": "/faq/3340"
    dics=diease_id_dic()
    # print(len(dics))
    i=0
    for key, value in dics.items():
        i=i+1
        print(i)
        obtain_quetion_answer(url,value)
