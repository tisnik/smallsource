from storage_interface import create_connection, select_all_ecosystems

connection = create_connection("../workdir/smallsource.db")
select_all_ecosystems(connection)
