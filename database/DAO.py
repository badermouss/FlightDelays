from database.DB_connect import DBConnect
from modello.airport import Airport
from modello.connessione import Connessione


class DAO:

    @staticmethod
    def getAllAirports():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT * from airports a order by a.AIRPORT asc"""

        cursor.execute(query)

        for row in cursor:
            result.append(Airport(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(nMin, idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select a.ID, a.IATA_CODE , count(distinct(f.AIRLINE_ID)) as numCompDiverse
                    from airports a, flights f  
                    where a.ID = f.ORIGIN_AIRPORT_ID or a.ID = f.DESTINATION_AIRPORT_ID
                    group by a.ID, a.IATA_CODE 
                    having numCompDiverse >= %s
                    order by a.ID , f.AIRLINE_ID 
                    """

        cursor.execute(query, (nMin,))

        for row in cursor:
            # proseguire da qui prossima volta
            result.append(idMap[row["ID"]])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV1(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as N 
                    from flights f
                    group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID
                    order by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID 
                """

        cursor.execute(query)

        for row in cursor:
            # proseguire da qui prossima volta
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                                      idMap[row["DESTINATION_AIRPORT_ID"]],
                                      row["N"
                                          ""
                                          ""
                                          ""])
                          )

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdgesV2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select t1.ORIGIN_AIRPORT_ID, t1.DESTINATION_AIRPORT_ID, coalesce (t1.peso, 0) + coalesce (t2.peso, 
        0) as pesoTotale
        from (select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as peso from flights f 
        group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID order by f.ORIGIN_AIRPORT_ID , 
        f.DESTINATION_AIRPORT_ID ) t1 left join ( select f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID, count(*) as 
        peso from flights f group by f.ORIGIN_AIRPORT_ID , f.DESTINATION_AIRPORT_ID order by f.ORIGIN_AIRPORT_ID , 
        f.DESTINATION_AIRPORT_ID ) t2 on t1.ORIGIN_AIRPORT_ID = t2.DESTINATION_AIRPORT_ID and 
        t1.DESTINATION_AIRPORT_ID = t2.ORIGIN_AIRPORT_ID where t1.ORIGIN_AIRPORT_ID < t1.DESTINATION_AIRPORT_ID or 
        t2.ORIGIN_AIRPORT_ID is null"""

        cursor.execute(query)

        for row in cursor:
            # proseguire da qui prossima volta
            result.append(Connessione(idMap[row["ORIGIN_AIRPORT_ID"]],
                                      idMap[row["DESTINATION_AIRPORT_ID"]],
                                      row["pesoTotale"])
                          )

        cursor.close()
        conn.close()
        return result
