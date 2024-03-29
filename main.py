from flask import Flask, request, redirect, render_template, session, flash
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(project_dir, "build-a-blog.db"))
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 't0p5ecr3tk3y'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    # ownder_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        # self.owner = owner

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(db.String(120))
#     blog_posts = db.relationship('Blog', backref='owner')

#     def __init__(self, email, password):
#         self.email = email
#         self.password=password

@app.route('/post')
def post():
    #Need to pass in current blogs xtitle and body.
    post_id = request.args.get('id')
    print("here" + post_id)
    current_blog = Blog.query.filter_by().all()
    print(current_blog)
    print("__/n")
    print(type(current_blog))
    print("__/n")
    print(type(current_blog[0].title))
    print("__/n")

    blog_title = current_blog[int(post_id)-1].title
    blog_body = current_blog[int(post_id)-1].body


    return render_template('post.html', blog_title=blog_title, blog_body=blog_body)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    input_errors = {'blog_title':[], 'blog_body':[]}

    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog_body = request.form['blog_body']
        no_post = False
        if blog_title == "":
            input_errors['blog_title'].append('Title cannot be blank.')
            no_post = True
        if blog_body == "":
            input_errors['blog_body'].append('Blog post cannot be blank.')
            no_post = True
        if no_post == False:
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()
            return render_template('post.html', blog_title=blog_title, blog_body=blog_body)

    return render_template('newpost.html', input_errors=input_errors)
    

@app.route('/', methods=['POST', 'GET'])
def index():

    # owner = User.query.filter_by(email=session['email']).first()

    blogs = Blog.query.all()
    for post in blogs:
        id = post.id
        print(id)

    return render_template('blog.html', title="Build-a-blog", blogs=blogs)




if __name__ == '__main__':
    app.run()