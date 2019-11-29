from functools import wraps
# from flask_sqlalchemy import Pagination
import flask_restful

success_result = 'success', 200


class Api(flask_restful.Api):

    def handle_error(self, e):
        # flask_restful的错误处理功能不好用
        # 而且还会拦截掉错误导致flask的错误处理器不起作用
        # 所以将错误直接上抛至flask来处理
        raise e


def result_formatter(*args):
    def formatter(*data):

        if len(data) == 1:
            data = data[0]
            # if isinstance(data, Pagination):
            #     return {
            #         'status': 200,
            #         'message': 'success',
            #         'data': data.items,
            #         'total': data.total,
            #         'has_next': data.has_next,
            #         'page': data.page,
            #         'pages': data.pages,
            #     }
            return {'data': data, 'status': 200, 'message': 'success'}

        if len(data) == 2:
            first, second = data
            if isinstance(first, int) and isinstance(second, str):
                return {'status': first, 'message': second}
            elif isinstance(first, str) and isinstance(second, int):
                return {'status': second, 'message': first}
            else:
                raise TypeError('Unexpected types')

        elif len(data) == 3:
            data, status, message = data
            # TODO 判断类型
            return {'data': data, 'status': status, 'message': message}

    if callable(args[0]):
        # 作为装饰器使用
        func = args[0]
        @wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            # 函数本意是返回单个对象，但返回的又是元组的情况不考虑
            return formatter(*ret) \
                if isinstance(ret, tuple) else formatter(ret)
        return wrapper

    else:
        # 直接传入数据
        return formatter(*args)


def str_to_bool(arg: str) -> bool:
    '''当字符串为TRUE, true, True, 1的时候，返回True'''
    if isinstance(arg, str):
        return arg.lower() in ('true', '1')
    return bool(arg)
