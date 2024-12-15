from flask import Flask, request, jsonify, flash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app import app

def limit_flash(e):
    flash('Слишком много запросов!', 'error')

limiter = Limiter(
    get_remote_address,
    on_breach=limit_flash,
    app=app,
    default_limits=["10 per 5 second"])