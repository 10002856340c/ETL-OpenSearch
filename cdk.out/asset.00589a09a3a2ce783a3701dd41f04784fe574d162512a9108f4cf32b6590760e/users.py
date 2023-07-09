import main

main_functions = main.Main()

# Consulta de miembros en workplace
df_workplace = main_functions.users_workplace()

# Permisos reales vs permisos actuales de:
#Plug
df_roles_plug = main_functions.roles_s3("plug")
#Learning
df_roles_learning = main_functions.roles_s3("learning")
# #Adminhr
df_roles_adminhr = main_functions.roles_s3("adminhr")

# Tabla final de usuarios vs permisos
df_validations_plug = main_functions.table_final(
    df_roles_plug, df_workplace)

df_validations_learning =  main_functions.table_final(
    df_roles_learning, df_workplace)

df_validations_adminhr =  main_functions.table_final(
    df_roles_adminhr, df_workplace)

#Subir tablas a s3
main_functions.csv_s3(df_validations_plug, "plug_database/users_plug")
main_functions.csv_s3(df_validations_learning, "learning_database/users_learning")
main_functions.csv_s3(df_validations_adminhr, "admin_database/users_admihr")