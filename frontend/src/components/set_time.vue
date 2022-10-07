<!--
 * @FileDescription: 设置角色与用户的绑定事件
 * @Author: yaojianzhu
 * @Date: 2021.4.22
 * @LastEditors: yaojianzhu
 * @LastEditTime: 2021.4.22
 -->
<template>
    <el-dialog
        title="绑定时间修改"
        v-model="visible"
        width="30%"
        @close="close"
    >
        请设置角色绑定期限（单位：天）
        <div class="block">
            <el-slider
                v-model="value"
                show-input
                :min="min"
                :max="max"
            ></el-slider>
        </div>
        <template #footer>
            <span class="dialog-footer">
                <el-button type="danger" @click="infinite"
                    >绑定时间设为无穷</el-button
                >
                <el-button @click="close">取 消</el-button>
                <el-button :disabled="!value" type="primary" @click="confirm">确 定</el-button>
            </span>
        </template>
    </el-dialog>
</template>
<script>
import { set_role_time } from "../utils/communication.js";
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    name: "set_time",
    props: {
        selected_user: String,
        selected_key: String,
        visible: false,
        app_token: String,
    },
    emits: ["close", "update"],
    data() {
        return {
            value: Number, //角色绑定的时间
            min: 0, //可以选择的时间最小值
            max: 365, //可以选择的时间最大值
        };
    },
    methods: {
        infinite: function () {
            /**
             * @description: 将用户与角色的绑定时间设为无穷大
             * @return void
             */
            // console.log("设为无穷");
            var that = this;
            set_role_time(
                this.app_token,
                localStorage.getItem("app_key"),
                [
                    {
                        key: this.selected_user,
                        time_out: -1,
                    },
                ],
                [this.selected_key]
            ).then(function (res) {
                // console.log("修改时间", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    succeed_msg("修改成功");
                }
                that.$emit("close");
            });
        },
        close: function () {
            /**
             * @description: 关闭当前编辑token对话框
             * @return void
             */
            this.$emit("close");
        },
        confirm: function () {
            /**
             * @description: 确认添加/编辑token
             * @return void
             */
            var that = this;
            set_role_time(
                this.app_token,
                localStorage.getItem("app_key"),
                [
                    {
                        key: this.selected_user,
                        time_out: this.value * 86400,
                    },
                ],
                [this.selected_key]
            ).then(function (res) {
                // console.log("修改时间", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    succeed_msg("修改成功");
                }
                that.$emit("close");
            });
        },
    },
    watch: {
        visible: {
            handler() {
                // console.log(this.visible);
                this.value = 0;
            },
        },
    },
};
</script>
<style></style>
