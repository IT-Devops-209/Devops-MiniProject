import { useCallback, useEffect, useState } from 'react'
import { api, clearCredentials, setCredentials } from './api.js'

const emptyPost = { title: '', content: '', categoryId: '' }
const emptyApply = { contactInfo: '', message: '', roleOrSkill: '' }

function formatDate(value) {
  if (!value) return ''
  return new Intl.DateTimeFormat('vi-VN', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value))
}

function App() {
  const [user, setUser] = useState(null)
  const [categories, setCategories] = useState([])
  const [posts, setPosts] = useState([])
  const [selectedPost, setSelectedPost] = useState(null)
  const [filters, setFilters] = useState({ keyword: '', categoryId: '', status: '' })
  const [activeTab, setActiveTab] = useState('feed') // 'feed' | 'bookmarks' | 'myPosts'
  const [dialog, setDialog] = useState(null) // null | 'login' | 'post' | 'apply' | 'myApplications'
  const [notice, setNotice] = useState('')
  const [myApplications, setMyApplications] = useState([])

  const loadPosts = useCallback(async () => {
    try {
      if (activeTab === 'bookmarks') {
        const list = await api('/users/me/bookmarks')
        setPosts(list)
        return
      }
      const query = new URLSearchParams()
      if (filters.keyword) query.set('keyword', filters.keyword)
      if (filters.categoryId) query.set('categoryId', filters.categoryId)
      if (filters.status) query.set('status', filters.status)

      const page = await api(`/posts?${query}`)
      let list = page.content || []
      if (activeTab === 'myPosts' && user) {
        list = list.filter((p) => p.author.id === user.id)
      }
      setPosts(list)
    } catch (error) {
      setNotice(error.message)
    }
  }, [filters, activeTab, user])

  useEffect(() => {
    api('/categories').then(setCategories).catch((error) => setNotice(error.message))
    api('/auth/me').then(setUser).catch(() => clearCredentials())
  }, [])

  useEffect(() => {
    loadPosts()
  }, [loadPosts])

  async function openPost(id) {
    try {
      const data = await api(`/posts/${id}`)
      setSelectedPost(data)
    } catch (error) {
      setNotice(error.message)
    }
  }

  function logout() {
    clearCredentials()
    setUser(null)
    setSelectedPost(null)
    setActiveTab('feed')
    setNotice('Đã đăng xuất')
  }

  async function refreshSelected() {
    if (selectedPost) await openPost(selectedPost.id)
    await loadPosts()
  }

  async function openMyApplications() {
    try {
      const data = await api('/users/me/applications')
      setMyApplications(data)
      setDialog('myApplications')
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function toggleBookmark(postId) {
    if (!user) {
      setDialog('login')
      return
    }
    try {
      const res = await api(`/posts/${postId}/bookmark`, { method: 'POST' })
      setNotice(res.bookmarked ? 'Đã lưu bài viết' : 'Đã bỏ lưu bài viết')
      await refreshSelected()
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => { setSelectedPost(null); setActiveTab('feed') }}>
          <span className="brand-mark">C</span>
          <span className="brand-name">Campus Hub</span>
        </button>

        <nav>
          {user ? (
            <>
              <div className="nav-tabs">
                <button
                  className={`tab-btn ${activeTab === 'feed' && !selectedPost ? 'active' : ''}`}
                  onClick={() => { setSelectedPost(null); setActiveTab('feed') }}
                >
                  Trang chủ
                </button>
                <button
                  className={`tab-btn ${activeTab === 'bookmarks' ? 'active' : ''}`}
                  onClick={() => { setSelectedPost(null); setActiveTab('bookmarks') }}
                >
                  Đã lưu
                </button>
                <button
                  className={`tab-btn ${activeTab === 'myPosts' ? 'active' : ''}`}
                  onClick={() => { setSelectedPost(null); setActiveTab('myPosts') }}
                >
                  Bài của tôi
                </button>
                <button className="tab-btn highlight" onClick={openMyApplications}>
                  Đơn đã nộp
                </button>
              </div>

              <span className="user-name">Xin chào, <strong>{user.displayName}</strong></span>
              <button className="button ghost" onClick={() => setDialog('post')}>+ Đăng bài</button>
              <button className="button secondary" onClick={logout}>Đăng xuất</button>
            </>
          ) : (
            <button className="button primary" onClick={() => setDialog('login')}>Đăng nhập</button>
          )}
        </nav>
      </header>

      <main>
        {notice && <div className="notice" onClick={() => setNotice('')}>{notice} ✕</div>}

        {selectedPost ? (
          <PostDetail
            post={selectedPost}
            user={user}
            onBack={() => setSelectedPost(null)}
            onChanged={refreshSelected}
            onDeleted={() => { setSelectedPost(null); loadPosts() }}
            onToggleBookmark={() => toggleBookmark(selectedPost.id)}
            onOpenApply={() => setDialog('apply')}
            setNotice={setNotice}
          />
        ) : (
          <>
            <section className="hero">
              <div>
                <p className="eyebrow">Cổng thông tin & Giao lưu sinh viên</p>
                <h1>Không gian kết nối & trao đổi Campus Hub</h1>
                <p>
                  Đăng tin sự kiện trường lớp, tìm đồng đội làm đồ án DevOps, chia sẻ tài liệu ôn tập và đăng ký tham gia các hoạt động một cách tiện lợi.
                </p>
              </div>
              <div className="hero-stats-group">
                <div className="hero-stat">
                  <strong>{posts.length}</strong>
                  <span>bài viết</span>
                </div>
                {user && (
                  <div className="hero-stat badge-stat">
                    <strong>{user.role}</strong>
                    <span>vai trò</span>
                  </div>
                )}
              </div>
            </section>

            <section className="filters" aria-label="Tìm kiếm bài đăng">
              <input
                value={filters.keyword}
                placeholder="Tìm bài viết theo tiêu đề hoặc nội dung..."
                onChange={(event) => setFilters({ ...filters, keyword: event.target.value })}
              />
              <select
                value={filters.categoryId}
                onChange={(event) => setFilters({ ...filters, categoryId: event.target.value })}
              >
                <option value="">Tất cả chuyên mục</option>
                {categories.map((category) => (
                  <option key={category.id} value={category.id}>{category.name}</option>
                ))}
              </select>
              <select
                value={filters.status}
                onChange={(event) => setFilters({ ...filters, status: event.target.value })}
              >
                <option value="">Tất cả trạng thái</option>
                <option value="PUBLISHED">Đang mở (Published)</option>
                <option value="RESOLVED">Đã hoàn tất (Resolved)</option>
              </select>
            </section>

            <section className="post-grid">
              {posts.map((post) => (
                <PostCard
                  key={post.id}
                  post={post}
                  onOpen={openPost}
                  onToggleBookmark={(e) => { e.stopPropagation(); toggleBookmark(post.id) }}
                />
              ))}
              {!posts.length && <div className="empty">Không có bài đăng nào phù hợp với bộ lọc.</div>}
            </section>
          </>
        )}
      </main>

      <footer>Campus Hub · Mini Project Session 13 · Hệ thống Containerized Full-stack DevOps</footer>

      {dialog === 'login' && (
        <AuthDialog
          onClose={() => setDialog(null)}
          onLogin={(loggedInUser) => {
            setUser(loggedInUser)
            setDialog(null)
            setNotice('Đăng nhập thành công')
            loadPosts()
          }}
        />
      )}

      {dialog === 'post' && (
        <PostDialog
          categories={categories}
          onClose={() => setDialog(null)}
          onSaved={() => {
            setDialog(null)
            setNotice('Đã đăng bài thành công')
            loadPosts()
          }}
        />
      )}

      {dialog === 'apply' && selectedPost && (
        <ApplyDialog
          post={selectedPost}
          onClose={() => setDialog(null)}
          onApplied={() => {
            setDialog(null)
            setNotice('Đã gửi đơn đăng ký tham gia thành công!')
            refreshSelected()
          }}
        />
      )}

      {dialog === 'myApplications' && (
        <MyApplicationsDialog
          applications={myApplications}
          onClose={() => setDialog(null)}
          onCancelled={async () => {
            setNotice('Đã hủy đơn đăng ký')
            const refreshed = await api('/users/me/applications')
            setMyApplications(refreshed)
            await refreshSelected()
          }}
        />
      )}
    </div>
  )
}

function PostCard({ post, onOpen, onToggleBookmark }) {
  const isResolved = post.status === 'RESOLVED'
  return (
    <article className={`post-card ${isResolved ? 'resolved-card' : ''}`} onClick={() => onOpen(post.id)}>
      <div className="card-top">
        <span className="tag">{post.category.name}</span>
        <div className="card-top-right">
          {isResolved && <span className="status-badge resolved">Đã hoàn tất</span>}
          <button
            className={`bookmark-btn ${post.bookmarkedByCurrentUser ? 'active' : ''}`}
            title={post.bookmarkedByCurrentUser ? 'Bỏ lưu' : 'Lưu bài'}
            onClick={onToggleBookmark}
          >
            {post.bookmarkedByCurrentUser ? '★' : '☆'}
          </button>
        </div>
      </div>
      <h2>{post.title}</h2>
      <p>{post.content}</p>
      <div className="card-footer">
        <span className="author-name">👤 {post.author.displayName}</span>
        <div className="meta-stats">
          <span title="Lượt quan tâm">♥ {post.reactionCount}</span>
          <span title="Bình luận">💬 {post.commentCount}</span>
          {post.applicationCount > 0 && (
            <span className="app-badge" title="Số người đăng ký tham gia">👥 {post.applicationCount}</span>
          )}
        </div>
      </div>
    </article>
  )
}

function PostDetail({ post, user, onBack, onChanged, onDeleted, onToggleBookmark, onOpenApply, setNotice }) {
  const [comment, setComment] = useState('')
  const [applicants, setApplicants] = useState([])
  const [loadingApplicants, setLoadingApplicants] = useState(false)
  const canManage = user && (user.id === post.author.id || user.role === 'ADMIN')
  const isAuthor = user && user.id === post.author.id

  // Load applicants if user can manage this post
  const loadApplicants = useCallback(async () => {
    if (!canManage) return
    setLoadingApplicants(true)
    try {
      const data = await api(`/posts/${post.id}/applications`)
      setApplicants(data)
    } catch {
      // Forbidden or not author
    } finally {
      setLoadingApplicants(false)
    }
  }, [canManage, post.id])

  useEffect(() => {
    loadApplicants()
  }, [loadApplicants])

  async function act(action, success) {
    try {
      await action()
      setNotice(success)
      await onChanged()
      await loadApplicants()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function updateAppStatus(appId, status) {
    try {
      await api(`/applications/${appId}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status }),
      })
      setNotice(status === 'ACCEPTED' ? 'Đã duyệt chấp nhận ứng viên' : 'Đã từ chối ứng viên')
      await loadApplicants()
      await onChanged()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function cancelMyApp(appId) {
    if (!window.confirm('Bạn có chắc muốn hủy đơn đăng ký này?')) return
    try {
      await api(`/applications/${appId}`, { method: 'DELETE' })
      setNotice('Đã hủy đơn đăng ký thành công')
      await onChanged()
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <section className="detail">
      <div className="detail-header-actions">
        <button className="back" onClick={onBack}>← Quay lại danh sách</button>
        <button
          className={`button ${post.bookmarkedByCurrentUser ? 'primary' : 'secondary'} bookmark-action`}
          onClick={onToggleBookmark}
        >
          {post.bookmarkedByCurrentUser ? '★ Đã lưu vào mục yêu thích' : '☆ Lưu bài viết'}
        </button>
      </div>

      <div className="detail-card">
        <div className="card-top">
          <div className="tag-group">
            <span className="tag">{post.category.name}</span>
            <span className={`status-badge ${post.status === 'RESOLVED' ? 'resolved' : 'published'}`}>
              {post.status === 'RESOLVED' ? 'Đã hoàn tất' : 'Đang mở'}
            </span>
          </div>
          <span className="date-text">{formatDate(post.createdAt)}</span>
        </div>

        <h1>{post.title}</h1>
        <p className="author">Đăng bởi <strong>{post.author.displayName}</strong> (@{post.author.username})</p>
        <div className="content">{post.content}</div>

        <div className="actions">
          <button
            className={`button ${post.reactedByCurrentUser ? 'primary' : 'secondary'}`}
            disabled={!user}
            onClick={() => act(() => api(`/posts/${post.id}/reaction`, { method: 'POST' }), 'Đã cập nhật quan tâm')}
          >
            ♥ {post.reactionCount} quan tâm
          </button>

          {canManage && post.status !== 'RESOLVED' && (
            <button
              className="button secondary"
              onClick={() => act(() => api(`/posts/${post.id}/status`, {
                method: 'PATCH', body: JSON.stringify({ status: 'RESOLVED' }),
              }), 'Đã đánh dấu hoàn tất')}
            >
              ✓ Đánh dấu hoàn tất
            </button>
          )}

          {user?.role === 'ADMIN' && post.status !== 'HIDDEN' && (
            <button
              className="button secondary"
              onClick={() => act(() => api(`/posts/${post.id}/status`, {
                method: 'PATCH', body: JSON.stringify({ status: 'HIDDEN' }),
              }), 'Đã ẩn bài đăng')}
            >
              Ẩn bài
            </button>
          )}

          {canManage && (
            <button
              className="button danger"
              onClick={async () => {
                if (!window.confirm('Bạn có chắc muốn xóa bài đăng này?')) return
                try {
                  await api(`/posts/${post.id}`, { method: 'DELETE' })
                  setNotice('Đã xóa bài đăng')
                  onDeleted()
                } catch (error) {
                  setNotice(error.message)
                }
              }}
            >
              Xóa bài
            </button>
          )}
        </div>
      </div>

      {/* --- COLLABORATION & REGISTRATION SECTION --- */}
      <div className="collaboration-box">
        <div className="collaboration-header">
          <h3>👥 Đăng ký tham gia & Ứng tuyển nhóm ({post.applicationCount})</h3>
          <p className="collaboration-desc">
            Dành cho sinh viên muốn tham gia sự kiện, ghép nhóm nghiên cứu / đồ án hoặc nhận đồ trao đổi.
          </p>
        </div>

        {!user ? (
          <div className="collab-guest">
            <p>Vui lòng đăng nhập để đăng ký tham gia hoặc ứng tuyển vào nhóm này.</p>
          </div>
        ) : isAuthor ? (
          <div className="applicant-management">
            <p className="author-tip">Bạn là chủ bài viết. Dưới đây là danh sách ứng viên đã nộp đơn đăng ký:</p>
            {loadingApplicants ? (
              <p>Đang tải danh sách ứng viên...</p>
            ) : applicants.length === 0 ? (
              <div className="empty-sub">Chưa có ứng viên nào đăng ký.</div>
            ) : (
              <div className="applicant-list">
                {applicants.map((app) => (
                  <div key={app.id} className={`applicant-card status-${app.status.toLowerCase()}`}>
                    <div className="app-main">
                      <div className="app-header-row">
                        <strong>{app.applicant.displayName}</strong>
                        <span className="app-username">(@{app.applicant.username})</span>
                        <span className={`status-pill ${app.status.toLowerCase()}`}>{app.status}</span>
                        <span className="app-time">{formatDate(app.createdAt)}</span>
                      </div>
                      <div className="app-detail-row">
                        <span>📞 <strong>Liên hệ:</strong> {app.contactInfo}</span>
                        {app.roleOrSkill && <span>🎯 <strong>Kỹ năng/Vị trí:</strong> {app.roleOrSkill}</span>}
                      </div>
                      <p className="app-message">💬 "{app.message}"</p>
                    </div>

                    {app.status === 'PENDING' && (
                      <div className="app-actions">
                        <button
                          className="button primary small"
                          onClick={() => updateAppStatus(app.id, 'ACCEPTED')}
                        >
                          Chấp nhận
                        </button>
                        <button
                          className="button danger small"
                          onClick={() => updateAppStatus(app.id, 'REJECTED')}
                        >
                          Từ chối
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : (
          <div className="applicant-user-zone">
            {post.myApplication ? (
              <div className={`my-application-status status-${post.myApplication.status.toLowerCase()}`}>
                <div className="my-app-info">
                  <strong>Trạng thái đơn của bạn:</strong>
                  <span className={`status-pill ${post.myApplication.status.toLowerCase()}`}>
                    {post.myApplication.status === 'PENDING' && '⏳ Chờ duyệt'}
                    {post.myApplication.status === 'ACCEPTED' && '✓ Đã được chấp nhận'}
                    {post.myApplication.status === 'REJECTED' && '✕ Đã bị từ chối'}
                    {post.myApplication.status === 'CANCELLED' && 'Đã hủy'}
                  </span>
                  <p className="my-app-text">Lời nhắn của bạn: "{post.myApplication.message}"</p>
                </div>
                {post.myApplication.status === 'PENDING' && (
                  <button className="button danger small" onClick={() => cancelMyApp(post.myApplication.id)}>
                    Hủy đơn
                  </button>
                )}
              </div>
            ) : post.status === 'RESOLVED' ? (
              <div className="collab-closed">
                <p>Bài đăng này đã được đánh dấu hoàn tất. Hiện không nhận thêm đơn đăng ký.</p>
              </div>
            ) : (
              <div className="collab-action-row">
                <p>Bạn quan tâm đến sự kiện hoặc nhóm này? Hãy gửi đơn đăng ký tham gia ngay!</p>
                <button className="button primary" onClick={onOpenApply}>
                  ✍ Gửi đơn đăng ký tham gia
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* --- COMMENTS SECTION --- */}
      <div className="comments">
        <h2>Bình luận & Thảo luận ({post.commentCount})</h2>
        {user ? (
          <form
            onSubmit={(event) => {
              event.preventDefault()
              act(
                () => api(`/posts/${post.id}/comments`, { method: 'POST', body: JSON.stringify({ content: comment }) }),
                'Đã thêm bình luận'
              ).then(() => setComment(''))
            }}
          >
            <textarea
              value={comment}
              onChange={(event) => setComment(event.target.value)}
              placeholder="Chia sẻ ý kiến hoặc đặt câu hỏi cho tác giả..."
              required
              maxLength="1000"
            />
            <button className="button primary">Gửi bình luận</button>
          </form>
        ) : (
          <p className="muted">Vui lòng đăng nhập để bình luận hoặc bày tỏ quan tâm.</p>
        )}
        <div className="comment-list">
          {post.comments.map((item) => (
            <div className="comment" key={item.id}>
              <strong>{item.author.displayName}</strong>
              <span>{formatDate(item.createdAt)}</span>
              <p>{item.content}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

function AuthDialog({ onClose, onLogin }) {
  const [mode, setMode] = useState('login')
  const [form, setForm] = useState({ username: '', displayName: '', password: '' })
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    try {
      if (mode === 'register') {
        await api('/auth/register', { method: 'POST', body: JSON.stringify(form) })
      }
      setCredentials(form.username, form.password)
      onLogin(await api('/auth/me'))
    } catch (requestError) {
      clearCredentials()
      setError(requestError.message)
    }
  }

  return (
    <Dialog title={mode === 'login' ? 'Đăng nhập Campus Hub' : 'Tạo tài khoản mới'} onClose={onClose}>
      <form className="form" onSubmit={submit}>
        {error && <p className="form-error">{error}</p>}
        <label>
          Tên đăng nhập
          <input
            required
            minLength="3"
            value={form.username}
            onChange={(event) => setForm({ ...form, username: event.target.value })}
          />
        </label>
        {mode === 'register' && (
          <label>
            Tên hiển thị
            <input
              required
              value={form.displayName}
              onChange={(event) => setForm({ ...form, displayName: event.target.value })}
            />
          </label>
        )}
        <label>
          Mật khẩu
          <input
            required
            minLength="6"
            type="password"
            value={form.password}
            onChange={(event) => setForm({ ...form, password: event.target.value })}
          />
        </label>
        <button className="button primary">{mode === 'login' ? 'Đăng nhập' : 'Đăng ký tài khoản'}</button>
        <button
          type="button"
          className="text-button"
          onClick={() => { setMode(mode === 'login' ? 'register' : 'login'); setError('') }}
        >
          {mode === 'login' ? 'Chưa có tài khoản? Đăng ký ngay' : 'Đã có tài khoản? Quay lại đăng nhập'}
        </button>
      </form>
    </Dialog>
  )
}

function PostDialog({ categories, onClose, onSaved }) {
  const [form, setForm] = useState(emptyPost)
  const [error, setError] = useState('')

  async function submit(event) {
    event.preventDefault()
    try {
      await api('/posts', { method: 'POST', body: JSON.stringify({ ...form, categoryId: Number(form.categoryId) }) })
      onSaved()
    } catch (requestError) {
      setError(requestError.message)
    }
  }

  return (
    <Dialog title="Đăng bài mới" onClose={onClose}>
      <form className="form" onSubmit={submit}>
        {error && <p className="form-error">{error}</p>}
        <label>
          Tiêu đề bài viết
          <input
            required
            maxLength="160"
            placeholder="Ví dụ: Cần tìm 2 bạn làm đồ án DevOps..."
            value={form.title}
            onChange={(event) => setForm({ ...form, title: event.target.value })}
          />
        </label>
        <label>
          Chuyên mục
          <select
            required
            value={form.categoryId}
            onChange={(event) => setForm({ ...form, categoryId: event.target.value })}
          >
            <option value="">-- Chọn chuyên mục --</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
        </label>
        <label>
          Nội dung chi tiết
          <textarea
            required
            maxLength="10000"
            rows="7"
            placeholder="Mô tả cụ thể mục đích, yêu cầu kỹ năng hoặc thông tin liên quan..."
            value={form.content}
            onChange={(event) => setForm({ ...form, content: event.target.value })}
          />
        </label>
        <button className="button primary">Đăng bài</button>
      </form>
    </Dialog>
  )
}

function ApplyDialog({ post, onClose, onApplied }) {
  const [form, setForm] = useState(emptyApply)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function submit(event) {
    event.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      await api(`/posts/${post.id}/applications`, {
        method: 'POST',
        body: JSON.stringify(form),
      })
      onApplied()
    } catch (requestError) {
      setError(requestError.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog title={`Đăng ký tham gia: "${post.title}"`} onClose={onClose}>
      <form className="form" onSubmit={submit}>
        {error && <p className="form-error">{error}</p>}
        <label>
          Thông tin liên hệ (SĐT / Zalo / Telegram) *
          <input
            required
            maxLength="100"
            placeholder="Ví dụ: 0987654321 hoặc t.me/username"
            value={form.contactInfo}
            onChange={(event) => setForm({ ...form, contactInfo: event.target.value })}
          />
        </label>
        <label>
          Kỹ năng / Vai trò mong muốn đảm nhận
          <input
            maxLength="150"
            placeholder="Ví dụ: Docker & CI/CD, Frontend React, Hậu cần sự kiện..."
            value={form.roleOrSkill}
            onChange={(event) => setForm({ ...form, roleOrSkill: event.target.value })}
          />
        </label>
        <label>
          Lời nhắn gửi tác giả *
          <textarea
            required
            maxLength="500"
            rows="4"
            placeholder="Giới thiệu bản thân và lý do bạn muốn tham gia..."
            value={form.message}
            onChange={(event) => setForm({ ...form, message: event.target.value })}
          />
        </label>
        <button className="button primary" disabled={submitting}>
          {submitting ? 'Đang gửi đơn...' : 'Gửi đơn đăng ký'}
        </button>
      </form>
    </Dialog>
  )
}

function MyApplicationsDialog({ applications, onClose, onCancelled }) {
  return (
    <Dialog title="Đơn đăng ký tham gia của tôi" onClose={onClose}>
      {applications.length === 0 ? (
        <div className="empty-sub">Bạn chưa nộp đơn đăng ký cho bài viết nào.</div>
      ) : (
        <div className="my-app-list">
          {applications.map((app) => (
            <div key={app.id} className="my-app-card">
              <div className="my-app-card-header">
                <strong>{app.postTitle}</strong>
                <span className={`status-pill ${app.status.toLowerCase()}`}>{app.status}</span>
              </div>
              <p className="app-message">💬 "{app.message}"</p>
              <div className="my-app-meta">
                <span>📞 {app.contactInfo}</span>
                {app.roleOrSkill && <span>🎯 {app.roleOrSkill}</span>}
                <span>📅 {formatDate(app.createdAt)}</span>
              </div>
              {app.status === 'PENDING' && (
                <button
                  className="button danger small"
                  style={{ marginTop: 8 }}
                  onClick={async () => {
                    if (!window.confirm('Hủy đơn đăng ký này?')) return
                    try {
                      await api(`/applications/${app.id}`, { method: 'DELETE' })
                      onCancelled()
                    } catch (err) {
                      alert(err.message)
                    }
                  }}
                >
                  Hủy đơn
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </Dialog>
  )
}

function Dialog({ title, onClose, children }) {
  return (
    <div className="dialog-backdrop" onMouseDown={onClose}>
      <section className="dialog" role="dialog" aria-modal="true" onMouseDown={(event) => event.stopPropagation()}>
        <div className="dialog-title">
          <h2>{title}</h2>
          <button onClick={onClose} aria-label="Đóng">✕</button>
        </div>
        {children}
      </section>
    </div>
  )
}

export default App
