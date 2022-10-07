<!--
 * @FileDescription: app_token列表页
 * @Author: yaojianzhu
 * @Date: 2021.3.29
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.30
 -->
<template>
    <access_dialog
        @close="close_access_dialog"
        :visible="access_dialog_visible"
        :token="selected_token"
        :int="selected_token_access"
        :self="max_access"
    ></access_dialog>
    <modify_token_dialog
        @update="update_tokens"
        @close="close_add_dialog"
        :visible="add_token_dialog_visible"
        :selected_token="modified_token"
        :type="dialog_type"
    ></modify_token_dialog>
    <el-dialog @close="close" title="token列表" v-model="visible" id="test_dialog">
        <el-button round type="primary" @click="open_add_dialog"
            >新建token</el-button
        >
        <el-table :data="token_list">
            <el-table-column property="content" label="token"></el-table-column>

            <el-table-column label="权限">
                <template #default="scope">{{
                    access_title[scope.row.access]
                }}</template></el-table-column
            >
            <el-table-column
                property="dead_time"
                label="到期时间"
            ></el-table-column>
            <el-table-column>
                <template #default="scope">
                    <el-button
                        @click="open_edit_dialog(scope)"
                        square
                        type="success"
                        >设置时长</el-button
                    >
                </template>
            </el-table-column>
            <el-table-column>
                <template #default="scope">
                    <el-button
                        @click="open_access_dialog(scope)"
                        square
                        type="primary"
                        >设置权限</el-button
                    >
                </template>
            </el-table-column>
            <el-table-column>
                <template #default="scope">
                    <el-popconfirm
                        title="确定要删除这个token吗"
                        @confirm="remove_token(scope.row)"
                    >
                        <template #reference>
                            <el-button>删除</el-button>
                        </template>
                    </el-popconfirm>
                </template>
            </el-table-column>
        </el-table>
    </el-dialog>
</template>

<script>
import { delete_token, get_app_detail } from "../utils/communication.js";
import modify_token_dialog from "./modify_token_dialog.vue";
import { fail_msg, succeed_msg } from "../utils/msg.js";
import { parser, parse_to_string } from "../utils/time_parser.js";
import access_dialog from "./access_dialog.vue";
export default {
    name: "token_detail",
    props: {
        token: String, //当前选择的token
        visible: false, //当前页面是否可见
    },
    components: {
        modify_token_dialog,
        access_dialog,
    },
    emits: ["close"],
    data() {
        return {
            max_access: 0,
            add_token_dialog_visible: false, //添加token对话框，只需要显示添加几天
            edit_token_time_dialog_visible: false, //编辑app_token的时长
            user_name: String, //用户名
            pass_word: String, //密码
            token_list: [], //展示的token 列表
            dialog_type: Number, //表示子对话框的类型，0为添加，1为编辑
            loading: true,
            modified_token: "", //正在修改的token
            access_title: ["all", "admin", "add", "edit", "see"],
            selected_token: "",
            access_dialog_visible: false,
            selected_token_access: 0,
        };
    },
    methods: {
        open_access_dialog: function (value) {
            this.selected_token_access = value.row.access;
            this.selected_token = value.row.content;
            this.access_dialog_visible = true;
        },
        close_access_dialog: function () {
            this.access_dialog_visible = false;
            this.update_tokens();
        },
        open_add_dialog: function () {
            /**
             * @description: 打开添加token对话框
             * @return void
             */
            this.dialog_type = 0;
            this.modified_token = this.token;
            this.add_token_dialog_visible = true;
        },
        close_add_dialog: function () {
            /**
             * @description: 关闭添加token对话框
             * @return void
             */
            this.add_token_dialog_visible = false;
        },
        open_edit_dialog: function (val) {
            /**
             * @description: 打开token编辑对话框
             * @return void
             */
            this.modified_token = val.row.content;
            this.dialog_type = 1;
            this.add_token_dialog_visible = true;
        },
        remove_token: function (token) {
            /**
             * @description: 删除指定的token
             * @param {String} token
             * @return void
             */
            var that = this;
            delete_token(
                [
                    {
                        app_token: token.content,
                        app_key: localStorage.getItem("app_key"),
                    },
                ],
                this.user_name,
                this.pass_word
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    if (res.data.msg) fail_msg(res.data.msg);
                    else succeed_msg("删除成功");
                }
                if (that.token != token.content) that.update_tokens();
                else that.$emit("close");
            });
        },
        close: function () {
            /**
             * @description: 关闭当前对话框
             * @return void
             */
            this.$emit("close");
        },
        update_tokens: function () {
            /**
             * @description: 更新页面的token列表
             * @return void
             */
            var that = this;

            //在这里进行时长的获得与展示

            get_app_detail(this.token, localStorage.getItem("app_key")).then(
                function (res) {
                    // console.log(res);
                    if (res.data.status == "fail") fail_msg(res.data.msg);
                    else {
                        var temp_list_data = res.data.tokens;
                        for (var i = 0; i < temp_list_data.length; i++) {
                            temp_list_data[i].created_time = parse_to_string(
                                parser(temp_list_data[i].created_time)
                            );
                            if (temp_list_data[i].dead_time == "forever") {
                                temp_list_data[i].dead_time = "永久";
                                continue;
                            }
                            temp_list_data[i].dead_time = parse_to_string(
                                parser(temp_list_data[i].dead_time)
                            );
                        }
                        that.token_list = temp_list_data;
                        that.max_access = that.token_list[0].access;

                        that.loading = false;
                    }
                }
            );
        },
    },
    mounted() {
        this.user_name = localStorage.getItem("user_name");
        this.pass_word = localStorage.getItem("pass_word");
    },
    watch: {
        visible: {
            handler(vis) {
                /**
                 * @description: 当本页面可见时，更新含有的token列表
                 * @return void
                 */
                if (vis == true) this.update_tokens();
                else if (vis == false) this.token_list = [];
                // console.log(this.token_list[0]);
                // this.max_access = this.token_list[0].access;
            },
        },
        token: {
            handler() {
                /**
                 * @description: 当token发生变化时，更新当前token列表
                 * @return void
                 */
                if (this.visible == true) this.update_tokens();
            },
        },
    },
};
</script>

<style></style>
