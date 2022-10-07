<template>
    <share_dialog
        @close="close_share_dialog"
        :visible="share_dialog_visible"
        :token="selected_token"
    >
    </share_dialog>
    <token_detail
        @close="close_app_token_dialog"
        :visible="token_dialog_visible"
        :token="selected_token"
    ></token_detail>
    <app_dialog
        @new_app="new_app"
        @edit="edit"
        @close="add_closed"
        :visible="add_app_dialog_visible"
        :type="dialog_type"
    ></app_dialog>
    <app_dialog
        @new_app="new_app"
        @edit="edit"
        @close="edit_closed"
        :visible="edit_app_dialog_visible"
        :token="selected_token"
        :type="dialog_type"
        :state="state"
    ></app_dialog>
    <div v-for="item in bundled_app_list" :key="item" class="row">
        <div v-if="item[0]" class="col-md-8 col-xl-6">
            <div class="card">
                <h5 class="card-header">{{ item[0].name }}</h5>
                <div class="card-body">
                    <h5 class="card-title">App信息</h5>
                    <form>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >创建时间：</label
                            >
                            <div class="col-sm-9">
                                {{ item[0].created_time }}
                            </div>
                        </div>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >创建用户：</label
                            >
                            <div class="col-sm-9">
                                {{ item[0].created_user }}
                            </div>
                        </div>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >描述：</label
                            >
                            <div class="col-sm-9">
                                {{ item[0].description }}
                            </div>
                        </div>
                        <div style="text-align: right">
                            <el-button
                                type="primary"
                                square
                                @click="
                                    set_token(
                                        item[0].tokens[0].content,
                                        item[0].key
                                    )
                                "
                                icon="el-icon-user"
                                >管理
                            </el-button>
                            <el-button
                                v-if="type == 0"
                                type="primary"
                                square
                                @click="
                                    open_share_dialog(
                                        item[0].tokens[0].content,
                                        item[0].key
                                    )
                                "
                                icon="el-icon-share"
                                >分享
                            </el-button>
                            <el-button
                                type="success"
                                square
                                @click="
                                    show_app_token(item[0].tokens, item[0].key)
                                "
                                icon="el-icon-lock"
                                >查看token
                            </el-button>
                            <el-button
                                class="edit_app_button"
                                @click="
                                    edit_app(item[0].tokens[0].content, item[0])
                                "
                                square
                                icon="el-icon-edit"
                                >编辑</el-button
                            >
                            <el-popconfirm
                                title="确定删除吗？"
                                @confirm="
                                    delete_app(
                                        item[0].tokens[0].content,
                                        item[0]
                                    )
                                "
                            >
                                <template #reference>
                                    <el-button
                                        class="delete_app_button"
                                        type="danger"
                                        square
                                        icon="el-icon-delete"
                                        >删除</el-button
                                    >
                                </template>
                            </el-popconfirm>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        <div v-if="item[1]" class="col-md-8 col-xl-6">
            <div class="card">
                <h5 class="card-header">{{ item[1].name }}</h5>
                <div class="card-body">
                    <h5 class="card-title">App信息</h5>
                    <form>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >创建时间：</label
                            >
                            <div class="col-sm-9">
                                {{ item[1].created_time }}
                            </div>
                        </div>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >创建用户：</label
                            >
                            <div class="col-sm-9">
                                {{ item[1].created_user }}
                            </div>
                        </div>
                        <div class="form-group row">
                            <label
                                class="col-sm-3 col-form-label font-weight-bolder"
                                >描述：</label
                            >
                            <div class="col-sm-9">
                                {{ item[1].description }}
                            </div>
                        </div>

                        <div style="text-align: right">
                            <el-button
                                type="primary"
                                square
                                @click="
                                    set_token(
                                        item[1].tokens[0].content,
                                        item[1].key
                                    )
                                "
                                icon="el-icon-user"
                                >管理
                            </el-button>
                            <el-button
                                v-if="type == 0"
                                type="primary"
                                square
                                @click="
                                    open_share_dialog(
                                        item[1].tokens[0].content,
                                        item[1].key
                                    )
                                "
                                icon="el-icon-share"
                                >分享
                            </el-button>
                            <el-button
                                type="success"
                                square
                                @click="
                                    show_app_token(item[1].tokens, item[1].key)
                                "
                                icon="el-icon-lock"
                                >查看token
                            </el-button>
                            <el-button
                                class="edit_app_button"
                                @click="
                                    edit_app(item[1].tokens[0].content, item[1])
                                "
                                square
                                icon="el-icon-edit"
                                >编辑</el-button
                            >
                            <el-popconfirm
                                title="确定删除吗？"
                                @confirm="
                                    delete_app(
                                        item[1].tokens[0].content,
                                        item[1]
                                    )
                                "
                            >
                                <template #reference>
                                    <el-button
                                        class="delete_app_button"
                                        type="danger"
                                        square
                                        icon="el-icon-delete"
                                        >删除</el-button
                                    >
                                </template>
                            </el-popconfirm>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { add_app, edit, remove } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
import token_detail from "../components/token_detail.vue";
import app_dialog from "../components/add_app_dialog.vue";
import share_dialog from "../components/share_dialog.vue";
export default {
    props: {
        app_list: Array,
        type: 0, //0表示是自己创建的applist，1表示共享的app list
    },
    emits: ["update", "show_detail"],
    data() {
        return {
            bundled_app_list: [],
            selected_token: "",
            user_name: "",
            pass_word: "",
            token_dialog_visible: false,
            edit_app_dialog_visible: false,
            add_app_dialog_visible: false, //增加app
            dialog_type: 0, //对话框类型，0表示添加对话框，1表示编辑对话框
            state: {
                //app信息
                name: "",
                description: "",
                key: "",
            },
            share_dialog_visible: false,
        };
    },
    components: {
        token_detail,
        app_dialog,
        share_dialog,
    },
    methods: {
        close_share_dialog: function () {
            this.selected_token = "";
            localStorage.setItem("app_key", "");
            this.share_dialog_visible = false;
        },
        open_share_dialog: function (token, key) {
            this.selected_token = token;
            localStorage.setItem("app_key", key);
            this.share_dialog_visible = true;
        },
        open_new_app: function () {
            /**
             * @description: 打开新建app的对话框
             * @return void
             */
            this.dialog_type = 0; //对话框种类为0，表示新建条目
            this.add_app_dialog_visible = true; //设置对话框可见
        },
        new_app: function (name, description) {
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
                        description: description,
                    },
                ],
                this.user_name,
                this.pass_word
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("新增app成功");
                that.$emit("update"); //新建app后，更新app列表
            });
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
                key: key,
                description: description,
            }).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("编辑已保存");
                that.$emit("update");
            });
        },
        edit_app: function (token, item) {
            /**
             * @description: 打开编辑app对话框
             * @param {String} token
             * @param {Object} item
             * @return void
             */
            localStorage.setItem("app_key", item.key);
            console.log("进入edit", item);
            this.state.name = item.name;
            this.state.description = item.description;
            this.state.key = item.key;
            this.dialog_type = 1; //设置对话框种类为1
            this.selected_token = token;
            this.edit_app_dialog_visible = true; //显示编辑对话框
        },
        add_closed: function () {
            /**
             * @description: 关闭添加app对话框
             * @return void
             */
            this.add_app_dialog_visible = false;
        },
        edit_closed: function () {
            /**
             * @description: 关闭编辑app对话框
             * @return void
             */
            this.edit_app_dialog_visible = false;
            this.selected_token = "";
            localStorage.setItem("app_key", "");
        },
        show_app_token(tokens, key) {
            /**
             * @description: 查看app的所有token信息
             * @param {Array} tokens
             * @return void
             */
            if (!tokens) fail_msg("你没有权限这样做！");
            // console.log("查看tokens: ", tokens);
            localStorage.setItem("app_key", key);
            this.selected_token = tokens[0].content;
            this.token_dialog_visible = true;
        },
        close_app_token_dialog() {
            /**
             * @description: 关闭查看token信息对话框
             * @return void
             */
            this.$emit("update");
            localStorage.setItem("app_key", "");
            this.token_dialog_visible = false;
            this.selected_token = "";
        },
        set_token: function (token, key) {
            /**
             * @description: 设置当前的app_token，用于跳转到对应的app列表页
             * @param {String} token
             * @return 页面跳转
             */
            localStorage.setItem("app_token", token);
            localStorage.setItem("app_key", key);
            this.$emit("show_detail", 0);
            // this.$router.push({
            //     //转至detail页面
            //     path: "/detail",
            // });
        },
        delete_app: function (token, item) {
            /**
             * @description: 删除app
             * @param {String} token
             * @return void
             */
            var that = this;
            // console.log(token, item);
            remove(token, item.key, [], "").then(function (res) {
                // console.log(res);
                if (res.data.status == "succeed") {
                    succeed_msg("删除app成功");
                } else {
                    fail_msg(res.data.msg);
                }
                that.$emit("update");
            });
        },
    },
    mounted() {
        this.bundled_app_list = [];
        var temp_list = [];
        for (var i = 0; i < this.app_list.length; i++) {
            temp_list.push(this.app_list[i]);
            if (i % 2 == 1) {
                this.bundled_app_list.push(temp_list);
                temp_list = [];
            } else if (i == this.app_list.length - 1) {
                this.bundled_app_list.push(temp_list);
            }
        }
        this.user_name = localStorage.getItem("user_name");
        this.pass_word = localStorage.getItem("pass_word");
    },
    watch: {
        app_list: {
            handler() {
                this.bundled_app_list = [];
                var temp_list = [];
                for (var i = 0; i < this.app_list.length; i++) {
                    temp_list.push(this.app_list[i]);
                    if (i % 2 == 1) {
                        this.bundled_app_list.push(temp_list);
                        temp_list = [];
                    } else if (i == this.app_list.length - 1) {
                        this.bundled_app_list.push(temp_list);
                    }
                }
            },
        },
    },
};
</script>
