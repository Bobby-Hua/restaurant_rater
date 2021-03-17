# -*- coding: utf-8 -*-
def search_res(conn,rname,city,cuisine,cost):
    query = "SELECT rs.res_id, rs.res_name,avg(r.stars_value) as star,"\
            "rs.cost_category, ct.cuisine_name, c.city_name "\
            "FROM restaurant rs, cuisine_type ct, serves_cuisine s, rating r,city c "\
            "WHERE rs.res_id = s.res_id AND ct.cuisine_id = s.cuisine_id "\
            "  AND rs.res_id = r.res_id AND rs.res_name LIKE %s "\
            "  AND rs.city_id = c.city_id AND c.city_name = %s "\
            "  AND ct.cuisine_name in %s AND rs.cost_category in %s "\
            "GROUP BY rs.res_id, rs.res_name, rs.cost_category, ct.cuisine_name, c.city_name "\
            "ORDER BY star desc;"
    args = "%" + rname +"%", city[0], tuple(cuisine), tuple(cost)
    
    return conn.execute(query, args)

def all_city(conn):
    query = "SELECT city_name "\
            "FROM city;"
    
    return conn.execute(query)
            
def all_cuisine(conn):
    query = "SELECT cuisine_name "\
            "FROM cuisine_type;"
    
    return conn.execute(query)
            