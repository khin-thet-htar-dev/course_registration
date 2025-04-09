<script lang="ts">
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  let courseId = "";
  let courseName = "";
  let instructor = "";
  let semester = "";

  function handleSubmit() {
    dispatch("submit", {
      course_id: courseId,
      course_name: courseName,
      instructor,
      semester,
    });
  }

  function handleCancel() {
    dispatch("cancel");
  }
</script>

<div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
  <h2 class="text-2xl font-bold mb-6">Add New Course</h2>
  <form on:submit|preventDefault={handleSubmit} class="space-y-4">
    <div>
      <label for="courseId" class="block text-sm font-medium text-gray-700">
        Course ID
      </label>
      <input
        type="text"
        id="courseId"
        bind:value={courseId}
        required
        minlength="5"
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
      />
    </div>

    <div>
      <label for="courseName" class="block text-sm font-medium text-gray-700">
        Course Name
      </label>
      <input
        type="text"
        id="courseName"
        bind:value={courseName}
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
      />
    </div>

    <div>
      <label for="instructor" class="block text-sm font-medium text-gray-700">
        Instructor
      </label>
      <input
        type="text"
        id="instructor"
        bind:value={instructor}
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
      />
    </div>

    <div>
      <label for="semester" class="block text-sm font-medium text-gray-700">
        Semester
      </label>
      <input
        type="text"
        id="semester"
        bind:value={semester}
        required
        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
      />
    </div>

    <div class="flex justify-end space-x-3 mt-6">
      <button
        type="button"
        on:click={handleCancel}
        class="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
      >
        Cancel
      </button>
      <button
        type="submit"
        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
      >
        Add Course
      </button>
    </div>
  </form>
</div> 