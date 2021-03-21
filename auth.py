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
    """View decorator that redirects anonymous customer to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_id is None or g.user_type!='customer':
            return redirect(url_for("auth.customer_login"))

        return view(**kwargs)

    return wrapped_view

#requires restaurant login
def res_login_required(view):
    """View decorator that redirects anonymous customer to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_id is None or g.user_type!='restaurant':
            return redirect(url_for("auth.res_login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    g.user_id=session.get("user_id")
    g.user_name=session.get("user_name")
    g.user_type=session.get("user_type")
    
            


@bp.route("/customerregister", methods=("GET", "POST"))
def register_customer():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    conn=g.conn
    if request.method == "POST":
        name = request.form["username"]
        password = request.form["password"]
        phone_num=request.form["phone number"]
        
        customer_id=shortuuid.uuid() #generates a universally unique id; 22 chars
        
        args=customer_id,name,phone_num,generate_password_hash(password)
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
            
            return redirect(url_for("auth.customer_login"))
        print('-'*30)
        print(error)

        flash(error)

    return render_template("auth/customerregister.html")


@bp.route("/customerlogin", methods=("GET", "POST"))
def customer_login():
    if request.method=="POST":
        phone_num = request.form["phone_num"]
        password = request.form["password"]
  
        
    
        conn=g.conn
        error = None
        user =conn.execute("SELECT * FROM customer WHERE phone_num=%s",
                           (phone_num,)).fetchone()
        if user is None:
            error="Incorrect phone number."
        elif not check_password_hash(user['password'], password):
            error='Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id']=user['customer_id']
            session['user_name']=user['name']           
            session['user_type']='customer'
            return redirect(url_for("index"))
        flash(error)
    return render_template('auth/customerlogin.html')

@bp.route("/resregister", methods=("GET", "POST"))
def register_restaurant():
    """Register a new restaurant

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    conn=g.conn
    if request.method == "POST":
        name = request.form["username"]
        addr=request.form["street_addr"]
        cost=request.form['cost']
        description=request.form['Description']
        city_id=request.form['city_id']
        password = request.form["password"]
       
        res_id=shortuuid.uuid() #generates a universally unique id; 22 chars
        avg_star=0
        args=res_id,name,addr,cost,city_id,description,generate_password_hash(password),avg_star
        error = None


        cost_ranges=['$','$$','$$$','$$$$']


        if not name:
            error = "Name is required."
        elif not addr:
            error='Address is required'
       
        elif (cost not in cost_ranges):
            error = "Illegal cost category"
        elif not city_id:
            error="select your city"           
        elif not password:
            error = "Password is required."

        if error is None:
            # the name is available, store it in the database and go to
            # the login page
            conn.execute(
                "INSERT INTO Restaurant "\
                    "VALUES (%s, %s,%s,%s,%s,%s,%s)",
                args
            )
            
            return render_template("auth/resRegisterSuccess.html",res_id=res_id)
       

        flash(error)


    cities=conn.execute('SELECT * from city')
    all_cities=[]
    for c in cities:
        c_dict=dict(c)
        all_cities.append(c_dict)

    context=dict(cities=all_cities)

    return render_template("auth/resregister.html",**context)

@bp.route("/reslogin", methods=("GET", "POST"))
def res_login():
    if request.method=="POST":
        res_id = request.form["res_id"]
        password = request.form["password"]
    
        conn=g.conn
        error = None
        user =conn.execute("SELECT * FROM restaurant WHERE res_id=%s",
                           (res_id,)).fetchone()
        if user is None:
            error="Incorrect ID."
        elif not check_password_hash(user['password'], password):
            error='Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id']=user['res_id']
            session['user_name']=user['res_name']           
            session['user_type']='restaurant'
            return redirect(url_for("index"))
        flash(error)
    return render_template('auth/reslogin.html')

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))