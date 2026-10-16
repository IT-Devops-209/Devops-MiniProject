package vn.edu.ptit.campushub.bookmark;

import java.security.Principal;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import vn.edu.ptit.campushub.common.ApiException;
import vn.edu.ptit.campushub.post.Post;
import vn.edu.ptit.campushub.post.PostDtos.PostView;
import vn.edu.ptit.campushub.post.PostRepository;
import vn.edu.ptit.campushub.post.PostService;
import vn.edu.ptit.campushub.user.User;
import vn.edu.ptit.campushub.user.UserRepository;

@Service
@Transactional(readOnly = true)
public class BookmarkService {
    private final BookmarkRepository bookmarkRepository;
    private final PostRepository postRepository;
    private final UserRepository userRepository;
    private final PostService postService;

    public BookmarkService(BookmarkRepository bookmarkRepository,
                           PostRepository postRepository,
                           UserRepository userRepository,
                           PostService postService) {
        this.bookmarkRepository = bookmarkRepository;
        this.postRepository = postRepository;
        this.userRepository = userRepository;
        this.postService = postService;
    }

    @Transactional
    public boolean toggleBookmark(Long postId, Principal principal) {
        User user = currentUser(principal);
        Post post = postRepository.findById(postId)
                .orElseThrow(() -> new ApiException(HttpStatus.NOT_FOUND, "Không tìm thấy bài đăng"));

        return bookmarkRepository.findByPostIdAndUserId(postId, user.getId())
                .map(bm -> {
                    bookmarkRepository.delete(bm);
                    return false;
                })
                .orElseGet(() -> {
                    bookmarkRepository.save(new Bookmark(post, user));
                    return true;
                });
    }

    public List<PostView> getMyBookmarks(Principal principal) {
        User user = currentUser(principal);
        List<Bookmark> list = bookmarkRepository.findByUserIdOrderByCreatedAtDesc(user.getId());
        return list.stream()
                .map(bm -> postService.findOne(bm.getPost().getId(), principal))
                .toList();
    }

    private User currentUser(Principal principal) {
        if (principal == null) {
            throw new ApiException(HttpStatus.UNAUTHORIZED, "Vui lòng đăng nhập");
        }
        return userRepository.findByUsername(principal.getName())
                .orElseThrow(() -> new ApiException(HttpStatus.UNAUTHORIZED, "Không tìm thấy người dùng"));
    }
}
