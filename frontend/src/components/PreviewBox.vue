<script setup>
import { ElButton } from 'element-plus'
import { onMounted, ref, watch } from 'vue'

// 接收父组件参数
const props = defineProps({
  functionName: String,
  params: Object,
  original: String,
})
// 处理后的图片
const processedImage = ref('')
//  加载状态
const loading = ref(true)

async function processImage() {
  if (!props.original) {
    processedImage.value = ''
    loading.value = false
    return
  }

  loading.value = true
  let response

  try {
    response = await fetch('http://localhost:8000/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        image: props.original,
        function: props.functionName,
        params: props.params,
      }),
    })

    const result = await response.json()
    console.warn('处理后的图像 base64:', result.processed)
    processedImage.value = result.processed
  }
  catch (err) {
    console.error('处理失败', err)
  }
  finally {
    loading.value = false
  }
}

watch(
  [() => props.original, () => props.functionName, () => props.params],
  processImage,
  { immediate: true, deep: true },
)

onMounted(processImage)

function saveImage() {
  if (!processedImage.value)
    return

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
    <div v-if="loading">
      处理中...
    </div>
    <div v-else>
      <img
        :src="processedImage"
        alt="Processed"
        style="max-width: 100%; border: 1px solid #ccc;"
      >
      <ElButton
        type="primary"
        size="small"
        style="margin-top: 8px;"
        @click="saveImage"
      >
        保存图片
      </ElButton>
    </div>
  </div>
</template>
