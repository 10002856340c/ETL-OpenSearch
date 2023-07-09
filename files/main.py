import pandas as pd
import numpy as np
import base64
import pymysql
import requests
import json


class transformed_data:

    def __init__(self, rds_host_moodle, db_user_moodle, db_pass_moodle, db_name_moodle, db_port_moodle, username, password, endpoint, index_name):

        self.df_final = None
        self.rds_host_moodle = rds_host_moodle
        self.db_user_moodle = db_user_moodle
        self.db_pass_moodle = db_pass_moodle
        self.db_name_moodle = db_name_moodle
        self.db_port_moodle = db_port_moodle
        self.username_opensearch = username
        self.password_opensearch = password
        self.endpoint_opensearch = endpoint
        self.index_name_opensearch = index_name

    def connection_database(self):
            try:
                conn = pymysql.connect(
                    host=self.rds_host_moodle,
                    user=self.db_user_moodle,
                    passwd=self.db_pass_moodle,
                    db=self.db_name_moodle,
                    port=int(self.db_port_moodle),
                    connect_timeout=60,
                )
                cursor = conn.cursor()
                # Validar consulta

                self.df_mdl_files = pd.read_sql_query(
                    "SELECT id, contextid, component, filearea, filepath, filename FROM mdl_files;",
                    conn,
                ).rename({'id': 'id_mdl_files'}, axis=1)

                self.df_mdl_course = pd.read_sql_query(
                    "SELECT id, summary, sortorder, fullname, category, visible FROM mdl_course;",
                    conn,
                ).rename({'id': 'id_mdl_course'}, axis=1)

                self.df_mdl_course_categories = pd.read_sql_query(
                    "SELECT id, `path`, name, parent, coursecount, visible FROM mdl_course_categories;",
                    conn,
                ).rename({'id': 'id_mdl_course_categories'}, axis=1)

                self.df_mdl_context = pd.read_sql_query(
                    "SELECT id, contextlevel, instanceid FROM mdl_context;", conn
                ).rename({'id': 'id_mdl_context'}, axis=1)

                self.df_mdl_block_instances = pd.read_sql_query(
                    "SELECT id, blockname, parentcontextid, configdata FROM mdl_block_instances;",
                    conn,
                ).rename({'id': 'id_mdl_block_instances'}, axis=1)

                self.df_mdl_u_course_additional_info = pd.read_sql_query(
                    "SELECT id, course_id, level_id, expert_id, content_type_id FROM mdl_u_course_additional_info;",
                    conn,
                ).rename({'id': 'id_mdl_u_course_additional_info'}, axis=1)

                self.df_mdl_u_course_content_type = pd.read_sql_query(
                    "SELECT id, content_type, visible FROM mdl_u_course_content_type;", conn
                ).rename({'id': 'id_mdl_u_course_content_type'}, axis=1)

                self.df_mdl_u_course_expert = pd.read_sql_query(
                    "SELECT id, fullname FROM mdl_u_course_expert;", conn
                ).rename({'id': 'id_mdl_u_course_expert'}, axis=1)

                self.df_mdl_u_course_level = pd.read_sql_query(
                    "SELECT id, level FROM mdl_u_course_level;", conn
                ).rename({'id': 'id_mdl_u_course_level'}, axis=1)

                self.df_mdl_u_course_partnership = pd.read_sql_query(
                    "SELECT course_id, partnership_id FROM mdl_u_course_partnership;", conn
                ).rename({'id': 'id_mdl_u_course_partnership'}, axis=1)

                self.df_mdl_u_partnership = pd.read_sql_query(
                    "SELECT id, partnership_name FROM mdl_u_partnership;", conn
                ).rename({'id': 'id_mdl_u_partnership'}, axis=1)

                cursor.close()
                conn.close()


            except pymysql.Error as e:
                print("Hubo un error de conexión %d: %s" % (e.args[0], e.args[1]))

    def filter_tables_database(self):

        self.df_mdl_course_categories_filter = self.df_mdl_course_categories[
            (~self.df_mdl_course_categories["path"].str.contains("/2/")) & (
                self.df_mdl_course_categories["parent"] != 1)
            & (self.df_mdl_course_categories["coursecount"] > 0)
            & (self.df_mdl_course_categories["visible"] == 1)].reset_index(drop=True)
        self.df_courses_category_temporary = self.df_mdl_course.merge(
            self.df_mdl_course_categories_filter, how="inner", left_on="category", right_on="id_mdl_course_categories"
        )
        self.df_courses_category_temporary = self.df_courses_category_temporary[
            (self.df_courses_category_temporary["visible_x"] == 1)
            & (~self.df_courses_category_temporary["category"].isin([1, 2]))
            & (self.df_courses_category_temporary["id_mdl_course"] != 1)
        ].reset_index(drop=True)
        self.df_courses_category_temporary = self.df_courses_category_temporary[
            ['id_mdl_course', 'summary', 'sortorder', 'fullname', 'category', 'visible_x', 'id_mdl_course_categories', 'path',
             'name']].rename(
            columns={"visible_x": "visible", "id_mdl_course_categories": "catid", "fullname": "course_name",
                     "category": "category_id", "name": "category_name"})

        self.df_academies_temporary = self.df_mdl_course_categories[
            (self.df_mdl_course_categories["visible"] == 1)
            & (self.df_mdl_course_categories["parent"] != 2)
            & (self.df_mdl_course_categories["parent"] == 0)
            & (self.df_mdl_course_categories["id_mdl_course_categories"] != 2)
            & (self.df_mdl_course_categories["id_mdl_course_categories"] != 1880)
        ].reset_index(drop=True)
        self.df_academies_temporary = self.df_academies_temporary[[
            'id_mdl_course_categories', 'path', 'name']].rename(
            {'id_mdl_course_categories': 'academy_id', 'path': 'path_academy', 'name': 'academy_name'}, axis=1)

        self.df_files_courses_temporary = self.df_mdl_files[(self.df_mdl_files["filename"] != ".") & (
            self.df_mdl_files["filearea"] == "overviewfiles") & (self.df_mdl_files[
                "component"] == "course")].reset_index(
            drop=True)
        self.df_files_courses_temporary = self.df_files_courses_temporary[[
            'contextid', 'filename']]

        def decode(text):
            if text != None:
                return base64.b64decode(text).decode('utf-8')
            else:
                return ''

        self.df_mdl_block_instances['configdata'].replace(
            [None], '', inplace=True)
        self.df_mdl_block_instances['block_config'] = [
            decode(x) for x in self.df_mdl_block_instances['configdata']]

        # Código correspondiente a la celda #6
        self.df_courses_category_context = self.df_courses_category_temporary.merge(
            self.df_mdl_context, left_on='id_mdl_course', right_on='instanceid', how='left')
        self.df_courses_category_context = self.df_courses_category_context[
            (self.df_courses_category_context["contextlevel"] == 50)
        ].reset_index(drop=True)

        self.df_mdl_block_instances_filter = self.df_mdl_block_instances[self.df_mdl_block_instances['blockname']
                                                                         == 'ubits_course_features'].reset_index(drop=True)

        self.df_context_block_instances = self.df_courses_category_context.merge(
            self.df_mdl_block_instances_filter, left_on='id_mdl_context', right_on='parentcontextid', how='left')

        self.df_context_files_courses = self.df_context_block_instances.merge(
            self.df_files_courses_temporary, left_on='id_mdl_context', right_on='contextid', how='left')
        self.df_context_files_courses['contextid'] = self.df_context_files_courses['contextid'].fillna(
            0).astype(int)

        self.df_context_files_courses['course_image_url'] = np.where(self.df_context_files_courses['filename'].isna(), ('{environment_url}/theme/edumy/pix/default.jpg'), (
            '{environment_url}/pluginfile.php/' + self.df_context_files_courses['contextid'].apply(str) + '/course/overviewfiles/' + self.df_context_files_courses['filename'].apply(str)))

        self.df_courses_category_additional_info = self.df_context_files_courses.merge(
            self.df_mdl_u_course_additional_info, left_on='id_mdl_course', right_on='course_id', how='left')

        self.df_additional_info_course_expert = self.df_courses_category_additional_info.merge(
            self.df_mdl_u_course_expert, left_on='expert_id', right_on='id_mdl_u_course_expert', how='left')

        self.df_additional_info_course_level = self.df_additional_info_course_expert.merge(
            self.df_mdl_u_course_level, left_on='level_id', right_on='id_mdl_u_course_level', how='left')

        self.df_additional_info_course_content_type = self.df_additional_info_course_level.merge(
            self.df_mdl_u_course_content_type, left_on='content_type_id', right_on='id_mdl_u_course_content_type', how='left')

        self.df_courses_category_course_partnership = self.df_additional_info_course_content_type.merge(
            self.df_mdl_u_course_partnership, left_on='id_mdl_course', right_on='course_id', how='left', suffixes=('_left', '_right'))

        self.df_courses_category_partnership = self.df_courses_category_course_partnership.merge(
            self.df_mdl_u_partnership, left_on='partnership_id', right_on='id_mdl_u_partnership', how='left')

        self.df_courses_category_partnership['new_path'] = self.df_courses_category_partnership['path'].str.split(
            "/", expand=True)[1].astype(int)

        self.df_courses_category_academies_temporary = self.df_courses_category_partnership.merge(
            self.df_academies_temporary, left_on='new_path', right_on='academy_id', how='left')

        # return self.df_courses_category_academies_temporary

    def merge_table(self):

        self.df_final = self.df_courses_category_academies_temporary[['id_mdl_course', 'summary', 'sortorder', 'course_name', 'path', 'academy_id',
                                                                      'category_name']].rename({'id_mdl_course': 'id'}, axis=1)
        self.df_final['academy_id'] = self.df_final['academy_id'].fillna(
            0).astype(int)
        self.df_final['academy_id'] = np.where(
            self.df_final['academy_id'] == 0, '', self.df_final['academy_id'])

    def delete_documents(self):

        headers = {"Content-Type": "application/json"}
        username = self.username_opensearch
        password = self.password_opensearch
        endpoint = self.endpoint_opensearch
        index_name = self.index_name_opensearch

        # Eliminar todos los documentos en el índice
        url = f"{endpoint}/{index_name}/_delete_by_query"
        query = {"query": {"match_all": {}}}
        response = requests.post(url, auth=(
            username, password), headers=headers, json=query)

        if response.status_code == 200:
            print("Documentos eliminados con éxito.")
        else:
            print(f"Error al eliminar documentos: {response.status_code}")

    def insert_index_bulk(self, df):

        headers = {"Content-Type": "application/x-ndjson"}
        username = self.username_opensearch
        password = self.password_opensearch
        endpoint = self.endpoint_opensearch
        index_name = self.index_name_opensearch

        # Verifica la conexión
        response = requests.get(endpoint, auth=(username, password))
        if response.status_code == 200:
            print("Conexión exitosa a OpenSearch.")
        else:
            print("Error de conexión a OpenSearch.")
            return

        # Construir el cuerpo de la solicitud para la API Bulk
        bulk_request_body = ""
        for i, row in df.iterrows():
            document = row.to_dict()
            document_id = document["id"]
            bulk_request_body += json.dumps(
                {"index": {"_index": index_name, "_id": document_id}}) + "\n"
            bulk_request_body += json.dumps(document) + "\n"

        # Enviar la solicitud a la API Bulk
        url = f"{endpoint}/_bulk"
        response = requests.post(url, auth=(
            username, password), headers=headers, data=bulk_request_body)

        # Manejar la respuesta
        if response.status_code == 200:
            response_json = json.loads(response.content)
            num_inserted = response_json["items"].count("index")
            print("documentos insertados con éxito.")
        else:
            print(f"Error al insertar los documentos: {response.status_code}")

    def extract_data(self):

        self.connection_database()
        self.filter_tables_database()
        self.merge_table()

        # Eliminar los documentos existentes en el índice de OpenSearch
        self.delete_documents()

        # Insertar el DataFrame en el índice de OpenSearch
        self.insert_index_bulk(self.df_final)
