export function parser(str) {
    /**
     * @description: 将当前字符串日期转换为可读类型
     * @param {String} str
     * @return {
     *      year: Number,
     *      month: Number,
     *      day: Number,
     *      hour: Number,
     *      minute: Number,
     *      total_sec: Number,
     *      now_sec: Number,
     * }
     */
    const date = new Date(str); //转换成Date类型
    var now = new Date(); //执行函数的当前时间
    var year = date.getFullYear(); //获得年份
    var month = date.getMonth() + 1; //获得月份
    var day = date.getDate(); //获得日期
    var hour = date.getHours(); //获得小时
    var minute = date.getMinutes(); //获得分钟
    var total_sec = date.getTime(); //获得原始值
    var now_sec = now.getTime(); //获得现在的原始值

    return {
        year: year, //年份
        month: month, //月份
        day: day, //日期
        hour: hour, //小时
        minute: minute, //分钟
        total_sec: total_sec, //总时间
        now_sec: now_sec, //当前时间
    };
}

export function parse_to_string(obj) {
    /**
     * @description: 将当前字符串日期转换为可读类型
     * @param {Object} {
     *      year: Number,
     *      month: Number,
     *      day: Number,
     *      hour: Number,
     *      minute: Number,
     *      total_sec: Number,
     *      now_sec: Number,
     * }
     * @return {String} result
     */
    return (
        String(obj.year) +
        "." +
        String(obj.month) +
        "." +
        String(obj.day) +
        " " +
        String(obj.hour) +
        ":" +
        String(obj.minute)
    );
}
