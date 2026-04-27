from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.transaction import Transaction

# 定義 Blueprint，用來模組化專案的路由
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """
    首頁：顯示總結餘、歷史紀錄清單與新增紀錄的表單。
    輸入: ?category= (URL Query Parameter，可選) 用於篩選特定類別
    輸出: 渲染 templates/index.html
    """
    category = request.args.get('category')
    
    # 獲取總結餘
    total_balance = Transaction.get_total_balance()
    
    # 依條件查詢歷史明細
    transactions = Transaction.get_all(category_filter=category)
    
    return render_template(
        'index.html', 
        total_balance=total_balance, 
        transactions=transactions,
        selected_category=category
    )

@main_bp.route('/add', methods=['POST'])
def add_transaction():
    """處理新增收支紀錄的請求"""
    try:
        amount = request.form.get('amount')
        trans_type = request.form.get('type')
        category = request.form.get('category')
        note = request.form.get('note', '')
        
        # 1. 驗證必填
        if not amount or not trans_type or not category:
            flash("請填寫金額、屬性與類別等必填欄位！", "danger")
            return redirect(url_for('main.index'))
            
        # 2. 驗證金額型態
        try:
            amount_int = int(amount)
            if amount_int < 0:
                flash("金額必須是大於等於 0 的正整數！", "danger")
                return redirect(url_for('main.index'))
        except ValueError:
            flash("金額輸入無效，必須為不含小數的整數數字！", "danger")
            return redirect(url_for('main.index'))
            
        # 3. 驗證收支屬性
        if trans_type not in ['income', 'expense']:
            flash("無效的收支屬性設定！", "danger")
            return redirect(url_for('main.index'))
            
        # 4. 寫入資料庫
        record_id = Transaction.create(amount_int, trans_type, category, note)
        if record_id == -1:
            flash("新增記錄時發生錯誤，請稍後再試。", "danger")
        else:
            flash("成功新增一筆帳目！", "success")
            
    except Exception as e:
        flash(f"發生未預期的系統錯誤: {str(e)}", "danger")
        
    return redirect(url_for('main.index'))

@main_bp.route('/edit/<int:record_id>', methods=['GET'])
def edit_transaction_page(record_id):
    """呈現編輯特定紀錄的頁面"""
    transaction = Transaction.get_by_id(record_id)
    
    if not transaction:
        flash("找不到該筆紀錄，可能已被刪除！", "danger")
        return redirect(url_for('main.index'))
        
    return render_template('edit.html', transaction=transaction)

@main_bp.route('/update/<int:record_id>', methods=['POST'])
def update_transaction(record_id):
    """處理更新單筆收支紀錄的請求"""
    try:
        amount = request.form.get('amount')
        trans_type = request.form.get('type')
        category = request.form.get('category')
        note = request.form.get('note', '')
        
        # 驗證必填
        if not amount or not trans_type or not category:
            flash("修改失敗：必填欄位不可為空！", "danger")
            return redirect(url_for('main.edit_transaction_page', record_id=record_id))
            
        # 驗證金額
        try:
            amount_int = int(amount)
            if amount_int < 0:
                flash("修改失敗：金額必須是大於等於 0 的整數！", "danger")
                return redirect(url_for('main.edit_transaction_page', record_id=record_id))
        except ValueError:
            flash("修改失敗：金額輸入格式有誤！", "danger")
            return redirect(url_for('main.edit_transaction_page', record_id=record_id))
            
        # 寫入更新
        success = Transaction.update(record_id, amount_int, trans_type, category, note)
        if success:
            flash("記錄已成功更新！", "success")
            return redirect(url_for('main.index'))
        else:
            flash("更新紀錄失敗（找不到原紀錄或資料庫錯誤）。", "danger")
            
    except Exception as e:
        flash(f"發生未預期錯誤: {str(e)}", "danger")
        
    return redirect(url_for('main.edit_transaction_page', record_id=record_id))

@main_bp.route('/delete/<int:record_id>', methods=['POST'])
def delete_transaction(record_id):
    """處理刪除特定收支紀錄的請求"""
    success = Transaction.delete(record_id)
    if success:
        flash("已成功刪除該筆帳目！", "success")
    else:
        flash("刪除失敗，可能記錄已不存在。", "danger")
        
    return redirect(url_for('main.index'))
