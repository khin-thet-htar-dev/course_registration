<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import type { Course } from "../types";
  import axios from "axios";

  export let courses: Course[] = [];
  const dispatch = createEventDispatcher();

  let showForm = false;
  let showUploadForm = false;
  let selectedCourse: Course | null = null;
  let studentId = "";
  let studentName = "";
  let studentEmail = "";
  let enrollmentDate = "";
  let error = "";
  let uploadError = "";
  let selectedFile: File | null = null;
  let expandedRow: string | null = null;
  let grades: any[] = [];
  let loadingGrades = false;
  let gradesError = "";
  let sortField = "student_name";
  let sortDirection = "asc";
  let filterGrade = "";
  let filterStudentName = "";

  // Add this after the existing variables
  $: sortedAndFilteredGrades = grades
    .filter(grade => {
      const matchesGrade = !filterGrade || grade.grade === filterGrade;
      const matchesName = !filterStudentName || 
        grade.student.name.toLowerCase().includes(filterStudentName.toLowerCase());
      return matchesGrade && matchesName;
    })
    .sort((a, b) => {
      let comparison = 0;
      if (sortField === "student_name") {
        comparison = a.student.name.localeCompare(b.student.name);
      } else if (sortField === "student_id") {
        comparison = a.student.student_id.localeCompare(b.student.student_id);
      } else if (sortField === "grade") {
        comparison = a.grade.localeCompare(b.grade);
      }
      return sortDirection === "asc" ? comparison : -comparison;
    });

  async function handleViewGrades(course: Course) {
    selectedCourse = course;
    loadingGrades = true;
    gradesError = "";
    try {
      const response = await axios.get(`http://localhost:8000/api/courses/${course.course_id}/grades/`);
      grades = response.data;
    } catch (err) {
      console.error("Error fetching grades:", err);
      gradesError = "Failed to fetch grades";
    } finally {
      loadingGrades = false;
    }
  }

  function handleSort(field: string) {
    if (sortField === field) {
      sortDirection = sortDirection === "asc" ? "desc" : "asc";
    } else {
      sortField = field;
      sortDirection = "asc";
    }
  }

  function exportToCSV() {
    if (!selectedCourse) return;
    
    const headers = ["Student Name", "Student ID", "Grade", "Comments"];
    const csvContent = [
      headers.join(","),
      ...sortedAndFilteredGrades.map(grade => [
        `"${grade.student.name}"`,
        grade.student.student_id,
        grade.grade,
        `"${grade.comments || ""}"`
      ].join(","))
    ].join("\n");

    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", `${selectedCourse.course_name}_grades.csv`);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  function handleUploadGrades(course: Course) {
    selectedCourse = course;
    showUploadForm = true;
  }

  function handleRegisterStudent(course: Course) {
    selectedCourse = course;
    showForm = true;
  }

  async function handleSubmit() {
    if (!studentId || !studentName || !studentEmail || !enrollmentDate) {
      error = "Please fill in all fields";
      return;
    }

    if (selectedCourse) {
      try {
        let student;
        // First check if student exists
        try {
          const studentResponse = await axios.get(`http://localhost:8000/api/students/${studentId}/`);
          student = studentResponse.data;
        } catch (err) {
          // If student doesn't exist, create new student
          const createStudentResponse = await axios.post("http://localhost:8000/api/students/", {
            student_id: studentId,
            name: studentName,
            email: studentEmail,
            enrollment_date: enrollmentDate
          });
          student = createStudentResponse.data;
        }
        

        // Create enrollment with student_id and course_id
        const enrollmentResponse = await axios.post("http://localhost:8000/api/enrollments/", {
          student_id: studentId,
          course_id: selectedCourse.id
        });

        // Reset form
        studentId = "";
        studentName = "";
        studentEmail = "";
        enrollmentDate = "";
        error = "";
        showForm = false;
        selectedCourse = null;

        // Dispatch event to notify parent component
        dispatch("studentRegistered", { course: selectedCourse, student: student });
      } catch (err) {
        console.error("Error registering student:", err);
        error = "Failed to register student. Please try again.";
      }
    }
  }

  function handleCancel() {
    showForm = false;
    selectedCourse = null;
    studentId = "";
    studentName = "";
    studentEmail = "";
    enrollmentDate = "";
    error = "";
  }

  function handleFileSelect(event: Event) {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files.length > 0) {
      selectedFile = target.files[0];
    }
  }

  async function handleUploadSubmit() {
    if (!selectedFile || !selectedCourse) {
      uploadError = "Please select a file";
      return;
    }

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('course_id', selectedCourse.id.toString());

      const response = await axios.post('http://localhost:8000/api/grades/upload_csv/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      if (response.data.errors && response.data.errors.length > 0) {
        uploadError = `Some records failed to upload. Please check the file format.`;
        console.error('Upload errors:', response.data.errors);
      } else {
        // Reset form
        selectedFile = null;
        showUploadForm = false;
        selectedCourse = null;
        uploadError = "";
        
        // Dispatch event to notify parent component
        dispatch("gradesUploaded", { course: selectedCourse });
      }
    } catch (err) {
      console.error("Error uploading grades:", err);
      uploadError = "Failed to upload grades. Please try again.";
    }
  }

  function handleUploadCancel() {
    showUploadForm = false;
    selectedCourse = null;
    selectedFile = null;
    uploadError = "";
  }
</script>

<div class="container mx-auto px-4 py-8">
  <div class="bg-white shadow overflow-hidden sm:rounded-md">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Course ID
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Course Name
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Instructor
          </th>
          <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
            Semester
          </th>
          <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
            Actions
          </th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each courses as course (course.id)}
          <tr>
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
              {course.course_id}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
              {course.course_name}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {course.instructor}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {course.semester}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <div class="flex justify-end space-x-2">
                <button
                  class="bg-green-500 hover:bg-green-700 text-white text-sm font-bold py-1 px-3 rounded"
                  on:click={() => handleRegisterStudent(course)}
                >
                  Register Student
                </button>
                <button
                  class="bg-purple-500 hover:bg-purple-700 text-white text-sm font-bold py-1 px-3 rounded"
                  on:click={() => handleUploadGrades(course)}
                >
                  Upload Grading
                </button>
                <button
                  class="bg-blue-500 hover:bg-blue-700 text-white text-sm font-bold py-1 px-3 rounded"
                  on:click={() => handleViewGrades(course)}
                >
                  View Grading
                </button>
              </div>
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>

  {#if selectedCourse}
    <div class="mt-8">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold">Grades for {selectedCourse.course_name}</h2>
        <button
          class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
          on:click={exportToCSV}
        >
          Export CSV
        </button>
      </div>

      <div class="mb-4 flex space-x-4">
        <div class="flex-1">
          <label for="filterStudentName" class="block text-sm font-medium text-gray-700">
            Filter by Student Name
          </label>
          <input
            type="text"
            id="filterStudentName"
            bind:value={filterStudentName}
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            placeholder="Search student name..."
          />
        </div>
        <div class="w-48">
          <label for="filterGrade" class="block text-sm font-medium text-gray-700">
            Filter by Grade
          </label>
          <select
            id="filterGrade"
            bind:value={filterGrade}
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          >
            <option value="">All Grades</option>
            <option value="A">A</option>
            <option value="B">B</option>
            <option value="C">C</option>
            <option value="D">D</option>
            <option value="F">F</option>
          </select>
        </div>
      </div>

      {#if loadingGrades}
        <div class="text-center py-8">Loading grades...</div>
      {:else if gradesError}
        <div class="text-red-500 text-center py-8">{gradesError}</div>
      {:else}
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  on:click={() => handleSort("student_name")}
                >
                  Student Name {sortField === "student_name" ? (sortDirection === "asc" ? "↑" : "↓") : ""}
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  on:click={() => handleSort("student_id")}
                >
                  Student ID {sortField === "student_id" ? (sortDirection === "asc" ? "↑" : "↓") : ""}
                </th>
                <th
                  scope="col"
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer"
                  on:click={() => handleSort("grade")}
                >
                  Grade {sortField === "grade" ? (sortDirection === "asc" ? "↑" : "↓") : ""}
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Comments
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              {#each sortedAndFilteredGrades as grade (grade.id)}
                <tr>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {grade.student.name}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {grade.student.student_id}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {grade.grade}
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500">
                    {grade.comments || "-"}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        </div>
      {/if}
    </div>
  {/if}

  {#if showForm && selectedCourse}
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h2 class="text-2xl font-bold mb-6">Register Student for {selectedCourse.course_name}</h2>
        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
          <div>
            <label for="studentId" class="block text-sm font-medium text-gray-700">
              Student ID
            </label>
            <input
              type="text"
              id="studentId"
              bind:value={studentId}
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label for="studentName" class="block text-sm font-medium text-gray-700">
              Name
            </label>
            <input
              type="text"
              id="studentName"
              bind:value={studentName}
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label for="studentEmail" class="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              type="email"
              id="studentEmail"
              bind:value={studentEmail}
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          <div>
            <label for="enrollmentDate" class="block text-sm font-medium text-gray-700">
              Enrollment Date
            </label>
            <input
              type="date"
              id="enrollmentDate"
              bind:value={enrollmentDate}
              required
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
            />
          </div>

          {#if error}
            <p class="text-red-500 text-sm">{error}</p>
          {/if}

          <div class="flex justify-end space-x-2">
            <button
              type="button"
              class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
              on:click={handleCancel}
            >
              Cancel
            </button>
            <button
              type="submit"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Register
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}

  {#if showUploadForm && selectedCourse}
    <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center">
      <div class="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
        <h2 class="text-2xl font-bold mb-6">Upload Grades for {selectedCourse.course_name}</h2>
        <div class="mb-4">
          <p class="text-sm text-gray-600 mb-2">CSV File Format:</p>
          <ul class="text-sm text-gray-600 list-disc pl-5 mb-4">
            <li>Student ID</li>
            <li>Grade (A, B, C, D, F)</li>
            <li>Comments (optional)</li>
          </ul>
          <input
            type="file"
            accept=".csv"
            on:change={handleFileSelect}
            class="block w-full text-sm text-gray-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-blue-50 file:text-blue-700
              hover:file:bg-blue-100"
          />
        </div>

        {#if uploadError}
          <p class="text-red-500 text-sm mb-4">{uploadError}</p>
        {/if}

        <div class="flex justify-end space-x-2">
          <button
            type="button"
            class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
            on:click={handleUploadCancel}
          >
            Cancel
          </button>
          <button
            type="button"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            on:click={handleUploadSubmit}
          >
            Upload
          </button>
        </div>
      </div>
    </div>
  {/if}
</div> 