<!--
 * @FileDescription: 表格组件，用来展示三种条目的表格
 * @Author: yaojianzhu
 * @Date: 2021.3.15
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <div v-if="type == 0">
        <user_list
            @search="search"
            @update="update_data"
            :app_token="token"
            :user_list="list_data"
        ></user_list>
    </div>
    <div v-else-if="type == 1">
        <role_list
            @search="search"
            @update="update_data"
            :app_token="token"
            :role_list="list_data"
        ></role_list>
    </div>
    <div v-else-if="type == 2">
        <permission_list
            @search="search"
            @update="update_data"
            :app_token="token"
            :permission_list="list_data"
        ></permission_list>
    </div>
    <div v-else-if="type == -1">
        <el-table :data="shared_user_list">
            <el-table-column property="name" label="用户名"></el-table-column>

            <el-table-column label="权限"
                ><template #default="scope"
                    >{{ access_title[scope.row.access] }}
                </template></el-table-column
            >
            <el-table-column label="消息"
                ><template #default="scope"
                    ><a
                        @click="send_msg(scope.row.name)"
                        href="#!"
                        class="btn waves-effect waves-light btn-rounded btn-outline-primary"
                        >+ 新消息</a
                    >
                </template></el-table-column
            >
            <el-table-column v-if="app_type == 0" label="取消共享"
                ><template #default="scope"
                    ><a
                        @click="cancel_share(scope.row.name)"
                        href="#!"
                        class="btn waves-effect waves-light btn-rounded btn-outline-info"
                        >取消共享</a
                    >
                </template></el-table-column
            >
        </el-table>
    </div>
    <el-pagination
        v-if="type != -1 && type != 3"
        class="pagination"
        :page-size="12"
        layout="prev, pager, next"
        :total="total_item"
        :current-page="current_page"
        background
        @current-change="change_page"
    >
    </el-pagination>
</template>

<script>
import user_list from "./user_list.vue";
import role_list from "./role_list.vue";
import permission_list from "./permission_list.vue";
import { fail_msg, succeed_msg } from "../utils/msg";
import { parser, parse_to_string } from "../utils/time_parser.js";
import {
    search_content,
    get_total,
    get_list,
    get_user_group,
    unshare,
} from "../utils/communication.js";
import { init_local } from "../utils/init_local";
export default {
    name: "Table",
    props: {
        type: 0, //展示类型
        token: "", //apptoken
        app_type: 0,
    },
    emits: ["send_msg"],
    data() {
        return {
            list_data: [], //需要传给三个list的全部数据
            total_item: 110, //所有条目
            current_page: 1, //当前页面
            from: 0, //当前页面展示的条目索引开始
            to: 12, //索引结束
            table_type: 0, //0表示是普通列表，1表示是搜索结果
            shared_user_list: [],
            search_from: 0, //搜索索引开始
            search_to: 1, //搜索索引结束
            search_total_item: 1, //搜索结果总条目数
            search_content: "", //搜索内容
            access_title: ["all", "admin", "add", "edit", "see"],
        };
    },
    components: {
        user_list,
        role_list,
        permission_list,
    },
    methods: {
        cancel_share: function (name) {
            var that = this;
            unshare(
                this.token,
                localStorage.getItem("app_key"),
                name,
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word")
            ).then(function (res) {
                // console.log("取消共享", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    succeed_msg("取消共享成功");
                }
                that.refresh_table();
            });
        },
        send_msg: function (name) {
            this.$emit(
                "send_msg",
                this.token,
                localStorage.getItem("app_key"),
                name
            );
        },
        update_data: function (page = 1, type = this.type) {
            /**
             * @description: 更新列表中的数据
             * @param {Number} page
             * @param {Number} type
             * @return void
             */

            // console.log(
            //     "update data in page",
            //     page,
            //     "from and to: ",
            //     this.from,
            //     this.to
            // );
            var that = this;
            get_list(
                this.token,
                localStorage.getItem("app_key"),
                type,
                this.from,
                this.to
            ).then(function (res) {
                //获得当前展示内容列表
                // console.log("get_list", res);
                if (!res.data.list) return;
                var temp_list_data = res.data.list;
                for (var i = 0; i < temp_list_data.length; i++) {
                    temp_list_data[i].created_time = parse_to_string(
                        parser(temp_list_data[i].created_time)
                    );
                }
                that.list_data = temp_list_data;
                get_total(
                    that.token,
                    localStorage.getItem("app_key"),
                    type
                ).then(function (result) {
                    // console.log("get total", result);
                    if (result.data.status == "succeed") {
                        that.total_item = result.data.total;
                        localStorage.setItem("total", that.total_item);
                    } else {
                        fail_msg(result.data.msg);
                    }
                });
            });
        },
        change_page: function (num) {
            /**
             * @description: 换页
             * @param {Number} num
             * @return void
             */

            var that = this;
            var from = (num - 1) * 12;
            var to = from + 12;
            if (this.table_type == 0) {
                //不是搜索框
                // console.log("change to ", num);
                get_list(
                    this.token,
                    localStorage.getItem("app_key"),
                    this.type,
                    from,
                    to
                ).then(function (res) {
                    // console.log(res);
                    if (res.data.status == "fail") {
                        that.current_page = 1;
                        fail_msg(res.data.msg);
                    } else {
                        that.from = from;
                        that.current_page = num;
                        localStorage.setItem("current_page", num);
                        localStorage.setItem("from", from);
                        localStorage.setItem("to", to);
                        that.to = to;

                        that.list_data = res.data.list;
                    }
                });
            } else {
                //搜索框的翻页
                // console.log("change search to", num);
                search_content(
                    this.token,
                    localStorage.getItem("app_key"),
                    this.search_content,
                    this.type,
                    from,
                    to
                ).then(function (res) {
                    // console.log("search change res", res);
                    if (res.data.status == "succeed") {
                        var temp_list_data = res.data.list;
                        for (var i = 0; i < temp_list_data.length; i++) {
                            temp_list_data[i].created_time = parse_to_string(
                                parser(temp_list_data[i].created_time)
                            );
                        }
                        that.list_data = temp_list_data;
                        that.search_from = from;
                        that.search_to = to;
                    } else {
                        fail_msg(res.data.msg);
                        that.current_page = 1;
                    }
                });
            }
        },
        refresh_table: function () {
            if (this.type == -1) {
                var that = this;
                get_user_group(
                    this.token,
                    localStorage.getItem("app_key")
                ).then(function (res) {
                    // console.log("获得共享用户", res);
                    if (res.data.status == "succeed") {
                        that.shared_user_list = res.data.list;
                    } else fail_msg(res.data.msg);
                });
                init_local();
                return;
            }
            this.table_type = localStorage.getItem("table_type");
            this.content = localStorage.getItem("content");
            this.from = localStorage.getItem("from");
            this.to = localStorage.getItem("to");
            this.search_to = localStorage.getItem("search_to");
            this.search_from = localStorage.getItem("search_from");
            this.current_page = Number(localStorage.getItem("current_page"));
            // console.log(
            //     "in type update",
            //     this.current_page,
            //     this.from,
            //     this.to
            // );
            if (this.table_type == 0) {
                this.update_data();
            } else {
                this.search(this.content);
            }
        },
        search: function (content, from, to) {
            /**
             * @description: 搜索
             * @param {String} content
             * @param {Number} from
             * @param {Number} to
             * @return void
             */

            var that = this;
            this.search_content = content;
            search_content(
                this.token,
                localStorage.getItem("app_key"),
                content,
                this.type,
                (from = 0),
                (to = 12)
            ).then(function (res) {
                //进行搜索
                // console.log("search result", res);
                if (res.data.status == "succeed") {
                    that.total_item = res.data.total;
                    var temp_list_data = res.data.list;
                    for (var i = 0; i < temp_list_data.length; i++) {
                        temp_list_data[i].created_time = parse_to_string(
                            parser(temp_list_data[i].created_time)
                        );
                    }
                    that.list_data = temp_list_data;
                    that.search_from = from;
                    that.search_to = to;
                    localStorage.setItem("total", that.total_item);
                } else {
                    fail_msg(res.data.msg);
                }
            });
        },
    },
    mounted() {
        this.refresh_table();
    },
    watch: {
        type: {
            handler() {
                this.refresh_table();
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
