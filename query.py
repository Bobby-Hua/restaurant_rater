# -*- coding: utf-8 -*-
def search_res(conn,rname,city,cuisine,cost):
    query = "SELECT rs.res_id, rs.res_name,avg(r.stars_value) as star "\
            "FROM restaurant join cuisine_type join serves_cuisine as rs, rating r,city c "\
            "WHERE rs.res_id = r.res_id AND rs.res_name LIKE %s "\
            "  AND rs.city_id = c.city_id AND c.city_name = %s "\
            "  AND rs.cuisine_name LIKE %s AND rs.cost_category = %s "\
            "GROUP BY rs.res_id, rs.res_name "\
            "ORDER BY star desc;"
    args = "%" + rname +"%", city, cuisine, cost
    
    return conn.execute(query, args)

def all_city(conn):
    query = "SELECT city_name "\
            "FROM city;"
    
    return conn.execute(query)
            
def all_cuisine(conn):
    query = "SELECT cuisine_name "\
            "FROM cuisine_type;"
    
    return conn.execute(query)
            