<template>
    <div class="card">
        <div class="card-header">
            <h4 class="d-inline-block m-0">{{ title }}</h4>
            <p class="float-right m-0">
                <strong>{{ created_time }}</strong>
            </p>
        </div>
        <div class="card-body">
            <div class="email-read">
                <div>
                    <p class="user-name text-dark mb-1">
                        <strong>From:{{ from }}</strong>
                    </p>
                </div>
            </div>
            <div class="m-b-20 m-l-50">
                <div class="">
                        {{ msg }}
                </div>
            </div>
        </div>
    </div>
    <el-button @click="back">返回</el-button>
</template>

<script>
export default {
    props: {
        from: "",
        msg: "",
        to: "",
        title: "",
        created_time: "",
    },
    data() {
        return {};
    },
    emits: ["back"],
    methods: {
        back: function () {
            this.$emit("back");
        },
    },
};
</script>
