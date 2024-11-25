from fastapi import Query, Body, APIRouter

from schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix='/hotels', tags=['Отели'])

hotels = [
    {'id': 1, 'title': 'Сочи', 'name': 'sochi'},
    {'id': 2, 'title': 'Дубай', 'name': 'dubai'},
    {'id': 3, 'title': 'Москва', 'name': 'moscow'},
    {'id': 4, 'title': 'Казань', 'name': 'kazan'},
    {'id': 5, 'title': 'Санкт-Петербург', 'name': 'spb'},
    {'id': 6, 'title': 'Владивосток', 'name': 'vld'},
    {'id': 7, 'title': 'Петропавловск', 'name': 'chatka'},
]


@router.get('')
def get_hotel(
        hotel_id: int | None = Query(None, description='ID отеля'),
        title: str | None = Query(None, description='Название отеля'),
        page: int = Query(1, description='Номер стр.'),
        per_page: int = Query(3, description='Кол-во отелей на стр.'),
):
    hotels_ = []
    for hotel in hotels:
        if hotel_id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_.append(hotel)

    start = (page-1) * per_page
    end = start + per_page

    return hotels_[start:end]


@router.post('')
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    '1': {'summary': "Владивосток",
          'value': {
            'title': 'Отель Меридиан',
            'name': 'meridian'
            }
          },
    '2': {'summary': "Дубай",
          'value': {
            'title': 'Отель Дубай у фонтана',
            'name': 'dubai_fountain'
            }
          }})):

    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': hotel_data.title,
        'name': hotel_data.name
    })
    return {'status': 'OK'}


@router.put("/{hotel_id}")
def update_hotel(hotel_id: int, hotel_data: Hotel):
    for hotel in hotels:
        if hotel['id'] == hotel_id:
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
