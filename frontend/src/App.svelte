<script lang="ts">
  import { Router, Route } from "svelte-routing";
  import Courses from "./routes/Courses.svelte";
</script>

<Router>
  <main class="min-h-screen bg-gray-100">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold text-gray-800 mb-8 text-center">Course Registration</h1>
      <Route path="/" component={Courses} />
    </div>
  </main>
</Router>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen,
      Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
  }
</style> 