from flask import render_template, Blueprint, jsonify
from flask_login import login_required, current_user
from .models import db, Post

import parser

blog_blueprint = Blueprint(
    'blog',
    __name__,
    template_folder='../templates/blog',
    url_prefix="/blog"
)


@blog_blueprint.route('/')
@login_required
def home():
    return render_template(
        'home.html',
    )


limits = {
    'default': 100,
    'poster': 200,
    'admin': 300
}


@blog_blueprint.route('/refresh')
@login_required
def refresh():
    role = current_user.roles[-1].name
    limit = limits[role]

    data = parser.main(limit)
    Post.query.delete()

    post_data = []
    for item in data:
        param = item['params'][0]['value'] if item['params'] else None
        photo = item['photos'][0]['link'] if item['photos'] else None

        post = Post()
        post.olx_id = item['id']
        post.title = item['title']
        post.price = param['value']
        post.photo = photo
        post.seller = item['user']['name']

        post_data.append(post)

    db.session.bulk_save_objects(post_data)
    db.session.commit()

    serializer = [p.serialize(role) for p in Post.query.limit(limit).all()]

    return jsonify(posts=serializer)


@blog_blueprint.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_post(id):
    post = Post.query.filter_by(olx_id=id).first()
    db.session.delete(post)
    db.session.commit()
    return '', 201


@blog_blueprint.route('/sort/<order>', methods=['GET'])
@login_required
def sort_posts(order=None):
    role = role = current_user.roles[-1].name
    limit = limits[role]

    if order == 'asc':
        serializer = [p.serialize(role) for p in Post.query.order_by(Post.price).limit(limit).all()]
    elif order == 'desc':
        serializer = [p.serialize(role) for p in Post.query.order_by(Post.price.desc()).limit(limit).all()]
    else:
        serializer = [p.serialize(role) for p in Post.query.limit(limit).all()]

    return jsonify(posts=serializer)
