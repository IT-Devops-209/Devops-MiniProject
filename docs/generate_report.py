import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = Document()

    # Set margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)

    # Style colors
    PRIMARY = RGBColor(27, 77, 52)     # Deep Green #1B4D34
    SECONDARY = RGBColor(46, 117, 89)  # Forest Green #2E7559
    DARK_TEXT = RGBColor(30, 41, 35)   # #1E2923
    GRAY_TEXT = RGBColor(90, 100, 95)  # #5A645F

    # Set Normal Font
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = DARK_TEXT

    # ==================== TRANG BÌA ====================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\nKHOA CÔNG NGHỆ THÔNG TIN\n---***---")
    r_inst.font.size = Pt(13)
    r_inst.font.bold = True
    r_inst.font.color.rgb = DARK_TEXT

    for _ in range(3):
        doc.add_paragraph()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_title.add_run("BÁO CÁO BÀI TẬP LỚN / MINI PROJECT\n")
    r_t1.font.size = Pt(16)
    r_t1.font.bold = True
    r_t1.font.color.rgb = SECONDARY

    r_t2 = p_title.add_run("HỆ THỐNG CAMPUS HUB MỞ RỘNG:\nQUẢN LÝ ĐĂNG KÝ THAM GIA, ỨNG TUYỂN NHÓM VÀ CONTAINER HÓA ĐA TẦNG DOCKER COMPOSE\n")
    r_t2.font.size = Pt(20)
    r_t2.font.bold = True
    r_t2.font.color.rgb = PRIMARY

    r_t3 = p_title.add_run("(Học phần: DevOps & Triển khai Hệ thống phần mềm - Session 13)")
    r_t3.font.size = Pt(13)
    r_t3.font.italic = True
    r_t3.font.color.rgb = GRAY_TEXT

    for _ in range(4):
        doc.add_paragraph()

    # Table for student info
    info_table = doc.add_table(rows=4, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_data = [
        ("Sinh viên thực hiện:", "Nguyễn Quang Anh"),
        ("Mã sinh viên:", "N24DTCn001"),
        ("Email liên hệ:", "qn50606@gmail.com"),
        ("Liên kết GitHub dự án:", "https://github.com/IT-Devops-209/Devops-MiniProject.git")
    ]
    for i, (k, v) in enumerate(info_data):
        row = info_table.rows[i]
        c0 = row.cells[0]
        c1 = row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(12)
        r1 = p1.add_run(v)
        r1.font.size = Pt(12)
        if i == 3:
            r1.font.bold = True
            r1.font.color.rgb = PRIMARY
        set_cell_margins(c0, 60, 60, 100, 100)
        set_cell_margins(c1, 60, 60, 100, 100)

    for _ in range(4):
        doc.add_paragraph()

    p_footer = doc.add_paragraph()
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_footer.add_run("Hà Nội, Tháng 10 năm 2026")
    r_foot.font.size = Pt(12)
    r_foot.font.italic = True

    doc.add_page_break()

    # Helper function for headings
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = SECONDARY
        return p

    def add_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.bold = True
        p.add_run(text)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.font.bold = True
        p.add_run(text)
        return p

    def add_img_safe(img_path, caption):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            run = p_img.add_run()
            run.add_picture(img_path, width=Inches(5.8))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r_c = p_cap.add_run(caption)
            r_c.font.size = Pt(10)
            r_c.font.italic = True
            r_c.font.color.rgb = GRAY_TEXT

    # ==================== PHẦN 1: TÓM TẮT SẢN PHẨM ====================
    add_h1("1. TÓM TẮT SẢN PHẨM VÀ ĐIỂM TRUY CẬP HỆ THỐNG")
    
    add_p("Trong khuôn khổ Mini Project tổng hợp của Session 13, nhóm đã phát triển và hoàn thiện giải pháp Campus Hub Extended dựa trên dự án nền được giảng viên cung cấp. Sản phẩm được mở rộng toàn diện cả về mặt tính năng nghiệp vụ người dùng lẫn kiến trúc DevOps container hóa chuẩn công nghiệp.")
    
    add_h2("1.1. Thông tin liên kết và mã nguồn dự án")
    add_bullet("https://github.com/IT-Devops-209/Devops-MiniProject.git", "GitHub Repository: ")
    add_bullet("Nguyễn Quang Anh (Mã SV: N24DTCn001)", "Sinh viên thực hiện: ")
    add_bullet("main (commit hoàn chỉnh Session 13)", "Phiên bản triển khai: ")

    add_h2("1.2. Bảng thông số điểm truy cập dịch vụ (Endpoints)")
    ep_table = doc.add_table(rows=5, cols=3)
    ep_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    ep_headers = ["Thành phần", "Địa chỉ truy cập (URL / Port)", "Mô tả vai trò"]
    for j, h in enumerate(ep_headers):
        cell = ep_table.cell(0, j)
        set_cell_background(cell, "1F6F4D")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 100, 100)

    ep_rows = [
        ("Frontend Web App", "http://localhost:3000", "Giao diện người dùng Single Page App (React + Nginx Reverse Proxy)"),
        ("Backend REST API", "http://localhost:8080/api", "Hệ thống backend Spring Boot 3 xử lý API, logic nghiệp vụ & xác thực"),
        ("Health Check", "http://localhost:8080/actuator/health", "Actuator endpoint giám sát trạng thái sức khỏe (UP) của service"),
        ("MySQL Database", "localhost:3307 (Container 3306)", "Cơ sở dữ liệu quan hệ MySQL 8.0 lưu trữ bền vững qua Docker Volume")
    ]
    for i, row in enumerate(ep_rows):
        for j, val in enumerate(row):
            cell = ep_table.cell(i + 1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F4F8F5")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10.5)
            set_cell_margins(cell, 60, 60, 100, 100)

    add_h2("1.3. Tài khoản mẫu thử nghiệm")
    acc_table = doc.add_table(rows=4, cols=3)
    acc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Tên đăng nhập", "Mật khẩu", "Vai trò và Quyền hạn"]):
        cell = acc_table.cell(0, j)
        set_cell_background(cell, "2E7559")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 100, 100)
    acc_data = [
        ("admin", "admin123", "Quản trị viên (ADMIN) - Toàn quyền quản trị bài đăng, phê duyệt ứng viên, ẩn bài"),
        ("student", "student123", "Sinh viên (USER) - Đăng bài, gửi đơn ứng tuyển, lưu bài viết yêu thích, bình luận"),
        ("minhchau", "chau123", "Sinh viên (USER) - Dùng đối soát quá trình nộp đơn và duyệt đơn chéo")
    ]
    for i, row in enumerate(acc_data):
        for j, val in enumerate(row):
            cell = acc_table.cell(i + 1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F4F8F5")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10.5)
            set_cell_margins(cell, 60, 60, 100, 100)

    # ==================== PHẦN 2: PHÂN TÍCH BÀI TOÁN ====================
    add_h1("2. PHÂN TÍCH BÀI TOÁN, NGƯỜI DÙNG VÀ PHẠM VI")
    
    add_h2("2.1. Bối cảnh và Vấn đề thực tế cần giải quyết")
    add_p("Trong môi trường đại học, việc giao lưu và hợp tác giữa các sinh viên diễn ra rất thường xuyên. Các nhu cầu phổ biến nhất bao gồm: tìm thành viên ghép nhóm làm đồ án môn học (đặc biệt là đồ án chuyên ngành như DevOps, Công nghệ phần mềm), đăng ký tham gia các sự kiện/workshop do câu lạc bộ tổ chức, và chia sẻ trao đổi đồ dùng học tập.")
    add_p("Tuy nhiên, ở dự án nền Campus Hub ban đầu, hệ thống chỉ hỗ trợ xem bài, đăng bài viết và bình luận chung. Tồn tại các hạn chế lớn:", "Vấn đề của dự án nền: ")
    add_bullet("Không có kênh liên lạc riêng tư: Sinh viên muốn ứng tuyển tham gia nhóm phải để lại số điện thoại/Zalo công khai trong bình luận, gây nguy cơ lộ lọt dữ liệu cá nhân.")
    add_bullet("Thiếu quy trình xét duyệt thành viên: Tác giả bài viết không thể quản lý số lượng người muốn tham gia, không biết kỹ năng của từng bạn và không có nút duyệt/từ chối.")
    add_bullet("Sinh viên ứng tuyển không theo dõi được kết quả: Không có trang quản lý đơn cá nhân, không biết mình đã được nhóm chấp nhận hay bị từ chối.")
    add_bullet("Chưa hỗ trợ lưu bài đọc sau (Bookmarks) và bộ lọc trạng thái bài viết còn đơn điệu.")

    add_h2("2.2. Giá trị giải pháp mang lại")
    add_p("Campus Hub Extended mang đến một giải pháp hoàn chỉnh cho sinh viên với các giá trị cốt lõi:")
    add_bullet("Quy trình Ứng tuyển & Phê duyệt minh bạch: Cho phép sinh viên điền thông tin liên hệ, nguyện vọng, kỹ năng để gửi tới chủ bài viết. Tác giả bài có bảng quản lý trực quan để duyệt hoặc từ chối.", "1. ")
    add_bullet("Bảo mật dữ liệu cá nhân: Thông tin liên hệ (SĐT/Zalo) của ứng viên chỉ hiển thị duy nhất cho chủ bài viết và quản trị viên, không bị công khai trên diễn đàn.", "2. ")
    add_bullet("Tiện ích quản lý cá nhân: Bổ sung tính năng Lưu bài viết yêu thích (Bookmarks) và trung tâm Quản lý đơn đã nộp (My Applications).", "3. ")
    add_bullet("Đóng gói chuẩn DevOps: Triển khai toàn diện cả 3 tầng (Frontend Nginx, Backend Spring Boot, MySQL) qua Docker Compose với tự động hóa CI/CD.", "4. ")

    add_h2("2.3. Phạm vi thực hiện và Những nội dung chủ động không thực hiện")
    add_p("Các chức năng được thực hiện đầy đủ:", "Phạm vi thực hiện: ")
    add_bullet("Module Quản lý Đăng ký & Ứng tuyển (Applications) với đầy đủ CRUD, quy trình duyệt trạng thái PENDING -> ACCEPTED/REJECTED/CANCELLED.")
    add_bullet("Module Đánh dấu & Lưu bài viết yêu thích (Bookmarks).")
    add_bullet("Bộ lọc đa tiêu chí theo từ khóa, chuyên mục và trạng thái bài viết (PUBLISHED / RESOLVED).")
    add_bullet("Đóng gói Multi-stage Dockerfile cho Frontend và Backend, Docker Compose điều phối 3 containers.")
    add_bullet("GitHub Actions Pipeline kiểm thử tự động và build Docker images.")
    add_p("Theo đúng định hướng tinh gọn, nhất quán và ổn định của Session 13, nhóm chủ động không thực hiện các tính năng như thanh toán trực tuyến hoặc kênh chat WebSocket đa người dùng, vì các tính năng này không nằm trong trọng tâm phân tích quy trình nghiệp vụ và kiến trúc triển khai của dự án.", "Nội dung chủ động không thực hiện: ")

    # ==================== PHẦN 3: LUỒNG SỬ DỤNG VÀ THIẾT KẾ GIAO DIỆN ====================
    add_h1("3. LUỒNG SỬ DỤNG VÀ THIẾT KẾ GIAO DIỆN")

    add_h2("3.1. Luồng sử dụng chính (Core Business Workflow)")
    add_p("Hệ thống vận hành trọn vẹn theo 3 luồng sử dụng nghiệp vụ liên hoàn:")
    add_bullet("Bước 1: Sinh viên đăng nhập vào hệ thống, duyệt danh sách bài viết trên trang chủ hoặc lọc theo chuyên mục 'Tìm nhóm' / 'Sự kiện'.", "Luồng 1 - Ứng tuyển nhóm: ")
    add_bullet("Bước 2: Sinh viên mở bài viết chi tiết, bấm nút 'Gửi đơn đăng ký tham gia'.")
    add_bullet("Bước 3: Nhập số điện thoại/Zalo liên hệ, vai trò/kỹ năng mong muốn (ví dụ: 'DevOps / Backend'), và lời nhắn giới thiệu ngắn.")
    add_bullet("Bước 4: Hệ thống xác thực tính hợp lệ, lưu đơn với trạng thái PENDING và hiển thị huy hiệu trạng thái cho sinh viên.")
    add_bullet("Bước 1: Chủ bài viết mở bài đăng của mình và kéo đến khu vực 'Đăng ký tham gia & Ứng tuyển nhóm'.", "Luồng 2 - Phê duyệt ứng viên: ")
    add_bullet("Bước 2: Hệ thống hiển thị danh sách toàn bộ các ứng viên đã nộp đơn kèm thông tin liên hệ và lời nhắn.")
    add_bullet("Bước 3: Tác giả nhấn nút 'Chấp nhận' (ACCEPTED) hoặc 'Từ chối' (REJECTED). Dữ liệu được cập nhật tức thời.")
    add_bullet("Sinh viên có thể đánh dấu lưu các bài viết quan tâm bằng icon ngôi sao. Bấm vào tab 'Đã lưu' trên thanh điều hướng để xem lại danh sách bài viết này.", "Luồng 3 - Lưu bài viết: ")

    add_h2("3.2. Xử lý các trường hợp ngoại lệ và dữ liệu không hợp lệ")
    add_bullet("Tự đăng ký bài của chính mình: Hệ thống kiểm tra ID tác giả và người nộp, chặn lại với thông báo: 'Bạn không thể tự đăng ký tham gia bài đăng của chính mình'.", "Lỗi nghiệp vụ 1: ")
    add_bullet("Nộp đơn trùng lặp: Ngăn chặn gửi 2 đơn đang hoạt động cho cùng một bài viết, phản hồi mã lỗi 409 Conflict.", "Lỗi nghiệp vụ 2: ")
    add_bullet("Đăng ký bài đã đóng (RESOLVED) hoặc ẩn (HIDDEN): Hệ thống từ chối nhận đơn mới với bài không còn ở trạng thái PUBLISHED.", "Lỗi nghiệp vụ 3: ")
    add_bullet("Người lạ xem thông tin liên hệ của ứng viên: API trả về 403 Forbidden nhằm bảo vệ thông tin cá nhân của sinh viên.", "Lỗi phân quyền 4: ")

    add_h2("3.3. Hình ảnh giao diện minh họa thực tế")
    add_img_safe("docs/images/04-campus-hub-feed.png", "Hình 1: Giao diện Trang chủ Feed với bộ lọc đa tiêu chí và thống kê bài viết")
    add_img_safe("docs/images/05-post-collaboration-detail.png", "Hình 2: Giao diện Chi tiết bài viết và Khu vực Quản lý Ứng tuyển dành cho Chủ bài")

    # ==================== PHẦN 4: THIẾT KẾ CHỨC NĂNG, API VÀ CSDL ====================
    add_h1("4. THIẾT KẾ CHỨC NĂNG, API VÀ DỮ LIỆU")

    add_h2("4.1. Danh sách RESTful API")
    api_table = doc.add_table(rows=8, cols=4)
    api_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Phương thức", "Endpoint", "Yêu cầu quyền", "Mô tả chức năng"]):
        cell = api_table.cell(0, j)
        set_cell_background(cell, "1F6F4D")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 80, 80)

    apis = [
        ("POST", "/api/posts/{id}/applications", "Authenticated", "Nộp đơn đăng ký tham gia sự kiện / nhóm"),
        ("GET", "/api/posts/{id}/applications", "Owner / Admin", "Lấy danh sách người đăng ký của bài viết"),
        ("GET", "/api/posts/{id}/applications/my", "Authenticated", "Lấy thông tin đơn đăng ký của người dùng hiện tại"),
        ("GET", "/api/users/me/applications", "Authenticated", "Lấy danh sách toàn bộ đơn đăng ký mà sinh viên đã nộp"),
        ("PATCH", "/api/applications/{id}/status", "Owner / Admin", "Cập nhật trạng thái đơn (ACCEPTED / REJECTED)"),
        ("DELETE", "/api/applications/{id}", "Applicant", "Hủy đơn đăng ký khi còn ở trạng thái PENDING"),
        ("POST", "/api/posts/{id}/bookmark", "Authenticated", "Bật / tắt lưu bài viết vào mục yêu thích (Toggle)")
    ]
    for i, row in enumerate(apis):
        for j, val in enumerate(row):
            cell = api_table.cell(i + 1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F4F8F5")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10)
            if j == 0:
                r.font.bold = True
            set_cell_margins(cell, 60, 60, 80, 80)

    add_h2("4.2. Thiết kế Mô hình Cơ sở Dữ liệu (Database Schema)")
    add_p("Hệ thống sử dụng Flyway để quản lý phiên bản cơ sở dữ liệu. Phiên bản mới bổ sung file migration V2__add_applications_and_bookmarks.sql tạo thêm 2 bảng quan hệ:")
    
    add_bullet("Bảng post_applications: Quản lý thông tin đơn ứng tuyển, liên kết khóa ngoại với posts(id) và users(id). Có ràng buộc duy nhất UNIQUE(post_id, applicant_id).", "1. ")
    add_bullet("Bảng bookmarks: Quản lý danh sách lưu bài viết của sinh viên, ràng buộc UNIQUE(post_id, user_id).", "2. ")

    schema_table = doc.add_table(rows=9, cols=4)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Tên bảng", "Tên cột", "Kiểu dữ liệu", "Ràng buộc & Ghi chú"]):
        cell = schema_table.cell(0, j)
        set_cell_background(cell, "2E7559")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 80, 80)

    fields = [
        ("post_applications", "id", "BIGINT AUTO_INCREMENT", "PRIMARY KEY"),
        ("post_applications", "post_id", "BIGINT NOT NULL", "FK -> posts(id) ON DELETE CASCADE"),
        ("post_applications", "applicant_id", "BIGINT NOT NULL", "FK -> users(id)"),
        ("post_applications", "contact_info", "VARCHAR(100) NOT NULL", "SĐT / Zalo / Telegram"),
        ("post_applications", "message", "VARCHAR(500) NOT NULL", "Lời nhắn gửi tác giả"),
        ("post_applications", "role_or_skill", "VARCHAR(150)", "Kỹ năng, vai trò mong muốn"),
        ("post_applications", "status", "VARCHAR(20) NOT NULL", "CHECK IN (PENDING, ACCEPTED, REJECTED, CANCELLED)"),
        ("bookmarks", "post_id, user_id", "BIGINT, BIGINT", "FK -> posts, users, UNIQUE(post_id, user_id)")
    ]
    for i, row in enumerate(fields):
        for j, val in enumerate(row):
            cell = schema_table.cell(i + 1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F4F8F5")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10)
            set_cell_margins(cell, 60, 60, 80, 80)

    # ==================== PHẦN 5: KIẾN TRÚC VÀ TRIỂN KHAI ====================
    add_h1("5. KIẾN TRÚC PHẦN MỀM VÀ KIẾN TRÚC TRIỂN KHAI DOCKER")

    add_h2("5.1. Kiến trúc 3 tầng (3-Tier Container Architecture)")
    add_p("Hệ thống được tổ chức theo mô hình phân tầng chặt chẽ và đóng gói toàn bộ trong Docker Compose:")
    add_bullet("Tầng 1 - Presentation Layer (Frontend Container): Ứng dụng SPA viết bằng React 18, Vite. Được đóng gói qua Multi-stage build với Node 22 Alpine, phục vụ bằng máy chủ Nginx 1.27 Alpine. Nginx đóng vai trò Reverse Proxy nhận yêu cầu từ trình duyệt (cổng 3000), phục vụ tài nguyên tĩnh và chuyển tiếp các request /api/ và /actuator/ vào container Backend nội bộ.")
    add_bullet("Tầng 2 - Business Logic Layer (Backend Container): Ứng dụng Java Spring Boot 3 đóng gói Multi-stage build với Eclipse Temurin 21 JDK -> JRE Alpine. Chạy dưới quyền người dùng non-root (appuser) nhằm tuân thủ nguyên tắc bảo mật. Xử lý logic nghiệp vụ, JPA, Hibernate và Spring Security.")
    add_bullet("Tầng 3 - Data Storage Layer (Database Container): Cơ sở dữ liệu MySQL 8.0, cấu hình kết nối thông qua mạng nội bộ campus-network. Dữ liệu được lưu trữ bền vững qua Docker Named Volume (mysql_data) không bị mất khi container khởi động lại.")

    add_h2("5.2. Đường ống Tự động hóa CI/CD (GitHub Actions)")
    add_p("File cấu hình .github/workflows/ci.yml thiết lập quy trình tích hợp liên tục tự động mỗi khi có mã nguồn được push lên GitHub:")
    add_bullet("Job 1 (test-backend): Khởi tạo môi trường Ubuntu với JDK 21, tự động chạy bộ kiểm thử ./gradlew test và build bootJar.")
    add_bullet("Job 2 (test-frontend): Khởi tạo môi trường Node.js 22, cài đặt dependencies và kiểm tra lệnh npm run build.")
    add_bullet("Job 3 (docker-build): Xây dựng Docker images của Frontend và Backend, khởi chạy Docker Compose thử nghiệm và kiểm tra health check trước khi hoàn tất.")

    # ==================== PHẦN 6: NỘI DUNG ĐÃ PHÁT TRIỂN ====================
    add_h1("6. NỘI DUNG ĐÃ PHÁT TRIỂN SO VỚI DỰ ÁN NỀN")

    comp_table = doc.add_table(rows=6, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Tiêu chí đối chiếu", "Dự án nền ban đầu (Base)", "Phiên bản mở rộng hoàn chỉnh (Nhóm thực hiện)"]):
        cell = comp_table.cell(0, j)
        set_cell_background(cell, "1F6F4D")
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_margins(cell, 80, 80, 80, 80)

    comparisons = [
        ("Nghiệp vụ Đăng ký & Ứng tuyển", "Không có. Sinh viên chỉ có thể bình luận công khai.", "Hoàn chỉnh luồng gửi đơn, xét duyệt thành viên, cập nhật trạng thái PENDING/ACCEPTED/REJECTED."),
        ("Bảo mật thông tin liên hệ", "Lộ thông tin nếu sinh viên để lại SĐT trong bình luận.", "Thông tin liên hệ được bảo mật, chỉ chủ bài viết và ADMIN mới có quyền truy cập."),
        ("Tiện ích người dùng", "Chưa có lưu bài viết hay quản lý đơn nộp.", "Bổ sung chức năng Lưu bài viết yêu thích (Bookmarks) và bảng xem các đơn đã gửi."),
        ("Bộ lọc & Tìm kiếm bài viết", "Chỉ lọc theo danh mục cơ bản.", "Tìm kiếm theo từ khóa kết hợp lọc theo danh mục và trạng thái bài đăng (Published/Resolved)."),
        ("Kiến trúc Đóng gói DevOps", "Frontend chạy dev server, chưa container hóa toàn diện.", "Container hóa 3 tầng: Nginx Reverse Proxy (Frontend) + Temurin JRE (Backend) + MySQL 8.0.")
    ]
    for i, row in enumerate(comparisons):
        for j, val in enumerate(row):
            cell = comp_table.cell(i + 1, j)
            if i % 2 == 1:
                set_cell_background(cell, "F4F8F5")
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10)
            if j == 0:
                r.font.bold = True
            set_cell_margins(cell, 60, 60, 80, 80)

    # ==================== PHẦN 7: KẾT QUẢ KIỂM THỬ VÀ MINH CHỨNG ====================
    add_h1("7. KẾT QUẢ KIỂM THỬ, TRIỂN KHAI VÀ MINH CHỨNG THỰC TẾ")

    add_h2("7.1. Kết quả kiểm thử tự động Backend (Gradle Integration Tests)")
    add_p("Nhóm đã viết thêm bộ kiểm thử tích hợp ApplicationApiIntegrationTest.java và mở rộng PostApiIntegrationTest.java. Toàn bộ 8 ca kiểm thử bao phủ các tình huống nghiệp vụ và bảo mật:")
    add_bullet("Kiểm thử người dùng vãng lai đọc danh sách bài viết (Pass)")
    add_bullet("Kiểm thử chặn người dùng chưa xác thực tạo bài viết mới (Pass)")
    add_bullet("Kiểm thử sinh viên xác thực đăng bài thành công (Pass)")
    add_bullet("Kiểm thử sinh viên gửi đơn ứng tuyển vào bài viết thành công (Pass)")
    add_bullet("Kiểm thử ngăn chặn tự ứng tuyển vào bài viết của chính mình (Pass)")
    add_bullet("Kiểm thử chặn gửi đơn đăng ký trùng lặp (Pass - Trả về HTTP 409)")
    add_bullet("Kiểm thử phân quyền: Người lạ bị chặn xem danh sách ứng viên (Pass - Trả về HTTP 403)")
    add_bullet("Kiểm thử chủ bài viết phê duyệt chấp nhận ứng viên thành công (Pass)")
    add_bullet("Kiểm thử tính năng bật/tắt lưu bài viết yêu thích (Pass)")
    add_img_safe("docs/images/01-docker-build.png", "Hình 3: Kết quả thực thi kiểm thử Gradle Backend thành công 100%")

    add_h2("7.2. Minh chứng khởi chạy hệ thống trên Docker Compose")
    add_p("Toàn bộ 3 dịch vụ được khởi chạy ổn định với cờ healthy được ghi nhận thực tế:")
    add_img_safe("docs/images/02-docker-compose-ps.png", "Hình 4: Trạng thái các dịch vụ container hoạt động và đạt chuẩn Healthy")

    add_h2("7.3. Minh chứng Actuator Health Check")
    add_p("Endpoint http://localhost:8080/actuator/health phản hồi HTTP 200 và trạng thái UP:")
    add_img_safe("docs/images/03-actuator-health.png", "Hình 5: Phản hồi UP từ Actuator Health Check xác thực kết nối CSDL thành công")

    # ==================== PHẦN 8: HẠN CHẾ VÀ HƯỚNG PHÁT TRIỂN ====================
    add_h1("8. HẠN CHẾ HIỆN TẠI VÀ HƯỚNG PHÁT TRIỂN")

    add_h2("8.1. Hạn chế hiện tại")
    add_bullet("Thông báo trạng thái duyệt đơn hiện tại được hiển thị qua polling khi người dùng mở lại trang, chưa có hệ thống thông báo đẩy (Push Notifications / WebSocket).")
    add_bullet("Chưa tích hợp dịch vụ tải ảnh trực tiếp từ máy tính lên Cloud Storage (hiện tại bài đăng sử dụng nội dung văn bản thuần).")

    add_h2("8.2. Hướng phát triển tiếp theo")
    add_bullet("Tích hợp WebSocket / SSE (Server-Sent Events) để thông báo cho sinh viên ngay khi đơn ứng tuyển được chủ bài phê duyệt.")
    add_bullet("Triển khai hệ thống lên môi trường đám mây Kubernetes (K8s) hoặc Cloud Run với HTTPS chứng chỉ SSL tự động.")
    add_bullet("Bổ sung tính năng đánh giá độ uy tín (Reputation Score) của thành viên sau khi hoàn thành dự án/sự kiện cùng nhau.")

    output_filename = "Báo cáo Mini Project - Nguyễn Quang Anh - N24DTCn001.docx"
    doc.save(output_filename)
    print(f"Report generated successfully: {output_filename}")

if __name__ == "__main__":
    create_report()
