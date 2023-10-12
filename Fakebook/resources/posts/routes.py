from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, get_jwt_identity

from resources.users.models import UserModel

from .RecipeModel import RecipeModel
from schemas import RecipeSchema
from . import bp


@bp.route('/')
class RecipeList(MethodView):
  
  @jwt_required()
  @bp.response(200, RecipeSchema(many=True))
  def get(self):
    return RecipeModel.query.all()

  @jwt_required()
  @bp.arguments(RecipeSchema)
  @bp.response(200, RecipeSchema)
  def recipe(self, post_data):
    user_id = get_jwt_identity()
    p = RecipeModel(**recipe_data, user_id = user_id)
    try:
      p.save()
      return p
    except IntegrityError:
      abort(400, message="Invalid User Id")

@bp.route('/<recipe_id>')
class Recipe(MethodView):
  
  @jwt_required()
  @bp.response(200, RecipeSchema)
  def get(self, post_id):
    p = RecipeModel.query.get(recipe_id)
    if p:
      return p
    abort(400, message='Invalid Recipe Id')

  @jwt_required()
  @bp.arguments(RecipeSchema)
  @bp.response(200, RecipeSchema)
  def put(self, recipe_data, recipe_id):
    p = RecipeModel.query.get(recipe_id)
    if p and recipe_data['body']:
      user_id = get_jwt_identity()
      if p.user_id == user_id:
        p.body = recipe_data['body']
        p.save()
        return p
      else:
        abort(401, message='Unauthorized')
    abort(400, message='Invalid Recipe Data')

  @jwt_required()
  def delete(self, recipe_id):
     user_id = get_jwt_identity()
     p = RecipeModel.query.get(recipe_id)
     if p:
       if p.user_id == user_id:
        p.delete()
        return {'message' : 'Recipe Deleted'}, 202
       abort(401, message='User doesn\'t have rights')
     abort(400, message='Invalid Recipe Id')