export interface Course {
  id: number;
  course_id: string;
  course_name: string;
  instructor: string;
  semester: string;
  created_at: string;
  updated_at: string;
}

export interface Student {
  id: number;
  student_id: string;
  name: string;
  email: string;
  enrollment_date: string;
  created_at: string;
  updated_at: string;
}

export interface Grade {
  id: number;
  student: Student;
  course: Course;
  grade: string;
  comments?: string;
  created_at: string;
  updated_at: string;
}

export interface Enrollment {
  id: number;
  student: Student;
  course: Course;
  enrolled_date: string;
} 