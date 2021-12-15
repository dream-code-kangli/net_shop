import jsonpickle


def getLoginUserInfo(request):
    """获取用户登录对象信息"""
    user = request.session.get('user', '')

    if user:
        user = jsonpickle.loads(user)
    return {'loginUser': user}
