#encoding=utf-8
import tensorflow as tf
def refine_text():
    """
    将2列的去掉， 这种情况没有答案
    :return:
    """
    fw=open("Chinese_media_QA_0.txt","w",encoding="utf-8")
    fr=open("Chinese_media_QA_init.txt","r",encoding="utf-8")
    for line in fr.readlines():
        line=line.strip().split("\t")
        if len(line)==3:
            fw.write(line[0]+"\t"+line[1]+"\t"+line[2]+"\n")
    fw.close()



if __name__=="__main__":
    # refine_text()
    print(tf.__version__)
