/*
 * @Description: 文件及简介
 * @Author: Cary
 * @Date: 2021-03-18 10:44:31
 * @FilePath: \excel-to-jsone:\work\vue-project\frontend\src\api\index.js
 */

import request from '@/utils/request'

//用户注册
/**
 * 注册接口
 * @param {*} data { username: 'admin', password: '123456' } 
 * @returns 
 */
export function register(data) {

  // 写了 axios 封装 以后统一的方法可以，JSON.stringify 全部都放到  request.js 里面来处理
  // 'Content-Type' = 'application/x-www-form-urlencoded' 全局写了这个配置的话， 不需要再写 JSON.stringify 转换了 
  // 第一种写法
  return request.post('/register', data)
}

////////////////////////////////////////////////////////////////////////////////////////
// 一下为简单示例


export function login(data) {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/user/info',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/user/logout',
    method: 'post'
  })
}

/**
 * 获取用户信息
 */
export function getUserMessageList() {
  return request.get('/user/message/list')
}

/**
 * 获取用户菜单
 */
export function getMenuMessageList() {
  return request.get('/menu/message/list')
}
