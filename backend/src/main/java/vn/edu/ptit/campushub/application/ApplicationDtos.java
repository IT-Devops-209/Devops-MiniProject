package vn.edu.ptit.campushub.application;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import java.time.Instant;
import vn.edu.ptit.campushub.post.PostDtos.AuthorView;

public final class ApplicationDtos {
    private ApplicationDtos() {
    }

    public record ApplyRequest(
            @NotBlank(message = "Thông tin liên hệ không được để trống")
            @Size(max = 100, message = "Thông tin liên hệ tối đa 100 ký tự")
            String contactInfo,

            @NotBlank(message = "Lời nhắn không được để trống")
            @Size(max = 500, message = "Lời nhắn tối đa 500 ký tự")
            String message,

            @Size(max = 150, message = "Kỹ năng / Vai trò tối đa 150 ký tự")
            String roleOrSkill
    ) {}

    public record UpdateStatusRequest(
            @NotNull(message = "Trạng thái không được để trống")
            ApplicationStatus status
    ) {}

    public record ApplicationView(
            Long id,
            Long postId,
            String postTitle,
            AuthorView applicant,
            String contactInfo,
            String message,
            String roleOrSkill,
            ApplicationStatus status,
            Instant createdAt,
            Instant updatedAt
    ) {
        public static ApplicationView from(PostApplication app) {
            return new ApplicationView(
                    app.getId(),
                    app.getPost().getId(),
                    app.getPost().getTitle(),
                    new AuthorView(app.getApplicant().getId(), app.getApplicant().getUsername(), app.getApplicant().getDisplayName()),
                    app.getContactInfo(),
                    app.getMessage(),
                    app.getRoleOrSkill(),
                    app.getStatus(),
                    app.getCreatedAt(),
                    app.getUpdatedAt()
            );
        }
    }
}
