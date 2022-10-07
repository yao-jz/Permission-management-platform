import datetime

from typing import Any, Dict, List, Tuple, Type, Union
from django.contrib.auth import get_user_model
from django.db.models.manager import Manager
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from pytz import UTC

from application_token.models import ApplicationToken
from application_auth.models import ApplicationAuth
from application_role.models import ApplicationRole
from application_user.models import ApplicationUser
from user_role_relation.models import UserRoleRelation
from user_app_relation.models import UserApplicationRelation
from user_message.models import UserMessage, send_message as send_user_message
from utils.views import generate_json_response_dict, get_request_field, general_set_model_check, general_set_model_check_for_application
from utils.const import RequestFieldConst, JsonResponseDictConst
from utils.models import SetModelStatus
from utils.decorators import POST_only, JSON_POST, GET_only, login_needed, NeedFields, judge_from_to

from .models import Application

# Create your views here.

User = get_user_model()


class NeedApplication:
    '''
    装饰器类，用来判断使用token鉴权的时候该token是否有关联的App且能满足函数操作该App所需的权限
    '''

    def __init__(self, access_needed: ApplicationToken.ApplicationAccessStatus = ApplicationToken.ApplicationAccessStatus.SEE) -> None:
        '''
        标明view_function需要用Request参数的app_token来寻找Application，不允许该app_token没有关联Application

        如果发现没有关联的Application，返回反映相应错误的JsonResponse

        参数列表传入需要的权限，如果不满足则会返回相应的错误JsonResponse

        请保证前置修饰器有NeedFields，且传参有RequestFieldConst.APP_TOKEN，指定类型为str，否则可能出现异常

        还要保证NeedFields传参有RequestFieldConst.APP_KEY，指定类型为str

        修饰的view_function需要提供一个application参数来接受最后获取的Application实例，提供一个token_access参数来获得最后获取的token权限
        '''

        self.access_needed = access_needed

    def __call__(self, view_function):
        def need_application(*args, param_dict: Dict[str, Any], **wargs) -> JsonResponse:
            app_token = param_dict[RequestFieldConst.APP_TOKEN]
            app_key = param_dict[RequestFieldConst.APP_KEY]
            application, access = Application.get_application_by_token_string(app_token, app_key)

            if application is None:
                return JsonResponse(generate_json_response_dict(False, 'no application attached to this app_token, maybe token wrong or timed out'))
            elif not access.check_access(self.access_needed):
                return JsonResponse(generate_json_response_dict(False, f'token "{app_token}" has no enough access (provided {access}, needed {self.access_needed})'))

            return view_function(*args, **wargs, application=application, param_dict=param_dict, token_access=access)

        return need_application

def need_key_object(view_function):
    '''
    表明view_function需要request传入的key关联有某一对象，否则返回相关错误

    需要前置有指定RequestFieldConst.TYPE和RequestFieldConst.KEY的NeedFields修饰器和NeedApplication修饰器（或者传参有param_dict和application）

    被修饰的函数需要提供一个key_object参数来接受得到的非None对象
    '''

    def get_key_object(*args, param_dict: Dict[str, Any], application: Application, **wargs) -> JsonResponse:
        key_object = get_set_of_application_field_by_type(application, param_dict[RequestFieldConst.TYPE]).filter(key=param_dict[RequestFieldConst.KEY]).first()
        if key_object is None:
            return JsonResponse(generate_json_response_dict(False, f'the key "{param_dict[RequestFieldConst.KEY]}" of type "{param_dict[RequestFieldConst.TYPE].value}" belongs to no object'))
        return view_function(*args, param_dict=param_dict, application=application, key_object=key_object, **wargs)

    return get_key_object

def get_class_of_type(operate_type: RequestFieldConst.OperateType) -> Union[Type[ApplicationAuth], Type[ApplicationRole], Type[ApplicationUser], None]:
    '''
    通过OperateType获得相应的类

    如果传入参数错误，返回None
    '''

    if operate_type == RequestFieldConst.OperateType.USER:
        return ApplicationUser
    elif operate_type == RequestFieldConst.OperateType.AUTH:
        return ApplicationAuth
    elif operate_type == RequestFieldConst.OperateType.ROLE:
        return ApplicationRole
    else:
        return None

def get_manager_of_type(operate_type: RequestFieldConst.OperateType) -> Union[Manager, None]:
    '''
    通过OperateType直接获得相应ApplicationXXX类的objects

    是直接返回manager，这是为了支持函数search
    '''

    operate_class = get_class_of_type(operate_type)
    return None if operate_class is None else operate_class.objects

def get_set_of_application_field_by_type(application: Application, operate_type: RequestFieldConst.OperateType) -> Union[QuerySet, None]:
    '''
    通过OperateType和Application来获得指定App的指定关联的application_xxxs域

    由于获得operate_type的时候应该已经判断过是否合法，所以这个函数的返回值None很多时候不用再进行判断
    '''

    if operate_type == RequestFieldConst.OperateType.USER:
        return application.application_users.all()
    elif operate_type == RequestFieldConst.OperateType.AUTH:
        return application.application_auths.all()
    elif operate_type == RequestFieldConst.OperateType.ROLE:
        return application.application_roles.all()
    else:
        return None

@JSON_POST
@login_needed
def get_application_list(request: HttpRequest) -> JsonResponse:
    '''
    获得app列表（GET/POST），需要登录
   
    url: /app
   
    { }
        =>
    {
        msg: string,
        status: string,
        list: [
            {
                name: string,
                key: string,
                tokens: [
                    {
                        content: string,
                        created_time: string,
                        dead_time: string,
                        access: int,
                    }
                ],
                created_time: string,
                description: string,
            }
        ],
    }
    '''

    return JsonResponse(generate_json_response_dict(
        list = [application.to_dict() for application in request.user.applications.all()]
    ))

@NeedFields([RequestFieldConst.TYPE, RequestFieldConst.KEY], [RequestFieldConst.OperateType, str])
@need_key_object
def get_detail_objects(request: HttpRequest, application: Application, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType]], 
    key_object: Union[ApplicationAuth, ApplicationRole, ApplicationUser]):
    '''
    由get_detail调用，用于返回有type的情况（查询角色，用户或权限详情）
    '''

    return_dict = generate_json_response_dict()
    return_dict.update(key_object.to_dict())
    return JsonResponse(return_dict)

@GET_only
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY], [str, str])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.SEE)
def get_detail(request: HttpRequest, param_dict: Dict[str, str], application: Application, token_access: ApplicationToken.ApplicationAccessStatus
    ) -> JsonResponse:
    '''
    获得本身的信息（GET）

    如果不提供type域，则认为要获得App的详细信息

    url: /app/detail

    {
        app_token: string,
        app_key: string,
        type: int, ?
        key: int, ?
    }
        =>
    {
        status: string,
        msg: string,
        name: string,
        created_time: string,
        description: string, ?
        tokens: [
            {
                content: string,
                created_time: string,
                dead_time: string,
            }
        ], ?
    }
    '''

    operate_type = RequestFieldConst.get_request_type_field(request)
    if operate_type is None:
        return_dict = generate_json_response_dict()
        return_dict.update(application.to_dict(token_access=token_access))
        return JsonResponse(return_dict)
    else:
        return get_detail_objects(request, application=application)

@GET_only
@NeedFields([RequestFieldConst.TYPE, RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.FROM, RequestFieldConst.TO], [RequestFieldConst.OperateType, str, str, int, int])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.SEE)
@judge_from_to
def list_items(*args, param_dict: Dict[str, Union[RequestFieldConst.OperateType, str, int]], application: Application, **wargs) -> JsonResponse:
    '''
    获得角色，权限或用户列表（GET）

    url: /app/list

    {
        type: 0,
        app_token: string,
        app_key: string,
        from: int,
        to: int,    // [from, to)
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                name: string,
                key: string,
                created_time: string,
            }
        ]
    }
    '''

    operate_type = param_dict[RequestFieldConst.TYPE]
    from_int = param_dict[RequestFieldConst.FROM]
    to_int = param_dict[RequestFieldConst.TO]

    query_set = get_set_of_application_field_by_type(application, operate_type)

    if operate_type == RequestFieldConst.OperateType.AUTH:
        query_set = query_set.filter(parent_auth__isnull=True)

    count = query_set.count()

    if from_int >= count and count != 0:
        return JsonResponse(generate_json_response_dict(False, JsonResponseDictConst.ErrorMessage.FROM_INT_TOO_BIG))

    return JsonResponse(generate_json_response_dict(
        list = [item.to_dict() for item in query_set[from_int: to_int]]
    ))

def get_objects_lists_from_request(request: HttpRequest, application: Application
    ) -> Tuple[List[Tuple[ApplicationUser, Union[int, None]]], List[ApplicationRole], List[ApplicationAuth], str]:
    '''
    适用于attach和detach方法，解析需要操作的用户，角色，权限列表
    '''

    # pylint: disable=too-many-locals
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements

    user_details = get_request_field(request, RequestFieldConst.USER_KEYS)
    auth_details = get_request_field(request, RequestFieldConst.AUTH_KEYS)
    role_details = get_request_field(request, RequestFieldConst.ROLE_KEYS)

    msg = ''

    if user_details is None or not isinstance(user_details, list):
        msg += 'no user_keys or failed to parse;'
        user_details = []

    if auth_details is None or not isinstance(auth_details, list):
        msg += 'no permission_keys or failed to parse;'
        auth_details = []

    if role_details is None or not isinstance(role_details, list):
        msg += 'no role_keys or failed to parse;'
        role_details = []

    users = []
    auths = []
    roles = []

    for user_detail in user_details:
        if not isinstance(user_detail, dict):
            msg += f'user_info "{user_detail}" not a dict;'
            user_key = str(user_detail)
            time_out = None
        else:
            user_key = user_detail.get(RequestFieldConst.KEY, None)
            if user_key is None:
                msg += f'user_info "{user_detail}" has no key;'
                continue
            user_key = str(user_key)
            time_out = user_detail.get(RequestFieldConst.TIME_OUT, None)
            if time_out is not None:
                try:
                    time_out = int(time_out)
                except ValueError:
                    msg += f'time_out "{time_out}" not an int, so set forever;'
                    time_out = None

                if time_out < 0:
                    msg += f'time_out "{time_out}" not a positive number, so set forever;'
                    time_out = None

        user = application.application_users.filter(key=user_key).first()
        if user is None:
            msg += f'user_info "{user_detail}" fail to get user;'
            continue

        users += [(user, time_out)]

    for auth_detail in auth_details:
        if not isinstance(auth_detail, dict):
            msg += f'permission_detail "{auth_detail}" not a dict;'
            auth_key = str(auth_detail)
        else:
            auth_key = auth_detail.get(RequestFieldConst.KEY, None)
            if auth_key is None:
                msg += f'can\'t find key in permission_detail "{auth_detail}";'
                continue
            auth_key = str(auth_key)

        auth = application.application_auths.filter(key=auth_key).first()
        if auth is None:
            msg += f'permission_key "{auth_key}" fail to get permission;'
            continue

        auths += list(auth.get_childest_set())

    for role_detail in role_details:
        if not isinstance(role_detail, dict):
            msg += f'role_detail "{role_detail}" not a dict;'
            role_key = str(role_detail)
        else:
            role_key = role_detail.get(RequestFieldConst.KEY, None)
            if role_key is None:
                msg += f'role_detail "{role_detail}" has no key;'
                continue
            role_key = str(role_key)

        role = application.application_roles.filter(key=role_key).first()
        if role is not None:
            roles += [role]
        else:
            msg += f'role_key "{role_key}" fail to get role;'

    return (users, roles, auths, msg)

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY], [str, str])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.EDIT)
def attach(request: HttpRequest, application: Application, **wargs) -> JsonResponse:
    '''
    角色，用户，权限关联（POST）

    url: /app/attach

    {
        app_token: string,
        user_keys: [
            string | {
                key: string, 
                time_out: string,
            }, 
        ],
        permission_keys: [string],
        role_keys: [string],
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    users, roles, auths, warning_msg = get_objects_lists_from_request(request, application)

    for role in roles:
        role.attach_application_users(users)
        role.attach_application_auths(auths)

    return JsonResponse(generate_json_response_dict(msg=warning_msg))

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY], [str, str])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.EDIT)
def detach(request: HttpRequest, application: Application, **wargs) -> JsonResponse:
    '''
    角色，用户，权限解联（POST）

    url: /app/detach

    {
        app_token: string,
        app_key: string,
        user_keys: [string],
        permission_keys: [string],
        role_keys: [string],
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    users, roles, auths, warning_msg = get_objects_lists_from_request(request, application)

    for role in roles:
        role.detach_application_users(users)
        role.detach_application_auths(auths)

    return JsonResponse(generate_json_response_dict(msg=warning_msg))

@NeedFields([RequestFieldConst.NEW_APP_KEY], [str])
def check_app(request: HttpRequest, param_dict: Dict[str, Any], application: Application) -> JsonResponse:
    '''
    检查application改key是否可行
    '''
    app_key = get_request_field(request, RequestFieldConst.APP_KEY)
    new_app_key = param_dict[RequestFieldConst.NEW_APP_KEY]
    if app_key == new_app_key:
        return JsonResponse(generate_json_response_dict())

    general_check_result = general_set_model_check_for_application(Application, key=new_app_key)
    if general_check_result != SetModelStatus.SUCCEED:
        return JsonResponse(generate_json_response_dict(False, general_check_result.value))

    if Application.objects.filter(key=new_app_key, user=application.user).exists():
        return JsonResponse(generate_json_response_dict(False, 'key conflicts'))
    return JsonResponse(generate_json_response_dict())


@NeedFields([RequestFieldConst.TYPE, RequestFieldConst.KEY], [RequestFieldConst.OperateType, str])
def check_object(request: HttpRequest, param_dict: Dict[str, Any], application: Application) -> JsonResponse:
    '''
    检查user, role, auth改key是否可行
    '''
    operate_type = param_dict[RequestFieldConst.TYPE]
    key = param_dict[RequestFieldConst.KEY]

    general_check_result = general_set_model_check(get_class_of_type(operate_type), key=key)
    if general_check_result != SetModelStatus.SUCCEED:
        return JsonResponse(generate_json_response_dict(False, general_check_result.value))

    query_set = get_set_of_application_field_by_type(application, operate_type)
    if not query_set.filter(key=key).exists():
        return JsonResponse(generate_json_response_dict())
    else:
        return JsonResponse(generate_json_response_dict(False, 'key conflicts'))

@GET_only
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY], [str, str, RequestFieldConst.OperateType, str])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.SEE)
def check(request: HttpRequest, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType]], application: Application, **wargs) -> JsonResponse:
    '''
    改key的时候检查是否有冲突（GET）

    url: /app/check

    {
        app_token: string,
        app_key: string,
        type: int, ?
        key: string, ?
        new_app_key: string, ?
    }
        =>
    {
        msg: string,
        status: string,
    }
    '''

    operate_type = get_request_field(request, RequestFieldConst.TYPE)
    if operate_type is None:
        return check_app(request, application=application)
    else:
        return check_object(request, application=application)

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY], [str, str])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.ADD)
def delete(request: HttpRequest, application: Application, token_access: ApplicationToken.ApplicationAccessStatus, **wargs) -> JsonResponse:
    '''
    删除角色，用户，权限或者app（POST）

    如果没有type域或不合法，则认为是要删除这个app

    url: /app/delete

    {
        app_token: string,
        app_key: string,
        keys: [string], ?
        type: int, ?
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    operate_type = get_request_field(request, RequestFieldConst.TYPE)
    warning_msg = ''

    if operate_type is None:
        if not token_access.check_access(ApplicationToken.ApplicationAccessStatus.ALL):
            return JsonResponse(generate_json_response_dict(False, 'only token with access "all" can delete application'))
        application.delete()
        return JsonResponse(generate_json_response_dict())
    else:
        objects = get_set_of_application_field_by_type(application, operate_type)

    keys = get_request_field(request, RequestFieldConst.KEYS)
    if keys is None or not isinstance(keys, list):
        return JsonResponse(generate_json_response_dict(False, 'no keys or keys not a list'))
    
    for key in keys:
        objects_for_delete = objects.filter(key=str(key))
        if not objects_for_delete.exists():
            warning_msg += f'the key "{key}" found no object;'
        else:
            objects_for_delete.delete()

    return JsonResponse(generate_json_response_dict(
        msg=warning_msg
    ))

@login_needed
@NeedFields([RequestFieldConst.LIST], [list])
def add_applications(request: HttpRequest, param_dict: Dict[str, list]) -> JsonResponse:
    '''
    专用于新建应用，在add函数中调用

    不要用来接受url
    '''

    applications = param_dict[RequestFieldConst.LIST]

    return_list = []
    warning_msg = ''

    for application_info in applications:
        if not isinstance(application_info, dict):
            warning_msg += f'info: "{application_info}" is not a dict;'
            continue

        name = application_info.get(RequestFieldConst.NAME, None)
        if name is None:
            warning_msg += f'info: "{application_info}" has no attribution name;'
            continue

        name = str(name)
        description = str(application_info.get(RequestFieldConst.DESCRIPTION, ''))
        key = str(application_info.get(RequestFieldConst.APP_KEY, name))

        application, status = Application.create_application_for_user(
            user = request.user, 
            name = name, 
            description = description, 
            app_key = key,
            default_auths = [] if name == 'test' else None,
            with_status=True
        )

        if application is not None:
            application.create_token()
            return_list += [application.to_dict()]
        else:
            warning_msg += f'error in creating application with name "{name}" ({status});'

    return JsonResponse(generate_json_response_dict(
        msg = warning_msg,
        list = return_list
    ))

@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.TYPE, RequestFieldConst.LIST], [str, str, RequestFieldConst.OperateType, list])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.ADD)
def add_objects(*args, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType, list]], application: Application, **wargs) -> JsonResponse:
    '''
    专用于新建角色，用户或权限，在add函数中调用

    不要用来接受url
    '''

    operate_type = param_dict[RequestFieldConst.TYPE]
    info_list = param_dict[RequestFieldConst.LIST]

    warning_msg = ''
    return_list = []

    for info in info_list:
        if not isinstance(info, dict):
            warning_msg += f'info: "{info}" is not a dict;'
            continue

        key = info.get(RequestFieldConst.KEY, None)
        if key is None or key == '':
            warning_msg += f'info: "{info}" has no or empty key field;'
            continue

        name = info.get(RequestFieldConst.NAME, None)
        description = str(info.get(RequestFieldConst.DESCRIPTION, ''))
        parent_key = info.get(RequestFieldConst.PARENT_KEY, None)

        status, result = application.create_type(
                operate_type, str(key), name, description
            ) if parent_key is None else application.create_child_type(
                operate_type, str(key), str(parent_key), name, description
            )

        if status != SetModelStatus.SUCCEED:
            warning_msg += f'error when using info: "{info}" to create object (status: {status.value});'
            continue

        return_list += [result.to_dict()]

    return JsonResponse(generate_json_response_dict(
        msg=warning_msg,
        list=return_list
    ))

@login_needed
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.LIST], [str, str, list])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.ADMIN)
def add_application_tokens(*args, param_dict: Dict[str, Any], application: Application, token_access: ApplicationToken.ApplicationAccessStatus, **wargs) -> JsonResponse:
    '''
    专用于新建app_token，在add函数中调用

    不要用来接受url
    '''

    warning_msg = ''
    token_list = []

    for token_info in param_dict[RequestFieldConst.LIST]:
        if not isinstance(token_info, dict):
            warning_msg += f'token_info "{token_info}" could not be parsed as a dict;'
            continue

        new_token_access = token_info.get(RequestFieldConst.TOKEN_ACCESS, None)
        if new_token_access is None:
            if token_access == ApplicationToken.ApplicationAccessStatus.ALL:
                new_token_access = ApplicationToken.ApplicationAccessStatus.ADMIN
            else:
                new_token_access = ApplicationToken.ApplicationAccessStatus.ADD
            warning_msg += f'token info "{token_info}" didn\'t provide token_access, to set to {new_token_access};'
        else:
            try:
                new_token_access = ApplicationToken.ApplicationAccessStatus(int(new_token_access))
            except ValueError:
                warning_msg += f'token_access "{new_token_access}" doesn\'t make sense;'
                continue

            if not token_access.check_access(new_token_access):
                warning_msg += f'token_access "{new_token_access}" is beyond access now "{token_access}";'
                continue

        token = application.create_token(token_access=new_token_access)
        token_list += [token]

        alive_time = token_info.get(RequestFieldConst.ALIVE_TIME, None)
        if alive_time is None:
            continue

        try:
            alive_time = int(alive_time)
        except ValueError:
            warning_msg += f'alive_time "{alive_time}" not an int, so set to one week;'
            continue

        if alive_time <= 0:
            warning_msg += f'alive_time "{alive_time}" <= 0, so set to one week;'
            continue

        token.dead_time = datetime.datetime.now(UTC) + datetime.timedelta(seconds=alive_time)
        token.save()

    return JsonResponse(generate_json_response_dict(
        msg=warning_msg,
        list=[token.to_dict() for token in token_list]
    ))

@POST_only
@JSON_POST
def add(request: HttpRequest) -> JsonResponse:
    '''
    新建用户，权限，角色，应用（POST）

    如果没有app_token域，则认为是要新建一些app，此时需要用户已经登录

    如果有app_token但是没有type，则认为是要新建一些app_token，也需要用户已登录

    url: /app/add

    {
        app_token: string, ?
        type: int, ?
        list: [
            {
                name: string, ?
                key: string, ?
                description: string, ?
                parent_key: string, ?  // 标示新建子权限的时候关联的父权限
                alive_time: int, ?
                token_access: int, ?
            }
        ],
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                name: string, ?
                key: string, ?
                tokens: [string], ?
                created_time: string,
                dead_time: string, ?  // app_token的失效时间
                description: string, ?
                parent_permission: {
                    name: string,
                    key: string,
                }, ?
                tokens: [string], ?  // 如果是新建App，返回所有的token
                child_permissions: [], ?
            }
        ]
    }
    '''

    token = get_request_field(request, RequestFieldConst.APP_TOKEN)
    operate_type = get_request_field(request, RequestFieldConst.TYPE)

    if token is None:
        return add_applications(request)
    elif operate_type is None:
        return add_application_tokens(request)
    else:
        return add_objects(request)

def warp_relation_time(one: Any, another: Any, warp_dict: Union[Dict[str, Any], None] = None
    ) -> Dict[str, Any]:
    '''
    包装返回信息，使得其中含有用户和角色关联时间限制的信息

    只有当前两个参数分别为ApplicationUser和ApplicationRole类型（顺序不定）才会做事情

    应当仅用于show函数
    '''

    user, role = one, another
    if not isinstance(user, ApplicationUser):
        user, role = role, user

    if not isinstance(user, ApplicationUser) or not isinstance(role, ApplicationRole):
        return warp_dict

    return_dict = warp_dict if warp_dict is not None else dict()
    relation = UserRoleRelation.objects.filter(application_user=user, application_role=role).first()
    if relation is None:
        return return_dict

    return_dict.update({
        JsonResponseDictConst.DETACH_TIME: 'forever' if relation.forever else relation.dead_time,
    })

    return return_dict

@GET_only
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.TYPE, RequestFieldConst.WANTED_TYPE, RequestFieldConst.KEY, RequestFieldConst.FROM, RequestFieldConst.TO],
    [str, str, RequestFieldConst.OperateType, RequestFieldConst.OperateType, str, int, int])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.SEE)
@need_key_object
@judge_from_to
def show(*args, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType, int]], 
    key_object: Union[ApplicationAuth, ApplicationRole, ApplicationUser], **wargs) -> JsonResponse:
    '''
    显示用户，角色，权限的关联关系（GET）

    目标对象由app_token, type, key来定位，获得它所有的关联的want_type类型的对象数据

    url: /app/show

    {
        app_token: string,
        app_key: string,
        type: int,
        want_type: int,
        key: string,
        from: int,
        to: int,    // [from, to)
    }
    =>
    {
        status: string,
        msg: string,
        list: [
            {
                key: string,
                name: string,
                created_time: string,
                detach_time: string, ?
            }
        ]
    }
    '''

    want_type = param_dict[RequestFieldConst.WANTED_TYPE]
    from_int = param_dict[RequestFieldConst.FROM]
    to_int = param_dict[RequestFieldConst.TO]

    wanted_objects = key_object.get_objects_of_type(want_type)
    count = len(wanted_objects)

    if from_int >= count and count != 0:
        return JsonResponse(generate_json_response_dict(False, JsonResponseDictConst.ErrorMessage.FROM_INT_TOO_BIG))

    return JsonResponse(generate_json_response_dict(
        list = [warp_relation_time(key_object, item, item.to_dict()) for item in list(wanted_objects)[from_int: to_int]]
    ))

@GET_only
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.TYPE], [str, str, RequestFieldConst.OperateType])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.SEE)
def total(*args, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType]], application: Application, **wargs) -> JsonResponse:
    '''
    获取某东西的总数（GET）

    url: /app/total

    {
        app_token: string,
        app_key: string,
        type: int,
    }
        =>
    {
        msg: string,
        status: string,
        total: int,
    }
    '''

    operate_type = param_dict[RequestFieldConst.TYPE]

    return JsonResponse(generate_json_response_dict(
        total = get_set_of_application_field_by_type(application, operate_type).count()
    ))

@NeedFields([RequestFieldConst.KEY, RequestFieldConst.TYPE], [str, RequestFieldConst.OperateType])
@need_key_object
def get_object_description(request: HttpRequest, application: Application, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType]], 
    key_object: Union[ApplicationAuth, ApplicationRole, ApplicationUser]) -> JsonResponse:
    '''
    专用于获得角色，用户和权限的description

    应该只由get_description函数来调用，不可用于接受url
    '''

    return JsonResponse(generate_json_response_dict(
        content = key_object.description
    ))

@GET_only
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY], [str, str])
@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.SEE)
def get_description(request: HttpRequest, application: Application, **wargs) -> JsonResponse:
    '''
    获得description，由于可能会很长所以专门分一个（GET）

    现在先不搞那么复杂，不会返回page，也不会有分页逻辑

    url: /app/description

    {
        app_token: string,
        app_key: string,
        type: int, ?
        key: int, ?
    }
        =>
    {
        msg: string,
        status: string,
        content: string,
        page: int, ?
    }
    '''

    operate_type = get_request_field(request, RequestFieldConst.TYPE)

    if operate_type is None:
        return JsonResponse(generate_json_response_dict(
            content = application.description
        ))
    else:
        return get_object_description(request, application=application)

@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.ALL)
def edit_application(param_dict: Dict[str, Any], application: Application, **wargs) -> JsonResponse:
    '''
    专用于修改App信息

    应该由edit函数调用，不要用来接受url
    '''

    detail = param_dict[RequestFieldConst.DETAIL]

    name = detail.get(RequestFieldConst.NAME, None)
    description = detail.get(RequestFieldConst.DESCRIPTION, None)
    key = detail.get(RequestFieldConst.KEY, None)

    result = application.change_detail(name=name, description=description, user=application.user, key=key)
    if result != Application.ApplicationCheckStatus.SUCCEED:
        return JsonResponse(generate_json_response_dict(False, f'fail in changing, check status: {result}'))

    return JsonResponse(generate_json_response_dict())

@NeedApplication(access_needed=ApplicationToken.ApplicationAccessStatus.ADD)
def edit_object(request: HttpRequest, param_dict: Dict[str, Any], application: Application,
    operate_type: RequestFieldConst.OperateType, **wargs) -> JsonResponse:
    '''
    专用于修改用户，角色和权限信息

    应该由edit函数调用，不要用来接受url
    '''

    detail = param_dict[RequestFieldConst.DETAIL]

    name = detail.get(RequestFieldConst.NAME, None)
    key = detail.get(RequestFieldConst.KEY, None)
    description = detail.get(RequestFieldConst.DESCRIPTION, None)

    object_key = get_request_field(request, RequestFieldConst.KEY)
    if object_key is None:
        return JsonResponse(generate_json_response_dict(False, 'no key in detail'))

    object_key = str(object_key)
    operate_object = get_set_of_application_field_by_type(application, operate_type).filter(key=object_key).first()
    if operate_object is None:
        return JsonResponse(generate_json_response_dict(False, 'no object attached to the key in detail'))

    general_check_result = general_set_model_check(
        get_class_of_type(operate_type), name=name, key=key, description=description)
    if general_check_result != SetModelStatus.SUCCEED:
        return JsonResponse(generate_json_response_dict(False, general_check_result.value))

    warning_msg = ''

    if name is not None:
        name = str(name)
        operate_object.name = name
        operate_object.save()

    if key is not None:
        key = str(key)
        if get_set_of_application_field_by_type(application, operate_type).filter(key=key).exists():
            warning_msg += f'key "{key}" conflicted, so not changed;'
        else:
            operate_object.key = key
            operate_object.save()

    if description is not None:
        description = str(description)
        operate_object.description = description
        operate_object.save()

    return JsonResponse(generate_json_response_dict(
        msg = warning_msg
    ))

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.DETAIL], [str, str, dict])
def edit(request: HttpRequest, param_dict: Dict[str, Union[str, dict]], **wargs) -> JsonResponse:
    '''
    编辑某东西信息，采用覆盖策略（POST）

    如果没有type则认为要编辑App信息

    url: /app/edit

    {
        app_token: string,
        app_key: string,
        key: string, ?
        type: int, ?
        detail: {
            name: string, ?
            key: string, ?
            description: string, ?
        }
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    operate_type = get_request_field(request, RequestFieldConst.TYPE)
    if operate_type is None:
        return edit_application(param_dict=param_dict)
    else:
        return edit_object(param_dict=param_dict, operate_type=operate_type, request=request)

@GET_only
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.CONTENT, RequestFieldConst.TYPE, RequestFieldConst.FROM, RequestFieldConst.TO],
    [str, str, str, RequestFieldConst.OperateType, int, int])
@NeedApplication(ApplicationToken.ApplicationAccessStatus.SEE)
@judge_from_to
def search(*args, param_dict: Dict[str, Union[str, RequestFieldConst.OperateType, int]], application: Application, **wargs) -> JsonResponse:
    '''
    搜索（GET）

    url: /app/search

    {
        app_token: string,
        app_key: string,
        content: string,
        type: int,
        from: int, 
        to: int,
    }
        =>
    {
        status: string,
        msg: string,
        total: int,
        list: [
            {
                key: string,
                name: string,
                created_time: string,    
            }
        ],
    }
    '''

    operate_type = param_dict[RequestFieldConst.TYPE]
    content = param_dict[RequestFieldConst.CONTENT]
    from_int = param_dict[RequestFieldConst.FROM]
    to_int = param_dict[RequestFieldConst.TO]

    objects = get_manager_of_type(operate_type)
    search_result = objects.filter(name__icontains=content, application=application) | objects.filter(key__icontains=content, application=application)
    count = search_result.count()

    if from_int >= count and count != 0:
        return JsonResponse(generate_json_response_dict(False, JsonResponseDictConst.ErrorMessage.FROM_INT_TOO_BIG))

    return JsonResponse(generate_json_response_dict(
        total = count,
        list = [item.to_dict() for item in search_result[from_int: to_int]]
    ))

@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.APP_KEY, RequestFieldConst.APP_TOKEN, RequestFieldConst.USERNAME_SHARE, RequestFieldConst.ACCESS],
    [str, str, str, int])
@NeedApplication()
def share_application(request: HttpRequest, param_dict: Dict[str, Any], application: Application, **wargs) -> JsonResponse:
    '''
    向其他用户分享自己的App（POST），需要登录

    url: /app/share

    {
        app_token: string,
        app_key: string,
        share_username: string,
        access: int,
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    if application.user != request.user:
        return JsonResponse(generate_json_response_dict(False, 
            f'only creator can share the application ({JsonResponseDictConst.ErrorMessage.ACCESS_ERROR});'
        ))

    share_username = param_dict[RequestFieldConst.USERNAME_SHARE]

    share_user = User.objects.filter(username=share_username).first()
    if share_user is None:
        return JsonResponse(generate_json_response_dict(False, 
            f'user of username "{share_username}" doesn\'t exist ({JsonResponseDictConst.ErrorMessage.USER_NOT_FIND});'
        ))
    if share_user == application.user:
        return JsonResponse(generate_json_response_dict(False, 'don\'t share application to create user'))

    try: 
        share_access = UserApplicationRelation.UserAccessStatus(param_dict[RequestFieldConst.ACCESS])
    except ValueError:
        return JsonResponse(generate_json_response_dict(False,
            f'access doesn\'t make sense ({JsonResponseDictConst.ErrorMessage.PARSE_MESS});'
        ))

    if share_access == UserApplicationRelation.UserAccessStatus.CREATOR:
        return JsonResponse(generate_json_response_dict(False, 'highest shared access is ADMIN'))

    result = application.share(share_user, share_access)
    return JsonResponse(generate_json_response_dict(result))

@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.APP_TOKEN, RequestFieldConst.APP_KEY, RequestFieldConst.USERNAME_SHARE], 
    [str, str, str])
@NeedApplication()
def unshare_application(request: HttpRequest, param_dict: Dict[str, Any], application: Application, **wargs) -> JsonResponse:
    '''
    对特定用户取消App共享（POST），需要登录

    url: /app/unshare

    {
        app_token: string,
        app_key: string,
        share_username: string,
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    if request.user != application.user:
        return JsonResponse(generate_json_response_dict(False, 'only creator can unshare application'))

    share_username = param_dict[RequestFieldConst.USERNAME_SHARE]
    possible_user = User.objects.filter(username=share_username).first()
    if possible_user is None:
        return JsonResponse(generate_json_response_dict(False, f'username "{share_username}" doesn\'t make sense'))

    if possible_user == application.user:
        return JsonResponse(generate_json_response_dict(False, 'can\'t unshare creator'))

    unshare_result = application.unshare(possible_user)
    return JsonResponse(generate_json_response_dict(unshare_result))

@POST_only
@JSON_POST
@login_needed
def get_shared_application_list(request: HttpRequest) -> JsonResponse:
    '''
    获得所有被分享的App的列表（POST），需要登录

    url: /app/shared_list

    { }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                name: string,
                tokens: [
                    {
                        content: string,
                        created_time: string,
                        dead_time: string,
                        access: int,
                    }
                ],
                created_time: string,
                description: string,
                access: int,
            }
        ]
    }
    '''

    applications = request.user.shared_applications.all()
    return_list = [application.to_dict(user=request.user) for application in applications]

    return_list.sort(key=lambda application_dict: application_dict[JsonResponseDictConst.ACCESS])

    return JsonResponse(generate_json_response_dict(
        list = return_list
    ))

@POST_only
@JSON_POST
@NeedFields([RequestFieldConst.APP_KEY, RequestFieldConst.APP_TOKEN], [str, str])
@NeedApplication()
def get_user_group(*args, application: Application, **wargs) -> JsonResponse:
    '''
    获取用户组（POST）

    url: /app/user_group

    {
        app_key: string,
        app_token: string,
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                name: string,
                avatar: string,
                access: int,
            }
        ]
    }
    '''

    return JsonResponse(generate_json_response_dict(
        list = application.get_user_group()
    ))

@POST_only
@JSON_POST
@login_needed
@NeedFields([RequestFieldConst.APP_KEY, RequestFieldConst.APP_TOKEN, RequestFieldConst.MESSAGE, RequestFieldConst.TO_USERNAME], 
    [str, str, str, str])
@NeedApplication()
def send_message(request: HttpRequest, param_dict: Dict[str, Any], application: Application, **wargs) -> JsonResponse:
    '''
    向同组的用户发送信息（POST），需要登录

    url: /app/send_message

    {
        app_key: string,
        app_token: string,
        message: string,
        to_username: string,
        title: string, ?
    }
        =>
    {
        status: string,
        msg: string,
    }
    '''

    to_username = param_dict[RequestFieldConst.TO_USERNAME]
    to_user = User.objects.filter(username=to_username).first()
    if to_user is None:
        return JsonResponse(generate_json_response_dict(False, f'no user named "{to_username}"'))

    title = get_request_field(request, RequestFieldConst.TITLE)
    if title is not None:
        title = str(title)

    if application.get_user_access(to_user) == UserApplicationRelation.UserAccessStatus.NO:
        return JsonResponse(generate_json_response_dict(False, f'user named "{to_username}" doesn\'t manage the application'))

    message = param_dict[RequestFieldConst.MESSAGE]
    user_message, check_status = UserMessage.create_message(request.user, to_user, message, application, title)
    if check_status != UserMessage.MessageCheckStatus.SUCCEED:
        return JsonResponse(generate_json_response_dict(False, f'message error, status: {check_status.value}'))

    send_user_message(user_message)
    return JsonResponse(generate_json_response_dict())
