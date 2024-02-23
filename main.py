from flask import (
    Flask,
    request,
    render_template,
    abort,
)
from marshmallow import ValidationError
from service.main import AntiplagService
from service.entities import (
    CheckInput,
    CheckResult
)
from schema import (
    BadRequestSchema,
    CheckSchema
)

def create_app():

    app = Flask(__name__)

    @app.errorhandler(400)
    def bad_request_handler(ex: ValidationError):
        return BadRequestSchema().dump(ex), 400

    @app.route('/', methods=['get'])
    def index():
        return render_template("index.html")

    @app.route('/check/', methods=['get', 'post'])
    def check() -> CheckResult:
 
        schema = CheckSchema()
        service = AntiplagService()

        if request.method == "POST":
            
            try:
                name=request.form['alg']
                ref_text=request.form['ref_text'],
                candidate_text=request.form['candidate_text']
                
                request_data = CheckInput(
                    name=request.form['alg'],
                    ref_text=request.form['ref_text'],
                    candidate_text=request.form['candidate_text']
                )
                data = service.check(
                    data=schema.load(request_data)
                )
            except ValidationError as ex:
                abort(400, ex)
            else:
                schema.dump(data)
            finally:
                return render_template('index.html', result=data['percent'])          
        else:
            return render_template("index.html")

    return app


app = create_app()