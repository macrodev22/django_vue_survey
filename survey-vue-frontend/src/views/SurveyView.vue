<template>
    <div class="flex items-center justify-between mb-4">
        <RouterLink
            class="flex items-center justify-center gap-2 basis-60 py-3 px-4 w-15 bg-emerald-500 rounded-md hover:bg-emerald-600 transition-colors"
            :to="{ name: 'SurveysCreate' }">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                stroke="currentColor" class="size-6 inline-block">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Add New Survey
        </RouterLink>
    </div>
    <div class="grid grid-cols-1 gap-3 sm:grid-cols-2 md:grid-cols-3 text-black">
        <SurveyListItem v-for="survey in surveys" :key="survey.id" :survey="survey"
            @delete-survey="deleteSurvey(survey.id)" />
    </div>
</template>

<script setup>
import { computed } from 'vue';
import { useStore } from '../store';
import { RouterLink } from 'vue-router';
import SurveyListItem from '../components/SurveyListItem.vue';

const store = useStore()
const surveys = computed(() => store.suveys)

const deleteSurvey = (surveyID) => {
    if (confirm('Are you sure you want to delete this survey? This operation cannot be undone!')) {
        // Delete survey
        store.deleteSurvey(surveyID)
    }
}

</script>