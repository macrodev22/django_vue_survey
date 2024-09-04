<template>
    <div class="flex items-center justify-between text-gray-500">
        <h3 class="text-lg font-bold"> {{ `${index + 1}. ${model.question}` }}</h3>
        <div class="flex items-center">
            <!-- Add new question  -->
            <button @click="emit('add-question')"
                class="flex items-center gap-2 text-xs py-1 px-3 mr-2 rounded-sm text-white bg-blue-500 hover:bg-blue-600">
                <PlusIcon class="w-4 h-4" />
                Add
            </button>
            <!-- Delete Question  -->
            <button @click="emit('delete-question')"
                class="flex items-center gap-2 text-xs py-1 px-3 mr-2 rounded-sm text-red-500 bg-transparent hover:bg-red-600 hover:text-white">
                <TrashIcon class="w-4 h-4" />
                Delete
            </button>
        </div>
    </div>
    <!-- Question  -->
    <div class="grid gap-3 grid-cols-12 text-gray-700">
        <!-- Qn  -->
        <div class="mt-3 col-span-9">
            <label class="block text-sm font-medium text-gray-700">Question Text</label>
            <input type="text" v-model="model.question"
                class="block w-full shadow-sm mt-1 focus:ring-indigi-500 focus:border-indigo-500 rounded">
        </div>
        <!-- Qn type  -->
        <div class="mt-3 col-span-3">
            <label class="block text-sm font-medium text-gray-700">Choose answer format</label>
            <select id="question_type" v-model="model.type"
                class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm">
                <option v-for="type in questionTypes" :key="type.type" :value="type.type">
                    {{ type.name }}
                </option>
            </select>
        </div>

        <!-- Qn Description  -->
        <div class="mt-3 col-span-12">
            <label class="block text-sm font-medium text-gray-700">Description</label>
            <textarea v-model="model.description"
                class="mt-1 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"></textarea>
        </div>

        <!-- Question Data  -->
        <div class="mt-2 col-span-12" v-if="shouldHaveOptions">
            <h4 class="text-sm font-semibold mb-1 flex justify-between items-center">
                Options
                <button type="button" @click="addOption"
                    class="py-1 px-3 text-sm rounded-sm text-white bg-gray-600 gap-2 flex items-center justify-center hover:bg-gray-700">
                    <PlusIcon class="w-4 h-4" />
                    Add Option
                </button>
            </h4>
            <div v-if="!model.data?.options?.length" class="text-xs text-gray-600 text-center py-3">
                You don't have any options defined. Click Add option above to add options
            </div>
            <!-- List of options  -->
            <div>
                <div class="flex items-center mb-1" v-for="option, index in model.data.options" :key="option.uuid">
                    <span class="w-6 text-sm">{{ index + 1 }}.</span>
                    <input type="text" v-model="option.text"
                        class="w-full rounded-sm py-1 px-2 text-xs border border-gray-300 focus:border-indigo-500">
                    <button type="button" @click="removeOption(option.uuid)"
                        class="ml-2 w-6 h-6 rounded-full flex items-center justify-center border border-transparent transition-colors hover:border-red-100">
                        <TrashIcon class="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>

    </div>
    <hr class="my-4 shadow-sm">
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useStore } from '../store';
import { v4 as uuidv4 } from 'uuid';
import { PlusIcon, TrashIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
    question: Object,
    index: Number,
})
const store = useStore()

const model = ref({ ...props.question })
const questionTypes = computed(() => store.questionTypes)
const shouldHaveOptions = computed(() => {
    const optionTypes = ['checkbox', 'radio', 'select']
    return optionTypes.includes(model.value.type)
})

const emit = defineEmits(['change', 'add-question', 'delete-question'])

const addOption = () => {
    const option = {
        uuid: uuidv4(),
        text: ''
    }
    model.value.data.options = model.value.data.options || []
    model.value.data.options.push(option)
    emit('change', model.value)
    //TODO: Focus the last element added
}

const removeOption = (uuid) => {
    model.value.data.options = model.value.data.options.filter(o => o.uuid !== uuid)
    emit('change', model.value)
}

watch(model, (newValue) => {
    emit('change', { index: props.index, newValue })
}, { deep: true })

</script>