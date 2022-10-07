import json

from typing import Any, Dict, List
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.client import Client

from .const import JsonResponseDictConst, RequestFieldConst, TestConst

# Create your tests here.

User = get_user_model()


class TestCaseFactory:
    '''
    将一些常用的测试逻辑封装于此
    '''

    class TestDemo:
        def demoSetUp(self) -> None:
            self.client = Client()
            self.username = 'test'
            self.password = 'test'

    def __init__(self, reverse_url: str, support_methods: List[TestConst.RequestMethod] = [TestConst.RequestMethod.POST, TestConst.RequestMethod.GET], 
        need_login: bool = False) -> None:
        '''
        传入各自定义参数，生成模板测试类供继承
        '''

        self.url = reverse(reverse_url)
        self.need_login = need_login

        if TestConst.RequestMethod.GET not in support_methods:
            self.method_for_test = TestConst.RequestMethod.GET
        elif TestConst.RequestMethod.POST not in support_methods:
            self.method_for_test = TestConst.RequestMethod.POST
        else:
            self.method_for_test = None

    def __call__(self) -> type:
        cls = type(self)

        class Demo(cls.TestDemo):
            def demoSetUp(demo_self) -> None:
                super().demoSetUp()
                demo_self.url = self.url

            def request_methods(demo_self) -> list:
                return_list = []

                if self.method_for_test != TestConst.RequestMethod.GET:
                    def get_request(data: Dict[str, Any]):
                        return demo_self.client.get(path=demo_self.url, data=data)
                    return_list += [get_request]
                if self.method_for_test != TestConst.RequestMethod.POST:
                    def json_post_request(data: Dict[str, Any]):
                        return demo_self.client.post(path=demo_self.url, data=json.dumps(data), content_type=TestConst.JSON_CONTENT)
                    return_list += [json_post_request]

                return return_list

        return_class = Demo

        if self.method_for_test is not None:
            class TestMethod(return_class):
                def test_unsupported_method(demo_self) -> None:
                    request_function = demo_self.client.get if self.method_for_test == TestConst.RequestMethod.GET else demo_self.client.post
                    response = request_function(demo_self.url)

                    demo_self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
                    demo_self.assertIn(JsonResponseDictConst.ErrorMessage.METHOD_ONLY, response.json()[JsonResponseDictConst.MSG])

            return_class = TestMethod

        if self.need_login:
            class TestLogin(return_class):
                def test_no_login(demo_self) -> None:
                    for request_method in super().request_methods():
                        response = request_method(data={})
                        demo_self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
                        demo_self.assertIn(JsonResponseDictConst.ErrorMessage.EMPTY_OR_NO_LOGIN_FIELDS, response.json()[JsonResponseDictConst.MSG])
                        
                        response = request_method(data={})
                        
                        demo_self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
                        demo_self.assertIn(JsonResponseDictConst.ErrorMessage.EMPTY_OR_NO_LOGIN_FIELDS, response.json()[JsonResponseDictConst.MSG])

                def test_wrong_login(demo_self) -> None:
                    for request_method in super().request_methods():
                        response = request_method(data={})
                        demo_self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
                        demo_self.assertIn(JsonResponseDictConst.ErrorMessage.EMPTY_OR_NO_LOGIN_FIELDS, response.json()[JsonResponseDictConst.MSG])
                        
                        response = request_method(data={
                            RequestFieldConst.USERNAME: demo_self.username + 'fake',
                            RequestFieldConst.PASSWORD: demo_self.password + 'fake',
                        })

                        demo_self.assertEqual(response.json()[JsonResponseDictConst.STATUS], JsonResponseDictConst.FAIL)
                        demo_self.assertIn(JsonResponseDictConst.ErrorMessage.LOGIN_FAIL, response.json()[JsonResponseDictConst.MSG])

                def request_methods(demo_self) -> list:
                    return_list = []

                    for request_method in super().request_methods():
                        def loginned_method(data: Dict[str, Any]):
                            loginned_data = {
                                RequestFieldConst.USERNAME: demo_self.username,
                                RequestFieldConst.PASSWORD: demo_self.password,
                            }

                            loginned_data.update(data)

                            return request_method(loginned_data)

                        return_list += [loginned_method]

                    return return_list

            return_class = TestLogin

        return return_class

def DemoTestCase(reverse_url: str, support_methods: List[TestConst.RequestMethod] = [TestConst.RequestMethod.POST, TestConst.RequestMethod.GET],
    need_login: bool = False) -> type:
    '''
    得到一个已经预含有一些常用测试方法的类，用于给测试类继承

    用法：

    class MyTestCase(DemoTestCase(...)):
        ...

    将带有的域和方法：
    - username: str
    - password: str
    - client: Client
    - url: str
    - request_methods: () -> List[function]
    '''

    class _DemoTestCase(TestCase, TestCaseFactory(reverse_url=reverse_url, support_methods=support_methods, need_login=need_login)()):
        def setUp(self) -> None:
            self.demoSetUp()

    return _DemoTestCase
