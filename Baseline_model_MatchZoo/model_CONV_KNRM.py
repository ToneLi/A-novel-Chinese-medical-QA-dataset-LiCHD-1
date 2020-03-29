#encoding=utf-8
import matchzoo as mz
import  pandas as pd
import csv
import datetime
task=mz.tasks.Ranking()

#OK! let's begin! In the first you should download this toolkit in https://github.com/NTMC-Community/MatchZoo

def _read_data(path):
    table = pd.read_csv(path, sep='\t', header=0, quoting=csv.QUOTE_NONE)
    df = pd.DataFrame({
        'text_left': table['Question'],
        'text_right': table['Sentence'],
        # 'id_left': table['QuestionID'],
        # 'id_right': table['SentenceID'],
        'label': table['Label']
    })
    return mz.pack(df)


#
# print(train_raw.left)
# print(train_raw.right)
# print(train_raw.relation.head())
# print(train_raw.frame().head())

def configure_model():


    """
    emb = mz.embedding.load_from_file(mz.datasets.embeddings.EMBED_CPWS)
    this function is to reload  the Chinese vector matrix,
    for emb: step:
    1: download the Chinese word embedding, put it in this dic:
    this mine:E: \Anaconda3\Lib\site-packages\MatchZoo-2.2.0-py3.6.egg\matchzoo\datasets\embeddings
    2: add one code in \Anaconda3\Lib\site-packages\MatchZoo-2.2.0-py3.6.egg\matchzoo\datasets\embeddings\__init__.py:
                    EMBED_CPWS = DATA_ROOT.joinpath('sgns.baidubaike.txt')
    """
    emb = mz.embedding.load_from_file(mz.datasets.embeddings.EMBED_CPWS)
    #model
    model_class = mz.models.ConvKNRM
    #reload the embedding
    model, preprocessor, data_generator_builder, embedding_matrix = mz.auto.prepare(
        task=task,
        model_class=model_class,
        data_pack=train_raw,
        embedding=emb
    )

    return model, preprocessor, data_generator_builder, embedding_matrix




if __name__=="__main__":
    """
    # the style of  "train_wikistype.tsv" and "train_wikistype.tsv" a shown in the next
    Question	Sentence	Label
    how are glacier caves formed?	A partly submerged glacier cave on Perito Moreno Glacier .	0
    how are glacier caves formed?	The ice facade is approximately 60 m high	0
    how are glacier caves formed?	Glacier caves are often called ice caves , but this term is proper	0
    How are the directions of..	In physics , circular motion is a movement of an object along the	0
    How are the directions of.	It can be uniform, with constant angular rate of rotation (and consta	0
    """
    begin=datetime.datetime.now()
    train_path = "train_wikistype.tsv"
    test_path = "test_wikistype.tsv"

    train_raw = _read_data(train_path)
    test_raw = _read_data(test_path)
    model, preprocessor, data_generator_builder, embedding_matrix=configure_model()
    #adjust parameter
    # model.params['mlp_num_units'] = 3
    model.params['with_embedding'] = True
    # model.params['dropout_rate'] = 0.5
    #there are six  #evaluation metrics,
    model.params['task'].metrics = [#mz.metrics.AveragePrecision(threshold=1),
                                    # mz.metrics.Precision(k=2, threshold=2),
                                    # mz.metrics.DiscountedCumulativeGain(k=2),
                                    mz.metrics.MeanReciprocalRank(),
                                    mz.metrics.MeanAveragePrecision(),
                                    mz.metrics.NormalizedDiscountedCumulativeGain(k=1),
                                    mz.metrics.NormalizedDiscountedCumulativeGain(k=5),
                                    mz.metrics.NormalizedDiscountedCumulativeGain(k=10)
                                    ]

    print(model.params)  # to show the parameters which can be adjusted
    s=preprocessor.context  # check the size of dic, such as vocab_size': 13, 'embedding_input_dim': 13, 'input_shapes': [(30,), (30,)
    train_processed = preprocessor.transform(train_raw)
    test_processed = preprocessor.transform(test_raw)

    #generate trainset
    x, y = train_processed.unpack()
    #generate testset
    test_x, test_y = test_processed.unpack()
    model.build()
    model.compile()


    model.fit(x, y, batch_size=128, epochs=4)
    #evaluate model
    b=model.evaluate(test_x, test_y)
    print(b)
    end = datetime.datetime.now()

    print("运行时间为：",(end-begin).seconds)