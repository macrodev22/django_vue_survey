<template>
    <div class="flex items-center justify-between mb-4">
        <h1 class="text-3xl text-gray-900 font-bold">{{ survey.title ? survey.title : 'Create a survey' }}</h1>
        <button v-if="route.params.id" role="button" @click="deleteSurvey"
            class="flex items-center gap-1 justify-center py-2 px-3 bg-red-500 rounded-md text-white hover:bg-red-600">
            <TrashIcon class="w-5 h-5" />
            Delete
        </button>
    </div>
    <form @submit.prevent="saveSurvey">
        <div class="shadow sm:rounded-md sm:overflow-hidden">
            <Loading v-if="isLoading" />
            <!-- Survey fields  -->
            <div class="p-5 bg-white space-y-6 sm:p-6">
                <!-- image  -->
                <div>
                    <label for="" class="block text-sm font-medium text-gray-700">Image</label>
                    <div class="mt-1 flex items-center">
                        <img v-if="survey.image_url" :src="survey.image_url" class="w-64 h-48 object-cover">
                        <UserCircleIcon v-else class="h-12 w-12 text-gray-300" aria-hidden="true" />
                        <div class="ml-5 flex flex-col gap-5 items-center">
                            <button type="button"
                                class="relative rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
                                <input type="file" @change="imageChanged" name="survey-image" accept="image/*"
                                    class="absolute left-0 top-0 top-0 bottom-0 opacity-0 cursor-pointer">
                                Change
                            </button>
                            <button type="button" @click="revertImage"
                                class="flex items-center justify-center rounded-full w-10 h-10 border hover:bg-gray-50">
                                <ArrowPathIcon class="w-7 h-7" style="color: black;" />
                            </button>
                        </div>
                    </div>
                </div>

                <!-- Title  -->
                <div>
                    <label for="" class="block text-sm font-medium text-gray-700">Title</label>
                    <input type="text" v-model="survey.title" autocomplete="survey_title"
                        class="mt-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                </div>
                <!-- Description  -->
                <div class="col-span-full">
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Description</label>
                    <div class="mt-2">
                        <textarea id="about" name="about" rows="3" v-model="survey.description"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
                    </div>
                    <p class="mt-3 text-sm leading-6 text-gray-600">What is the survey about? (HTML allowed)</p>
                </div>
                <!-- Expire date  -->
                <div>
                    <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Expiry date</label>
                    <input type="datetime-local" required v-model="date_time_expiry"
                        class="mt-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                </div>

                <!-- Status  -->
                <div class="flex items-start">
                    <div class="flex items-center h-5">
                        <input type="checkbox" name="status" id="status" v-model="survey.status"
                            class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded">
                    </div>
                    <div class="ml-3 text-sm">
                        <label for="status" class="font-medium text-gray-700">Active</label>
                    </div>
                </div>
                <!-- Questions  -->
                <div class="py-5 px-4 bg-white space-y-6 sm:p-6">
                    <h3 class="flex items-center justify-between font-semibold text-2xl text-gray-600">
                        Questions
                        <button type="button" @click="addQuestion"
                            class="bg-gray-600 hover:bg-gray-700 text-white text-sm font-medium py-4 px-5 rounded-md">
                            Add new question
                        </button>
                    </h3>
                    <div v-for="question, index in survey.questions" :key="question.id">
                        <QuestionEditor :question="question" :index="index"
                            @delete-question="deleteQuestion(question.id)" @add-question="addQuestionBefore(index)"
                            @change="changeQuestion($event)" />
                    </div>
                </div>

                <!-- Submit3  -->
                <div class="px-4 py-3 bg-gray-50 text-right sm:px-6">
                    <button type="submit" @click="saveSurvey"
                        class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-700 focus:ring-offset-2">Submit</button>
                </div>
            </div>
        </div>
    </form>
</template>
<script setup>
import { useRoute, useRouter } from 'vue-router';
import { useStore } from '../store';
import { ref, watch, onMounted } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import apiClient from '../services/apiClient';

import { ArrowPathIcon, UserCircleIcon, TrashIcon } from '@heroicons/vue/24/outline';
import QuestionEditor from '../components/QuestionEditor.vue';
import Loading from '../components/Loading.vue';

const survey = ref({
    id: uuidv4(),
    title: '',
    status: true,
    description: '',
    image: null,
    image_url: null,
    expire_date: '',
    questions: []
})

const imageHasChanged = ref(false)
const date_time_expiry = ref('')
const isLoading = ref(false)

const route = useRoute()
const store = useStore()
const router = useRouter()

const isNewSurvey = () => {
    return route.name === 'SurveysCreate'
}

const reloadSurveys = () => {
    apiClient.get('/surveys')
        .then(({ data }) => {
            store.suveys = data
            // console.log('Surveys reloaded')
            return Promise.resolve()
        })
        .catch(err => {
            console.error('Error', err)
            return Promise.reject(err)
        })
}

const retrieveCurrentSurvey = () => {
    if (route.params.id) {
        // Get survey
        const retrievedSurvey = store.getSurvey(route.params.id)
        survey.value = retrievedSurvey || survey.value
    }
}
// retrieveCurrentSurvey()

const imageChanged = (event) => {
    const file = event.target.files[0]
    imageHasChanged.value = true

    const reader = new FileReader()
    reader.onloadend = () => {
        survey.value.image_url = reader.result
    }

    reader.readAsDataURL(file)
}

const revertImage = () => {
    imageHasChanged.value = false
    survey.value.image_url = survey.value.image
}

const dbDateToHTML = (originalDateStr) => {
    // 2025-03-05T11:41:14Z
    // 2025-03-05 11:41:14
    return originalDateStr.slice(0, 16); // Output: 2025-03-05T11:41
}

const htmlDatetoDb = (originalDateStr) => {
    // Original format 2024-09-20T12:30
    const [date, time] = originalDateStr.split('T')
    const formatedDateString = `${date} ${time}:00.000000Z`

    return formatedDateString // Output 2024-09-20 12:30:00
}

watch(date_time_expiry, () => {
    survey.value.expire_date = htmlDatetoDb(date_time_expiry.value)
})

onMounted(() => {
    // Load surveys if none
    if (!store.suveys) {
        reloadSurveys()
            .then(() => retrieveCurrentSurvey())
            .catch(err => console.error(err))
    } else retrieveCurrentSurvey()

    // Format expiry date for display
    if (survey.value.expire_date) {
        date_time_expiry.value = dbDateToHTML(survey.value.expire_date)
    }
})

const saveSurvey = () => {
    isLoading.value = true
    // New survey or existing survey
    if (!isNewSurvey()) {
        console.log(`%cThis is an old survey`, 'font-size: 24px; font-weight: bold; color: red;')

        // Remove image_url
        const payload = { ...survey.value }
        if (!imageHasChanged.value) delete payload.image
        else payload.image = payload.image_url

        delete payload.image_url
        console.log('%cPayload', 'font-size: 20px; color: green', payload)

        apiClient.put(`/surveys/${route.params.id}`, payload)
            .then(res => {
                console.log(res.data)
                // Reload surveys
                reloadSurveys()
                isLoading.value = false
            })
            .catch(err => {
                console.log(err)
            })
    }
    // New survey
    else {
        console.log(`%cThis is a new survey`, 'font-size: 24px; font-weight: bold; color: red;')

        // Remove image_url
        const payload = { ...survey.value }
        if (imageChanged.value) payload.image = payload.image_url

        delete payload.image_url

        apiClient.post('/surveys', payload)
            .then(res => {
                console.log(res.data)
                // Reload surveys in store
                reloadSurveys()
                isLoading.value = false

                // Redirect to survey view page
                router.push({ name: 'Surveys' })

            })
            .catch(err => {
                console.log(err)
            })
    }
}

const deleteSurvey = () => {
    // console.log('Deleting survey', route.params.id)
    if (confirm(`Are you sure you want to delete the survey: ${survey.value.title}?`)) {
        store.deleteSurvey(route.params.id)
            .then(() => router.replace({ name: 'Surveys' }))
    }
}

const addQuestion = () => {
    const questionModel = {
        id: uuidv4(),
        type: 'text',
        question: '',
        description: null,
        data: {}
    }

    survey.value.questions.push(questionModel)
}

const addQuestionBefore = (index) => {
    const questionModel = {
        id: uuidv4(),
        type: '',
        question: '',
        description: null,
        data: {
            options: []
        }
    }

    survey.value.questions.splice(index, 0, questionModel)
}

const deleteQuestion = (id) => {
    survey.value.questions = survey.value.questions.filter(q => q.id !== id)
}

const changeQuestion = ({ index, newValue }) => {
    // Update the changed question in the suvery
    // console.log('Change registered to:', questionData)
    survey.value.questions[index] = newValue
}
</script>