# views.py

import uuid
import openpyxl

from django.shortcuts             import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http                  import JsonResponse, HttpResponseBadRequest
from django.db                    import connection

# ─── 1. Excel Upload ──────────────────────────────────────────────────────────

@csrf_exempt
def upload_students(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        wb = openpyxl.load_workbook(request.FILES['excel_file'], data_only=True)
        ws = wb.active
        inserted = 0

        with connection.cursor() as cursor:
            for row in ws.iter_rows(min_row=2, values_only=True):
                if len(row) < 4:
                    continue

                college, project, domain, num_students = row[:4]
                try:
                    num_students = int(num_students)
                except (TypeError, ValueError):
                    continue

                num_students = max(0, min(4, num_students))

                base = 4
                for i in range(num_students):
                    offset = base + i*4
                    if offset + 3 >= len(row):
                        break
                    name    = row[offset]
                    email   = row[offset+1]
                    contact = row[offset+2]

                    if not name or not email:
                        continue

                    cursor.execute("""
                        INSERT INTO student_info
                          (id, college_name, project_name, domain,
                           number_of_students, name, email, contact)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (email) DO NOTHING
                    """, [
                        str(uuid.uuid4()),
                        college, project, domain,
                        num_students, name, email, contact
                    ])
                    inserted += 1

        return JsonResponse({"status": "success", "inserted": inserted})

    return JsonResponse({"status": "error", "message": "Invalid request"})



# ─── 2. QR Scanner Page ───────────────────────────────────────────────────────

from django.db import connection
from django.shortcuts import render

def scan_page(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, college_name, project_name, domain,
                   name, email, contact, attendance
            FROM student_info
            ORDER BY name
        """)
        rows = cursor.fetchall()

    students = [
        {
            "id": row[0],
            "college_name": row[1],
            "project_name": row[2],
            "domain": row[3],
            "name": row[4],
            "email": row[5],
            "contact": row[6],
            "attendance": row[7],
        }
        for row in rows
    ]
    return render(request, 'scan.html', {"students": students})



# ─── 3. API: Check Existence ─────────────────────────────────────────────────

def api_check_id(request, qr_id):
    """
    GET /api/check_id/<uuid:qr_id>/
      → { exists: true/false }
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM student_info WHERE id = %s LIMIT 1",
                [str(qr_id)]
            )
            exists = bool(cursor.fetchone())
    except Exception:
        return HttpResponseBadRequest("Invalid ID format")
    return JsonResponse({'exists': exists})


# ─── 4. API: List All Users ──────────────────────────────────────────────────

def api_users(request):
    """
    GET /api/users/
      → [ { id, name, email }, … ]
    """
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, email
              FROM student_info
             ORDER BY name
        """)
        rows = cursor.fetchall()

    data = [
        {'id': r[0], 'name': r[1], 'email': r[2]}
        for r in rows
    ]
    return JsonResponse(data, safe=False)


# ─── 5. API: Full Student Detail ─────────────────────────────────────────────

def api_student_detail(request, qr_id):
    """
    GET /api/student/<uuid:qr_id>/
      → JSON {
           college_name, project_name, domain,
           name, email, contact, attendance
         }
      also sets attendance=1 for this student
    """
    try:
        with connection.cursor() as cursor:
            # Fetch current details
            cursor.execute("""
                SELECT
                  college_name, project_name, domain,
                  name, email, contact, attendance
                FROM student_info
                WHERE id = %s
            """, [str(qr_id)])
            row = cursor.fetchone()

            if not row:
                return JsonResponse({'error': 'not found'}, status=404)

            # Immediately mark attendance = 1
            cursor.execute("""
                UPDATE student_info
                   SET attendance = 1
                 WHERE id = %s
            """, [str(qr_id)])
    except Exception:
        return HttpResponseBadRequest("Invalid ID format")

    keys = ['college_name', 'project_name', 'domain',
            'name', 'email', 'contact', 'attendance']
    data = dict(zip(keys, row))
    return JsonResponse(data)


import io
import qrcode
from django.conf       import settings
from django.core.mail  import EmailMessage
from django.db         import connection
from django.http       import JsonResponse
from django.views.decorators.http import require_POST

# @require_POST
# def api_send_qr_emails(request):
#     """
#     POST /api/send_qr_emails/
#       → generates QR for each student.id, emails it to student.email
#       → returns JSON { sent: <count>, failed: [<email list>] }
#     """
#     sent_count = 0
#     failed = []

#     # 1. Fetch all students
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT id, email FROM student_info WHERE email IS NOT NULL")
#         rows = cursor.fetchall()

#     for uid, email in rows:
#         try:
#             # 2. Generate QR image in memory
#             qr = qrcode.QRCode(box_size=10, border=4)
#             qr.add_data(str(uid))
#             qr.make(fit=True)
#             img = qr.make_image(fill_color="black", back_color="white")

#             buf = io.BytesIO()
#             img.save(buf, format='PNG')
#             buf.seek(0)

#             # 3. Create and send email
#             mail = EmailMessage(
#                 subject="Your Student QR Code",
#                 body=(
#                     "Hello,\n\n"
#                     "Please find attached your unique QR code for event check‑in.\n\n"
#                     "Thank you."
#                 ),
#                 from_email=settings.DEFAULT_FROM_EMAIL,
#                 to=[email],
#             )
#             mail.attach(f"{uid}.png", buf.read(), "image/png")
#             mail.send(fail_silently=False)

#             sent_count += 1

#         except Exception as e:
#             # log or collect failures
#             failed.append({'email': email, 'error': str(e)})

#     return JsonResponse({'sent': sent_count, 'failed': failed})

import io
import os
import qrcode
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db import connection
# from django.core.mail import EmailMessage  # Mail logic is commented

# Constants for ticket template
TEMPLATE_PATH = "qr-design.png"   # Blank ticket template
X, Y    = 547, 790                # Top‑left corner of QR box
BW, BH  = 320, 320                # QR box width & height
TICKETS_DIR = "tickets"          # Folder to store PDF tickets

# Ensure folder exists
os.makedirs(TICKETS_DIR, exist_ok=True)

def to_snake_case(name):
    return name.strip().lower().replace(" ", "_")

@require_POST
def api_send_qr_emails(request):
    """
    POST /api/send_qr_emails/
      → generates QR for each student.id, places it on template,
        saves as ticket PDF in /tickets folder with name_snake_case.pdf
    """
    sent_count = 0
    failed = []

    with connection.cursor() as cursor:
        cursor.execute("SELECT id, email, name FROM student_info WHERE email IS NOT NULL")
        rows = cursor.fetchall()

    for uid, email, name in rows:
        try:
            # Generate QR code in memory
            qr = qrcode.QRCode(box_size=10, border=4)
            qr.add_data(str(uid))
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            # Load and resize QR
            qr_resized = img.resize((BW, BH), Image.LANCZOS)

            # Load ticket template
            if not os.path.exists(TEMPLATE_PATH):
                raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
            template = Image.open(TEMPLATE_PATH).convert("RGB")

            # Paste QR onto ticket
            template.paste(qr_resized, (X, Y))

            # Save as PDF in tickets/ folder
            filename = f"{to_snake_case(name)}.pdf"
            output_path = os.path.join(TICKETS_DIR, filename)
            template.save(output_path, format="PDF")

            sent_count += 1

            # # Send email with PDF attachment (COMMENTED OUT)
            # mail = EmailMessage(
            #     subject="Your Student QR Code",
            #     body=(
            #         "Hello,\n\n"
            #         "Please find attached your unique QR code for event check‑in.\n\n"
            #         "Thank you."
            #     ),
            #     from_email=settings.DEFAULT_FROM_EMAIL,
            #     to=[email],
            # )
            # with open(output_path, "rb") as f:
            #     mail.attach(filename, f.read(), "application/pdf")
            # mail.send(fail_silently=False)

        except Exception as e:
            failed.append({'email': email, 'error': str(e)})

    return JsonResponse({'sent': sent_count, 'failed': failed})


from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def api_toggle_attendance(request, qr_id):
    """
    POST /api/toggle_attendance/<uuid:qr_id>/
      → toggles attendance 0 ⇄ 1
      ← JSON { success: true, new_state: 0|1 }
    """
    with connection.cursor() as cursor:
        cursor.execute("SELECT attendance FROM student_info WHERE id = %s", [str(qr_id)])
        row = cursor.fetchone()
        if not row:
            return JsonResponse({'error': 'Student not found'}, status=404)

        current = row[0]
        new_state = 1 if current == 0 else 0

        cursor.execute("UPDATE student_info SET attendance = %s WHERE id = %s", [new_state, str(qr_id)])
    return JsonResponse({'success': True, 'new_state': new_state})
