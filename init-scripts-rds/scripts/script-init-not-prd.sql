DO $$
BEGIN
    EXECUTE format('CREATE SCHEMA IF NOT EXISTS %I', current_database());
END $$;

-- criar roles de AD
DO $$
BEGIN
CREATE ROLE rl_ad WITH
	NOLOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION;
EXCEPTION WHEN duplicate_object THEN RAISE NOTICE '%, moving to next statement', SQLERRM USING ERRCODE = SQLSTATE;
END
$$;

DO $$
BEGIN
CREATE ROLE rl_ad_select WITH
	NOLOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION;
EXCEPTION WHEN duplicate_object THEN RAISE NOTICE '%, moving to next statement', SQLERRM USING ERRCODE = SQLSTATE;
END
$$;

-- criar usuarios time AD e inseri-los nas roles
DO $$
BEGIN
CREATE ROLE useradmin WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	CONNECTION LIMIT -1
	PASSWORD '';

EXCEPTION WHEN duplicate_object THEN RAISE NOTICE '%, moving to next statement', SQLERRM USING ERRCODE = SQLSTATE;
END
$$;

-- criar roles de auditoria
DO $$
BEGIN
CREATE ROLE rl_auditoria_select WITH
    NOLOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION;
EXCEPTION WHEN duplicate_object THEN RAISE NOTICE '%, moving to next statement', SQLERRM USING ERRCODE = SQLSTATE;
END
$$;

-- criar usuario de auditoria
DO $$
BEGIN
CREATE ROLE useraudit WITH
    LOGIN
    NOSUPERUSER
    NOCREATEDB
    NOCREATEROLE
    INHERIT
    NOREPLICATION
    CONNECTION LIMIT -1
    PASSWORD '';

EXCEPTION WHEN duplicate_object THEN RAISE NOTICE '%, moving to next statement', SQLERRM USING ERRCODE = SQLSTATE;
END
$$;

-- conceder grants de criacao, acesso, insercao e uso a roles de AD

GRANT rl_ad TO useraudit;
GRANT rl_ad_select TO useraudit;
GRANT rl_auditoria_select TO useraudit;
DO $$
DECLARE
    schema_name text := current_database();
BEGIN
    -- Conceder permissões ao usuário 'rl_ad'
    EXECUTE format('GRANT CREATE ON SCHEMA %I TO rl_ad', schema_name);
    EXECUTE format('GRANT INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO rl_ad WITH GRANT OPTION', schema_name);
    EXECUTE format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %I TO rl_ad WITH GRANT OPTION', schema_name);
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO rl_ad WITH GRANT OPTION', schema_name);
 
    -- Conceder permissões ao usuário 'rl_ad_select'
    EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO rl_ad_select WITH GRANT OPTION', schema_name);
    EXECUTE format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %I TO rl_ad_select', schema_name);
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO rl_ad_select', schema_name);
 
    -- Conceder permissões ao usuário 'RL_AUDITORIA_SELECT'
    EXECUTE format('GRANT SELECT ON ALL TABLES IN SCHEMA %I TO rl_auditoria_select', schema_name);
    EXECUTE format('GRANT USAGE ON SCHEMA %I TO rl_auditoria_select', schema_name);
END $$;