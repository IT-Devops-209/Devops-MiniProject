# Bài kiểm tra đầu giờ — Đóng gói và chạy Campus Hub với Docker

## Thông tin sinh viên
- **Họ và tên:** [Họ và tên sinh viên]
- **Mã sinh viên:** [Mã sinh viên]
- **Email:** qn50606@gmail.com
- **Repository:** https://github.com/IT-Devops-209/Devops-TestDauGio.git

---

## 1. Hướng dẫn chạy hệ thống

### 1.1. Kiểm thử backend bằng Gradle
```powershell
cd backend
./gradlew test
```

### 1.2. Đóng gói Docker Image backend
```powershell
cd backend
docker build -t campus-hub-backend .
```
Kiểm tra image đã tạo:
```powershell
docker images campus-hub-backend
```

### 1.3. Khởi chạy toàn bộ hệ thống bằng Docker Compose
Tại thư mục gốc chứa file `compose.yml`:
```powershell
docker compose up -d
```

Kiểm tra trạng thái các service:
```powershell
docker compose ps
```

Dừng hệ thống khi cần:
```powershell
docker compose down
```

---

## 2. Cổng và URL kiểm tra hệ thống

| Dịch vụ | Địa chỉ / URL | Mô tả |
|---|---|---|
| **Health Check Endpoint** | [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health) | Trả về HTTP 200 và trạng thái `UP` |
| **API Danh mục bài đăng** | [http://localhost:8080/api/categories](http://localhost:8080/api/categories) | Xác thực kết nối dữ liệu MySQL |
| **Backend Port** | `8080` | Cổng HTTP công khai của Backend |
| **MySQL Port** | `3307` (Host) -> `3306` (Container) | CSDL `campus_hub`, user `campus_user` |

---

## 3. Minh chứng kết quả thực hiện

### 3.1. Gradle Test & Docker Image backend build thành công
Gradle kiểm thử thành công 5/5 test cases và Docker Image `campus-hub-backend:latest` được build hoàn tất với kiến trúc Multi-stage:
![Minh chứng 1: Docker Build Backend](docs/images/01-docker-build.png)

### 3.2. Trạng thái các service sau khi khởi chạy Docker Compose
Cả hai service `campus-hub-backend` và `campus-hub-mysql` đều khởi động thành công và duy trì trạng thái `healthy`:
![Minh chứng 2: Docker Compose Services](docs/images/02-docker-compose-ps.png)

### 3.3. Kết quả gọi `/actuator/health`
Endpoint `/actuator/health` trả về HTTP 200 với trạng thái `UP`, kết nối database thành công:
![Minh chứng 3: Actuator Health](docs/images/03-actuator-health.png)

---

## 4. Kiến trúc & Cấu hình hệ thống

- **Base Image:** `eclipse-temurin:21-jdk-alpine` (Build stage) và `eclipse-temurin:21-jre-alpine` (Runtime stage).
- **Cơ sở dữ liệu:** `mysql:8.0` chạy trên volume `mysql_data`, tự động migration schema qua Flyway khi khởi động.
- **Biến môi trường Backend:**
  - `DB_URL`: `jdbc:mysql://mysql:3306/campus_hub?createDatabaseIfNotExist=true&useSSL=false&allowPublicKeyRetrieval=true`
  - `DB_USERNAME`: `campus_user`
  - `DB_PASSWORD`: `campus_password`
  - `SERVER_PORT`: `8080`
- **Network:** Bridge network `campus-network` kết nối an toàn giữa backend và MySQL bằng tên service `mysql`.

---

# Campus Hub Base

Campus Hub là dự án nền cho Mini Project Session 13. Ứng dụng cung cấp một không gian chung để sinh viên đăng sự kiện, tìm đồ thất lạc, hỏi đáp, trao đổi đồ dùng và tìm nhóm.

## Chức năng có sẵn

- Xem, tìm kiếm và lọc bài đăng.
- Đăng ký, đăng nhập bằng HTTP Basic.
- Tạo bài đăng theo chuyên mục.
- Bình luận và bày tỏ quan tâm.
- Chủ bài đăng có thể đánh dấu bài đã hoàn tất.
- Quản trị viên có quyền quản lý trạng thái bài đăng qua API.
- Health check tại `/actuator/health`.

Tài khoản mẫu được tạo khi ứng dụng khởi động lần đầu:

| Vai trò | Tên đăng nhập | Mật khẩu |
|---|---|---|
| Sinh viên | `student` | `student123` |
| Quản trị viên | `admin` | `admin123` |
