<!-- <script setup>
import { ElMessage } from 'element-plus'
import { ref, watch } from 'vue'

const functionConfigs = {
  高斯滤波: [
    { name: 'kernelSize', label: '卷积核大小', type: 'number', default: 3 },
    { name: 'sigma', label: '标准差', type: 'number', default: 1.0 },
  ],
  图像锐化: [
    { name: 'strength', label: '锐化强度', type: 'range', default: 0.5, min: 0, max: 1 },
  ],
  边缘检测: [
    { name: 'threshold', label: '阈值', type: 'number', default: 100 },
  ],
}

const selectedFunction = ref('')
const paramValues = ref({})
const selectedFunctions = defineModel('selectedFunctions', { type: Array, required: true })

watch(selectedFunction, (newFunc) => {
  const defaults = {}
  functionConfigs[newFunc]?.forEach((param) => {
    defaults[param.name] = param.default
  })
  paramValues.value = defaults
})

function addFunction() {
  if (!selectedFunction.value)
    return

  if (selectedFunctions.value.some(f => f.name === selectedFunction.value)) {
    ElMessage.warning('您已选择过此功能')
    return
  }

  selectedFunctions.value.push({
    name: selectedFunction.value,
    params: { ...paramValues.value },
  })

  selectedFunction.value = ''
  paramValues.value = {}
}

function removeFunction(index) {
  selectedFunctions.value.splice(index, 1)
}
</script>

<template>
  <div>
    <el-select v-model="selectedFunction" placeholder="请选择功能" style="width: 100%;">
      <el-option
        v-for="func in Object.keys(functionConfigs)"
        :key="func"
        :label="func"
        :value="func"
      />
    </el-select>

    <div v-if="selectedFunction" style="margin-top: 10px;">
      <div v-for="param in functionConfigs[selectedFunction]" :key="param.name" style="margin-bottom: 10px;">
        <span>{{ param.label }}：</span>
        <el-input-number
          v-if="param.type === 'number'"
          v-model="paramValues[param.name]"
          :min="param.min"
          :max="param.max"
          :step="param.step || 1"
        />
        <el-slider
          v-else-if="param.type === 'range'"
          v-model="paramValues[param.name]"
          :min="param.min"
          :max="param.max"
          :step="param.step || 0.01"
        />
      </div>
    </div>

    <el-button type="primary" :disabled="!selectedFunction" style="margin-top: 10px;" @click="addFunction">
      添加功能
    </el-button>

    <ul style="margin-top: 15px;">
  <li
    v-for="(func, index) in selectedFunctions"
    :key="index"
    style="margin-bottom: 12px; border: 1px solid #dcdfe6; padding: 10px; border-radius: 8px;"
  >
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <strong>{{ func.name }}</strong>
      <el-button size="small" type="danger" @click="removeFunction(index)">删除</el-button>
    </div>
    <div v-if="func.params" style="margin-top: 8px; padding-left: 10px;">
      <div
        v-for="(value, key) in func.params"
        :key="key"
        style="font-size: 14px; color: #666;"
      >
        {{ key }}: {{ value }}
      </div>
    </div>
  </li>
</ul>

  </div>
</template> -->
<script setup>
import { ElMessage } from 'element-plus'
import { ref, watch } from 'vue'
// props是父组件传递过来的数据
const props = defineProps({
  selectedFunctions: {
    type: Array,
    required: true,
  },
})

const emit = defineEmits(['update:selectedFunctions'])
// 定义函数配置
const functionConfigs = {
  高斯滤波: [
    { name: 'kernelSize', label: '卷积核大小', type: 'number', default: 3, min: 1, max: 15 },
    { name: 'sigma', label: '标准差', type: 'number', default: 1.0, min: 0, max: 10, step: 0.1 },
  ],
  图像锐化: [
    { name: 'strength', label: '锐化强度', type: 'range', default: 0.5, min: 0, max: 1, step: 0.01 },
  ],
  边缘检测: [
    { name: 'threshold', label: '阈值', type: 'number', default: 100, min: 0, max: 255 },
  ],
}

//  参数定义
// seletedFunction的类型是string
const selectedFunction = ref('')
// paramValues的类型是object
const paramValues = ref({})

// 监听选中功能，自动填默认参数
watch(selectedFunction, (newFunc) => {
  const defaults = {}
  functionConfigs[newFunc]?.forEach((param) => {
    defaults[param.name] = param.default
  })
  paramValues.value = defaults
})
function addFunction() {
  if (!selectedFunction.value)
    return
  // if (props.selectedFunctions.some(f => f.name === selectedFunction.value)) {
  //   ElMessage.warning('您已选择过此功能')
  //   return
  // }
  // newArr是一个新数组，它包含了props.selectedFunctions数组中的所有元素，并添加了一个新的对象。
  const newArr = [...props.selectedFunctions]
  //  newArr.push() 方法向数组的末尾添加一个或多个元素，并返回新的长度。
  newArr.push({
    name: selectedFunction.value,
    params: { ...paramValues.value },
  })

  emit('update:selectedFunctions', newArr)
  //  移除
  selectedFunction.value = ''
  // 清空
  paramValues.value = {}
}

function removeFunction(index) {
  const newArr = [...props.selectedFunctions]
  newArr.splice(index, 1)
  emit('update:selectedFunctions', newArr)
}
</script>

<template>
  <div>
    <el-select v-model="selectedFunction" placeholder="请选择功能" style="width: 100%;">
      <el-option
        v-for="func in Object.keys(functionConfigs)"
        :key="func"
        :label="func"
        :value="func"
      />
    </el-select>

    <div v-if="selectedFunction" style="margin-top: 10px;">
      <div v-for="param in functionConfigs[selectedFunction]" :key="param.name" style="margin-bottom: 10px;">
        <span>{{ param.label }}：</span>
        <el-input-number
          v-if="param.type === 'number'"
          v-model="paramValues[param.name]"
          :min="param.min"
          :max="param.max"
          :step="param.step || 1"
          style="width: 100%;"
        />
        <el-slider
          v-else-if="param.type === 'range'"
          v-model="paramValues[param.name]"
          :min="param.min"
          :max="param.max"
          :step="param.step || 0.01"
        />
      </div>
    </div>

    <el-button type="primary" :disabled="!selectedFunction" style="margin-top: 10px;" @click="addFunction">
      添加功能
    </el-button>

    <ul style="margin-top: 15px;">
      <li
        v-for="(func, index) in props.selectedFunctions"
        :key="index"
        style="margin-bottom: 12px; border: 1px solid #dcdfe6; padding: 10px; border-radius: 8px;"
      >
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <strong>{{ func.name }}</strong>
          <el-button size="small" type="danger" @click="removeFunction(index)">
            删除
          </el-button>
        </div>
        <div v-if="func.params" style="margin-top: 8px; padding-left: 10px;">
          <div
            v-for="(value, key) in func.params"
            :key="key"
            style="font-size: 14px; color: #666;"
          >
            {{ key }}: {{ value }}
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>
