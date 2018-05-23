from bottle import get, post, template, run, request, response
from data_manager import get_random_result, mark_result
from data_manager import WRONG, RIGHT


INDEX = 'templates/index.html'
RESULT = 'templates/finish.html'


@get('/')
def get_page():
    """Home Page"""
    info = get_random_result()

    if info:
        return template(INDEX, info)
    else:
        return template(RESULT)


@post('/collect')
def post_result():
    answer_id = request.forms.get('answer_id', type=int)
    current = request.forms.get('current', type=int)
    if request.forms.get('choose') == RIGHT:
        mark_result(answer_id, right=True)
        print('right')
    elif request.forms.get('choose') == WRONG:
        mark_result(answer_id, right=False)
        print('wrong')

    info = get_random_result(finished_num=current)

    if info:
        return template(INDEX, info)
    else:
        return template(RESULT)


run(host='0.0.0.0', port=9999)
