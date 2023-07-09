import os
from main import transformed_data


def apiMain(event, context):

    rds_host_moodle = os.environ['rds_host_moodle']
    db_user_moodle = os.environ['db_user_moodle']
    db_pass_moodle = os.environ['db_pass_moodle']
    db_name_moodle = os.environ['db_name_moodle']
    db_port_moodle = int(os.environ['db_port_moodle'])
    username_opensearch = os.environ['username_opensearch']
    password_opensearch = os.environ['password_opensearch']
    endpoint_opensearch = os.environ['endpoint_opensearch']
    index_opensearch = os.environ['index_opensearch']

    data = transformed_data(rds_host_moodle, db_user_moodle, db_pass_moodle, db_name_moodle, db_port_moodle,
                            username_opensearch, password_opensearch, endpoint_opensearch, index_opensearch)
    data.extract_data()

    return {
        'statusCode': 200
    }

