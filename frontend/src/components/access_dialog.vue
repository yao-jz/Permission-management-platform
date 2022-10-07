<!--
 * @FileDescription: 修改token类型对话框
 * @Author: yaojianzhu
 * @Date: 2021.5.1
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.5.1
 -->
<template>
    <el-dialog
        title="修改token权限"
        v-model="visible"
        width="30%"
        @close="close"
    >
        请设置token的权限
        <div style="margin-top: 20px">
            <el-radio-group
                @change="change_value"
                v-model="access"
                size="medium"
            >
                <el-radio-button label="all"></el-radio-button>
                <el-radio-button label="admin"></el-radio-button>
                <el-radio-button label="add"></el-radio-button>
                <el-radio-button label="edit"></el-radio-button>
                <el-radio-button label="see"></el-radio-button>
            </el-radio-group>
        </div>
        <div text-align="right">
            <span class="dialog-footer">
                <el-button @click="close">取 消</el-button>
                <el-button type="primary" @click="confirm">确 定</el-button>
            </span>
        </div>
    </el-dialog>
</template>
<script>
import { change_token_access } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    props: {
        visible: false,
        token: "",
        int: 0,
        self: 0,
    },
    emits: ["close"],
    data() {
        return {
            access: "",
            access_int: 0,
            access_title: ["all", "admin", "add", "edit", "see"],
        };
    },
    methods: {
        close: function () {
            this.$emit("close");
        },
        confirm: function () {
            if(this.self > this.access_int){
                fail_msg("你的权限不够提升至此！");
                this.close();
                return;
            } 
            var that = this;
            change_token_access(
                [
                    {
                        app_key: localStorage.getItem("app_key"),
                        app_token: this.token,
                        token_access: this.access_int,
                    },
                ],
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word")
            ).then(function (res) {
                // console.log("修改token权限", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    succeed_msg("修改token权限成功");
                    that.close();
                }
            });
        },
        change_value: function (value) {
            if (value == "all") {
                this.access_int = 0;
            } else if (value == "admin") {
                this.access_int = 1;
            } else if (value == "add") {
                this.access_int = 2;
            } else if (value == "edit") {
                this.access_int = 3;
            } else if (value == "see") {
                this.access_int = 4;
            }
        },
    },
    watch: {
        visible: {
            handler() {
                this.access = this.access_title[this.int];
            },
        },
    },
};
</script>
