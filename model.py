import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import model_from_json

json_file = open("model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("model.h5")


def predict(s, mot, model = model):
    data = pd.read_csv("dataAnnotated.csv", encoding="utf-8")
    data = data.fillna(method="ffill")
    words = list(set(data["Word"].values))
    tags = list(set(data["Tag"].values))
    tag2idx = {t: i + 1 for i, t in enumerate(tags)}
    tag2idx["PAD"] = 0
    idx2tag = {i: w for w, i in tag2idx.items()}

    max_len = 75
    max_len_char = 20
    chars = set([w_i for w in words for w_i in w])
    char2idx = {c: i + 2 for i, c in enumerate(chars)}
    char2idx["UNK"] = 1
    char2idx["PAD"] = 0
    ind = s.find(mot)
    s1 = s[:ind]
    s1 = s1.split(" ")[:-1]
    s2 = s[ind+len(mot):]
    s2 = s2.split(" ")[1:]
    s = s1+[mot]+s2
    sentence = s
    sent_seq = []
    for i in range(max_len):
        word_seq = []
        for j in range(max_len_char):
            try:
                word_seq.append(char2idx.get(sentence[i][j]))
            except:
                word_seq.append(char2idx.get("PAD"))
        sent_seq.append(word_seq)
    x_char_test = np.array([sent_seq])
    for w in s:
        if w not in words:
            words.append(w)
    word2idx = {w: i + 2 for i, w in enumerate(words)}
    word2idx["UNK"] = 1
    word2idx["PAD"] = 0
    idx2word = {i: w for w, i in word2idx.items()}
    chars = set([w_i for w in words for w_i in w])
    char2idx = {c: i + 2 for i, c in enumerate(chars)}
    char2idx["UNK"] = 1
    char2idx["PAD"] = 0
    x_test_sent = pad_sequences(sequences=[[word2idx[w] for w in s]],
                                padding="post", truncating='post', value=word2idx["PAD"], maxlen=max_len)
    tmp_word = x_test_sent
    tmp_char = x_char_test
    p = model.predict([tmp_word, tmp_char.reshape((len(tmp_char), max_len, max_len_char))])
    p = np.argmax(p[0], axis=-1)
    for w, pred in zip(tmp_word[0], p):
        if w != 0:
            if idx2word[w] == mot:
                return idx2tag[pred]
    return "";