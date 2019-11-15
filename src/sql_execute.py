import mysql
import json

from config import create_query
from io import StringIO
from mysql.connector import Error


class SqlExecute(object):
    def __init__(self, db_config, logger):
        self.db_config = db_config
        self.logger = logger

    def fetch(self, sku_id, master_table_name):
        try:
            myconn = mysql.connector.connect(host=self.db_config.get('host'),
                                             user=self.db_config.get('user'),
                                             passwd=self.db_config.get('password'),
                                             database=self.db_config.get('database'))
            sql_query = f"SELECT * FROM `{master_table_name}` Where id_master = '{sku_id}'"
            print(sku_id)
            cursor = myconn.cursor(dictionary=True)
            cursor.execute(sql_query)
            result = cursor.fetchall()[0]
            if result:
                print(result)
                return json.dumps({"master_table_name": master_table_name,
                                   "sku_id": sku_id,
                                   "sku_name": result['name'],
                                    "sell_uom": result['sell_uom'],
                                    "sell_uom_type": result['sell_uom_type'],
                                    "avg_weight_per_uom": result['sell_uom_avg_wt_per_uom'],
                                    "packaging_cost": result['packaging_cost'],
                                    "loading_percent": result['loading_percent']
                                })
        except Error as err:
            self.logger.error(err)
            raise ValueError('Unable to Fetch Row from Master Table')
        finally:
            myconn.commit()
            myconn.close()
            cursor.close()

    def create(self, params, filepath='./dump.sql'):
        try:
            myconn = mysql.connector.connect(host=self.db_config.get('host'),
                                             user=self.db_config.get('user'),
                                             passwd=self.db_config.get('password'),
                                             database=self.db_config.get('database'))
            cursor = myconn.cursor()
            master_table_name = params.get('master_table_name')
            query = create_query.replace('master_group', master_table_name)
            cursor.execute(query)
            return json.dumps({'Output': 'Master Table created'})

        except Error as err:
            self.logger.error(err)
            raise ValueError('Table already exists')
        finally:
            myconn.commit()
            myconn.close()
            cursor.close()

    def append(self, params):
        try:
            myconn = mysql.connector.connect(host=self.db_config.get('host'),
                                             user=self.db_config.get('user'),
                                             passwd=self.db_config.get('password'),
                                             database=self.db_config.get('database'))
            cursor = myconn.cursor()
            master_table_name = params.get('master_table_name')
            sku_id = params.get('sku_id')
            sku_name = params.get('sku_name')
            sell_uom = params.get('sell_uom')
            sell_uom_type = params.get('sell_uom_type')
            avg_weight_per_uom = params.get('avg_weight_per_uom')
            packaging_cost = params.get('packaging_cost')
            loading_percent = params.get('loading_percent')

            update_query = f"UPDATE `{master_table_name}` SET name = '{sku_name}', sell_uom = '{sell_uom}'," \
                           f"sell_uom_type = '{sell_uom_type}', sell_uom_avg_wt_per_uom = {avg_weight_per_uom}," \
                           f"packaging_cost = {packaging_cost}, loading_percent = {loading_percent} WHERE id_master= '{sku_id}'"

            cursor.execute(update_query)
            return json.dumps({'Output': 'Master Table updated'})

        except Error as err:
            self.logger.error(err)
            raise ValueError('Unable to append Row to Master Table')
        finally:
            myconn.commit()
            myconn.close()
            cursor.close()

    def insert(self, params):
        try:
            buf = StringIO()
            sub_group_name = params.get("sub_group_name")
            master_table_name = params.get("master_table_name")

            # No Parent table for now so left empty
            parent_id = ''

            if not sub_group_name:
                raise ValueError("Sub-Group Name can't be empty")

            if not master_table_name:
                raise ValueError("Master Table Name can't be empty")

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
            output_sku_id = self.get_id(master_table_name)
            
            connector = mysql.connector.connect(host=self.db_config.get('host'),
                                                user=self.db_config.get('user'),
                                                passwd=self.db_config.get('password'),
                                                database=self.db_config.get('database'))
            print(connector)
            sql_select_insert_query = f"INSERT INTO `{master_table_name}` (id_master, name, sell_uom," \
                                      f"sell_uom_type, sell_uom_avg_wt_per_uom," \
                                      f"packaging_cost, loading_percent) VALUES ('{output_sku_id}'," \
                                      f"'{output_sku}','{sell_uom}','{sell_uom_type}',{avg_weight_per_uom},{packaging_cost},{loading_percent});"
            print(sql_select_insert_query)
            cursor = connector.cursor()
            print(cursor)
            cursor.execute(sql_select_insert_query)
            connector.commit()
            connector.close()
            cursor.close()
            self.logger.info("Data Collected for Main Group: " + output_sku)
            return json.dumps({
                "Output Sku Id: ": output_sku_id,
                "Output Sku Name: ": output_sku,
                "Master Table Update Status: ": "Done"})
        except Error as e:
            self.logger.error(e)
            raise ValueError('Data already present in Master table')

    def get_id(self, master_table_name):
        try:
            con = mysql.connector.connect(host=self.db_config.get('host'),
                                          user=self.db_config.get('user'),
                                          passwd=self.db_config.get('password'),
                                          database=self.db_config.get('database'))
            sql_select_master_query = f"SELECT MAX(id_master) FROM `{master_table_name}`"
            cur = con.cursor()
            cur.execute(sql_select_master_query)
            max_id = cur.fetchall()[0][0]
            if max_id:
                output_sku_id = max_id.split('-')[0] + '-' + str(int(max_id.split('-')[1]) + 1)
            else:
                output_sku_id = 'RO-01'
            return output_sku_id
        except Error as err:
            self.logger.error(err)
            raise ValueError(str(err))
        finally:
            con.commit()
            con.close()
            cur.close()
