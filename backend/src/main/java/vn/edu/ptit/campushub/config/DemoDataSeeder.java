package vn.edu.ptit.campushub.config;

import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;
import vn.edu.ptit.campushub.application.ApplicationRepository;
import vn.edu.ptit.campushub.application.PostApplication;
import vn.edu.ptit.campushub.category.Category;
import vn.edu.ptit.campushub.category.CategoryRepository;
import vn.edu.ptit.campushub.post.Post;
import vn.edu.ptit.campushub.post.PostRepository;
import vn.edu.ptit.campushub.user.Role;
import vn.edu.ptit.campushub.user.User;
import vn.edu.ptit.campushub.user.UserRepository;

@Component
public class DemoDataSeeder implements ApplicationRunner {
    private final UserRepository users;
    private final CategoryRepository categories;
    private final PostRepository posts;
    private final ApplicationRepository applications;
    private final PasswordEncoder passwordEncoder;

    public DemoDataSeeder(UserRepository users,
                          CategoryRepository categories,
                          PostRepository posts,
                          ApplicationRepository applications,
                          PasswordEncoder passwordEncoder) {
        this.users = users;
        this.categories = categories;
        this.posts = posts;
        this.applications = applications;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    @Transactional
    public void run(ApplicationArguments args) {
        Category events = createCategoryIfMissing("Sự kiện", "su-kien");
        Category lost = createCategoryIfMissing("Đồ thất lạc", "do-that-lac");
        Category study = createCategoryIfMissing("Hỏi đáp học tập", "hoi-dap");
        Category trade = createCategoryIfMissing("Trao đổi đồ dùng", "trao-doi");
        Category feedback = createCategoryIfMissing("Phản ánh", "phan-anh");
        Category team = createCategoryIfMissing("Tìm nhóm", "tim-nhom");

        User admin = createUserIfMissing("admin", "Quản trị viên", "admin123", Role.ADMIN);
        User student = createUserIfMissing("student", "Nguyễn Quang Anh", "student123", Role.USER);
        User student2 = createUserIfMissing("minhchau", "Trần Minh Châu", "chau123", Role.USER);

        if (posts.count() == 0) {
            Post p1 = posts.save(new Post("Ngày hội câu lạc bộ sinh viên",
                    "Các câu lạc bộ sẽ gặp gỡ sinh viên mới tại sân A2 vào chiều thứ Sáu.", events, admin));
            Post p2 = posts.save(new Post("Tìm ví màu đen gần thư viện",
                    "Mình làm rơi một chiếc ví màu đen vào sáng nay. Bạn nào nhặt được vui lòng bình luận giúp mình.",
                    lost, student));
            Post p3 = posts.save(new Post("Tìm 2 bạn cùng làm đồ án DevOps CI/CD và Docker",
                    "Nhóm đang cần thêm 2 bạn có định hướng làm DevOps, thực hành Spring Boot + React + Docker Compose. Liên hệ hoặc bấm Đăng ký bên dưới nhé!",
                    team, admin));

            if (applications.count() == 0) {
                applications.save(new PostApplication(
                        p3,
                        student,
                        "0987654321 / zalo.me/quanganh",
                        "Em có kinh nghiệm viết Dockerfile và cấu hình GitHub Actions, muốn tham gia nhóm cùng các bạn!",
                        "DevOps / Backend"
                ));
            }
        }
    }

    private Category createCategoryIfMissing(String name, String slug) {
        return categories.findBySlug(slug)
                .orElseGet(() -> categories.save(new Category(name, slug)));
    }

    private User createUserIfMissing(String username, String displayName, String password, Role role) {
        return users.findByUsername(username)
                .orElseGet(() -> users.save(new User(username, displayName,
                        passwordEncoder.encode(password), role)));
    }
}
