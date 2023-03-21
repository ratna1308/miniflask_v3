import pdb
import json
from flask import Blueprint, request, Response
from dal.dml import fetch_resource, insert_resource, __delete_resource, upsert_films
from models.datamodels.characters import Character_
from pydantic import parse_obj_as, error_wrappers
from pydantic.error_wrappers import ValidationError
from models.datamodels.planets import Planet_

from pydantic import BaseModel, validator
from typing import Union, Optional
from datetime import datetime



class PatchPlanet_(BaseModel):
    climate: str
    created: str
    diameter: Optional[str]
    edited: Union[str,datetime]
    gravity: Optional[str]
    name: Optional[str]
    orbital_period: Optional[str]
    population: Union[str,int]
    rotation_period: str
    surface_water: str
    terrain: str
    url: Optional[str]

class PostPlanetResponse(BaseModel):
    """
      response_obj = {
        "records_count": result,
        "planet_name": planet.name,
        "message": msg
    }
    """

    records_count: Union[int, str]
    planet_name: Optional[str]
    message: str

    @validator("records_count")
    def check_records_count(cls, records_count):
        if isinstance(records_count, int) or isinstance(records_count, str):
            return int(records_count)

# Blueprit class instantiation
Planet_app = Blueprint("star", __name__, url_prefix="/star")


@Planet_app.get("/welcome")
def welcome():
    return "hello world from starwars sub-application for planet"

@Planet_app.route("/Planet", methods=["GET"])
def get_planet():
    data = fetch_resource("planet")
    Planet = data.get("name")
    Planet = parse_obj_as(list(Planet), Planet_)
    response = {
        "name": data.get("name"),
        "message": "successful"
    }
    return Response(response, status=200, mimetype="application/json")

@Planet_app.route("/Planet", methods=["POST"])
def post_planet():
    """
        {
    "climate": "Arid",
    "created": "2014-12-09T13:50:49.641000Z",
    "diameter": "10465",
    "edited": "2014-12-15T13:48:16.167217Z",
    "gravity": "1",
    "name": "Tatooine",
    "orbital_period": "304",
    "population": "120000",
    rotation_period: str,
    "url": "https://swapi.dev/api/planets/1/"
        }
    :return:
    """

    request_data = request.json
    # request body validation
    try:
        planet_data = Planet_(**request_data)
    except error_wrappers.ValidationError as ex:
        response_obj = {
            "message": f"{ex}"
        }
        return Response(
            json.dumps(response_obj),
            status=422,
            mimetype="application/json"
        )

    planet_column = [
        "climate",
        "created",
        "diameter",
        "edited",
        "gravity",
        "name",
        "orbital_period",
        "population",
        "rotation_period"
        "surface_water"
        "terrain"
        "url"
    ]

    planet_values = [
        planet_data.climate,
        planet_data.created,
        planet_data.diameter,
        planet_data.edited,
        planet_data.gravity,
        planet_data.name,
        planet_data.orbital_period,
        planet_data.population,
        planet_data.rotation_period,
        planet_data.surface_water,
        planet_data.terrain,
        planet_data.url

    ]

    result = insert_resource(
        "planet", "planet_name", planet_data.gravity, planet_column, planet_values
    )

    msg = None
    if result:
        msg = "record created successfully"
    else:
        response_obj = {
            "message": "failed to insert record"
        }
        return Response(
            json.dumps(response_obj),
            status=409,
            mimetype="application/json"
        )

    response_obj = {
        "records_count": result,
        "planet_name": planet_data.name,
        "message": msg
    }

    # response validation
    PostPlanetResponse(**response_obj)

    return Response(
        json.dumps(response_obj),
        status=201,
        mimetype="application/json"
    )








