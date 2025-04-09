# Course Registration

## API Endpoints

- [Courses](#courses)
- [Students](#students)
- [Enrollments](#enrollments)
- [Grades](#grades)

### 1. Courses

- **GET /api/courses/**  
  List all courses.

- **POST /api/courses/**  
  Create a new course.

- **GET /api/courses/{course_id}/**  
  Get details of a specific course.

- **PUT /api/courses/{course_id}/**  
  Update an existing course.

- **DELETE /api/courses/{course_id}/**  
  Delete a course.

- **GET /api/courses/{course_id}/students/**  
  List all students in a course.

- **GET /api/courses/{course_id}/grades/**  
  List grades for a specific course.

---

### 2. Students

- **GET /api/students/**  
  List all students.

- **POST /api/students/**  
  Create a new student.

- **GET /api/students/{student_id}/**  
  Get details of a specific student.

- **PUT /api/students/{student_id}/**  
  Update an existing student.

- **DELETE /api/students/{student_id}/**  
  Delete a student.

- **GET /api/students/{student_id}/courses/**  
  List all courses that a specific student is enrolled in.

---

### 3. Enrollments

- **GET /api/enrollments/**  
  List all enrollments.

- **POST /api/enrollments/**  
  Enroll a student in a course.

---

### 4. Grades

- **GET /api/grades/**  
  List all grades.

- **POST /api/grades/**  
  Add a grade for a student.

- **POST /api/grades/upload_csv/**  
  Bulk upload grades via CSV.

---

## Database Structure

### 1. Course
![Course Table](./images/course_table.png)

### 2. Student
![Student Table](./images/student_table.png)

### 3. Grade
![Grade Table](./images/grade_table.png)

### 4. Enrollment
![Enrollment Table](./images/enrollment_table.png)

## Frontend UI
### Course List
![Course List](./images/course_list_view.png)

### Add New Course
![Add New Course](./images/add_new course.png)

### Register Student
![Register Student](./images/register_student.png)

### Upload Grading
![Upload Grading](./images/upload_grading.png)

### View Grading
![View Grading](./images/view_grading.png)

### Download CSV
![Download CSV](./images/download_csv.png)
