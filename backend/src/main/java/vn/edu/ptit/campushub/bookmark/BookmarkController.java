package vn.edu.ptit.campushub.bookmark;

import java.security.Principal;
import java.util.List;
import java.util.Map;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import vn.edu.ptit.campushub.post.PostDtos.PostView;

@RestController
@RequestMapping("/api")
public class BookmarkController {
    private final BookmarkService bookmarkService;

    public BookmarkController(BookmarkService bookmarkService) {
        this.bookmarkService = bookmarkService;
    }

    @PostMapping("/posts/{postId}/bookmark")
    public Map<String, Boolean> toggleBookmark(@PathVariable Long postId, Principal principal) {
        boolean bookmarked = bookmarkService.toggleBookmark(postId, principal);
        return Map.of("bookmarked", bookmarked);
    }

    @GetMapping("/users/me/bookmarks")
    public List<PostView> getMyBookmarks(Principal principal) {
        return bookmarkService.getMyBookmarks(principal);
    }
}
