<script setup>
import { ref } from 'vue'
import FunctionPanel from './components/FunctionPanel.vue'
import ImageUploader from './components/ImageUploader.vue'
import PreviewBox from './components/PreviewBox.vue'

const selectedFunctions = ref([])
const originalImage = ref('')

function handleUploadSuccess(data) {
  originalImage.value = data
}
</script>

<template>
  <div class="container">
    <!-- 顶部标题 -->
    <header class="header">
      图像处理平台
    </header>

    <div class="main">
      <aside class="sidebar">
        <FunctionPanel v-model:selected-functions="selectedFunctions" />
      </aside>

      <section class="upload-area">
        <ImageUploader
          @upload-success="handleUploadSuccess"
          @clear="originalImage = ''"
        />

        <div v-if="originalImage" class="original-preview">
          <h4>原始图像预览</h4>
          <img :src="originalImage" alt="Original" width="400px">
        </div>
      </section>

      <section class="preview-area">
        <h4>预处理结果对比</h4>
        <div class="preview-grid">
          <Suspense>
            <template #default>
              <PreviewBox
                v-for="(func, index) in selectedFunctions"
                :key="index"
                :processor="func"
                :params="func.params"
                :original="originalImage"
              />
            </template>
            <template #fallback>
              <div>加载中...</div>
            </template>
          </Suspense>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  font-size: 24px;
  padding: 10px;
  text-align: center;
  font-weight: bold;
  background-color: #f0f0f0;
}

.main {
  display: flex;
  flex: 1;
}

.sidebar {
  width: 20%;
  padding: 20px;
  background-color: #fafafa;
  border-right: 1px solid #ddd;
}

.upload-area {
  width: 40%;
  padding: 20px;
  border-right: 1px solid #ddd;
}

.original-preview img {
  max-width: 100%;
  margin-top: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.preview-area {
  width: 40%;
  padding: 20px;
  overflow-y: auto;
}

.preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
}
</style>
