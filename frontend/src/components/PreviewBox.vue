<script setup>
import { ElButton } from 'element-plus'
import { onMounted, ref, watch } from 'vue'

// 接收父组件传来的三个参数
const props = defineProps({
  functionName: String,
  params: Object,
  original: String,
})

const processedImage = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function processImage() {
  if (!props.original) {
    processedImage.value = ''
    loading.value = false
    errorMsg.value = ''
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
    const response = await fetch('http://127.0.0.1:8000/api/image/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image_data: props.original,
        processor_name: props.functionName,
        params: props.params,
      }),
    })

    if (!response.ok) {
      throw new Error(`服务器错误：${response.status}`)
    }

    const result = await response.json()

    if (result.data) {
      // 给返回的纯base64字符串加上前缀
      processedImage.value = 'data:image/png;base64,' + result.data
    } else {
      throw new Error('接口返回数据格式异常，没有data字段')
    }
  } catch (err) {
    errorMsg.value = '处理失败：' + err.message
    console.error('处理失败', err)
  } finally {
    loading.value = false
  }
}

// 监听 props 变化，立即触发图片处理
watch(
  [() => props.original, () => props.functionName, () => props.params],
  processImage,
  { immediate: true, deep: true }
)

onMounted(processImage)

function saveImage() {
  if (!processedImage.value) return

  const link = document.createElement('a')
  link.href = processedImage.value
  link.download = `${props.functionName || 'processed-image'}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div style="text-align: center;">
    <h5>{{ functionName }}</h5>

    <div v-if="loading" style="margin: 20px 0; font-weight: bold;">
      处理中...
    </div>

    <div v-else>
      <img
        v-if="processedImage"
        :src="processedImage"
        alt="处理后的图片"
        style="max-width: 100%; border: 1px solid #ccc;"
      />
      <div v-else style="color: #888; margin: 10px 0;">
        暂无处理结果
      </div>

      <div v-if="errorMsg" style="color: red; margin: 10px 0;">
        {{ errorMsg }}
      </div>

      <ElButton
        v-if="processedImage"
        type="primary"
        size="small"
        style="margin-top: 10px;"
        @click="saveImage"
      >
        保存图片
      </ElButton>
    </div>
  </div>
</template>
