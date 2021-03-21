# -*- coding: utf-8 -*-
def search_res(conn,rname,city,cuisine,cost):
    query = "SELECT rs.res_id, rs.res_name,rs.avg_star,"\
            "rs.cost_category, ct.cuisine_name, c.city_name "\
            "FROM restaurant rs, cuisine_type ct, serves_cuisine s, city c "\
            "WHERE rs.res_id = s.res_id AND ct.cuisine_id = s.cuisine_id "\
            "  AND UPPER(rs.res_name) LIKE UPPER(%s) "\
            "  AND rs.city_id = c.city_id AND c.city_name in %s "\
            "  AND ct.cuisine_name in %s AND rs.cost_category in %s "\
            "ORDER BY rs.avg_star desc;"
    args = "%" + rname +"%", tuple(city), tuple(cuisine), tuple(cost)
    
    return conn.execute(query, args)

def all_city(conn):
    query = "SELECT city_name "\
            "FROM city;"
    
    return conn.execute(query)
            
def all_cuisine(conn):
    query = "SELECT cuisine_name, cuisine_id "\
            "FROM cuisine_type;"
    
    return conn.execute(query)

def fav_food(conn, uid):
    query ="SELECT c.cuisine_id, c.cuisine_name "\
           "FROM likes_cuisine l, cuisine_type c "\
           "WHERE l.customer_id = %s AND l.cuisine_id = c.cuisine_id;"
    args = uid
    
    return conn.execute(query, args)

def recommendation(conn, fav_food_id):
    query ="SELECT rs.res_id, rs.res_name,rs.avg_star,"\
            "rs.cost_category, ct.cuisine_name, c.city_name "\
            "FROM restaurant rs, cuisine_type ct, serves_cuisine s, city c "\
            "WHERE rs.res_id = s.res_id AND ct.cuisine_id = s.cuisine_id "\
            "  AND rs.city_id = c.city_id "\
            "  AND ct.cuisine_id = %s "\
            "ORDER BY rs.avg_star desc "\
            "LIMIT 2;"
    
    return conn.execute(query, fav_food_id)

            