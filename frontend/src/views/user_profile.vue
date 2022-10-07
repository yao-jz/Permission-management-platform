<template>
    <user_edit
        @close="close_user_edit_dialog"
        :visible="user_edit_dialog_visible"
    ></user_edit>
    <email
        :visible="email_edit_dialog_visible"
        @close="close_email_edit_dialog"
    ></email>
    <confirm_delete
        @close="close_user_delete_dialog"
        @confirm="confirm_user_delete"
        :visible="user_delete_dialog_visible"
    >
    </confirm_delete>
    <br /><br />
    <div class="user-profile user-card mb-4">
        <div class="card-body py-0">
            <div class="user-about-block m-0">
                <div class="row">
                    <div class="col-md-4 text-center mt-n5">
                        <div class="change-profile text-center">
                            <div class="dropdown d-inline-block">
                                <a
                                    class="dropdown-toggle"
                                    data-toggle="dropdown"
                                    aria-haspopup="true"
                                    aria-expanded="false"
                                >
                                    <div class="profile-dp">
                                        <div
                                            class="position-relative d-inline-block"
                                        >
                                            <img
                                                class="img-radius img-fluid wid-100"
                                                :src="avatar_url + now_time"
                                                alt="User image"
                                            />
                                        </div>
                                    </div>
                                    <div class="certificated-badge">
                                        <i
                                            class="fas fa-certificate text-c-blue bg-icon"
                                        ></i>
                                        <i
                                            class="fas fa-check front-icon text-white"
                                        ></i>
                                    </div>
                                </a>
                            </div>
                        </div>
                        <h5 class="mb-1">{{ old_user_name }}</h5>
                        <p class="mb-2 text-muted">管理员</p>
                        <br />
                    </div>
                    <div class="col-md-8 mt-md-4">
                        <div class="row">
                            <div class="col-md-6">
                                <a
                                    href="#!"
                                    class="mb-1 text-muted d-flex align-items-end text-h-primary"
                                    ><i class="feather icon-globe mr-2 f-18"></i
                                    >49.232.101.156</a
                                >
                                <div class="clearfix"></div>
                                <a
                                    href="#!"
                                    class="mb-1 text-muted d-flex align-items-end text-h-primary"
                                    ><i class="feather icon-mail mr-2 f-18"></i
                                    >{{ email }}</a
                                >
                                <div class="clearfix"></div>
                            </div>
                            <div class="col-md-6">
                                <div class="media">
                                    <i
                                        class="feather icon-map-pin mr-2 mt-1 f-18"
                                    ></i>
                                    <div class="media-body">
                                        <p class="mb-0 text-muted">软件工程</p>
                                        <p class="mb-0 text-muted">
                                            计算机科学与技术系
                                        </p>
                                        <p class="mb-0 text-muted">
                                            清华大学(Tsinghua University)
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="row">
        <div class="col-xl-3 col-md-6">
            <div class="card bg-c-red order-card">
                <div class="card-body">
                    <h6 class="text-white">创建的App</h6>
                    <h2 class="text-white">{{ app_number }}</h2>
                    <i class="card-icon feather icon-list"></i>
                </div>
            </div>
        </div>
        <div class="col-xl-3 col-md-6">
            <div class="card bg-c-blue order-card">
                <div class="card-body">
                    <h6 class="text-white">共享的App</h6>
                    <h2 class="text-white">{{ shared_app_number }}</h2>
                    <i class="card-icon feather icon-share"></i>
                </div>
            </div>
        </div>
        <div class="col-xl-3 col-md-6">
            <div class="card bg-c-yellow order-card">
                <div class="card-body">
                    <h6 class="text-white">收件箱</h6>
                    <h2 class="text-white">{{ inbox_num }}</h2>
                    <i class="card-icon feather icon-inbox"></i>
                </div>
            </div>
        </div>
        <div class="col-xl-3 col-md-6">
            <div class="card bg-c-green order-card">
                <div class="card-body">
                    <h6 class="text-white">管理的App</h6>
                    <h2 class="text-white">
                        {{ app_number + shared_app_number }}
                    </h2>
                    <i class="card-icon feather icon-command"></i>
                </div>
            </div>
        </div>
        <div class="col-md-4 order-md-2">
            <el-calendar> </el-calendar>
        </div>
        <div class="col-md-8 order-md-2">
            <div class="card">
                <div
                    class="card-body d-flex align-items-center justify-content-between"
                >
                    <h5 class="mb-0">个人信息</h5>
                </div>
                <div
                    class="card-body avatar border-top show"
                    id="pro-det-edit-1"
                >
                    <el-upload
                        class="avatar-uploader"
                        :action="post_avatar_url"
                        :show-file-list="false"
                        :on-success="handle_avatar_success"
                        :before-upload="before_avatar_upload"
                        :data="{
                            username: old_user_name,
                            password: old_pass_word,
                        }"
                    >
                        <img
                            v-if="avatar_url"
                            width="100"
                            :src="avatar_url + now_time"
                            class="avatar"
                        />
                        <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                    </el-upload>
                    点击上传新头像
                </div>
                <div class="card-body show" id="pro-det-edit-1">
                    <form>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >用户名</label
                            >
                            <div class="col-sm-9">{{ old_user_name }}</div>
                        </div>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >邮箱</label
                            >
                            <div class="col-sm-9">{{ email }}</div>
                        </div>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >地址</label
                            >
                            <div class="col-sm-9">
                                <p class="mb-0 text-muted">软件工程</p>
                                <p class="mb-0 text-muted">
                                    计算机科学与技术系
                                </p>
                                <p class="mb-0 text-muted">
                                    清华大学(Tsinghua University)
                                </p>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="card-body d-flex">
                    <div class="col-md-8 text-center mt-n5"></div>
                    <div class="col-md-1 text-center mt-n5">
                        <el-button type="primary" @click="open_user_edit_dialog"
                            >编辑</el-button
                        >
                    </div>
                    <div class="col-md-1 text-center mt-n5">
                        <el-button
                            type="primary"
                            @click="open_email_edit_dialog"
                            >邮箱</el-button
                        >
                    </div>
                    <div class="col-md-1 text-center mt-n5">
                        <el-button type="danger" @click="logout"
                            >登出</el-button
                        >
                    </div>
                    <div class="col-md-1 text-center mt-n5">
                        <el-button
                            type="danger"
                            @click="open_user_delete_dialog"
                            >删除</el-button
                        >
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import "../../public/assets/js/pcoded.min.js";
import "../../public/assets/js/ripple.js";
import "../../public/assets/js/vendor-all.min.js";
import "../../public/assets/js/plugins/jquery-ui.min.js";
import "../../public/assets/js/plugins/fullcalendar.min.js";
import {
    get_avatar,
    get_info,
    delete_user,
    receive_list,
    logout,
} from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
import GLOBAL from "../utils/global_variable.js";
import user_edit from "../components/user_edit.vue";
import email from "../components/email.vue";
import confirm_delete from "../components/confirm_delete.vue";
import { init_local } from "../utils/init_local.js";
export default {
    props: {
        avatar_url: "",
        user_name: "",
        app_number: 0,
        shared_app_number: 0,
    },
    components: {
        user_edit,
        email,
        confirm_delete,
    },
    data() {
        return {
            now_time: "?time=" + new Date().getTime(),
            form_label_width: "120px", //输入框宽度
            form: {
                user_name: "", //用户名
                pass_word: "", //密码
            },
            old_user_name: "", //旧用户名
            old_pass_word: "", //旧密码
            post_avatar_url: GLOBAL.url + "/user_info/avatar",
            email: "",
            inbox_num: 0,
            user_edit_dialog_visible: false,
            email_edit_dialog_visible: false,
            user_delete_dialog_visible: false,
        };
    },
    methods: {
        open_user_delete_dialog: function () {
            /**
             * @description: 打开删除用户确认对话框
             * @return void
             */
            this.user_delete_dialog_visible = true;
        },
        close_user_delete_dialog: function () {
            /**
             * @description: 关闭删除用户确认对话框
             * @return void
             */
            this.user_delete_dialog_visible = false;
        },
        confirm_user_delete: function () {
            /**
             * @description: 确认注销用户
             * @return void
             */
            var that = this;
            delete_user(this.old_user_name, this.old_pass_word).then(function (
                res
            ) {
                if (res.status == "fail") fail_msg(res.data.msg);
                else {
                    init_local();
                    localStorage.setItem("user_name", "");
                    localStorage.setItem("pass_word", "");
                    that.$router.replace({
                        name: "Login",
                    });
                    succeed_msg("注销用户成功");
                }
            });
        },
        open_email_edit_dialog: function () {
            this.email_edit_dialog_visible = true;
        },
        close_email_edit_dialog: function () {
            this.email = localStorage.getItem("email");
            this.email_edit_dialog_visible = false;
        },
        open_user_edit_dialog: function () {
            /**
             * @description: 打开用户编辑对话框
             * @return void
             */
            this.user_edit_dialog_visible = true;
        },
        logout: function () {
            /**
             * @description: 登出
             * @return 跳转登录页面
             */
            logout();
            localStorage.setItem("user_name", "");
            init_local();
            localStorage.setItem("pass_word", "");
            localStorage.setItem("app_key", "");
            this.$router.replace({
                //跳转至登录页面
                name: "Login",
            });
        },
        close_user_edit_dialog: function () {
            /**
             * @description: 关闭用户编辑对话框
             * @return void
             */
            this.old_user_name = localStorage.getItem("user_name");
            this.old_pass_word = localStorage.getItem("pass_word");
            // console.log(this.old_user_name, this.old_pass_word);
            this.user_edit_dialog_visible = false;
        },
        func: function () {
            // console.log("aosidfjoaisdjf");
        },
        init_form: function () {
            this.form.user_name = "";
            this.form.pass_word = "";
        },
        handle_avatar_success: function () {
            var that = this;
            get_avatar(
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word")
            ).then(function (res) {
                /**
                 * @description: 获得当前用户头像Url
                 * @return void
                 */
                // console.log("获得头像", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    localStorage.setItem("avatar_url", res.data.avatar);
                    that.avatar_url = GLOBAL.url + res.data.avatar;
                    that.now_time = "?time=" + new Date().getTime();
                }
            });
            location.reload();
        },
        before_avatar_upload: function (file) {
            const isJPG = file.type === "image/jpeg";
            const isLt2M = file.size / 1024 / 1024 < 2;

            if (!isJPG) {
                this.$message.error("上传头像图片只能是 JPG 格式!");
            }
            if (!isLt2M) {
                this.$message.error("上传头像图片大小不能超过 2MB!");
            }
            return isJPG && isLt2M;
        },
    },
    mounted() {
        var that = this;
        this.old_user_name = localStorage.getItem("user_name");
        this.old_pass_word = localStorage.getItem("pass_word");
        get_info(this.old_user_name, this.old_pass_word).then(function (res) {
            // console.log("get email", res);
            if (res.data.email) that.email = res.data.email;
            else that.email = "未绑定邮箱";
        });
        this.form.user_name = this.old_user_name;
        this.now_time = "?time=" + new Date().getTime();
        receive_list(
            localStorage.getItem("user_name"),
            localStorage.getItem("pass_word"),
            0,
            100
        ).then(function (res) {
            that.inbox_num = res.data.list.length;
        });
    },
};
</script>

<style>
.avatar {
    text-align: center;
}
</style>
