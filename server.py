from bottle import get, post, template, run, request, response
from data_manager import get_random_result, mark_result


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
    choose = request.forms.get('choose')
    right_id = request.forms.get('right', type=int)
    mark_result(answer_id, choose, right_id)
    print(choose)

    info = get_random_result(finished_num=current)

    if info:
        return template(INDEX, info)
    else:
        return template(RESULT)


run(host='0.0.0.0', port=9999)
