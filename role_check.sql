Check default privileges referencing role_a:

SELECT *
FROM pg_default_acl
WHERE defaclrole = 'role_a'::regrole
   OR defacluser = 'role_a'::regrole;


If present, remove them:

ALTER DEFAULT PRIVILEGES FOR ROLE kyc_admin IN SCHEMA test3 REVOKE ALL ON TABLES FROM role_a;
ALTER DEFAULT PRIVILEGES FOR ROLE kyc_admin IN SCHEMA test3 REVOKE ALL ON SEQUENCES FROM role_a;
ALTER DEFAULT PRIVILEGES FOR ROLE kyc_admin IN SCHEMA test3 REVOKE ALL ON FUNCTIONS FROM role_a;


Drop any ownership references:

REASSIGN OWNED BY role_a TO kyc_admin;
DROP OWNED BY role_a;


Drop the role:

DROP ROLE role_a;


If step 2 fails, manually inspect using:

\ddp  -- in psql, shows default privileges


Confirm all entries mentioning role_a are cleared before dropping.
