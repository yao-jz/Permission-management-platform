<!--
 * @FileDescription: app列表页，支持展示所有的app
 * @Author: yaojianzhu
 * @Date: 2021.3.17
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.5.1
 -->
<template>
    <div class="container box-layout">
        <app_dialog
            @new_app="new_app"
            @edit="edit"
            @close="add_closed"
            :visible="add_app_dialog_visible"
            :type="dialog_type"
        ></app_dialog>
        <header
            class="navbar pcoded-header navbar-expand-lg navbar-light header-blue"
        >
            <div class="m-header">
                <div
                    style="padding-left: 0px; font-size: 25px"
                    face="黑体"
                    color="#000000"
                >
                    <strong>权限管理平台</strong>
                    <a class="mobile-menu" id="mobile-collapse" href="#!"
                        ><span></span
                    ></a>
                </div>
            </div>
        </header>

        <nav :class="nav_class_status[nav_status]">
            <div class="navbar-wrapper">
                <div class="navbar-content scroll-div">
                    <div class="">
                        <div class="main-menu-header">
                            <img
                                class="img-radius"
                                :src="avatar_url + now_time"
                                alt="User-Profile-Image"
                            />
                            <div class="user-details">
                                <div id="more-details">{{ user_name }}</div>
                            </div>
                        </div>
                    </div>
                    <ul class="nav pcoded-inner-navbar">
                        <li class="nav-item pcoded-menu-caption">
                            <label>用户</label>
                        </li>
                        <li
                            @click="active(0)"
                            class="nav-item"
                            :class="active_list[0]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-user"></i></span
                                ><span class="pcoded-mtext">用户信息</span></a
                            >
                        </li>
                        <li
                            @click="active(1)"
                            class="nav-item"
                            :class="active_list[1]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-inbox"></i></span
                                ><span class="pcoded-mtext">消息页面</span></a
                            >
                        </li>
                        <li class="nav-item pcoded-menu-caption">
                            <label>App</label>
                        </li>
                        <li
                            @click="active(5)"
                            class="nav-item"
                            :class="active_list[5]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-home"></i></span
                                ><span class="pcoded-mtext">拥有的App</span></a
                            >
                        </li>
                        <li
                            @click="active(6)"
                            class="nav-item"
                            :class="active_list[6]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-share-2"></i></span
                                ><span class="pcoded-mtext">共享的App</span></a
                            >
                        </li>
                        <li
                            v-if="app_available"
                            class="nav-item pcoded-menu-caption"
                        >
                            <label>App管理</label>
                        </li>
                        <li
                            v-if="app_available"
                            @click="active(7)"
                            class="nav-item"
                            :class="active_list[7]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-grid"></i></span
                                ><span class="pcoded-mtext">App详情</span></a
                            >
                        </li>
                        <li
                            v-if="app_available"
                            @click="active(8)"
                            class="nav-item"
                            :class="active_list[8]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-users"></i></span
                                ><span class="pcoded-mtext">用户</span></a
                            >
                        </li>
                        <li
                            v-if="app_available"
                            @click="active(9)"
                            class="nav-item"
                            :class="active_list[9]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-gitlab"></i></span
                                ><span class="pcoded-mtext">角色</span></a
                            >
                        </li>
                        <li
                            v-if="app_available"
                            @click="active(10)"
                            class="nav-item"
                            :class="active_list[10]"
                        >
                            <a href="#!" class="nav-link"
                                ><span class="pcoded-micon"
                                    ><i class="feather icon-lock"></i></span
                                ><span class="pcoded-mtext">权限</span></a
                            >
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

        <div class="pcoded-main-container">
            <div class="pcoded-content">
                <div class="page-header">
                    <div class="page-block">
                        <div class="row align-items-center">
                            <div class="col-md-10">
                                <div class="page-header-title">
                                    <h5 class="m-b-10">
                                        {{ label_title[active_index] }}
                                    </h5>
                                </div>
                                <ul class="breadcrumb">
                                    <li class="breadcrumb-item">
                                        <a href="#!"
                                            ><i
                                                class="feather icon-align-left"
                                            ></i
                                        ></a>
                                    </li>
                                    <li class="breadcrumb-item">
                                        <a href="#!">{{
                                            header_title[active_index]
                                        }}</a>
                                    </li>
                                </ul>
                            </div>
                            <div v-if="active_index == 5" class="col-md-2">
                                <el-button
                                    class="add_app_button"
                                    type="success"
                                    square
                                    @click="open_new_app"
                                    icon="el-icon-document-add"
                                    >新建app</el-button
                                >
                            </div>
                        </div>
                    </div>
                </div>

                <user_profile
                    v-if="active_index == 0"
                    :app_number="app_number"
                    :shared_app_number="shared_app_number"
                    :user_name="user_name"
                    :avatar_url="avatar_url"
                ></user_profile>
                <have_app_list
                    v-if="active_index == 5"
                    :type="active_index - 5"
                    @update="get_list"
                    @show_detail="show_detail"
                    :app_list="app_list"
                ></have_app_list>
                <have_app_list
                    v-if="active_index == 6"
                    :type="active_index - 5"
                    @update="get_shared_list"
                    @show_detail="show_detail"
                    :app_list="shared_app_list"
                ></have_app_list>
                <message_page
                    @close_msg_send="close_msg_send"
                    v-if="active_index == 1"
                    :send="send"
                    :send_token="send_msg_token"
                    :send_key="send_msg_key"
                    :send_to="send_to"
                >
                </message_page>
                <div v-if="app_available" class="row">
                    <table_page
                        @send_msg="turn_to_send_msg"
                        :token="selected_token"
                        :app_type="app_type"
                        :type="active_index - 8"
                    ></table_page>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import "../../public/assets/js/pcoded.min.js";
import "../../public/assets/js/ripple.js";
import "../../public/assets/js/vendor-all.min.js";
import user_profile from "./user_profile.vue";
import app_dialog from "../components/add_app_dialog";
import { fail_msg, succeed_msg } from "../utils/msg.js";
import { init_local } from "../utils/init_local.js";
import token_detail from "../components/token_detail.vue";
import confirm_delete from "../components/confirm_delete.vue";
import { parser, parse_to_string } from "../utils/time_parser.js";
import GLOBAL from "../utils/global_variable.js";
import message_page from "./message.vue";
import {
    get_app_list,
    edit,
    add_app,
    get_avatar,
    get_shared_app,
} from "../utils/communication.js";
import have_app_list from "./have_app_list.vue";
import table_page from "../components/table.vue";
export default {
    props: {
        token: "",
    },
    components: {
        app_dialog,
        token_detail,
        confirm_delete,
        user_profile,
        have_app_list,
        table_page,
        message_page,
    },
    data() {
        return {
            app_list: [],
            shared_app_list: [],
            shared_app_number: 0,
            avatar_url: "",
            user_name: "", //用户名
            pass_word: "", //密码
            app_number: 0, //app数量
            add_app_dialog_visible: false, //增加app对话框
            edit_app_dialog_visible: false, //编辑app对话框
            dialog_type: 0, //对话框类型，0表示添加对话框，1表示编辑对话框
            selected_token: "", //选择的app的token
            state: {
                //app信息
                name: "",
                description: "",
            },
            user_edit_dialog_visible: false, //编辑用户信息对话框是否显示
            user_delete_dialog_visible: false, //删除用户对话框是否显示
            now_time: "?time=" + new Date().getTime(),
            email_edit_dialog_visible: false, //邮箱编辑对话框是否显示

            active_list: ["", "", "", "", "", "", "", "", "", "", ""],
            active_index: Number,
            label_title: [
                "用户",
                "用户",
                "文档",
                "文档",
                "文档",
                "App",
                "App",
                "App详情",
                "App详情",
                "App详情",
                "App详情",
            ],
            header_title: [
                "用户信息",
                "消息页面",
                "前端使用文档",
                "后端使用文档",
                "API文档",
                "拥有的App",
                "共享的App",
                "App信息",
                "用户",
                "角色",
                "权限",
            ],
            nav_class_status: [
                "pcoded-navbar menu-light",
                "pcoded-navbar menu-light mob-open",
            ],
            nav_status: 0,
            app_available: false, //是否可以看到app管理页面
            app_type: 0, //0表示自己的app，否则是共享的app

            send_msg_token: "",
            send_msg_key: "",
            send_to: "", //发送给谁
            send: false,
        };
    },
    computed: {},
    mounted() {
        for (var i = 0; i < this.active_list.length; i++) {
            this.active_list[i] = "";
        }
        this.selected_token = localStorage.getItem("app_token");
        this.active_index = localStorage.getItem("active_index");
        if (this.active_index > 6) this.app_available = true;
        this.active_list[this.active_index] = "active";
        init_local();
        localStorage.setItem("page_index", 0);
        this.user_name = localStorage.getItem("user_name");
        this.pass_word = localStorage.getItem("pass_word");
        // console.log(this.user_name, this.pass_word);
        this.set_avatar();
        if (this.user_name == "" || this.pass_word == "") {
            //当没有用户名或密码时
            this.$router.replace({
                name: "Login",
            });
        } else {
            this.get_list();
            this.get_shared_list();
        }
        this.now_time = "?time=" + new Date().getTime();
    },
    methods: {
        close_msg_send: function () {
            this.send_msg_token = "";
            this.send_msg_key = "";
            this.send = false;
            this.send_to = "";
        },
        turn_to_send_msg: function (token, key, who) {
            // console.log("向", token, key, who, "发送消息");
            this.send_to = who;
            this.send_msg_token = token;
            this.send_msg_key = key;
            this.send = true;
            this.active(1);
        },
        show_detail: function (app_type) {
            this.active_index = 7;
            this.app_available = true;
            this.app_type = app_type;
            this.selected_token = localStorage.getItem("app_token");
            for (var i = 0; i < this.active_list.length; i++) {
                this.active_list[i] = "";
            }
            this.active_list[this.active_index] = "active";
        },
        change_nav: function () {
            // console.log(this.nav_status);
            this.nav_status = 1 - this.nav_status;
        },
        active: function (num) {
            if (num != 1) this.send = false;
            if (num < 7) {
                localStorage.setItem("app_key", "");
                localStorage.setItem("app_token", "");
                this.app_available = false;
                this.app_type = 0;
            }
            for (var i = 0; i < 11; i++) {
                this.active_list[i] = "";
            }
            this.active_list[num] = "active";
            this.active_index = num;
            localStorage.setItem("active_index", this.active_index);
        },
        set_avatar: function () {
            var that = this;
            get_avatar(this.user_name, this.pass_word).then(function (res) {
                /**
                 * @description: 获得当前用户头像Url
                 * @return void
                 */
                // console.log("获得头像", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    localStorage.setItem("avatar_url", res.data.avatar);
                    that.avatar_url =
                        GLOBAL.url + localStorage.getItem("avatar_url");
                    that.now_time = "?time=" + new Date().getTime();
                }
            });
        },
        get_list: function () {
            /**
             * @description: 获得app列表
             * @return void
             */
            var that = this;
            get_app_list(this.user_name, this.pass_word).then(function (res) {
                // console.log("get_app_list", res);
                if (res.data.status == "succeed") {
                    var temp_app_list = res.data.list; //更新app列表
                    for (var i = 0; i < temp_app_list.length; i++) {
                        temp_app_list[i].created_time = parse_to_string(
                            parser(temp_app_list[i].created_time)
                        );
                    }
                    that.app_list = temp_app_list;
                    that.app_number = that.app_list.length; //获得app数目
                } else {
                    fail_msg(res.data.msg); //错误信息
                }
            });
        },
        get_shared_list: function () {
            /**
             * @description: 获得共享app列表
             * @return void
             */
            var that = this;
            get_shared_app(this.user_name, this.pass_word).then(function (res) {
                // console.log("获得共享app", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    var temp_app_list = res.data.list; //更新app列表
                    for (var i = 0; i < temp_app_list.length; i++) {
                        temp_app_list[i].created_time = parse_to_string(
                            parser(temp_app_list[i].created_time)
                        );
                    }
                    that.shared_app_list = temp_app_list;
                    that.shared_app_number = that.shared_app_list.length; //获得app数目
                }
            });
        },
        new_app: function (name, key, description) {
            /**
             * @description: 新建app，提供app的名字和描述
             * @param {String} name
             * @param {String} description
             * @return void
             */
            var that = this;
            add_app(
                [
                    {
                        name: name,
                        app_key: key,
                        description: description,
                    },
                ],
                this.user_name,
                this.pass_word
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    if(res.data.msg) fail_msg(res.data.msg);
                    else succeed_msg("新增app成功");
                }
                that.get_list(); //新建app后，更新app列表
                that.get_shared_list();
            });
        },
        open_new_app: function () {
            /**
             * @description: 打开新建app的对话框
             * @return void
             */
            this.dialog_type = 0; //对话框种类为0，表示新建条目
            this.add_app_dialog_visible = true; //设置对话框可见
        },
        add_closed: function () {
            /**
             * @description: 关闭添加app对话框
             * @return void
             */
            this.add_app_dialog_visible = false;
        },
        edit: function (name, key, description, token) {
            /**
             * @description: 编辑app
             * @param {String} name
             * @param {String} description
             * @param {String} token
             * @return void
             */
            var that = this;
            edit(token, localStorage.getItem("app_key"), "", "", {
                name: name,
                app_key: key,
                description: description,
            }).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    if(res.data.msg) fail_msg(res.data.msg);
                    else succeed_msg("编辑已保存");
                }
                that.get_list();
                that.get_shared_list();
            });
        },
    },
};
</script>

<style lang="scss" scoped>
::v-deep .left .el-card__header {
    padding: 8px 10px;
}
::v-deep .left .el-card__body {
    padding: 0px;
}
::v-deep .right .el-card__body {
    padding: 0px;
}
.c-header {
    height: 50px;
    box-shadow: 0 1px 4px rgb(0 21 41 / 8%);
}

.content {
    padding: 0 20px;
    margin-top: 20px;
    .card-header {
        text-align: center;
        .h-title {
            margin-top: 10px;
        }
    }
    .card-content {
        padding: 16px 10px;
        border-bottom: 1px solid #ebeef5;
        color: rgb(83, 83, 202);
    }
    .center,
    .right {
        .box-card {
            margin-bottom: 20px;
        }
    }
    .right {
        .card-con-head {
            padding: 16px 10px;
            background-color: #ebeef5;
        }
        .r-card-warp {
            display: flex;
            justify-content: space-between;
        }
        .card-c-text {
            margin-top: 10px;
            color: #666;
            width: 80%;
        }
    }
}

.card-c-t {
    color: rgb(83, 83, 202);
}
</style>
