package vn.edu.ptit.campushub.application;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import jakarta.persistence.UniqueConstraint;
import java.time.Instant;
import vn.edu.ptit.campushub.post.Post;
import vn.edu.ptit.campushub.user.User;

@Entity
@Table(name = "post_applications", uniqueConstraints = {
        @UniqueConstraint(name = "uk_post_applicant", columnNames = {"post_id", "applicant_id"})
})
public class PostApplication {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "post_id")
    private Post post;

    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "applicant_id")
    private User applicant;

    @Column(nullable = false, length = 100)
    private String contactInfo;

    @Column(nullable = false, length = 500)
    private String message;

    @Column(length = 150)
    private String roleOrSkill;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 20)
    private ApplicationStatus status = ApplicationStatus.PENDING;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @Column(nullable = false)
    private Instant updatedAt;

    protected PostApplication() {
    }

    public PostApplication(Post post, User applicant, String contactInfo, String message, String roleOrSkill) {
        this.post = post;
        this.applicant = applicant;
        this.contactInfo = contactInfo;
        this.message = message;
        this.roleOrSkill = roleOrSkill;
        this.status = ApplicationStatus.PENDING;
        this.createdAt = Instant.now();
        this.updatedAt = this.createdAt;
    }

    public void updateStatus(ApplicationStatus newStatus) {
        this.status = newStatus;
        this.updatedAt = Instant.now();
    }

    public Long getId() { return id; }
    public Post getPost() { return post; }
    public User getApplicant() { return applicant; }
    public String getContactInfo() { return contactInfo; }
    public String getMessage() { return message; }
    public String getRoleOrSkill() { return roleOrSkill; }
    public ApplicationStatus getStatus() { return status; }
    public Instant getCreatedAt() { return createdAt; }
    public Instant getUpdatedAt() { return updatedAt; }
}
