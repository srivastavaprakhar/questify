from llama_index.core.schema import Document
import sqlite3

def get_foreign_keys(cursor, table_name):
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    return cursor.fetchall()

def get_sqlite_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]
    documents = []

    for table_name in tables:
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]
            foreign_keys = get_foreign_keys(cursor, table_name)

            for row in rows:
                row_data = dict(zip(col_names, row))
                field_lines = []

                for col in col_names:
                    val = row_data.get(col)
                    if val is not None and str(val).strip():
                        field_lines.append(f"{col.replace('_', ' ').capitalize()}: {val}")

                # Inject FK join summary (only 1-2 fields max)
                for fk in foreign_keys:
                    from_col, ref_table, to_col = fk[3], fk[2], fk[4]
                    fk_val = row_data.get(from_col)
                    if fk_val:
                        try:
                            cursor.execute(f"SELECT * FROM {ref_table} WHERE {to_col} = ?", (fk_val,))
                            join_row = cursor.fetchone()
                            if join_row:
                                join_col_names = [desc[0] for desc in cursor.description]
                                join_data = dict(zip(join_col_names, join_row))
                                for jcol, jval in list(join_data.items())[:2]:
                                    if jval:
                                        field_lines.append(f"{jcol.replace('_', ' ').capitalize()} (from {ref_table}): {jval}")
                        except Exception as e:
                            print(f"[!] FK join failed: {e}")

                doc_text = f"Record from {table_name} table:\n" + "\n".join(field_lines)
                documents.append(Document(text=doc_text, metadata={"table": table_name}))

        except Exception as e:
            print(f"[!] Error reading table '{table_name}': {e}")
            continue

    conn.close()
    return documents
