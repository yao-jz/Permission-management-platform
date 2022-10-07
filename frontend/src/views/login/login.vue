<!--
 * @FileDescription: 登录页
 * @Author: yaojianzhu
 * @Date: 2021.3.17
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021年04月27日16:22:06
 -->
<template>
    <div class="auth-wrapper align-items-stretch aut-bg-img">
        <div class="flex-grow-1">
            <div class="h-100 d-md-flex align-items-center auth-side-img">
                <div class="col-sm-10 auth-content w-auto">
                    <h1 class="text-white my-4">欢迎回来！</h1>
                    <h4 class="text-white font-weight-normal">
                        请登录企业权限管理系统
                    </h4>
                </div>
            </div>
            <div class="auth-side-form">
                <div class="auth-content">
                    <h3 class="mb-4 f-w-400">{{ title_list[type] }}</h3>
                    <el-form
                        ref="login_form"
                        :model="login_form"
                        class="login-form"
                        autocomplete="on"
                        label-position="left"
                    >
                        <el-form-item prop="user_name">
                            <div class="form-group mb-3">
                                <el-input
                                    ref="user_name"
                                    class="user_name"
                                    v-model="login_form.user_name"
                                    placeholder="用户名"
                                    name="user_name"
                                    type="text"
                                    tabindex="1"
                                    autocomplete="on"
                                />
                            </div>
                        </el-form-item>
                        <el-tooltip
                            v-model="caps_tooltip"
                            content="Caps lock is On"
                            placement="right"
                            manual
                        >
                            <el-form-item prop="pass_word">
                                <div class="form-group mb-4">
                                    <el-input
                                        ref="pass_word"
                                        class="pass_word"
                                        v-model="login_form.pass_word"
                                        placeholder="密码"
                                        name="pass_word"
                                        tabindex="2"
                                        autocomplete="on"
                                        show-password
                                    />
                                </div>
                            </el-form-item>
                        </el-tooltip>
                    </el-form>
                    <el-button
                        class="login_button"
                        v-if="type == 0"
                        style="width: 100%"
                        @click="login"
                        type="primary"
                        size="medium"
                        round
                        >登录</el-button
                    >
                    <el-button
                        class="register_button"
                        v-if="type == 1"
                        style="width: 100%"
                        @click="register"
                        type="primary"
                        size="medium"
                        round
                        >注册</el-button
                    >
                    <div class="text-center">
                        <div class="saprator my-4"><span>OR</span></div>
                        <p v-if="type == 0" class="mb-0 text-muted">
                            还没有账号？
                            <el-button
                                class="register_button"
                                style="width: 20%"
                                @click="register"
                                type="success"
                                round
                                >注册</el-button
                            >
                        </p>
                        <p v-if="type == 1" class="mb-0 text-muted">
                            已经有账号了？
                            <el-button
                                class="register_button"
                                style="width: 20%"
                                @click="return_to_login"
                                type="success"
                                round
                                >登录</el-button
                            >
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
</template>

<script>
import "../../../public/assets/js/pcoded.min.js";
import "../../../public/assets/js/ripple.js";
import "../../../public/assets/js/vendor-all.min.js";
import { login, register } from "../../utils/communication.js";
import { fail_msg } from "../../utils/msg.js";
import { init_local } from "../../utils/init_local.js";
export default {
    name: "Login",
    data() {
        return {
            title_list: [
                //标题类型
                "登录",
                "注册",
            ],
            caps_tooltip: false, //大写检查
            login_form: {
                //登录信息
                user_name: "",
                pass_word: "",
            },
            type: 0, //0表示这是登录页面，1表示注册页面
        };
    },
    methods: {
        login: function () {
            /**
             * @description: 登录函数
             * @return 如登录成功，跳转app列表页，否则清空当前form
             */
            var that = this;
            if (
                this.login_form.user_name == "" ||
                this.login_form.pass_word == ""
            ) {
                fail_msg("请检查用户名和密码是否均已填写");
                return;
            }
            // console.log(
            //     "login",
            //     this.login_form.user_name,
            //     this.login_form.pass_word
            // );
            login(this.login_form.user_name, this.login_form.pass_word).then(
                function (res) {
                    // console.log("login", res);
                    if (res.data.status == "succeed") {
                        //登陆成功，跳转到app_list页面
                        that.init_login();
                        localStorage.setItem(
                            "user_name",
                            that.login_form.user_name
                        );
                        localStorage.setItem(
                            "pass_word",
                            that.login_form.pass_word
                        );
                        that.$router.push({
                            name: "Userlist",
                        });
                    } else {
                        //登录失败，清空用户名和密码，错误提示
                        fail_msg(res.data.msg);
                        that.login_form.user_name = "";
                        that.login_form.pass_word = "";
                    }
                }
            );
        },
        register: function () {
            /**
             * @description: 注册
             * @return 如注册成功直接进入app列表页，否则提示错误
             */
            var that = this;
            if (this.type == 0) {
                //之前处于登录页面
                this.login_form.user_name = "";
                this.login_form.pass_word = "";
                this.type = 1;
            } else if (this.type == 1) {
                //已经处于注册页面，直接进行注册操作
                if (
                    this.login_form.user_name == "" ||
                    this.login_form.pass_word == ""
                ) {
                    fail_msg("请检查用户名和密码是否均已填写");
                    return;
                }
                register(
                    this.login_form.user_name,
                    this.login_form.pass_word
                ).then(function (res) {
                    // console.log("register", res);
                    if (res.data.status == "succeed") {
                        //注册成功，跳转到login页面
                        that.init_login();
                        localStorage.setItem(
                            "user_name",
                            that.login_form.user_name
                        );
                        localStorage.setItem(
                            "pass_word",
                            that.login_form.pass_word
                        );
                        that.$router.push({
                            name: "Userlist",
                        });
                    } else {
                        //注册失败，消息提示
                        fail_msg(res.data.msg);
                        that.login_form.user_name = "";
                        that.login_form.pass_word = "";
                    }
                });
            }
        },
        return_to_login: function () {
            /**
             * @description: 返回登录页面
             * @return void
             */
            this.login_form.user_name = "";
            this.login_form.pass_word = "";
            this.type = 0;
        },
        init_login(){
            init_local();
            localStorage.setItem("active_index", 0);
        },

    },
};
</script>

<style lang="scss">
$bg: #283443;
$light_gray: #283443;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
    // .login-container .el-input input {
    //     color: $cursor;
    // }
}

/* reset element-ui css */
.login-container {
    padding-top: 0px;
    background-position: right top;
    background-repeat: no-repeat;
    background-attachment: scroll;
    background-size: cover;
    background-image: url(/img/login_bg.12181f13.jpg);
    .login-body {
        max-width: 500px;
        margin: 0 auto;
        // background-color: #efefe8;
    }
    .el-input {
        display: inline-block;
        height: 47px;
        width: 100%;
        .el-input__inner {
            height: 46px;
            line-height: 46px;
        }
        .el-input__suffix {
            line-height: 46px;
        }
    }

    .c-btn {
        margin-top: 10px;
    }
}
</style>

<style lang="scss" scoped>
$bg: #efefe8;
$dark_gray: #889aa4;
$light_gray: #eee;

.c-login__bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow-x: hidden;
    background-position: right top;
    background-repeat: no-repeat;
    background-attachment: scroll;
    background-size: cover;
    background-image: url(../../../static/login_bg.jpg);
}

.login-container {
    min-height: 100%;
    width: 100%;
    background-color: $bg;
    overflow: hidden;

    .login-form {
        position: relative;
        width: 100%;
        max-width: 100%;
        padding: 50px 0px;
        margin: 0 auto;
        overflow: hidden;
        background-color: #fff;
    }

    .tips {
        font-size: 14px;
        color: #969696;
        margin-bottom: 10px;
        span {
            &:first-of-type {
                margin-right: 16px;
            }
        }
    }

    .svg-container {
        padding: 6px 5px 6px 15px;
        color: $dark_gray;
        vertical-align: middle;
        width: 30px;
        display: inline-block;
    }

    .title-container {
        position: relative;
        .title {
            font-size: 26px;
            margin: 0px auto 40px auto;
            text-align: center;
            font-weight: bold;
        }
    }

    .show-pwd {
        position: absolute;
        right: 10px;
        top: 7px;
        font-size: 16px;
        color: $dark_gray;
        cursor: pointer;
        user-select: none;
    }

    .thirdparty-button {
        position: absolute;
        right: 0;
        bottom: 6px;
    }

    @media only screen and (max-width: 470px) {
        .thirdparty-button {
            display: none;
        }
    }
}

.aut-bg-img {
    background-image: url("../../../public/assets/images/auth/img-auth-big.jpg");
    background-size: cover;
    background-attachment: fixed;
    background-position: center;
}
</style>
