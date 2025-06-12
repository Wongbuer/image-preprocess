<script setup>
import api from '@/api/index.js'
import { ElButton } from 'element-plus'
import { onMounted, ref, watch } from 'vue'

const props = defineProps({
  processor: Object,
  params: Object,
  original: String,
})

const processedImage = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function processImage() {
  if (!props.original || !props.processor?.name) {
    processedImage.value = ''
    loading.value = false
    errorMsg.value = ''
    return
  }

  loading.value = true
  errorMsg.value = ''

  try {
  const result = await api.post('/image/process', {
    image_data: props.original,
    processor_name: props.processor.name,
    params: props.params,
  })

  if (result) {
    processedImage.value = 'data:image/png;base64,' + result
  } else {
    throw new Error('接口返回为空')
  }
} catch (err) {
  errorMsg.value = '处理失败：' + err.message
  console.error('处理失败', err)
} finally {
  loading.value = false
}

watch(
  [() => props.original, () => props.processor, () => props.params],
  processImage,
  { immediate: true, deep: true }
)

onMounted(processImage)

function saveImage() {
  if (!processedImage.value) return

  const link = document.createElement('a')
  link.href = processedImage.value
  link.download = `${props.processor?.name || 'processed-image'}.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div style="text-align: center;">
    <h5>{{ props.processor?.description || props.processor?.name || '未选择处理器' }}</h5>

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
