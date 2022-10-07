'''
这些测试采用了DemoTestCase等一系列工具链，所以专门开了一个新文件

测试的部分并不一定贴合“new”的语义
'''

import datetime
import random

from pytz import UTC
from django.contrib.auth import get_user_model

from application_token.models import ApplicationToken
from user_app_relation.models import UserApplicationRelation
from user_info.views import create_user
from utils.const import TestConst, RequestFieldConst, JsonResponseDictConst
from utils.tests import DemoTestCase

from .models import Application

User = get_user_model()


class TokenDeleteTestCase(DemoTestCase(
        reverse_url='token:delete',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    def get_unused_token(self, token_access: ApplicationToken.ApplicationAccessStatus 
        = ApplicationToken.ApplicationAccessStatus.ALL) -> str:
        '''
        创建一个不存在的token内容
        '''

        new_token = self.another_application.create_token(token_access=token_access)
        return_str = new_token.content
        ApplicationToken.objects.filter(content=return_str).delete()
        return return_str

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(username=self.username, password=self.password)
        self.application_name = 'test'
        self.application = Application.create_application_for_user(
            self.user, self.application_name)
        self.another_application = Application.create_application_for_user(
            self.user, self.application_name + 'test')

        self.token_num = 9
        self.tokens = []
        for _ in range(self.token_num):
            self.tokens += [self.application.create_token()]

    def test_unavailable_token(self) -> None:
        '''
        测试传入不存在的token
        '''

        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_TOKEN: self.get_unused_token(),
                        RequestFieldConst.APP_KEY: self.application.key,
                    },
                ],
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertEqual(len(self.application.tokens.all()), self.token_num)

    def test_mess(self) -> None:
        '''
        测试是否能够正确处理胡乱的字符串
        '''

        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: ['kasfjoofwclnlsl'],
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertEqual(len(self.application.tokens.all()), self.token_num)

            response_json = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_KEY: self.application.key,
                    }
                ]
            }).json()
            
            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertEqual(len(self.application.tokens.all()), self.token_num)
            self.assertIn(JsonResponseDictConst.ErrorMessage.NO_REQUIRED_FIELD, response_json[JsonResponseDictConst.MSG])

    def test_succeed(self) -> None:
        '''
        正确传入token并删除
        '''

        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_TOKEN: self.tokens[0].content,
                        RequestFieldConst.APP_KEY: self.application.key,
                    },
                ],
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertEqual(len(self.application.tokens.all()), self.token_num - 1)

    def test_no_access(self) -> None:
        '''
        测试用户没有足够权限删除
        '''

        another_username = self.username + 'another'
        another_password = self.password + 'another'
        another_user = create_user(username=another_username, password=another_password)
        self.application.share(another_user, UserApplicationRelation.UserAccessStatus.SEE)

        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.USERNAME: another_username,
                RequestFieldConst.PASSWORD: another_password,
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_KEY: self.application.key,
                        RequestFieldConst.APP_TOKEN: self.tokens[0].content,
                    }
                ]
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertIn(JsonResponseDictConst.ErrorMessage.ACCESS_ERROR, response_json[JsonResponseDictConst.MSG])


class TokenChangeTestCase(DemoTestCase(
        reverse_url='token:change',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(username=self.username, password=self.password)
        self.application_name = 'test'
        self.application = Application.create_application_for_user(
            self.user, self.application_name)
        self.token = self.application.create_token()

    def test_unavailable_token(self) -> None:
        '''
        测试不存在的token
        '''

        token_string = 'test'

        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_KEY: self.application.key,
                        RequestFieldConst.APP_TOKEN: token_string,
                    }
                ]
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertIn(JsonResponseDictConst.ErrorMessage.TOKEN_ATTACH_NO_APPLICATION,
                response.json()[JsonResponseDictConst.MSG])

    def test_mess(self) -> None:
        '''
        测试杂乱数据
        '''
        
        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: ['jsdfjlsdlksd']
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertIn(JsonResponseDictConst.ErrorMessage.PARSE_MESS, response.json()[JsonResponseDictConst.MSG])

    def test_no_app_key(self) -> None:
        '''
        测试没有app_key
        '''
        
        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_TOKEN: self.token.content,
                    }
                ]
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertIn(JsonResponseDictConst.ErrorMessage.NO_REQUIRED_FIELD, 
                response.json()[JsonResponseDictConst.MSG])

    def test_set_forever(self) -> None:
        '''
        测试正确设置为永久token
        '''
        
        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_KEY: self.application.key,
                        RequestFieldConst.APP_TOKEN: self.token.content,
                        RequestFieldConst.ALIVE_TIME: RequestFieldConst.FOREVER,
                    }
                ]
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            changed_token = ApplicationToken.objects.filter(content=self.token.content).first()
            self.assertTrue(changed_token.forever)

    def test_set_another_time(self) -> None:
        '''
        测试正确设置为一定期限的token
        '''

        new_time_out = datetime.timedelta(hours=1)
        bias = datetime.timedelta(seconds=2)
        
        for request_method in self.request_methods():
            response = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_KEY: self.application.key,
                        RequestFieldConst.APP_TOKEN: self.token.content,
                        RequestFieldConst.ALIVE_TIME: int(new_time_out.total_seconds()),
                    }
                ]
            })

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            changed_token = ApplicationToken.objects.filter(content=self.token.content).first()
            self.assertTrue(
                datetime.datetime.now(UTC) + new_time_out - bias 
                <= changed_token.dead_time <= 
                datetime.datetime.now(UTC) + new_time_out + bias
            )

    def test_set_access_succeed(self) -> None:
        '''
        测试成功更改token的权限
        '''

        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.LIST: [
                    {
                        RequestFieldConst.APP_KEY: self.application.key,
                        RequestFieldConst.APP_TOKEN: self.token.content,
                        RequestFieldConst.TOKEN_ACCESS: ApplicationToken.ApplicationAccessStatus.ADD.value,
                    }
                ]
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertEqual(ApplicationToken.objects.filter(content=self.token.content).first().access, 
                ApplicationToken.ApplicationAccessStatus.ADD.value)


class DeleteUserTestCase(DemoTestCase(
        reverse_url='root:delete',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(username=self.username, password=self.password)

    def test_succeed(self) -> None:
        '''
        测试成功删除用户
        '''

        for request_method in self.request_methods():
            response = request_method({})

            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            self.assertFalse(User.objects.filter(username=self.username).exists())


class ApplicationShareTestCase(DemoTestCase(
        reverse_url='application:share',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(username=self.username, password=self.password)
        self.application_name = 'test'
        self.application = Application.create_application_for_user(self.user, self.application_name)
        self.token = self.application.create_token()

        self.another_username = self.username + 'another'
        self.another_password = self.password + 'another'
        self.another_user = create_user(username=self.another_username, password=self.another_password)

    def test_user_not_exist(self) -> None:
        '''
        测试共享给一个不存在的用户
        '''

        unavailable_username = self.username + 'no_exist'
        
        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.APP_TOKEN: self.token.content,
                RequestFieldConst.APP_KEY: self.application.key,
                RequestFieldConst.USERNAME_SHARE: unavailable_username,
                RequestFieldConst.ACCESS: UserApplicationRelation.UserAccessStatus.ADMIN.value,
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
            self.assertIn(JsonResponseDictConst.ErrorMessage.USER_NOT_FIND, response_json[JsonResponseDictConst.MSG])

    def test_not_creator(self) -> None:
        '''
        测试非创建者试图进行App共享
        '''

        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.USERNAME: self.another_username,
                RequestFieldConst.PASSWORD: self.another_password,
                RequestFieldConst.APP_TOKEN: self.token.content,
                RequestFieldConst.APP_KEY: self.application.key,
                RequestFieldConst.USERNAME_SHARE: self.username,
                RequestFieldConst.ACCESS: UserApplicationRelation.UserAccessStatus.ADMIN.value,
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
            self.assertIn(JsonResponseDictConst.ErrorMessage.ACCESS_ERROR, response_json[JsonResponseDictConst.MSG])

    def test_succeed(self) -> None:
        '''
        测试成功共享App
        '''
        
        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.APP_TOKEN: self.token.content,
                RequestFieldConst.APP_KEY: self.application.key,
                RequestFieldConst.USERNAME_SHARE: self.another_username,
                RequestFieldConst.ACCESS: UserApplicationRelation.UserAccessStatus.ADMIN.value,
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

            new_access = self.application.get_user_access(self.another_user)
            self.assertEqual(new_access, UserApplicationRelation.UserAccessStatus.ADMIN)

    def test_mess(self) -> None:
        '''
        测试杂乱数据
        '''
        
        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.APP_TOKEN: self.token.content,
                RequestFieldConst.APP_KEY: self.application.key,
                RequestFieldConst.USERNAME_SHARE: self.another_username,
                RequestFieldConst.ACCESS: 100,
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
            self.assertIn(JsonResponseDictConst.ErrorMessage.PARSE_MESS, response_json[JsonResponseDictConst.MSG])


class SharedApplicationListTestCase(DemoTestCase(
        reverse_url='application:shared_list',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(username=self.username, password=self.password)
        self.num = 10
        self.other_usernames = [self.username + str(i) for i in range(self.num)]
        self.other_passwords = [self.password + str(i) for i in range(self.num)]
        self.other_users = [create_user(username=self.other_usernames[i], password=self.other_passwords[i]) for i in range(self.num)]

        self.other_applications = [Application.create_application_for_user(another_user, another_user.username) for another_user in self.other_users]

    def test_succeed(self) -> None:
        '''
        测试正常获取被分享的App
        '''

        application = self.other_applications[random.randint(0, self.num - 1)]
        application.share(self.user)

        for request_method in self.request_methods():
            response_json = request_method({}).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            return_application = response_json[JsonResponseDictConst.LIST][0]
            self.assertEqual(return_application[JsonResponseDictConst.KEY], application.key)


class UserGroupTestCase(DemoTestCase(
        reverse_url='application:user_group',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=False
    )):

    def setUp(self) -> None:
        super().setUp()
        self.user_num = 10
        self.usernames = ['test_name' + str(i) for i in range(self.user_num)]
        self.passwords = ['test_password' + str(i) for i in range(self.user_num)]
        self.users = [create_user(username=self.usernames[i], password=self.passwords[i]) for i in range(self.user_num)]

        self.creator_username = 'creator'
        self.creator_password = 'creator'
        self.creator = create_user(username=self.creator_username, password=self.creator_password)

        self.application = Application.create_application_for_user(self.creator, 'test_app')
        self.token = self.application.create_token()

    def test_succeed(self) -> None:
        '''
        测试正常获得用户组
        '''

        shared_user = self.users[0]
        share_access = UserApplicationRelation.UserAccessStatus.ADMIN
        self.application.share(shared_user, share_access)

        for request_method in self.request_methods():
            response_json = request_method({
                RequestFieldConst.APP_KEY: self.application.key,
                RequestFieldConst.APP_TOKEN: self.token.content,
            }).json()

            self.assertEqual(response_json[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
            response_user = response_json[JsonResponseDictConst.LIST][1]
            self.assertEqual(response_user[JsonResponseDictConst.USER_NAME], shared_user.username)
            self.assertEqual(response_user[JsonResponseDictConst.ACCESS], share_access.value)


class UnshareApplicationTestCase(DemoTestCase(
        reverse_url='application:unshare',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    pass


class SendMessageTestCase(DemoTestCase(
        reverse_url='application:send_message',
        support_methods=[TestConst.RequestMethod.POST],
        need_login=True
    )):

    pass
