<!--
 * @FileDescription: 用户列表，用来展示app的所有用户并展示用户操作
 * @Author: yaojianzhu
 * @Date: 2021.3.15
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
        :selected_name="selected_user"
    ></add_dialog>
    <modify_dialog
        @update="update_list_data"
        @change="modify"
        @close="close_modify"
        :token="app_token"
        :type="type"
        :list_data="role_list_data"
        :visible="modify_dialog_visible"
        :selected_user="selected_user"
        :selected_key="selected_key"
    ></modify_dialog>
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
                    class="add_user_button"
                    type="success"
                    round
                    @click="add_user_dialog"
                    icon="el-icon-document-add"
                    >添加用户</el-button
                >
            </div>
        </el-col>
        <el-col :span="16">
            <div class="grid-content bg-purple-light"></div>
        </el-col>
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
    
    <el-table :data="user_list" stripe>
        
        <el-table-column prop="key" label="key"></el-table-column>

        <el-table-column prop="name" label="姓名"></el-table-column>

        <el-table-column
            class="created_time"
            prop="created_time"
            label="创建时间"
        ></el-table-column>

        <el-table-column label="查看">
            <template #default="scope">
                <el-button
                    class="show_role_button"
                    type="primary"
                    plain
                    @click="open_list(1, scope.row)"
                    icon="el-icon-view"
                    >角色</el-button
                >
                <el-button
                    class="show_permission_button"
                    type="primary"
                    plain
                    icon="el-icon-view"
                    @click="open_list(2, scope.row)"
                    >权限</el-button
                >
            </template>
        </el-table-column>

        <el-table-column label="编辑">
            <template #default="scope">
                <el-button
                    class="edit_role_button"
                    type="primary"
                    plain
                    icon="el-icon-edit"
                    @click="user_role(scope.row)"
                    >编辑角色</el-button
                >
            </template>
        </el-table-column>

        <el-table-column label="操作">
            <template #default="scope">
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
                            class="delete_button"
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
import {
    attach,
    detach,
    remove,
    add,
    show_relative,
    edit,
} from "../utils/communication.js";
import add_dialog from "./add_dialog.vue";
import select_dialog from "./select_dialog";
import modify_dialog from "./modify_dialog.vue";
import list_dialog from "./list_dialog.vue";
import {parser, parse_to_string} from "../utils/time_parser.js"
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    name: "User_List",
    emits: ["update", "search"],
    props: {
        user_list: Array, //当前展示的所有内容
        app_token: "", //apptoken
    },
    components: {
        add_dialog,
        modify_dialog,
        list_dialog,
        select_dialog,
    },
    data() {
        return {
            input: "", //搜索的内容
            add_dialog_visible: false, //添加对话框是否可见
            modify_dialog_visible: false, //关联对话框是否可见
            list_dialog_visible: false, //展示条目对话框是否可见
            selected_key: "", //选择的Key
            list_type: 0, //展示条目种类
            type: 0, //类型
            dialog_type: 0, //对话框类型
            selected_user: "", //选择的用户
            list_data: [], //储存用来展示table_Dialog的list
            type_title: ["用户", "角色", "权限"], //标题列表

            now_page: 1, //默认现在的page
            loading: false, //是否正在加载中
            loading_instance: this.$loading(),
            role_list_data: [],
        };
    },
    methods: {
        update_list_data: function () {
            var that = this;
            show_relative(
                this.app_token,
                localStorage.getItem("app_key"),
                this.type,
                this.type + 1,
                this.selected_key,
                0,
                100
            ).then(function (res) {
                // console.log("update data", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    var temp_list_data = res.data.list;
                    for (var i = 0; i < temp_list_data.length; i++) {
                        temp_list_data[i].created_time = parse_to_string(
                            parser(temp_list_data[i].created_time)
                        );
                        if(temp_list_data[i].detach_time == "forever"){
                            temp_list_data[i].detach_time = "永久";
                            continue;
                        }
                        temp_list_data[i].detach_time = parse_to_string(
                            parser(temp_list_data[i].detach_time)
                        );
                    }
                    that.role_list_data = temp_list_data;
                }
            });
        },
        search: function () {
            /**
             * @description: 进行搜索
             * @return void
             */
            this.loading_instance = this.$loading()
            this.loading = true;
            this.$emit("search", this.input);
        },
        add_user_dialog: function () {
            /**
             * @description: 打开添加用户对话框
             * @return void
             */

            this.dialog_type = 0;
            this.selected_user = "";
            this.selected_key = "";
            this.add_dialog_visible = true;
        },
        add: function (state) {
            /**
             * @description: 添加用户
             * @param {Object} state
             * @return void
             */

            // console.log("add", state, type);
            var that = this;
            add(this.app_token, localStorage.getItem("app_key"), 0, [
                {
                    name: state.name,
                    key: state.key,
                },
            ]).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("新增用户成功");
                that.$emit("update", that.now_page, 0);
            });
        },
        close: function () {
            /**
             * @description: 关闭添加用户对话框
             * @return void
             */

            this.add_dialog_visible = false;
            this.selected_key = "";
            this.selected_user = "";
        },
        user_role: function (user) {
            /**
             * @description: 打开关联对话框
             * @param {Object} user
             * @return void
             */

            this.selected_user = user.name;
            this.selected_key = user.key;
            this.modify_dialog_visible = true;
        },
        close_modify: function () {
            /**
             * @description: 关闭关联对话框
             * @return void
             */

            this.modify_dialog_visible = false;
            this.selected_user = "";
            this.selected_key = "";
        },
        modify: function (now, direction, arr) {
            /**
             * @description: 进行关联操作
             * @param {Array} now
             * @param {String} direction
             * @param {Array} arr
             * @return void
             */
            var that = this;
            var add_key_list = []; //用户增加的角色列表
            var rm_key_list = [];
            // console.log(now); //当前拥有的
            // console.log(direction); //方向
            // console.log(arr); //改变了
            var j = 1,
                len = 1;
            if (direction == "right") {
                //attach
                for (j = 0, len = arr.length; j < len; j++) {
                    add_key_list.push(arr[j]);
                }
                attach(
                    this.app_token,
                    localStorage.getItem("app_key"),
                    [this.selected_key],
                    add_key_list,
                    []
                ).then(function (res) {
                    if (res.data.status == "succeed") succeed_msg("修改成功");
                    else {
                        that.close_modify();
                        fail_msg(res.data.msg);
                        return;
                    }
                    that.update_list_data();
                });
            } else if (direction == "left") {
                //detach
                for (j = 0, len = arr.length; j < len; j++) {
                    rm_key_list.push(arr[j]);
                }
                detach(
                    this.app_token,
                    localStorage.getItem("app_key"),
                    [this.selected_key],
                    rm_key_list,
                    []
                ).then(function (res) {
                    if (res.data.status == "succeed") succeed_msg("删除成功");
                    else {
                        that.close_modify();
                        fail_msg(res.data.msg);
                        return;
                    }
                    // console.log("detach result:", res);
                    that.update_list_data();
                });
            }
        },
        open_list: function (num, value) {
            /**
             * @description: 打开列表对话框，用来展示用户拥有的角色或用户拥有的权限
             * @param {Number} num
             * @param {Object} value
             * @return void
             */

            var that = this;
            show_relative(
                this.app_token,
                localStorage.getItem("app_key"),
                0,
                num,
                value.key,
                0,
                19
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") {
                    if (res.data.msg == "out of range") {
                        fail_msg("它还没有" + that.type_title[num]);
                    } else {
                        fail_msg(res.data.msg);
                    }
                } else {
                    var temp_list_data = res.data.list;
                    for (var i = 0; i < temp_list_data.length; i++) {
                        temp_list_data[i].created_time = parse_to_string(
                            parser(temp_list_data[i].created_time)
                        );
                    }
                    that.list_data = temp_list_data;
                    that.list_type = num;
                    that.list_dialog_visible = true;
                }
            });
        },
        close_list: function () {
            this.list_dialog_visible = false;
            this.list_data = []; //返回初始值
        },
        edit: function (state, type) {
            /**
             * @description: 编辑信息
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
                    key: state.key,
                }
            ).then(function (res) {
                // console.log(res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("编辑已保存");
                that.selected_key = "";
                that.$emit("update", that.now_page, 0);
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
            this.selected_user = state.name;
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
                0
            ).then(function (res) {
                // console.log("删除用户", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else succeed_msg("已删除");
                that.$emit("update", that.now_page, 0);
            });
        },
    },
    watch: {
        user_list: {
            handler() {
                this.loading_instance.close()
                this.loading = false;
            },
        },
    },
};
</script>

<style>
.el-main {
    background-color: #e9eef3;
    color: #333;
    text-align: left;
    line-height: 20px;
}
.el-table--small td,
.el-table--small th {
    padding: 0px 0;
}
.el-table__header {
    line-height: 40px;
}
.el-table__row {
    height: 50px;
}
.el-table {
    width: 100% !important;
    font-size: 15px;
}
.modify {
    width: 10px;
}
.el-pagination {
    margin-top: 14px;
    text-align: center !important;
}
.el-input {
    width: 100%;
    text-align: right;
}
.el-row {
    margin-bottom: 15px;
}
</style>
