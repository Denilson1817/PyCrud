from marshmallow import Schema, fields, validate

class MovieSchema(Schema):
    name = fields.Str(required=True, validate=[validate.Length(min=1)])
    actors = fields.Str(required=True, validate=[validate.Length(min=1)])
    director = fields.Str(required=True, validate=[validate.Length(min=1)])
    genre = fields.Str(required=True, validate=[validate.Length(min=1)])
    
    # Rating ahora solo acepta números decimales (float)
    rating = fields.Float(required=True, validate=validate.Range(min=0, max=10))
    
    # Asegura que realeseDate sea una fecha válida
    realeseDate = fields.Date(required=True)
    done = fields.Bool()