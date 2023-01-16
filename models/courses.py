def get_popular_courses_info(count):
    return [generate_test_course(i) for i in range(1, count + 1)]


def get_course_info(id):
    return generate_test_course(id)


def generate_test_course(index):
    return {
        'id': index,
        'name': f'Курс номер {index}',
        'description': f'Это описание шикарного курс под номером {index}. Проходите не пожалеете!',
    }
