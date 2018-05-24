from gensim.models.keyedvectors import KeyedVectors, Vocab
from numpy import float32 as REAL
import numpy as np
import time


class XiaoMGensim(KeyedVectors):
    '''
    The augmented version of gensim.
    Which could read words and word's vector form memory.

    Author: Minquan Gao minchiuan.gao@gmail.com
    Date: 2018-May-24
    '''

    def __init__(self):
        super().__init__()

    @classmethod
    def load_word2vec_from_words_and_ndarray(cls, words, matrix):
        """
        :param words: the words list, could be ['I', 'am', 'a', 'boy']
        :param matrix: matrix shape is len(words) * vector-size
        :return: the word2vec model.
        """
        assert len(words) == matrix.shape[0]

        vocab_size = matrix.shape[0]
        vector_size = matrix.shape[1]
        result = cls()
        result.vector_size = vector_size
        result.syn0 = np.zeros((vocab_size, vector_size), dtype=REAL)

        def add_word(word, weights):
            word_id = len(result.vocab)
            if word in result.vocab:
                return
            result.vocab[word] = Vocab(index=word_id, count=vocab_size - word_id)
            result.syn0[word_id] = weights
            result.index2word.append(word)

        for w, vector in zip(words, matrix):
            add_word(w, list(map(REAL, vector)))

        return result


if __name__ == '__main__':
    _words = ['但是', '我', '也', '不', '知道']

    def s2l(s): return list(map(REAL, s.split()))

    assert s2l('1 0 0 0 0') == [1., 0., 0., 0., 0.]

    _matrix = """1 0 0 0 0
    1 0 0 0 1
    1 0 0 0 2
    1 0 0 0 3
    2 0 0 0 4""".split('\n')

    _matrix = np.array([s2l(line) for line in _matrix], dtype=REAL)

    assert _matrix.shape == (5, 5)
    print(_matrix)

    start = time.time()
    m_model = XiaoMGensim.load_word2vec_from_words_and_ndarray(words=_words, matrix=_matrix)
    print('load vector from mdarray used time: {}'.format(time.time() - start))

    start = time.time()
    model = KeyedVectors.load_word2vec_format(fname='/Users/kouminquan/Workspaces/IBM/EvaluationPlateform/data/mock_w2v.vec')
    print('load vector from file used time: {}'.format(time.time() - start))

    # np.testing.assert_array_equal(model.wv['但是'], m_model.wv['但是'])
    assert model.wv.most_similar('但是') == \
           m_model.wv.most_similar('但是')

    print('used time: {}'.format(time.time() - start))
    print('test done!')