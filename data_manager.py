import random
import pandas as pd

TEST_MODE = False
TOTAL = 60
MARK = '2018-06-01-zhongyuan-bank'

result_pre = 'data/zhongyuan_bank.csv'
result_pre = result_pre.replace('.csv', '')

result_src = '{}.csv'.format(result_pre)
output_src = '{}-{}.csv'.format(result_src, MARK)
result_test = '{}-test.csv'.format(result_pre)

RIGHT = 'right'
WRONG = 'wrong'
UNSURE = 'unsure'
IGNORE = 'ignore'

marked_indices = set()

result = pd.read_csv(result_src)

if TEST_MODE: result = result[:15]

indices = set(range(len(result)))

questions = result['input'].values
topn = 20
topn_results = [None] * topn

RIGHT_FIELD = 'right'

result[RIGHT_FIELD] = UNSURE

for i in range(topn):
    field = 'top' + str(i)
    topn_results[i] = result[field].values


def get_sample_result():
    print('len(unmarked_indices) == {}'.format(len(indices)))

    random_index = random.choice(list(indices)) if indices else None

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

    print(finished_num)
    print(qid)

    if qid is None or finished_num >= TOTAL:
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
            'total': TOTAL,
            'current': finished_num+1,
            'right': RIGHT,
            'wrong': WRONG,
        }

    return info


def mark_result(qid, mark, right_id=None):
    global result_src

    assert mark in (RIGHT, WRONG, UNSURE, IGNORE)

    if mark == RIGHT:
        assert right_id is not None, 'when mark is right, right id cannot be none'

    result[RIGHT_FIELD][qid] = right_id if mark == RIGHT else mark

    output = result_test if TEST_MODE else output_src

    result.to_csv(output, index=False)
    if qid in indices:
        indices.remove(qid)

    print('set result')
