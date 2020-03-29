# A-novel-Chinese-medical-QA-dataset-LiCHD-1
This is a novel Chinese medical QA dataset-(LiCHD-1)
## Introduction

Data is the soul of model, making a clean dataset needs a lot of time and manpower, but it is worthy. The investigation discovered that there are few of datasets about Chinese medical QA, [1] proposed the first public Chinese medical QA dataset, it is called [cMedQA2](https://github.com/zhangsheng93/cMedQA2). In 2017, the authors released cMedQA1. cMedQA2 is an enhanced version. In cMedQA2, it totally has 108000 questions and 203569 answers. the content in this data is mainly about disease diagnosis. The patients use a sentence to describe their symptom, and then the doctors give the relevent solution. But there are many noises in cMedQA2, we have summarized five main noises in Table1. [2] created a Chinese medical corpus ChiMed in 2019, but it isn't released. It has 46731 questions and 91416 answers. So, based on above problems, we constructed a less noise and public Chinese health question answering dataset, it mainly about the common sense of disease. In the last, 6 models are contrasted based on this dataset by toolkit MatchZoo.

## Chinese Health dataset
### Dataset's Source
To create LiCHD-1, we acquired it from a public Chinese medical forum (https://www.dxy.com/). We collected all question answer pairs based on 1228 diseases. Otherwise, this dataset is an encyclopedic QA dataset for common diseases in our live. It includes pathogeny, hazard, medication, and some points we should pay attention in daily life.
### Data Cleaning
By analysing the public Chinese medical QA ( Such as, cMedQA) and our initial dataset (scrape from web), we find that there are many noises in these dataset. We summary five typical noises in the below, top half refers to wrong question sample, upper half refers to right question sample (after correction). It's difficult to correct these errors by using template or other automatic methods, because each type has many wrong situations. So we clean our dataset by manually.

|wrong| Question Sample | Type|
| ------ | ------ | ------ |
|1| 胸闷气短感觉憋的上用力呼气胸痛 | SE |
|2| 我这是痔疮还是脱肛？我这是痔疮还是脱肛？| SR  |
|3| 发病持续时间：一年以上| WQ |
|4| 金锁固精丸，，可以治疗早泄吗，，，，| PE|
|5| 中医能治疗截瘫吗（h5class=""f12f14mt20""）| WN |
|right|||
|1|胸闷气短，感觉憋的上，用力呼气胸痛| SE|
|2|我这是痔疮还是脱肛？| SR |	
|3| "----------" |WQ|
|4| 金锁固精丸可以治疗早泄吗？ | PE |
|5|中医能治疗截瘫吗？|	WN|

Note: Five typical noises in public Chinese medical question answer. SE refers to "segment error", SR refers to "sentence repetition", WQ refers to "wrong question" (delete it), PE refers to "punctuation error", WN refers to "web noise"

### Dataset Generation
We follow the rules about existing QA dataset, such as HealthQA, cMedQA, etc. A QA dataset should not only have positive QA pairs, but also need some negative QA pairs. This form can help model have enough discriminative power to give points to each answer that relate to their question and improve robustness. Hence, we sampled some negative data samples of QA pairs, for each question, the negative answers are chosen by below ways:

* <font color=#7FFF00 size=3>Irrelevant negative answers:</font> In order to make the model have a high level of discrimination. We sample some very low relevance to question. In our dataset, the QA pairs are divided by disease, so a question's negative answer is about other disease.
	
	
* Partially relevant answers: these answers and positive answer have the same disease, but they have not the same question. Otherwise, we also consider: (1) overlapping words; (2) question and answer have the same topic, but they are not positive QA pair. [3] and [4] used such samples in the training progress, it make model have a high discriminative power, as compared to the model use randomly choose negitive sample.

To create a high-quality QA dataset, we hired seven workers, include: undergraduate, graduate, doctor, IT coder. These people are ensured to be very careful, patient and have good Chinese skills. They were intructed to clean the data and generate dataset. In the progress of generating dataset, works were ask to ensure one question at least one positive answer, the number of irrelevant negative answers and  partially relevant answers is greater than 0, one answer have 30 candicate questions (relevant, irrelevant, partially relevant). The statistics of the LiCHD-1 are shown in the below.
	     	
| items | Count|
| ------ | ------ |
|Number of answers| 27296 |
|Number of questions|27170 |
|Number of diseases| 1228 |
|Average length of questions (in characters)|14.75|
|Average length of answers (in characters)| 133.80|
|The size of Trainset|659862 |
|The size of Testset|82413 |
|The size of Devset|81661 |
## Experiments
### Compared Models

* DRMM [5]: This model encodes the local interaction between query and document to Matching Histogram Mapping which is inputted in feed forward network. At last, the authors use cosine similarity to compute the relevant between query and document semantic representation. More specially, they use a term gating network to clarify the importance of the query term.

* MV-LSTM [6]: This model uses Bi-LSTM to generate the sentence representation of question and answer, and then use a Interaction Tensor to compute the interaction information between them. This information finally passes a K-Max Pooling and MLP layer to compute the relevant score.

* ANMM [7]: This model first uses a QA Matching Matrix to compute the interaction information bewteen question embedding and answer embedding. It also uses the attention mechanism, and then combines the interaction feature to compute the final relevent score. More specially, they adopted a value-shared weighting scheme to combine the different matching score.

* DUET [8]:  This model uses two separate deep neural networks to represent the query and document, and then use Hadamard Product to compute the relevance feature. More specially, the anthors reuse CNN to learn the potential information of relevanve feature.

* KNRM [9]: It was proposed in 2017, the anthors used Kernel Pooling layer to generate the ranking feather for the text, at last this method used soft-TF feature to compute the final similarity score. 

* CONV-KNRM [10]: This method can complete n-gram soft matches, and use a cross-match layer to learn the interaction information between answer and question. the method of computing the relevent score is same as KNRM.

|Model name| MRR|NDCG@1|NDCG@5|NDCG@10|
| ------ | ------ |------ |------ |------ |
|DRMM| 0.9627|0.6081|0.7653|0.7917|
|MV-LSTM| 0.9446|0.5344|0.7020|0.7437|
|ANMM| 0.7748|0.4493|0.5483|0.5537 |
|DUET| 0.8391|0.4893|0.5505|0.6157|	
|KNRM| 0.7110|0.3106|0.4595|0.5492|
|CoNV-KNRM| 0.9044|0.5411|0.6714|0.729|







## References
1: ShengZhang, XinZhang, HuiWang, LixiangGuo, andShanshanLiu. [n.d.]. MultiScale Attentive Interaction Networks for Chinese Medical Question Answer Selection. IEEE Access ([n.d.]),1–1. 

2: YuanheTian, WeichengMa, FeiXia, andYanSong. 2019. ChiMed:AChinese Medical Corpus for Question Answering.In Proceedings of the 18th BioNLP Workshop and Shared Task.Association for Computational Linguistics,Florence,Italy, 250–260. https://doi.org/10.18653/v1/W19-5027 

3: MingZhu, AmanAhuja, WeiWei, and ChandanK.Reddy.2019. A Hierarchical Attention Retrieval Model for Healthcare Question Answering. In The World Wide Web Conference, WWW2019, SanFrancisco, CA, USA, May13-17,2019.2472–2482. https://doi.org/10.1145/3308558.3313699 

4: JiangWang, YangSong, ThomasLeung, ChuckRosenberg, JingbinWang, James Philbin, BoChen, andYingWu.2014. Learning Fine-Grained Image Similarity with Deep Ranking. In 2014 IEEE Conference on Computer Vision and Pattern Recognition, CVPR 2014, Columbus, OH, USA, June 23-28, 2014.1386–1393. https: //doi.org/10.1109/CVPR.2014.180 

5: JiafengGuo, YixingFan, QingyaoAi, and W.BruceCroft.2016.A Deep Relevance Matching Model for Ad-hocRetrieval.

6:  ShengxianWan, YanyanLan, JiafengGuo,JunXu, LiangPang, and XueqiCheng. [n.d.]. A Deep Architecture for Semantic Matching with Multiple Positional Sentence Representations. ([n.d.]).

7:  YangLiu, QingyaoAi, JiafengGuo, and W.BruceCroft. 2016. aNMM: Ranking Short Answer Texts with Attention-Based Neural Matching Model.Inthe 25th ACM International. 

8: Bhaskar Mitra, Fernando Diaz, and Nick Craswell. [n.d.]. Learning to Match Using Local and Distributed Representations of Text for WebSearch. ([n.d.]). 

9: Chenyan Xiong, Zhuyun Dai, Jamie Callan, Zhiyuan Liu, and Russell Power. [n.d.]. End-to-End Neural Ad-hocRanking with Kernel Pooling. ([n.d.]). 

10: ZhuyunDai, Chenyan Xiong,JamieCal lan, and Zhiyuan Liu.2018.Convolutional Neural Networks for  Soft-MatchingN-Gram sin Ad-hocSearch.InProceedings of the Eleventh ACM International Conference on Web Search and Data Mining, WSDM 2018, Marina Del Rey, CA, USA, February 5-9, 2018.126–134.

