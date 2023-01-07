from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis(Resource):
    def get(self):
        return {"hoteis":[hotel.json() for hotel in HotelModel.query.all()]}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument("nome", type=str, required=True, help="o campo 'nome' não pode estar vazio")
    argumentos.add_argument("estrelas", type=float, required=True, help="o campo 'estrelas' não pode estar vazio")
    argumentos.add_argument("diaria")
    argumentos.add_argument("cidade")

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {"message": "Hotel não encontrado"}, 404

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {
                'message': "Id '{}' já existente".format(hotel_id)
            }, 400  
    
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'ocorreu um erro enquanto tentava salvar'}, 500
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            try:
                hotel_encontrado.save_hotel()
            except:
                return {'message': 'ocorreu um erro enquanto tentava salvar'}, 500
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {'message': 'ocorreu um erro enquanto tentava salvar'}, 500
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
                return {"message": "Hotel deleted."}
            except:
                return {'message': 'ocorreu um erro enquanto tentava excluir'}, 500
        return {"message": "Hotel não foi encontrado"}, 404
