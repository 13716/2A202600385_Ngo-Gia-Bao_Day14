# Knowledge Base được trích xuất từ access_control_sop.txt
KNOWLEDGE_BASE = [
    {
        "id": "sop_scope_purpose",
        "text": "QUY TRÌNH KIỂM SOÁT TRUY CẬP HỆ THỐNG (ACCESS CONTROL SOP). Phạm vi: Áp dụng cho tất cả nhân viên, contractor, và third-party vendor. Quy định quy trình cấp phép truy cập vào các hệ thống nội bộ của công ty."
    },
    {
        "id": "sop_level_1_read_only",
        "text": "Level 1 — Read Only: Áp dụng cho Tất cả nhân viên mới trong 30 ngày đầu. Phệ duyệt: Line Manager. Thời gian xử lý: 1 ngày làm việc."
    },
    {
        "id": "sop_level_2_standard",
        "text": "Level 2 — Standard Access: Áp dụng cho Nhân viên chính thức đã qua thử việc. Phê duyệt: Line Manager + IT Admin. Thời gian xử lý: 2 ngày làm việc."
    },
    {
        "id": "sop_level_3_elevated",
        "text": "Level 3 — Elevated Access: Áp dụng cho Team Lead, Senior Engineer, Manager. Phê duyệt: Line Manager + IT Admin + IT Security. Thời gian xử lý: 3 ngày làm việc."
    },
    {
        "id": "sop_level_4_admin",
        "text": "Level 4 — Admin Access: Áp dụng cho DevOps, SRE, IT Admin. Phê duyệt: IT Manager + CISO. Thời gian xử lý: 5 ngày làm việc. Yêu cầu thêm: Training bắt buộc về security policy."
    },
    {
        "id": "sop_workflow_steps",
        "text": "Quy trình yêu cầu cấp quyền: Bước 1: Nhân viên tạo Access Request ticket Jira (IT-ACCESS). Bước 2: Line Manager phê duyệt (1 ngày). Bước 3: IT Admin kiểm tra compliance và cấp quyền. Bước 4: IT Security review cấp 3/4. Bước 5: Thông báo email."
    },
    {
        "id": "sop_escalation_policy",
        "text": "Escalation thay đổi quyền: Áp dụng ngoài quy trình thông thường (Sự cố P1, Fix incident). On-call IT Admin cấp quyền tạm thời (max 24h) sau khi Tech Lead phê duyệt lời."
    },
    {
        "id": "sop_escalation_rules",
        "text": "Luật Escalation khẩn cấp: Sau 24h phải có ticket chính thức hoặc quyền bị thu hồi tự động. Mọi quyền tạm thời phải được ghi log vào hệ thống Security Audit."
    },
    {
        "id": "sop_revocation_cases",
        "text": "Thu hồi quyền: Nghỉ việc thu hồi ngay ngày cuối. Hết hạn hợp đồng thu hồi đúng ngày hết hạn. Chuyển bộ phận điều chỉnh trong 3 ngày làm việc."
    },
    {
        "id": "sop_audit_review",
        "text": "Audit: IT Security thực hiện access review mỗi 6 tháng. Mọi bất thường phải được báo cáo lên CISO trong vòng 24 giờ."
    },
    {
        "id": "sop_tools_systems",
        "text": "Công cụ quản lý: Ticket (Jira project IT-ACCESS), IAM (Okta), Audit log (Splunk), Email it-access@company.internal."
    }
]
