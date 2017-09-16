#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, g, render_template, redirect, request, session
from flask_sijax import Sijax, route
from sijax.response.base import BaseResponse
from util.session import is_logged_in
from handler.base import AutoRoute, Handler

from handler.index import Index
from handler.about import About
from handler.login import Login
from handler.signup import SignUp
from handler.alert import Alert
from handler.profile import Profile
from handler.free import Free

__all__ = ['app', 'render_template', 'redirect', 'BaseResponse', 'request', 'Handler']

app = Flask(
    __name__, template_folder='../resource/template', static_folder='../resource/static'
)

Sijax(app)


allow_anonymous = (
    '/login'
)


@app.before_request
def before_request():
    """
    login check
    :return:
    """
    if request.path not in allow_anonymous and not is_logged_in():
        redirect('login')


@route(app, '/<page>')
@route(app, '/')
def index(page: str = 'index'):
    """
    index route
    :param page:
    :return:
    """
    handler: AutoRoute = AutoRoute.route.get(page)
    if not handler:
        return f'Page "{page}" not found', 404
    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_object(handler())
        return g.sijax.process_request()

    return handler().render(navbar=dict(left=(Index(), Alert(), About()), right=(Free(), Login(), Profile())))
