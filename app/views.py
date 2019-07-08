import json

from flask import (Response, abort, jsonify, redirect,
                   render_template, request, url_for)

import jutils

from app import app
from app.parser import journal

# import exceptions as exc



@app.route('/')
def index():
    return redirect('/jrnl/')


@app.route('/jrnl/<string:jrnl_name>/')
def frontend_root(jrnl_name):
    jrnl = jutils.load(jrnl_name)
    if jrnl is None:
        abort(404)

    entries = journal(jrnl)

    return render_template('index.html', entries=entries,
                           jrnl_name=jrnl_name)


# @api.route('/', endpoint='index')
# def api_root():
#     return jsonify(help="See /api/jrnl/")


# @api.route('/jrnl/')
# def get_jrnl_list():
#     rv = {}
#     for name in jutils.ls():
#         rv[name] = url_for('api.jrnl', name=name, _external=True)

#     return jsonify(journals=rv)


# @api.route('/jrnl/<string:name>/', endpoint='jrnl')
# def get_jrnl(name):
#     jrnl = jutils.load(name)
#     if jrnl is None:
#         raise exc.NotFound("Journal '%s' not found." % name)

#     filters = dict(
#         tags=request.args.getlist('tags'),
#         start_date=request.args.get('start_date'),
#         end_date=request.args.get('end_date'),
#         starred=request.args.get('starred') == 'true',
#         strict=request.args.get('strict') == 'true',
#         short=request.args.get('short') == 'true',
#     )

#     jrnl.filter(**filters)

#     return Response(
#         json.dumps(jutils.entries(jrnl)),
#         mimetype='application/json'
#     )


# @api.route('/jrnl/<string:name>/tags/')
# def jrnl_tag(name):
#     jrnl = jutils.load(name)
#     if jrnl is None:
#         raise exc.NotFound("Journal '%s' not found." % name)

#     tags = jutils.tags(jrnl)
#     return jsonify(tags=tags, count=len(tags))
