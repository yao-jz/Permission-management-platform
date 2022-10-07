/*
 * @Description: 文件及简介
 * @Author: Cary
 * @Date: 2021-03-18 10:35:24
 * @FilePath: \excel-to-jsone:\work\vue-project\frontend\src\utils\request.js
 */
import axios from 'axios'
import { ElMessage } from 'element-plus'
import Config from '../config'

// create an axios instance
const Request = axios.create({
  baseURL: Config.baseUrl, // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

// request interceptor
Request.interceptors.request.use(
  config => {
    // do something before request is sent

    // 可以在请求前添加 app_token
    // config.headers['X-Token'] = getToken()

    // 统一配置请求头为 formdata
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    ElMessage.error('请求出错，请检查重试')
    return Promise.reject(error)
  }
)

// response interceptor
Request.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    const res = response.data

    // if the custom code is not 20000, it is judged as an error.
    if (res.code !== 200) {
      ElMessage.warning('数据出错，请检查重试')
      // 出错了 可以抛出错误
      // return Promise.reject(new Error('Error'))
    } else {
      return res
    }
  },
  error => {
    console.log('err' + error) // for debug
    ElMessage.error('响应出错，请检查重试')
    return Promise.reject(error)
  }
)

export default Request
