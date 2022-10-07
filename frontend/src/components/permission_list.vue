<!--
 * @FileDescription: 权限列表，用来展示所有的权限，并提供各种权限操作
 * @Author: yaojianzhu
 * @Date: 2021.3.16
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <add_dialog
        :app_token="app_token"
        @close="close"
        @new_add="add"
        @new_edit="edit"
        :type="type"
        :visible="add_dialog_visible"
        :dialog_type="dialog_type"
        :selected_key="selected_key"
        :selected_name="selected_permission"
    ></add_dialog>
    <add_dialog
        :app_token="app_token"
        @close="close_child_dialog"
        @new_add="add_child"
        :type="type"
        :visible="add_child_dialog_visible"
        :dialog_type="dialog_type"
        :selected_key="selected_key"
        :selected_name="selected_permission"
    ></add_dialog>
    <list_dialog
        @close="close_list"
        :type="list_type"
        :visible="list_dialog_visible"
        :list_data="list_data"
    ></list_dialog>

    <el-row>
        <el-col :span="2">
            <div class="grid-content bg-purple-dark">
                <el-button
                    class="add_permission_button"
                    type="success"
                    round
                    icon="el-icon-document-add"
                    @click="add_permission_dialog"
                >
                    添加权限
                </el-button>
            </div>
        </el-col>
        <el-col :span="16"
            ><div class="grid-content bg-purple-light"></div
        ></el-col>
        <el-col :span="5">
            <div class="grid-content bg-purple">
                <el-input
                    @change="search"
                    class="search_input"
                    placeholder="请输入内容"
                    prefix-icon="el-icon-search"
                    v-model="input"
                >
                </el-input>
            </div>
        </el-col>
        <el-col :span="1">
            <div class="grid-content bg-purple-light">
                <el-button
                    @click="search"
                    class="search_button"
                    icon="el-icon-search"
                    plain
                    type="primary"
                ></el-button>
            </div>
        </el-col>
    </el-row>
    
    <el-table
        :data="permission_list"
        row-key="key"
        border
        :tree-props="{
            children: 'child_permissions',
            hasChildren: 'hasChildren',
        }"
        stripe
    >
        <el-table-column class="key" prop="key" label="key"> </el-table-column>

        <el-table-column class="name" prop="name" label="权限">
        </el-table-column>

        <el-table-column label="查看">
            <template #default="scope">
                <el-button
                    class="show_role_button"
                    type="primary"
                    plain
                    icon="el-icon-view"
                    @click="open_list(1, scope.row)"
                    >角色</el-button
                >
                <el-button
                    class="show_user_button"
                    type="primary"
                    plain
                    icon="el-icon-view"
                    @click="open_list(0, scope.row)"
                    >用户</el-button
                >
                <el-button
                    class="show_child_button"
                    type="primary"
                    plain
                    icon="el-icon-view"
                    @click="open_list(3, scope.row)"
                    >子权限</el-button
                >
            </template>
        </el-table-column>

        <el-table-column label="操作">
            <template #default="scope">
                <el-button
                    class="edit_button"
                    type="success"
                    round
                    @click="open_add_child(scope.row)"
                    >添加子权限</el-button
                >
                <el-button
                    class="edit_button"
                    type="primary"
                    round
                    icon="el-icon-edit"
                    @click="open_edit(scope.row)"
                    >编辑</el-button
                >
                <el-popconfirm title="确定删除吗？" @confirm="rm(scope.row)">
                    <template #reference>
                        <el-button
                            class="delete"
                            type="danger"
                            round
                            icon="el-icon-delete"
                            >删除</el-button
                        >
                    </template>
                </el-popconfirm>
            </template>
        </el-table-column>
    </el-table>
</template>

<script>
import { edit, remove, add, show_relative } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
import add_dialog from "./add_dialog.vue";
import list_dialog from "./list_dialog.vue";
import { parser, parse_to_string } from "../utils/time_parser.js";
export default {
    name: "Permission_List",
    props: {
        app_token: "", //app token
        permission_list: Array, //当前展示条目
    },
    emits: ["update", "search"],
    components: {
        add_dialog,
        list_dialog,
    },
    data() {
        return {
            input: "", //搜索输入
            add_dialog_visible: false, //添加输入框是否可见
            list_dialog_visible: false, //关联条目是否可见
            type: 2, //类型
            list_data: [], //储存用来展示table_Dialog的list
            list_type: 0, //关联条目类型
            selected_key: "", //选择的key
            dialog_type: 0, //对话框类型
            selected_permission: "", //选择的权限
            now_page: 1, //当前页码
            list_title: ["用户", "角色", "权限"], //标题列表
            add_child_dialog_visible: false, //添加子权限对话框是否可见
            loading: true, //是否正在加载中
            loading_instance: this.$loading()
        };
    },
    methods: {
        close_child_dialog: function () {
            /**
             * @description: 关闭添加子权限对话框
             * @return void
             */

            this.add_child_dialog_visible = false;
        },
        open_add_child: function (state) {
            /**
             * @description: 打开添加子权限对话框
             * @param {Object} state
             * @return void
             */

            this.selected_key = state.key;
            this.dialog_type = 2;
            this.add_child_dialog_visible = true;
        },
        add_child: function (state) {
            /**
             * @description: 添加子权限
             * @param {Object} state
             * @return void
             */

            // console.log("add child permission", state);
            var that = this;
            add(this.app_token, localStorage.getItem("app_key"), 2, [
                {
                    name: state.name,
                    key: state.key,
                    parent_key: this.selected_key,
                },
            ]).then(function (res) {
                // console.log("添加子权限", res);
                if (res.data.status == "succeed") {
                    that.$emit("update", that.now_page, 2);
                    succeed_msg("添加成功");
                } else {
                    fail_msg(res.data.msg);
                }
            });
        },
        search: function () {
            /**
             * @description: 搜索
             * @return void
             */
            this.loading_instance = this.$loading()
            this.loading = true;
            this.$emit("search", this.input);
        },
        add_permission_dialog: function () {
            /**
             * @description: 添加权限
             * @return void
             */

            this.dialog_type = 0;
            this.selected_key = "";
            this.selected_permission = "";
            this.add_dialog_visible = true;
        },
        add: function (state, type) {
            /**
             * @description: 添加
             * @param {Object} state
             * @param {Number}type
             * @return void
             */

            var that = this;
            // console.log("add", state, type);
            add(this.app_token, localStorage.getItem("app_key"), 2, [
                {
                    name: state.name,
                    key: state.key,
                },
            ]).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("添加成功");
                that.$emit("update", that.now_page, 2);
            });
        },
        close: function () {
            /**
             * @description: 关闭添加对话框
             * @return void
             */

            this.add_dialog_visible = false;
            this.selected_key = "";
            this.selected_permission = "";
        },
        open_list: function (num, value) {
            /**
             * @description: 打开展示列表
             * @param {Number} num
             * @param {Object} value
             * @return void
             */

            if (num == 3) {
                this.list_type = num;
                var temp_list_data = value.child_permissions;
                for (var i = 0; i < temp_list_data.length; i++) {
                    temp_list_data[i].created_time = parse_to_string(
                        parser(temp_list_data[i].created_time)
                    );
                }
                this.list_data = temp_list_data;
                this.list_dialog_visible = true;
                this.list_type = num;
            } else {
                var that = this;
                show_relative(
                    this.app_token,
                    localStorage.getItem("app_key"),
                    2,
                    num,
                    value.key,
                    0,
                    19
                ).then(function (res) {
                    if (res.data.status == "fail") {
                        if (res.data.msg == "out of range") {
                            fail_msg("它还没有关联的" + that.list_title[num]);
                        } else {
                            fail_msg(res.data.msg);
                        }
                    } else {
                        var temp_list_data1 = res.data.list;
                        for (var j = 0; j < temp_list_data1.length; j++) {
                            temp_list_data1[j].created_time = parse_to_string(
                                parser(temp_list_data1[j].created_time)
                            );
                        }
                        that.list_data = temp_list_data1;
                        that.list_type = num;
                        that.list_dialog_visible = true;
                    }
                });
            }
        },
        close_list: function () {
            /**
             * @description: 关闭展示对话框
             * @return void
             */

            this.list_dialog_visible = false;
            this.list_data = []; //返回初始值
        },
        edit: function (state, type) {
            /**
             * @description: 编辑
             * @param {Object} state
             * @param {Number} type
             * @return void
             */

            var that = this;
            edit(
                this.app_token,
                localStorage.getItem("app_key"),
                this.selected_key,
                type,
                {
                    name: state.name,
                    key: this.key,
                }
            ).then(function (res) {
                // console.log("编辑完成", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("编辑已保存");
                that.selected_key = "";
                that.$emit("update", that.now_page, 2);
            });
        },
        open_edit: function (state) {
            /**
             * @description: 打开编辑对话框
             * @param {Object} state
             * @return void
             */

            this.dialog_type = 1;
            this.add_dialog_visible = true;
            this.selected_key = state.key;
            this.selected_permission = state.name;
        },
        rm: function (state) {
            /**
             * @description: 删除条目
             * @param {Object} state
             * @return void
             */

            // console.log("delete ", state);
            var that = this;
            remove(
                this.app_token,
                localStorage.getItem("app_key"),
                [state.key],
                2
            ).then(function (res) {
                // console.log("删除权限", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("已删除");
                that.$emit("update", that.now_page, 2);
            });
        },
    },
    watch: {
        permission_list: {
            handler() {
                this.loading = false;
                this.loading_instance.close()
            },
        },
    },
};
</script>

<style></style>
