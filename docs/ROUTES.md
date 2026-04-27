# 路由設計文件 (ROUTES)

本文件依據 PRD、架構設計與資料庫設計，規劃個人記帳系統的 Flask 路由與對應的頁面模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| 首頁與歷史清單 | GET | `/` | `templates/index.html` | 顯示總餘額、歷史記錄列表及新增表單。支援 `?category=` 查詢參數進行篩選。 |
| 新增紀錄 | POST | `/add` | — | 接收並驗證新增表單資料，寫入 DB 後重導向至 `/`。 |
| 編輯紀錄頁面 | GET | `/edit/<int:record_id>` | `templates/edit.html` | 顯示單筆紀錄的編輯表單 (Nice to Have 功能)。 |
| 更新紀錄 | POST | `/update/<int:record_id>`| — | 接收編輯表單資料，更新 DB 中該筆記錄後重導向至 `/`。 |
| 刪除紀錄 | POST | `/delete/<int:record_id>`| — | 刪除單一帳目，完成後重導向回首頁 `/`。 |

## 2. 每個路由的詳細說明

### 首頁與歷史清單
- **HTTP 方法**：`GET`
- **URL**：`/`
- **輸入**：URL 參數 `category` (可選)
- **處理邏輯**：
  1. 呼叫 `Transaction.get_total_balance()` 獲得目前帳戶總餘額。
  2. 若有 `category` 篩選參數，則呼叫 `Transaction.get_all(category_filter=category)`；否則呼叫 `Transaction.get_all()` 獲取清單。
- **輸出**：將餘額資訊與清單回傳並渲染 `index.html`。
- **錯誤處理**：無異常時不處理，無資料則回傳空陣列（前端顯示空狀態提示）。

### 新增紀錄
- **HTTP 方法**：`POST`
- **URL**：`/add`
- **輸入**：HTML form data (`amount`, `type`, `category`, `note`)
- **處理邏輯**：驗證 `amount` 是否為正數、`type` 是否正確、`category` 是否為空。若驗證通過，呼叫 `Transaction.create(...)`。
- **輸出**：透過 302 Redirect 重新導向回 `/`。
- **錯誤處理**：若資料格式不對，使用 `flash()` 功能顯示錯誤訊息並重新導向回首頁。

### 編輯紀錄頁面
- **HTTP 方法**：`GET`
- **URL**：`/edit/<int:record_id>`
- **輸入**：路徑中的 `record_id` (整數)
- **處理邏輯**：呼叫 `Transaction.get_by_id(record_id)`。
- **輸出**：將獲取到的該筆紀錄字典傳送給 `edit.html` 並渲染。
- **錯誤處理**：若查無該紀錄，產生 `flash()` 錯誤訊息並重新導向回 `/` 首頁。

### 更新紀錄
- **HTTP 方法**：`POST`
- **URL**：`/update/<int:record_id>`
- **輸入**：路徑 `record_id`，以及表單資料 (`amount`, `type`, `category`, `note`)
- **處理邏輯**：驗證資料後呼叫 `Transaction.update(...)`。
- **輸出**：重新導向回 `/`。
- **錯誤處理**：若欄位不齊全，發出錯誤訊息並回原編輯頁面或首頁。

### 刪除紀錄
- **HTTP 方法**：`POST` (依 REST 慣例，HTML 無法直接傳 DELETE，以 POST 取代)
- **URL**：`/delete/<int:record_id>`
- **輸入**：路徑 `record_id`
- **處理邏輯**：呼叫 `Transaction.delete(record_id)`。
- **輸出**：重新導向回 `/`。
- **錯誤處理**：如果該記錄不存在，忽略錯誤並重導回首頁。

## 3. Jinja2 模板清單

| 模板路徑 | 繼承 | 用途 |
| :--- | :--- | :--- |
| `templates/base.html` | — | **通用骨架**：包含 HTML Head（引用的 CSS/JS）、全域 Navbar（如果有的話）、Flash 訊息顯示區域。 |
| `templates/index.html`| `base.html` | **首頁**：主畫面容器，包含餘額顯示模組、新增表單模組、歷史清單模組（及篩選過濾器）。 |
| `templates/edit.html` | `base.html` | **編輯頁**：呈現修改表單，載入該筆項目原始資料供使用者修改。 |

## 4. 路由骨架程式碼

已在 `app/routes/main_routes.py` 中建立含有 Docstring 註解的骨架，開發者可直接於該檔案實作對應邏輯。
