from django.urls import path
from .views import (
    upload_students,
    scan_page,
    api_check_id,
    api_users,
    api_student_detail,
    api_send_qr_emails,
    api_toggle_attendance
)

urlpatterns = [
    # ─── 1. Upload Students ─────────────────────────────────────────────────────
    path('upload/', upload_students, name='upload_students'),
    
    # ─── 2. QR Scanner Page ───────────────────────────────────────────────────────
    path('scan/', scan_page, name='scan_page'),

    # ─── 3. API: Check Existence ─────────────────────────────────────────────────
    path('api/check_id/<uuid:qr_id>/', api_check_id, name='api_check_id'),

    # ─── 4. API: List All Users ──────────────────────────────────────────────────
    path('api/users/', api_users, name='api_users'),

    # ─── 5. API: Full Student Detail ─────────────────────────────────────────────
    path('api/student/<uuid:qr_id>/', api_student_detail, name='api_student_detail'),

    path('api/send_qr_emails/', api_send_qr_emails, name='api_send_qr_emails'),

    path('api/toggle_attendance/<uuid:qr_id>/', api_toggle_attendance, name='toggle_attendance'),


]
