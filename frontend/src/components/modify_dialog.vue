<!--
 * @FileDescription: 编辑对话框，可以修改用户和角色之间的关联关系
 * @Author: yaojianzhu
 * @Date: 2021.3.16
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <set_time
        @close="close_set_time_dialog"
        :selected_key="set_time_key"
        :selected_user="selected_key"
        :visible="set_time_dialog_visible"
        :app_token="token"
    ></set_time>

    <el-dialog @close="close" :title="title_list[type]" v-model="outer_visible" id="test_dialog">
        {{ modify_list[type] }}：{{ selected_user }}
        <el-transfer
            @change="modify"
            :titles="[total_list[type], existed_list[type]]"
            v-model="value"
            :data="data"
        />
        <el-row v-if="type == 0">
            <el-row>
                <h3>已有的角色列表</h3>
            </el-row>
            <el-table stripe :data="list_data" row-key="key" border>
                <el-table-column class="name" prop="name" :label="title[type]">
                </el-table-column>
                <el-table-column class="key" prop="key" label="key">
                </el-table-column>
                <el-table-column
                    class="created_time"
                    prop="created_time"
                    label="创建时间"
                >
                </el-table-column>
                <el-table-column
                    class="detach_time"
                    prop="detach_time"
                    label="到期时间"
                >
                </el-table-column>

                <el-table-column
                    class="alive_time"
                    prop="alive_time"
                    label="操作"
                    ><template #default="scope">
                        <el-button
                            type="success"
                            @click="change_alive_time(scope.row)"
                            >修改时限</el-button
                        ></template
                    >
                </el-table-column>
            </el-table>
        </el-row>
            <template #footer>
            <div class="dialog-footer">
                <el-button class="close_button" @click="close">关闭</el-button>
            </div>
            </template>

    </el-dialog>
</template>

<script>
import set_time from "./set_time.vue";
import { show_relative, get_list } from "../utils/communication.js";
export default {
    name: "Modify_Dialog",
    emits: ["close", "change", "update"],
    components: {
        set_time,
    },
    props: {
        type: 0, //展示类型
        visible: false, //是否可见
        selected_user: "", //选择的用户
        selected_key: "", //表示被选中的key
        token: "", //app token
        list_data: Array,
    },
    data() {
        return {
            title: ["角色", "用户"], //标题列表
            mode: "transfer", //穿梭框状态
            data: [], //数据
            outer_visible: false, //是否可见
            modify_list: ["操作用户名", "操作角色名"], //操作标题列表
            title_list: ["修改用户", "修改角色"], //操作列表
            total_list: ["全部角色", "全部权限", "占位符"],
            existed_list: ["已有角色", "已有权限", "占位符"],
            value: [], //根据value的索引，可以获得右边的key,

            set_time_dialog_visible: false,
            set_time_key: "",
        };
    },
    methods: {
        change_alive_time: function (data) {
            // console.log("修改时限", data);
            this.set_time_key = data.key;
            this.set_time_dialog_visible = true;
        },
        close: function () {
            /**
             * @description: 关闭当前编辑框
             * @return void
             */

            this.$emit("close");
        },
        modify: function (num, direction, arr) {
            /**
             * @description: 修改
             * @param {Number} num
             * @param {String} direction
             * @param {Array} arr
             * @return void
             */

            this.$emit("change", num, direction, arr);
        },
        close_set_time_dialog: function () {
            this.set_time_dialog_visible = false;
            this.$emit("update", this.selected_key);
        },
    },
    watch: {
        visible: {
            handler(vis) {
                if (vis) this.$emit("update", this.selected_key);
                this.outer_visible = vis;
                var that = this;
                //更新已经有的条目
                show_relative(
                    this.token,
                    localStorage.getItem("app_key"),
                    this.type,
                    this.type + 1,
                    this.selected_key,
                    0,
                    100
                ).then(function (res) {
                    //获得用户的所有角色
                    that.value = [];
                    if (res.data.list)
                        for (var i = 0; i < res.data.list.length; i++) {
                            that.value.push(res.data.list[i].key);
                        }
                });
                //获得所有条目
                get_list(
                    this.token,
                    localStorage.getItem("app_key"),
                    this.type + 1,
                    0,
                    100
                ).then(function (res) {
                    //获得所有条目
                    that.data = [];
                    if (res.data.list)
                        for (var i = 0; i < res.data.list.length; i++) {
                            that.data.push({
                                key: res.data.list[i].key,
                                label: res.data.list[i].name,
                                disabled: false,
                            });
                        }
                });
            },
        },
    },
};
</script>

<style></style>
