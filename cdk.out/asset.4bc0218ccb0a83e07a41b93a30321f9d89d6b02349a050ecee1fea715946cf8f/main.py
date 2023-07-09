import main
import pandas as pd

main_functions = main.Main()

# Consulta de miembros en workplace
df_workplace = main_functions.users_workplace()
df_roles = main_functions.roles_s3()

# Tabla final de usuarios vs permisos
df_validations = main_functions.table_final(
    df_roles, df_workplace)

print(df_validations)