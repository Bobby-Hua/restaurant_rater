#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 13:48:56 2021

@author: roberthua
"""

import functools
import uuid
import shortuuid
import base64
from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash




bp = Blueprint("auth", __name__, url_prefix="/auth")


#requires customer login
def customer_login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user_type!='customer':
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view




@bp.before_app_request
def load_logged_in_customer():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    g.user_id = session.get("user_id")
    g.user_type=session.get("user_type")


@bp.route("/customerregister", methods=("GET", "POST"))
def register_customer(conn):
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        phone_num=request.form["phone number"]
        
        customer_id=shortuuid.uuid() #generates a universally unique id; 22 chars
        
        args=customer_id,name,phone_num,password
        error = None

        if not name:
            error = "Name is required."
        elif not password:
            error = "Password is required."
        elif not phone_num:
            error = "Phone number is required."
            
        elif (
            conn.execute("SELECT phone_num FROM customer WHERE phone_num = %s", (phone_num,)).fetchone()
            is not None
        ):
            error = f"phone number {phone_num} is already registered."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            conn.execute(
                "INSERT INTO Customer (customer_id,name,phone_num,password)"\
                    "VALUES (%s, %s,%s,%s)",
                args
            )
            
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/customerregister.html")


