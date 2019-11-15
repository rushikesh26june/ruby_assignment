import json
from config import get_logger, db_config, filepath
from flask import Flask, request, Response
from sql_execute import SqlExecute
from response_messages import health_response, response_success, response_server_failure, \
    response_bad_request

app = Flask(__name__)

logger = get_logger('log.txt')
exec_obj = SqlExecute(db_config=db_config,
                      logger=logger)


@app.route('/health_status', methods=['GET'])
def health():
    return Response(
        status=health_response['status'],
        response=json.dumps(
            health_response['response']),
        mimetype='application/json')


@app.route('/invoke_master', methods=['GET', 'POST'])
def runner_child():
    try:
        if request.method == 'GET':
            logger.info('Received request {} '.format(request.query_string))
            id = request.args.get('sku_id')
            master_table_name = request.args.get('master_table_name')
            output = exec_obj.fetch(sku_id=id, master_table_name=master_table_name)
            logger.info('logged response {}'.format(output))
            return Response(
                status=response_success['status'],
                response=output,
                mimetype='application/json')
        else:
            msg = json.loads(request.data)
            logger.info('Received request {} '.format(msg))
            query_type = msg.get("query_type").lower()
            params = msg.get('payload')
            if not query_type:
                raise ValueError("Operation to be performed has to be specified")
            elif query_type == 'insert':
                output = exec_obj.insert(params)
            elif query_type == 'create':
                output = exec_obj.create(params, filepath)
            elif query_type == 'append':
                output = exec_obj.append(params)

            logger.info('logged response {}'.format(output))
            return Response(
                status=response_success['status'],
                response=output,
                mimetype='application/json')

    except ValueError as ve:
        return Response(
            status=response_bad_request['status'],
            response=json.dumps({
                'response': str(ve)}),
            mimetype='application/json')

    except Exception as e:
        logger.error(e)
        return Response(
            status=response_server_failure['status'],
            response=json.dumps({
                'response': response_server_failure['response']}),
            mimetype='application/json')


if __name__ == '__main__':
    print("Running")
    app.run(host='0.0.0.0', port=8080, threaded=True)


