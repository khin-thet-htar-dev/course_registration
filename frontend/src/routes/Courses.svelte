<script lang="ts">
  import { onMount } from "svelte";
  import axios from "axios";
  import CourseList from "../components/CourseList.svelte";
  import CourseForm from "../components/CourseForm.svelte";

  let courses = [];
  let showForm = false;
  let loading = true;
  let error = null;

  async function fetchCourses() {
    try {
      const response = await axios.get("http://localhost:8000/api/courses/");
      courses = response.data.results;
      loading = false;
    } catch (err) {
      error = "Failed to fetch courses";
      loading = false;
    }
  }

  async function handleAddCourse(event) {
    try {
      const response = await axios.post("http://localhost:8000/api/courses/", event.detail);
      courses = [...courses, response.data];
      showForm = false;
    } catch (err) {
      error = "Failed to add course";
    }
  }

  onMount(fetchCourses);
</script>

<div class="space-y-6">
  <div class="flex justify-between items-center">
    <h1 class="text-3xl font-bold text-gray-900">Courses</h1>
    <button
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      on:click={() => (showForm = true)}
    >
      Add Course
    </button>
  </div>

  {#if loading}
    <div class="text-center">Loading...</div>
  {:else if error}
    <div class="text-red-500">{error}</div>
  {:else}
    <CourseList {courses} />
  {/if}

  {#if showForm}
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <CourseForm
        on:submit={handleAddCourse}
        on:cancel={() => (showForm = false)}
      />
    </div>
  {/if}
</div> 