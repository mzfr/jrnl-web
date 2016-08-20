from flask import (
    abort,
    Blueprint,
    jsonify,
    request,
    Response,
    render_template,
    redirect,
    url_for,
)

import jutils

import app.exceptions as exc

frontend = Blueprint('jrnl', __name__)
api = Blueprint('api', __name__)


@frontend.route('/')
def react_root():
    return redirect('/jrnl/idea')


@frontend.route('/jrnl/<string:journal_name>')
def frontend_root(journal_name='idea'):
    journal = jutils.load(journal_name or 'idea')
    if journal is None:
        abort(404)

    entries = jutils.entries(journal, count='all')
    return render_template('index.html', entries=entries)


@api.route('/', endpoint='index')
def api_root():
    return jsonify(help="See /api/jrnl/")


@api.route('/jrnl/')
def get_jrnl_list():
    rv = {}
    for name in jutils.ls():
        rv[name] = url_for('api.jrnl', name=name, _external=True)

    return jsonify(journals=rv)


@api.route('/jrnl/<string:name>/', endpoint='jrnl')
def get_jrnl(name):
    jrnl = jutils.load(name)
    if jrnl is None:
        raise exc.NotFound("Journal '%s' not found." % name)

    filters = dict(
        tags=request.args.getlist('tags'),
        start_date=request.args.get('start_date'),
        end_date=request.args.get('end_date'),
        starred=request.args.get('starred') == 'true',
        strict=request.args.get('strict') == 'true',
        short=request.args.get('short') == 'true',
    )

    print(filters['starred'])

    jrnl.filter(**filters)

    return Response(
        jutils.to_json(jrnl),
        mimetype='application/json'
    )


@api.route('/jrnl/<string:name>/tags/')
def jrnl_tag(name):
    jrnl = jutils.load(name)
    if jrnl is None:
        raise exc.NotFound("Journal '%s' not found." % name)

    tags = jutils.tags(jrnl)
    return jsonify(tags=tags, count=len(tags))
