<<<<<<< Updated upstream
<script setup>
import { ref } from 'vue'
import FunctionPanel from '@/components/FunctionPanel.vue'
import ImageUploader from '@/components/ImageUploader.vue'

import PreviewBox from '@/components/PreviewBox.vue'

const selectedFunctions = ref([])
const processedImageUrl = ref('')

function handleProcessed(url) {
  processedImageUrl.value = url
=======
<script setup lang="ts" generic="T extends any, O extends any">
defineOptions({
  name: 'IndexPage',
})

const name = ref('')

const router = useRouter()
function go() {
  if (name.value)
    router.push(`/hi/${encodeURIComponent(name.value)}`)
>>>>>>> Stashed changes
}
</script>

<template>
<<<<<<< Updated upstream
  <div class="p-4 flex gap-8">
    <FunctionPanel v-model:selected-functions="selectedFunctions" class="w-1/3" />
    <div class="w-2/3">
      <ImageUploader v-model:selected-functions="selectedFunctions" @image-processed="handleProcessed" />
      <PreviewBox :processed-image-url="processedImageUrl" />
=======
  <div>
    <div i-carbon-campsite text-4xl inline-block />
    <p>
      <a rel="noreferrer" href="https://github.com/antfu-collective/vitesse-lite" target="_blank">
        Vitesse Lite
      </a>
    </p>
    <p>
      <em text-sm op75>Opinionated Vite Starter Template</em>
    </p>

    <div py-4 />

    <TheInput
      v-model="name"
      placeholder="What's your name?"
      autocomplete="false"
      @keydown.enter="go"
    />

    <div>
      <button
        class="text-sm m-3 btn"
        :disabled="!name"
        @click="go"
      >
        Go
      </button>
>>>>>>> Stashed changes
    </div>
  </div>
</template>
