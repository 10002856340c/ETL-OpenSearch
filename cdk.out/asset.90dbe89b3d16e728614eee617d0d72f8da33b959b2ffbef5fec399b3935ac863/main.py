import requests
import pandas as pd
import json
import numpy as np
import pandas.io.sql as psql
import boto3
import pymysql
import logging
import os
from botocore.exceptions import ClientError
import datetime
from pandas import json_normalize
from pandas import DataFrame
from io import StringIO

class Main:
    def __init__(self):
        self.token = os.environ['token']
        self.id_tech = os.environ['id_tech']
        self.limit = os.environ['limit']
        self.fields = os.environ['fields']
        self.rds_host_moodle_plug = os.environ['rds_host_moodle_plug']
        self.rds_host_moodle_adminhr = os.environ['rds_host_moodle_adminhr']
        self.rds_host_moodle_learning = os.environ['rds_host_moodle_learning']
        self.db_user_moodle = os.environ['db_user_moodle']
        self.db_pass_moodle = os.environ['db_pass_moodle']
        self.db_name_moodle_plug =os.environ['db_name_moodle_plug']
        self.db_name_moodle_adminhr = os.environ['db_name_moodle_adminhr']
        self.db_name_moodle_learning = os.environ['db_name_moodle_learning']
        self.db_port_moodle_plug = int(os.environ['db_port_moodle_plug'])
        self.db_port_moodle_learning = int(os.environ['db_port_moodle_learning'])
        self.db_port_moodle_adminhr = int(os.environ['db_port_moodle_adminhr'])
        self.file_name = os.environ['file_name']
        self.bucket_name = os.environ['bucket_name']


    # Lista de usuarios en Workplace
    def users_workplace(self):
        url = "https://graph.facebook.com/v15.0/284719169503437/members?access_token=DQVJ1LUZAiTnEzWTQ4R0EzcS1jRnNOQjZAwVFVuUVJJd21hUzNhYzhlREdkNlJsR29GT2lOQUhQd0dnNlhwc0VueXNfV092T19vcm5zZAkRuZAWpfc3NnYXNUd1UtQ3dxN1JMek5YeHhtQnJsUlY1Q05VS0diNlNZAZAWdzNHpncDZAxOGtGMzRtcWtoMUhxazdPZAy1FLUxzTEhiMU9WZAWNESzBiYi1rYlNqT3BlVlpPc0NhTmRFeUNHTTd5VXd0N1l4bFFuajFiSUlR&limit=20000&fields=id,first_name,last_name,name,title,email,department"
        response = requests.request("GET", url, headers={}, data={})
        json_data = json.loads(response.text)

        # Creación de DataFrame usuarios workplace
        df_members = pd.json_normalize(json_data["data"])
        df_members = df_members.assign(
            username=(df_members["email"].str.split("@", n=1, expand=True))[0]
        )
        df_members = df_members[["name", "title", "username"]]
        return df_members

    # Seleccionar campos específicos de la base de datos
    def fields_database(self, df):
        df_users = df[
            [
                "HostU",
                "UserU",
                "Select_privU",
                "Insert_privU",
                "Update_privU",
                "Delete_privU",
                "Create_privU",
                "Drop_privU",
                "Grant_privU",
                "Index_privU",
                "Alter_privU",
                "Execute_privU",
                "Create_routine_privU",
                "Alter_routine_privU",
                "Create_user_privU",
                "Host",
                "Db",
                "User",
                "Select_priv",
                "Insert_priv",
                "Update_priv",
                "Delete_priv",
                "Create_priv",
                "Drop_priv",
                "Grant_priv",
                "Index_priv",
                "Alter_priv",
                "Create_routine_priv",
                "Alter_routine_priv",
                "Execute_priv",
            ]
        ]
        return df_users

    # Conexión a bases de datos Plug
    def connection_database_plug(self):
        conn = pymysql.connect(host=self.rds_host_moodle_plug, user=self.db_user_moodle, passwd=self.db_pass_moodle,
                               db=self.db_name_moodle_plug, port=self.db_port_moodle_plug, connect_timeout=60)
        cursor = conn.cursor()
        # Validar consulta
        sql = "SELECT u.Host as HostU ,u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU ,u.Event_priv as Event_privU ,u.Trigger_priv as Trigger_privU ,u.Create_tablespace_priv as Create_tablespace_privU,u.ssl_type as ssl_typeU ,u.ssl_cipher as ssl_cipherU ,u.x509_issuer as x509_issuerU ,u.x509_subject as x509_subjectU ,u.max_questions as max_questionsU ,u.max_updates as max_updatesU ,u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU ,u.plugin as pluginU ,u.authentication_string as authentication_stringU ,d.Host ,d.Db ,d.`User` ,d.Select_priv ,d.Insert_priv ,d.Update_priv ,d.Delete_priv ,d.Create_priv ,d.Drop_priv ,d.Grant_priv ,d.References_priv ,d.Index_priv ,d.Alter_priv ,d.Create_tmp_table_priv ,d.Lock_tables_priv ,d.Create_view_priv ,d.Show_view_priv ,d.Create_routine_priv ,d.Alter_routine_priv ,d.Execute_priv ,d.Event_priv ,d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User` UNION SELECT u.Host as HostU , u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU , u.Event_priv as Event_privU , u.Trigger_priv as Trigger_privU , u.Create_tablespace_priv as Create_tablespace_privU, u.ssl_type as ssl_typeU , u.ssl_cipher as ssl_cipherU , u.x509_issuer as x509_issuerU , u.x509_subject as x509_subjectU , u.max_questions as max_questionsU , u.max_updates as max_updatesU , u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU , u.plugin as pluginU , u.authentication_string as authentication_stringU ,  d.Host , d.Db , d.`User` , d.Select_priv , d.Insert_priv , d.Update_priv , d.Delete_priv , d.Create_priv , d.Drop_priv , d.Grant_priv , d.References_priv , d.Index_priv , d.Alter_priv , d.Create_tmp_table_priv , d.Lock_tables_priv , d.Create_view_priv , d.Show_view_priv , d.Create_routine_priv , d.Alter_routine_priv , d.Execute_priv , d.Event_priv , d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User`;"
        df = pd.read_sql_query(sql, conn)
        cursor.close()
        conn.close()
        df_users = self.fields_database(df)
        return df_users

    # Conexión a base de datos de Learning
    def connection_database_learning(self):
        conn = pymysql.connect(host=self.rds_host_moodle_learning, user=self.db_user_moodle, passwd=self.db_pass_moodle,
                               db=self.db_name_moodle_learning, port=self.db_port_moodle_learning, connect_timeout=60)
        cursor = conn.cursor()
        # Validar consulta
        sql = "SELECT u.Host as HostU ,u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU ,u.Event_priv as Event_privU ,u.Trigger_priv as Trigger_privU ,u.Create_tablespace_priv as Create_tablespace_privU,u.ssl_type as ssl_typeU ,u.ssl_cipher as ssl_cipherU ,u.x509_issuer as x509_issuerU ,u.x509_subject as x509_subjectU ,u.max_questions as max_questionsU ,u.max_updates as max_updatesU ,u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU ,u.plugin as pluginU ,u.authentication_string as authentication_stringU ,u.password_expired as password_expiredU ,u.password_last_changed as password_last_changedU ,u.password_lifetime as password_lifetimeU ,u.account_locked as account_lockedU ,u.Load_from_S3_priv as Load_from_S3_privU ,u.Select_into_S3_priv as Select_into_S3_privU ,u.Invoke_lambda_priv as Invoke_lambda_privU ,u.Invoke_sagemaker_priv as Invoke_sagemaker_privU ,u.Invoke_comprehend_priv as Invoke_comprehend_privU,d.Host ,d.Db ,d.`User` ,d.Select_priv ,d.Insert_priv ,d.Update_priv ,d.Delete_priv ,d.Create_priv ,d.Drop_priv ,d.Grant_priv ,d.References_priv ,d.Index_priv ,d.Alter_priv ,d.Create_tmp_table_priv ,d.Lock_tables_priv ,d.Create_view_priv ,d.Show_view_priv ,d.Create_routine_priv ,d.Alter_routine_priv ,d.Execute_priv ,d.Event_priv ,d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User` UNION SELECT u.Host as HostU , u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU , u.Event_priv as Event_privU , u.Trigger_priv as Trigger_privU , u.Create_tablespace_priv as Create_tablespace_privU, u.ssl_type as ssl_typeU , u.ssl_cipher as ssl_cipherU , u.x509_issuer as x509_issuerU , u.x509_subject as x509_subjectU , u.max_questions as max_questionsU , u.max_updates as max_updatesU , u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU , u.plugin as pluginU , u.authentication_string as authentication_stringU , u.password_expired as password_expiredU , u.password_last_changed as password_last_changedU , u.password_lifetime as password_lifetimeU , u.account_locked as account_lockedU , u.Load_from_S3_priv as Load_from_S3_privU , u.Select_into_S3_priv as Select_into_S3_privUl, u.Invoke_lambda_priv as Invoke_lambda_privU , u.Invoke_sagemaker_priv as Invoke_sagemaker_privU , u.Invoke_comprehend_priv as Invoke_comprehend_privU, d.Host , d.Db , d.`User` , d.Select_priv , d.Insert_priv , d.Update_priv , d.Delete_priv , d.Create_priv , d.Drop_priv , d.Grant_priv , d.References_priv , d.Index_priv , d.Alter_priv , d.Create_tmp_table_priv , d.Lock_tables_priv , d.Create_view_priv , d.Show_view_priv , d.Create_routine_priv , d.Alter_routine_priv , d.Execute_priv , d.Event_priv , d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User`;"
        df = pd.read_sql_query(sql, conn)
        cursor.close()
        conn.close()
        df_users = self.fields_database(df)
        return df_users

    # Conexión a base de datos de Adminhr
    def connection_database_adminhr(self):
        conn = pymysql.connect(host=self.rds_host_moodle_adminhr, user=self.db_user_moodle, passwd=self.db_pass_moodle,
                               db=self.db_name_moodle_adminhr, port=self.db_port_moodle_adminhr, connect_timeout=60)
        cursor = conn.cursor()
        # Validar consulta
        sql = "SELECT u.Host as HostU ,u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU ,u.Event_priv as Event_privU ,u.Trigger_priv as Trigger_privU ,u.Create_tablespace_priv as Create_tablespace_privU,u.ssl_type as ssl_typeU ,u.ssl_cipher as ssl_cipherU ,u.x509_issuer as x509_issuerU ,u.x509_subject as x509_subjectU ,u.max_questions as max_questionsU ,u.max_updates as max_updatesU ,u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU ,u.plugin as pluginU ,u.authentication_string as authentication_stringU ,d.Host ,d.Db ,d.`User` ,d.Select_priv ,d.Insert_priv ,d.Update_priv ,d.Delete_priv ,d.Create_priv ,d.Drop_priv ,d.Grant_priv ,d.References_priv ,d.Index_priv ,d.Alter_priv ,d.Create_tmp_table_priv ,d.Lock_tables_priv ,d.Create_view_priv ,d.Show_view_priv ,d.Create_routine_priv ,d.Alter_routine_priv ,d.Execute_priv ,d.Event_priv ,d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User` UNION SELECT u.Host as HostU , u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU , u.Event_priv as Event_privU , u.Trigger_priv as Trigger_privU , u.Create_tablespace_priv as Create_tablespace_privU, u.ssl_type as ssl_typeU , u.ssl_cipher as ssl_cipherU , u.x509_issuer as x509_issuerU , u.x509_subject as x509_subjectU , u.max_questions as max_questionsU , u.max_updates as max_updatesU , u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU , u.plugin as pluginU , u.authentication_string as authentication_stringU ,  d.Host , d.Db , d.`User` , d.Select_priv , d.Insert_priv , d.Update_priv , d.Delete_priv , d.Create_priv , d.Drop_priv , d.Grant_priv , d.References_priv , d.Index_priv , d.Alter_priv , d.Create_tmp_table_priv , d.Lock_tables_priv , d.Create_view_priv , d.Show_view_priv , d.Create_routine_priv , d.Alter_routine_priv , d.Execute_priv , d.Event_priv , d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User`;"
        df = pd.read_sql_query(sql, conn)
        cursor.close()
        conn.close()
        df_users = self.fields_database(df)
        return df_users

    # Validaciones y transformaciones de DataFrame Usuarios BD
    def validations(self, database):

        # Dataframe de BD
        if database == "plug":
            df_users = self.connection_database_plug()
            df_users = self.transformation(df_users)
            return df_users
        elif database == "learning":
            df_users = self.connection_database_learning()
            df_users = self.transformation(df_users)
            return df_users
        elif database == "adminhr":
            df_users = self.connection_database_adminhr()
            df_users = self.transformation(df_users)
            return df_users

    # Validaciones y transformaciones
    def transformation(self, df_users):
        df_users["HostFinal"] = np.where(
            ((df_users["Host"] == "%") | (df_users["Host"] == "localhost")),
            df_users["Host"],
            df_users["HostU"],
        )
        df_users["UserFinal"] = np.where(
            (df_users["User"].isnull), df_users["UserU"], df_users["User"]
        )

        df_users['Db'].replace([None], "Todas", inplace=True)

        df_users["Select"] = np.where(
            ((df_users["Select_priv"] == "Y") |
             (df_users["Select_priv"] == "N")),
            df_users["Select_priv"],
            df_users["Select_privU"],
        )
        df_users["Insert"] = np.where(
            ((df_users["Insert_priv"] == "Y") |
             (df_users["Insert_priv"] == "N")),
            df_users["Insert_priv"],
            df_users["Insert_privU"],
        )
        df_users["Update"] = np.where(
            ((df_users["Update_priv"] == "Y") |
             (df_users["Update_priv"] == "N")),
            df_users["Update_priv"],
            df_users["Update_privU"],
        )
        df_users["Delete"] = np.where(
            ((df_users["Delete_priv"] == "Y") |
             (df_users["Delete_priv"] == "N")),
            df_users["Delete_priv"],
            df_users["Delete_privU"],
        )
        df_users["Create"] = np.where(
            ((df_users["Create_priv"] == "Y") |
             (df_users["Create_priv"] == "N")),
            df_users["Create_priv"],
            df_users["Create_privU"],
        )
        df_users["Drop"] = np.where(
            ((df_users["Drop_priv"] == "Y") | (df_users["Drop_priv"] == "N")),
            df_users["Drop_priv"],
            df_users["Drop_privU"],
        )
        df_users["Grant"] = np.where(
            ((df_users["Grant_priv"] == "Y") |
             (df_users["Grant_priv"] == "N")),
            df_users["Grant_priv"],
            df_users["Grant_privU"],
        )
        df_users["Execute"] = np.where(
            ((df_users["Execute_priv"] == "Y") |
             (df_users["Execute_priv"] == "N")),
            df_users["Execute_priv"],
            df_users["Execute_privU"],
        )
        df_users["Index"] = np.where(
            ((df_users["Index_priv"] == "Y") |
             (df_users["Index_priv"] == "N")),
            df_users["Index_priv"],
            df_users["Index_privU"],
        )
        df_users["Alter"] = np.where(
            ((df_users["Alter_priv"] == "Y") |
             (df_users["Alter_priv"] == "N")),
            df_users["Alter_priv"],
            df_users["Alter_privU"],
        )
        df_users["Create_routine"] = np.where(
            (
                (df_users["Create_routine_priv"] == "Y")
                | (df_users["Create_routine_priv"] == "N")
            ),
            df_users["Create_routine_priv"],
            df_users["Create_routine_privU"],
        )
        df_users["Alter_routine"] = np.where(
            ((df_users["Alter_routine_priv"] == "Y") |
             (df_users["Alter_routine_priv"] == "N")),
            df_users["Alter_routine_priv"],
            df_users["Alter_routine_privU"],
        )

        df_users = df_users[
            [
                "HostFinal",
                "Db",
                "UserFinal",
                "Select",
                "Insert",
                "Update",
                "Delete",
                "Alter",
                "Create",
                "Drop",
                "Grant",
                "Execute",
                "Index",
                "Create_routine",
                "Alter_routine",
                "Create_user_privU",
            ]
        ]

        return df_users

    def current_validations(self, df_permission):
        # Transformaciones DataFrame Permisos Actuales
        df_permission["Validation"] = np.where(
            (
                (df_permission["Select"] == "Y")
                & (df_permission["Insert"] == "Y")
                & (df_permission["Update"] == "Y")
                & (df_permission["Delete"] == "Y")
                & (df_permission["Alter"] == "Y")
                & (df_permission["Create"] == "Y")
                & (df_permission["Drop"] == "Y")
                & (df_permission["Grant"] == "Y")
                & (df_permission["Execute"] == "Y")
                & (df_permission["Index"] == "Y")
                & (df_permission["Create_routine"] == "Y")
                & (df_permission["Alter_routine"] == "Y")
                & (df_permission["Create_user_privU"] == "Y")
            ),
            "Admin",
            np.where(
                (
                    (df_permission["Select"] == "Y")
                    & (df_permission["Insert"] == "N")
                    & (df_permission["Update"] == "N")
                    & (df_permission["Delete"] == "N")
                    & (df_permission["Alter"] == "N")
                    & (df_permission["Create"] == "N")
                    & (df_permission["Drop"] == "N")
                    & (df_permission["Grant"] == "N")
                    & (df_permission["Execute"] == "N")
                    & (df_permission["Index"] == "N")
                    & (df_permission["Create_routine"] == "N")
                    & (df_permission["Alter_routine"] == "N")
                    & (df_permission["Create_user_privU"] == "N")
                ),
                "Lectura",
                np.where(
                    (
                        (df_permission["Select"] == "Y")
                        & (df_permission["Insert"] == "Y")
                        & (df_permission["Update"] == "Y")
                        | (df_permission["Delete"] == "Y")
                    ),
                    "Lectura y Escritura",
                    np.where(
                        (
                            (df_permission["Select"] == "Y")
                            & (df_permission["Insert"] == "N")
                            & (df_permission["Update"] == "N")
                            & (df_permission["Delete"] == "N")
                            & (df_permission["Alter"] == "N")
                            & (df_permission["Create"] == "N")
                            & (df_permission["Drop"] == "N")
                            & (df_permission["Grant"] == "N")
                            & (df_permission["Execute"] == "N")
                            & (df_permission["Index"] == "N")
                            & (df_permission["Create_routine"] == "N")
                            & (df_permission["Alter_routine"] == "N")
                            & (df_permission["Create_user_privU"] == "Y")
                        ),
                        "Lectura y Creación Usuarios",
                        np.where(
                            (
                                (df_permission["Insert"] == "N")
                                | (df_permission["Select"] == "N")
                                & (df_permission["Update"] == "N")
                                & (df_permission["Delete"] == "N")
                                & (df_permission["Alter"] == "N")
                                & (df_permission["Create"] == "N")
                                & (df_permission["Drop"] == "N")
                                & (df_permission["Grant"] == "N")
                                & (df_permission["Execute"] == "Y")
                                & (df_permission["Index"] == "N")
                                | (df_permission["Create_routine"] == "Y")
                                | (df_permission["Alter_routine"] == "Y")
                                & (df_permission["Create_user_privU"] == "N")
                            ),
                            "Ejecución Procedimientos Almacenados",
                            np.where(
                                (
                                    (df_permission["Select"] == "N")
                                    & (df_permission["Insert"] == "Y")
                                    & (df_permission["Update"] == "N")
                                    & (df_permission["Delete"] == "N")
                                    & (df_permission["Alter"] == "N")
                                    & (df_permission["Create"] == "N")
                                    & (df_permission["Drop"] == "N")
                                    | (df_permission["Grant"] == "Y")
                                    & (df_permission["Execute"] == "N")
                                    & (df_permission["Index"] == "N")
                                    & (df_permission["Create_routine"] == "N")
                                    & (df_permission["Alter_routine"] == "N")
                                    & (df_permission["Create_user_privU"] == "Y")
                                ),
                                "Creación Usuarios",
                                np.where(
                                    (
                                        (df_permission["Select"] == "N")
                                        & (df_permission["Insert"] == "N")
                                        & (df_permission["Update"] == "N")
                                        & (df_permission["Delete"] == "N")
                                        & (df_permission["Alter"] == "N")
                                        & (df_permission["Create"] == "N")
                                        & (df_permission["Drop"] == "N")
                                        & (df_permission["Grant"] == "N")
                                        & (df_permission["Execute"] == "N")
                                        & (df_permission["Index"] == "N")
                                        & (df_permission["Create_routine"] == "N")
                                        & (df_permission["Alter_routine"] == "N")
                                        & (df_permission["Create_user_privU"] == "N")
                                    ),
                                    "Rol AWS",
                                    np.where(
                                        (
                                            (df_permission["Insert"] == "Y")
                                            & (df_permission["Select"] == "Y")
                                            & (df_permission["Update"] == "Y")
                                            & (df_permission["Delete"] == "Y")
                                            & (df_permission["Alter"] == "Y")
                                            & (df_permission["Create"] == "N")
                                            & (df_permission["Drop"] == "N")
                                            & (df_permission["Grant"] == "N")
                                            & (df_permission["Execute"] == "Y")
                                            & (df_permission["Index"] == "N")
                                            | (df_permission["Create_routine"] == "Y")
                                            | (df_permission["Alter_routine"] == "Y")
                                            & (df_permission["Create_user_privU"] == "N")
                                        ),
                                        "Lectura, Escritura y Ejecución Procedimientos Almacenados", "Otros",
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
            )
        )

        df_permission = df_permission[[
            'Usuarios', 'Tipo Usuario', 'Nombre usuario', 'Team', 'Cargo',
            'HostFinal', 'Db', 'UserFinal', 'Validation',  'Permisos Reales'
        ]]

        return df_permission
    # Lectura de permisos actuales y permisos reales desde s3
    def roles_s3(self, database):
        s3 = self.session.client("s3")
        obj = s3.get_object(Bucket=self.bucket_name, Key=self.file_name)
        df_initial = pd.read_csv(obj["Body"])
        df_permission = pd.merge(df_initial, self.validations(database),
                                 left_on='Usuarios', right_on='UserFinal', how="right")
        df_permission['Usuarios'] = np.where(
            (df_permission['Usuarios'].isnull), df_permission['UserFinal'], df_permission['Usuarios'])
        df_permission_final = self.current_validations(df_permission)
        return df_permission_final

    # Selección de campos
    def table(self, df_final):
        df_table_final = df_final[
            [
                "Usuarios",
                "name_user",
                "Tipo Usuario",
                "cargo_usuario",
                "Team",
                "Db",
                "Validation",
                "Permisos Reales",
                "user_delete",
                "Comments",
            ]
        ]
        # Renombrar columnas de Dataframe
        df_table_final.rename(
            columns={
                "Usuarios": "Usuario",
                "name_user": "Nombre Usuario",
                "cargo_usuario": "Cargo",
                "Db": "Base de Datos",
                "Validation": "Permisos Actuales",
                "Permisos Reales": "Permisos de Rol",
                "user_delete": "Eliminación Usuario",
                "Comments": "Acciones",
            },
            inplace=True,
        )
        return df_table_final

    # Tabla final
    def table_final(self, df_roles, df_users):
        df_final = pd.merge(
            df_roles, df_users, left_on='Usuarios', right_on='username', how='left')
        df_final["user_delete"] = np.where(
            ((df_final["username"].isnull()) &
             (df_final["Tipo Usuario"] == "Personal")),
            "SI",
            "NO",
        )
        df_final["Comments"] = np.where(
            ((df_final["Tipo Usuario"] == "Aplicación")),
            "OK",
            np.where(
                ((df_final["Validation"] == df_final["Permisos Reales"])
                 ),
                "OK",
                "Cambiar permisos",
            ),
        )
        df_final["name_user"] = np.where(
            df_final['name'].isnull(), df_final['Nombre usuario'], df_final['name'])
        df_final['cargo_usuario'] = np.where(
            (df_final["Tipo Usuario"] == "Aplicación"), "Usuario aplicación", df_final['title'])

        df_table_final = self.table(df_final)
        return df_table_final

    # Subir dataframe a s3 en formato csv
    def csv_s3(self, df_final, file_name):
        s3 = self.session.client("s3")
        csv_buf = StringIO()
        file = df_final.to_csv(csv_buf,header=True,index=False)
        csv_buf.seek(0)
        fecha = str(datetime.datetime.now().strftime('%Y-%m-%d'))
        try:
            s3.put_object(Bucket = self.bucket_name, Body = csv_buf.getvalue(), Key = file_name+fecha+".csv")
            #s3.upload_file(file, self.bucket_name, file_name+fecha+".csv")
            return print("Se subió correctamente el archivo a" + file_name)
        except ClientError as e:
            logging.error(e)
            return print("Hubo un error")