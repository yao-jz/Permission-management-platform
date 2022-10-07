# 后端仓库

本仓库是软工大作业的后端部分。

后端的运行地址：`http://49.232.101.156:8000/`。设置了`Debug = True`，所以不要告诉其他人或捣乱。

## 环境和依赖

- `python 3.8.3`

- `pip 21.0.1`

- `mysql 8.0.22`

  有用户`'test'@'localhost'`，密码`test`，并有数据库`test`的全部权限。

## 运行方式

1. 先把最新的`backend/settings_for_copy.py`的变化拷贝到`backend/settings.py`里面。如果是初次拷贝，请将数据库设置换成`mysql`（见相关部分的注释）。

2. 若没有安装过需要的各个`python`库，先安装库：

   ```powershell
   pip install -r ./requirements.txt
   ```

3. 进行数据库迁移和应用：

   ```powershell
   python manage.py makemigrations
   ```

   ```powershell
   python manage.py migrate
   ```

4. 运行：

   ```powershell
   python manage.py runserver
   ```
   
5. 如果想要进行本地测试，运行：

   ```powershell
   coverage run --source='.' manage.py test
   ```

   然后使用命令：

   ```powershell
   coverage html
   coverage report
   ```

   分别可以生成`html`和命令行报表。
   
   由于加入了代码风格测试，所以还需要运行`pylint`。具体建议见document仓库的”关于测试“部分。

## 后端已完成的接口

### 通用约定说明

- 所有列表相关（`from` `to`或者`page`之类的）都是0开始计数。
- `status`域的值只有`succeed`或`fail`。
- 由于浏览器原因，后端无法给请求设置cookie。因此所有标注“需要登录”的函数都可以通过加上`username`和`password`域实现登录效果（每次都要）。
- `type`为0表示用户，为1表示角色，为2表示权限，其它值会视为错误。
- 后面加`?`表示这个域可能不用提供或不会返回，对应不同的情况和逻辑（API简介会有专门的说明）。
- 如果返回信息里面有权限，该返回信息还会带有一个域是`child_permissions: []`，里面是所有子权限的信息，子权限信息本身也会带有`child_permissions`，层层嵌套，直到叶子权限时列表为空；同时会有一个域`parent_permission`表明其父权限的信息（包括`name`和`key`域）。由于接口繁多，不一定每一个相关接口都有这个标识，在此统一说明。
- 当进行关联和解联操作时，后端会自动把所有具有子权限的权限都转为它所有叶子权限的集合，然后再进行关联和解联。
- 如果一个角色关联了一个叶子权限，但是通过delete api删除了该权限的某个父权限，则该角色和该权限将自动解联。
- 不允许用户直接关联权限，所有关联都要通过角色层转发。
- 本阶段的所有API都是可以被第三方应用使用的。
- 对于每个系统用户，他的所有App的`name`都需要是不同的。对于每个App，其下属的权限的`key`不能有重复，而`name`可以；对于角色和用户同理。

### 各接口详情

1. 用户登录（POST）

   "/login"

   ```json
   {
       username: string,
       password: string,
   }
       =>
   {
       status: string,
       msg: string,
   }
   ```

2. 获得app列表（GET/POST），需要已经登录

   "/app"

   ```json
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
   ```

3. 用户登出（GET/POST），需要已经登录

   "/logout"

   ```json
   { }
       =>
   {
       status: string,
       msg: string,
   }
   ```

4. 用户注册（POST）

   "/register"

   ```json
   {
       password: string,
       username: string,
   }
       =>
   {
       status: string,
       msg: string,
   }
   ```

5. 获得本身的信息（GET）

   如果不提供type域，则认为要获得App的详细信息

   "/app/detail"

   ```json
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
               access: string,
           }
       ], ?
   }
   ```

6. 获得角色，权限或用户列表（GET）

   "/app/list"

   ```json
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
   ```

7. 角色，用户，权限关联（POST）

   "/app/attach"

   ```json
   {
       app_token: string,
       user_keys: [
           string | {
               key: string,
               time_out: int,  // 设置和角色关联关系的时限（秒）
           }
       ],
       permission_keys: [string],
       role_keys: [string],
   }
       =>
   {
       status: string,
       msg: string,
   }
   ```

8. 角色，用户，权限解联（POST）

   "/app/detach"

   ```json
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
   ```

9. 改key的时候检查是否有冲突（GET）

   "/app/check"

   ```json
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
   ```

10. 删除角色，用户，权限或者app（POST）

    如果没有type域或不合法，则认为是要删除这个app

    "/app/delete"

    ```json
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
    ```

11. 新建用户，权限，角色，应用，app_token（POST）

    如果没有app_token域，则认为是要新建一些app，此时需要用户已经登录

    如果有app_token但是没有type，则认为是要新建一些app_token，也需要用户已登录

    "/app/add"

    ```json
    {
         app_token: string, ?
         type: int, ?
         list: [
             {
                 name: string, ?
                 key: string, ?
                 description: string, ?
                 parent_key: string, ?  // 标示新建子权限的时候关联的父权限
                 alive_time: int, ?  // 标示新建app_token的时候的期限（单位：秒），不写则为默认的一周
                 token_access: int, ?  // 新建的app_token的权限等级
             },
         ]
     }
         =>
     {
         status: string,
         msg: string,
         list: [
             {
                 name: string, ?
                 key: string, ?
                 created_time: string,
                 dead_time: string, ?  // app_token的失效时间
                 description: string, ?
                 parent_permission: {
                     name: string,
                     key: string,
                 },   ?
                 tokens: [string], ?  // 如果是新建App，返回所有的token
                 child_permissions: [], ?
             },
         ]
     }
    ```

12. 显示用户，角色，权限的关联关系（GET）

    目标对象由app_token, type, key来定位，获得它所有的关联的want_type类型的对象数据

    显示的关联关系是角色和用户之间的关系，还有一个detach_time域来指示两者关联的期限

    "/app/show"

    ```json
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
    ```

13. 获取某东西的总数（GET）

    "/app/total"

    ```json
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
    ```

14. 获得description，由于可能会很长所以专门分一个（GET）

    现在先不搞那么复杂，不会返回page，也不会有分页逻辑

    "/app/description"

    ```json
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
    ```

15. 编辑某东西信息，采用覆盖策略（POST）

    如果没有type则认为要编辑App信息

    "/app/edit"

    ```json
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
    ```

16. 搜索（GET）

    会在name和key字段都进行搜索，支持中文

    "/app/search"

    ```json
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
    ```

17. 删除app_token（POST），需要登录

    "/token/delete"

    ```json
    {
        list: [
            {
                app_key: string,
                app_token: string,
            }
        ],
    }
        =>
    {
        status: string,
        msg: string,
    }
    ```

18. 修改app_token期限和权限（POST），需要登录

    alive_time可以用int类型的数据表示期限的秒数（需为正数），也可以写forever，表示设为永久

    "/token/change"

    ```json
    {
        list: [
            {
                app_key: string,
                app_token: string,
                alive_time: int | string("forever"), ?
                token_access: int, ?
            }
        ]
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                content: string,
                created_time: string,
                dead_time: string,
                access: int,
            } | {}
        ]
    }
    ```

19. 获得用户本人的详细信息（POST），需要登录

    "/user_info/"

    ```json
    { }
        =>
    {
        status: string,
        msg: string,
        avatar: string,
        email: string,
    }
    ```

20. 修改用户头像（POST），需要登录

    传入的应该是一个文件对象，可用el-upload实现

    "/user_info/avatar"

    ```json
    {
        file: file,
    }
        =>
    {
        status: string,
        msg: string,
    }
    ```

21. 修改用户信息（POST），需要已登录

    "/user_info/edit"

    ```json
    {
        detail: {
            username: string, ?
            password: string, ?
            email: string, ?
        }
    }
        =>
    {
        status: string,
        msg: string,
    }
    ```

22. 永久删除用户（POST），需要已登录

    "/delete"

    ```json
    { }
        =>
    {
        status: string,
        msg: string,
    }
    ```

23. 验证邮件验证码（POST）

    "/verify/code"

    ```json
    {
        code: string,
        email: string,
    }
        =>
    {
        status: string,
        msg: string,
    }
    ```

24. 向其他用户分享自己的App（POST），需要登录

    "/app/share"

    ```json
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
    ```

25. 获得所有被分享的App的列表（POST），需要登录

    "/app/shared_list"

    ```json
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
    ```

26. 获取用户组（POST）

    "/app/user_group"

    ```json
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
    ```

27. 向同组的用户发送信息（POST），需要登录

    "/app/send_message"

    ```json
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
    ```

28. 对特定用户取消App共享（POST），需要登录

    "/app/unshare"

    ```json
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
    ```

29. 获得用户接受的所有信息的列表（POST），需要登录

    "/message/recv_list"

    ```json
    { 
        from: int,
        to: int,
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                created_time: string,
                message: string,
                title: string,
                from: string,
                to: string
            }
        ]
    }
    ```

30. 获得用户发出的所有信息的列表（POST），需要登录

    "/message/sended_list"

    ```json
    { 
        from: int,
        to: int,
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                created_time: string,
                message: string,
                title: string,
                from: string,
                to: string
            }
        ]
    }
    ```
