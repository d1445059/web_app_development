from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import Transaction

# 定義 Blueprint，用來模組化專案的路由
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁：顯示總結餘、歷史紀錄清單與新增紀錄的表單。
    輸入: ?category= (URL Query Parameter，可選) 用於篩選特定類別
    邏輯: 獲取最新結餘與所有的相關收支列表
    輸出: 渲染 templates/index.html
    """
    pass

@main_bp.route('/add', methods=['POST'])
def add_transaction():
    """
    處理新增收支紀錄的請求
    輸入: 表單資料 (amount, type, category, note)
    邏輯: 進行基本表單驗證後，寫入資料庫
    輸出: 處理成功或失敗均重導向 (Redirect) 至首頁 /
    """
    pass

@main_bp.route('/edit/<int:record_id>', methods=['GET'])
def edit_transaction_page(record_id):
    """
    呈現編輯特定紀錄的頁面
    輸入: 路徑參數 record_id
    邏輯: 查詢 DB 該筆紀錄
    輸出: 若存在則渲染 templates/edit.html，否則 flash 錯誤並重導向 /
    """
    pass

@main_bp.route('/update/<int:record_id>', methods=['POST'])
def update_transaction(record_id):
    """
    處理更新單筆收支紀錄的請求
    輸入: 路徑參數 record_id, 表單資料 (amount, type, category, note)
    邏輯: 驗證欄位後進行資料庫 update
    輸出: 處理後重導向至首頁 /
    """
    pass

@main_bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_transaction(record_id):
    """
    處理刪除特定收支紀錄的請求
    輸入: 路徑參數 record_id
    邏輯: 對 DB 執行 delete 操作
    輸出: 處理完成後重導向至首頁 /
    """
    pass
