SELECT defaclobjtype, n.nspname AS schema, r.rolname AS grantor, d.defaclacl
FROM pg_default_acl d
JOIN pg_roles r ON r.oid = d.defaclrole
LEFT JOIN pg_namespace n ON n.oid = d.defaclnamespace
WHERE d.defaclacl::text LIKE '%role_a%';
