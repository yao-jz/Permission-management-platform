<!--
 * @FileDescription: 设置关联对话框，用来进行角色和权限之间的关联，同时支持子权限的关联
 * @Author: yaojianzhu
 * @Date: 2021.3.24
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.3.27
 -->
<template>
    <el-dialog @close="close" :title="title_list[type]" v-model="outer_visible">
        <el-input placeholder="输入关键字进行过滤" v-model="filter_text">
        </el-input>
        {{ select_list[type] }}：{{ selected_role }}
        <br />
        权限：
        <el-row>
            <el-tree
                class="filter-tree"
                empty-text="无内容"
                :data="data"
                :props="default_props"
                show-checkbox
                node-key="key"
                :default-checked-keys="value"
                default-expand-all
                :filter-node-method="filter_node"
                @check-change="handle_check_change"
                ref="tree"
            >
            </el-tree>
        </el-row>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="close">取 消</el-button>
                <el-button type="primary" @click="confirm">确 定</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import {
    show_relative,
    get_list,
    attach,
    detach,
} from "../utils/communication.js";
import { succeed_msg } from "../utils/msg";

export default {
    name: "Select_Dialog",
    props: {
        type: "", //类型
        visible: false, //是否可见
        token: "", //apptoken
        selected_role: "", //选择的角色
        selected_key: "", //选择的key
    },
    data() {
        return {
            title_list: ["编辑用户", "编辑角色"], //标题列表
            outer_visible: false, //是否可见
            select_list: ["操作用户名", "操作角色名"], //选择标题列表
            filter_text: "", //搜索内容
            data: [], //数据
            default_props: {
                //对话框设置
                children: "child_permissions",
                label: "name",
            },
            value: [], //拥有的条目，用以勾选已添加的内容
        };
    },
    methods: {
        confirm: function () {
            /**
             * @description: 关闭当前对话框
             * @return void
             */
            this.$emit("close");
            this.filter_text = "";
            succeed_msg("保存成功");
        },
        close: function () {
            /**
             * @description: 关闭当前对话框
             * @return void
             */

            this.$emit("close");
            this.filter_text = "";
        },
        filter_node(value, data) {
            /**
             * @description: 筛选信息，实现搜索功能
             * @param {String} value
             * @param {Array} data
             * @return void
             */

            // console.log(value, data);
            if (!value) return true;
            return data.name.indexOf(value) !== -1;
        },
        handle_check_change(data, checked) {
            /**
             * @description: 选择状态发生变化时的触发函数
             * @param {Object} data
             * @param {Boolean} checked
             * @return void
             */

            if (checked == false) {
                //删除data
                detach(
                    this.token,
                    localStorage.getItem("app_key"),
                    [],
                    [this.selected_key],
                    [data.key]
                );
            } else {
                //增加data
                attach(
                    this.token,
                    localStorage.getItem("app_key"),
                    [],
                    [this.selected_key],
                    [data.key]
                );
            }
        },
    },
    watch: {
        visible: {
            handler(vis) {
                this.outer_visible = vis;
                var that = this;
                //显示已经拥有的条目
                show_relative(
                    this.token,
                    localStorage.getItem("app_key"),
                    this.type,
                    this.type + 1,
                    this.selected_key,
                    0,
                    100
                ).then(function (res) {
                    //获得角色的所有权限
                    // console.log("获得角色的所有权限", res);
                    that.value = [];
                    if (res.data.list) {
                        for (var i = 0; i < res.data.list.length; i++) {
                            that.value.push(res.data.list[i].key);
                        }
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
                    // console.log("获得所有条目成功", res);
                    that.data = [];
                    if (res.data.list) {
                        for (var i = 0; i < res.data.list.length; i++) {
                            that.data.push({
                                key: res.data.list[i].key,
                                name: res.data.list[i].name,
                                child_permissions:
                                    res.data.list[i].child_permissions,
                                disabled: false,
                            });
                        }
                    }
                    // console.log(that.data);
                });
            },
        },
        filter_text: {
            //过滤器
            handler(val) {
                this.$refs.tree.filter(val);
            },
        },
    },
};
</script>

<style>
.el-tree__empty-text {
    position: absolute;
    left: 50px;
    top: 10px;
    -webkit-transform: translate(-50%, -50%);
    transform: translate(-50%, -50%);
    color: #909399;
    font-size: 14px;
    width: 100px;
    align-content: center;
}
.el-tree {
    position: relative;
    cursor: default;
    background: #fff;
    color: #606266;
    width: 100%;
}
</style>
