SELECT defaclobjtype, n.nspname AS schema, r.rolname AS grantor, d.defaclacl
FROM pg_default_acl d
JOIN pg_roles r ON r.oid = d.defaclrole
LEFT JOIN pg_namespace n ON n.oid = d.defaclnamespace
WHERE d.defaclacl::text LIKE '%role_a%';

SELECT r.rolname
FROM pg_auth_members m
JOIN pg_roles r ON m.roleid = r.oid
WHERE m.member = (SELECT oid FROM pg_roles WHERE rolname = CURRENT_USER);

SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public'
  AND table_name = 'mytable'
  AND grantee IN (CURRENT_USER, 'PUBLIC');


SELECT r.usename AS grantor,
       e.usename AS grantee,
       nspname,
       privilege_type,
       is_grantable
  FROM pg_namespace
JOIN LATERAL (SELECT *
                FROM aclexplode(nspacl) AS x) a
          ON true
        JOIN pg_user e
          ON a.grantee = e.usesysid
        JOIN pg_user r
          ON a.grantor = r.usesysid 
       WHERE e.usename = 'YOUR_USER';
