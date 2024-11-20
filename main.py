from fastapi import FastAPI, Query, Body
import uvicorn


app = FastAPI()


hotels = [
    {'id': 1, 'title': 'Sochi', 'name': 'sochi'},
    {'id': 2, 'title': 'Dubai', 'name': 'dubai'},
]


@app.get('/')
def get_hotels():
    return hotels


@app.get('/hotels')
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

# Задание №1 Put and Patch
@app.post('/hotels')
def create_hotel(
   title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        'id': hotels[-1]['id'] + 1,
        'title': title,
    })
    return {'status': 'OK'}


@app.put("/hotels/{hotel_id}")
def update_hotel(
        id: int = Query(description='ID отеля'),
        title: str = Body(embed=True,  description='Название отеля'),
        name: str = Body(embed=True,  description='Альтернативное название отеля'),
):
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['title'] = title
            hotel['name'] = name
            return {'status': 'OK'}
    return {'status': 'hotel not found'}


@app.patch("/hotels/{hotel_id}")
def update_hotel_fields(
        id: int = Query(description='ID отеля'),
        title: str | None = Body(default=None, embed=True, description='Название отеля'),
        name: str | None = Body(default=None, embed=True, description='Альтернативное название отеля'),
):
    hotels_ = get_hotels()
    for hotel in hotels_:
        if hotel['id'] == id:
            update_fields = []
            if title:
                hotel['title'] = title
                update_fields.append('title')
            if name:
                hotel['name'] = name
                update_fields.append('name')
            return {'status': 'OK', 'update_fields': update_fields} if update_fields else {'status': 'no changes made'}

    return {'status': 'hotel not found'}


@app.delete('/hotels/{hotel_id}')
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != hotel_id]
    return {'status': 'OK'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
