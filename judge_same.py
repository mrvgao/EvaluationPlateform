from collections import defaultdict
from itertools import combinations

kinds_map = {
    (101, 121): 0,
    (2121, 123124, 341): 1,
    (12341, 453, 1231): 2,
    (99090, 534, 123): 3,
    (11, ): 4
}

category_id_map = {}  # init  a dictionary

for category, ids in kinds_map.items():
    for q in category: category_id_map[q] = ids


def sort_list(L):
    ranked = defaultdict(list)

    for qids in L:
        for _id in qids:
            ranked[category_id_map[_id]].append(_id)

    ranked_list = [ranked[kind] if ranked[kind] != [] else [None]
                   for kind in range(len(kinds_map))]

    # ranked_list = [sorted(qids) for qids in ranked_list]

    return ranked_list


def judege_list_is_same(list1, list2):
    assert len(list1) == len(list2)

    for l1, l2 in zip(list1, list2):
        override = set(l1).issubset(set(l2)) or set(l2).issubset(set(l1))
        if l1 == l2 or override:
            pass
        else:
            # print(l1, l2)
            return False

    return True


some_qids = [[101, ], [12341, ], [2121, 341]]
some_qids_2 = [[101, ], [2121, ], [12341, ]]

# print(sort_list(some_qids))
# print(sort_list(some_qids_2))

qids1 = sort_list(some_qids)
qids2 = sort_list(some_qids_2)

# print(judege_list_is_same(qids1, qids2))

case1 = [ [101], [2121], [12341], [123]]
caes2 = [ [101], [2121,341], [12341], [123]]
case3 = [ [101], [12341], [123]]


def f(c1, c2): return judege_list_is_same(sort_list(c1), sort_list(c2))


assert f(case1, caes2)
assert not f(caes2, case3)
assert not f(case1, case3)


def get_list(*L):
    return [[e] if not isinstance(e, list) else e for e in L]


print('test done!')

case1 = get_list(101, 2121, 12341, 123)
caes2 = get_list(101, [2121,341], 12341, 123)
case3 = get_list(101, 12341, 123)
c1 = get_list(101,2121,12341,123)
c2 = get_list(101,2121,12341)
c3 = get_list(101,2121,12341,11)
c4 = get_list([101,121],341,12341,121)

case1, case2, case3 = (case1, 'case1'), (caes2, 'case2'), (case3, 'case3')
c1 = (c1, 'c1')
c2 = (c2, 'c2')
c3 = (c3, 'c3')
c4 = (c4, 'c4')

for t1, t2 in combinations([case1, case2, case3, c1, c2, c3, c4], r=2):
    v1, n1 = t1
    v2, n2 = t2
    equal = f(v1, v2)
    print("{} {}= {}".format(n1, '=' if equal else '!', n2))
