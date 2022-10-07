/*
 * @Description: 添加 处理所有时间的方法
 * @Author: Cary
 * @Date: 2021-03-18 13:39:03
 * @FilePath: \excel-to-jsone:\work\vue-project\frontend\src\utils\date.js
 */

import dayjs from 'dayjs'

/**
 * 格式化时间函数
 * @param {*} date new Date()
 * @param {*} fmt yyyy-MM-dd 
 * @returns 
 */
export const dateFmt = (date, fmt) => dayjs(date).format(fmt)

/**
 * 获取 dayjs 对象
 */
export const getDayjs = dayjs
