package vn.edu.ptit.campushub.application;

import java.security.Principal;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import vn.edu.ptit.campushub.application.ApplicationDtos.ApplicationView;
import vn.edu.ptit.campushub.application.ApplicationDtos.ApplyRequest;
import vn.edu.ptit.campushub.common.ApiException;
import vn.edu.ptit.campushub.post.Post;
import vn.edu.ptit.campushub.post.PostRepository;
import vn.edu.ptit.campushub.post.PostStatus;
import vn.edu.ptit.campushub.user.Role;
import vn.edu.ptit.campushub.user.User;
import vn.edu.ptit.campushub.user.UserRepository;

@Service
@Transactional(readOnly = true)
public class ApplicationService {
    private final ApplicationRepository applicationRepository;
    private final PostRepository postRepository;
    private final UserRepository userRepository;

    public ApplicationService(ApplicationRepository applicationRepository,
                              PostRepository postRepository,
                              UserRepository userRepository) {
        this.applicationRepository = applicationRepository;
        this.postRepository = postRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public ApplicationView apply(Long postId, ApplyRequest request, Principal principal) {
        User user = currentUser(principal);
        Post post = findPost(postId);

        if (post.getStatus() != PostStatus.PUBLISHED) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Bài đăng này hiện không nhận đơn đăng ký mới");
        }

        if (post.getAuthor().getId().equals(user.getId())) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Bạn không thể tự đăng ký tham gia bài đăng của chính mình");
        }

        var existing = applicationRepository.findByPostIdAndApplicantId(postId, user.getId());
        if (existing.isPresent()) {
            PostApplication app = existing.get();
            if (app.getStatus() == ApplicationStatus.CANCELLED) {
                // Allow re-applying if previously cancelled
                app.updateStatus(ApplicationStatus.PENDING);
                return ApplicationView.from(app);
            }
            throw new ApiException(HttpStatus.CONFLICT, "Bạn đã gửi đơn đăng ký cho bài viết này rồi");
        }

        PostApplication application = new PostApplication(
                post,
                user,
                request.contactInfo().trim(),
                request.message().trim(),
                request.roleOrSkill() != null ? request.roleOrSkill().trim() : null
        );

        return ApplicationView.from(applicationRepository.save(application));
    }

    public List<ApplicationView> getPostApplications(Long postId, Principal principal) {
        User user = currentUser(principal);
        Post post = findPost(postId);

        if (!post.getAuthor().getId().equals(user.getId()) && user.getRole() != Role.ADMIN) {
            throw new ApiException(HttpStatus.FORBIDDEN, "Chỉ chủ bài đăng hoặc quản trị viên mới có quyền xem danh sách người đăng ký");
        }

        return applicationRepository.findByPostIdOrderByCreatedAtDesc(postId).stream()
                .map(ApplicationView::from)
                .toList();
    }

    public ApplicationView getMyApplicationForPost(Long postId, Principal principal) {
        if (principal == null) return null;
        User user = currentUser(principal);
        return applicationRepository.findByPostIdAndApplicantId(postId, user.getId())
                .map(ApplicationView::from)
                .orElse(null);
    }

    public List<ApplicationView> getMyApplications(Principal principal) {
        User user = currentUser(principal);
        return applicationRepository.findByApplicantIdOrderByCreatedAtDesc(user.getId()).stream()
                .map(ApplicationView::from)
                .toList();
    }

    @Transactional
    public ApplicationView updateStatus(Long applicationId, ApplicationStatus status, Principal principal) {
        User user = currentUser(principal);
        PostApplication app = findApplication(applicationId);
        Post post = app.getPost();

        if (!post.getAuthor().getId().equals(user.getId()) && user.getRole() != Role.ADMIN) {
            throw new ApiException(HttpStatus.FORBIDDEN, "Bạn không có quyền duyệt đơn đăng ký này");
        }

        if (status == ApplicationStatus.CANCELLED) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Chủ bài chỉ có thể Chấp nhận hoặc Từ chối đơn");
        }

        app.updateStatus(status);
        return ApplicationView.from(app);
    }

    @Transactional
    public void cancelApplication(Long applicationId, Principal principal) {
        User user = currentUser(principal);
        PostApplication app = findApplication(applicationId);

        if (!app.getApplicant().getId().equals(user.getId()) && user.getRole() != Role.ADMIN) {
            throw new ApiException(HttpStatus.FORBIDDEN, "Bạn không có quyền hủy đơn đăng ký của người khác");
        }

        if (app.getStatus() != ApplicationStatus.PENDING) {
            throw new ApiException(HttpStatus.BAD_REQUEST, "Chỉ có thể hủy đơn khi đang ở trạng thái Chờ duyệt (PENDING)");
        }

        app.updateStatus(ApplicationStatus.CANCELLED);
    }

    private Post findPost(Long id) {
        return postRepository.findById(id)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Không tìm thấy bài đăng"));
    }

    private PostApplication findApplication(Long id) {
        return applicationRepository.findById(id)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Không tìm thấy đơn đăng ký"));
    }

    private User currentUser(Principal principal) {
        if (principal == null) {
            throw new ApiException(HttpStatus.UNAUTHORIZED, "Vui lòng đăng nhập");
        }
        return userRepository.findByUsername(principal.getName())
                .orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Không tìm thấy người dùng"));
    }
}
