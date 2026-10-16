package vn.edu.ptit.campushub.application;

import jakarta.validation.Valid;
import java.security.Principal;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import vn.edu.ptit.campushub.application.ApplicationDtos.ApplicationView;
import vn.edu.ptit.campushub.application.ApplicationDtos.ApplyRequest;
import vn.edu.ptit.campushub.application.ApplicationDtos.UpdateStatusRequest;

@RestController
@RequestMapping("/api")
public class ApplicationController {
    private final ApplicationService applicationService;

    public ApplicationController(ApplicationService applicationService) {
        this.applicationService = applicationService;
    }

    @PostMapping("/posts/{postId}/applications")
    @ResponseStatus(HttpStatus.CREATED)
    public ApplicationView apply(@PathVariable Long postId,
                                 @Valid @RequestBody ApplyRequest request,
                                 Principal principal) {
        return applicationService.apply(postId, request, principal);
    }

    @GetMapping("/posts/{postId}/applications")
    public List<ApplicationView> getPostApplications(@PathVariable Long postId, Principal principal) {
        return applicationService.getPostApplications(postId, principal);
    }

    @GetMapping("/posts/{postId}/applications/my")
    public ApplicationView getMyApplicationForPost(@PathVariable Long postId, Principal principal) {
        return applicationService.getMyApplicationForPost(postId, principal);
    }

    @GetMapping("/users/me/applications")
    public List<ApplicationView> getMyApplications(Principal principal) {
        return applicationService.getMyApplications(principal);
    }

    @PatchMapping("/applications/{id}/status")
    public ApplicationView updateStatus(@PathVariable Long id,
                                        @Valid @RequestBody UpdateStatusRequest request,
                                        Principal principal) {
        return applicationService.updateStatus(id, request.status(), principal);
    }

    @DeleteMapping("/applications/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void cancelApplication(@PathVariable Long id, Principal principal) {
        applicationService.cancelApplication(id, principal);
    }
}
