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

Render lại: tab **Actions** → **Render** → **Run workflow**, nhập `jobs/<ten>.json`.

## Cài đặt (một lần)

Cần một token tên `RENDER_TOKEN` đặt ở **cả hai repo** (Settings → Secrets and variables → Actions → New repository secret). Tạo token tại GitHub → Settings → Developer settings → Fine-grained tokens, chọn hai repo `nguoi-que-video` và `nguoi-que-render`, quyền **Contents: Read and write**.
