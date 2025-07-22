from django.urls import path
from .views import (
    upload_students,
    scan_page,
    api_check_id,
    api_users,
    api_student_detail,
    api_send_qr_emails,
    api_toggle_attendance,
    api_generate_qr_pdfs,
)

urlpatterns = [
    # 1. Upload Excel
    path('upload/', upload_students, name='upload_students'),
    # 2. Scanner Page
    path('', scan_page, name='scan_page'),
    # 3. Check ID
    path('api/check_id/<uuid:qr_id>/', api_check_id, name='api_check_id'),
    # 4. List Users
    path('api/users/', api_users, name='api_users'),
    # 5. Student Detail
    path('api/student/<uuid:qr_id>/', api_student_detail, name='api_student_detail'),
    # 6. Generate QR PDFs
    path('api/generate_qr_pdfs/', api_generate_qr_pdfs, name='api_generate_qr_pdfs'),
    # 7. Send QR Emails
    path('api/send_qr_emails/', api_send_qr_emails, name='api_send_qr_emails'),
    # 8. Toggle Attendance
    path('api/toggle_attendance/<uuid:qr_id>/', api_toggle_attendance, name='toggle_attendance'),
]
