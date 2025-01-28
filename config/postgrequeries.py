import sys
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_dir)

from postgresqlservice import PostgresService


def getLeadData(idarr: list):
    ids = ",".join(str(element) for element in idarr)
    query = """
            SELECT leads.test_drive_date_time AS "Test Drive Date", 
            leads.make, leads.brand,
            leads.model_name AS "Selected Model", leads.car_price AS "Car Price",
                leads.interaction_id AS ID,
                    CASE
                        WHEN models.length_unit = 'mm' THEN ROUND(length / 1000,2)
                        ELSE models.length
                    END AS length_in_meters
                FROM leads INNER JOIN models ON
                leads.model_id = models.id
                WHERE leads.id IN ({id})
            """.format(id = ids)
    postgresDB = PostgresService()
    return postgresDB.query(query)

def getLeadDataformodel(idarr: list):
    ids = ",".join(str(element) for element in idarr)
    query = """
            SELECT le.id, le.model_name as model, le.test_drive_date_time as test_drive_date,
            le.make, le.brand, le.initial_model, le.final_model,
            le.primary_usage, le.preferences ,inte.visited_models,
            inte.total_interaction_time as total_chat_time,
            CASE
            	WHEN le.car_price_unit = 'SAR' then TRUNC(TO_NUMBER(le.car_price, '9999999') * 0.27)
            	WHEN le.car_price_unit = 'EUR' then TRUNC(TO_NUMBER(le.car_price, '9999999') * 1.07)
            	ELSE TRUNC(TO_NUMBER(le.car_price, '9999999'))
            END AS car_price,
            CASE
            	WHEN le.car_price_unit = 'SAR' then TRUNC(TO_NUMBER(le.initial_budget, '9999999') * 0.27)
            	WHEN le.car_price_unit = 'EUR' then TRUNC(TO_NUMBER(le.initial_budget, '9999999') * 1.07)
            	ELSE TRUNC(TO_NUMBER(le.initial_budget, '9999999'))
            END AS initial_budget,
            CASE
            	WHEN le.car_price_unit = 'SAR' then TRUNC(TO_NUMBER(le.final_budget, '9999999') * 0.27)
            	WHEN le.car_price_unit = 'EUR' then TRUNC(TO_NUMBER(le.final_budget, '9999999') * 1.07)
            	ELSE TRUNC(TO_NUMBER(le.final_budget, '9999999'))
            END AS final_budget,
            cu.age_range
            FROM models mo INNER JOIN leads le ON
            le.model_id = mo.id INNER JOIN interactions inte ON
            inte.lead_id = le.id INNER JOIN customer_master cu ON
            cu.id = inte.customer_id
            WHERE le.brand != 'rar' AND le.preferences is not NULL 
            AND le.preferences != '' AND le.preferences != 'null' 
            AND le.id IN ({id}) ORDER BY le.id asc
            """.format(id = ids)
    
    postgresDB = PostgresService()
    return postgresDB.query(query)
