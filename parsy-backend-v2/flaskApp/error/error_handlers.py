class BadRequest(Exception):
    status_code = 400
    body = {'err_msg': 'Bad request'}


class ValidationFailed(Exception):
    status_code = 401
    body = {'err_msg': 'Validation failed'}


class NotFound(Exception):
    status_code = 404
    body = {'err_msg': 'Not found'}
