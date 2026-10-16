package vn.edu.ptit.campushub;

import static org.hamcrest.Matchers.equalTo;
import static org.hamcrest.Matchers.greaterThanOrEqualTo;
import static org.hamcrest.Matchers.hasSize;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.httpBasic;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.patch;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest
@AutoConfigureMockMvc
class ApplicationApiIntegrationTest {
    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Test
    void userCanApplyToPostAndAuthorCanAccept() throws Exception {
        // 1. minhchau creates a new team post
        MvcResult postResult = mockMvc.perform(post("/api/posts")
                        .with(httpBasic("minhchau", "chau123"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"title":"Tìm bạn ghép nhóm Hackathon DevOps","content":"Cần 1 bạn chuyên Docker.","categoryId":6}
                                """))
                .andExpect(status().isCreated())
                .andReturn();

        JsonNode postJson = objectMapper.readTree(postResult.getResponse().getContentAsString());
        long createdPostId = postJson.get("id").asLong();

        // 2. student applies to minhchau's post
        MvcResult applyResult = mockMvc.perform(post("/api/posts/" + createdPostId + "/applications")
                        .with(httpBasic("student", "student123"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "contactInfo": "0912345678 - Telegram: @studentptit",
                                  "message": "Mình thành thạo Docker và CI/CD, muốn tham gia nhóm!",
                                  "roleOrSkill": "DevOps Engineer"
                                }
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.status").value("PENDING"))
                .andExpect(jsonPath("$.applicant.username").value("student"))
                .andReturn();

        JsonNode applyJson = objectMapper.readTree(applyResult.getResponse().getContentAsString());
        long applicationId = applyJson.get("id").asLong();

        // 3. student cannot apply a second time (duplicate application)
        mockMvc.perform(post("/api/posts/" + createdPostId + "/applications")
                        .with(httpBasic("student", "student123"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {
                                  "contactInfo": "0912345678",
                                  "message": "Gửi lại đơn",
                                  "roleOrSkill": "DevOps"
                                }
                                """))
                .andExpect(status().isConflict());

        // 4. another user cannot view applicants (only author or admin)
        mockMvc.perform(get("/api/posts/" + createdPostId + "/applications")
                        .with(httpBasic("student", "student123")))
                .andExpect(status().isForbidden());

        // 5. author (minhchau) can view applicants
        mockMvc.perform(get("/api/posts/" + createdPostId + "/applications")
                        .with(httpBasic("minhchau", "chau123")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(1))));

        // 6. author accepts application
        mockMvc.perform(patch("/api/applications/" + applicationId + "/status")
                        .with(httpBasic("minhchau", "chau123"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"status": "ACCEPTED"}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("ACCEPTED"));

        // 7. student checks their application list
        mockMvc.perform(get("/api/users/me/applications")
                        .with(httpBasic("student", "student123")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].status").value("ACCEPTED"));
    }

    @Test
    void cannotApplyToOwnPost() throws Exception {
        // student attempts to apply to their own post (post 2 from seeder)
        mockMvc.perform(post("/api/posts/2/applications")
                        .with(httpBasic("student", "student123"))
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"contactInfo":"091234","message":"Tu dang ky bai minh","roleOrSkill":"Member"}
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.message").value(equalTo("Bạn không thể tự đăng ký tham gia bài đăng của chính mình")));
    }

    @Test
    void userCanToggleBookmark() throws Exception {
        mockMvc.perform(post("/api/posts/1/bookmark")
                        .with(httpBasic("student", "student123")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.bookmarked").value(true));

        mockMvc.perform(get("/api/users/me/bookmarks")
                        .with(httpBasic("student", "student123")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$", hasSize(greaterThanOrEqualTo(1))));

        // Toggle again to remove
        mockMvc.perform(post("/api/posts/1/bookmark")
                        .with(httpBasic("student", "student123")))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.bookmarked").value(false));
    }
}
