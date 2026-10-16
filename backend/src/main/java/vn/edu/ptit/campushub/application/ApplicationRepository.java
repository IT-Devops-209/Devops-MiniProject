package vn.edu.ptit.campushub.application;

import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ApplicationRepository extends JpaRepository<PostApplication, Long> {
    Optional<PostApplication> findByPostIdAndApplicantId(Long postId, Long applicantId);
    List<PostApplication> findByPostIdOrderByCreatedAtDesc(Long postId);
    List<PostApplication> findByApplicantIdOrderByCreatedAtDesc(Long applicantId);
    long countByPostId(Long postId);
    long countByPostIdAndStatus(Long postId, ApplicationStatus status);
    void deleteByPostId(Long postId);
}
