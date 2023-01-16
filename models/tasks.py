def get_task_list(course_id, count):
    return [generate_task(course_id, i) for i in range(1, count + 1)]


def generate_task(course_id, index):
    return {
        'id': index,
        'description': f'Описание задания под номером {index} для курса {course_id}',
        'task_type': 'single',
        'answers': ['Вариант ответа 1', 'Вариант ответа 2', 'Вариант ответа 3', 'Вариант ответа 4'],
        'correct_answer': [2]
    }