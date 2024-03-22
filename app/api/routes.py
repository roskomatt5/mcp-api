from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Portfolio, Resume, project_schema, projects_schema, resume_schema, resumes_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/projects', methods=['POST'])
@token_required
def create_project(current_user_token):
    title = request.json['title']
    link = request.json['link']
    repo_link = request.json['repo_link']
    user_token = current_user_token.token

    project = Portfolio(title, link, repo_link, user_token=user_token,date_created=current_timestamp)

    db.session.add(project)
    db.session.commit()
    response = {
        'title': project.title,
        'link': project.link,
        'repo_link': project.repo_link,
        'date_created': project.date_created
    }
    return jsonify(response)


@api.route('/projects', methods = ['GET'])
@token_required
def get_project(current_user_token):
    a_user = current_user_token.token
    project = Portfolio.query.filter_by(user_token = a_user).all()
    response = projects_schema.dump(project)
    return jsonify(response)

@api.route('/projects/<id>', methods = ['GET'])
@token_required
def get_single_project(current_user_token, id):
    author = current_user_token.token
    project = Portfolio.query.get(id)
    response = project_schema.dump(project)
    return jsonify(response)


@api.route('/projects/<id>', methods = ['POST','PUT'])
@token_required
def update_file(current_user_token, id):
    project = Portfolio.query.get(id)
    project.title = request.json['title']
    project.link = request.json['link']
    project.repo_link = request.json['repo_link']
    project.date_created = request.json['date_created']
    project.user_token = current_user_token.token

    db.session.commit()
    response = project_schema.dump(project)
    return jsonify(response)

@api.route('/projects/<id>', methods = ['DELETE'])
@token_required
def delete_file(current_user_token, id):
    project = Portfolio.query.get(id)
    db.session.delete(project)
    db.session.commit()
    response = project_schema.dump(project)
    return jsonify(response)


@api.route('/resumes', methods = ['POST'])
@token_required
def create_resume(current_user_token):
    filename = request.json['filename']
    file_path = request.json['file_path']
    uploaded_at = request.json['uploaded_at']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    resume = Resume(filename,file_path,uploaded_at,user_token=user_token) 
    
    db.session.add(resume)
    db.session.commit()

    response = project_schema.dump(resume)
    return jsonify(response)

@api.route('/resumes', methods = ['GET'])
@token_required
def get_resume(current_user_token):
    a_user = current_user_token.token
    resume = Resume.query.filter_by(user_token = a_user).all()
    response = resumes_schema.dump(resume)
    return jsonify(response)

@api.route('/resumes/<id>', methods = ['GET'])
@token_required
def get_single_resume(current_user_token, id):
    author = current_user_token.token
    resume = Resume.query.get(id)
    response = resume_schema.dump(resume)
    return jsonify(response)

@api.route('/resumes/<id>', methods = ['POST','PUT'])
@token_required
def update_resume(current_user_token, id):
    resume = Resume.query.get(id)
    resume.filename = request.json['filename']
    resume.file_path = request.json['file_path']
    resume.uploaded_at = request.json['uploaded_at']
    resume.user_token = current_user_token.token

    db.session.commit()
    response =resume_schema.dump(resume)
    return jsonify(response)

@api.route('/resumes/<id>', methods = ['DELETE'])
@token_required
def delete_resume(current_user_token, id):
    resume = Resume.query.get(id)
    db.session.delete(resume)
    db.session.commit()
    response = project_schema.dump(resume)
    return jsonify(response)
