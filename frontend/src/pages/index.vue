<script setup>
import { ref } from 'vue'
import FunctionPanel from '@/components/FunctionPanel.vue'
import ImageUploader from '@/components/ImageUploader.vue'
import PreviewBox from '@/components/PreviewBox.vue'

const selectedFunctions = ref([])
const processedImageUrl = ref('')

function handleProcessed(url) {
  processedImageUrl.value = url
}
</script>

<template>
  <div class="p-4 flex gap-8">
    <FunctionPanel v-model:selected-functions="selectedFunctions" class="w-1/3" />
    <div class="w-2/3">
      <ImageUploader v-model:selected-functions="selectedFunctions" @image-processed="handleProcessed" />
      <PreviewBox :processed-image-url="processedImageUrl" />
    </div>
  </div>
</template>
