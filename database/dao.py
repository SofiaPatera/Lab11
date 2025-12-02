from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """
    @staticmethod
    def leggiConnessione(year):
        conn = DBConnect.get_connection()
        results = []
        query = """SELECT LEAST(c.id_rifugio1, c.id_rifugio2) as r1, 
                    GREATEST (c.id_rifugio1, c.id_rifugio2), 
                    c.id, c.id_rifugio1, c.id_rifugio2, c.distanza, c.diffocolta, c.durata, c.anno 
                    FROM connessione as c 
                    WHERE c.anno <= year"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            connessione = Connessione(row['id'], row['id_rifugio1'], row['id_rifugio2'],
                                      row['distanza'], row['difficolta'], row['durata'],
                                      row['anno'])
            results.append(connessione)
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def leggiRifugio(year):
        conn = DBConnect.get_connection()
        results = []
        query = """SELECT DISTINCT r.id, r.nome, r.localita, r.altitudine, r.capienza, r.aperto
                    FROM connessione as c, rifugio as r 
                    WHERE ( c.id_rifugio1 = r.id or c.id_rifugio2 = r.id) and c.anno <= year 
                    GROUP BY r.nome"""
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        for row in cursor:
            results.append(Rifugio(**row))
        cursor.close()
        conn.close()
        return results



