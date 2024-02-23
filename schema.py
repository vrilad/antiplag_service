from marshmallow import Schema, validate
from marshmallow.fields import (
    Float,
    String,
    Method
)
from marshmallow.decorators import (
    post_load
)
from service.entities import (
    CheckInput
)
from service.enums import Algorithm


class CheckSchema(Schema):

    name = String(
        load_only=True,
        required=True,
        validate=validate.OneOf(Algorithm.VALUES)
    )
    ref_text = String(required=True, load_only=True)
    candidate_text = String(required=True, load_only=True)

    percent = String(dump_only=True)

    @post_load
    def make_check_data(self, data, **kwargs) -> CheckInput:
        return CheckInput(**data)


class BadRequestSchema(Schema):

    error = Method('dump_error')
    details = Method('dump_details')

    def dump_error(self, obj):
        return 'Validation Error'

    def dump_details(self, obj):
        return obj.description.messages
