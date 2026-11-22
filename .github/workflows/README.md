# DevSecOps cho hạ tầng mạng và dịch vụ: Kiểm toán cấu hình CIS Benchmark và quét lỗ hổng image

## Trọng tâm triển khai
- **Kiểm toán cấu hình Cisco IOS theo CIS Benchmark** bằng script Python (`audit.py`) tự động trong CI/CD.
- **Đóng gói ứng dụng dịch vụ & quét lỗ hổng Docker Image bằng Trivy** trong GitHub Actions (chặn pipeline nếu phát hiện lỗ hổng mức `CRITICAL`).

---

## Cấu trúc thư mục dự án
```text
├── .github/
│   └── workflows/
│       └── devsecops-ci.yml          # Pipeline CI/CD GitHub Actions (Phần 4)
├── Nguoi1_Cisco_Hardening/
│   └── Nguoi1_Cisco_Hardening/
│       ├── Checklist_CIS.csv         # Danh sách 20 tiêu chí CIS Benchmark
│       ├── Cisco_Hardening_R1.pkt    # Mô hình mạng Cisco Packet Tracer
│       ├── router_before.cfg         # Cấu hình trước khi hardening
│       ├── router_after.cfg          # Cấu hình sau khi hardening
│       ├── Nguoi2_Python_Audit/
│       │   ├── audit.py              # Script kiểm toán cấu hình Cisco IOS
│       │   └── reports/              # Báo cáo before.json, after.json, comparison.html
│       └── Nguoi3_Report/            # Báo cáo Word & ảnh minh chứng
├── app.py                            # Ứng dụng Web mẫu (Flask)
├── requirements.txt                  # Thư viện Python cho ứng dụng Web
├── Dockerfile                        # File đóng gói Docker Image
└── README.md                         # Tài liệu mô tả dự án & Phần 4
```

---

## Phần 4: Cách sản phẩm hoạt động khi demo

### 1. Luồng xử lý tự động trong GitHub Actions
Khi có thao tác **push code** hoặc **cập nhật file cấu hình** lên nhánh `main` / `master`, workflow `.github/workflows/devsecops-ci.yml` tự động kích hoạt 2 giai đoạn:

1. **Job 1 — Python Audit Cisco IOS (`cisco-ios-cis-audit`):**
   - Thiết lập môi trường Python 3.11 trên runner `ubuntu-latest`.
   - Chạy `Nguoi1_Cisco_Hardening/Nguoi1_Cisco_Hardening/Nguoi2_Python_Audit/audit.py` để kiểm tra `router_before.cfg` và `router_after.cfg` theo 20 tiêu chí CIS.
   - Tính điểm tuân thủ (tăng từ **0.0%** lên **100.0%** trên 17 tiêu chí đánh giá được) và xuất báo cáo `before.json`, `after.json`, `comparison.html`.
   - Đóng gói thư mục `reports/` thành **GitHub Actions Artifact** (`cisco-ios-cis-reports`) để tải về trực tiếp trên giao diện GitHub.

2. **Job 2 — Build Docker Image & Trivy Scan (`docker-trivy-scan`):**
   - Build Docker image từ `Dockerfile` của dịch vụ mẫu (`devsecops-cisco-service:ci`).
   - Sử dụng **Trivy** (`aquasecurity/trivy-action`) quét image và thống kê các lỗ hổng bảo mật mức **HIGH** và **CRITICAL**.
   - **Cổng kiểm soát (Quality Gate):** Thiết lập `exit-code: "1"` cho mức `CRITICAL` — nếu image tồn tại lỗ hổng nghiêm trọng, pipeline lập tức đánh dấu **FAIL**; nếu sạch lỗ hổng `CRITICAL`, pipeline chuyển sang **PASS**.

### 2. Kịch bản demo 2 trạng thái (FAIL vs. PASS)
- **Kịch bản 1 — Trạng thái FAIL (Phát hiện lỗ hổng CRITICAL):**
  - Đổi dòng đầu tiên trong `Dockerfile` sang base image cũ có lỗ hổng nghiêm trọng (ví dụ `FROM python:3.8-slim` hoặc `FROM ubuntu:18.04`) và commit lên nhánh `main`.
  - GitHub Actions chạy Job 1 thành công, nhưng Job 2 dừng lại với trạng thái **FAIL (màu đỏ)** do Trivy phát hiện lỗ hổng mức `CRITICAL`.
- **Kịch bản 2 — Trạng thái PASS (Đã khắc phục & hardening):**
  - Khôi phục `Dockerfile` về `FROM python:3.12-slim` (hoặc `FROM python:3.12-alpine`) và commit lại.
  - Cả 2 job trong GitHub Actions đều hoàn tất với trạng thái **PASS (màu xanh)** và xuất đầy đủ báo cáo kiểm toán CIS.
