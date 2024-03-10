from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Task
from forms import TaskForm
from flask_login import login_required,current_user

# memoのBlueprint
task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/')
@login_required
def index():
    tasks = Task.query.filter_by(task_id=current_user.id).all() 
    uncompleted_tasks = Task.query.filter_by(is_completed=False).all()
    completed_tasks = Task.query.filter_by(is_completed=True).all()
    return render_template('task/index.html',tasks=tasks,uncompleted_tasks=uncompleted_tasks,completed_tasks=completed_tasks)

@task_bp.route('/new',methods=['GET','POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        task = Task(title=title,content=content,task_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        #flash("登録しました")
        return redirect(url_for('task.index'))
    return render_template("task/new_task.html",form=form)

# def new_task():
#     if request.method == 'POST':
#         content = request.form['content']
#         task = Task(content=content,task_id=current_user.id)
#         db.session.add(task)
#         db.session.commit()
#         return redirect(url_for('task.index'))
#     return render_template('task/new_task.html')

@task_bp.route('/tasks/<int:task_id>/complete',methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.is_completed = True
    db.session.commit()
    return redirect(url_for('task.index'))

@task_bp.route('/tasks/<int:task_id>/uncomplete',methods=['POST'])
@login_required
def uncomplete_task(task_id):
    task = Task.query.get(task_id)
    task.is_completed = False
    db.session.commit()
    return redirect(url_for('task.index'))

# @task_bp.route("/delete/<int:task_id>")
# @login_required
# def delete(task_id):
#     # データベースからmemo_idに一致するメモを取得し、
#     # 見つからない場合は404エラーを表示
#     task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()  # <= 13-5変更
#     # 削除処理
#     db.session.delete(task)
#     db.session.commit()
#     # フラッシュメッセージ
#     flash("削除しました")
#     # 画面遷移
#     return redirect(url_for("task.index"))