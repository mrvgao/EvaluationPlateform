import random
import pandas as pd

MARK = '2018-05-23-03-tst-all-question'

result_pre = 'data/result_100'
result_src = '{}.csv'.format(result_pre)
output_src = '{}-{}.csv'.format(result_src, MARK)
result_test = '{}-test.csv'.format(result_pre)

RIGHT = 'right'
WRONG = 'wrong'
UNSURE = 'unsure'

marked_indices = set()

result = pd.read_csv(result_src)

test_mode = False

if test_mode:
    result = result[:15]

indices = set(range(len(result)))

questions = result['input'].values
models = result['model'].values
topn = 20
topn_results = [None] * topn

for i in range(topn):
    field = 'top' + str(i)
    topn_results[i] = result[field].values


def get_sample_result():
    print('len(unmarked_indices) == {}'.format(len(indices)))

    if len(indices) > 0:
        random_index = random.choice(list(indices))
    else:
        random_index = None

    print('random index is: {}'.format(random_index))
    return random_index


def get_candidates_by_index(index):
    return [topn_results[i][index] for i in range(topn)]


def _get_random_result():
    index = get_sample_result()

    if index is None:
        return (None, ) * 4
    else:
        question = questions[index]
        model = questions[index]
        candidates = get_candidates_by_index(index)

        return index, question, model, candidates


def get_random_result(finished_num=0):
    qid, question, model, candidates = _get_random_result()

    total = 50
    print(finished_num)
    print(qid)

    if qid is None or finished_num >= total:
        info = None
    else:
        candidates_set = set()
        pure_candidates = []
        for c in candidates:
            if c not in candidates_set:
                pure_candidates.append(c)
                candidates_set.add(c)

        info = {
            'question': question,
            'answers': pure_candidates,
            'answer_id': qid,
            'model': model,
            'total': total,
            'current': finished_num+1,
            'right': RIGHT,
            'wrong': WRONG,
        }

    return info


def mark_result(qid, mark):
    global result_src

    assert mark in (RIGHT, WRONG, UNSURE)

    result['right'][qid] = mark

    output = result_test if test_mode else output_src

    result.to_csv(output, index=False)
    if qid in indices:
        indices.remove(qid)

    print('set result')
