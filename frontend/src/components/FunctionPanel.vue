<script setup>
import axios from 'axios'
import { ElMessage } from 'element-plus'
import api from '@/api/index.js'
import { ref, onMounted, watch } from 'vue'

// 向父组件传递 selectedFunctions
const emit = defineEmits(['update:selectedFunctions'])

const processors = ref([])
const selectedProcessor = ref(null)
const paramValues = ref({})
const loading = ref(false)

async function fetchProcessors() {
  loading.value = true
  try {
    const res = await api.get('/image/processors')
    processors.value = res
  } catch (e) {
    console.error('获取处理器失败', e)
  } finally {
    loading.value = false
  }
}

// 当选择的处理器变化时，更新参数默认值
watch(selectedProcessor, (newProcessor) => {
  if (newProcessor) {
    const defaults = {}
    newProcessor.parameters?.forEach(param => {
      if (param.default !== null && param.default !== undefined) {
        defaults[param.name] = param.default
      } else {
        if (param.type === 'int') {
          defaults[param.name] = 0
        } else if (param.type === 'str') {
          defaults[param.name] = ''
        } else if (param.type === 'bool') {
          defaults[param.name] = false
        } else {
          defaults[param.name] = null
        }
      }
    })
    paramValues.value = defaults
  } else {
    paramValues.value = {}
  }
}, { immediate: true })

// 当处理器或参数改变时，通知父组件更新
watch(
  [selectedProcessor, paramValues],
  () => {
    if (selectedProcessor.value) {
      const rawParams = paramValues.value
      const normalizedParams = {}

      selectedProcessor.value.parameters.forEach(param => {
        const val = rawParams[param.name]
        if (param.type === 'bool') {
          normalizedParams[param.name] = val ? 1 : 0
        } else {
          normalizedParams[param.name] = val
        }
      })

      emit('update:selectedFunctions', [{
        name: selectedProcessor.value.name,
        description: selectedProcessor.value.description,
        params: normalizedParams
      }])
    } else {
      emit('update:selectedFunctions', [])
    }
  },
  { deep: true }
)

onMounted(fetchProcessors)
</script>

<template>
  <div>
    <el-select
      v-model="selectedProcessor"
      placeholder="请选择图像处理器"
      filterable
      :loading="loading"
      style="width: 100%;"
      clearable
    >
      <el-option
        v-for="proc in processors"
        :key="proc.name"
        :label="proc.description"
        :value="proc"
      />
    </el-select>

    <div v-if="selectedProcessor" style="margin-top: 16px;">
      <h4>参数设置：</h4>
      <div
        v-if="selectedProcessor.parameters && selectedProcessor.parameters.length > 0"
      >
        <div
          v-for="param in selectedProcessor.parameters"
          :key="param.name"
          style="margin-bottom: 12px;"
        >
          <label :for="param.name" style="display: block; font-weight: 600;">
            {{ param.name }} <span v-if="param.required" style="color: red;">*</span>：
            <small style="color: #999;">{{ param.description }}</small>
          </label>
          <!-- 整数参数 -->
          <el-input-number
            v-if="param.type === 'int'"
            v-model="paramValues[param.name]"
            :min="param.min_value ?? 0"
            :max="param.max_value ?? 100"
            :step="param.step ?? 1"
            :id="param.name"
            style="width: 100%;"
          />
          <!-- 字符串参数 -->
          <el-input
            v-else-if="param.type === 'str'"
            v-model="paramValues[param.name]"
            :id="param.name"
            placeholder="请输入文本"
            style="width: 100%;"
          />
          <!-- 布尔参数 -->
          <el-switch
            v-else-if="param.type === 'bool'"
            v-model="paramValues[param.name]"
            :id="param.name"
            active-text="是"
            inactive-text="否"
          />
          <!-- 其他类型提示 -->
          <div v-else>
            <em>暂不支持参数类型: {{ param.type }}</em>
          </div>
        </div>
      </div>
      <!-- 💡 没有参数的情况 -->
      <div v-else style="color: #999; font-style: italic; margin-top: 10px;">
        当前处理器无需设置参数。
      </div>
    </div>
  </div>
</template>
