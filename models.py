from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship

# Flask-SQLAlchemyの生成
db = SQLAlchemy()

# ==================================================
# モデル
# ==================================================
# メモ
class Memo(db.Model):
    # テーブル名
    __tablename__ = 'memos'
    # ID（PK）
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # タイトル（NULL許可しない）
    title = db.Column(db.String(50), nullable=False)
    # 内容
    content = db.Column(db.Text)

    # ユーザーID
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name="fk_memos_users"), nullable=False)

    # User とのリレーション
    user = relationship("User", back_populates = "memos")

    
# ユーザー
class User(UserMixin, db.Model):
    # テーブル名
    __tablename__ = 'users'
    # ID（PK）    
    id = db.Column(db.Integer, primary_key=True)
    # ユーザー名
    username = db.Column(db.String(50), unique=True, nullable=False)
    # パスワード
    password = db.Column(db.String(120), nullable=False)

    email = db.Column(db.String(100),unique=True)
    

    # Memo とのリレーション
    # リレーション: １対多
    memos = relationship("Memo", back_populates = "user")


    tasks = relationship("Task",back_populates="user")
    
    # パスワードをハッシュ化して設定する
    def set_password(self, password):
        self.password = generate_password_hash(password)
    # 入力したパスワードとハッシュ化されたパスワードの比較
    def check_password(self, password):
        return check_password_hash(self.password, password)
    

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.String(200),nullable=False)
    is_completed = db.Column(db.Boolean,default=False)

    task_id = db.Column(db.Integer, db.ForeignKey('users.id', name="fk_tasks_users"), nullable=False)

    user = relationship("User", back_populates = "tasks")

    def __str__(self):
        return f'課題ID:{self.id} タイトル：{self.title} 内容：{self.content} 完了フラグ:{self.is_completed}'