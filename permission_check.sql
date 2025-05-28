SELECT 
    r.rolname AS user_name,
    n.nspname AS schema_name,
    c.relname AS object_name,
    c.relkind AS object_type,
    has_select_privilege(r.rolname, c.oid) AS can_select,
    has_insert_privilege(r.rolname, c.oid) AS can_insert,
    has_update_privilege(r.rolname, c.oid) AS can_update,
    has_delete_privilege(r.rolname, c.oid) AS can_delete
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
JOIN pg_roles r ON r.rolname = 'your_user' -- << replace with the actual role/user
WHERE c.relname = 'my_materialized_view'   -- << replace with your materialized view name
  AND c.relkind = 'm';                     -- 'm' = materialized view
