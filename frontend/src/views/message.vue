<template>
    <div class="row">
        <div class="col-sm-12">
            <div class="card email-card">
                <div class="card-header">
                    <div class="mail-header">
                        <div class="row align-items-center">
                            <div class="col-xl-4 col-md-3">
                                <a href="#!" class="b-brand">
                                    <div class="b-bg">A+</div>
                                    <span class="b-title text-muted"
                                        >企业权限管理系统-消息页面</span
                                    >
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div class="mail-body">
                        <div class="row">
                            <div class="col-xl-2 col-md-3">
                                <ul
                                    class="mb-2 nav nav-tab flex-column nav-pills"
                                    id="v-pills-tab"
                                    role="tablist"
                                    aria-orientation="vertical"
                                >
                                    <li class="nav-item mail-section">
                                        <a
                                            @click="changeto(0)"
                                            class="nav-link text-left active"
                                            id="v-pills-home-tab"
                                            data-toggle="pill"
                                            href="#v-pills-home"
                                            role="tab"
                                            aria-controls="v-pills-home"
                                            aria-selected="false"
                                        >
                                            <span
                                                ><i
                                                    class="feather icon-inbox"
                                                ></i>
                                                收件箱</span
                                            >
                                            <span class="float-right">{{
                                                inbox_num
                                            }}</span>
                                        </a>
                                    </li>
                                    <li class="nav-item mail-section">
                                        <a
                                            @click="changeto(1)"
                                            class="nav-link text-left"
                                            id="v-pills-settings-tab"
                                            data-toggle="pill"
                                            href="#v-pills-mail"
                                            role="tab"
                                        >
                                            <span
                                                ><i
                                                    class="feather icon-navigation"
                                                ></i>
                                                发件箱</span
                                            >
                                            <span class="float-right">{{
                                                sent_num
                                            }}</span>
                                        </a>
                                    </li>
                                </ul>
                            </div>
                            <div class="col-xl-10 col-md-9 inbox-right">
                                <div
                                    class="tab-content p-0"
                                    id="v-pills-tabContent"
                                >
                                    <div
                                        class="tab-pane fade show active"
                                        id="v-pills-home"
                                        role="tabpanel"
                                        aria-labelledby="v-pills-home-tab"
                                    >
                                        <div
                                            class="tab-content"
                                            id="pills-tabContent"
                                        >
                                            <div
                                                class="tab-pane fade show active"
                                                id="pills-primary"
                                                role="tabpanel"
                                                aria-labelledby="pills-primary-tab"
                                            >
                                                <div
                                                    class="mail-body-content table-responsive"
                                                >
                                                    <inbox
                                                        v-if="
                                                            (show_type == 0 ||
                                                                show_type ==
                                                                    1) &&
                                                            !send
                                                        "
                                                        :list="inbox_list"
                                                    ></inbox>

                                                    <write
                                                        v-if="send"
                                                        @send_msg="send_msg"
                                                        :send_to="send_to"
                                                    ></write>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
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
import "../../public/assets/js/menu-setting.min.js";
import {
    sent_message,
    receive_list,
    sent_list,
} from "../utils/communication.js";
import inbox from "../components/inbox.vue";
import { parser, parse_to_string } from "../utils/time_parser.js";
import write from "../components/write.vue";
import { fail_msg, succeed_msg } from "../utils/msg.js";
export default {
    props: {
        send_token: "",
        send_key: "",
        send_to: "",
        send: false,
    },
    components: {
        inbox,
        write,
    },
    emits: ["close_msg_send"],
    data() {
        return {
            show_type: 0, //0表示收件箱，1表示发件箱，2表示展示具体消息，3表示发信息
            user_name: "",
            pass_word: "",
            inbox_list: [],
            inbox_num: 0,
            sent_num: 0,
            recycle_num: 0,
        };
    },
    methods: {
        send_msg: function (to, msg, title) {
            var that = this;
            sent_message(
                this.send_token,
                this.send_key,
                msg,
                to,
                this.user_name,
                this.pass_word,
                title
            ).then(function (res) {
                // console.log("发送消息", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    succeed_msg("发送消息成功！");
                    that.show_type = 0;
                    that.changeto(0);
                }
                that.get_sent_num();
            });
        },
        changeto: function (num) {
            this.$emit("close_msg_send");
            this.show_type = num;
            if (num == 0) this.get_receive_list();
            else this.get_sent_list();
        },
        get_receive_list: function () {
            var that = this;
            receive_list(
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word"),
                0,
                100
            ).then(function (res) {
                // console.log("获得收件箱列表", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    that.inbox_list = res.data.list;
                    if (that.inbox_list) {
                        for (var i = 0; i < that.inbox_list.length; i++) {
                            that.inbox_list[i].created_time = parse_to_string(
                                parser(that.inbox_list[i].created_time)
                            );
                        }
                        that.inbox_num = that.inbox_list.length;
                    }
                }
            });
        },
        get_sent_list: function () {
            var that = this;
            sent_list(
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word"),
                0,
                100
            ).then(function (res) {
                // console.log("获得发件箱列表", res);
                if (res.data.status == "fail") fail_msg(res.data.msg);
                else {
                    that.inbox_list = res.data.list;
                    if (that.inbox_list) {
                        for (var i = 0; i < that.inbox_list.length; i++) {
                            that.inbox_list[i].created_time = parse_to_string(
                                parser(that.inbox_list[i].created_time)
                            );
                        }
                        that.sent_num = that.inbox_list.length;
                    }
                }
            });
        },
        get_sent_num: function () {
            var that = this;
            sent_list(
                localStorage.getItem("user_name"),
                localStorage.getItem("pass_word"),
                0,
                100
            ).then(function (res) {
                if (res.data.list) that.sent_num = res.data.list.length;
            });
        },
    },
    mounted() {
        this.user_name = localStorage.getItem("user_name");
        this.pass_word = localStorage.getItem("pass_word");
        this.get_sent_num();
        this.get_receive_list();
    },
};
</script>

<style></style>
