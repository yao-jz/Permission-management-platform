# 前端仓库

本仓库是软工大作业的前端部分。

## 环境和依赖

-   `npm 6.14.11`
-   `@vue/cli@4.5.11`
-   `vue@3.0.7`

## 运行方式

1. 先安装和更新依赖：

    ```powershell
    npm install
    ```

2. 运行测试版本：

    ```powershell
    npm run serve
    ```

3. 如果要发布：

    先进行打包：

    ```powershell
    npm run build
    ```

    然后使用某个前端服务器运行（例：`serve`）：

    ```powershell
    npm install -g serve@11.3.2
    ```

    ```powershell
    serve -s ./dist
    ```

## 前端确定需要的接口

-   所有列表相关（from to 或者 page 之类的）都是 0 开始计数。
-   `status`域的值只有`succeed`或`fail`。
-   由于浏览器原因，后端无法给请求设置 cookie。因此所有标注“需要登录”的函数都可以通过加上 username 和 password 域实现登录效果（每次都要）。

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

2. 获得 app 列表（GET/POST），需要已经登录

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
    			tokens: [
    				{
    					content: string,
    					created_time: string,
                        dead_time: string,
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

    如果不提供 type 域，则认为要获得 App 的详细信息

    "/app/detail"

    ```json
    {
        app_token: string,
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
    ```

6. 获得角色，权限或用户列表（GET）

    "/app/list"

    ```json
    {
    	type: 0,
        app_token: string,
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

8. 角色，用户，权限解联（POST）

    "/app/detach"

    ```json
    {
        app_token: string,
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

9. 改 key 的时候检查是否有冲突（GET）

    "/app/check"

    ```json
    {
        app_token: string,
        type: int,
        key: string,
    }
        =>
    {
        msg: string,
        status: string,
    }
    ```

10. 删除角色，用户，权限或者 app（POST）

    如果没有 type 域或不合法，则认为是要删除这个 app

    "/app/delete"

    ```json
    {
        app_token: string,
        keys: [string], ?
        type: int, ?
    }
        =>
    {
        status: string,
        msg: string,
    }
    ```

11. 新建用户，权限，角色，应用（POST）

    如果没有 app_token 域，则认为是要新建一些 app，此时需要用户已经登录

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
    	    }
    	],
    }
        =>
    {
        status: string,
        msg: string,
        list: [
            {
                name: string,
                key: string, ?
                tokens: [string], ?
                created_time: string,
        		description: string, ?
            }
        ]
    }
    ```

12. 显示用户，角色，权限的关联关系（GET）

    目标对象由 app_token, type, key 来定位，获得它所有的关联的 want_type 类型的对象数据

    "/app/show"

    ```json
    {
        app_token: string,
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
            }
        ]
    }
    ```

13. 获取某东西的总数（GET）

    "/app/total"

    ```json
    {
    	app_token: string,
    	type: int,
    }
    	=>
    {
    	msg: string,
    	status: string,
    	total: int,
    }
    ```

14. 获得 description，由于可能会很长所以专门分一个（GET）

    现在先不搞那么复杂，不会返回 page，也不会有分页逻辑

    "/app/description"

    ```json
    {
        app_token: string,
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

    如果没有 type 则认为要编辑 App 信息

    "/app/edit"

    ```json
    {
        app_token: string,
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

    会在 name 和 key 字段都进行搜索，支持中文

    "/app/search"

    ```json
    {
    	app_token: string,
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

```


简记：

- type为0表示用户，为1表示角色，为2表示权限，其它值会视为错误。
- 后面加?表示这个域可能不用提供或不会返回，对应不同的情况和逻辑（API简介会有专门的说明）。
- 如果返回信息里面有权限，该返回信息还会带有一个域是`child_permissions: []`，里面是所有子权限的信息，子权限信息本身也会带有`child_permissions`，层层嵌套，直到叶子权限时列表为空。
- 当进行关联和解联操作时，后端会自动把所有具有子权限的权限都转为它所有叶子权限的集合，然后再进行关联和解联。
- 如果一个角色关联了一个叶子权限，但是通过delete api删除了该权限的某个父权限，则该角色和该权限将自动解联。
- 不允许用户直接关联权限，所有关联都要通过角色层转发。
```
