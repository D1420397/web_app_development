# 路由設計文件 (ROUTES.md) - 食譜收藏夾系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 顯示熱門食譜與網站介紹 |
| **註冊頁面** | GET | `/auth/register` | `auth/register.html` | 顯示註冊表單 |
| **執行註冊** | POST | `/auth/register` | — | 建立帳號並自動登入 |
| **登入頁面** | GET | `/auth/login` | `auth/login.html` | 顯示登入表單 |
| **執行登入** | POST | `/auth/login` | — | 驗證身分並導向首頁 |
| **登出** | GET | `/auth/logout` | — | 清除 Session 並導向首頁 |
| **食材搜尋** | GET | `/search` | `search/index.html` | 顯示食材勾選清單 |
| **搜尋結果** | POST | `/search` | `search/results.html`| 根據勾選食材顯示食譜列表 |
| **食譜詳情** | GET | `/recipe/<int:id>` | `recipe/detail.html` | 顯示食譜完整內容 |
| **發佈食譜頁面**| GET | `/recipe/create` | `recipe/create.html` | 顯示發佈食譜表單 |
| **執行發佈** | POST | `/recipe/create` | — | 儲存食譜、食材關聯、圖片 |
| **編輯食譜頁面**| GET | `/recipe/<int:id>/edit`| `recipe/edit.html` | 顯示編輯表單 |
| **更新食譜** | POST | `/recipe/<int:id>/update`| — | 更新資料後重導向至詳情頁 |
| **刪除食譜** | POST | `/recipe/<int:id>/delete`| — | 刪除後重導向至個人中心 |
| **我的收藏** | GET | `/user/favorites` | `user/favorites.html`| 顯示已收藏的食譜 |
| **加入收藏** | POST | `/recipe/<int:id>/favorite`| — | 加入或取消收藏 (AJAX/Redirect) |
| **個人管理中心**| GET | `/user/recipes` | `user/recipes.html` | 顯示自己發佈的食譜列表 |
| **管理員儀表板**| GET | `/admin/dashboard` | `admin/dashboard.html`| 管理員管理分類與內容 |

---

## 2. 詳細路由說明

### 2.1 認證模組 (auth.py)
*   **登入/註冊**: 
    - 處理邏輯: 呼叫 `User.get_by_email` 與密碼驗證。
    - 錯誤處理: 密碼錯誤或帳號重複時，返回原頁面並顯示 Flash Message。
*   **權限控制**: 除首頁與搜尋外，多數操作需登入（使用 `@login_required`）。

### 2.2 食譜模組 (recipe.py)
*   **建立食譜**: 
    - 輸入: `title`, `description`, `instructions`, `category_id`, `ingredients[]`, `quantities[]`, `image`。
    - 處理邏輯: 建立 `Recipe` 物件，遍歷 `ingredients` 建立 `RecipeIngredient` 關聯。
*   **搜尋**:
    - 處理邏輯: 根據 `ingredient_ids` 列表，執行 SQL `IN` 查詢並計算符合度。

### 2.3 使用者中心 (user.py)
*   **收藏功能**:
    - 處理邏輯: 檢查 `favorites` 關聯是否存在，切換 (Toggle) 收藏狀態。

---

## 3. Jinja2 模板清單

| 模板路徑 | 繼承底稿 | 主要用途 |
| :--- | :--- | :--- |
| `base.html` | — | 全域導覽列、頁尾、Flash Msg |
| `index.html` | `base.html` | 展示網站門面 |
| `auth/login.html` | `base.html` | 登入表單 |
| `auth/register.html` | `base.html` | 註冊表單 |
| `search/index.html` | `base.html` | 食材選擇器 (Checkbox 列表) |
| `search/results.html` | `base.html` | 搜尋結果列表 |
| `recipe/detail.html` | `base.html` | 單一食譜顯示 |
| `recipe/create.html` | `base.html` | 新增食譜表單 |
| `recipe/edit.html` | `base.html` | 編輯食譜表單 |
| `user/favorites.html` | `base.html` | 個人收藏清單 |
| `user/recipes.html` | `base.html` | 我發佈過的食譜 |
| `admin/dashboard.html`| `base.html` | 管理員後台 |

---

## 4. 路由骨架程式碼

路由實作將分布於以下檔案：
- `app/routes/auth.py`
- `app/routes/recipe.py`
- `app/routes/user.py`
- `app/routes/admin.py`
