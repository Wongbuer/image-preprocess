<script setup>
import { ElMessage } from 'element-plus'
import { ref } from 'vue'

// 定义事件
// 触发 App.vue 的处理
const emit = defineEmits(['uploadSuccess', 'clear'])
function beforeUpload(file) {
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }

  const reader = new FileReader()
  reader.onload = () => {
    emit('uploadSuccess', reader.result)
  }
  reader.readAsDataURL(file)
  return false
}

function handleClear() {
  emit('clear')
}
</script>

<template>
  <div class="upload-buttons">
    <el-upload
      :show-file-list="false"
      :before-upload="beforeUpload"
    >
      <el-button type="primary">
        选择图片
      </el-button>
    </el-upload>
    <el-button type="danger" @click="handleClear">
      清除图像
    </el-button>
  </div>
</template>

<style scoped>
.upload-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
</style>
