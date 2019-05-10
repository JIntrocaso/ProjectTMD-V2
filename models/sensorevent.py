import psycopg2
import datetime
from openzwave.value import ZWaveValue
from config import configDb

def logOpen(value):
    conn = None
    try:
        params = configDb()

        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        node_id = value.node.node_id
        message = "Node {}: Opened".format(value.node.node_id)
        event_time = datetime.datetime.now()

        sql = """INSERT INTO tmd_event(
            node_id,
            action,
            event_datetime
        ) VALUES (
            %(nodeId)s,
            %(action)s,
            %(eventDate)s
        ) RETURNING event_id;"""

        cur.execute(sql, {'nodeId': node_id, 'action': message, 'eventDate': event_time})

        event_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return event_id

def logClose(value):
    conn = None
    try:
        params = configDb()

        conn = psycopg2.connect(**params)

        cur = conn.cursor()

        node_id = value.node.node_id
        message = "Node {}: Closed".format(value.node.node_id)
        event_time = datetime.datetime.now()

        sql = """INSERT INTO tmd_event(
            node_id,
            action,
            event_datetime
        ) VALUES (
            %(nodeId)s,
            %(action)s,
            %(eventDate)s
        ) RETURNING event_id;"""

        cur.execute(sql,{'nodeId': node_id, 'action': message, 'eventDate': event_time})

        event_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return event_id