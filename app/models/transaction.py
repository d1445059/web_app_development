from app.models.database import get_db_connection
from typing import List, Dict, Any, Optional

class Transaction:
    @staticmethod
    def create(amount: int, trans_type: str, category: str, note: str = "") -> int:
        """建立一筆新的收支紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''INSERT INTO transactions (amount, type, category, note) 
                   VALUES (?, ?, ?, ?)''',
                (amount, trans_type, category, note)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all(category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """取得歷史收支清單，可依據類別過濾，並依照時間由最新到最舊排序"""
        with get_db_connection() as conn:
            if category_filter:
                cursor = conn.execute(
                    'SELECT * FROM transactions WHERE category = ? ORDER BY created_at DESC',
                    (category_filter,)
                )
            else:
                cursor = conn.execute('SELECT * FROM transactions ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(record_id: int) -> Optional[Dict[str, Any]]:
        """取得單筆明細"""
        with get_db_connection() as conn:
            cursor = conn.execute('SELECT * FROM transactions WHERE id = ?', (record_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def update(record_id: int, amount: int, trans_type: str, category: str, note: str = "") -> bool:
        """修改/編輯已送出的紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''UPDATE transactions 
                   SET amount = ?, type = ?, category = ?, note = ? 
                   WHERE id = ?''',
                (amount, trans_type, category, note, record_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(record_id: int) -> bool:
        """刪除特定紀錄"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM transactions WHERE id = ?', (record_id,))
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_total_balance() -> int:
        """自動計算總餘額 (總收入 - 總支出)"""
        with get_db_connection() as conn:
            cursor = conn.execute(
                '''SELECT 
                     SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) - 
                     SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) 
                   AS balance 
                   FROM transactions'''
            )
            row = cursor.fetchone()
            return row['balance'] if row and row['balance'] is not None else 0
