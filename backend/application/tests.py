import json
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.urls import reverse
from pytz import UTC

from application_auth.models import ApplicationAuth
from application_user.models import ApplicationUser
from application_role.models import ApplicationRole
from utils.models import SetModelStatus
from utils.const import JsonResponseDictConst, RequestFieldConst, TestConst

from .models import Application

# Create your tests here.

User = get_user_model()


def dict_in_dict(dict1: dict, dict2: dict) -> bool:
    for key, value in dict1.items():
        if key != 'created_time' and not (key in dict2.keys() and value == dict2[key]):
            return False
    return True

def test_no_token(self, method: str, other_keys: dict) -> None:
    self.assertIn(method, ['get', 'post'])
    method = Client().get if method == 'get' else Client().post
    response = method(self.url, other_keys)
    self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

def test_wrong_token(self, method: str, other_keys: dict) -> None:
    self.assertIn(method, ['get', 'post'])
    method = Client().get if method == 'get' else Client().post
    other_keys.update({RequestFieldConst.APP_TOKEN: self.app_token + '~'})
    response = method(self.url, other_keys)
    self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

def prebuild(self: TestCase, username: str, password: str, application_name: str, url_for_reserve: str = '', app_key: str = '', application_description: str = '',
    user_num: int = 0, role_num: int = 0, auth_num: int = 0) -> None:
    if not app_key:
        app_key = application_name
    self.client = Client()
    self.username = username
    self.password = password
    self.user = User.objects.create_user(username=self.username, password=self.password)
    self.application_name = application_name
    self.app_key = app_key
    self.application_description = application_description
    self.application = Application.create_application_for_user(
        user = self.user,
        name = self.application_name,
        description = application_description,
        app_key = app_key,
        default_auths = []
    )
    self.app_token = self.application.create_token().content
    if url_for_reserve:
        self.url = reverse(url_for_reserve)

    self.application_user = []
    self.application_auth = []
    self.application_role = []

    for i in range(user_num):
        self.application_user.append(self.application.create_type(
            operate_type=RequestFieldConst.OperateType.USER,
            key=str(i),
            name=str(i) + '号选手',
            description=str(i) + '号选手'
        )[1])

    for i in range(role_num):
        self.application_role.append(self.application.create_type(
            operate_type=RequestFieldConst.OperateType.ROLE,
            key=str(i),
            name=str(i) + '号角色',
            description=str(i) + '号角色'
        )[1])

    for i in range(auth_num):
        self.application_auth.append(self.application.create_type(
            operate_type=RequestFieldConst.OperateType.AUTH,
            key=str(i),
            name=str(i) + '号权限',
            description=str(i) + '号权限'
        )[1])


class LoginTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.username = 'login_test'
        self.password = 'login_test'
        self.application_user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.url = reverse('root:login')

    def test_successful_login(self) -> None:
        response = self.client.post(self.url, {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password,
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

    def test_failed_login(self) -> None:
        response = self.client.post(self.url, {
            RequestFieldConst.USERNAME: self.username[1:],
            RequestFieldConst.PASSWORD: '',
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_get_method(self) -> None:
        response = self.client.get(self.url, {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password,
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_no_password(self) -> None:
        response = self.client.post(self.url, {
            RequestFieldConst.USERNAME: self.username
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_no_user(self) -> None:
        response = self.client.post(self.url, {
            RequestFieldConst.PASSWORD: self.password
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)


class LogoutTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.username = 'logout_test'
        self.password = '114514'
        self.url = reverse('root:logout')
        self.client = Client()
        self.application_user = User.objects.create_user(username=self.username, password=self.password)

    def test_logout_using_get_method(self) -> None:
        self.client.post(reverse('root:login'), {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password
        })
        response = self.client.get(self.url)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

    def test_logout_without_login(self) -> None:
        response = self.client.post(self.url)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_logout_with_new_login_method(self) -> None:
        response = self.client.post(self.url, {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password,
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)


class RegisterTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse('root:register')
        self.username = 'register_test'
        self.password = '114514'

    def test_username_or_password_empty(self):
        response = Client().post(self.url, {
            RequestFieldConst.USERNAME: '',
            RequestFieldConst.PASSWORD: self.password
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        response = Client().post(self.url, {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: ''
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_duplicated_username(self):
        response = Client().post(self.url, {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        response = Client().post(self.url, {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)


class ApplicationListTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.username = 'application_list_test'
        self.password = 'application_list_test'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.application_name = 'test_application'
        self.application = Application.create_application_for_user(self.user, self.application_name)
        self.client = Client()
        self.url = reverse('application:list')

    def test_not_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_login(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.url)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)


class ApplicationTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            application_name='test',
            user_num=0,
            role_num=0,
            auth_num=0
        )

    def test_crashed_application_name(self) -> None:
        self.assertNotEqual(self.application, None)
        self.assertEqual(Application.create_application_for_user(self.user, 'test'), None)

    def test_get_application_by_token(self) -> None:
        token = self.application.create_token()
        self.assertEqual(Application.get_application_by_token_string(token.content, self.app_key)[0], self.application)

    def test_token_time_out(self) -> None:
        token = self.application.create_token()
        self.assertEqual(Application.get_application_by_token_string(token.content, self.app_key)[0], self.application)
        token.dead_time = datetime.datetime.now(UTC) - datetime.timedelta(seconds=1)
        token.save()
        self.assertEqual(Application.get_application_by_token_string(token.content, self.app_key)[0], None)

    def test_application_auth(self) -> None:
        test_auth_status, test_auth = self.application.create_auth('test')
        self.assertEqual(test_auth_status, SetModelStatus.SUCCEED)
        self.assertNotEqual(test_auth, None)
        self.assertEqual(test_auth, self.application.application_auths.first())
        self.test_auth = test_auth

        test_auth_status, test_auth = self.application.create_auth('test')
        self.assertEqual(test_auth_status, SetModelStatus.KEY_ALREADY_EXISTS)
        self.assertEqual(test_auth, None)

        # def test_child_auths(self) -> None:
        child_auth_status, test_child_auth = self.test_auth.create_child_auth('test_child')
        self.assertEqual(child_auth_status, SetModelStatus.SUCCEED)
        self.assertNotEqual(test_child_auth, None)
        self.assertEqual(test_child_auth, self.test_auth.child_auths.first())
        self.assertEqual(test_child_auth.parent_auth, self.test_auth)

        # def test_cascade_delete(self) -> None:
        self.application.delete()
        self.assertEqual(None, Application.objects.filter(name='application').first())
        self.assertEqual(None, ApplicationAuth.objects.filter(name='test').first())
        self.assertEqual(None, ApplicationAuth.objects.filter(name='test_child').first())


class DetailTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            application_name='test',
            app_key='ghfjsjkf',
            url_for_reserve='application:detail',
            user_num=10,
            role_num=10,
            auth_num=10
        )

    def test_no_token(self):
        response = Client().get(self.url, {})
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_wrong_token(self):
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token + '~',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_wrong_app_key(self):
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key + '~'
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_right_token(self):
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

    def test_wrong_user_key(self):
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: 11,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_wrong_auth_key(self):
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: -1,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_wrong_role_key(self):
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEY: 100,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_right_user_key(self):
        test_key = 2
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: test_key,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(
            dict_in_dict(self.application_user[test_key].to_dict(), response.json()), True)

    def test_right_auth_key(self):
        test_key = 0
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: test_key,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertTrue(
            dict_in_dict(self.application_auth[test_key].to_dict(), response.json()))

    def test_right_role_key(self):
        test_key = 9
        response = Client().get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEY: test_key,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertTrue(
            dict_in_dict(self.application_role[test_key].to_dict(), response.json()))


class ListTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            application_name='test',
            app_key='hsdfjsdlk',
            url_for_reserve='application:list_items',
            user_num=10,
            role_num=10,
            auth_num=10
        )

    def test_app_token(self):
        other_keys = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.FROM: 0,
            RequestFieldConst.TO: 2,
            RequestFieldConst.APP_KEY: self.app_key
        }
        test_no_token(self, 'get', other_keys)
        test_wrong_token(self, 'get', other_keys)

    def test_out_of_range_or_empty_range(self):
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.FROM: -1,
            RequestFieldConst.TO: 0,
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.FROM: 10,
            RequestFieldConst.TO: 11,
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.FROM: 4,
            RequestFieldConst.TO: 3,
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_str_range(self):
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER,
            RequestFieldConst.FROM: 'rg',
            RequestFieldConst.TO: 1,
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE,
            RequestFieldConst.FROM: 2,
            RequestFieldConst.TO: 'xz',
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_right_input(self):
        from_int, to_int = 0, 10
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.FROM: from_int,
            RequestFieldConst.TO: to_int,
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        for i in range(from_int, to_int):
            self.assertEqual(dict_in_dict(self.application_user[i].to_dict(), response.json()['list'][i - from_int]), True)

        from_int, to_int = 3, 7
        data = {
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.FROM: from_int,
            RequestFieldConst.TO: to_int,
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        }
        response = Client().get(self.url, data)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        for i in range(from_int, to_int):
            self.assertEqual(dict_in_dict(self.application_user[i].to_dict(), response.json()['list'][i - from_int]), True)


class AttachTestCase(TestCase):
    
    # url: /app/attach

    def setUp(self) -> None:
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            application_name='test',
            app_key='56896789fghj',
            url_for_reserve='application:attach',
            user_num=10,
            role_num=10,
            auth_num=10
        )
        self.user_keys_str = RequestFieldConst.USER_KEYS
        self.auth_keys_str = RequestFieldConst.AUTH_KEYS
        self.role_keys_str = RequestFieldConst.ROLE_KEYS

    def test_get_method(self) -> None:
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: '[]',
            self.auth_keys_str: '[]',
            self.role_keys_str: '[]',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(JsonResponseDictConst.FAIL, response.json()[JsonResponseDictConst.STATUS])

    def test_mess_input(self) -> None:
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: 'sofsdpff2',
            self.auth_keys_str: '****',
            self.role_keys_str: 'fsdfsdl',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])

        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: ["sfsdkk"],
            self.auth_keys_str: [[1, 2]],
            self.role_keys_str: '[]',
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])

        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: 'vsdfslfslv',
            self.auth_keys_str: '[',
            self.role_keys_str: '',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])

        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: 'vsdv',
            self.auth_keys_str: [{}, 1, 'kskkf'],
            self.role_keys_str: [-1, '9999', 9999],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])

    def test_succeed(self) -> None:
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: [0, 1],
            self.auth_keys_str: [1, 2],
            self.role_keys_str: [0, 2, 3],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        role = ApplicationRole.objects.get(application=self.application, key='0')
        self.assertTrue(role.users.all().exists())
        self.assertTrue(role.auths.all().exists())
        auth = ApplicationAuth.objects.get(application=self.application, key='0')
        self.assertFalse(auth in role.auths.all())
        
    def test_duplicated_attach(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: [0, 1, 2],
            self.role_keys_str: [3, 4, 5],
            self.auth_keys_str: [6, 7, 8],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: [0, 1, 2],
            self.role_keys_str: [4, 5, 6],
            self.auth_keys_str: [5, 6, 7],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        role4 = ApplicationRole.objects.get(application=self.application, key='4')
        self.assertEqual(['0', '1', '2'], sorted([user.key for user in role4.users.all()]))
        self.assertEqual(['5', '6', '7', '8'], sorted([auth.key for auth in role4.auths.all()]))
        auth7 = ApplicationAuth.objects.get(application=self.application, key='7')
        self.assertEqual(['3', '4', '5', '6'], sorted([role.key for role in auth7.roles.all()]))
        user0 = ApplicationUser.objects.get(application=self.application, key='0')
        self.assertEqual(['3', '4', '5', '6'], sorted([role.key for role in user0.roles.all()]))


class DetachTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            application_name='test',
            app_key='shjkfslk',
            url_for_reserve='application:detach',
            user_num=10,
            role_num=10,
            auth_num=10
        )
        self.user_keys_str = RequestFieldConst.USER_KEYS
        self.auth_keys_str = RequestFieldConst.AUTH_KEYS
        self.role_keys_str = RequestFieldConst.ROLE_KEYS

        self.client.post(reverse('application:attach'), json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: [1, 2, 3],
            self.role_keys_str: [4, 5, 6],
            self.auth_keys_str: [7, 8, 9],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')

    def test_get_method(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: '[]',
            self.auth_keys_str: '[]',
            self.role_keys_str: '[]',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(JsonResponseDictConst.FAIL, response.json()[JsonResponseDictConst.STATUS])

    def test_mess_input(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: '[1, 2, 3]',
            self.role_keys_str: '[4, 5, 6]',
            self.auth_keys_str: '[7, 8, 9]',
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])

        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: ['11'],
            self.role_keys_str: ['4'],
            self.auth_keys_str: ['7'],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])

    def test_succeed(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            self.user_keys_str: [1, 2],
            self.role_keys_str: [4, 5],
            self.auth_keys_str: [7, 8],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(JsonResponseDictConst.SUCCEED, response.json()[JsonResponseDictConst.STATUS])
        role4 = ApplicationRole.objects.get(application=self.application, key='4')
        self.assertEqual(sorted([user.key for user in role4.users.all()]), ['3'])
        self.assertEqual(sorted([user.key for user in role4.auths.all()]), ['9'])
        auth7 = ApplicationAuth.objects.get(application=self.application, key='7')
        self.assertEqual(sorted([role.key for role in auth7.roles.all()]), ['6'])
        user1 = ApplicationUser.objects.get(application=self.application, key='1')
        self.assertEqual(sorted([role.key for role in user1.roles.all()]), ['6'])


class CheckTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            application_name='test',
            app_key='hfsjlskdfjlsd',
            url_for_reserve='application:check',
            user_num=10,
            role_num=10,
            auth_num=10
        )

    def test_post_method(self):
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_mess_input(self):
        # no key
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        # empty key
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.KEY: '',
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        self.assertEqual(response.json()[JsonResponseDictConst.MSG], SetModelStatus.EMPTY_KEY.value)
        # key too long
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '0' * 1000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        self.assertEqual(response.json()[JsonResponseDictConst.MSG], SetModelStatus.KEY_TOO_LONG.value)
        # invalid key char
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '01msldk\\][.~',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        self.assertEqual(response.json()[JsonResponseDictConst.MSG], SetModelStatus.INVALID_KEY_CHAR.value)

    def test_key_conflict(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '9',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_succeed(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '10',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.NEW_APP_KEY: self.app_key + '1'
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

    def test_no_change(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.NEW_APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

    def test_mess_new_app_key(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.NEW_APP_KEY: ''
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.NEW_APP_KEY: '1' * 1000
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.NEW_APP_KEY: []
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_app_key_conflicted(self):
        self.application_name2 = 'test2'
        self.app_key2 = 'fsjlskfjlks23'
        self.application2 = Application.create_application_for_user(user=self.user, name=self.application_name2, app_key=self.app_key2)
        self.app_token2 = self.application2.create_token().content
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.NEW_APP_KEY: self.app_key2
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        self.assertIn('conflict', response.json()[JsonResponseDictConst.MSG])


class DeleteTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:delete',
            application_name='test',
            user_num=10,
            role_num=10,
            auth_num=10
        )
        self.application_name2 = 'test2'
        self.app_key2 = '78hjkn'
        self.application2 = Application.create_application_for_user(user=self.user, name=self.application_name2, app_key=self.app_key2)
        self.app_token2 = self.application2.create_token().content

    def test_get_method(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEYS: ['1', '2', '-1'],
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_with_wrong_keys(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEYS: "['1', '2', '-1']",
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEYS: ['1', '2', '-1'],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotIn(['1', '2'], [app.key for app in self.application.application_roles.all()])
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEYS: ['1', '2', 'asfnwka', 9],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotIn(['1', '2', '9'], [app.key for app in self.application.application_users.all()])
        # not a list
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEYS: "['1', '2', 'asfnwka', 9]",
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_delete_app(self):
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token2,
            RequestFieldConst.APP_KEY: self.app_key2
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotIn(self.application2, Application.objects.all())
        self.assertIn(self.application, Application.objects.all())
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotIn(self.application, Application.objects.all())

    def test_duplicated_keys(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEYS: ['1', '1', 'asfnwka', 9, '2', '2'],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotIn(['1', '2', '9'], [app.key for app in self.application.application_users.all()])



class AddTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:add',
            application_name='test'
        )
        self.application2_name = 'test2'
        self.app_key2 = '--___--'
        self.application2_description = 'test add application'
        response = self.client.post(reverse('root:login'), {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

    def test_add_application_with_duplicated_key(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.LIST: [{
                RequestFieldConst.NAME: self.application_name + '~',
                RequestFieldConst.APP_KEY: self.app_key,
                RequestFieldConst.KEY: 'afkjasl000dfldfsd',
                RequestFieldConst.DESCRIPTION: self.application2_description
            }]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn(self.application_name, response.json()[JsonResponseDictConst.MSG])

    def test_add_application(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.LIST: [{
                RequestFieldConst.NAME: self.application2_name,
                RequestFieldConst.APP_KEY: self.app_key2,
                RequestFieldConst.KEY: 'afkjasl000dfldfsd',
                RequestFieldConst.DESCRIPTION: self.application2_description
            }]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(response.json()[RequestFieldConst.LIST][0][RequestFieldConst.NAME], self.application2_name)
        self.assertEqual(response.json()[RequestFieldConst.LIST][0][RequestFieldConst.KEY], self.app_key2)
        self.assertEqual(
            response.json()[RequestFieldConst.LIST][0][RequestFieldConst.DESCRIPTION], self.application2_description)

    def test_add_object(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.LIST: [
                {
                    RequestFieldConst.NAME: '0号选手',
                    RequestFieldConst.KEY: '0',
                },
                {
                    RequestFieldConst.KEY: '1',
                    RequestFieldConst.DESCRIPTION: '???????'
                },
                {
                    RequestFieldConst.KEY: '2',
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(['0', '1', '2'], sorted([user.key for user in self.application.application_users.all()]))

    def test_wrong_input(self):
        # get method
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.LIST: [
                {
                    RequestFieldConst.NAME: '0号选手',
                    RequestFieldConst.KEY: '0',
                },
                {
                    RequestFieldConst.KEY: '1',
                    RequestFieldConst.DESCRIPTION: '???????'
                },
                {
                    RequestFieldConst.KEY: '2',
                }
            ]
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        # wrong type
        # TODO: 这种情况下，将会解析为要新建token
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: '-1',
            RequestFieldConst.LIST: [{
                    RequestFieldConst.NAME: '0号选手',
                    RequestFieldConst.KEY: '0',
            }]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        # no key
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.LIST: [{
                RequestFieldConst.NAME: '0号角色',
                RequestFieldConst.DESCRIPTION: '?????'
            }]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn(SetModelStatus.EMPTY_KEY.value, response.json()[JsonResponseDictConst.MSG])
        # empty key
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.LIST: [{
                RequestFieldConst.KEY: '',
                RequestFieldConst.NAME: '0号权限',
                RequestFieldConst.DESCRIPTION: '?????'
            }]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn(SetModelStatus.EMPTY_KEY.value, response.json()[JsonResponseDictConst.MSG])
        # duplicated key
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.LIST: [
                {
                    RequestFieldConst.NAME: '0号选手',
                    RequestFieldConst.KEY: '0',
                },
                {
                    RequestFieldConst.KEY: '2',
                    RequestFieldConst.DESCRIPTION: '???????'
                },
                {
                    RequestFieldConst.KEY: '0',
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn(SetModelStatus.KEY_ALREADY_EXISTS.value, response.json()[JsonResponseDictConst.MSG])
        self.assertEqual(['0', '2'], sorted([user.key for user in self.application.application_users.all()]))
        # not a list
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.LIST: [[{
                    RequestFieldConst.NAME: '0号选手',
                    RequestFieldConst.KEY: '0',
            }]]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.LIST: [[{
                RequestFieldConst.NAME: '0号选手',
                RequestFieldConst.KEY: '0',
            }]]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])
        # no name
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.LIST: [{
                RequestFieldConst.KEY: '0',
            }]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertNotEqual('', response.json()[JsonResponseDictConst.MSG])
    
    def test_add_parent_auth(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.APP_KEY: self.app_key,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.LIST: [
                {
                    RequestFieldConst.NAME: '0号选手',
                    RequestFieldConst.KEY: '0',
                },
                {
                    RequestFieldConst.KEY: '1',
                    RequestFieldConst.DESCRIPTION: '???????'
                },
                {
                    RequestFieldConst.KEY: '2',
                }
            ]
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        # self.assertEqual(['0', '1', '2'], sorted([user.key for user in self.application.application_users.all()]))


class ShowTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:show_related',
            application_name='test',
            user_num=10,
            role_num=10,
            auth_num=10
        )
        self.client.post(reverse('application:attach'), json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.USER_KEYS: [0, 1, 2],
            RequestFieldConst.ROLE_KEYS: [3, 4, 5],
            RequestFieldConst.AUTH_KEYS: [6, 7, 8],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.client.post(reverse('application:attach'), json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.USER_KEYS: [0, 1],
            RequestFieldConst.ROLE_KEYS: [4, 5],
            RequestFieldConst.AUTH_KEYS: [0, 1],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)
        self.client.post(reverse('application:attach'), json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.USER_KEYS: [7, 8, 9],
            RequestFieldConst.ROLE_KEYS: [4, 5],
            RequestFieldConst.AUTH_KEYS: [0, 1],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type=TestConst.JSON_CONTENT)

    def test_post_method(self):
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.FROM: 0,
            RequestFieldConst.TO: 10,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_wrong_key(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEY: '-1',
            RequestFieldConst.FROM: 0,
            RequestFieldConst.TO: 10,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_indirectly_related_types(self):
        # user -> auth
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '0',
            RequestFieldConst.FROM: -1000,
            RequestFieldConst.TO: 10000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(
            ['0', '1', '6', '7', '8'],
            sorted([auth[JsonResponseDictConst.AUTH_KEY] for auth in response.json()[RequestFieldConst.LIST]])
        )
        # auth -> user
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '0',
            RequestFieldConst.FROM: -1000,
            RequestFieldConst.TO: 10000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(
            ['0', '1', '2', '7', '8', '9'],
            sorted([user[JsonResponseDictConst.USER_KEY] for user in response.json()[RequestFieldConst.LIST]])
        )
        # user -> user
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '0',
            RequestFieldConst.FROM: -1000,
            RequestFieldConst.TO: 10000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(
            [],
            sorted([auth[JsonResponseDictConst.AUTH_KEY] for auth in response.json()[RequestFieldConst.LIST]])
        )

    def test_out_of_range(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '0',
            RequestFieldConst.FROM: -1000,
            RequestFieldConst.TO: 0,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '0',
            RequestFieldConst.FROM: 6,
            RequestFieldConst.TO: 1000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_empty_range(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '0',
            RequestFieldConst.FROM: 1,
            RequestFieldConst.TO: 1,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_right_input(self):
        # role -> user
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '5',
            RequestFieldConst.FROM: -1000,
            RequestFieldConst.TO: 10000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(
            ['0', '1', '2', '7', '8', '9'],
            sorted([user[JsonResponseDictConst.USER_KEY] for user in response.json()[RequestFieldConst.LIST]])
        )
        
        # auth -> role
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.WANTED_TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEY: '8',
            RequestFieldConst.FROM: -1,
            RequestFieldConst.TO: 10000,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(
            ['3', '4', '5'],
            sorted([role[JsonResponseDictConst.ROLE_KEY] for role in response.json()[RequestFieldConst.LIST]])
        )


class TotalTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:total',
            application_name='test',
            user_num=7,
            role_num=8,
            auth_num=9
        )

    def test_post_method(self):
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_succeed(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(7, response.json()[JsonResponseDictConst.TOTAL])
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(8, response.json()[JsonResponseDictConst.TOTAL])
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(9, response.json()[JsonResponseDictConst.TOTAL])


class DescriptionTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:description',
            application_name='test',
            application_description='???',
            user_num=10,
            role_num=10,
            auth_num=10
        )

    def test_post_method(self):
        response = self.client.post(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_succeed(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual('1号选手', response.json()[RequestFieldConst.CONTENT])
        self.application2_name = 'test2'
        self.app_key2 = 'hjkghjkghjklp'
        self.application2 = Application.create_application_for_user(
            user=self.user, name=self.application2_name, description='***', app_key=self.app_key2)
        self.app_token2 = self.application2.create_token().content
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token2,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.APP_KEY: self.app_key2
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual('***', response.json()[RequestFieldConst.CONTENT])

    def test_type_out_of_range(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: 10,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual('???', response.json()[RequestFieldConst.CONTENT])


class EditTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:edit',
            application_name='test',
            application_description='???',
            user_num=10,
            role_num=10,
            auth_num=10
        )
        self.client.post(reverse('root:login'), {
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password
        })
        self.application2_name = 'test2'
        self.app_key2 = '84rwhjfsj'
        self.application2 = Application.create_application_for_user(
            user=self.user, name=self.application2_name, description='***', app_key=self.app_key2)
        self.app_token2 = self.application2.create_token().content

    def test_get_method(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.DETAIL: {
                RequestFieldConst.NAME: '10号选手',
                RequestFieldConst.KEY: 10,
                RequestFieldConst.DESCRIPTION: '10号选手'
            },
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_modify_type_key(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.DETAIL: {
                RequestFieldConst.NAME: '10号选手',
                RequestFieldConst.KEY: '10',
                RequestFieldConst.DESCRIPTION: '10号选手'
            },
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        user10 = ApplicationUser.objects.filter(key='10')
        self.assertNotEqual(user10.count(), 0)
        user10 = user10.first()
        self.assertEqual('10号选手', user10.name)
        self.assertEqual('10号选手', user10.description)
        self.assertEqual(ApplicationUser.objects.filter(key='1').count(), 0)

    def test_conflicted_key(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.DETAIL: {
                RequestFieldConst.KEY: '0',
            },
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn('conflicted', response.json()[JsonResponseDictConst.MSG])

    def test_wrong_input(self):
        # wrong detail format
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.DETAIL: [{
                RequestFieldConst.NAME: '10号选手',
                RequestFieldConst.KEY: '10',
                RequestFieldConst.DESCRIPTION: '10号选手'
            }],
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.DETAIL: None,
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

        # wrong key
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.KEY: '-1',
            RequestFieldConst.DETAIL: {
                RequestFieldConst.KEY: '1',
            },
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

        # no key with type
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.DETAIL: {
                RequestFieldConst.NAME: '10号权限',
                RequestFieldConst.KEY: '10',
                RequestFieldConst.DESCRIPTION: '10号权限',
            },
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

        # no name
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.DETAIL: {
                RequestFieldConst.KEY: '10',
                RequestFieldConst.DESCRIPTION: '10号权限',
                RequestFieldConst.NAME: 123
            },
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        self.assertEqual(response.json()[JsonResponseDictConst.MSG], SetModelStatus.NAME_NOT_STR.value)

    def test_conflicted_application_key(self):
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.KEY: '1',
            RequestFieldConst.DETAIL: {
                RequestFieldConst.KEY: self.app_key2,
            },
            RequestFieldConst.APP_KEY: self.app_key
        }), content_type='application/json')
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
        self.assertIn(Application.ApplicationCheckStatus.KEY_CONFLICT, response.json()[JsonResponseDictConst.MSG])


class SearchTestCase(TestCase):
    def setUp(self):
        super().setUp()
        prebuild(
            self=self,
            username='test',
            password='test',
            url_for_reserve='application:search',
            application_name='test',
            application_description='???',
            user_num=10,
            role_num=10,
            auth_num=10
        )

    def test_empty_content(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.USER.value,
            RequestFieldConst.FROM: -1,
            RequestFieldConst.TO: 1000,
            RequestFieldConst.CONTENT: '',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(10, response.json()[JsonResponseDictConst.TOTAL])

    def test_empty_list(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.ROLE.value,
            RequestFieldConst.FROM: -1,
            RequestFieldConst.TO: 1000,
            RequestFieldConst.CONTENT: '???',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(0, response.json()[JsonResponseDictConst.TOTAL])
        self.assertEqual([], response.json()[RequestFieldConst.LIST])

    def test_from_not_less_than_count(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.FROM: 1,
            RequestFieldConst.TO: 2,
            RequestFieldConst.CONTENT: '0',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_succeed(self):
        response = self.client.get(self.url, {
            RequestFieldConst.APP_TOKEN: self.app_token,
            RequestFieldConst.TYPE: RequestFieldConst.OperateType.AUTH.value,
            RequestFieldConst.FROM: 2,
            RequestFieldConst.TO: 10,
            RequestFieldConst.CONTENT: '权限',
            RequestFieldConst.APP_KEY: self.app_key
        })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertEqual(8, response.json()[RequestFieldConst.LIST].__len__())
        self.assertEqual(10, response.json()[JsonResponseDictConst.TOTAL])
