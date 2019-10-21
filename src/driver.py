import json
import logging
import logging.config
import sys
import mysql.connector

from mysql.connector import Error
from src.config import log_config, db_config
from flask import Flask, request, Response
from io import StringIO
from src.response_messages import health_response, response_success, response_server_failure, \
    response_bad_request

logging.config.dictConfig(log_config)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
myconn = ''


# def __init__():
#     global myconn
#     myconn = mysql.connector.connect(host=db_config.get('host'),
#                                      user=db_config.get('user'),
#                                      passwd=db_config.get('password'),
#                                      database=db_config.get('database'))
#

app = Flask(__name__)


@app.route('/invoke_main', methods=['POST'])
def runner_main():
    try:
        msg = json.loads(request.data)
        LOGGER.info(msg)
        params = msg.get('payload')
        main_group_id = params.get('main_group_id')
        main_group_name = params.get("main_group_name")
        main_group_type = params.get("main_group_type")

        LOGGER.info("Data Collected for Main Group")
        return Response(
            status=response_success['status'],
            response=json.dumps({
                        "Group Id: ": main_group_id,
                        "Group Name: ": main_group_name,
                        "Group Type: ": main_group_type}),
            mimetype='application/json')

        # print("Group Id: ", main_group_id)
        # print("Group Name: ", main_group_name)
        # print("Group Type: ", main_group_type)

    except Exception as e:
        LOGGER.error(e)
        return Response(
            status=response_bad_request['status'],
            response=json.dumps({
                'response': response_bad_request['response']}),
            mimetype='application/json')


@app.route('/invoke_parent', methods=['POST'])
def runner_parent():
    try:
        msg = json.loads(request.data)
        LOGGER.info(msg)
        params = msg.get('payload')
        main_group_id = params.get('main_group_id')
        main_group_name = params.get("main_group_name")
        main_group_type = params.get("main_group_type")

        LOGGER.info("Data Collected for Main Group")
        return Response(
            status=response_success['status'],
            response=json.dumps({
                "Group Id: ": main_group_id,
                "Group Name: ": main_group_name,
                "Group Type: ": main_group_type}),
            mimetype='application/json')

        # print("Group Id: ", main_group_id)
        # print("Group Name: ", main_group_name)
        # print("Group Type: ", main_group_type)

    except Exception as e:
        LOGGER.error(e)
        return Response(
            status=response_bad_request['status'],
            response=json.dumps({
                'response': response_bad_request['response']}),
            mimetype='application/json')


@app.route('/invoke_master', methods=['POST'])
def runner_child():
    try:
        msg = json.loads(request.data)
        LOGGER.info(msg)
        params = msg.get('payload')
        buf = StringIO()
        sub_group_name = params.get("sub_group_name")

        if not sub_group_name:
            raise ValueError("Sub-Group Name can't be empty")

        try:
            sql_select_parent_query = f"SELECT idparent_group FROM parent_group WHERE name_parent_group='{sub_group_name}';"
            LOGGER.info(sql_select_parent_query)
            myconn = mysql.connector.connect(host=db_config.get('host'),
                                             user=db_config.get('user'),
                                             passwd=db_config.get('password'),
                                             database=db_config.get('database'))
            cursor = myconn.cursor()
            cursor.execute(sql_select_parent_query)
            parent_id = cursor.fetchall()[0][0]
        except Error as err:
            LOGGER.error(err)
            raise ValueError("Sub Group not present in parent table! Update the Parent table first.")
        finally:
            myconn.close()
            cursor.close()

        buf.write(sub_group_name + " ")

        sell_uom_type = params.get("sell_uom_type")
        if not sell_uom_type or sell_uom_type == '-':
            sell_uom_type = 0
        else:
            buf.write(sell_uom_type + " ")

        quantity = params.get("quantity")
        if quantity and not quantity == '-':
            buf.write("(" + quantity + ") ")

        sell_uom = params.get("sell_uom")
        if not sell_uom or sell_uom == '-':
            sell_uom = 0

        avg_weight_per_uom = params.get("avg_weight_per_uom")
        if not avg_weight_per_uom or avg_weight_per_uom == '-':
            avg_weight_per_uom = 0

        packaging_cost = params.get("packaging_cost")
        if not packaging_cost or packaging_cost == '-':
            packaging_cost = 0

        loading_percent = params.get("loading_percent")
        if not loading_percent or loading_percent == '-':
            loading_percent = 0

        output_sku = buf.getvalue()
        try:
            myconn = mysql.connector.connect(host=db_config.get('host'),
                                             user=db_config.get('user'),
                                             passwd=db_config.get('password'),
                                             database=db_config.get('database'))
            sql_select_master_query = "SELECT MAX(idmaster_group) FROM master_group"
            cursor = myconn.cursor()
            cursor.execute(sql_select_master_query)
            max_id = cursor.fetchall()[0][0]
            output_sku_id = max_id.split('-')[0]+'-'+str(int(max_id.split('-')[1])+1)
        except Error:
            raise ValueError('Unable to fetch last id from Master table')
        finally:
            myconn.close()
            cursor.close()

        try:
            myconn = mysql.connector.connect(host=db_config.get('host'),
                                             user=db_config.get('user'),
                                             passwd=db_config.get('password'),
                                             database=db_config.get('database'))
            sql_select_insert_query = f"INSERT INTO 'master_group' ('idmaster_group', 'name_master_group','sell_uom_master_group'," \
            f"'sell_uom_type_main_group', 'sell_uom_avg_wt_per_uom_master_group'," \
            f"'packaging_cost_master_group', 'loading_percent_master_group', 'idparent_group') VALUES ({output_sku_id}," \
            f"{output_sku},{sell_uom},{sell_uom_type},{avg_weight_per_uom},{packaging_cost},{loading_percent},{parent_id});"
            cursor = myconn.cursor()
            cursor.execute(sql_select_master_query)

            myconn.commit()
        except Error:
            raise ValueError('Data already present in Master table')
        finally:
            myconn.close()
            cursor.fetchall()
            cursor.close()

        LOGGER.info("Data Collected for Main Group: " + output_sku)
        return Response(
            status=response_success['status'],
            response=json.dumps({
                "Output Sku Id: ": output_sku_id,
                "Output Sku Name: ": output_sku,
                "Master Table Update Status: ": "Done"}),
            mimetype='application/json')

    except Error as error:
        LOGGER.error(error)
        return Response(
            status=response_bad_request['status'],
            response=json.dumps({
                'response': "Data already present in Master table"}),
            mimetype='application/json')

    except ValueError as ve:
        LOGGER.error(ve)
        return Response(
            status=response_bad_request['status'],
            response=json.dumps({
                'response': str(ve)}),
            mimetype='application/json')

    except Exception as e:
        LOGGER.error(e)
        return Response(
            status=response_bad_request['status'],
            response=json.dumps({
                'response': response_bad_request['response']}),
            mimetype='application/json')


if __name__ == '__main__':
    print("Running")
    # __init__()
    app.run(host='localhost', port=5000)


