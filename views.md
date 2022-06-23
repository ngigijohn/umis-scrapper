home_url = https://registration.ueab.ac.ke/ueab/
login_verification_url = https://registration.ueab.ac.ke/ueab/j_security_check'

student_login_view = https://registration.ueab.ac.ke/ueab/a_students.jsp?view=1:0
student_dashboard_view = https://registration.ueab.ac.ke/ueab/a_students.jsp?view=1:0

student_profile = https://registration.ueab.ac.ke/ueab/a_students.jsp?view=2:0
student_major_details = https://registration.ueab.ac.ke/ueab/a_students.jsp?view=2:1&data=

## The urls follow a similar pattern { base_url + query_string_parameter }

---

**base_url = https://registration.ueab.ac.ke/ueab/a_students.jsp**

| Page                     | query_string_parameter           |
| ------------------------ | -------------------------------- |
| schools_list             | ?view=10:0&data=                 |
| school_detail            | view=10:0:1&data=[EDUC,BUSS,etc] |
| e.g. school_of_education | view=10:0:1&data=EDUC            |
| current_timetable        | ?view=9:0                        |
| semester_gpa             | ?view=19:0                       |
| unofficial_transcript    | ?view=21:0                       |
| semester_register        | ?view=22:0                       |
| selected_courses         | ?view=90:0                       |
| selected_timetable       | ?view=28:0                       |
| check_listing            | ?view=26:0                       |
|                          |                                  |

## Finance Statement

**base_url = https://registration.ueab.ac.ke/ueab/a_statement.jsp**
| Page | query_string_parameter |
| ----------- | ----------- |
| finance_statement | ?view=22:0 |

## Action Buttons

| Button            | XPATH                                                      |
| ----------------- | ---------------------------------------------------------- |
| semester_register | //\*[@id="portletBody"]/div/table/tbody/tr[8]/td[2]/button |
