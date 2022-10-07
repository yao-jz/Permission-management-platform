/**
 * @file 前端所有的api函数
 * @author yaojianzhu
 */

import axios from "axios";
import qs from "qs";

axios.defaults.baseURL = "http://49.232.101.156:8000";
axios.defaults.withCredentials = true;

export function get_list(token, key, type, from_page, to_page) {
    /**
     * @description: 获得对应列表
     * @param {String} token
     * @param {Number} type
     * @param {Number} from_page
     * @param {Number} to_page
     * @return {
     *      list: Array,
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log(token, key, type, from_page, to_page);
    return axios({
        method: "GET",
        url:
            "/app/list?" +
            qs.stringify({
                type: type,
                app_token: token,
                app_key: key,
                from: from_page,
                to: to_page,
            }),
    });
}

export function attach(
    token,
    key,
    user_key_list,
    role_key_list,
    permission_key_list
) {
    /**
     * @description: 关联三类条目
     * @param {String} token
     * @param {String} key
     * @param {Array} user_key_list
     * @param {Array} role_key_list
     * @param {Array} permission_key_list
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log(user_key_list, role_key_list, permission_key_list);
    return axios.post("/app/attach", {
        app_token: token,
        app_key: key,
        user_keys: user_key_list,
        permission_keys: permission_key_list,
        role_keys: role_key_list,
    });
}

export function detach(
    token,
    key,
    user_key_list,
    role_key_list,
    permission_key_list
) {
    /**
     * @description: 用户、权限、角色解联
     * @param {String} token
     * @param {String} key
     * @param {Array} user_key_list
     * @param {Array} role_key_list
     * @param {Array} permission_key_list
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log(user_key_list, role_key_list, permission_key_list);
    return axios.post("/app/detach", {
        app_token: token,
        app_key: key,
        user_keys: user_key_list,
        permission_keys: permission_key_list,
        role_keys: role_key_list,
    });
}

export function check_key(token, key, type, new_key) {
    /**
     * @description: 检查key是否有冲突
     * @param {String} token
     * @param {String} key
     * @param {Number} type
     * @param {String} new_key
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log(token, type, new_key);
    return axios({
        method: "GET",
        url:
            "/app/check?" +
            qs.stringify({
                app_token: token,
                app_key: key,
                type: type,
                key: new_key,
            }),
    });
}

export function remove(token, key, key_list, type) {
    /**
     * @description: 删除条目
     * @param {String} token
     * @param {String} key
     * @param {Array} key_list
     * @param {Number} type
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log(token, key_list, type);
    return axios.post("/app/delete", {
        app_token: token,
        app_key: key,
        keys: key_list,
        type: type,
    });
}

export function add_app(l, user_name, pass_word) {
    /**
     * @description: 新建应用
     * @param {String} user_name
     * @param {Array} l
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     *      list: Array,
     * }
     */
    // console.log("新建应用");
    return axios.post("/app/add", {
        list: l,
        username: user_name,
        password: pass_word,
    });
}

export function add(token, key, type, list) {
    /**
     * @description: 新建用户角色权限
     * @param {String} token
     * @param {String} key
     * @param {Number} type
     * @param {Array} list
     * @return {
     *      msg: String,
     *      status: String,
     *      list: Array,
     * }
     */
    // console.log("新建一个东西", token, type, list);
    return axios.post("/app/add", {
        app_token: token,
        app_key: key,
        type: type,
        list: list,
    });
}

export function login(user_name, pass_word) {
    /**
     * @description: 登录
     * @param {String} user_name
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log("登录", user_name, pass_word);
    return axios.post("/login", {
        username: user_name,
        password: pass_word,
    });
}

export function get_app_list(user_name, pass_word) {
    /**
     * @description: 获得app列表
     * @param {String} user_name
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     *      list: Array,
     * }
     */
    // console.log("获得app列表");
    return axios({
        method: "GET",
        url:
            "/app?" +
            qs.stringify({
                username: user_name,
                password: pass_word,
            }),
    });
}

export function logout() {
    /**
     * @description: 登出
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log("用户登出");
    return axios.post("/logout", {});
}

export function register(user_name, pass_word) {
    /**
     * @description: 注册
     * @param {String} user_name
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    console.log("用户注册", user_name, pass_word);
    return axios.post("/register", {
        username: user_name,
        password: pass_word,
    });
}

export function get_detail(token, app_key, type, key) {
    /**
     * @description: 获得用户、角色、权限信息
     * @param {String} token
     * @param {String} app_key
     * @param {Number} type
     * @param {String} key
     * @return {
     *      msg: String,
     *      status: String,
     *      name: String,
     *      created_time: String,
     *      description: String,
     * }
     */
    // console.log(token, type, key);
    return axios({
        method: "GET",
        url:
            "/app/detail?" +
            qs.stringify({
                app_token: token,
                app_key: app_key,
                type: type,
                key: key,
            }),
    });
}

export function get_app_detail(token, key) {
    /**
     * @description: 获得应用信息
     * @param {String} token
     * @param {String} key
     * @return {
     *      msg: String,
     *      status: String,
     *      name: String,
     *      created_time: String,
     *      desciprtion: String,
     *      tokens: Array,
     * }
     */
    // console.log("获得应用信息");
    return axios({
        method: "GET",
        url:
            "/app/detail?" +
            qs.stringify({
                app_token: token,
                app_key: key,
            }),
    });
}

export function show_relative(token, app_key, type, want_type, key, from, to) {
    /**
     * @description: 显示关联关系
     * @param {String} token
     * @param {String} key
     * @param {Number} type
     * @param {Number} want_type
     * @param {String} key
     * @param {Number} from
     * @param {Number} to
     * @return {
     *      msg: String,
     *      status: String,
     *      list: Array,
     * }
     */
    // console.log("显示关联关系");
    return axios({
        method: "GET",
        url:
            "/app/show?" +
            qs.stringify({
                app_token: token,
                app_key: app_key,
                type: type,
                want_type: want_type,
                key: key,
                from: from,
                to: to,
            }),
    });
}

export function get_total(token, key, type) {
    /**
     * @description: 获得某条目的总数
     * @param {String} token
     * @param {String} key
     * @param {Number} type
     * @return {
     *      msg: String,
     *      status: String,
     *      total: Number,
     * }
     */
    // console.log("获得总数", token, type);
    return axios({
        method: "GET",
        url:
            "/app/total?" +
            qs.stringify({
                app_token: token,
                app_key: key,
                type: type,
            }),
    });
}

export function get_description(token, app_key, type, key) {
    /**
     * @description: 获得对象描述
     * @param {String} token
     * @param {String} app_key
     * @param {Number} type
     * @param {String} key
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log("获得description", token, type, key);
    return axios({
        method: "GET",
        url:
            "/app/detail?" +
            qs.stringify({
                app_token: token,
                app_key: app_key,
                type: type,
                key: key,
            }),
    });
}

export function edit(token, app_key, key, type, detail) {
    /**
     * @description: 编辑信息，采取覆盖策略
     * @param {String} token
     * @param {String} app_key
     * @param {String} key
     * @param {Number} type
     * @param {String} detail
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log("编辑信息", token, key, type, detail);
    return axios.post("/app/edit", {
        app_token: token,
        app_key: app_key,
        type: type,
        key: key,
        detail: detail,
    });
}

export function search_content(token, key, content, type, from, to) {
    /**
     * @description: 对name和key字段进行搜索
     * @param {String} token
     * @param {String} key
     * @param {String} content
     * @param {Number} type
     * @param {Number} from
     * @param {Number} to
     * @return {
     *      msg: String,
     *      status: String,
     *      total: Number,
     *      list: Array,
     * }
     */
    // console.log("搜索", token, content, type);
    return axios({
        method: "GET",
        url:
            "/app/search?" +
            qs.stringify({
                app_token: token,
                app_key: key,
                content: content,
                type: type,
                from: from,
                to: to,
            }),
    });
}

export function add_token(token, key, list, user_name, pass_word) {
    /**
     * @description: 新建app_token
     * @param {String} token
     * @param {String} key
     * @param {Array} list
     * @param {String} user_name
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     *      list: Array,
     * }
     */
    // console.log("新建app_token", token, list);
    return axios.post("/app/add", {
        app_token: token,
        app_key: key,
        username: user_name,
        password: pass_word,
        list: list,
        // list = [
        //     {
        //         alive_time: Number
        //     }
        // ]
    });
}

export function delete_token(list, user_name, pass_word) {
    /**
     * @description: 删除app_token
     * @param {Array} list
     * @param {String} user_name
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log("删除app_token", list);
    return axios.post("/token/delete", {
        list: list,
        username: user_name,
        password: pass_word,
    });
}

export function change_token(list, user_name, pass_word) {
    /**
     * @description: 修改app_token期限
     * @param {Array} list
     * @param {String} user_name
     * @param {String} pass_word
     * list = [
     *      {
     *          app_token: String,
     *          alive_time: Number,
     *      }
     * ]
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log("修改apptoken的期限", list, user_name, pass_word);
    return axios.post("/token/change", {
        list: list,
        username: user_name,
        password: pass_word,
    });
}

export function edit_user(
    old_user_name,
    old_password,
    new_user_name,
    new_password
) {
    /**
     * @description: 编辑系统用户信息
     * @param {String} old_user_name
     * @param {String} old_password
     * @param {String} new_user_name
     * @param {String} new_password
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    // console.log(
    //     "修改用户名和密码",
    //     old_user_name,
    //     old_password,
    //     new_user_name,
    //     new_password
    // );
    return axios.post("/user_info/edit", {
        username: old_user_name,
        password: old_password,
        detail: {
            username: new_user_name,
            password: new_password,
        },
    });
}

export function get_avatar(user_name, pass_word) {
    /**
     * @description: 编辑系统用户信息
     * @param {String} user_name
     * @param {String} pass_word
     * @return {
     *      msg: String,
     *      status: String,
     * }
     */
    return axios.post("/user_info/", {
        username: user_name,
        password: pass_word,
    });
}

export function delete_user(user_name, pass_word) {
    /**
     * @description: 永久注销用户
     * @param {String} user_name
     * @param {String} pass_word
     * @return void
     */
    return axios.post("/delete", {
        username: user_name,
        password: pass_word,
    });
}

export function verify_code(code, email) {
    /**
     * @description: 验证邮件验证码
     * @param {String} code
     * @param {String} email
     * @return void
     */
    return axios.post("/verify/code", {
        code: code,
        email: email,
    });
}

export function edit_email(user_name, pass_word, email) {
    /**
     * @description: 修改用户的邮箱，需要用户名和密码
     * @param {String} user_name
     * @param {String} pass_word
     * @param {String} email
     * @return void
     */
    return axios.post("/user_info/edit", {
        username: user_name,
        password: pass_word,
        detail: {
            username: "",
            password: "",
            email: email,
        },
    });
}

// 邮箱
export function get_info(user_name, pass_word) {
    /**
     * @description: 获得用户的邮箱
     * @param {String} user_name
     * @param {String} pass_word
     * @return void
     */
    return axios.post("/user_info/", {
        username: user_name,
        password: pass_word,
    });
}

export function set_role_time(token, key, user_keys, role_keys) {
    /**
     * @description: 修改用户与角色的绑定期限
     * @param {String} token
     * @param {String} key
     * @param {List} user_keys
     * @param {List} role_keys
     * @return void
     */
    return axios.post("/app/attach", {
        app_token: token,
        app_key: key,
        permission_keys: [],
        role_keys: role_keys,
        user_keys: user_keys,
    });
}

export function share_app(
    token,
    key,
    shared_user_name,
    access,
    user_name,
    pass_word
) {
    /**
     * @description: 向指定用户分享app
     * @param {String} token
     * @param {String} key
     * @param {String} user_name
     * @param {String} pass_word
     * @param {String} shared_user_name
     * @param {Number} access
     * @return Object
     */
    return axios.post("/app/share", {
        username: user_name,
        password: pass_word,
        app_token: token,
        app_key: key,
        share_username: shared_user_name,
        access: access,
    });
}

export function get_shared_app(user_name, pass_word) {
    /**
     * @description: 获得共享app的list
     * @param {String} user_name
     * @param {String} pass_word
     * @return Object
     */
    return axios.post("/app/shared_list", {
        username: user_name,
        password: pass_word,
    });
}

export function get_user_group(token, key) {
    /**
     * @description: 获得app的用户组
     * @param {String} token
     * @param {String} key
     * @return Object
     */
    return axios.post("/app/user_group", {
        app_key: key,
        app_token: token,
    });
}

export function change_token_access(list, user_name, pass_word) {
    /**
     * @description: 修改token的期限和权限
     * @param {Array} list
     * @param {String} user_name
     * @param {String} pass_word
     * @return Object
     */
    return axios.post("/token/change", {
        list: list,
        username: user_name,
        password: pass_word,
    });
}

export function sent_message(
    token,
    key,
    message,
    to_user_name,
    user_name,
    pass_word,
    title
) {
    /**
     * @description: 向同组用户发送信息
     * @param {String} token
     * @param {String} key
     * @param {String} message
     * @param {String} to_user_name
     * @param {String} user_name
     * @param {String} pass_word
     * @param {String} title
     * @return Object
     */
    return axios.post("/app/send_message", {
        app_key: key,
        app_token: token,
        message: message,
        to_username: to_user_name,
        username: user_name,
        password: pass_word,
        title: title,
    });
}

export function unshare(token, key, share_username, user_name, pass_word) {
    /**
     * @description: 取消app的共享
     * @param {String} token
     * @param {String} key
     * @param {String} share_username
     * @param {String} user_name
     * @param {String} pass_word
     * @return Object
     */
    return axios.post("/app/unshare", {
        app_token: token,
        app_key: key,
        share_username: share_username,
        username: user_name,
        password: pass_word,
    });
}

export function receive_list(user_name, pass_word, from, to) {
    /**
     * @description: 获得所有信息列表
     * @param {Number} from
     * @param {Number} to
     * @param {String} user_name
     * @param {String} pass_word
     * @return Object
     */
    return axios.post("/message/recv_list", {
        username: user_name,
        password: pass_word,
        from: from,
        to: to,
    });
}

export function sent_list(user_name, pass_word, from, to) {
    /**
     * @description: 获得自己已经发送的信息列表
     * @param {Number} from
     * @param {Number} to
     * @param {String} user_name
     * @param {String} pass_word
     * @return Object
     */
    return axios.post("/message/sended_list", {
        username: user_name,
        password: pass_word,
        from: from,
        to: to,
    });
}
