import { ElMessage } from "element-plus";

export function fail_msg(message) {
    /**
     * @description: 提示错误信息
     * @param {String} message
     * @return void
     */

    ElMessage({
        showClose: true,
        message: message,
        type: "error", //success, warning, error
    });
}

export function succeed_msg(message) {
    /**
     * @description: 提示成功信息
     * @param {String} message
     * @return void
     */

    ElMessage.success({
        message: message,
        type: "success",
    });
}
