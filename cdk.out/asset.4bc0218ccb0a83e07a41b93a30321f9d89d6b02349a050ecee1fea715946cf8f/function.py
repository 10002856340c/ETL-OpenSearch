import requests
import pandas as pd
import json
import numpy as np
import pyodbc
import pandas.io.sql as psql
import sshtunnel
import mysql.connector
import mariadb
import boto3
import pymysql
from pandas import json_normalize
from pandas import DataFrame
import os

class Main:
    def __init__(self):
        self.token = "DQVJ1LUZAiTnEzWTQ4R0EzcS1jRnNOQjZAwVFVuUVJJd21hUzNhYzhlREdkNlJsR29GT2lOQUhQd0dnNlhwc0VueXNfV092T19vcm5zZAkRuZAWpfc3NnYXNUd1UtQ3dxN1JMek5YeHhtQnJsUlY1Q05VS0diNlNZAZAWdzNHpncDZAxOGtGMzRtcWtoMUhxazdPZAy1FLUxzTEhiMU9WZAWNESzBiYi1rYlNqT3BlVlpPc0NhTmRFeUNHTTd5VXd0N1l4bFFuajFiSUlR%0A"
        self.id_tech = "284719169503437"
        self.limit = "20000"
        self.fields = "id,first_name,last_name,name,title,email,department"
        self.rds_host_moodle = 'localhost'
        self.db_user_moodle = 'psabogal'
        self.db_pass_moodle = 'jWAj8vJ8HI97'
        self.db_name_moodle = 'bitnami_uplug'
        self.db_port_moodle = int(8082)

        self.session = boto3.Session(
            aws_access_key_id="ASIASUBAG3E3NDV3D5U5",
            aws_secret_access_key="z7HnfI+7UceJQvlv7uHAOSOG84N4B5XBzTfdwoTE",
            aws_session_token="IQoJb3JpZ2luX2VjEFUaCXVzLWVhc3QtMSJGMEQCIBfbI8tMH6BSl/+d41b4noB53TMXvrJbVlkcEb8V2Vd1AiAo8RHX6cRD0Z5dTLCf87JgNebDkcxK9MeQu78x27hsgyqUAwiu//////////8BEAEaDDE4MDQ1NjE4NDExOCIMWzMXA0xGcve/SjrdKugCY4I3Ru/760SXaevxBS1mGL//NKxgZpPepHpQlpJXDzM9nemeXUnvj6twN16DzTmmwy+S5RgTfqbebC8GJDkJZm/1SjEUzWwikv5rSawy5GKARVObyyErhXCtIIHNusRQV1YJaHnBf97CaMutPHVlNnFFnWuAf9cQgaG0BGoZFlbKsU2cO3iVUwBNlIxb5lxujEuRTbX6BGHfrDjj6paxk0efg8ViBWnw5uT891lA0r/F6beNwe0nZcMTJ2FkO3Zl20ad44XWiGeyhB6VacYppOaFdh/qTaYBoE36keC30W8HoKGFPn2OinFmsEZZg/7PX8ZbVNQKK5rYQ8nHN51JPkhqklIlBn4WvPe3CwjtQBYafqry7wBNMALbUB+9yzrkFu+YPT4f3Fr5byxKBS66oHlqK6kC1Qs8fZP4FrUSuiJ0ZWJ7zhMDKaBhFjLUSXgNmBPhwKInWDUChos8A2QWYapc2+6hWd03MLK//J0GOqcBIUAX5MdwTwU/yBFPy0LLTYKW4E76q8uxJmY9s6yvVqq+fj0vgRl0P1sP3sylAPfX5At0eATsJNMVnccGoGa6smGu+EEUDPFIXTCZHCtHH1aMIqYUgcb4ykGpmmg72ak27IpguhSlGSGzxkYpo0j+OyETsbsVWGhamkPIDRW8uD7KUco63AxwHdjCp9TGzPQu7mcijZS4D1FXj6rdT+y9/B/oFhxzUmo=",
            region_name="us-east-1")

    # Lista de usuarios en Workplace
    def users_workplace(self):
        url = f"https://graph.facebook.com/v15.0/{self.id_tech}/members?access_token={self.token}&limit={self.limit}&fields={self.fields}"
        response = requests.request("GET", url, headers={}, data={})
        json_data = json.loads(response.text)

        # Creación de DataFrame usuarios workplace
        df_members = pd.json_normalize(json_data["data"])
        df_members = df_members.assign(
            username=(df_members["email"].str.split("@", n=1, expand=True))[0]
        )
        df_members = df_members[["name", "title", "username"]]
        return df_members

    # Conexión a bases de datos Test
    def connection_database(self):
        conn = pymysql.connect(host=self.rds_host_moodle, user=self.db_user_moodle, passwd=self.db_pass_moodle,
                               db=self.db_name_moodle, port=self.db_port_moodle, connect_timeout=60)
        cursor = conn.cursor()
        # Validar consulta
        sql = "SELECT u.Host as HostU ,u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU ,u.Event_priv as Event_privU ,u.Trigger_priv as Trigger_privU ,u.Create_tablespace_priv as Create_tablespace_privU,u.ssl_type as ssl_typeU ,u.ssl_cipher as ssl_cipherU ,u.x509_issuer as x509_issuerU ,u.x509_subject as x509_subjectU ,u.max_questions as max_questionsU ,u.max_updates as max_updatesU ,u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU ,u.plugin as pluginU ,u.authentication_string as authentication_stringU ,d.Host ,d.Db ,d.`User` ,d.Select_priv ,d.Insert_priv ,d.Update_priv ,d.Delete_priv ,d.Create_priv ,d.Drop_priv ,d.Grant_priv ,d.References_priv ,d.Index_priv ,d.Alter_priv ,d.Create_tmp_table_priv ,d.Lock_tables_priv ,d.Create_view_priv ,d.Show_view_priv ,d.Create_routine_priv ,d.Alter_routine_priv ,d.Execute_priv ,d.Event_priv ,d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User` UNION SELECT u.Host as HostU , u.`User` as UserU ,u.Select_priv as Select_privU ,u.Insert_priv as Insert_privU ,u.Update_priv as Update_privU ,u.Delete_priv as Delete_privU ,u.Create_priv as Create_privU ,u.Drop_priv as Drop_privU ,u.Reload_priv as Reload_privU ,u.Shutdown_priv as Shutdown_privU ,u.Process_priv as Process_privU ,u.File_priv as File_privU ,u.Grant_priv as Grant_privU ,u.References_priv as References_privU ,u.Index_priv as Index_privU ,u.Alter_priv as Alter_privU ,u.Show_db_priv as Show_db_privU ,u.Super_priv as Super_privU ,u.Create_tmp_table_priv as Create_tmp_table_privU ,u.Lock_tables_priv as Lock_tables_privU ,u.Execute_priv as Execute_privU ,u.Repl_slave_priv as Repl_slave_privU ,u.Repl_client_priv as Repl_client_privU ,u.Create_view_priv as Create_view_privU ,u.Show_view_priv as Show_view_privU ,u.Create_routine_priv as Create_routine_privU ,u.Alter_routine_priv as Alter_routine_privU ,u.Create_user_priv as Create_user_privU , u.Event_priv as Event_privU , u.Trigger_priv as Trigger_privU , u.Create_tablespace_priv as Create_tablespace_privU, u.ssl_type as ssl_typeU , u.ssl_cipher as ssl_cipherU , u.x509_issuer as x509_issuerU , u.x509_subject as x509_subjectU , u.max_questions as max_questionsU , u.max_updates as max_updatesU , u.max_connections as max_connectionsU ,u.max_user_connections as max_user_connectionsU , u.plugin as pluginU , u.authentication_string as authentication_stringU ,  d.Host , d.Db , d.`User` , d.Select_priv , d.Insert_priv , d.Update_priv , d.Delete_priv , d.Create_priv , d.Drop_priv , d.Grant_priv , d.References_priv , d.Index_priv , d.Alter_priv , d.Create_tmp_table_priv , d.Lock_tables_priv , d.Create_view_priv , d.Show_view_priv , d.Create_routine_priv , d.Alter_routine_priv , d.Execute_priv , d.Event_priv , d.Trigger_priv FROM mysql.`user` u LEFT JOIN mysql.db d ON u.`User` = d.`User`;"
        df = pd.read_sql_query(sql, conn)
        cursor.close()
        conn.close()
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

    # Validaciones y transformaciones de DataFrame Usuarios BD
    def validations(self):

        # Dataframe de BD
        df_users = self.connection_database()
        # Validaciones y transformaciones
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

    def roles_s3(self):
        s3 = self.session.client("s3")
        bucket_name = "ubits-test-databases"
        file_name = "RolesTest.csv"
        obj = s3.get_object(Bucket=bucket_name, Key=file_name)
        df_initial = pd.read_csv(obj["Body"])
        df_permission = pd.merge(df_initial, self.validations(),
                                 left_on='Usuarios', right_on='UserFinal')

        df_permission_final = self.current_validations(df_permission)
        return df_permission_final

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