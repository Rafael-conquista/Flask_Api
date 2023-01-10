from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
import hmac

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="O campo 'login' deve ser preenchido")
atributos.add_argument('senha', type=str, required=True, help="O campo 'senha' deve ser preenchido")

class User(Resource):
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {"message": "usuario não encontrado"}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
                return {"message": "usuario deleted."}
            except:
                return {'message': 'ocorreu um erro enquanto tentava excluir'}, 500
        return {"message": "usuario não foi encontrado"}, 404

class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message': 'usuario já existente'}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'usuario foi criado'},201

class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if hmac.compare_digest(user.senha,dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'acess_token': token_de_acesso}, 200
        return {'message': 'o usuario ou senha está incorreto'}, 401

    
