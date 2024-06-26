from database.DB_connect import DBConnect
from model.gene import Gene


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_nodes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from genes"""

        cursor.execute(query)

        for row in cursor:
            result.append(Gene(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_edge(c1,c2):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select sum(corr1) as weight
                from
                (select distinct i.GeneID1 g1ID1,i.GeneID2 g1ID2,i.Expression_Corr corr1,g1.Chromosome cromo1,g2.Chromosome cromo2
                from interactions i join genes g1 join genes g2
                on i.GeneID1 = g1.GeneID  and i.GeneID2 = g2.GeneID 
                where g1.Chromosome != 0 and g2.Chromosome != 0 and g1.Chromosome = %s and g2.Chromosome = %s)
                as t1
                """

        cursor.execute(query, (c1,c2,))

        result = cursor.fetchall()

        cursor.close()
        conn.close()
        return result

