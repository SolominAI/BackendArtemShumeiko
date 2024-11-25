from fastapi import Query, APIRouter

from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
]


@router.get('')
def get_hotel(
        id: int | None = Query(None, description='ID отеля'),
        title: str | None = Query(None, description='Название отеля'),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.post('')
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
    return {'status': 'OK'}


@router.put("/{hotel_id}")
def update_hotel(id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['title'] = hotel_data.title
            hotel['name'] = hotel_data.name
            return {'status': 'OK'}
    return {'status': 'hotel not found'}


@router.patch("/{hotel_id}",
              summary='Частичное обновление данных об отеле',
              description='<h1>Метод для обновления name и title</h1>')
def update_hotel_fields(hotel_id: int, hotel_data: HotelPATCH,):
    global hotels
    update_fields = []

    for hotel in hotels:
        if hotel['id'] == hotel_id:
            if hotel_data.title:
                hotel['title'] = hotel_data.title
                update_fields.append('title')

            if hotel_data.name:
                hotel['name'] = hotel_data.name
                update_fields.append('name')

            return {'status': 'OK', 'update_fields': update_fields} if update_fields else {'status': 'no changes made'}

    return {'status': 'hotel not found'}


@router.delete('/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}