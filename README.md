# A-novel-Chinese-medical-QA-dataset-LiCHD-1
This is a novel Chinese medical QA dataset-(LiCHD-1)
## Introduction

Data is the soul of model, making a clean dataset needs a lot of time and manpower, but it is worthy. The investigation discovered that there are few of datasets about Chinese medical QA, [1] proposed the first public Chinese medical QA dataset, it is called [cMedQA2](https://github.com/zhangsheng93/cMedQA2). In 2017, the authors released cMedQA1. cMedQA2 is an enhanced version. In cMedQA2, it totally has 108000 questions and 203569 answers. the content in this data is mainly about disease diagnosis. The patients use a sentence to describe their symptom, and then the doctors give the relevent solution. But there are many noises in cMedQA2, we have summarized five main noises in Table1. [2] created a Chinese medical corpus ChiMed in 2019, but it isn't released. It has 46731 questions and 91416 answers. So, based on above problems, we constructed a less noise and public Chinese health question answering dataset, it mainly about the common sense of disease. In the last, 6 models are contrasted based on this dataset by toolkit MatchZoo.

## Chinese Health dataset
### Dataset's Source
To create LiCHD-1, we acquired it from a public Chinese medical forum (https://www.dxy.com/). We collected all question answer pairs based on 1228 diseases. Otherwise, this dataset is an encyclopedic QA dataset for common diseases in our live. It includes pathogeny, hazard, medication, and some points we should pay attention in daily life.
### Data Cleaning
By analysing the public Chinese medical QA ( Such as, cMedQA) and our initial dataset (scrape from web), we find that there are many noises in these dataset. We summary five typical noises in Table 1, top half refers to wrong question sample, upper half refers to right question sample (after correction). It's difficult to correct these errors by using template or other automatic methods, because each type has many wrong situations. So we clean our dataset by manually.

| Question Sample | Type |
| www | SE |
| Bayes+TF-IDF| 0.8572 |
| Bi-GRU and attention| 0.8069 |
| Transformer| 0.8343|
| Transformer+CNN| 0.8354 |
|Transformer+CNN+BiGRU| 0.8422 |



## Reference
1: ShengZhang, XinZhang, HuiWang, LixiangGuo, andShanshanLiu. [n.d.]. MultiScale Attentive Interaction Networks for Chinese Medical Question Answer Selection. IEEE Access ([n.d.]),1–1. 

2:YuanheTian, WeichengMa, FeiXia, andYanSong. 2019. ChiMed:AChinese Medical Corpus for Question Answering.In Proceedings of the 18th BioNLP Workshop and Shared Task.Association for Computational Linguistics,Florence,Italy, 250–260. https://doi.org/10.18653/v1/W19-5027 
