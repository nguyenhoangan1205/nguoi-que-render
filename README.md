# nguoi-que-render

Máy render cho [nguoi-que-video](https://github.com/nguyenhoangan1205/nguoi-que-video) và [lam-phim-ve-tay](https://github.com/nguyenhoangan1205/lam-phim-ve-tay) (phim vẽ tay, xem mục cuối).

1. Ở `nguoi-que-video`, nhánh nào push file `phim/<ten>.json` mới hoặc đã sửa thì workflow **Gửi sang render** tự đóng gói thành phiếu `jobs/<ten>.json` và đẩy sang repo này.
2. Repo này thấy phiếu mới thì tự render (lấy engine, nhân vật, giọng nói đúng commit đã gửi).
3. Xong, video MP4 và bảng phân cảnh PNG nằm ở **Releases**, mỗi lần render một bản (`<ten>-<số>`).

Mọi phim đều được đóng logo **Sống Vui** mờ 30% ở góc trên bên phải (file logo ở [`logo/`](logo)). Phim của `nguoi-que-video` được đóng logo ở bước **ghep**; phim vẽ tay đã có logo sẵn từ app `lam-phim-ve-tay`.

## Phim 3D: render song song

Phim 3D (file phim có `"engine": "3d"`) vẽ bằng CPU nên chậm, khoảng 2,5 giây một khung. Workflow chia phim thành **8 đoạn**, mỗi đoạn render trên một máy riêng cùng lúc. Job **ghep** nối các đoạn với tiếng rồi đăng lên Releases. Cảnh 43 giây mất khoảng 10 phút thay vì gần 1 giờ.

- Đổi số máy: **Actions → Render → Run workflow**, ô "Số máy render song song" (tối đa 20 máy cùng lúc với tài khoản miễn phí).
- Phim 2D nhanh nên vẫn render trọn trên một máy.
- Phiếu gửi từ commit cũ (trước khi `nguoi-que-video` hỗ trợ chia đoạn) tự render trọn trên một máy.

## Phiếu render

```json
{
  "ten": "kinh-kha",
  "nguon": { "repo": "nguyenhoangan1205/nguoi-que-video", "nhanh": "main", "commit": "<sha>" },
  "phim": { "...": "nội dung phim/kinh-kha.json" }
}
```

## Tự gửi phim bằng tay trên GitHub

Có sẵn phiếu mẫu [`mau/demo.json`](mau/demo.json): phim demo "Một ngày đi dạo", khoảng 30 giây, có giọng nói. Phiếu lấy engine ở commit `6cc86b5`, nhánh `claude/upbeat-davinci-i8q4v1` của `nguoi-que-video`. Tải file này về máy để làm thử.

**Bước 0: kiểm tra token.** Vào **Settings → Secrets and variables → Actions** của repo này, xem đã có `RENDER_TOKEN` chưa (cách tạo ở mục "Cài đặt" bên dưới). Thiếu token thì lần chạy báo đỏ "Thiếu secret RENDER_TOKEN".

**Bước 1: tải phiếu lên.**
1. Mở thư mục [`jobs/`](jobs).
2. Bấm **Add file → Upload files**, kéo file phiếu (ví dụ `demo.json`) vào.
3. Bấm **Commit changes**.

**Bước 2: theo dõi.** Tab **Actions** sẽ có lần chạy **Render** mới. Phim ngắn mất khoảng 3–5 phút, phim 3 phút lâu hơn.

**Bước 3: lấy video.** Khi có dấu ✅, mở [Releases](../../releases). Mỗi lần render có một bản `<ten>-<số>` (ví dụ `demo-1`), trong đó:
- `<ten>.mp4`: video, bấm vào là tải về.
- `<ten>-storyboard.png`: bảng phân cảnh.

**Render lại:** tab **Actions → Render → Run workflow**, nhập `jobs/<ten>.json`.

**Sửa phim:** mở `jobs/<ten>.json` trên GitHub, bấm ✏️, sửa trong phần `"phim"` (ví dụ lời thoại ở `"say"`), rồi **Commit changes**. Phim tự render lại.

**Phim mới:** sao chép một phiếu, đổi `"ten"` (cũng là tên file và tên video) và thay nội dung `"phim"`. `"nguon"` chỉ nhánh và commit của `nguoi-que-video` có đủ nhân vật, đạo cụ và file giọng mà phim dùng.

Lần chạy báo lỗi: bấm vào lần chạy đó → job **render** → xem bước có dấu ❌.

## Phim vẽ tay (lam-phim-ve-tay)

Workflow **Render phim vẽ tay** nhận phiếu trong `jobs-ve-tay/<id>.json`:

```json
{
  "ten": "2026-10-22-thu-09",
  "nguon": { "repo": "nguyenhoangan1205/lam-phim-ve-tay", "nhanh": "main", "commit": "<sha>" },
  "du_an": "2026-10-22-thu-09",
  "chay_thu": false,
  "phu_de": true
}
```

- `du_an`: thư mục dự án trong `phim-projects/` của lam-phim-ve-tay (có `project.json`, hình và file giọng `.mp3`).
- `chay_thu: true`: chỉ render 10% đầu (`chay-thu-10.mp4`) để xem thử.
- `phu_de: false`: không in phụ đề, đăng kèm file `.srt`.

Workflow lấy app ở đúng commit, đổi giọng `.mp3` sang `.wav` (`server/chuan_bi_render.py`), chạy server render của app,
thêm hiệu ứng âm thanh nếu dự án có `them_hieu_ung.py`, rồi đăng `songvui_viet-<ten>.mp4` lên Releases (`<ten>-<số>`).

Gửi phiếu: ở lam-phim-ve-tay, commit file `phim-projects/<id>/render.json` (vd. `{"chay_thu": false, "phu_de": true}`)
rồi push, workflow **Gửi sang render** bên đó tự viết phiếu sang đây. Hoặc tự tải phiếu lên `jobs-ve-tay/` như phim người que.

## Cài đặt (một lần)

Cần một token tên `RENDER_TOKEN` đặt ở **cả ba repo** (Settings → Secrets and variables → Actions → New repository secret). Tạo token tại GitHub → Settings → Developer settings → Fine-grained tokens, chọn các repo `nguoi-que-video`, `lam-phim-ve-tay` và `nguoi-que-render`, quyền **Contents: Read and write**.
