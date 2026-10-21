# nguoi-que-render

Máy render cho [nguoi-que-video](https://github.com/nguyenhoangan1205/nguoi-que-video).

1. Ở `nguoi-que-video`, nhánh nào push file `phim/<ten>.json` mới hoặc đã sửa thì workflow **Gửi sang render** tự đóng gói thành phiếu `jobs/<ten>.json` và đẩy sang repo này.
2. Repo này thấy phiếu mới thì tự render (lấy engine, nhân vật, giọng nói đúng commit đã gửi).
3. Xong, video MP4 và bảng phân cảnh PNG nằm ở **Releases**, mỗi lần render một bản (`<ten>-<số>`).

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

## Cài đặt (một lần)

Cần một token tên `RENDER_TOKEN` đặt ở **cả hai repo** (Settings → Secrets and variables → Actions → New repository secret). Tạo token tại GitHub → Settings → Developer settings → Fine-grained tokens, chọn hai repo `nguoi-que-video` và `nguoi-que-render`, quyền **Contents: Read and write**.
