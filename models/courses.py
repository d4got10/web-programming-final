def get_courses_info():
    return [generate_test_course(i) for i in range(1, 20)]


def generate_test_course(index):
    return {
        'id': index,
        'name': f'Курс номер {index}',
        'description': f'Это курс под номером {index}',
    }
