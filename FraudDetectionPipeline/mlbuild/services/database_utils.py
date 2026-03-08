def sqlQuery(tablename):
    tablename = tablename.strip()
    query = f"""select * from {tablename} order by time ASC"""
    return query

