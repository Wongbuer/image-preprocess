import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  timeout: 15000,
})

// 请求拦截器（可加token）
api.interceptors.request.use(config => {
   return config
}, error => {
  return Promise.reject(error)
})

// 响应拦截器
api.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 200) {
      ElMessage.error(res.message || '请求出错')
      return Promise.reject(new Error(res.message || '请求出错'))
    }
    return res.data // 直接返回 data 字段
  },
  error => {
    ElMessage.error(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export default api
