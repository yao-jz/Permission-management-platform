import json
import random

from django.contrib import auth as django_auth

from utils.const import JsonResponseDictConst, RequestFieldConst, TestConst
from utils.tests import DemoTestCase

from .views import create_user, get_user_info
from .models import UserInfo

# Create your tests here.


class GetInfoTestCase(DemoTestCase('user_info:get_info', [TestConst.RequestMethod.POST], True)):
    # url: /user_info/

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(password=self.password, username=self.username)

    def test_succeed(self) -> None:
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password,
        }), content_type=TestConst.JSON_CONTENT)

        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn(f'{self.user.id}', response.json()[JsonResponseDictConst.AVATAR])

    def test_mess(self) -> None:
        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.USERNAME: 'jlksklf',
            RequestFieldConst.PASSWORD: 'jlsdfj',
        }), content_type=TestConst.JSON_CONTENT)

        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_no_info(self) -> None:
        self.user.info.delete()
        self.assertTrue(not UserInfo.objects.filter(user=self.user).exists())

        response = self.client.post(self.url, json.dumps({
            RequestFieldConst.USERNAME: self.username,
            RequestFieldConst.PASSWORD: self.password,
        }), content_type=TestConst.JSON_CONTENT)

        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)
        self.assertIn(f'{self.user.id}', response.json()[JsonResponseDictConst.AVATAR])
        self.assertTrue(UserInfo.objects.filter(user=self.user).exists())


class ChangeAvatarTestCase(DemoTestCase('user_info:avatar', [TestConst.RequestMethod.POST], True)):
    # url: /user_info/avatar

    def setUp(self) -> None:
        super().setUp()
        self.user = create_user(password=self.password, username=self.username)

    def test_change(self) -> None:
        with open(TestConst.TEST_USER_AVATAR, 'br') as test_avatar:
            response = self.client.post(self.url, {
                RequestFieldConst.USERNAME: self.username,
                RequestFieldConst.PASSWORD: self.password,
                'file': test_avatar,
            })
        self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

        with open(TestConst.TEST_USER_AVATAR, 'br') as test_avatar:
            with open(get_user_info(self.user).get_entire_avatar_path(), 'br') as avatar:
                self.assertEqual(test_avatar.readlines(), avatar.readlines())


class EditInfoTestCase(DemoTestCase('user_info:edit', [TestConst.RequestMethod.POST], True)):
    # url: /user_info/edit
    
    def setUp(self) -> None:
        super().setUp()
        random.seed()
        self.user = create_user(password=self.password, username = self.username)

    def test_no_detail(self) -> None:
        for request_func in self.request_methods():
            response = request_func({
                RequestFieldConst.USERNAME: self.username,
                RequestFieldConst.PASSWORD: self.password,
            })
            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)

    def test_edit_password(self) -> None:
        for request_func in self.request_methods():
            random_str = str(random.randint(0, 100))
            response = request_func({
                RequestFieldConst.USERNAME: self.username,
                RequestFieldConst.PASSWORD: self.password,
                RequestFieldConst.DETAIL: {
                    RequestFieldConst.PASSWORD: self.password + random_str,
                },
            })
            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

            changed_user = django_auth.authenticate(username=self.username, password=self.password + random_str)
            self.assertNotEqual(changed_user, None)

    def test_edit_username(self) -> None:
        for request_func in self.request_methods():
            random_str = str(random.randint(0, 100))
            response = request_func({
                RequestFieldConst.USERNAME: self.username,
                RequestFieldConst.PASSWORD: self.password,
                RequestFieldConst.DETAIL: {
                    RequestFieldConst.USERNAME: self.username + random_str,
                },
            })
            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

            changed_user = django_auth.authenticate(username=self.username + random_str, password=self.password)
            self.assertNotEqual(changed_user, None)

    def test_edit_all(self) -> None:
        for request_func in self.request_methods():
            random_str = str(random.randint(0, 100))
            response = request_func({
                RequestFieldConst.USERNAME: self.username,
                RequestFieldConst.PASSWORD: self.password,
                RequestFieldConst.DETAIL: {
                    RequestFieldConst.USERNAME: self.username + random_str,
                    RequestFieldConst.PASSWORD: self.password + random_str * 2,
                },
            })
            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

            changed_user = django_auth.authenticate(username=self.username + random_str, password=self.password + random_str * 2)
            self.assertNotEqual(changed_user, None)

    def test_username_conflict(self) -> None:
        for request_func in self.request_methods():
            random_str = str(random.randint(0, 100))
            create_user(username=self.username + random_str, password=self.password)
            response = request_func({
                RequestFieldConst.USERNAME: self.username,
                RequestFieldConst.PASSWORD: self.password,
                RequestFieldConst.DETAIL: {
                    RequestFieldConst.USERNAME: self.username + random_str,
                },
            })
            self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.SUCCEED)

            user = django_auth.authenticate(username=self.username, password=self.password)
            self.assertNotEqual(user, None)
