from app.models.turno import Turno
from app.models.centro import Centro
from app.helpers.forms import TurnoForm
from flask import jsonify, request, abort,Response
from datetime import date, datetime,time,timedelta
import json


def turno_list(id,fecha=date.today()):
    try:
        centro = Centro.with_id(id)
        if not centro:
            return Response('El centro no existe',status=400)
        turno= Turno.bloques_disponibles(id,str(fecha))
    except:
        return Response(status=500)
    data_turno = []

    for i in turno:
        date_time = datetime.strptime(i, "%H:%M") + timedelta(minutes=30)
        data_turno.append({
            "centro_id": id,
            "hora_inicio": i,
            "hora_fin": date_time.strftime("%H:%M"),
            "fecha": str(fecha)
        })

    final = json.dumps({"turnos": data_turno}, indent=2, ensure_ascii=False)
    return Response(final, mimetype='application/json')


def turno_create(id):
    data = request.get_json()
    form= TurnoForm(csrf_enabled=False)
    form.email= data['email']
    form.telefono = data['telefono']
    form.hora_inicio = data['hora_inicio']
    form.fecha = data['fecha']
    form.centro_id = data['centro_id']

    fecha = datetime.strptime(data["fecha"], '%Y-%m-%d')
    print("fecha",fecha)
    hora_inicio = datetime.now()
    hora_inicio = hora_inicio.strftime("%H:%M")
    if not form.validate_on_submit():
        print("form errors :",form.errors)
        return Response('Error de validacion',status=400)
    if not form.centro_id == id:
        return Response('Error de validacion del centro',status=400)
   
    date_time = datetime.strptime(data['hora_inicio'], "%H:%M") + timedelta(minutes=30)
    date_time = date_time.strftime("%H:%M")
    print("date_time",date_time)
    if fecha < (datetime.today()+ timedelta(days=-1)):
        return Response('La fecha debe ser mayor o igual a la fecha actual',status=400)
    print("form.hora_inicio:",form.hora_inicio)
    print("hora_inicio:",hora_inicio)
    if  (data['hora_fin'] > date_time) or (data['hora_fin'] < date_time):
        return Response('La hora fin de turno no coincide con lo esperado',status=400)
    print("form.fecha",form.fecha)
    print("date.today",date.today())
   
    if form.fecha == date.today():
        print("form.fecha dentro del if",form.fecha)
        print("entre a la fecha linea 63")
        if(form.hora_inicio < hora_inicio):
            print("entre a la comparacion de hora de inicio")
            return Response('La hora del turno debe ser mayor a la hora actual',status=400)
    try:

        centro = Centro.with_id(id)
        if not centro:
            return Response('El centro no existe',status=400)
        turnos_disponibles=Turno.bloques_disponibles(form.centro_id,form.fecha)
        if form.hora_inicio not in  turnos_disponibles:
            return Response('El turno no esta disponible',status=400)
        turno = Turno.add_and_return(data)

    except:

        return Response(status=400)
    turno_creado= {}

    turno_creado={
        "centro_id": turno.centro_id,
        "email": turno.email,
        "telefono":turno.telefono,
        "hora_inicio": turno.hora_inicio.strftime("%H:%M"),
        "hora_fin": turno.hora_fin.strftime("%H:%M"),
        "fecha": str(turno.fecha)
     }

    final = json.dumps({"atributos": turno_creado}, indent=2)
    return Response(final, status=201)
