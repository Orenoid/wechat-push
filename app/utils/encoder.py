import json
# from app.models import db


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):

        # if isinstance(obj, db.Model):
        #     if hasattr(obj, 'to_dict'):
        #         return obj.to_dict()
        #     return {col.name: getattr(obj, col.name) for col in obj.__table__.columns}

        return json.JSONEncoder.default(self, obj)
