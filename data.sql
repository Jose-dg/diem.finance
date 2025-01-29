--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+2)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY "public"."token_blacklist_outstandingtoken" DROP CONSTRAINT IF EXISTS "token_blacklist_outs_user_id_83bc629a_fk_auth_user";
ALTER TABLE IF EXISTS ONLY "public"."token_blacklist_blacklistedtoken" DROP CONSTRAINT IF EXISTS "token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_refreshtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_refreshtoken_user_id_da837fce_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_refreshtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_refreshtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_idtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_idtoken_user_id_dd512b59_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_idtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_grant" DROP CONSTRAINT IF EXISTS "oauth2_provider_grant_user_id_e8f62af8_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_grant" DROP CONSTRAINT IF EXISTS "oauth2_provider_gran_application_id_81923564_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_application" DROP CONSTRAINT IF EXISTS "oauth2_provider_application_user_id_79829054_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_accesstoken_user_id_6e4c9a65_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_user_permissions" DROP CONSTRAINT IF EXISTS "fintech_user_user_pe_user_id_5b840db9_fk_fintech_u";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_user_permissions" DROP CONSTRAINT IF EXISTS "fintech_user_user_pe_permission_id_ca4b8a5c_fk_auth_perm";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_role_id_45d07174_fk_fintech_role_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_phone_1_id_2077fbe4_fk_fintech_phonenumber_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_label_id_5129caf1_fk_fintech_label_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_groups" DROP CONSTRAINT IF EXISTS "fintech_user_groups_user_id_15fdbb30_fk_fintech_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_groups" DROP CONSTRAINT IF EXISTS "fintech_user_groups_group_id_18bcab92_fk_auth_group_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_document_id_f52d8362_fk_fintech_identifier_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_country_id_90ed5849_fk_fintech_country_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_city_id_f6cec28d_fk_fintech_paramslocation_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_transaction" DROP CONSTRAINT IF EXISTS "fintech_transaction_user_id_7a424d2c_fk_fintech_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_transaction" DROP CONSTRAINT IF EXISTS "fintech_transaction_category_id_e09c657c_fk_fintech_s";
ALTER TABLE IF EXISTS ONLY "public"."fintech_subcategory" DROP CONSTRAINT IF EXISTS "fintech_subcategory_category_id_50f7bc8f_fk_fintech_category_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_seller" DROP CONSTRAINT IF EXISTS "fintech_seller_user_id_168b245a_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_seller" DROP CONSTRAINT IF EXISTS "fintech_seller_role_id_f00a0466_fk_fintech_role_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_phonenumber" DROP CONSTRAINT IF EXISTS "fintech_phonenumber_country_related_id_5dbe9007_fk_fintech_c";
ALTER TABLE IF EXISTS ONLY "public"."fintech_identifier" DROP CONSTRAINT IF EXISTS "fintech_identifier_document_type_id_f348b6c7_fk_fintech_d";
ALTER TABLE IF EXISTS ONLY "public"."fintech_identifier" DROP CONSTRAINT IF EXISTS "fintech_identifier_country_id_355176a7_fk_fintech_country_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_expense" DROP CONSTRAINT IF EXISTS "fintech_expense_user_id_df173b21_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_expense" DROP CONSTRAINT IF EXISTS "fintech_expense_subcategory_id_e6c7e1f6_fk_fintech_s";
ALTER TABLE IF EXISTS ONLY "public"."fintech_expense" DROP CONSTRAINT IF EXISTS "fintech_expense_registered_by_id_6cd6d3d2_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_expense" DROP CONSTRAINT IF EXISTS "fintech_expense_account_id_84b59e55_fk_fintech_a";
ALTER TABLE IF EXISTS ONLY "public"."fintech_documenttype" DROP CONSTRAINT IF EXISTS "fintech_documenttype_country_id_id_0b6af4b2_fk_fintech_c";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_user_id_8f2f3be3_fk_fintech_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_subcategory_id_4e4ac2ca_fk_fintech_s";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_seller_id_c3d4f145_fk_fintech_seller_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_registered_by_id_5c849d88_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_periodicity_id_6f6a311a_fk_fintech_p";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_payment_id_62803c60_fk_fintech_a";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_currency_id_b12e7221_fk_fintech_currency_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_category" DROP CONSTRAINT IF EXISTS "fintech_category_category_type_id_8c2a931a_fk_fintech_c";
ALTER TABLE IF EXISTS ONLY "public"."fintech_address" DROP CONSTRAINT IF EXISTS "fintech_address_user_id_b141579e_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_address" DROP CONSTRAINT IF EXISTS "fintech_address_country_id_e50a90ec_fk_fintech_country_id";
ALTER TABLE IF EXISTS ONLY "public"."fintech_accountmethodamount" DROP CONSTRAINT IF EXISTS "fintech_accountmetho_transaction_id_962ad92f_fk_fintech_t";
ALTER TABLE IF EXISTS ONLY "public"."fintech_accountmethodamount" DROP CONSTRAINT IF EXISTS "fintech_accountmetho_payment_method_id_6a28ff5a_fk_fintech_a";
ALTER TABLE IF EXISTS ONLY "public"."fintech_accountmethodamount" DROP CONSTRAINT IF EXISTS "fintech_accountmetho_currency_id_088ff444_fk_fintech_c";
ALTER TABLE IF EXISTS ONLY "public"."fintech_accountmethodamount" DROP CONSTRAINT IF EXISTS "fintech_accountmetho_credit_id_c52a4a9c_fk_fintech_c";
ALTER TABLE IF EXISTS ONLY "public"."fintech_account" DROP CONSTRAINT IF EXISTS "fintech_account_currency_id_dcd5160a_fk_fintech_currency_id";
ALTER TABLE IF EXISTS ONLY "public"."django_admin_log" DROP CONSTRAINT IF EXISTS "django_admin_log_user_id_c564eba6_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."django_admin_log" DROP CONSTRAINT IF EXISTS "django_admin_log_content_type_id_c4bce8eb_fk_django_co";
ALTER TABLE IF EXISTS ONLY "public"."authtoken_token" DROP CONSTRAINT IF EXISTS "authtoken_token_user_id_35299eff_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_user_permissions" DROP CONSTRAINT IF EXISTS "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_user_permissions" DROP CONSTRAINT IF EXISTS "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_groups" DROP CONSTRAINT IF EXISTS "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_groups" DROP CONSTRAINT IF EXISTS "auth_user_groups_group_id_97559544_fk_auth_group_id";
ALTER TABLE IF EXISTS ONLY "public"."auth_permission" DROP CONSTRAINT IF EXISTS "auth_permission_content_type_id_2f476e4b_fk_django_co";
ALTER TABLE IF EXISTS ONLY "public"."auth_group_permissions" DROP CONSTRAINT IF EXISTS "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id";
ALTER TABLE IF EXISTS ONLY "public"."auth_group_permissions" DROP CONSTRAINT IF EXISTS "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm";
DROP INDEX IF EXISTS "public"."token_blacklist_outstandingtoken_user_id_83bc629a";
DROP INDEX IF EXISTS "public"."token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like";
DROP INDEX IF EXISTS "public"."oauth2_provider_refreshtoken_user_id_da837fce";
DROP INDEX IF EXISTS "public"."oauth2_provider_refreshtoken_application_id_2d1c311b";
DROP INDEX IF EXISTS "public"."oauth2_provider_idtoken_user_id_dd512b59";
DROP INDEX IF EXISTS "public"."oauth2_provider_idtoken_application_id_08c5ff4f";
DROP INDEX IF EXISTS "public"."oauth2_provider_grant_user_id_e8f62af8";
DROP INDEX IF EXISTS "public"."oauth2_provider_grant_code_49ab4ddf_like";
DROP INDEX IF EXISTS "public"."oauth2_provider_grant_application_id_81923564";
DROP INDEX IF EXISTS "public"."oauth2_provider_application_user_id_79829054";
DROP INDEX IF EXISTS "public"."oauth2_provider_application_client_secret_53133678_like";
DROP INDEX IF EXISTS "public"."oauth2_provider_application_client_secret_53133678";
DROP INDEX IF EXISTS "public"."oauth2_provider_application_client_id_03f0cc84_like";
DROP INDEX IF EXISTS "public"."oauth2_provider_accesstoken_user_id_6e4c9a65";
DROP INDEX IF EXISTS "public"."oauth2_provider_accesstoken_token_checksum_85319a26_like";
DROP INDEX IF EXISTS "public"."oauth2_provider_accesstoken_application_id_b22886e1";
DROP INDEX IF EXISTS "public"."fintech_user_username_1d15bc5f_like";
DROP INDEX IF EXISTS "public"."fintech_user_user_permissions_user_id_5b840db9";
DROP INDEX IF EXISTS "public"."fintech_user_user_permissions_permission_id_ca4b8a5c";
DROP INDEX IF EXISTS "public"."fintech_user_role_id_45d07174";
DROP INDEX IF EXISTS "public"."fintech_user_phone_1_id_2077fbe4";
DROP INDEX IF EXISTS "public"."fintech_user_label_id_5129caf1";
DROP INDEX IF EXISTS "public"."fintech_user_groups_user_id_15fdbb30";
DROP INDEX IF EXISTS "public"."fintech_user_groups_group_id_18bcab92";
DROP INDEX IF EXISTS "public"."fintech_user_document_id_f52d8362";
DROP INDEX IF EXISTS "public"."fintech_user_country_id_90ed5849";
DROP INDEX IF EXISTS "public"."fintech_user_city_id_f6cec28d";
DROP INDEX IF EXISTS "public"."fintech_transaction_user_id_7a424d2c";
DROP INDEX IF EXISTS "public"."fintech_transaction_category_id_e09c657c";
DROP INDEX IF EXISTS "public"."fintech_subcategory_category_id_50f7bc8f";
DROP INDEX IF EXISTS "public"."fintech_seller_role_id_f00a0466";
DROP INDEX IF EXISTS "public"."fintech_role_name_52d8e08d_like";
DROP INDEX IF EXISTS "public"."fintech_phonenumber_country_related_id_5dbe9007";
DROP INDEX IF EXISTS "public"."fintech_identifier_document_type_id_f348b6c7";
DROP INDEX IF EXISTS "public"."fintech_identifier_document_number_d8e74d5c_like";
DROP INDEX IF EXISTS "public"."fintech_identifier_country_id_355176a7";
DROP INDEX IF EXISTS "public"."fintech_expense_user_id_df173b21";
DROP INDEX IF EXISTS "public"."fintech_expense_registered_by_id_6cd6d3d2";
DROP INDEX IF EXISTS "public"."fintech_expense_category_id_8e608b51";
DROP INDEX IF EXISTS "public"."fintech_expense_account_id_84b59e55";
DROP INDEX IF EXISTS "public"."fintech_documenttype_country_id_id_0b6af4b2";
DROP INDEX IF EXISTS "public"."fintech_documenttype_code_d7ceaafb_like";
DROP INDEX IF EXISTS "public"."fintech_credit_user_id_8f2f3be3";
DROP INDEX IF EXISTS "public"."fintech_credit_subcategory_id_4e4ac2ca";
DROP INDEX IF EXISTS "public"."fintech_credit_seller_id_c3d4f145";
DROP INDEX IF EXISTS "public"."fintech_credit_registered_by_id_5c849d88";
DROP INDEX IF EXISTS "public"."fintech_credit_periodicity_id_6f6a311a";
DROP INDEX IF EXISTS "public"."fintech_credit_payment_id_62803c60";
DROP INDEX IF EXISTS "public"."fintech_credit_currency_id_b12e7221";
DROP INDEX IF EXISTS "public"."fintech_categorytype_name_b89ce7d3_like";
DROP INDEX IF EXISTS "public"."fintech_category_category_type_id_8c2a931a";
DROP INDEX IF EXISTS "public"."fintech_address_user_id_b141579e";
DROP INDEX IF EXISTS "public"."fintech_address_country_id_e50a90ec";
DROP INDEX IF EXISTS "public"."fintech_accountmethodamount_transaction_id_962ad92f";
DROP INDEX IF EXISTS "public"."fintech_accountmethodamount_payment_method_id_6a28ff5a";
DROP INDEX IF EXISTS "public"."fintech_accountmethodamount_payment_code_df824755_like";
DROP INDEX IF EXISTS "public"."fintech_accountmethodamount_currency_id_088ff444";
DROP INDEX IF EXISTS "public"."fintech_accountmethodamount_credit_id_c52a4a9c";
DROP INDEX IF EXISTS "public"."fintech_account_currency_id_dcd5160a";
DROP INDEX IF EXISTS "public"."django_session_session_key_c0390e0f_like";
DROP INDEX IF EXISTS "public"."django_session_expire_date_a5c62663";
DROP INDEX IF EXISTS "public"."django_admin_log_user_id_c564eba6";
DROP INDEX IF EXISTS "public"."django_admin_log_content_type_id_c4bce8eb";
DROP INDEX IF EXISTS "public"."authtoken_token_key_10f0b77e_like";
DROP INDEX IF EXISTS "public"."auth_user_username_6821ab7c_like";
DROP INDEX IF EXISTS "public"."auth_user_user_permissions_user_id_a95ead1b";
DROP INDEX IF EXISTS "public"."auth_user_user_permissions_permission_id_1fbb5f2c";
DROP INDEX IF EXISTS "public"."auth_user_groups_user_id_6a12ed8b";
DROP INDEX IF EXISTS "public"."auth_user_groups_group_id_97559544";
DROP INDEX IF EXISTS "public"."auth_permission_content_type_id_2f476e4b";
DROP INDEX IF EXISTS "public"."auth_group_permissions_permission_id_84c5c92e";
DROP INDEX IF EXISTS "public"."auth_group_permissions_group_id_b120cbf9";
DROP INDEX IF EXISTS "public"."auth_group_name_a6ea08ec_like";
ALTER TABLE IF EXISTS ONLY "public"."token_blacklist_outstandingtoken" DROP CONSTRAINT IF EXISTS "token_blacklist_outstandingtoken_pkey";
ALTER TABLE IF EXISTS ONLY "public"."token_blacklist_outstandingtoken" DROP CONSTRAINT IF EXISTS "token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq";
ALTER TABLE IF EXISTS ONLY "public"."token_blacklist_blacklistedtoken" DROP CONSTRAINT IF EXISTS "token_blacklist_blacklistedtoken_token_id_key";
ALTER TABLE IF EXISTS ONLY "public"."token_blacklist_blacklistedtoken" DROP CONSTRAINT IF EXISTS "token_blacklist_blacklistedtoken_pkey";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_refreshtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_refreshtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_refreshtoken_pkey";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_refreshtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_refreshtoken_access_token_id_key";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_idtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_idtoken_pkey";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_idtoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_idtoken_jti_key";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_grant" DROP CONSTRAINT IF EXISTS "oauth2_provider_grant_pkey";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_grant" DROP CONSTRAINT IF EXISTS "oauth2_provider_grant_code_key";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_application" DROP CONSTRAINT IF EXISTS "oauth2_provider_application_pkey";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_application" DROP CONSTRAINT IF EXISTS "oauth2_provider_application_client_id_key";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_accesstoken_token_checksum_85319a26_uniq";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_accesstoken_source_refresh_token_id_key";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_accesstoken_pkey";
ALTER TABLE IF EXISTS ONLY "public"."oauth2_provider_accesstoken" DROP CONSTRAINT IF EXISTS "oauth2_provider_accesstoken_id_token_id_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_username_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_user_permissions" DROP CONSTRAINT IF EXISTS "fintech_user_user_permissions_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_user_permissions" DROP CONSTRAINT IF EXISTS "fintech_user_user_permis_user_id_permission_id_a21e5774_uniq";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user" DROP CONSTRAINT IF EXISTS "fintech_user_id_user_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_groups" DROP CONSTRAINT IF EXISTS "fintech_user_groups_user_id_group_id_03e1aeef_uniq";
ALTER TABLE IF EXISTS ONLY "public"."fintech_user_groups" DROP CONSTRAINT IF EXISTS "fintech_user_groups_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_transaction" DROP CONSTRAINT IF EXISTS "fintech_transaction_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_transaction" DROP CONSTRAINT IF EXISTS "fintech_transaction_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_subcategory" DROP CONSTRAINT IF EXISTS "fintech_subcategory_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_subcategory" DROP CONSTRAINT IF EXISTS "fintech_subcategory_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_seller" DROP CONSTRAINT IF EXISTS "fintech_seller_user_id_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_seller" DROP CONSTRAINT IF EXISTS "fintech_seller_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_role" DROP CONSTRAINT IF EXISTS "fintech_role_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_role" DROP CONSTRAINT IF EXISTS "fintech_role_name_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_phonenumber" DROP CONSTRAINT IF EXISTS "fintech_phonenumber_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_periodicity" DROP CONSTRAINT IF EXISTS "fintech_periodicity_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_paramslocation" DROP CONSTRAINT IF EXISTS "fintech_paramslocation_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_language" DROP CONSTRAINT IF EXISTS "fintech_language_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_label" DROP CONSTRAINT IF EXISTS "fintech_label_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_label" DROP CONSTRAINT IF EXISTS "fintech_label_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_identifier" DROP CONSTRAINT IF EXISTS "fintech_identifier_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_identifier" DROP CONSTRAINT IF EXISTS "fintech_identifier_document_number_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_expense" DROP CONSTRAINT IF EXISTS "fintech_expense_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_expense" DROP CONSTRAINT IF EXISTS "fintech_expense_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_documenttype" DROP CONSTRAINT IF EXISTS "fintech_documenttype_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_documenttype" DROP CONSTRAINT IF EXISTS "fintech_documenttype_code_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_currency" DROP CONSTRAINT IF EXISTS "fintech_currency_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_credit" DROP CONSTRAINT IF EXISTS "fintech_credit_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_country" DROP CONSTRAINT IF EXISTS "fintech_country_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_categorytype" DROP CONSTRAINT IF EXISTS "fintech_categorytype_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_categorytype" DROP CONSTRAINT IF EXISTS "fintech_categorytype_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_categorytype" DROP CONSTRAINT IF EXISTS "fintech_categorytype_name_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_category" DROP CONSTRAINT IF EXISTS "fintech_category_uid_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_category" DROP CONSTRAINT IF EXISTS "fintech_category_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_address" DROP CONSTRAINT IF EXISTS "fintech_address_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_accountmethodamount" DROP CONSTRAINT IF EXISTS "fintech_accountmethodamount_pkey";
ALTER TABLE IF EXISTS ONLY "public"."fintech_accountmethodamount" DROP CONSTRAINT IF EXISTS "fintech_accountmethodamount_payment_code_key";
ALTER TABLE IF EXISTS ONLY "public"."fintech_account" DROP CONSTRAINT IF EXISTS "fintech_account_pkey";
ALTER TABLE IF EXISTS ONLY "public"."django_session" DROP CONSTRAINT IF EXISTS "django_session_pkey";
ALTER TABLE IF EXISTS ONLY "public"."django_migrations" DROP CONSTRAINT IF EXISTS "django_migrations_pkey";
ALTER TABLE IF EXISTS ONLY "public"."django_content_type" DROP CONSTRAINT IF EXISTS "django_content_type_pkey";
ALTER TABLE IF EXISTS ONLY "public"."django_content_type" DROP CONSTRAINT IF EXISTS "django_content_type_app_label_model_76bd3d3b_uniq";
ALTER TABLE IF EXISTS ONLY "public"."django_admin_log" DROP CONSTRAINT IF EXISTS "django_admin_log_pkey";
ALTER TABLE IF EXISTS ONLY "public"."authtoken_token" DROP CONSTRAINT IF EXISTS "authtoken_token_user_id_key";
ALTER TABLE IF EXISTS ONLY "public"."authtoken_token" DROP CONSTRAINT IF EXISTS "authtoken_token_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_user" DROP CONSTRAINT IF EXISTS "auth_user_username_key";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_user_permissions" DROP CONSTRAINT IF EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_user_permissions" DROP CONSTRAINT IF EXISTS "auth_user_user_permissions_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_user" DROP CONSTRAINT IF EXISTS "auth_user_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_groups" DROP CONSTRAINT IF EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq";
ALTER TABLE IF EXISTS ONLY "public"."auth_user_groups" DROP CONSTRAINT IF EXISTS "auth_user_groups_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_permission" DROP CONSTRAINT IF EXISTS "auth_permission_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_permission" DROP CONSTRAINT IF EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq";
ALTER TABLE IF EXISTS ONLY "public"."auth_group" DROP CONSTRAINT IF EXISTS "auth_group_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_group_permissions" DROP CONSTRAINT IF EXISTS "auth_group_permissions_pkey";
ALTER TABLE IF EXISTS ONLY "public"."auth_group_permissions" DROP CONSTRAINT IF EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq";
ALTER TABLE IF EXISTS ONLY "public"."auth_group" DROP CONSTRAINT IF EXISTS "auth_group_name_key";
ALTER TABLE IF EXISTS "public"."token_blacklist_outstandingtoken" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."token_blacklist_blacklistedtoken" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_user_user_permissions" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_user_groups" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_user" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_transaction" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_subcategory" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_seller" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_role" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_phonenumber" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_periodicity" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_paramslocation" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_language" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_label" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_identifier" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_expense" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_documenttype" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_currency" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_credit" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_country" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_categorytype" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_category" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_address" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_accountmethodamount" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."fintech_account" ALTER COLUMN "id_payment_method" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."django_migrations" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."django_content_type" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."django_admin_log" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."auth_user_user_permissions" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."auth_user_groups" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."auth_user" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."auth_permission" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."auth_group_permissions" ALTER COLUMN "id" DROP DEFAULT;
ALTER TABLE IF EXISTS "public"."auth_group" ALTER COLUMN "id" DROP DEFAULT;
DROP SEQUENCE IF EXISTS "public"."token_blacklist_outstandingtoken_id_seq";
DROP TABLE IF EXISTS "public"."token_blacklist_outstandingtoken";
DROP SEQUENCE IF EXISTS "public"."token_blacklist_blacklistedtoken_id_seq";
DROP TABLE IF EXISTS "public"."token_blacklist_blacklistedtoken";
DROP TABLE IF EXISTS "public"."oauth2_provider_refreshtoken";
DROP TABLE IF EXISTS "public"."oauth2_provider_idtoken";
DROP TABLE IF EXISTS "public"."oauth2_provider_grant";
DROP TABLE IF EXISTS "public"."oauth2_provider_application";
DROP TABLE IF EXISTS "public"."oauth2_provider_accesstoken";
DROP SEQUENCE IF EXISTS "public"."fintech_user_user_permissions_id_seq";
DROP TABLE IF EXISTS "public"."fintech_user_user_permissions";
DROP SEQUENCE IF EXISTS "public"."fintech_user_id_seq";
DROP SEQUENCE IF EXISTS "public"."fintech_user_groups_id_seq";
DROP TABLE IF EXISTS "public"."fintech_user_groups";
DROP TABLE IF EXISTS "public"."fintech_user";
DROP SEQUENCE IF EXISTS "public"."fintech_transaction_id_seq";
DROP TABLE IF EXISTS "public"."fintech_transaction";
DROP SEQUENCE IF EXISTS "public"."fintech_subcategory_id_seq";
DROP TABLE IF EXISTS "public"."fintech_subcategory";
DROP SEQUENCE IF EXISTS "public"."fintech_seller_id_seq";
DROP TABLE IF EXISTS "public"."fintech_seller";
DROP SEQUENCE IF EXISTS "public"."fintech_role_id_seq";
DROP TABLE IF EXISTS "public"."fintech_role";
DROP SEQUENCE IF EXISTS "public"."fintech_phonenumber_id_seq";
DROP TABLE IF EXISTS "public"."fintech_phonenumber";
DROP SEQUENCE IF EXISTS "public"."fintech_periodicity_id_seq";
DROP TABLE IF EXISTS "public"."fintech_periodicity";
DROP SEQUENCE IF EXISTS "public"."fintech_paramslocation_id_seq";
DROP TABLE IF EXISTS "public"."fintech_paramslocation";
DROP SEQUENCE IF EXISTS "public"."fintech_language_id_seq";
DROP TABLE IF EXISTS "public"."fintech_language";
DROP SEQUENCE IF EXISTS "public"."fintech_label_id_seq";
DROP TABLE IF EXISTS "public"."fintech_label";
DROP SEQUENCE IF EXISTS "public"."fintech_identifier_id_seq";
DROP TABLE IF EXISTS "public"."fintech_identifier";
DROP SEQUENCE IF EXISTS "public"."fintech_expense_id_seq";
DROP TABLE IF EXISTS "public"."fintech_expense";
DROP SEQUENCE IF EXISTS "public"."fintech_documenttype_id_seq";
DROP TABLE IF EXISTS "public"."fintech_documenttype";
DROP SEQUENCE IF EXISTS "public"."fintech_currency_id_seq";
DROP TABLE IF EXISTS "public"."fintech_currency";
DROP SEQUENCE IF EXISTS "public"."fintech_credit_id_seq";
DROP TABLE IF EXISTS "public"."fintech_credit";
DROP SEQUENCE IF EXISTS "public"."fintech_country_id_seq";
DROP TABLE IF EXISTS "public"."fintech_country";
DROP SEQUENCE IF EXISTS "public"."fintech_categorytype_id_seq";
DROP TABLE IF EXISTS "public"."fintech_categorytype";
DROP SEQUENCE IF EXISTS "public"."fintech_category_id_seq";
DROP TABLE IF EXISTS "public"."fintech_category";
DROP SEQUENCE IF EXISTS "public"."fintech_address_id_seq";
DROP TABLE IF EXISTS "public"."fintech_address";
DROP SEQUENCE IF EXISTS "public"."fintech_accountmethodamount_id_seq";
DROP TABLE IF EXISTS "public"."fintech_accountmethodamount";
DROP SEQUENCE IF EXISTS "public"."fintech_account_id_payment_method_seq";
DROP TABLE IF EXISTS "public"."fintech_account";
DROP TABLE IF EXISTS "public"."django_session";
DROP SEQUENCE IF EXISTS "public"."django_migrations_id_seq";
DROP TABLE IF EXISTS "public"."django_migrations";
DROP SEQUENCE IF EXISTS "public"."django_content_type_id_seq";
DROP TABLE IF EXISTS "public"."django_content_type";
DROP SEQUENCE IF EXISTS "public"."django_admin_log_id_seq";
DROP TABLE IF EXISTS "public"."django_admin_log";
DROP TABLE IF EXISTS "public"."authtoken_token";
DROP SEQUENCE IF EXISTS "public"."auth_user_user_permissions_id_seq";
DROP TABLE IF EXISTS "public"."auth_user_user_permissions";
DROP SEQUENCE IF EXISTS "public"."auth_user_id_seq";
DROP SEQUENCE IF EXISTS "public"."auth_user_groups_id_seq";
DROP TABLE IF EXISTS "public"."auth_user_groups";
DROP TABLE IF EXISTS "public"."auth_user";
DROP SEQUENCE IF EXISTS "public"."auth_permission_id_seq";
DROP TABLE IF EXISTS "public"."auth_permission";
DROP SEQUENCE IF EXISTS "public"."auth_group_permissions_id_seq";
DROP TABLE IF EXISTS "public"."auth_group_permissions";
DROP SEQUENCE IF EXISTS "public"."auth_group_id_seq";
DROP TABLE IF EXISTS "public"."auth_group";
-- *not* dropping schema, since initdb creates it
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

-- *not* creating schema, since initdb creates it


--
-- Name: SCHEMA "public"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA "public" IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = "heap";

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."auth_group" (
    "id" integer NOT NULL,
    "name" character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."auth_group_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."auth_group_id_seq" OWNED BY "public"."auth_group"."id";


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."auth_group_permissions" (
    "id" bigint NOT NULL,
    "group_id" integer NOT NULL,
    "permission_id" integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."auth_group_permissions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."auth_group_permissions_id_seq" OWNED BY "public"."auth_group_permissions"."id";


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."auth_permission" (
    "id" integer NOT NULL,
    "name" character varying(255) NOT NULL,
    "content_type_id" integer NOT NULL,
    "codename" character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."auth_permission_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."auth_permission_id_seq" OWNED BY "public"."auth_permission"."id";


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."auth_user" (
    "id" integer NOT NULL,
    "password" character varying(128) NOT NULL,
    "last_login" timestamp with time zone,
    "is_superuser" boolean NOT NULL,
    "username" character varying(150) NOT NULL,
    "first_name" character varying(150) NOT NULL,
    "last_name" character varying(150) NOT NULL,
    "email" character varying(254) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "date_joined" timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."auth_user_groups" (
    "id" bigint NOT NULL,
    "user_id" integer NOT NULL,
    "group_id" integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."auth_user_groups_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."auth_user_groups_id_seq" OWNED BY "public"."auth_user_groups"."id";


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."auth_user_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."auth_user_id_seq" OWNED BY "public"."auth_user"."id";


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."auth_user_user_permissions" (
    "id" bigint NOT NULL,
    "user_id" integer NOT NULL,
    "permission_id" integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."auth_user_user_permissions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."auth_user_user_permissions_id_seq" OWNED BY "public"."auth_user_user_permissions"."id";


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."authtoken_token" (
    "key" character varying(40) NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "user_id" integer NOT NULL
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."django_admin_log" (
    "id" integer NOT NULL,
    "action_time" timestamp with time zone NOT NULL,
    "object_id" "text",
    "object_repr" character varying(200) NOT NULL,
    "action_flag" smallint NOT NULL,
    "change_message" "text" NOT NULL,
    "content_type_id" integer,
    "user_id" integer NOT NULL,
    CONSTRAINT "django_admin_log_action_flag_check" CHECK (("action_flag" >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."django_admin_log_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."django_admin_log_id_seq" OWNED BY "public"."django_admin_log"."id";


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."django_content_type" (
    "id" integer NOT NULL,
    "app_label" character varying(100) NOT NULL,
    "model" character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."django_content_type_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."django_content_type_id_seq" OWNED BY "public"."django_content_type"."id";


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."django_migrations" (
    "id" bigint NOT NULL,
    "app" character varying(255) NOT NULL,
    "name" character varying(255) NOT NULL,
    "applied" timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."django_migrations_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."django_migrations_id_seq" OWNED BY "public"."django_migrations"."id";


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."django_session" (
    "session_key" character varying(40) NOT NULL,
    "session_data" "text" NOT NULL,
    "expire_date" timestamp with time zone NOT NULL
);


--
-- Name: fintech_account; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_account" (
    "id_payment_method" integer NOT NULL,
    "name" character varying(100) NOT NULL,
    "account_number" character varying(50),
    "balance" numeric(12,2) NOT NULL,
    "eletronic_software_id" character varying(50),
    "currency_id" bigint
);


--
-- Name: fintech_account_id_payment_method_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_account_id_payment_method_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_account_id_payment_method_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_account_id_payment_method_seq" OWNED BY "public"."fintech_account"."id_payment_method";


--
-- Name: fintech_accountmethodamount; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_accountmethodamount" (
    "id" bigint NOT NULL,
    "payment_code" character varying(100) NOT NULL,
    "amount" numeric(12,2) NOT NULL,
    "amount_paid" numeric(12,2) NOT NULL,
    "credit_id" bigint NOT NULL,
    "currency_id" bigint,
    "payment_method_id" integer NOT NULL,
    "transaction_id" bigint NOT NULL
);


--
-- Name: fintech_accountmethodamount_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_accountmethodamount_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_accountmethodamount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_accountmethodamount_id_seq" OWNED BY "public"."fintech_accountmethodamount"."id";


--
-- Name: fintech_address; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_address" (
    "id" bigint NOT NULL,
    "address_type" character varying(50) NOT NULL,
    "address" character varying(255) NOT NULL,
    "city" character varying(100) NOT NULL,
    "country_id" bigint,
    "user_id" integer NOT NULL
);


--
-- Name: fintech_address_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_address_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_address_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_address_id_seq" OWNED BY "public"."fintech_address"."id";


--
-- Name: fintech_category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_category" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "name" character varying(100) NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "category_type_id" bigint
);


--
-- Name: fintech_category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_category_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_category_id_seq" OWNED BY "public"."fintech_category"."id";


--
-- Name: fintech_categorytype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_categorytype" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "name" character varying(100) NOT NULL,
    "description" "text"
);


--
-- Name: fintech_categorytype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_categorytype_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_categorytype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_categorytype_id_seq" OWNED BY "public"."fintech_categorytype"."id";


--
-- Name: fintech_country; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_country" (
    "id" bigint NOT NULL,
    "name" character varying(100) NOT NULL,
    "utc_offset" integer NOT NULL
);


--
-- Name: fintech_country_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_country_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_country_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_country_id_seq" OWNED BY "public"."fintech_country"."id";


--
-- Name: fintech_credit; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_credit" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "state" character varying(15) NOT NULL,
    "cost" numeric(12,2) NOT NULL,
    "price" numeric(12,2) NOT NULL,
    "earnings" numeric(12,2),
    "first_date_payment" "date" NOT NULL,
    "second_date_payment" "date" NOT NULL,
    "credit_days" integer NOT NULL,
    "description" "text",
    "interest" numeric(5,2),
    "refinancing" numeric(12,2),
    "total_abonos" numeric(12,2) NOT NULL,
    "pending_amount" numeric(12,2),
    "installment_number" integer,
    "installment_value" numeric(12,2),
    "is_in_default" boolean NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "morosidad_level" character varying(20) NOT NULL,
    "currency_id" bigint,
    "payment_id" integer,
    "periodicity_id" bigint,
    "registered_by_id" integer,
    "subcategory_id" bigint,
    "user_id" bigint NOT NULL,
    "seller_id" bigint
);


--
-- Name: fintech_credit_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_credit_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_credit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_credit_id_seq" OWNED BY "public"."fintech_credit"."id";


--
-- Name: fintech_currency; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_currency" (
    "id" bigint NOT NULL,
    "asset_type" character varying(8) NOT NULL,
    "id_currency" character varying(4) NOT NULL,
    "currency" character varying(15) NOT NULL,
    "exchange_rate" numeric(10,4) NOT NULL
);


--
-- Name: fintech_currency_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_currency_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_currency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_currency_id_seq" OWNED BY "public"."fintech_currency"."id";


--
-- Name: fintech_documenttype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_documenttype" (
    "id" bigint NOT NULL,
    "code" character varying(2) NOT NULL,
    "description" character varying(50) NOT NULL,
    "country_id_id" bigint
);


--
-- Name: fintech_documenttype_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_documenttype_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_documenttype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_documenttype_id_seq" OWNED BY "public"."fintech_documenttype"."id";


--
-- Name: fintech_expense; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_expense" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "amount" numeric(12,2) NOT NULL,
    "description" "text",
    "date" timestamp with time zone NOT NULL,
    "account_id" integer NOT NULL,
    "subcategory_id" bigint,
    "registered_by_id" integer,
    "user_id" integer NOT NULL,
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL
);


--
-- Name: fintech_expense_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_expense_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_expense_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_expense_id_seq" OWNED BY "public"."fintech_expense"."id";


--
-- Name: fintech_identifier; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_identifier" (
    "id" bigint NOT NULL,
    "document_number" character varying(20) NOT NULL,
    "country_id" bigint,
    "document_type_id" bigint NOT NULL
);


--
-- Name: fintech_identifier_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_identifier_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_identifier_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_identifier_id_seq" OWNED BY "public"."fintech_identifier"."id";


--
-- Name: fintech_label; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_label" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "name" character varying(255) NOT NULL,
    "position" character varying(255)
);


--
-- Name: fintech_label_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_label_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_label_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_label_id_seq" OWNED BY "public"."fintech_label"."id";


--
-- Name: fintech_language; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_language" (
    "id" bigint NOT NULL,
    "name" character varying(100) NOT NULL,
    "region_of_use" character varying(100) NOT NULL
);


--
-- Name: fintech_language_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_language_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_language_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_language_id_seq" OWNED BY "public"."fintech_language"."id";


--
-- Name: fintech_paramslocation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_paramslocation" (
    "id" bigint NOT NULL,
    "city_code" character varying(10),
    "city_name" character varying(50),
    "state_code" character varying(10),
    "state_name" character varying(50),
    "country_code" character varying(10),
    "country_name" character varying(50)
);


--
-- Name: fintech_paramslocation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_paramslocation_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_paramslocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_paramslocation_id_seq" OWNED BY "public"."fintech_paramslocation"."id";


--
-- Name: fintech_periodicity; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_periodicity" (
    "id" bigint NOT NULL,
    "name" character varying(50) NOT NULL,
    "days" integer NOT NULL
);


--
-- Name: fintech_periodicity_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_periodicity_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_periodicity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_periodicity_id_seq" OWNED BY "public"."fintech_periodicity"."id";


--
-- Name: fintech_phonenumber; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_phonenumber" (
    "id" bigint NOT NULL,
    "country_code" character varying(15) NOT NULL,
    "phone_number" character varying(20) NOT NULL,
    "country_related_id" bigint
);


--
-- Name: fintech_phonenumber_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_phonenumber_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_phonenumber_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_phonenumber_id_seq" OWNED BY "public"."fintech_phonenumber"."id";


--
-- Name: fintech_role; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_role" (
    "id" bigint NOT NULL,
    "name" character varying(100) NOT NULL,
    "is_staff_role" boolean NOT NULL
);


--
-- Name: fintech_role_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_role_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_role_id_seq" OWNED BY "public"."fintech_role"."id";


--
-- Name: fintech_seller; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_seller" (
    "id" bigint NOT NULL,
    "total_sales" numeric(12,2) NOT NULL,
    "commissions" numeric(12,2) NOT NULL,
    "returns" integer NOT NULL,
    "role_id" bigint NOT NULL,
    "user_id" integer NOT NULL
);


--
-- Name: fintech_seller_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_seller_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_seller_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_seller_id_seq" OWNED BY "public"."fintech_seller"."id";


--
-- Name: fintech_subcategory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_subcategory" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "name" character varying(100) NOT NULL,
    "description" "text",
    "created_at" timestamp with time zone NOT NULL,
    "updated_at" timestamp with time zone NOT NULL,
    "category_id" bigint NOT NULL
);


--
-- Name: fintech_subcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_subcategory_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_subcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_subcategory_id_seq" OWNED BY "public"."fintech_subcategory"."id";


--
-- Name: fintech_transaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_transaction" (
    "id" bigint NOT NULL,
    "uid" "uuid" NOT NULL,
    "transaction_type" character varying(50) NOT NULL,
    "date" timestamp with time zone NOT NULL,
    "description" "text",
    "category_id" bigint,
    "user_id" bigint
);


--
-- Name: fintech_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_transaction_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_transaction_id_seq" OWNED BY "public"."fintech_transaction"."id";


--
-- Name: fintech_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_user" (
    "id" bigint NOT NULL,
    "password" character varying(128) NOT NULL,
    "last_login" timestamp with time zone,
    "is_superuser" boolean NOT NULL,
    "username" character varying(150) NOT NULL,
    "first_name" character varying(150) NOT NULL,
    "last_name" character varying(150) NOT NULL,
    "email" character varying(254) NOT NULL,
    "is_staff" boolean NOT NULL,
    "is_active" boolean NOT NULL,
    "date_joined" timestamp with time zone NOT NULL,
    "id_user" "uuid" NOT NULL,
    "billing_address" character varying(255) NOT NULL,
    "address_shipping" character varying(255) NOT NULL,
    "reference_1" character varying(255),
    "reference_2" character varying(255),
    "electronic_id" character varying(50),
    "city_id" bigint,
    "country_id" bigint,
    "document_id" bigint,
    "label_id" bigint,
    "phone_1_id" bigint,
    "role_id" bigint
);


--
-- Name: fintech_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_user_groups" (
    "id" bigint NOT NULL,
    "user_id" bigint NOT NULL,
    "group_id" integer NOT NULL
);


--
-- Name: fintech_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_user_groups_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_user_groups_id_seq" OWNED BY "public"."fintech_user_groups"."id";


--
-- Name: fintech_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_user_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_user_id_seq" OWNED BY "public"."fintech_user"."id";


--
-- Name: fintech_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."fintech_user_user_permissions" (
    "id" bigint NOT NULL,
    "user_id" bigint NOT NULL,
    "permission_id" integer NOT NULL
);


--
-- Name: fintech_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."fintech_user_user_permissions_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: fintech_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."fintech_user_user_permissions_id_seq" OWNED BY "public"."fintech_user_user_permissions"."id";


--
-- Name: oauth2_provider_accesstoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."oauth2_provider_accesstoken" (
    "id" bigint NOT NULL,
    "token" "text" NOT NULL,
    "expires" timestamp with time zone NOT NULL,
    "scope" "text" NOT NULL,
    "application_id" bigint,
    "user_id" integer,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone NOT NULL,
    "source_refresh_token_id" bigint,
    "id_token_id" bigint,
    "token_checksum" character varying(64) NOT NULL
);


--
-- Name: oauth2_provider_accesstoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE "public"."oauth2_provider_accesstoken" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."oauth2_provider_accesstoken_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_application; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."oauth2_provider_application" (
    "id" bigint NOT NULL,
    "client_id" character varying(100) NOT NULL,
    "redirect_uris" "text" NOT NULL,
    "client_type" character varying(32) NOT NULL,
    "authorization_grant_type" character varying(32) NOT NULL,
    "client_secret" character varying(255) NOT NULL,
    "name" character varying(255) NOT NULL,
    "user_id" integer,
    "skip_authorization" boolean NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone NOT NULL,
    "algorithm" character varying(5) NOT NULL,
    "post_logout_redirect_uris" "text" NOT NULL,
    "hash_client_secret" boolean NOT NULL,
    "allowed_origins" "text" NOT NULL
);


--
-- Name: oauth2_provider_application_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE "public"."oauth2_provider_application" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."oauth2_provider_application_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_grant; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."oauth2_provider_grant" (
    "id" bigint NOT NULL,
    "code" character varying(255) NOT NULL,
    "expires" timestamp with time zone NOT NULL,
    "redirect_uri" "text" NOT NULL,
    "scope" "text" NOT NULL,
    "application_id" bigint NOT NULL,
    "user_id" integer NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone NOT NULL,
    "code_challenge" character varying(128) NOT NULL,
    "code_challenge_method" character varying(10) NOT NULL,
    "nonce" character varying(255) NOT NULL,
    "claims" "text" NOT NULL
);


--
-- Name: oauth2_provider_grant_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE "public"."oauth2_provider_grant" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."oauth2_provider_grant_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_idtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."oauth2_provider_idtoken" (
    "id" bigint NOT NULL,
    "jti" "uuid" NOT NULL,
    "expires" timestamp with time zone NOT NULL,
    "scope" "text" NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone NOT NULL,
    "application_id" bigint,
    "user_id" integer
);


--
-- Name: oauth2_provider_idtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE "public"."oauth2_provider_idtoken" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."oauth2_provider_idtoken_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: oauth2_provider_refreshtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."oauth2_provider_refreshtoken" (
    "id" bigint NOT NULL,
    "token" character varying(255) NOT NULL,
    "access_token_id" bigint,
    "application_id" bigint NOT NULL,
    "user_id" integer NOT NULL,
    "created" timestamp with time zone NOT NULL,
    "updated" timestamp with time zone NOT NULL,
    "revoked" timestamp with time zone,
    "token_family" "uuid"
);


--
-- Name: oauth2_provider_refreshtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

ALTER TABLE "public"."oauth2_provider_refreshtoken" ALTER COLUMN "id" ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME "public"."oauth2_provider_refreshtoken_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: token_blacklist_blacklistedtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."token_blacklist_blacklistedtoken" (
    "id" bigint NOT NULL,
    "blacklisted_at" timestamp with time zone NOT NULL,
    "token_id" bigint NOT NULL
);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."token_blacklist_blacklistedtoken_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."token_blacklist_blacklistedtoken_id_seq" OWNED BY "public"."token_blacklist_blacklistedtoken"."id";


--
-- Name: token_blacklist_outstandingtoken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "public"."token_blacklist_outstandingtoken" (
    "id" bigint NOT NULL,
    "token" "text" NOT NULL,
    "created_at" timestamp with time zone,
    "expires_at" timestamp with time zone NOT NULL,
    "user_id" integer,
    "jti" character varying(255) NOT NULL
);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE "public"."token_blacklist_outstandingtoken_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE "public"."token_blacklist_outstandingtoken_id_seq" OWNED BY "public"."token_blacklist_outstandingtoken"."id";


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."auth_group_id_seq"'::"regclass");


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group_permissions" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."auth_group_permissions_id_seq"'::"regclass");


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_permission" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."auth_permission_id_seq"'::"regclass");


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."auth_user_id_seq"'::"regclass");


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_groups" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."auth_user_groups_id_seq"'::"regclass");


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_user_permissions" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."auth_user_user_permissions_id_seq"'::"regclass");


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_admin_log" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."django_admin_log_id_seq"'::"regclass");


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_content_type" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."django_content_type_id_seq"'::"regclass");


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_migrations" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."django_migrations_id_seq"'::"regclass");


--
-- Name: fintech_account id_payment_method; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_account" ALTER COLUMN "id_payment_method" SET DEFAULT "nextval"('"public"."fintech_account_id_payment_method_seq"'::"regclass");


--
-- Name: fintech_accountmethodamount id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_accountmethodamount_id_seq"'::"regclass");


--
-- Name: fintech_address id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_address" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_address_id_seq"'::"regclass");


--
-- Name: fintech_category id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_category" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_category_id_seq"'::"regclass");


--
-- Name: fintech_categorytype id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_categorytype" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_categorytype_id_seq"'::"regclass");


--
-- Name: fintech_country id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_country" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_country_id_seq"'::"regclass");


--
-- Name: fintech_credit id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_credit_id_seq"'::"regclass");


--
-- Name: fintech_currency id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_currency" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_currency_id_seq"'::"regclass");


--
-- Name: fintech_documenttype id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_documenttype" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_documenttype_id_seq"'::"regclass");


--
-- Name: fintech_expense id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_expense_id_seq"'::"regclass");


--
-- Name: fintech_identifier id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_identifier" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_identifier_id_seq"'::"regclass");


--
-- Name: fintech_label id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_label" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_label_id_seq"'::"regclass");


--
-- Name: fintech_language id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_language" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_language_id_seq"'::"regclass");


--
-- Name: fintech_paramslocation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_paramslocation" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_paramslocation_id_seq"'::"regclass");


--
-- Name: fintech_periodicity id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_periodicity" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_periodicity_id_seq"'::"regclass");


--
-- Name: fintech_phonenumber id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_phonenumber" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_phonenumber_id_seq"'::"regclass");


--
-- Name: fintech_role id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_role" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_role_id_seq"'::"regclass");


--
-- Name: fintech_seller id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_seller" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_seller_id_seq"'::"regclass");


--
-- Name: fintech_subcategory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_subcategory" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_subcategory_id_seq"'::"regclass");


--
-- Name: fintech_transaction id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_transaction" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_transaction_id_seq"'::"regclass");


--
-- Name: fintech_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_user_id_seq"'::"regclass");


--
-- Name: fintech_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_groups" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_user_groups_id_seq"'::"regclass");


--
-- Name: fintech_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_user_permissions" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."fintech_user_user_permissions_id_seq"'::"regclass");


--
-- Name: token_blacklist_blacklistedtoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_blacklistedtoken" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."token_blacklist_blacklistedtoken_id_seq"'::"regclass");


--
-- Name: token_blacklist_outstandingtoken id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_outstandingtoken" ALTER COLUMN "id" SET DEFAULT "nextval"('"public"."token_blacklist_outstandingtoken_id_seq"'::"regclass");


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."auth_group" ("id", "name") FROM stdin;
1	User
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."auth_group_permissions" ("id", "group_id", "permission_id") FROM stdin;
1	1	4
2	1	8
3	1	12
4	1	16
5	1	20
6	1	24
7	1	28
8	1	32
9	1	36
10	1	40
11	1	44
12	1	48
13	1	52
14	1	56
15	1	60
16	1	64
17	1	68
18	1	72
19	1	76
20	1	80
21	1	84
22	1	88
23	1	92
24	1	96
25	1	100
26	1	104
27	1	108
28	1	112
29	1	116
30	1	120
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."auth_permission" ("id", "name", "content_type_id", "codename") FROM stdin;
1	Can add Token	1	add_token
2	Can change Token	1	change_token
3	Can delete Token	1	delete_token
4	Can view Token	1	view_token
5	Can add token	2	add_tokenproxy
6	Can change token	2	change_tokenproxy
7	Can delete token	2	delete_tokenproxy
8	Can view token	2	view_tokenproxy
9	Can add blacklisted token	3	add_blacklistedtoken
10	Can change blacklisted token	3	change_blacklistedtoken
11	Can delete blacklisted token	3	delete_blacklistedtoken
12	Can view blacklisted token	3	view_blacklistedtoken
13	Can add outstanding token	4	add_outstandingtoken
14	Can change outstanding token	4	change_outstandingtoken
15	Can delete outstanding token	4	delete_outstandingtoken
16	Can view outstanding token	4	view_outstandingtoken
17	Can add log entry	5	add_logentry
18	Can change log entry	5	change_logentry
19	Can delete log entry	5	delete_logentry
20	Can view log entry	5	view_logentry
21	Can add permission	6	add_permission
22	Can change permission	6	change_permission
23	Can delete permission	6	delete_permission
24	Can view permission	6	view_permission
25	Can add group	7	add_group
26	Can change group	7	change_group
27	Can delete group	7	delete_group
28	Can view group	7	view_group
29	Can add user	8	add_user
30	Can change user	8	change_user
31	Can delete user	8	delete_user
32	Can view user	8	view_user
33	Can add content type	9	add_contenttype
34	Can change content type	9	change_contenttype
35	Can delete content type	9	delete_contenttype
36	Can view content type	9	view_contenttype
37	Can add session	10	add_session
38	Can change session	10	change_session
39	Can delete session	10	delete_session
40	Can view session	10	view_session
41	Can add account	11	add_account
42	Can change account	11	change_account
43	Can delete account	11	delete_account
44	Can view account	11	view_account
45	Can add category	12	add_category
46	Can change category	12	change_category
47	Can delete category	12	delete_category
48	Can view category	12	view_category
49	Can add category type	13	add_categorytype
50	Can change category type	13	change_categorytype
51	Can delete category type	13	delete_categorytype
52	Can view category type	13	view_categorytype
53	Can add country	14	add_country
54	Can change country	14	change_country
55	Can delete country	14	delete_country
56	Can view country	14	view_country
57	Can add currency	15	add_currency
58	Can change currency	15	change_currency
59	Can delete currency	15	delete_currency
60	Can view currency	15	view_currency
61	Can add document type	16	add_documenttype
62	Can change document type	16	change_documenttype
63	Can delete document type	16	delete_documenttype
64	Can view document type	16	view_documenttype
65	Can add identifier	17	add_identifier
66	Can change identifier	17	change_identifier
67	Can delete identifier	17	delete_identifier
68	Can view identifier	17	view_identifier
69	Can add label	18	add_label
70	Can change label	18	change_label
71	Can delete label	18	delete_label
72	Can view label	18	view_label
73	Can add language	19	add_language
74	Can change language	19	change_language
75	Can delete language	19	delete_language
76	Can view language	19	view_language
77	Can add params location	20	add_paramslocation
78	Can change params location	20	change_paramslocation
79	Can delete params location	20	delete_paramslocation
80	Can view params location	20	view_paramslocation
81	Can add periodicity	21	add_periodicity
82	Can change periodicity	21	change_periodicity
83	Can delete periodicity	21	delete_periodicity
84	Can view periodicity	21	view_periodicity
85	Can add phone number	22	add_phonenumber
86	Can change phone number	22	change_phonenumber
87	Can delete phone number	22	delete_phonenumber
88	Can view phone number	22	view_phonenumber
89	Can add role	23	add_role
90	Can change role	23	change_role
91	Can delete role	23	delete_role
92	Can view role	23	view_role
93	Can add sub category	24	add_subcategory
94	Can change sub category	24	change_subcategory
95	Can delete sub category	24	delete_subcategory
96	Can view sub category	24	view_subcategory
97	Can add user	25	add_user
98	Can change user	25	change_user
99	Can delete user	25	delete_user
100	Can view user	25	view_user
101	Can add transaction	26	add_transaction
102	Can change transaction	26	change_transaction
103	Can delete transaction	26	delete_transaction
104	Can view transaction	26	view_transaction
105	Can add expense	27	add_expense
106	Can change expense	27	change_expense
107	Can delete expense	27	delete_expense
108	Can view expense	27	view_expense
109	Can add credit	28	add_credit
110	Can change credit	28	change_credit
111	Can delete credit	28	delete_credit
112	Can view credit	28	view_credit
113	Can add address	29	add_address
114	Can change address	29	change_address
115	Can delete address	29	delete_address
116	Can view address	29	view_address
117	Can add account method amount	30	add_accountmethodamount
118	Can change account method amount	30	change_accountmethodamount
119	Can delete account method amount	30	delete_accountmethodamount
120	Can view account method amount	30	view_accountmethodamount
121	Can add seller	31	add_seller
122	Can change seller	31	change_seller
123	Can delete seller	31	delete_seller
124	Can view seller	31	view_seller
125	Can add application	32	add_application
126	Can change application	32	change_application
127	Can delete application	32	delete_application
128	Can view application	32	view_application
129	Can add access token	33	add_accesstoken
130	Can change access token	33	change_accesstoken
131	Can delete access token	33	delete_accesstoken
132	Can view access token	33	view_accesstoken
133	Can add grant	34	add_grant
134	Can change grant	34	change_grant
135	Can delete grant	34	delete_grant
136	Can view grant	34	view_grant
137	Can add refresh token	35	add_refreshtoken
138	Can change refresh token	35	change_refreshtoken
139	Can delete refresh token	35	delete_refreshtoken
140	Can view refresh token	35	view_refreshtoken
141	Can add id token	36	add_idtoken
142	Can change id token	36	change_idtoken
143	Can delete id token	36	delete_idtoken
144	Can view id token	36	view_idtoken
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."auth_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined") FROM stdin;
2	argon2$argon2id$v=19$m=102400,t=2,p=8$bXI1NHg5SWd0c2FqRHF3MW5LUm9Yeg$DZVDJRA2gTI+NkgCvrnF+1THDFpx8gknimaoBnzSHKU	\N	t	jose				t	t	2024-09-11 02:34:00+00
4	argon2$argon2id$v=19$m=102400,t=2,p=8$QUxyU3JISFRyR3NWd2pLcjVPZHg3Rw$HOAwKSvoK+gvdsyQ0CeP/EsoprbVhH31wPHBhNSMLds	\N	f	danielojeda				f	t	2024-09-12 02:01:36.663962+00
3	argon2$argon2id$v=19$m=102400,t=2,p=8$d25YSzdQc2R4YU44ZVRxemhReUdMTQ$leVAhWkUFf9fGtLRgLoAC8oZ11xki3eGqCTD8lDdpx8	2024-12-02 23:56:57.459288+00	f	lorena				t	t	2024-09-11 02:34:42+00
1	argon2$argon2id$v=19$m=102400,t=2,p=8$MEFjZk5QZWo3RkFKVjNJZTAzQ2FCSQ$8dHzLxafQo092hLzpa1sMmhQMpUB81xugksJSlYFDwk	2024-12-11 04:02:09.950319+00	t	admin			admin@example.com	t	t	2024-09-11 01:46:04.61091+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."auth_user_groups" ("id", "user_id", "group_id") FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."auth_user_user_permissions" ("id", "user_id", "permission_id") FROM stdin;
1	3	1
2	3	2
3	3	3
4	3	4
5	3	5
6	3	6
7	3	7
8	3	8
9	3	9
10	3	10
11	3	11
12	3	12
13	3	13
14	3	14
15	3	15
16	3	16
17	3	17
18	3	18
19	3	19
20	3	20
21	3	21
22	3	22
23	3	23
24	3	24
25	3	25
26	3	26
27	3	27
28	3	28
29	3	29
30	3	30
31	3	31
32	3	32
33	3	33
34	3	34
35	3	35
36	3	36
37	3	37
38	3	38
39	3	39
40	3	40
41	3	41
42	3	42
43	3	43
44	3	44
45	3	45
46	3	46
47	3	47
48	3	48
49	3	49
50	3	50
51	3	51
52	3	52
53	3	53
54	3	54
55	3	55
56	3	56
57	3	57
58	3	58
59	3	59
60	3	60
61	3	61
62	3	62
63	3	63
64	3	64
65	3	65
66	3	66
67	3	67
68	3	68
69	3	69
70	3	70
71	3	71
72	3	72
73	3	73
74	3	74
75	3	75
76	3	76
77	3	77
78	3	78
79	3	79
80	3	80
81	3	81
82	3	82
83	3	83
84	3	84
85	3	85
86	3	86
87	3	87
88	3	88
89	3	89
90	3	90
91	3	91
92	3	92
93	3	93
94	3	94
95	3	95
96	3	96
97	3	97
98	3	98
99	3	99
100	3	100
101	3	101
102	3	102
103	3	103
104	3	104
105	3	105
106	3	106
107	3	107
108	3	108
109	3	109
110	3	110
111	3	111
112	3	112
113	3	113
114	3	114
115	3	115
116	3	116
117	3	117
118	3	118
119	3	119
120	3	120
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."authtoken_token" ("key", "created", "user_id") FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."django_admin_log" ("id", "action_time", "object_id", "object_repr", "action_flag", "change_message", "content_type_id", "user_id") FROM stdin;
1	2024-09-11 02:34:02.54977+00	2	jose	1	[{"added": {}}]	8	1
2	2024-09-11 02:34:17.949812+00	2	jose	2	[{"changed": {"fields": ["Staff status", "Superuser status"]}}]	8	1
3	2024-09-11 02:34:44.248939+00	3	lorena	1	[{"added": {}}]	8	1
4	2024-09-11 02:34:55.354895+00	3	lorena	2	[{"changed": {"fields": ["Staff status", "User permissions"]}}]	8	1
5	2024-09-11 02:35:51.040335+00	1	Dólar	1	[{"added": {}}]	15	1
6	2024-09-11 02:36:03.043767+00	2	Euro	1	[{"added": {}}]	15	1
7	2024-09-11 02:36:15.297688+00	3	Peso colombiano	1	[{"added": {}}]	15	1
8	2024-09-11 02:36:22.838749+00	1	Yappy	1	[{"added": {}}]	11	1
9	2024-09-11 02:36:44.33707+00	2	Banco General	1	[{"added": {}}]	11	1
10	2024-09-11 02:37:09.836123+00	3	Banesco	1	[{"added": {}}]	11	1
11	2024-09-11 02:38:58.757417+00	1	User	1	[{"added": {}}]	7	1
12	2024-09-11 02:39:04.613249+00	1	carlosdelgado	1	[{"added": {}}]	25	1
13	2024-09-11 02:40:08.281148+00	1	User	1	[{"added": {}}]	23	1
14	2024-09-11 02:40:11.93494+00	2	colonvelasquez	1	[{"added": {}}]	25	1
15	2024-09-11 02:40:33.14916+00	1	carlosdelgado	2	[{"changed": {"fields": ["Role"]}}]	25	1
16	2024-09-11 02:41:24.541884+00	3	enriquefritos	1	[{"added": {}}]	25	1
17	2024-09-11 02:42:51.211669+00	1	Daily	1	[{"added": {}}]	21	1
18	2024-09-11 02:42:59.836421+00	2	Weekly	1	[{"added": {}}]	21	1
19	2024-09-11 02:43:08.264229+00	3	Beweekly	1	[{"added": {}}]	21	1
20	2024-09-11 02:43:17.339579+00	4	Monthly	1	[{"added": {}}]	21	1
21	2024-09-11 02:51:47.937859+00	1	Activos	1	[{"added": {}}]	13	1
22	2024-09-11 02:52:06.496103+00	2	Pasivos	1	[{"added": {}}]	13	1
23	2024-09-11 02:52:20.724007+00	3	Patrimonio Neto	1	[{"added": {}}]	13	1
24	2024-09-11 02:52:34.948597+00	4	Ingresos Operativos	1	[{"added": {}}]	13	1
25	2024-09-11 02:52:46.674573+00	5	Gastos Operativos	1	[{"added": {}}]	13	1
26	2024-09-11 02:53:13.931192+00	6	Ingresos no Operativos	1	[{"added": {}}]	13	1
27	2024-09-11 02:54:04.062978+00	1	Ventas	1	[{"added": {}}]	12	1
28	2024-09-11 02:54:16.132943+00	2	Créditos	1	[{"added": {}}]	12	1
29	2024-09-11 02:54:32.963156+00	3	Servicios	1	[{"added": {}}]	12	1
30	2024-09-11 02:54:54.272609+00	4	Otros ingresos operativos	1	[{"added": {}}]	12	1
31	2024-09-11 02:55:22.08685+00	5	Costo de ventas	1	[{"added": {}}]	12	1
32	2024-09-11 02:55:36.691845+00	6	Gastos de ventas	1	[{"added": {}}]	12	1
33	2024-09-11 02:56:02.944623+00	7	Gastos administrativos	1	[{"added": {}}]	12	1
34	2024-09-11 02:56:17.406081+00	8	Depreciación	1	[{"added": {}}]	12	1
35	2024-09-11 02:56:31.041957+00	9	Amortización	1	[{"added": {}}]	12	1
36	2024-09-11 02:57:14.092896+00	10	Ingresos financieros	1	[{"added": {}}]	12	1
37	2024-09-11 02:57:34.95329+00	11	Ganancias en venta de activos	1	[{"added": {}}]	12	1
38	2024-09-11 02:58:26.791191+00	1	Créditos - Crédito de consumo	1	[{"added": {}}]	24	1
39	2024-09-11 02:58:46.279211+00	2	Créditos - Crédito Personal	1	[{"added": {}}]	24	1
40	2024-09-11 02:58:58.353669+00	1	Créditos - Crédito de Consumo	2	[{"changed": {"fields": ["Name"]}}]	24	1
41	2024-09-11 02:59:13.423759+00	3	Créditos - Crédito hipotecario	1	[{"added": {}}]	24	1
42	2024-09-11 03:00:12.603466+00	3	Créditos - Crédito Hipotecario	2	[{"changed": {"fields": ["Name"]}}]	24	1
43	2024-09-11 03:14:09.935254+00	4	Efectivo	1	[{"added": {}}]	11	1
44	2024-09-11 05:39:37.676656+00	4	Gastos administrativos - Transporte	1	[{"added": {}}]	24	1
45	2024-09-11 05:43:53.087385+00	12	Gastos de operación	1	[{"added": {}}]	12	1
46	2024-09-11 05:44:08.735506+00	12	Gastos de actividad	2	[{"changed": {"fields": ["Name"]}}]	12	1
47	2024-09-11 05:44:40.850226+00	4	Gastos de actividad - Transporte	2	[{"changed": {"fields": ["Category"]}}]	24	1
48	2024-09-11 05:45:07.399986+00	5	Gastos de actividad - Gasolina	1	[{"added": {}}]	24	1
49	2024-09-11 05:46:41.912292+00	6	Gastos de actividad - Rent a car	1	[{"added": {}}]	24	1
50	2024-09-11 15:10:05.709445+00	7	Gastos de actividad - Viaticos	1	[{"added": {}}]	24	1
51	2024-09-11 15:12:38.299651+00	8	Gastos de actividad - Viaticos	1	[{"added": {}}]	24	1
52	2024-09-11 18:07:12.384622+00	3	lorena	2	[{"changed": {"fields": ["password"]}}]	8	1
53	2024-09-11 19:34:13.807459+00	4	Dario	1	[{"added": {}}]	25	3
54	2024-09-11 19:34:44.017251+00	4	DarioDominguez	2	[{"changed": {"fields": ["Username"]}}]	25	3
55	2024-09-11 19:34:44.214157+00	4	DarioDominguez	2	[]	25	3
56	2024-09-11 19:35:16.837513+00	1	DarioDominguez - Créditos - Crédito Personal: Credit:152, pending:152	1	[{"added": {}}]	28	3
57	2024-09-11 19:44:38.384993+00	5	SeleneNovio	1	[{"added": {}}]	25	3
58	2024-09-11 19:45:48.278182+00	2	SeleneNovio - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
59	2024-09-11 19:46:40.705648+00	6	SeleneIbarra	1	[{"added": {}}]	25	3
60	2024-09-11 19:47:38.94691+00	3	SeleneIbarra - Créditos - Crédito Personal: Credit:1100, pending:1100	1	[{"added": {}}]	28	3
61	2024-09-11 20:53:59.416977+00	4	Transaction object (4)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 275"}}]	26	3
62	2024-09-11 21:04:06.216681+00	7	RamiroGuerra	1	[{"added": {}}]	25	3
63	2024-09-11 21:06:48.944747+00	4	RamiroGuerra - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
64	2024-09-11 21:07:44.635673+00	5	RamiroGuerra - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
65	2024-09-11 21:15:24.236388+00	7	Transaction object (7)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 275"}}]	26	3
66	2024-09-11 21:15:48.323936+00	1	Colombia	1	[{"added": {}}]	14	1
67	2024-09-11 21:16:08.610306+00	1	CC - Cédula de ciudadanía	1	[{"added": {}}]	16	1
68	2024-09-11 21:16:15.149359+00	8	Transaction object (8)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
69	2024-09-11 21:16:16.981362+00	1	Cédula de ciudadanía (Colombia): 1214724312	1	[{"added": {}}]	17	1
70	2024-09-11 21:18:03.520988+00	8	JoseOjeda	1	[{"added": {}}]	25	1
71	2024-09-11 21:18:35.115725+00	6	JoseOjeda - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	1
72	2024-09-11 21:18:59.136128+00	9	MariaMartinez	1	[{"added": {}}]	25	3
73	2024-09-11 21:19:34.116583+00	7	MariaMartinez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
74	2024-09-11 21:22:50.852987+00	9	Créditos - Pago a Crédito Personal	1	[{"added": {}}]	24	1
75	2024-09-11 21:23:39.123649+00	10	Créditos - Pago a crédito de consumo	1	[{"added": {}}]	24	1
76	2024-09-11 21:24:18.549645+00	11	Créditos - Pago a Crédito Hipotecario	1	[{"added": {}}]	24	1
77	2024-09-11 23:21:38.544803+00	1	Transaction object (1)	2	[{"changed": {"fields": ["Transaction type", "Description"]}}]	26	1
78	2024-09-11 23:22:18.879044+00	2	Transaction object (2)	2	[{"changed": {"fields": ["Description"]}}]	26	1
79	2024-09-11 23:22:56.593263+00	1	Transaction object (1)	2	[]	26	1
80	2024-09-11 23:24:15.75357+00	2	Transaction object (2)	2	[{"changed": {"fields": ["Transaction type"]}}]	26	1
81	2024-09-11 23:26:45.339712+00	3	Transaction object (3)	2	[{"changed": {"fields": ["Transaction type"]}}]	26	1
82	2024-09-11 23:28:33.001046+00	5	Transaction object (5)	2	[{"changed": {"fields": ["Transaction type", "Description"]}}]	26	1
83	2024-09-11 23:36:18.301184+00	8	carlosdelgado - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	1
84	2024-09-11 23:37:19.105009+00	9	colonvelasquez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	1
85	2024-09-11 23:38:06.72421+00	10	enriquefritos - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	1
86	2024-09-11 23:38:17.307954+00	9	colonvelasquez - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[{"changed": {"fields": ["Created at"]}}]	28	1
87	2024-09-11 23:38:27.196004+00	8	carlosdelgado - Créditos - Crédito Personal: Credit:160.00, pending:160.00	2	[{"changed": {"fields": ["Created at"]}}]	28	1
88	2024-09-11 23:43:29.76062+00	12	Transaction object (12)	2	[{"changed": {"fields": ["Date"]}}]	26	1
89	2024-09-11 23:43:42.073244+00	11	Transaction object (11)	2	[{"changed": {"fields": ["Date"]}}]	26	1
90	2024-09-11 23:44:48.807038+00	10	leonardovaldez	1	[{"added": {}}]	25	1
91	2024-09-11 23:45:35.207813+00	11	leonardovaldez - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	1
92	2024-09-11 23:46:40.007611+00	15	Transaction object (15)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
93	2024-09-11 23:49:40.80094+00	14	Transaction object (14)	2	[{"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 1000"}}]	26	1
94	2024-09-11 23:49:57.813374+00	15	Transaction object (15)	2	[{"changed": {"fields": ["Date"]}}]	26	1
95	2024-09-11 23:51:19.100876+00	16	Transaction object (16)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
96	2024-09-11 23:52:06.208645+00	17	Transaction object (17)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
97	2024-09-11 23:53:08.578995+00	18	Transaction object (18)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
98	2024-09-12 00:47:56.812459+00	11	JessicaSanchez.	1	[{"added": {}}]	25	3
99	2024-09-12 00:48:38.906826+00	12	JessicaSanchez. - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
100	2024-09-12 01:55:08.624348+00	2	Controller	1	[{"added": {}}]	23	1
101	2024-09-12 02:01:38.333589+00	4	danielojeda	1	[{"added": {}}]	8	1
102	2024-09-12 02:01:44.492886+00	1	Seller: danielojeda	1	[{"added": {}}]	31	1
103	2024-09-12 02:58:34.26399+00	11	leonardovaldez - Créditos - Crédito Personal: Credit:1200.00, pending:40.00	3		28	1
104	2024-09-12 02:58:34.265494+00	6	JoseOjeda - Créditos - Crédito Personal: Credit:1200.00, pending:1200.00	3		28	1
105	2024-09-12 02:59:24.08009+00	18	Transaction object (18)	3		26	1
106	2024-09-12 02:59:24.081151+00	17	Transaction object (17)	3		26	1
107	2024-09-12 02:59:24.081982+00	16	Transaction object (16)	3		26	1
108	2024-09-12 02:59:24.082831+00	15	Transaction object (15)	3		26	1
109	2024-09-12 02:59:24.08358+00	14	Transaction object (14)	3		26	1
110	2024-09-12 03:03:38.976604+00	13	leonardovaldez - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	1
111	2024-09-12 03:22:03.305187+00	13	leonardovaldez - Créditos - Crédito Personal: Credit:1200.00, pending:1200.00	3		28	1
112	2024-09-12 03:22:21.834325+00	20	Transaction object (20)	3		26	1
113	2024-09-12 03:23:09.710927+00	14	leonardovaldez - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	1
114	2024-09-12 14:32:28.881512+00	14	leonardovaldez - Créditos - Crédito Personal: Credit:1200.00, pending:1200.00	3		28	1
115	2024-09-12 14:33:25.040241+00	11	JessicaSanchez	2	[{"changed": {"fields": ["Username"]}}]	25	1
116	2024-09-12 15:07:17.346973+00	15	JoseOjeda - Créditos - Crédito Personal: Credit:4000, pending:4000	1	[{"added": {}}]	28	1
117	2024-09-12 15:11:25.646146+00	22	Transaction object (22)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Yappy - Amount Paid: 120"}}]	26	1
118	2024-09-12 15:37:14.111199+00	15	JoseOjeda - Créditos - Crédito Personal: Credit:4000.00, pending:3880.00	3		28	1
119	2024-09-12 15:37:48.433198+00	22	Transaction object (22)	3		26	1
120	2024-09-12 15:37:48.434396+00	21	Transaction object (21)	3		26	1
121	2024-09-12 15:38:54.083758+00	16	leonardovaldez - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	1
122	2024-09-12 15:43:57.813059+00	24	Transaction object (24)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
123	2024-09-12 15:47:14.684411+00	25	Transaction object (25)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
124	2024-09-12 15:47:44.31577+00	25	Transaction object (25)	2	[{"changed": {"fields": ["Date"]}}]	26	1
125	2024-09-12 15:47:58.573091+00	25	Transaction object (25)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40.00", "fields": ["Payment code"]}}]	26	1
126	2024-09-12 15:51:38.173415+00	26	Transaction object (26)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
127	2024-09-12 15:52:36.936571+00	27	Transaction object (27)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	1
128	2024-09-12 15:52:50.71045+00	26	Transaction object (26)	2	[{"changed": {"fields": ["Category"]}}]	26	1
129	2024-09-12 23:54:17.107408+00	12	ZoilaOrtega	1	[{"added": {}}]	25	3
130	2024-09-12 23:55:31.218946+00	17	ZoilaOrtega - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
131	2024-09-12 23:59:11.024015+00	13	LisbethSoto	1	[{"added": {}}]	25	3
132	2024-09-12 23:59:48.530227+00	18	LisbethSoto - Créditos - Crédito Personal: Credit:525, pending:525	1	[{"added": {}}]	28	3
133	2024-09-13 00:00:58.423904+00	30	Transaction object (30)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
134	2024-09-13 00:05:22.639782+00	31	Transaction object (31)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 175"}}]	26	3
135	2024-09-13 00:05:49.327624+00	32	Transaction object (32)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
136	2024-09-13 00:13:08.707965+00	14	JorgeGonzales	1	[{"added": {}}]	25	3
137	2024-09-13 00:13:48.715844+00	19	JorgeGonzales - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
138	2024-09-13 00:15:26.31031+00	15	LeopoldoRamos	1	[{"added": {}}]	25	3
139	2024-09-13 00:15:56.623748+00	20	LeopoldoRamos - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
140	2024-09-13 00:18:17.802736+00	35	Transaction object (35)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
141	2024-09-13 00:18:49.236954+00	36	Transaction object (36)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
142	2024-09-13 00:23:52.103293+00	16	MereidaRodriguez	1	[{"added": {}}]	25	3
143	2024-09-13 00:24:31.137627+00	21	MereidaRodriguez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
144	2024-09-13 00:25:09.610246+00	17	EliaRosa	1	[{"added": {}}]	25	3
145	2024-09-13 00:25:55.327055+00	22	EliaRosa - Créditos - Crédito Personal: Credit:510, pending:510	1	[{"added": {}}]	28	3
146	2024-09-13 00:26:37.551851+00	39	Transaction object (39)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
147	2024-09-13 00:27:10.313316+00	40	Transaction object (40)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
148	2024-09-13 00:29:21.035185+00	18	MaximinoUnal	1	[{"added": {}}]	25	3
149	2024-09-13 00:29:50.334014+00	23	MaximinoUnal - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
150	2024-09-13 00:31:54.007648+00	19	MaricelEsther	1	[{"added": {}}]	25	3
151	2024-09-13 00:32:33.037593+00	24	MaricelEsther - Créditos - Crédito Personal: Credit:510, pending:510	1	[{"added": {}}]	28	3
152	2024-09-13 01:05:22.709415+00	43	Transaction object (43)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 167"}}]	26	3
153	2024-09-13 01:06:08.529874+00	44	Transaction object (44)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 167"}}]	26	3
154	2024-09-13 01:09:03.939415+00	20	OscarIvanMojica	1	[{"added": {}}]	25	3
155	2024-09-13 01:12:56.712989+00	25	OscarIvanMojica - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
156	2024-09-13 01:14:23.406005+00	21	Magdaxtra	1	[{"added": {}}]	25	3
157	2024-09-13 01:14:51.9503+00	26	Magdaxtra - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
158	2024-09-13 01:15:52.997183+00	47	Transaction object (47)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
159	2024-09-13 01:16:30.871221+00	48	Transaction object (48)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
160	2024-09-13 01:18:03.02633+00	22	JoseLuciano	1	[{"added": {}}]	25	3
161	2024-09-13 01:18:50.617759+00	27	JoseLuciano - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
162	2024-09-13 01:20:49.317437+00	23	JuanMendoza	1	[{"added": {}}]	25	3
163	2024-09-13 01:22:19.408969+00	28	JuanMendoza - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
164	2024-09-13 18:50:13.59721+00	24	LuisGonzales	1	[{"added": {}}]	25	3
165	2024-09-13 18:51:15.658604+00	29	LuisGonzales - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
166	2024-09-13 18:52:29.306876+00	30	MaximinoUnal - Créditos - Crédito Personal: Credit:100, pending:100	1	[{"added": {}}]	28	3
167	2024-09-13 18:53:28.452006+00	25	JavierInadeh	1	[{"added": {}}]	25	3
168	2024-09-13 19:54:40.400955+00	31	JavierInadeh - Créditos - Crédito de Consumo: Credit:50, pending:50	1	[{"added": {}}]	28	1
169	2024-09-13 19:59:02.928538+00	1	Inadeh	1	[{"added": {}}]	18	1
170	2024-09-13 21:05:38.440078+00	18	MaximinoMartinez	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	3
171	2024-09-13 21:06:52.422479+00	26	MaxMoreno	1	[{"added": {}}]	25	3
172	2024-09-13 21:07:38.432604+00	32	MaxMoreno - Créditos - Crédito de Consumo: Credit:50, pending:50	1	[{"added": {}}]	28	3
173	2024-09-13 21:08:54.597739+00	27	RobertoCarles	1	[{"added": {}}]	25	3
174	2024-09-13 21:09:18.825755+00	33	RobertoCarles - Créditos - Crédito de Consumo: Credit:50, pending:50	1	[{"added": {}}]	28	3
175	2024-09-13 21:09:58.19602+00	28	EliecerInadeh	1	[{"added": {}}]	25	3
176	2024-09-13 21:10:20.203649+00	34	EliecerInadeh - Créditos - Crédito de Consumo: Credit:50, pending:50	1	[{"added": {}}]	28	3
177	2024-09-13 21:11:29.904072+00	29	TomasAlbertoMartinez	1	[{"added": {}}]	25	3
178	2024-09-13 21:11:54.937641+00	35	TomasAlbertoMartinez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
179	2024-09-13 21:12:50.396675+00	30	AlbertoArocemena	1	[{"added": {}}]	25	3
180	2024-09-13 21:16:58.643795+00	36	AlbertoArocemena - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
181	2024-09-13 21:20:15.128447+00	31	EnockGuerra	1	[{"added": {}}]	25	3
182	2024-09-13 21:20:43.745346+00	37	EnockGuerra - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
183	2024-09-13 21:21:14.314641+00	32	GladysMontero	1	[{"added": {}}]	25	3
184	2024-09-13 21:21:34.541617+00	38	GladysMontero - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
185	2024-09-13 21:22:24.497948+00	33	CesarHernandez	1	[{"added": {}}]	25	3
186	2024-09-13 21:22:49.505302+00	39	CesarHernandez - Créditos - Crédito Personal: Credit:750, pending:750	1	[{"added": {}}]	28	3
187	2024-09-13 21:25:28.426552+00	34	SimonaDominguez	1	[{"added": {}}]	25	3
188	2024-09-13 21:25:49.556764+00	40	SimonaDominguez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
189	2024-09-13 21:27:32.626408+00	35	IdaniaBernalRuiz	1	[{"added": {}}]	25	3
190	2024-09-13 21:27:56.335203+00	41	IdaniaBernalRuiz - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
191	2024-09-13 21:28:27.398556+00	36	EdnaZulema	1	[{"added": {}}]	25	3
192	2024-09-13 21:28:46.594757+00	42	EdnaZulema - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
193	2024-09-13 21:29:45.910766+00	37	NoelRodriguez	1	[{"added": {}}]	25	3
194	2024-09-13 21:30:06.826987+00	43	NoelRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
195	2024-09-13 22:43:11.216175+00	38	ReinaldoVasquez	1	[{"added": {}}]	25	3
196	2024-09-13 22:43:30.817278+00	44	ReinaldoVasquez - Créditos - Crédito Personal: Credit:200, pending:200	1	[{"added": {}}]	28	3
197	2024-09-13 22:45:00.392998+00	39	MichaelAntonio	1	[{"added": {}}]	25	3
198	2024-09-13 22:45:29.134669+00	45	MichaelAntonio - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
199	2024-09-13 22:48:01.291337+00	40	Lazaro	1	[{"added": {}}]	25	3
200	2024-09-13 22:48:20.944754+00	46	Lazaro - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
201	2024-09-13 22:53:10.803466+00	41	LiceidaMartinez	1	[{"added": {}}]	25	3
202	2024-09-13 22:53:42.215087+00	47	LiceidaMartinez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
203	2024-09-13 22:54:54.395848+00	42	MariamTrejos	1	[{"added": {}}]	25	3
204	2024-09-13 22:55:17.983245+00	48	MariamTrejos - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
205	2024-09-13 22:56:55.71018+00	43	ClemenciaPerez	1	[{"added": {}}]	25	3
206	2024-09-13 22:57:15.613715+00	49	ClemenciaPerez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
207	2024-09-13 22:58:10.106709+00	44	GenaroRodriguez	1	[{"added": {}}]	25	3
208	2024-09-13 22:58:31.919099+00	50	GenaroRodriguez - Créditos - Crédito Personal: Credit:65, pending:65	1	[{"added": {}}]	28	3
209	2024-09-13 22:59:13.46956+00	45	OlmedoAlexy	1	[{"added": {}}]	25	3
210	2024-09-13 22:59:31.021293+00	51	OlmedoAlexy - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
211	2024-09-13 23:06:30.306697+00	46	JosephTrujillo	1	[{"added": {}}]	25	3
212	2024-09-13 23:06:54.426892+00	52	JosephTrujillo - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
213	2024-09-13 23:07:28.500834+00	47	NildaSanchez	1	[{"added": {}}]	25	3
214	2024-09-13 23:07:47.9082+00	53	NildaSanchez - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
215	2024-09-13 23:09:34.918916+00	48	JavierArosemena	1	[{"added": {}}]	25	3
216	2024-09-13 23:09:53.118346+00	54	JavierArosemena - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
217	2024-09-13 23:30:22.691853+00	49	ErickMartinez	1	[{"added": {}}]	25	3
218	2024-09-13 23:35:41.813657+00	55	ErickMartinez - Créditos - Crédito Personal: Credit:4200, pending:4200	1	[{"added": {}}]	28	3
219	2024-09-13 23:38:38.54135+00	50	IrisdelCarmen	1	[{"added": {}}]	25	3
220	2024-09-13 23:39:19.316172+00	56	IrisdelCarmen - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
221	2024-09-13 23:40:16.930777+00	79	Transaction object (79)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
222	2024-09-13 23:43:41.145179+00	80	Transaction object (80)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 375"}}]	26	3
223	2024-09-14 00:10:10.964018+00	51	JoseLuisFernandez	1	[{"added": {}}]	25	3
224	2024-09-14 00:10:55.225959+00	57	JoseLuisFernandez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
225	2024-09-14 00:48:32.983814+00	58	TomasAlbertoMartinez - Créditos - Crédito de Consumo: Credit:50, pending:50	1	[{"added": {}}]	28	3
226	2024-09-14 00:57:38.115759+00	52	LucianoMendoza	1	[{"added": {}}]	25	3
227	2024-09-14 00:57:56.80085+00	59	LucianoMendoza - Créditos - Crédito Personal: Credit:100, pending:100	1	[{"added": {}}]	28	3
228	2024-09-14 00:59:46.213832+00	53	JoseOrmelisArauz	1	[{"added": {}}]	25	3
229	2024-09-14 01:01:15.77623+00	53	JoseOrmelisArauz	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
230	2024-09-14 01:01:44.950664+00	60	JoseOrmelisArauz - Créditos - Crédito Personal: Credit:480, pending:480	1	[{"added": {}}]	28	3
231	2024-09-14 01:02:24.235417+00	15	LeopoldoRamos	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
232	2024-09-14 01:02:43.228908+00	61	LeopoldoRamos - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
233	2024-09-14 01:03:35.306202+00	54	MariaLuisaVillanueva	1	[{"added": {}}]	25	3
234	2024-09-14 01:03:56.878364+00	62	MariaLuisaVillanueva - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
235	2024-09-14 01:04:37.500014+00	52	LucianoMendoza	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
236	2024-09-14 01:04:52.123979+00	51	JoseLuisFernandez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
237	2024-09-14 01:05:03.721125+00	49	ErickMartinez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
238	2024-09-14 01:05:16.628313+00	48	JavierArosemena	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
239	2024-09-14 01:05:26.910399+00	47	NildaSanchez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
240	2024-09-14 01:05:41.60347+00	46	JosephTrujillo	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
241	2024-09-14 01:05:55.115901+00	45	OlmedoAlexy	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
242	2024-09-14 01:06:05.326144+00	44	GenaroRodriguez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
243	2024-09-14 01:06:18.534618+00	43	ClemenciaPerez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
244	2024-09-14 01:06:29.878597+00	42	MariamTrejos	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
245	2024-09-14 01:06:40.511971+00	41	LiceidaMartinez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
246	2024-09-14 01:06:55.024919+00	4	DarioDominguez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
247	2024-09-14 01:07:06.419114+00	24	LuisGonzales	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
248	2024-09-14 01:07:17.514283+00	31	EnockGuerra	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
249	2024-09-14 01:07:36.208939+00	39	MichelAntonio	2	[{"changed": {"fields": ["Username", "First name", "Last name"]}}]	25	3
250	2024-09-14 01:07:46.457209+00	38	ReinaldoVasquez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
251	2024-09-14 01:07:57.316995+00	37	NoelRodriguez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
252	2024-09-14 01:08:08.315767+00	36	EdnaZulema	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
253	2024-09-14 01:12:06.726708+00	35	IdaniaBernalRuiz	2	[{"changed": {"fields": ["Last name"]}}]	25	3
254	2024-09-14 01:12:28.023266+00	6	SeleneIbarra	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
255	2024-09-14 01:12:50.209317+00	9	MariaMartinez	2	[{"changed": {"fields": ["First name", "Last name"]}}]	25	3
256	2024-09-14 01:18:30.709578+00	55	WuendyRangel	1	[{"added": {}}]	25	3
257	2024-09-14 01:18:54.688478+00	63	WuendyRangel - Créditos - Crédito Personal: Credit:260, pending:260	1	[{"added": {}}]	28	3
258	2024-09-14 01:19:41.105371+00	56	BiancaCoronado	1	[{"added": {}}]	25	3
259	2024-09-14 01:19:57.988001+00	64	BiancaCoronado - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
260	2024-09-14 01:21:38.879993+00	57	SantanaPanaderia	1	[{"added": {}}]	25	3
261	2024-09-14 01:21:54.896121+00	65	SantanaPanaderia - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
262	2024-09-14 01:22:38.869062+00	58	MarinaMoreno	1	[{"added": {}}]	25	3
263	2024-09-14 01:22:56.439465+00	66	MarinaMoreno - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
264	2024-09-14 01:23:34.97939+00	23	JuanMendoza	2	[]	25	3
265	2024-09-14 01:23:53.779189+00	67	JuanMendoza - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
266	2024-09-14 01:26:10.126278+00	68	MariaMartinez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
267	2024-09-14 01:26:51.032766+00	59	Ubaldo	1	[{"added": {}}]	25	3
268	2024-09-14 01:27:08.278421+00	69	Ubaldo - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
269	2024-09-14 01:28:36.376309+00	71	TomasAlbertoMartinez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
270	2024-09-14 01:29:14.120883+00	60	JeisonOviedo	1	[{"added": {}}]	25	3
271	2024-09-14 01:29:34.115058+00	72	JeisonOviedo - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
272	2024-09-14 01:29:35.703089+00	2	Unal	1	[{"added": {}}]	18	1
273	2024-09-14 01:29:43.815654+00	18	MaximinoMartinez	2	[{"changed": {"fields": ["Label", "Groups"]}}]	25	1
274	2024-09-14 01:30:27.905806+00	61	AlvaroAlexis	1	[{"added": {}}]	25	3
275	2024-09-14 01:30:46.308157+00	73	AlvaroAlexis - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
276	2024-09-14 01:32:12.804472+00	62	CarlosArturo	1	[{"added": {}}]	25	3
277	2024-09-14 01:32:34.22625+00	74	CarlosArturo - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
278	2024-09-14 01:33:28.52113+00	63	JorgeReyes	1	[{"added": {}}]	25	3
279	2024-09-14 01:34:04.504057+00	75	JorgeReyes - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
280	2024-09-14 01:35:14.713386+00	64	RogelioCorro	1	[{"added": {}}]	25	3
281	2024-09-14 01:35:49.320537+00	76	RogelioCorro - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
282	2024-09-14 01:36:54.80993+00	65	MariamDelosAngeles	1	[{"added": {}}]	25	3
283	2024-09-14 01:37:14.782584+00	77	MariamDelosAngeles - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
284	2024-09-14 17:45:26.900822+00	102	Transaction object (102)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
285	2024-09-14 17:46:10.215822+00	103	Transaction object (103)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
286	2024-09-14 17:49:21.220431+00	104	Transaction object (104)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
287	2024-09-14 17:50:06.844338+00	105	Transaction object (105)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
288	2024-09-14 17:50:41.216274+00	106	Transaction object (106)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
289	2024-09-14 17:56:05.010409+00	66	IgnacioVega	1	[{"added": {}}]	25	3
290	2024-09-14 17:56:29.515546+00	78	IgnacioVega - Créditos - Crédito Personal: Credit:315, pending:315	1	[{"added": {}}]	28	3
291	2024-09-14 17:59:54.901188+00	67	FernandoMorales	1	[{"added": {}}]	25	3
292	2024-09-14 18:00:23.323891+00	79	FernandoMorales - Créditos - Crédito Personal: Credit:345, pending:345	1	[{"added": {}}]	28	3
293	2024-09-14 18:01:23.715886+00	68	AlejandroPinto	1	[{"added": {}}]	25	3
294	2024-09-14 18:01:54.318666+00	80	AlejandroPinto - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
295	2024-09-14 18:14:08.703226+00	69	ReinaldoAlto	1	[{"added": {}}]	25	3
296	2024-09-14 18:14:49.212957+00	81	ReinaldoAlto - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
297	2024-09-14 18:16:17.124675+00	111	Transaction object (111)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 37.5"}}]	26	3
298	2024-09-14 18:17:00.724372+00	112	Transaction object (112)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 37.5"}}]	26	3
299	2024-09-14 18:17:39.524781+00	113	Transaction object (113)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
300	2024-09-14 18:55:58.224168+00	114	Transaction object (114)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 37.5"}}]	26	3
301	2024-09-14 19:52:46.844966+00	70	CarlosMeneses	1	[{"added": {}}]	25	3
302	2024-09-14 19:53:12.817209+00	82	CarlosMeneses - Créditos - Crédito Personal: Credit:220, pending:220	1	[{"added": {}}]	28	3
303	2024-09-14 19:58:17.089259+00	71	ErickMagallon	1	[{"added": {}}]	25	3
304	2024-09-14 19:58:41.848672+00	83	ErickMagallon - Créditos - Crédito Personal: Credit:630, pending:630	1	[{"added": {}}]	28	3
305	2024-09-14 20:02:17.985672+00	117	Transaction object (117)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 200"}}]	26	3
306	2024-09-14 20:03:08.545201+00	72	JhonnyReyes	1	[{"added": {}}]	25	3
307	2024-09-14 20:03:42.317354+00	84	JhonnyReyes - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
308	2024-09-14 20:04:29.393712+00	73	AriadnaItzel	1	[{"added": {}}]	25	3
309	2024-09-14 20:04:58.90745+00	85	AriadnaItzel - Créditos - Crédito Personal: Credit:560, pending:560	1	[{"added": {}}]	28	3
310	2024-09-14 21:12:33.11088+00	120	Transaction object (120)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
311	2024-09-14 21:13:07.803003+00	121	Transaction object (121)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
312	2024-09-14 21:13:57.215445+00	122	Transaction object (122)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
313	2024-09-14 21:21:50.116109+00	86	NoelRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
314	2024-09-14 21:23:03.599056+00	74	ElianysMora	1	[{"added": {}}]	25	3
315	2024-09-14 21:25:33.807056+00	87	ElianysMora - Créditos - Crédito Personal: Credit:380, pending:380	1	[{"added": {}}]	28	3
316	2024-09-14 21:25:52.015097+00	86	NoelRodriguez - Créditos - Crédito Personal: Credit:140.00, pending:140.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
317	2024-09-14 21:27:13.289771+00	75	AnnaMares	1	[{"added": {}}]	25	3
318	2024-09-14 21:27:41.432484+00	88	AnnaMares - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
319	2024-09-14 21:34:30.419413+00	126	Transaction object (126)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
320	2024-09-14 21:36:03.312847+00	127	Transaction object (127)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 95"}}]	26	3
321	2024-09-14 21:36:56.211297+00	128	Transaction object (128)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 95"}}]	26	3
322	2024-09-14 21:38:07.312007+00	129	Transaction object (129)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
323	2024-09-14 21:38:40.503116+00	130	Transaction object (130)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
324	2024-09-14 21:59:02.117666+00	131	Transaction object (131)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
325	2024-09-14 22:00:01.711523+00	89	JoseLuisFernandez - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
326	2024-09-14 22:01:53.619881+00	133	Transaction object (133)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
327	2024-09-14 22:03:07.828632+00	134	Transaction object (134)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
328	2024-09-14 22:09:06.207285+00	76	YesirethIbarra	1	[{"added": {}}]	25	3
329	2024-09-14 22:09:37.139684+00	90	YesirethIbarra - Créditos - Pago a Crédito Personal: Credit:740, pending:740	1	[{"added": {}}]	28	3
330	2024-09-14 22:49:57.698505+00	77	EfrainMora	1	[{"added": {}}]	25	3
331	2024-09-14 22:50:27.638702+00	91	EfrainMora - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
332	2024-09-14 22:51:28.808631+00	78	JoséSamuelQuiroz	1	[{"added": {}}]	25	3
333	2024-09-14 22:51:51.104074+00	92	JoséSamuelQuiroz - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
334	2024-09-14 22:52:59.602589+00	138	Transaction object (138)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
335	2024-09-14 23:39:15.333179+00	93	GladysMontero - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
336	2024-09-14 23:44:22.274131+00	94	RogelioCorro - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
337	2024-09-14 23:44:53.094101+00	79	AndysMartinez	1	[{"added": {}}]	25	3
338	2024-09-14 23:45:15.234083+00	95	AndysMartinez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
339	2024-09-14 23:46:05.815304+00	98	ErickMartinez - Créditos - Crédito Personal: Credit:5600, pending:5600	1	[{"added": {}}]	28	3
340	2024-09-14 23:47:09.171095+00	103	LuisGonzales - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
341	2024-09-14 23:49:45.506432+00	80	MarioBetancur	1	[{"added": {}}]	25	3
342	2024-09-14 23:49:59.097948+00	104	MarioBetancur - Créditos - Crédito Personal: Credit:375, pending:375	1	[{"added": {}}]	28	3
343	2024-09-14 23:50:35.197704+00	81	JhonatanSegundo	1	[{"added": {}}]	25	3
344	2024-09-14 23:50:52.632627+00	105	JhonatanSegundo - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
345	2024-09-14 23:51:25.006587+00	106	SeleneNovio - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
346	2024-09-14 23:53:04.915051+00	153	Transaction object (153)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 2.5"}}]	26	3
347	2024-09-15 00:01:39.897532+00	82	ManuelSanchez	1	[{"added": {}}]	25	3
348	2024-09-15 00:02:02.713334+00	107	ManuelSanchez - Créditos - Crédito Personal: Credit:225, pending:225	1	[{"added": {}}]	28	3
349	2024-09-15 00:05:25.614313+00	83	OmairaCuava	1	[{"added": {}}]	25	3
350	2024-09-15 00:05:50.73303+00	108	OmairaCuava - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
351	2024-09-15 00:13:11.79774+00	156	Transaction object (156)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
352	2024-09-15 00:14:16.738051+00	157	Transaction object (157)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
353	2024-09-15 00:15:01.926599+00	158	Transaction object (158)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
354	2024-09-15 00:22:45.995462+00	84	MiguelOrdoñez	1	[{"added": {}}]	25	3
355	2024-09-15 00:23:12.526649+00	109	MiguelOrdoñez - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
356	2024-09-15 00:23:58.017203+00	85	DanitzaAguilar	1	[{"added": {}}]	25	3
357	2024-09-15 00:24:20.242388+00	110	DanitzaAguilar - Créditos - Crédito Personal: Credit:540, pending:540	1	[{"added": {}}]	28	3
358	2024-09-15 00:31:20.946167+00	161	Transaction object (161)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
359	2024-09-15 00:31:39.32387+00	162	Transaction object (162)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
360	2024-09-15 00:32:14.338016+00	162	Transaction object (162)	2	[{"changed": {"fields": ["User"]}}, {"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130", "fields": ["Amount", "Amount paid", "Credit"]}}]	26	3
361	2024-09-15 00:34:47.414663+00	86	DalvisMendoza	1	[{"added": {}}]	25	3
362	2024-09-15 00:35:17.524264+00	111	DalvisMendoza - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
363	2024-09-15 00:39:42.513698+00	87	JhonatanAguilar	1	[{"added": {}}]	25	3
364	2024-09-15 00:40:13.113757+00	112	JhonatanAguilar - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
365	2024-09-15 00:42:08.597034+00	88	OscarMegaexpress	1	[{"added": {}}]	25	3
366	2024-09-15 00:42:29.243425+00	113	OscarMegaexpress - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
367	2024-09-15 00:45:49.697536+00	89	NicolasMeneses	1	[{"added": {}}]	25	3
368	2024-09-15 00:46:30.597303+00	90	GeidyDominguez	1	[{"added": {}}]	25	3
369	2024-09-15 00:46:57.819231+00	114	GeidyDominguez - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
370	2024-09-15 00:47:40.714459+00	115	NicolasMeneses - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
371	2024-09-15 00:49:02.827022+00	168	Transaction object (168)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
475	2024-09-19 19:17:25.596896+00	115	YarisnethCárdenas	1	[{"added": {}}]	25	3
372	2024-09-15 00:50:02.658909+00	169	Transaction object (169)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
373	2024-09-15 00:57:31.395381+00	91	AuraSotiyo	1	[{"added": {}}]	25	3
374	2024-09-15 00:57:53.334013+00	116	AuraSotiyo - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
375	2024-09-15 00:58:56.299156+00	171	Transaction object (171)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
376	2024-09-15 01:09:48.314327+00	172	Transaction object (172)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
377	2024-09-15 01:11:58.118297+00	92	JaiberBusito	1	[{"added": {}}]	25	3
378	2024-09-15 01:12:29.033923+00	117	JaiberBusito - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
379	2024-09-15 01:15:52.811077+00	174	Transaction object (174)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
380	2024-09-15 01:17:35.602311+00	93	PublioProfe	1	[{"added": {}}]	25	3
381	2024-09-15 01:18:41.155288+00	118	PublioProfe - Créditos - Crédito Personal: Credit:450, pending:450	1	[{"added": {}}]	28	3
382	2024-09-15 01:19:53.930069+00	94	JoseSanchez	1	[{"added": {}}]	25	3
383	2024-09-15 01:20:59.634379+00	119	JoseSanchez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
384	2024-09-15 01:21:53.517011+00	95	GabrielaGuerrero	1	[{"added": {}}]	25	3
385	2024-09-15 01:22:28.434382+00	120	GabrielaGuerrero - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
386	2024-09-15 01:42:22.908896+00	96	CompañerodeNelson	1	[{"added": {}}]	25	3
387	2024-09-15 01:42:48.032248+00	121	CompañerodeNelson - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
388	2024-09-15 01:43:39.507984+00	97	AristidesMartinez	1	[{"added": {}}]	25	3
389	2024-09-15 01:44:12.621664+00	122	AristidesMartinez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
390	2024-09-15 01:47:20.096442+00	98	MariaTuñon	1	[{"added": {}}]	25	3
391	2024-09-15 01:48:00.808355+00	123	MariaTuñon - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
392	2024-09-15 01:48:49.109795+00	99	ChristianDomínguez	1	[{"added": {}}]	25	3
393	2024-09-15 01:49:11.110702+00	124	ChristianDomínguez - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
394	2024-09-15 01:49:51.606334+00	100	GladysPerez	1	[{"added": {}}]	25	3
395	2024-09-15 01:50:55.599366+00	125	GladysPerez - Créditos - Crédito Personal: Credit:110, pending:110	1	[{"added": {}}]	28	3
396	2024-09-15 01:51:59.907956+00	101	IndiraSanchez	1	[{"added": {}}]	25	3
397	2024-09-15 01:52:19.699004+00	126	IndiraSanchez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
398	2024-09-17 17:23:26.836449+00	51	joseluisfernandez	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	1
399	2024-09-17 22:07:26.232917+00	102	ChristianDominguez	1	[{"added": {}}]	25	3
400	2024-09-17 22:07:58.22316+00	127	LisbethSoto - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
401	2024-09-17 22:09:41.193449+00	185	Transaction object (185)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
402	2024-09-17 22:10:40.334381+00	128	JoséSamuelQuiroz - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
403	2024-09-17 22:10:53.211852+00	127	LisbethSoto - Créditos - Crédito Personal: Credit:600, pending:140.00	2	[{"changed": {"fields": ["Cost", "Price", "Credit days"]}}]	28	3
404	2024-09-17 22:12:22.097357+00	129	ChristianDominguez - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
405	2024-09-17 22:18:07.621599+00	188	Transaction object (188)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
406	2024-09-17 22:26:52.313567+00	130	OscarMegaexpress - Créditos - Crédito Personal: Credit:240, pending:240	1	[{"added": {}}]	28	3
407	2024-09-17 22:28:22.224326+00	190	Transaction object (190)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
408	2024-09-17 22:29:19.552104+00	191	Transaction object (191)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 32.5"}}]	26	3
409	2024-09-17 22:30:19.00185+00	103	JorgeCamel	1	[{"added": {}}]	25	3
410	2024-09-17 22:30:43.328828+00	131	JorgeCamel - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
411	2024-09-17 22:32:50.602598+00	193	Transaction object (193)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
412	2024-09-17 22:33:43.822855+00	194	Transaction object (194)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
413	2024-09-17 22:34:46.108832+00	195	Transaction object (195)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 200"}}]	26	3
414	2024-09-17 22:36:14.034447+00	196	Transaction object (196)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
415	2024-09-17 23:02:41.377336+00	132	AnnaMares - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
416	2024-09-17 23:03:27.107301+00	134	MichelAntonio - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
417	2024-09-17 23:21:31.729766+00	200	Transaction object (200)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
418	2024-09-17 23:24:08.111617+00	104	ArielHernandez	1	[{"added": {}}]	25	3
419	2024-09-17 23:24:35.013714+00	135	ArielHernandez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
420	2024-09-17 23:25:24.012482+00	105	Elcutty	1	[{"added": {}}]	25	3
421	2024-09-17 23:25:52.788729+00	136	Elcutty - Créditos - Crédito Personal: Credit:315, pending:315	1	[{"added": {}}]	28	3
422	2024-09-17 23:30:39.096429+00	203	Transaction object (203)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
423	2024-09-17 23:31:20.173878+00	204	Transaction object (204)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 167"}}]	26	3
424	2024-09-17 23:32:02.72778+00	205	Transaction object (205)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
425	2024-09-17 23:33:34.486759+00	206	Transaction object (206)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
426	2024-09-17 23:34:20.106741+00	207	Transaction object (207)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
427	2024-09-17 23:41:35.604349+00	106	ElizabethVayVen	1	[{"added": {}}]	25	3
428	2024-09-17 23:42:11.72149+00	137	ElizabethVayVen - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
429	2024-09-17 23:43:29.581464+00	209	Transaction object (209)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
430	2024-09-17 23:44:11.732374+00	210	Transaction object (210)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 250"}}]	26	3
431	2024-09-17 23:44:54.613274+00	211	Transaction object (211)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
432	2024-09-17 23:49:20.425083+00	212	Transaction object (212)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
433	2024-09-17 23:55:06.621879+00	213	Transaction object (213)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
434	2024-09-17 23:55:53.227537+00	214	Transaction object (214)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
435	2024-09-17 23:56:19.27987+00	213	Transaction object (213)	2	[{"changed": {"fields": ["Category"]}}]	26	3
436	2024-09-17 23:56:52.692161+00	107	DelfinaReyes	1	[{"added": {}}]	25	3
437	2024-09-17 23:57:09.127773+00	138	DelfinaReyes - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
438	2024-09-17 23:59:22.123019+00	216	Transaction object (216)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
439	2024-09-18 00:00:17.011482+00	217	Transaction object (217)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
440	2024-09-18 00:01:10.347283+00	218	Transaction object (218)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
441	2024-09-18 00:02:44.305825+00	108	JuanAguilar	1	[{"added": {}}]	25	3
442	2024-09-18 00:03:08.805769+00	139	JuanAguilar - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
443	2024-09-18 00:03:50.605499+00	109	CesarRodriguez	1	[{"added": {}}]	25	3
444	2024-09-18 00:04:17.023839+00	140	CesarRodriguez - Créditos - Crédito Personal: Credit:180, pending:180	1	[{"added": {}}]	28	3
445	2024-09-18 00:06:17.140231+00	110	BelisarioRodriguez	1	[{"added": {}}]	25	3
446	2024-09-18 00:06:38.581528+00	141	BelisarioRodriguez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
447	2024-09-18 00:07:16.439317+00	142	AristidesMartinez - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
448	2024-09-18 00:08:41.160761+00	143	MariaTuñon - Créditos - Crédito Personal: Credit:115, pending:115	1	[{"added": {}}]	28	3
449	2024-09-18 00:09:31.524328+00	111	CarlosKike	1	[{"added": {}}]	25	3
450	2024-09-18 00:09:47.180194+00	144	CarlosKike - Créditos - Crédito Personal: Credit:65, pending:65	1	[{"added": {}}]	28	3
451	2024-09-18 00:10:59.132781+00	225	Transaction object (225)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 180"}}]	26	3
452	2024-09-18 00:18:23.537447+00	226	Transaction object (226)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
453	2024-09-18 00:19:32.81831+00	227	Transaction object (227)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
454	2024-09-18 00:20:53.127632+00	228	Transaction object (228)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
455	2024-09-18 00:21:36.000531+00	229	Transaction object (229)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
456	2024-09-18 00:22:47.626589+00	230	Transaction object (230)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
457	2024-09-18 00:25:58.909809+00	112	ErwuinMartinez	1	[{"added": {}}]	25	3
458	2024-09-18 00:26:23.599641+00	145	ErwuinMartinez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
459	2024-09-18 00:27:31.310273+00	232	Transaction object (232)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
460	2024-09-18 00:29:32.504842+00	113	Advasadiermatatan	1	[{"added": {}}]	25	3
461	2024-09-18 00:30:09.724107+00	146	Advasadiermatatan - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
462	2024-09-18 00:31:33.819921+00	234	Transaction object (234)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
463	2024-09-18 00:34:03.610504+00	235	Transaction object (235)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
464	2024-09-19 18:58:08.342438+00	236	Transaction object (236)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
465	2024-09-19 18:58:59.575471+00	237	Transaction object (237)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
466	2024-09-19 19:00:37.235536+00	238	Transaction object (238)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
467	2024-09-19 19:02:59.684521+00	239	Transaction object (239)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
468	2024-09-19 19:08:26.802461+00	114	LeidyamPanaderia	1	[{"added": {}}]	25	3
469	2024-09-19 19:08:51.336268+00	147	LeidyamPanaderia - Créditos - Crédito Personal: Credit:501, pending:501	1	[{"added": {}}]	28	3
470	2024-09-19 19:10:35.506664+00	241	Transaction object (241)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
471	2024-09-19 19:11:48.030926+00	148	EdnaZulema - Créditos - Crédito Personal: Credit:200, pending:200	1	[{"added": {}}]	28	3
472	2024-09-19 19:12:26.933919+00	149	MereidaRodriguez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
473	2024-09-19 19:14:21.221572+00	244	Transaction object (244)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 450"}}]	26	3
474	2024-09-19 19:16:08.596645+00	150	PublioProfe - Créditos - Crédito Personal: Credit:800, pending:800	1	[{"added": {}}]	28	3
476	2024-09-19 19:17:51.324061+00	151	YarisnethCárdenas - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
477	2024-09-19 19:20:04.23781+00	247	Transaction object (247)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
478	2024-09-19 19:21:07.229109+00	248	Transaction object (248)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
479	2024-09-19 19:30:21.154393+00	247	Transaction object (247)	2	[{"changed": {"fields": ["Category"]}}]	26	3
480	2024-09-19 19:32:02.547385+00	249	Transaction object (249)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
481	2024-09-19 19:35:45.61542+00	250	Transaction object (250)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
482	2024-09-19 19:36:39.428688+00	251	Transaction object (251)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
483	2024-09-19 19:39:41.151967+00	252	Transaction object (252)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 500"}}]	26	3
484	2024-09-19 19:41:14.726338+00	253	Transaction object (253)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
485	2024-09-19 19:42:07.708962+00	254	Transaction object (254)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
486	2024-09-19 19:42:59.849457+00	255	Transaction object (255)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
487	2024-09-19 19:44:20.119193+00	116	Bernabethaguilar	1	[{"added": {}}]	25	3
488	2024-09-19 19:45:46.416376+00	152	Bernabethaguilar - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
489	2024-09-19 19:46:44.729855+00	153	TomasAlbertoMartinez - Créditos - Crédito Personal: Credit:400, pending:400	1	[{"added": {}}]	28	3
490	2024-09-19 19:47:35.747914+00	154	SimonaDominguez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
491	2024-09-19 19:48:28.994712+00	155	RogelioCorro - Créditos - Crédito Personal: Credit:800, pending:800	1	[{"added": {}}]	28	3
492	2024-09-19 19:49:11.295329+00	117	EliasPérez	1	[{"added": {}}]	25	3
493	2024-09-19 19:49:52.72615+00	156	EliasPérez - Créditos - Crédito Personal: Credit:345, pending:345	1	[{"added": {}}]	28	3
494	2024-09-19 19:50:43.070458+00	261	Transaction object (261)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
495	2024-09-19 19:51:25.531704+00	262	Transaction object (262)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
496	2024-09-19 19:53:12.32627+00	263	Transaction object (263)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
497	2024-09-19 19:53:46.305996+00	264	Transaction object (264)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
498	2024-09-19 19:54:22.049541+00	265	Transaction object (265)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
499	2024-09-19 19:55:03.938105+00	266	Transaction object (266)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
500	2024-09-19 23:42:20.019183+00	118	JamilethDominguez	1	[{"added": {}}]	25	3
501	2024-09-19 23:43:26.684796+00	157	JamilethDominguez - Créditos - Crédito Personal: Credit:408, pending:408	1	[{"added": {}}]	28	3
502	2024-09-19 23:47:35.4222+00	268	Transaction object (268)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
503	2024-09-19 23:48:18.986318+00	269	Transaction object (269)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
504	2024-09-19 23:49:03.233535+00	270	Transaction object (270)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
505	2024-09-19 23:49:55.409116+00	271	Transaction object (271)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
506	2024-09-19 23:50:25.582277+00	270	Transaction object (270)	2	[{"changed": {"fields": ["Category"]}}]	26	3
507	2024-09-19 23:50:53.928403+00	269	Transaction object (269)	2	[{"changed": {"fields": ["Category"]}}]	26	3
508	2024-09-19 23:51:20.232461+00	268	Transaction object (268)	2	[{"changed": {"fields": ["Category"]}}]	26	3
509	2024-09-19 23:51:51.707649+00	267	Transaction object (267)	2	[{"changed": {"fields": ["Category"]}}]	26	3
510	2024-09-19 23:52:41.213919+00	272	Transaction object (272)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
511	2024-09-19 23:53:30.627899+00	273	Transaction object (273)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
512	2024-09-19 23:54:16.296288+00	274	Transaction object (274)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
513	2024-09-19 23:54:55.77623+00	275	Transaction object (275)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
514	2024-09-19 23:55:36.213661+00	276	Transaction object (276)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
515	2024-09-19 23:56:38.642901+00	277	Transaction object (277)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
516	2024-09-19 23:59:42.028982+00	278	Transaction object (278)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Banesco - Amount Paid: 20"}}]	26	3
517	2024-09-20 00:00:18.785484+00	279	Transaction object (279)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
518	2024-09-20 00:14:42.454305+00	157	JamilethDominguez - Créditos - Crédito Personal: Credit:408.00, pending:178.00	2	[{"changed": {"fields": ["Description"]}}]	28	3
519	2024-09-20 00:51:59.910595+00	119	MaximilianoMoreno	1	[{"added": {}}]	25	3
520	2024-09-20 00:52:41.718088+00	158	MaximilianoMoreno - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
521	2024-09-20 00:53:42.623593+00	281	Transaction object (281)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
522	2024-09-20 00:54:20.6346+00	282	Transaction object (282)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
523	2024-09-20 18:29:53.333032+00	120	VictorExtar	1	[{"added": {}}]	25	3
524	2024-09-20 18:30:32.621819+00	159	VictorExtar - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
525	2024-09-20 18:49:41.034108+00	284	Transaction object (284)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
526	2024-09-20 18:50:27.526635+00	285	Transaction object (285)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
527	2024-09-20 19:00:42.536854+00	160	RobertoCarles - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
528	2024-09-20 20:10:51.754435+00	121	MorrisProfesor	1	[{"added": {}}]	25	3
529	2024-09-20 20:11:36.696447+00	161	MorrisProfesor - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	3
530	2024-09-20 20:12:21.607024+00	288	Transaction object (288)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 300"}}]	26	3
531	2024-09-20 20:13:56.227522+00	122	Lidia	1	[{"added": {}}]	25	3
532	2024-09-20 20:14:33.465394+00	162	Lidia - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
533	2024-09-20 20:23:16.654643+00	290	Transaction object (290)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
534	2024-09-20 20:24:29.573353+00	291	Transaction object (291)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
535	2024-09-20 20:25:43.612206+00	292	Transaction object (292)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
536	2024-09-20 20:27:01.130505+00	123	GemaGonzález	1	[{"added": {}}]	25	3
537	2024-09-20 20:27:47.271791+00	163	GemaGonzález - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
538	2024-09-20 20:29:10.101262+00	124	DorisAguilar	1	[{"added": {}}]	25	3
539	2024-09-20 20:29:39.333554+00	164	DorisAguilar - Créditos - Crédito Personal: Credit:180, pending:180	1	[{"added": {}}]	28	3
540	2024-09-20 20:30:38.516519+00	295	Transaction object (295)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
541	2024-09-20 20:38:32.927684+00	165	RobertoCarles - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
542	2024-09-20 20:39:26.889561+00	297	Transaction object (297)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
543	2024-09-20 20:40:50.618043+00	166	RobertoCarles - Créditos - Crédito Personal: Credit:480, pending:480	1	[{"added": {}}]	28	3
544	2024-09-20 20:41:37.2368+00	299	Transaction object (299)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
545	2024-09-20 20:42:26.097487+00	300	Transaction object (300)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
546	2024-09-20 20:43:40.673032+00	301	Transaction object (301)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
547	2024-09-20 21:05:25.414302+00	5	Gastos de actividad - Viaticos - 420	1	[{"added": {}}]	27	3
548	2024-09-20 22:27:03.268842+00	167	ElizabethVayVen - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
549	2024-09-20 22:28:47.098476+00	303	Transaction object (303)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
550	2024-09-20 22:29:45.85265+00	304	Transaction object (304)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
551	2024-09-20 22:31:14.958551+00	305	Transaction object (305)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 300"}}]	26	3
552	2024-09-20 22:32:15.50257+00	125	MariaKarla	1	[{"added": {}}]	25	3
553	2024-09-20 22:32:35.467321+00	168	MariaKarla - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
554	2024-09-20 22:34:22.432211+00	126	YoannaRodriguez	1	[{"added": {}}]	25	3
555	2024-09-20 22:34:42.719624+00	169	YoannaRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
556	2024-09-20 22:36:40.45306+00	308	Transaction object (308)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
557	2024-09-20 22:38:18.096846+00	309	Transaction object (309)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
558	2024-09-20 22:39:54.807519+00	310	Transaction object (310)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
559	2024-09-20 22:42:30.03036+00	127	MariaIsidora	1	[{"added": {}}]	25	3
560	2024-09-20 22:46:34.065637+00	170	MariaIsidora - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
561	2024-09-20 22:47:56.720757+00	312	Transaction object (312)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
562	2024-09-20 22:48:34.698998+00	313	Transaction object (313)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
563	2024-09-20 22:49:06.367653+00	314	Transaction object (314)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
564	2024-09-20 22:53:16.701083+00	128	LuisGomez	1	[{"added": {}}]	25	3
565	2024-09-20 22:53:38.127903+00	171	LuisGomez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
566	2024-09-20 22:54:06.380681+00	172	ZoilaOrtega - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
567	2024-09-20 22:55:05.285145+00	317	Transaction object (317)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
568	2024-09-20 22:55:52.712061+00	318	Transaction object (318)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
569	2024-09-20 22:56:35.450634+00	319	Transaction object (319)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
570	2024-09-21 21:00:42.746944+00	320	Transaction object (320)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
571	2024-09-21 21:01:34.542598+00	321	Transaction object (321)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
572	2024-09-21 21:02:14.65796+00	173	RobertoCarles - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
573	2024-09-21 21:03:49.813576+00	323	Transaction object (323)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
574	2024-09-21 21:06:57.442624+00	174	EliecerInadeh - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
575	2024-09-21 21:08:20.027751+00	325	Transaction object (325)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
576	2024-09-21 21:09:30.631242+00	129	YanCarlos	1	[{"added": {}}]	25	3
577	2024-09-21 21:09:51.736908+00	175	YanCarlos - Créditos - Crédito Personal: Credit:180, pending:180	1	[{"added": {}}]	28	3
578	2024-09-21 21:10:36.409993+00	327	Transaction object (327)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
579	2024-09-21 21:11:16.207662+00	328	Transaction object (328)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
580	2024-09-21 21:12:54.199585+00	130	EsposaJoseSanchez	1	[{"added": {}}]	25	3
581	2024-09-21 21:13:19.214399+00	176	EsposaJoseSanchez - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
582	2024-09-23 18:33:58.198359+00	131	OmeidaJubilada	1	[{"added": {}}]	25	3
583	2024-09-23 18:34:32.299408+00	177	OmeidaJubilada - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
584	2024-09-23 18:38:28.225963+00	331	Transaction object (331)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
585	2024-09-23 18:39:18.229924+00	332	Transaction object (332)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
586	2024-09-23 18:40:04.225792+00	333	Transaction object (333)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
587	2024-09-23 18:49:59.552562+00	334	Transaction object (334)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 32.5"}}]	26	3
588	2024-09-23 18:50:43.449929+00	335	Transaction object (335)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
589	2024-09-23 18:51:20.023158+00	336	Transaction object (336)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
590	2024-09-23 18:52:07.942521+00	178	ManuelSanchez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
591	2024-09-23 18:53:04.06274+00	179	CarlosKike - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
592	2024-09-23 18:57:02.233933+00	339	Transaction object (339)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
593	2024-09-23 18:58:00.807062+00	340	Transaction object (340)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
594	2024-09-23 18:58:58.229619+00	6	Gastos de actividad - Viaticos - 11	1	[{"added": {}}]	27	3
595	2024-09-23 19:23:04.197762+00	341	Transaction object (341)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
596	2024-09-23 19:24:04.013243+00	132	OrielBanismo	1	[{"added": {}}]	25	3
597	2024-09-23 19:24:23.492946+00	180	OrielBanismo - Créditos - Crédito Personal: Credit:30, pending:30	1	[{"added": {}}]	28	3
598	2024-09-23 19:25:03.115476+00	133	EdgardoMurillo	1	[{"added": {}}]	25	3
599	2024-09-23 19:25:34.935922+00	181	EdgardoMurillo - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
600	2024-09-23 19:34:40.698745+00	134	EdgardomurilloAmigogustavo	1	[{"added": {}}]	25	3
601	2024-09-23 19:35:06.317247+00	182	EdgardomurilloAmigogustavo - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
602	2024-09-24 00:15:48.603624+00	135	ArisGonzales	1	[{"added": {}}]	25	3
603	2024-09-24 00:16:27.507532+00	183	ArisGonzales - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
604	2024-09-24 00:17:31.049211+00	346	Transaction object (346)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
605	2024-09-24 00:18:21.009038+00	347	Transaction object (347)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Banesco - Amount Paid: 200"}}]	26	3
606	2024-09-24 00:18:54.509228+00	348	Transaction object (348)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
607	2024-09-24 00:20:00.212346+00	349	Transaction object (349)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
608	2024-09-24 00:28:15.718955+00	136	EleuterioDelrosarioTello	1	[{"added": {}}]	25	3
609	2024-09-24 00:28:47.316847+00	184	EleuterioDelrosarioTello - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
610	2024-09-24 00:29:37.819651+00	351	Transaction object (351)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 23"}}]	26	3
611	2024-09-24 00:30:07.612471+00	352	Transaction object (352)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 43"}}]	26	3
612	2024-09-24 00:30:40.611462+00	353	Transaction object (353)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
613	2024-09-24 00:31:11.629572+00	354	Transaction object (354)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
614	2024-09-24 00:31:52.89001+00	355	Transaction object (355)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
615	2024-09-24 00:32:32.827299+00	356	Transaction object (356)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
616	2024-09-24 00:33:02.140713+00	357	Transaction object (357)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
617	2024-09-25 18:23:57.064328+00	185	GenaroRodriguez - Créditos - Crédito Personal: Credit:132, pending:132	1	[{"added": {}}]	28	3
618	2024-09-25 18:28:48.347819+00	359	Transaction object (359)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 300"}}]	26	3
619	2024-09-25 18:30:49.444728+00	360	Transaction object (360)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
620	2024-09-25 18:31:51.254861+00	361	Transaction object (361)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
621	2024-09-25 18:32:45.884957+00	362	Transaction object (362)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 210"}}]	26	3
622	2024-09-25 18:33:22.553561+00	363	Transaction object (363)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
623	2024-09-25 18:34:04.1415+00	364	Transaction object (364)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
624	2024-09-25 18:58:40.728723+00	137	JoseEnriqueVillanueva	1	[{"added": {}}]	25	3
625	2024-09-25 18:59:10.354293+00	186	JoseEnriqueVillanueva - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
626	2024-09-25 18:59:38.097769+00	138	MarioMoreno	1	[{"added": {}}]	25	3
627	2024-09-25 19:00:01.797045+00	188	MarioMoreno - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
628	2024-09-25 19:00:51.488277+00	139	ElizabethJuilada	1	[{"added": {}}]	25	3
629	2024-09-25 19:01:14.012678+00	189	ElizabethJuilada - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
630	2024-09-25 19:01:23.524158+00	188	MarioMoreno - Créditos - Crédito Personal: Credit:500.00, pending:500.00	2	[{"changed": {"fields": ["Credit days"]}}]	28	3
631	2024-09-25 19:01:32.029417+00	186	JoseEnriqueVillanueva - Créditos - Crédito Personal: Credit:150.00, pending:150.00	2	[{"changed": {"fields": ["Credit days"]}}]	28	3
632	2024-09-25 19:02:41.301659+00	369	Transaction object (369)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 33"}}]	26	3
633	2024-09-25 19:03:16.726632+00	370	Transaction object (370)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
634	2024-09-25 19:03:49.665764+00	371	Transaction object (371)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
635	2024-09-25 19:04:29.341458+00	372	Transaction object (372)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
636	2024-09-25 19:07:57.162311+00	190	LeopoldoRamos - Créditos - Crédito Personal: Credit:375, pending:375	1	[{"added": {}}]	28	3
637	2024-09-27 17:35:45.338046+00	10	Créditos - Pago a crédito de Consumo	2	[{"changed": {"fields": ["Name"]}}]	24	1
638	2024-09-27 17:35:59.369523+00	10	Créditos - Pago a Crédito de Consumo	2	[{"changed": {"fields": ["Name"]}}]	24	1
639	2024-09-27 17:45:32.335491+00	8	Gastos de actividad - Viatico	2	[{"changed": {"fields": ["Name"]}}]	24	1
640	2024-09-27 17:45:48.725893+00	7	Gastos de actividad - Otros	2	[{"changed": {"fields": ["Name"]}}]	24	1
641	2024-09-27 17:46:40.127311+00	12	Gastos administrativos - Movimiento	1	[{"added": {}}]	24	1
642	2024-09-27 17:46:40.216954+00	13	Gastos administrativos - Movimiento	1	[{"added": {}}]	24	1
643	2024-09-27 17:47:14.804842+00	13	Gastos administrativos - Movimiento	3		24	1
644	2024-09-27 19:01:04.993799+00	140	ArianaMoreno	1	[{"added": {}}]	25	3
645	2024-09-27 19:01:33.766064+00	191	ArianaMoreno - Créditos - Crédito Personal: Credit:450, pending:450	1	[{"added": {}}]	28	3
646	2024-09-27 19:10:15.109523+00	375	Transaction object (375)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 225"}}]	26	3
647	2024-09-27 19:10:44.949003+00	376	Transaction object (376)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 225"}}]	26	3
648	2024-09-27 22:27:31.746269+00	377	Transaction object (377)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
649	2024-09-27 22:30:22.99129+00	192	MiguelOrdoñez - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
650	2024-09-27 22:31:57.206967+00	194	RobertoCarles - Créditos - Pago a Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
651	2024-09-27 22:35:36.447773+00	381	Transaction object (381)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
652	2024-09-27 22:39:10.067182+00	7	Gastos de actividad - Rent a car - 40	1	[{"added": {}}]	27	3
653	2024-09-27 22:40:02.720553+00	382	Transaction object (382)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
654	2024-09-27 22:40:27.942105+00	383	Transaction object (383)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
655	2024-09-27 22:41:00.43036+00	384	Transaction object (384)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
656	2024-09-27 23:25:56.164227+00	141	LazaroAgustiniani	1	[{"added": {}}]	25	3
657	2024-09-27 23:26:26.517221+00	195	LazaroAgustiniani - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
658	2024-09-27 23:27:13.511597+00	386	Transaction object (386)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
659	2024-09-27 23:27:44.768741+00	387	Transaction object (387)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
660	2024-09-27 23:29:24.380374+00	8	Gastos de actividad - Viatico - 28	1	[{"added": {}}]	27	3
661	2024-09-27 23:30:08.107306+00	9	Gastos de actividad - Transporte - 1.60	1	[{"added": {}}]	27	3
662	2024-09-27 23:38:41.903646+00	142	DianaEstherPerez	1	[{"added": {}}]	25	3
663	2024-09-27 23:39:03.620708+00	196	DianaEstherPerez - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
664	2024-09-27 23:41:25.204184+00	143	JhonatanMartinez	1	[{"added": {}}]	25	3
665	2024-09-27 23:41:48.363455+00	197	JhonatanMartinez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
666	2024-09-27 23:42:45.402209+00	144	DiegoAbdielMeneses	1	[{"added": {}}]	25	3
667	2024-09-27 23:43:04.024291+00	198	DiegoAbdielMeneses - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
668	2024-09-27 23:49:26.797733+00	10	Gastos de actividad - Viatico - 25	1	[{"added": {}}]	27	3
669	2024-09-27 23:49:46.022838+00	11	Gastos de actividad - Transporte - 1.85	1	[{"added": {}}]	27	3
670	2024-09-27 23:51:11.075954+00	391	Transaction object (391)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1117	2024-10-24 21:58:22.965928+00	197	VictorMorales	1	[{"added": {}}]	25	3
671	2024-09-27 23:51:54.776022+00	392	Transaction object (392)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
672	2024-09-27 23:55:03.411431+00	145	JulianMendoza	1	[{"added": {}}]	25	3
673	2024-09-27 23:55:33.768502+00	199	JulianMendoza - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
674	2024-09-28 00:03:18.815866+00	394	Transaction object (394)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
675	2024-09-28 00:03:51.525006+00	395	Transaction object (395)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
676	2024-09-28 00:04:20.367321+00	394	Transaction object (394)	2	[{"changed": {"fields": ["Date"]}}]	26	3
677	2024-09-28 00:04:53.300485+00	396	Transaction object (396)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
678	2024-09-28 00:08:28.124224+00	200	JhonatanAguilar - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
679	2024-09-28 00:09:01.174008+00	202	JulianMendoza - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
680	2024-09-28 00:40:46.712114+00	146	GregorioRodriguez	1	[{"added": {}}]	25	3
681	2024-09-28 00:41:17.605933+00	203	GregorioRodriguez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
682	2024-09-28 00:42:21.925897+00	204	FernandoMorales - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
683	2024-09-28 00:46:44.520525+00	402	Transaction object (402)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
684	2024-09-28 00:47:21.859762+00	403	Transaction object (403)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
685	2024-09-28 00:48:08.888757+00	404	Transaction object (404)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
686	2024-09-28 00:49:29.964539+00	405	Transaction object (405)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
687	2024-09-28 01:11:38.214159+00	205	SeleneIbarra - Créditos - Crédito Personal: Credit:1100, pending:1100	1	[{"added": {}}]	28	3
688	2024-09-28 01:12:04.210868+00	206	ErwuinMartinez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
689	2024-09-28 01:12:32.110001+00	12	Gastos de actividad - Viatico - 17.50	1	[{"added": {}}]	27	3
690	2024-09-28 01:12:45.596403+00	13	Gastos de actividad - Transporte - 1.50	1	[{"added": {}}]	27	3
691	2024-09-28 01:13:02.313934+00	14	Gastos de actividad - Otros - 20	1	[{"added": {}}]	27	3
692	2024-10-04 02:10:11.140344+00	147	RicardoPerez	1	[{"added": {}}]	25	3
693	2024-10-04 02:10:38.670631+00	207	RicardoPerez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
694	2024-10-04 02:11:23.617796+00	148	Trujillo	1	[{"added": {}}]	25	3
695	2024-10-04 02:11:47.126394+00	208	Trujillo - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
696	2024-10-04 02:12:28.241561+00	410	Transaction object (410)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
697	2024-10-04 02:14:22.841977+00	411	Transaction object (411)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
698	2024-10-04 02:15:00.551835+00	412	Transaction object (412)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
699	2024-10-04 02:15:39.948818+00	413	Transaction object (413)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 17"}}]	26	3
700	2024-10-04 02:16:24.229066+00	414	Transaction object (414)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
701	2024-10-04 02:17:42.855432+00	415	Transaction object (415)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
702	2024-10-04 02:20:08.647465+00	416	Transaction object (416)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
703	2024-10-04 02:23:42.065509+00	209	JaiberBusito - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
704	2024-10-04 02:24:25.95001+00	210	RicardoPerez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
705	2024-10-04 02:25:03.347427+00	211	LeopoldoRamos - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
706	2024-10-04 02:26:09.439144+00	149	KisilMarketAnton	1	[{"added": {}}]	25	3
707	2024-10-04 02:26:39.251316+00	212	KisilMarketAnton - Créditos - Crédito Personal: Credit:60, pending:60	1	[{"added": {}}]	28	3
708	2024-10-04 02:28:00.340139+00	421	Transaction object (421)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 125"}}]	26	3
709	2024-10-04 02:28:46.233074+00	422	Transaction object (422)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
710	2024-10-04 02:29:17.048831+00	423	Transaction object (423)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
711	2024-10-04 02:30:03.32513+00	424	Transaction object (424)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
712	2024-10-04 02:30:36.923292+00	15	Gastos de actividad - Viatico - 38	1	[{"added": {}}]	27	3
713	2024-10-04 02:30:52.037525+00	16	Gastos de actividad - Transporte - 1.50	1	[{"added": {}}]	27	3
714	2024-10-04 02:31:12.816095+00	17	Gastos de actividad - Viatico - 9	1	[{"added": {}}]	27	3
715	2024-10-04 02:31:33.522982+00	18	Gastos de actividad - Transporte - 1.60	1	[{"added": {}}]	27	3
716	2024-10-04 02:32:56.525747+00	425	Transaction object (425)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 33"}}]	26	3
717	2024-10-04 02:33:38.166401+00	426	Transaction object (426)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 18"}}]	26	3
718	2024-10-04 02:34:30.178116+00	150	CatalinaMartinez	1	[{"added": {}}]	25	3
719	2024-10-04 02:35:10.063799+00	213	CatalinaMartinez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
720	2024-10-04 02:38:15.952049+00	428	Transaction object (428)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1222	2024-10-25 00:04:24.031225+00	123	GemaGonzález	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
721	2024-10-04 02:39:09.24431+00	429	Transaction object (429)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 285"}}]	26	3
722	2024-10-04 02:40:03.551456+00	214	MariaLuisaVillanueva - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
723	2024-10-04 02:41:36.44741+00	431	Transaction object (431)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 400"}}]	26	3
724	2024-10-04 02:42:09.04347+00	432	Transaction object (432)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 38"}}]	26	3
725	2024-10-04 02:43:06.067182+00	433	Transaction object (433)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
726	2024-10-04 02:44:10.450501+00	434	Transaction object (434)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
727	2024-10-04 02:45:00.124365+00	435	Transaction object (435)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
728	2024-10-04 02:45:53.238247+00	436	Transaction object (436)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
729	2024-10-04 02:46:39.049152+00	437	Transaction object (437)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
730	2024-10-04 02:47:30.74773+00	438	Transaction object (438)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
731	2024-10-04 02:48:18.451454+00	439	Transaction object (439)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
732	2024-10-04 02:48:53.738976+00	440	Transaction object (440)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
733	2024-10-04 02:49:36.544299+00	441	Transaction object (441)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
734	2024-10-04 02:50:16.757504+00	215	ClemenciaPerez - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
735	2024-10-04 02:52:48.2398+00	151	JoseRicaute	1	[{"added": {}}]	25	3
736	2024-10-04 02:53:08.050899+00	216	JoseRicaute - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
737	2024-10-04 02:53:57.938849+00	444	Transaction object (444)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
738	2024-10-04 02:54:37.835694+00	445	Transaction object (445)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
739	2024-10-04 02:55:31.74814+00	446	Transaction object (446)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
740	2024-10-04 02:57:22.142339+00	447	Transaction object (447)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
741	2024-10-04 02:59:44.140551+00	152	AnaIsabelFernandez	1	[{"added": {}}]	25	3
742	2024-10-04 03:00:37.331491+00	217	AnaIsabelFernandez - Créditos - Pago a Crédito de Consumo: Credit:115, pending:115	1	[{"added": {}}]	28	3
743	2024-10-04 03:01:40.618225+00	218	JuanMendoza - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
744	2024-10-04 03:02:24.06003+00	219	GemaGonzález - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
745	2024-10-04 03:03:03.541007+00	153	ANYSANADELKAGONZALEZ	1	[{"added": {}}]	25	3
746	2024-10-04 03:03:29.850376+00	220	ANYSANADELKAGONZALEZ - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
747	2024-10-04 03:04:16.936024+00	154	YolandaArosemena	1	[{"added": {}}]	25	3
748	2024-10-04 03:04:42.245926+00	221	YolandaArosemena - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
749	2024-10-04 03:05:27.052983+00	453	Transaction object (453)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
750	2024-10-04 03:06:56.539676+00	155	EvelioRodriguez	1	[{"added": {}}]	25	3
751	2024-10-04 03:07:26.849335+00	222	EvelioRodriguez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
752	2024-10-04 03:08:09.353185+00	455	Transaction object (455)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
753	2024-10-04 03:08:52.939578+00	19	Gastos de actividad - Transporte - 1.65	1	[{"added": {}}]	27	3
754	2024-10-04 03:09:12.118768+00	20	Gastos de actividad - Viatico - 6.90	1	[{"added": {}}]	27	3
755	2024-10-04 03:09:37.456324+00	21	Gastos administrativos - Movimiento - 55	1	[{"added": {}}]	27	3
756	2024-10-08 23:03:07.623018+00	456	Transaction object (456)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
757	2024-10-08 23:06:04.114814+00	457	Transaction object (457)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
758	2024-10-08 23:08:37.441739+00	458	Transaction object (458)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
759	2024-10-08 23:11:02.310955+00	223	MaricelEsther - Créditos - Crédito Personal: Credit:501, pending:501	1	[{"added": {}}]	28	3
760	2024-10-08 23:12:15.422418+00	156	AngelTorres	1	[{"added": {}}]	25	3
761	2024-10-08 23:12:45.819714+00	224	AngelTorres - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
762	2024-10-08 23:13:39.313913+00	157	JavierMecanico	1	[{"added": {}}]	25	3
763	2024-10-08 23:14:18.488996+00	225	JavierMecanico - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
764	2024-10-08 23:15:40.498674+00	226	Bernabethaguilar - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
765	2024-10-08 23:19:50.215271+00	158	RafaelGonzalez	1	[{"added": {}}]	25	3
766	2024-10-08 23:20:20.690754+00	227	RafaelGonzalez - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
767	2024-10-08 23:21:26.625774+00	228	MariamTrejos - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
768	2024-10-08 23:22:11.323272+00	159	MiguelArquiñez	1	[{"added": {}}]	25	3
769	2024-10-08 23:22:44.098001+00	229	MiguelArquiñez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
770	2024-10-08 23:35:07.29134+00	466	Transaction object (466)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
771	2024-10-08 23:38:55.889193+00	467	Transaction object (467)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
772	2024-10-08 23:43:25.100457+00	468	Transaction object (468)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 175"}}]	26	3
773	2024-10-08 23:44:55.686902+00	469	Transaction object (469)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
774	2024-10-08 23:48:10.401458+00	470	Transaction object (470)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 200"}}]	26	3
775	2024-10-08 23:50:55.104938+00	471	Transaction object (471)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 180"}}]	26	3
776	2024-10-08 23:54:11.312769+00	472	Transaction object (472)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
777	2024-10-08 23:58:59.217398+00	473	Transaction object (473)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
778	2024-10-09 00:01:14.519603+00	474	Transaction object (474)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
779	2024-10-09 00:03:02.821871+00	475	Transaction object (475)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
780	2024-10-09 00:06:05.904782+00	476	Transaction object (476)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
781	2024-10-09 00:11:50.088908+00	477	Transaction object (477)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
782	2024-10-09 00:19:37.31019+00	230	RamiroGuerra - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
783	2024-10-09 00:22:29.792472+00	479	Transaction object (479)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
784	2024-10-09 00:26:46.793587+00	480	Transaction object (480)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 210"}}]	26	3
785	2024-10-09 00:31:44.888983+00	481	Transaction object (481)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
786	2024-10-09 00:37:54.399879+00	482	Transaction object (482)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
787	2024-10-09 00:39:11.011644+00	483	Transaction object (483)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
788	2024-10-09 00:40:38.511542+00	484	Transaction object (484)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
789	2024-10-09 00:46:08.188427+00	22	Gastos de actividad - Transporte - 138.7	1	[{"added": {}}]	27	3
790	2024-10-09 00:46:55.089958+00	23	Gastos de actividad - Viatico - 30	1	[{"added": {}}]	27	3
791	2024-10-09 00:47:40.695719+00	24	Gastos de actividad - Viatico - 5.0	1	[{"added": {}}]	27	3
792	2024-10-09 00:48:20.903028+00	22	Gastos de actividad - Rent a car - 138.70	2	[{"changed": {"fields": ["Subcategory"]}}]	27	3
793	2024-10-09 21:31:34.636933+00	485	Transaction object (485)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
794	2024-10-09 21:33:04.746008+00	486	Transaction object (486)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
795	2024-10-09 21:35:00.437474+00	487	Transaction object (487)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
796	2024-10-09 21:36:52.944983+00	488	Transaction object (488)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
797	2024-10-09 21:38:34.350277+00	489	Transaction object (489)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
798	2024-10-09 21:40:10.430338+00	490	Transaction object (490)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
799	2024-10-09 21:47:20.425689+00	491	Transaction object (491)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
800	2024-10-09 21:50:36.044166+00	492	Transaction object (492)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 95"}}]	26	3
801	2024-10-09 21:53:14.843645+00	493	Transaction object (493)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
802	2024-10-09 21:58:40.157904+00	494	Transaction object (494)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
803	2024-10-09 22:06:24.844516+00	231	LiceidaMartinez - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
804	2024-10-09 22:08:04.234111+00	232	DalvisMendoza - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
805	2024-10-09 22:16:51.133704+00	497	Transaction object (497)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 375"}}]	26	3
806	2024-10-09 22:21:15.340818+00	498	Transaction object (498)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
807	2024-10-09 22:24:03.344541+00	499	Transaction object (499)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
808	2024-10-09 22:25:00.818157+00	25	Gastos de actividad - Viatico - 22.5	1	[{"added": {}}]	27	3
809	2024-10-09 22:25:24.418021+00	26	Gastos de actividad - Viatico - 52	1	[{"added": {}}]	27	3
810	2024-10-09 22:34:07.833173+00	160	AleidaMendoza	1	[{"added": {}}]	25	3
811	2024-10-09 22:35:23.842053+00	233	AleidaMendoza - Créditos - Crédito Personal: Credit:400, pending:400	1	[{"added": {}}]	28	3
812	2024-10-09 22:37:01.348282+00	501	Transaction object (501)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
813	2024-10-09 22:37:59.640001+00	502	Transaction object (502)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
814	2024-10-09 22:42:29.318006+00	503	Transaction object (503)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
815	2024-10-09 23:03:45.15182+00	504	Transaction object (504)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
816	2024-10-09 23:05:35.365517+00	505	Transaction object (505)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
817	2024-10-09 23:07:09.476974+00	234	MariamDelosAngeles - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
818	2024-10-09 23:08:24.362541+00	235	ManuelSanchez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
819	2024-10-09 23:10:23.052514+00	236	EdgardoMurillo - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
820	2024-10-09 23:14:23.627467+00	509	Transaction object (509)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
821	2024-10-09 23:16:03.465777+00	510	Transaction object (510)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
822	2024-10-09 23:18:21.113883+00	511	Transaction object (511)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
823	2024-10-09 23:23:01.719481+00	161	DaniDaniel	1	[{"added": {}}]	25	3
824	2024-10-09 23:23:43.020846+00	237	DaniDaniel - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
825	2024-10-09 23:25:05.255244+00	162	CristianAlexanderGonzales	1	[{"added": {}}]	25	3
826	2024-10-09 23:25:39.059152+00	238	CristianAlexanderGonzales - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
827	2024-10-09 23:26:35.851688+00	163	YamiscellyAguilar	1	[{"added": {}}]	25	3
828	2024-10-09 23:27:04.959297+00	239	YamiscellyAguilar - Créditos - Crédito Personal: Credit:255, pending:255	1	[{"added": {}}]	28	3
829	2024-10-09 23:29:29.951518+00	27	Gastos de actividad - Viatico - 276	1	[{"added": {}}]	27	3
830	2024-10-09 23:29:56.929739+00	28	Gastos de actividad - Viatico - 42	1	[{"added": {}}]	27	3
831	2024-10-09 23:30:24.815456+00	29	Gastos de actividad - Gasolina - 20	1	[{"added": {}}]	27	3
832	2024-10-11 15:54:32.855607+00	240	ErickMagallon - Créditos - Crédito Personal: Credit:540, pending:540	1	[{"added": {}}]	28	3
833	2024-10-11 15:56:43.432024+00	516	Transaction object (516)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
834	2024-10-11 15:58:34.445337+00	517	Transaction object (517)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
835	2024-10-11 16:00:20.129022+00	518	Transaction object (518)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
836	2024-10-11 16:00:52.934324+00	517	Transaction object (517)	2	[{"changed": {"fields": ["Date"]}}]	26	3
837	2024-10-11 16:10:44.963186+00	241	MiguelOrdoñez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
838	2024-10-11 16:11:29.716483+00	164	JorgeCordoba	1	[{"added": {}}]	25	3
839	2024-10-11 16:11:56.736883+00	242	JorgeCordoba - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
840	2024-10-11 16:25:24.820572+00	165	RogelioTuñon	1	[{"added": {}}]	25	3
841	2024-10-11 16:26:24.241511+00	243	RogelioTuñon - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
842	2024-10-11 16:27:32.348328+00	522	Transaction object (522)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
843	2024-10-11 16:28:17.439646+00	523	Transaction object (523)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
844	2024-10-11 16:32:13.740841+00	524	Transaction object (524)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
845	2024-10-11 16:34:02.050419+00	525	Transaction object (525)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
846	2024-10-11 16:34:46.234896+00	30	Gastos de actividad - Viatico - 28	1	[{"added": {}}]	27	3
847	2024-10-11 16:35:08.118873+00	31	Gastos de actividad - Viatico - 17	1	[{"added": {}}]	27	3
848	2024-10-18 00:01:38.253286+00	526	Transaction object (526)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
849	2024-10-18 00:02:38.550662+00	527	Transaction object (527)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
850	2024-10-18 00:04:03.243858+00	244	Magdaxtra - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
851	2024-10-18 00:04:55.827482+00	166	LuisArmandoDominguez	1	[{"added": {}}]	25	3
852	2024-10-18 00:05:14.857632+00	245	LuisArmandoDominguez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
853	2024-10-18 00:06:25.201996+00	167	YennyGonzalesPerez	1	[{"added": {}}]	25	3
854	2024-10-18 00:06:44.655984+00	246	YennyGonzalesPerez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
855	2024-10-18 00:07:13.947882+00	247	MariamTrejos - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
856	2024-10-18 00:08:38.334549+00	168	GustavoErisnelGonzalesLorenzo	1	[{"added": {}}]	25	3
857	2024-10-18 00:08:55.634095+00	248	GustavoErisnelGonzalesLorenzo - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
858	2024-10-18 00:10:08.756607+00	169	LuisArmandoDominguezPerez	1	[{"added": {}}]	25	3
859	2024-10-18 00:10:29.154362+00	249	LuisArmandoDominguezPerez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
860	2024-10-18 00:11:05.240888+00	249	LuisArmandoDominguezPerez - Créditos - Crédito Personal: Credit:150.00, pending:150.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
861	2024-10-18 00:11:18.440968+00	248	GustavoErisnelGonzalesLorenzo - Créditos - Crédito Personal: Credit:150.00, pending:150.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
862	2024-10-18 00:11:31.05093+00	247	MariamTrejos - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
863	2024-10-18 00:11:40.547909+00	246	YennyGonzalesPerez - Créditos - Crédito Personal: Credit:140.00, pending:140.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
864	2024-10-18 00:12:51.484446+00	170	VictoriaCastroRojo	1	[{"added": {}}]	25	3
865	2024-10-18 00:13:10.451656+00	250	VictoriaCastroRojo - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
866	2024-10-18 00:13:57.727878+00	535	Transaction object (535)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1230	2024-10-25 00:09:12.720011+00	20	Colegio de la madera	1	[{"added": {}}]	18	3
867	2024-10-18 00:15:08.850433+00	138	DelfinaReyes - Créditos - Crédito Personal: Credit:150, pending:90.00	2	[{"changed": {"fields": ["Price", "Created at"]}}]	28	3
868	2024-10-18 00:16:45.819227+00	171	AlvaroGonzaleGomez	1	[{"added": {}}]	25	3
869	2024-10-18 00:17:02.946838+00	251	AlvaroGonzaleGomez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
870	2024-10-18 00:18:29.07708+00	254	OscarMegaexpress - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
871	2024-10-18 00:19:21.24297+00	540	Transaction object (540)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
872	2024-10-18 00:20:02.350208+00	541	Transaction object (541)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
873	2024-10-18 00:20:30.3316+00	542	Transaction object (542)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
874	2024-10-18 00:21:20.75525+00	543	Transaction object (543)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
875	2024-10-18 00:21:54.933597+00	544	Transaction object (544)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
876	2024-10-18 00:28:16.149476+00	545	Transaction object (545)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 68"}}]	26	3
877	2024-10-18 00:32:22.826994+00	172	LuisGomezSupercocle	1	[{"added": {}}]	25	3
878	2024-10-18 00:33:40.045054+00	255	LuisGomezSupercocle - None: Credit:220, pending:220	1	[{"added": {}}]	28	3
879	2024-10-18 00:34:50.333632+00	547	Transaction object (547)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
880	2024-10-18 00:35:28.440877+00	255	LuisGomezSupercocle - Créditos - Crédito Personal: Credit:220.00, pending:70.00	2	[{"changed": {"fields": ["Subcategory"]}}]	28	3
881	2024-10-18 00:36:15.049682+00	256	ArielHernandez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
882	2024-10-18 00:37:09.760004+00	549	Transaction object (549)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
883	2024-10-18 00:38:51.035027+00	257	MariaTuñon - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
884	2024-10-18 00:39:27.534306+00	258	OscarIvanMojica - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	3
885	2024-10-18 00:40:29.657554+00	259	EfrainMora - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
886	2024-10-18 00:43:05.225333+00	173	ArmandoRodriguezGonzales	1	[{"added": {}}]	25	3
887	2024-10-18 00:43:31.1702+00	260	ArmandoRodriguezGonzales - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
888	2024-10-18 00:44:22.929352+00	554	Transaction object (554)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
889	2024-10-18 00:44:51.146229+00	555	Transaction object (555)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
890	2024-10-18 00:46:12.922957+00	32	Gastos de actividad - Viatico - 7.50	1	[{"added": {}}]	27	3
891	2024-10-18 00:46:25.618504+00	33	Gastos de actividad - Transporte - 1.95	1	[{"added": {}}]	27	3
892	2024-10-18 00:48:44.54773+00	174	JuanPabloPanadero	1	[{"added": {}}]	25	3
893	2024-10-18 00:49:16.921688+00	261	JuanPabloPanadero - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
894	2024-10-18 00:50:17.045938+00	557	Transaction object (557)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
895	2024-10-18 00:51:35.344065+00	262	DiegoAbdielMeneses - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
896	2024-10-18 00:52:17.964735+00	263	NildaSanchez - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
897	2024-10-18 00:52:46.21999+00	175	NildaSanchezHijo	1	[{"added": {}}]	25	3
898	2024-10-18 00:53:14.444025+00	264	NildaSanchezHijo - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
899	2024-10-18 00:54:14.05354+00	561	Transaction object (561)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
900	2024-10-18 00:55:35.844333+00	562	Transaction object (562)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
901	2024-10-18 00:56:05.842499+00	563	Transaction object (563)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
902	2024-10-18 00:56:36.544734+00	34	Gastos de actividad - Viatico - 3.50	1	[{"added": {}}]	27	3
903	2024-10-18 00:56:49.832502+00	35	Gastos de actividad - Transporte - 1.50	1	[{"added": {}}]	27	3
904	2024-10-18 00:57:04.026747+00	36	Créditos - Crédito Personal - 15	1	[{"added": {}}]	27	3
905	2024-10-18 01:00:55.12222+00	176	ZuleikaGonzalesFonda	1	[{"added": {}}]	25	3
906	2024-10-18 01:01:47.644943+00	265	ZuleikaGonzalesFonda - Créditos - Crédito Personal: Credit:700, pending:700	1	[{"added": {}}]	28	3
907	2024-10-18 01:03:42.248117+00	565	Transaction object (565)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
908	2024-10-18 01:04:18.927456+00	566	Transaction object (566)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
909	2024-10-18 01:04:46.548369+00	567	Transaction object (567)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
910	2024-10-18 01:05:02.728858+00	568	Transaction object (568)	1	[{"added": {}}]	26	3
911	2024-10-18 01:05:36.32597+00	568	Transaction object (568)	2	[{"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
912	2024-10-18 01:08:45.054699+00	569	Transaction object (569)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
913	2024-10-18 01:09:20.940842+00	570	Transaction object (570)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
914	2024-10-18 01:10:08.722703+00	37	Gastos de actividad - Otros - 105	1	[{"added": {}}]	27	3
915	2024-10-18 01:10:24.235857+00	38	Gastos de actividad - Transporte - 3.75	1	[{"added": {}}]	27	3
916	2024-10-18 01:10:45.227633+00	39	Gastos de actividad - Viatico - 5.0	1	[{"added": {}}]	27	3
1116	2024-10-24 21:52:50.455182+00	314	EvangelistoyAngela - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
917	2024-10-19 22:32:39.819891+00	571	Transaction object (571)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
918	2024-10-19 22:34:12.13308+00	572	Transaction object (572)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
919	2024-10-19 22:35:08.932408+00	573	Transaction object (573)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
920	2024-10-19 22:36:11.129816+00	574	Transaction object (574)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
921	2024-10-19 22:38:13.019568+00	575	Transaction object (575)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
922	2024-10-19 22:41:11.338905+00	266	MaximilianoMoreno - Créditos - Crédito Personal: Credit:600, pending:600	1	[{"added": {}}]	28	3
923	2024-10-19 22:42:21.023055+00	269	colonvelasquez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
924	2024-10-19 22:43:02.910206+00	273	JhonatanAguilar - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
925	2024-10-19 22:43:56.147518+00	584	Transaction object (584)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
926	2024-10-19 22:44:23.209709+00	585	Transaction object (585)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
927	2024-10-19 22:44:54.84024+00	40	Gastos de actividad - Viatico - 11	1	[{"added": {}}]	27	3
928	2024-10-19 22:45:09.318677+00	41	Gastos de actividad - Transporte - 75	1	[{"added": {}}]	27	3
929	2024-10-19 22:46:43.642075+00	586	Transaction object (586)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
930	2024-10-19 22:49:10.130557+00	587	Transaction object (587)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
931	2024-10-19 22:49:47.417424+00	588	Transaction object (588)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
932	2024-10-19 22:50:36.930248+00	589	Transaction object (589)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
933	2024-10-19 22:51:27.439385+00	590	Transaction object (590)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
934	2024-10-19 22:52:09.225542+00	42	Gastos de actividad - Otros - 64.6	1	[{"added": {}}]	27	3
935	2024-10-19 22:52:22.822981+00	43	Gastos de actividad - Viatico - 5.60	1	[{"added": {}}]	27	3
936	2024-10-19 22:52:38.018672+00	44	Gastos de actividad - Transporte - 1.70	1	[{"added": {}}]	27	3
937	2024-10-19 22:53:22.128523+00	274	RobertoCarles - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
938	2024-10-19 22:54:14.450284+00	276	LuisGomezSupercocle - Créditos - Crédito Personal: Credit:260, pending:260	1	[{"added": {}}]	28	3
939	2024-10-19 22:54:57.320706+00	177	OrdoñezSr	1	[{"added": {}}]	25	3
940	2024-10-19 22:55:17.539319+00	277	OrdoñezSr - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
941	2024-10-19 22:57:56.219794+00	45	Gastos de actividad - Otros - 100	1	[{"added": {}}]	27	3
942	2024-10-19 23:00:43.943546+00	595	Transaction object (595)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
943	2024-10-19 23:05:39.110769+00	278	ReinaldoVasquez - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
944	2024-10-19 23:06:16.335054+00	279	OscarIvanMojica - Créditos - Crédito Personal: Credit:3600, pending:3600	1	[{"added": {}}]	28	3
945	2024-10-19 23:07:17.646622+00	598	Transaction object (598)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
946	2024-10-19 23:08:02.129017+00	599	Transaction object (599)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
947	2024-10-19 23:08:39.329871+00	600	Transaction object (600)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
948	2024-10-19 23:09:16.417418+00	46	Gastos de actividad - Viatico - 13	1	[{"added": {}}]	27	3
949	2024-10-19 23:09:30.913015+00	47	Gastos de actividad - Transporte - 170	1	[{"added": {}}]	27	3
950	2024-10-19 23:09:46.822065+00	48	Gastos de actividad - Viatico - 4.50	1	[{"added": {}}]	27	3
951	2024-10-19 23:10:14.336713+00	49	Gastos de actividad - Viatico - 76	1	[{"added": {}}]	27	3
952	2024-10-19 23:10:30.118221+00	50	Gastos de actividad - Viatico - 10.50	1	[{"added": {}}]	27	3
953	2024-10-19 23:10:48.968532+00	51	Gastos de actividad - Otros - 10	1	[{"added": {}}]	27	3
954	2024-10-19 23:11:42.223198+00	601	Transaction object (601)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
955	2024-10-19 23:12:43.429999+00	602	Transaction object (602)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
956	2024-10-19 23:14:55.811535+00	603	Transaction object (603)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
957	2024-10-19 23:16:01.232988+00	604	Transaction object (604)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
958	2024-10-19 23:16:41.426938+00	605	Transaction object (605)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
959	2024-10-19 23:17:18.113969+00	606	Transaction object (606)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
960	2024-10-19 23:17:48.830117+00	607	Transaction object (607)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
961	2024-10-19 23:18:51.322013+00	608	Transaction object (608)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
962	2024-10-19 23:20:43.815075+00	280	ElianysMora - Créditos - Crédito Personal: Credit:180, pending:180	1	[{"added": {}}]	28	3
963	2024-10-19 23:21:13.320497+00	178	AlcidesOrtegaFlorez	1	[{"added": {}}]	25	3
964	2024-10-19 23:21:32.928494+00	281	AlcidesOrtegaFlorez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
965	2024-10-19 23:23:25.730603+00	611	Transaction object (611)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 285"}}]	26	3
966	2024-10-19 23:24:08.032517+00	612	Transaction object (612)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 350"}}]	26	3
967	2024-10-19 23:25:04.521263+00	613	Transaction object (613)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
968	2024-10-19 23:26:20.522084+00	614	Transaction object (614)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 7"}}]	26	3
969	2024-10-19 23:28:42.922557+00	412	Transaction object (412)	2	[{"changed": {"fields": ["Date"]}}, {"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140", "fields": ["Amount", "Amount paid"]}}]	26	3
970	2024-10-19 23:30:37.232688+00	282	AlvaroAlexis - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
971	2024-10-19 23:31:10.874261+00	179	AndysBarrera	1	[{"added": {}}]	25	3
972	2024-10-19 23:31:27.809053+00	283	AndysBarrera - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
973	2024-10-19 23:31:54.650558+00	180	IdaniaBernal	1	[{"added": {}}]	25	3
974	2024-10-19 23:32:13.531719+00	284	IdaniaBernal - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
975	2024-10-19 23:33:09.83636+00	618	Transaction object (618)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
976	2024-10-19 23:33:37.023898+00	619	Transaction object (619)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
977	2024-10-19 23:34:15.237434+00	620	Transaction object (620)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
978	2024-10-19 23:35:34.548176+00	621	Transaction object (621)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 430"}}]	26	3
979	2024-10-19 23:36:09.013217+00	52	Gastos de actividad - Viatico - 5.0	1	[{"added": {}}]	27	3
980	2024-10-19 23:36:21.532812+00	53	Gastos de actividad - Transporte - 1.90	1	[{"added": {}}]	27	3
981	2024-10-19 23:36:36.620561+00	54	Gastos de actividad - Viatico - 20.25	1	[{"added": {}}]	27	3
982	2024-10-19 23:36:50.622435+00	55	Gastos de actividad - Otros - 10	1	[{"added": {}}]	27	3
983	2024-10-19 23:37:09.929979+00	56	Gastos de actividad - Otros - 40	1	[{"added": {}}]	27	3
984	2024-10-21 01:15:09.188578+00	181	CarlosRangel	1	[{"added": {}}]	25	3
985	2024-10-21 01:15:32.531813+00	285	CarlosRangel - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
986	2024-10-21 01:16:26.983901+00	182	IsisRodriguez	1	[{"added": {}}]	25	3
987	2024-10-21 01:16:51.547087+00	286	IsisRodriguez - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
988	2024-10-21 01:17:54.816264+00	183	YarisnethCardenasBijao	1	[{"added": {}}]	25	3
989	2024-10-21 01:18:18.497454+00	287	YarisnethCardenasBijao - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
990	2024-10-21 01:19:26.436237+00	625	Transaction object (625)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
991	2024-10-21 01:20:08.396267+00	626	Transaction object (626)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
992	2024-10-21 01:20:43.137001+00	627	Transaction object (627)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
993	2024-10-21 01:21:13.88484+00	628	Transaction object (628)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
994	2024-10-23 21:49:29.208862+00	288	MariaLuisaVillanueva - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
995	2024-10-23 22:02:35.600326+00	184	MiriamTrejos	1	[{"added": {}}]	25	3
996	2024-10-23 22:02:41.132819+00	247	MiriamTrejos - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[{"changed": {"fields": ["User"]}}]	28	3
997	2024-10-23 22:07:15.628062+00	185	JhoannaAguilar	1	[{"added": {}}]	25	3
998	2024-10-23 22:07:30.840988+00	273	JhoannaAguilar - Créditos - Crédito Personal: Credit:150.00, pending:150.00	2	[{"changed": {"fields": ["User"]}}]	28	3
999	2024-10-23 22:10:34.389116+00	186	OscarEmilioMojica	1	[{"added": {}}]	25	3
1000	2024-10-23 22:10:40.232512+00	279	OscarEmilioMojica - Créditos - Crédito Personal: Credit:3600.00, pending:3600.00	2	[{"changed": {"fields": ["User"]}}]	28	3
1001	2024-10-23 22:19:42.62084+00	43	ClementinaPerez	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	3
1002	2024-10-23 22:19:44.430349+00	215	ClementinaPerez - Créditos - Crédito Personal: Credit:360.00, pending:360.00	2	[]	28	3
1003	2024-10-23 23:02:24.184922+00	139	ElizabethJubilada	2	[{"changed": {"fields": ["Username"]}}]	25	3
1004	2024-10-23 23:02:26.288596+00	189	ElizabethJubilada - Créditos - Crédito Personal: Credit:255.00, pending:170.00	2	[]	28	3
1005	2024-10-23 23:09:05.128654+00	171	LuisGomez - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
1006	2024-10-23 23:09:18.58409+00	172	ZoilaOrtega - Créditos - Crédito Personal: Credit:360.00, pending:360.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
1007	2024-10-23 23:12:10.42179+00	187	ZulemaMoreno	1	[{"added": {}}]	25	3
1008	2024-10-23 23:12:34.019006+00	289	ZulemaMoreno - Créditos - Crédito Personal: Credit:200, pending:200	1	[{"added": {}}]	28	3
1009	2024-10-23 23:16:24.890546+00	290	ChristianDomínguez - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1010	2024-10-23 23:17:39.575638+00	291	DelfinaReyes - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1011	2024-10-23 23:18:10.833759+00	141	BelisarioRodriguez - Créditos - Crédito Personal: Credit:150.00, pending:80.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
1012	2024-10-23 23:21:38.624945+00	29	LuisGonzales - Créditos - Crédito de Consumo: Credit:50.00, pending:40.00	2	[{"changed": {"fields": ["Subcategory"]}}]	28	3
1013	2024-10-23 23:21:52.982213+00	29	LuisGonzales - Créditos - Crédito de Consumo: Credit:50.00, pending:40.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
1014	2024-10-23 23:25:18.917182+00	289	ZulemaMoreno - Créditos - Crédito Personal: Credit:200.00, pending:200.00	3		28	3
1015	2024-10-23 23:40:57.838408+00	188	JuanZyZ	1	[{"added": {}}]	25	3
1016	2024-10-23 23:41:24.024623+00	292	JuanZyZ - Créditos - Crédito Personal: Credit:30, pending:30	1	[{"added": {}}]	28	3
1017	2024-10-24 01:38:26.091541+00	634	Transaction object (634)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1018	2024-10-24 01:39:07.544487+00	635	Transaction object (635)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1019	2024-10-24 01:39:37.629824+00	636	Transaction object (636)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 74"}}]	26	3
1020	2024-10-24 01:40:56.344729+00	637	Transaction object (637)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1021	2024-10-24 01:46:23.639177+00	638	Transaction object (638)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1022	2024-10-24 01:47:51.833007+00	639	Transaction object (639)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1023	2024-10-24 01:48:23.934925+00	640	Transaction object (640)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1024	2024-10-24 01:49:02.751613+00	641	Transaction object (641)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1025	2024-10-24 01:50:01.437059+00	642	Transaction object (642)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1026	2024-10-24 01:51:30.733245+00	643	Transaction object (643)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1027	2024-10-24 01:52:14.836093+00	644	Transaction object (644)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 157"}}]	26	3
1028	2024-10-24 01:53:40.737819+00	645	Transaction object (645)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1029	2024-10-24 01:54:12.842219+00	646	Transaction object (646)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1030	2024-10-24 01:55:14.437554+00	647	Transaction object (647)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1031	2024-10-24 01:57:12.853533+00	648	Transaction object (648)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1032	2024-10-24 01:58:07.152059+00	649	Transaction object (649)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1033	2024-10-24 01:58:56.44028+00	650	Transaction object (650)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1034	2024-10-24 01:59:19.445676+00	651	Transaction object (651)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1035	2024-10-24 01:59:55.454919+00	652	Transaction object (652)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1036	2024-10-24 02:00:27.923499+00	653	Transaction object (653)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
1037	2024-10-24 16:08:38.190384+00	3	Hotel Buenaventura	1	[{"added": {}}]	18	1
1038	2024-10-24 16:09:25.025759+00	142	DianaEstherPerez	2	[{"changed": {"fields": ["Label"]}}]	25	1
1039	2024-10-24 16:19:29.213921+00	143	JhonatanMartinez	2	[{"changed": {"fields": ["Label"]}}]	25	1
1040	2024-10-24 16:24:56.641814+00	143	JhonatanMartinez	2	[]	25	1
1041	2024-10-24 16:29:28.724319+00	197	JhonatanMartinez - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[]	28	1
1042	2024-10-24 16:53:05.84757+00	4	Hotel Bijao	1	[{"added": {}}]	18	1
1043	2024-10-24 16:53:09.835479+00	39	MichelAntonio	2	[{"changed": {"fields": ["Label"]}}]	25	1
1044	2024-10-24 17:49:20.014672+00	5	Panaderia Sabores	1	[{"added": {}}]	18	3
1045	2024-10-24 17:51:05.41202+00	6	Super Extra	1	[{"added": {}}]	18	3
1046	2024-10-24 18:19:19.622207+00	189	OscarMegaSuegro	1	[{"added": {}}]	25	3
1047	2024-10-24 18:19:27.93136+00	254	OscarMegaSuegro - Créditos - Crédito Personal: Credit:80.00, pending:80.00	2	[{"changed": {"fields": ["User"]}}]	28	3
1048	2024-10-24 18:21:13.350767+00	654	Transaction object (654)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1049	2024-10-24 18:24:23.031343+00	655	Transaction object (655)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1050	2024-10-24 18:25:09.830337+00	293	ChristianDomínguez - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1051	2024-10-24 18:27:11.927224+00	295	EvelioRodriguez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1052	2024-10-24 18:27:52.234298+00	659	Transaction object (659)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1053	2024-10-24 18:36:26.949753+00	660	Transaction object (660)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1054	2024-10-24 18:44:17.32765+00	661	Transaction object (661)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1055	2024-10-24 18:44:52.614587+00	662	Transaction object (662)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1056	2024-10-24 18:45:16.301818+00	30	Transaction object (30)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1057	2024-10-24 18:45:49.747035+00	663	Transaction object (663)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1058	2024-10-24 18:47:32.128528+00	190	AlexioGonzalezGallo	1	[{"added": {}}]	25	3
1059	2024-10-24 18:47:51.436078+00	296	AlexioGonzalezGallo - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
1060	2024-10-24 18:49:15.838934+00	191	EdgarSotoPanaderia	1	[{"added": {}}]	25	3
1061	2024-10-24 18:49:38.739479+00	297	EdgarSotoPanaderia - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1062	2024-10-24 19:01:50.624455+00	192	IlkaBustos	1	[{"added": {}}]	25	3
1063	2024-10-24 19:02:10.722701+00	298	IlkaBustos - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1064	2024-10-24 19:02:43.442568+00	667	Transaction object (667)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
1065	2024-10-24 19:13:38.034869+00	668	Transaction object (668)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1066	2024-10-24 19:14:41.035064+00	669	Transaction object (669)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1067	2024-10-24 19:15:12.919152+00	670	Transaction object (670)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1068	2024-10-24 19:16:09.815404+00	671	Transaction object (671)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
1069	2024-10-24 19:17:01.546685+00	672	Transaction object (672)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1070	2024-10-24 19:17:37.046641+00	673	Transaction object (673)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1071	2024-10-24 19:19:15.839372+00	674	Transaction object (674)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1072	2024-10-24 19:20:43.367334+00	299	WuendyRangel - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1073	2024-10-24 19:21:27.939018+00	300	SeleneNovio - Créditos - Crédito Personal: Credit:525, pending:525	1	[{"added": {}}]	28	3
1074	2024-10-24 19:23:21.418973+00	193	TrinidadJeanPorfe	1	[{"added": {}}]	25	3
1075	2024-10-24 19:23:41.04267+00	301	TrinidadJeanPorfe - Créditos - Crédito Personal: Credit:315, pending:315	1	[{"added": {}}]	28	3
1076	2024-10-24 19:25:58.543528+00	302	JorgeReyes - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
1077	2024-10-24 19:27:24.138359+00	303	IlkaBustos - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
1078	2024-10-24 19:27:43.925447+00	129	YanCarlos	2	[{"changed": {"fields": ["Label"]}}]	25	3
1079	2024-10-24 19:28:00.856365+00	304	YanCarlos - Créditos - Crédito Personal: Credit:180, pending:180	1	[{"added": {}}]	28	3
1080	2024-10-24 19:35:54.425653+00	681	Transaction object (681)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
1081	2024-10-24 19:37:51.650271+00	682	Transaction object (682)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1082	2024-10-24 19:38:22.217082+00	683	Transaction object (683)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1083	2024-10-24 19:39:27.939976+00	305	EfrainMora - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
1084	2024-10-24 19:40:25.341621+00	685	Transaction object (685)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1085	2024-10-24 19:44:15.655512+00	686	Transaction object (686)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1086	2024-10-24 19:44:48.131371+00	687	Transaction object (687)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
1087	2024-10-24 19:45:31.529841+00	688	Transaction object (688)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1088	2024-10-24 19:46:29.450492+00	689	Transaction object (689)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1089	2024-10-24 19:47:00.730468+00	690	Transaction object (690)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1090	2024-10-24 19:47:16.139667+00	690	Transaction object (690)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80", "fields": ["Amount", "Amount paid"]}}]	26	3
1091	2024-10-24 19:49:13.720371+00	306	OscarMegaexpress - Créditos - Pago a Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1092	2024-10-24 19:49:53.736614+00	194	CristianAlexanderMega	1	[{"added": {}}]	25	3
1093	2024-10-24 19:50:18.729799+00	307	CristianAlexanderMega - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
1094	2024-10-24 19:51:20.825661+00	693	Transaction object (693)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 200"}}]	26	3
1095	2024-10-24 19:52:00.431334+00	57	SantanaPanaderia	2	[]	25	3
1096	2024-10-24 19:52:29.442224+00	308	SantanaPanaderia - Créditos - Crédito Personal: Credit:510, pending:510	1	[{"added": {}}]	28	3
1097	2024-10-24 19:53:03.842799+00	195	EDILBERTOJOELFIGUEROA	1	[{"added": {}}]	25	3
1098	2024-10-24 19:53:25.540288+00	309	EDILBERTOJOELFIGUEROA - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1099	2024-10-24 19:54:15.248637+00	696	Transaction object (696)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1100	2024-10-24 19:54:45.829182+00	697	Transaction object (697)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1101	2024-10-24 19:55:28.773418+00	57	Gastos de actividad - Transporte - 1.50	1	[{"added": {}}]	27	3
1102	2024-10-24 19:55:47.534116+00	58	Gastos de actividad - Rent a car - 54	1	[{"added": {}}]	27	3
1103	2024-10-24 19:56:02.229032+00	59	Gastos de actividad - Viatico - 6	1	[{"added": {}}]	27	3
1104	2024-10-24 19:56:23.226058+00	60	Gastos de actividad - Viatico - 14.5	1	[{"added": {}}]	27	3
1105	2024-10-24 19:56:38.530231+00	61	Gastos de actividad - Viatico - 11.50	1	[{"added": {}}]	27	3
1106	2024-10-24 19:56:54.729815+00	62	Gastos de actividad - Viatico - 6.50	1	[{"added": {}}]	27	3
1107	2024-10-24 21:11:26.547053+00	310	DanitzaAguilar - Créditos - Crédito Personal: Credit:540, pending:540	1	[{"added": {}}]	28	3
1108	2024-10-24 21:16:33.23408+00	699	Transaction object (699)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1109	2024-10-24 21:17:05.617989+00	700	Transaction object (700)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1110	2024-10-24 21:17:34.226272+00	701	Transaction object (701)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1111	2024-10-24 21:18:02.933063+00	702	Transaction object (702)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1112	2024-10-24 21:25:15.232432+00	311	SimonaDominguez - Créditos - Crédito Personal: Credit:400, pending:400	1	[{"added": {}}]	28	3
1113	2024-10-24 21:26:06.116933+00	313	RogelioCorro - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1114	2024-10-24 21:33:34.438835+00	706	Transaction object (706)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
1115	2024-10-24 21:51:20.417495+00	196	EvangelistoyAngela	1	[{"added": {}}]	25	3
1118	2024-10-24 21:58:45.54125+00	315	VictorMorales - Créditos - Crédito Personal: Credit:550, pending:550	1	[{"added": {}}]	28	3
1119	2024-10-24 21:59:12.850312+00	316	PublioProfe - Créditos - Crédito Personal: Credit:880, pending:880	1	[{"added": {}}]	28	3
1120	2024-10-24 22:00:04.170254+00	317	Advasadiermatatan - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1121	2024-10-24 22:01:39.817612+00	320	ManuelSanchez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1122	2024-10-24 22:02:37.856655+00	714	Transaction object (714)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1123	2024-10-24 22:02:56.531135+00	715	Transaction object (715)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1124	2024-10-24 22:04:39.442388+00	716	Transaction object (716)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1125	2024-10-24 22:05:25.230623+00	63	Gastos de actividad - Viatico - 22	1	[{"added": {}}]	27	3
1126	2024-10-24 22:12:14.019856+00	717	Transaction object (717)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1127	2024-10-24 22:13:16.747106+00	718	Transaction object (718)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1128	2024-10-24 22:14:28.838317+00	719	Transaction object (719)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1129	2024-10-24 22:32:22.916463+00	321	AlvaroAlexis - Créditos - Crédito Personal: Credit:900, pending:900	1	[{"added": {}}]	28	3
1130	2024-10-24 22:34:46.240592+00	62	CarlosArturoArauz	2	[{"changed": {"fields": ["Username"]}}]	25	3
1131	2024-10-24 22:36:00.652787+00	721	Transaction object (721)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1132	2024-10-24 22:36:36.667256+00	722	Transaction object (722)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1133	2024-10-24 22:37:20.84656+00	723	Transaction object (723)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1134	2024-10-24 22:39:06.241905+00	724	Transaction object (724)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1135	2024-10-24 22:45:58.726827+00	725	Transaction object (725)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1136	2024-10-24 22:46:57.239084+00	726	Transaction object (726)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
1137	2024-10-24 22:47:24.847647+00	727	Transaction object (727)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1138	2024-10-24 22:52:51.118468+00	198	RicauterSegundo	1	[{"added": {}}]	25	3
1139	2024-10-24 22:53:24.649981+00	322	RicauterSegundo - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
1140	2024-10-24 22:54:05.934858+00	729	Transaction object (729)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1141	2024-10-24 22:54:37.143264+00	730	Transaction object (730)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1142	2024-10-24 22:55:21.448519+00	731	Transaction object (731)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
1143	2024-10-24 22:55:55.824884+00	732	Transaction object (732)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1144	2024-10-24 22:56:37.746733+00	733	Transaction object (733)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1145	2024-10-24 22:57:28.049859+00	734	Transaction object (734)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1146	2024-10-24 22:57:56.126433+00	64	Gastos de actividad - Otros - 400	1	[{"added": {}}]	27	3
1147	2024-10-24 22:59:33.239797+00	735	Transaction object (735)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1148	2024-10-24 23:00:03.406036+00	736	Transaction object (736)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1149	2024-10-24 23:01:04.46972+00	737	Transaction object (737)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1150	2024-10-24 23:04:35.033189+00	738	Transaction object (738)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1151	2024-10-24 23:07:20.116631+00	323	OmeidaJubilada - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1152	2024-10-24 23:08:21.714162+00	199	David	1	[{"added": {}}]	25	3
1153	2024-10-24 23:08:40.326372+00	324	David - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1154	2024-10-24 23:09:36.244185+00	741	Transaction object (741)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1155	2024-10-24 23:10:24.521383+00	65	Gastos de actividad - Viatico - 55	1	[{"added": {}}]	27	3
1156	2024-10-24 23:10:39.119444+00	66	Gastos de actividad - Viatico - 7	1	[{"added": {}}]	27	3
1157	2024-10-24 23:12:23.251698+00	325	YarisnethCardenasBijao - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1158	2024-10-24 23:13:06.637673+00	328	AlbertoArocemena - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1159	2024-10-24 23:14:15.537241+00	746	Transaction object (746)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1160	2024-10-24 23:14:51.417425+00	747	Transaction object (747)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1161	2024-10-24 23:15:23.313826+00	67	Gastos de actividad - Transporte - 1.20	1	[{"added": {}}]	27	3
1162	2024-10-24 23:15:40.345427+00	68	Gastos de actividad - Viatico - 10.50	1	[{"added": {}}]	27	3
1163	2024-10-24 23:16:48.217668+00	200	MariaLuisaTercero	1	[{"added": {}}]	25	3
1164	2024-10-24 23:17:14.075163+00	329	MariaLuisaTercero - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1223	2024-10-25 00:04:55.627524+00	73	ArianaItzel	2	[{"changed": {"fields": ["Username", "First name", "Label", "Reference 1"]}}]	25	3
1165	2024-10-24 23:22:18.13937+00	749	Transaction object (749)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 375"}}]	26	3
1166	2024-10-24 23:22:59.13216+00	750	Transaction object (750)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 180"}}]	26	3
1167	2024-10-24 23:23:35.027522+00	751	Transaction object (751)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 170"}}]	26	3
1168	2024-10-24 23:24:11.527538+00	752	Transaction object (752)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 300"}}]	26	3
1169	2024-10-24 23:25:45.982903+00	201	AidaProfesora	1	[{"added": {}}]	25	3
1170	2024-10-24 23:26:07.545222+00	330	AidaProfesora - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1171	2024-10-24 23:27:08.807875+00	202	JoaquinAgrazal	1	[{"added": {}}]	25	3
1172	2024-10-24 23:27:26.339497+00	331	JoaquinAgrazal - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
1173	2024-10-24 23:28:02.932123+00	203	CarlosMora	1	[{"added": {}}]	25	3
1174	2024-10-24 23:28:24.633176+00	332	CarlosMora - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1175	2024-10-24 23:29:18.133443+00	756	Transaction object (756)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1176	2024-10-24 23:29:43.235832+00	757	Transaction object (757)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1177	2024-10-24 23:30:23.324003+00	69	Gastos de actividad - Viatico - 9.50	1	[{"added": {}}]	27	3
1178	2024-10-24 23:30:50.428795+00	70	Gastos de actividad - Transporte - 3.70	1	[{"added": {}}]	27	3
1179	2024-10-24 23:42:36.134635+00	138	DelfinaReyes - Créditos - Crédito Personal: Credit:90, pending:90.00	2	[{"changed": {"fields": ["Price", "Created at"]}}]	28	3
1180	2024-10-24 23:43:27.147978+00	138	DelfinaReyes - Créditos - Crédito Personal: Credit:150, pending:90.00	2	[{"changed": {"fields": ["Cost", "Price", "Description", "Created at"]}}]	28	3
1181	2024-10-24 23:46:58.127888+00	7	Colegio San Francisco Penonome	1	[{"added": {}}]	18	3
1182	2024-10-24 23:47:02.114353+00	8	Escuela Chorrera	1	[{"added": {}}]	18	3
1183	2024-10-24 23:47:05.515504+00	9	Escuela de las guabas	1	[{"added": {}}]	18	3
1184	2024-10-24 23:47:09.617213+00	10	Escuela Dominicana	1	[{"added": {}}]	18	3
1185	2024-10-24 23:47:14.095494+00	11	Escuela Manuel Patiño	1	[{"added": {}}]	18	3
1186	2024-10-24 23:47:23.217311+00	1	InadehT	2	[{"changed": {"fields": ["Name"]}}]	18	3
1187	2024-10-24 23:47:29.991607+00	1	Inadeht	2	[{"changed": {"fields": ["Name"]}}]	18	3
1188	2024-10-24 23:47:34.336726+00	12	IPEHE Antón	1	[{"added": {}}]	18	3
1189	2024-10-24 23:47:38.572604+00	13	IPEHE Penonome	1	[{"added": {}}]	18	3
1190	2024-10-24 23:47:41.866224+00	14	Salomon Ponce	1	[{"added": {}}]	18	3
1191	2024-10-24 23:47:45.622056+00	15	Salomon Ponce Aguilera	1	[{"added": {}}]	18	3
1192	2024-10-24 23:47:49.702781+00	16	SPA	1	[{"added": {}}]	18	3
1193	2024-10-24 23:47:54.437124+00	17	Universidad Nacional de Panamá	1	[{"added": {}}]	18	3
1194	2024-10-24 23:47:59.319991+00	18	Universidad Tecnologica de Panamá	1	[{"added": {}}]	18	3
1195	2024-10-24 23:48:04.369788+00	19	Universidad UDELAS	1	[{"added": {}}]	18	3
1196	2024-10-24 23:51:34.028825+00	193	TrinidadJeanPorfe	2	[{"changed": {"fields": ["Label"]}}]	25	3
1197	2024-10-24 23:51:48.722076+00	11	JessicaSanchez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1198	2024-10-24 23:52:16.301959+00	43	ClementinaPerez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1199	2024-10-24 23:53:13.626641+00	43	ClementinaPerez	2	[{"changed": {"fields": ["Reference 1"]}}]	25	3
1200	2024-10-24 23:53:30.026713+00	193	TrinidadJeanPorfe	2	[{"changed": {"fields": ["Reference 1"]}}]	25	3
1201	2024-10-24 23:53:44.425559+00	11	JessicaSanchez	2	[{"changed": {"fields": ["Reference 1"]}}]	25	3
1202	2024-10-24 23:54:45.940427+00	66	IgnacioVega	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1203	2024-10-24 23:55:10.739756+00	124	DorisAguilar	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1204	2024-10-24 23:55:36.22617+00	27	RobertoCharles	2	[{"changed": {"fields": ["Username", "Last name", "Label", "Reference 1"]}}]	25	3
1205	2024-10-24 23:55:50.03816+00	121	MorrisProfesor	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1206	2024-10-24 23:56:07.130596+00	119	MaximilianoMoreno	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1207	2024-10-24 23:56:28.827799+00	84	MiguelOrdoñez	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1208	2024-10-24 23:56:43.129347+00	28	EliecerInadeh	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1209	2024-10-24 23:56:53.725997+00	28	EliecerInadeh	2	[{"changed": {"fields": ["Reference 1"]}}]	25	3
1210	2024-10-24 23:57:05.43132+00	84	MiguelOrdoñez	2	[{"changed": {"fields": ["Reference 1"]}}]	25	3
1211	2024-10-24 23:57:20.326455+00	61	AlvaroAlexis	2	[{"changed": {"fields": ["Label"]}}]	25	3
1212	2024-10-24 23:57:37.914825+00	79	AndysMartinez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1213	2024-10-24 23:57:59.931479+00	32	GladysMontero	2	[{"changed": {"fields": ["Label"]}}]	25	3
1214	2024-10-24 23:59:25.639323+00	25	JavierInadeh	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1215	2024-10-24 23:59:41.73349+00	3	enriquefritos	2	[{"changed": {"fields": ["Label"]}}]	25	3
1216	2024-10-25 00:00:08.426137+00	58	MarinaMoreno	2	[{"changed": {"fields": ["Label"]}}]	25	3
1217	2024-10-25 00:00:24.632195+00	140	ArianaMoreno	2	[{"changed": {"fields": ["Label"]}}]	25	3
1218	2024-10-25 00:02:33.025338+00	76	YesibethIbarra	2	[{"changed": {"fields": ["Username", "First name", "Label"]}}]	25	3
1219	2024-10-25 00:02:53.430299+00	40	Lazaro	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1220	2024-10-25 00:03:15.720651+00	80	MarioBetancur	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1221	2024-10-25 00:03:34.428535+00	71	ErickMagallon	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1224	2024-10-25 00:05:13.027789+00	152	AnaIsabelFernandez	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1225	2024-10-25 00:05:48.223385+00	24	LuisGonzales	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1226	2024-10-25 00:06:03.239937+00	29	TomasAlbertoMartinez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1227	2024-10-25 00:06:23.753259+00	51	JoseLuisFernandez	2	[{"changed": {"fields": ["Username", "Label"]}}]	25	3
1228	2024-10-25 00:06:50.438862+00	59	Ubaldo	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1229	2024-10-25 00:07:15.154018+00	31	EnockGuerra	2	[{"changed": {"fields": ["Label"]}}]	25	3
1231	2024-10-25 00:09:15.041564+00	34	SimonaDominguez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1232	2024-10-25 00:11:33.538748+00	204	AdolfoCorrea	1	[{"added": {}}]	25	3
1233	2024-10-25 00:12:19.949015+00	333	AdolfoCorrea - Créditos - Crédito Personal: Credit:200, pending:200	1	[{"added": {}}]	28	3
1234	2024-10-25 00:13:12.85067+00	759	Transaction object (759)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1235	2024-10-25 00:13:38.44898+00	760	Transaction object (760)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1236	2024-10-25 00:14:17.826942+00	761	Transaction object (761)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1237	2024-10-25 00:14:57.327713+00	75	ArianaMares	2	[{"changed": {"fields": ["Username", "First name", "Label"]}}]	25	3
1238	2024-10-25 00:17:30.915166+00	205	MaicolIbarra	1	[{"added": {}}]	25	3
1239	2024-10-25 00:18:16.719534+00	334	MaicolIbarra - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1240	2024-10-25 00:19:05.239445+00	763	Transaction object (763)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1241	2024-10-25 00:20:27.137476+00	335	MaicolIbarra - Créditos - Pago a Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1242	2024-10-25 00:21:12.229909+00	765	Transaction object (765)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1243	2024-10-25 18:17:40.017048+00	21	Familia Gonzales	1	[{"added": {}}]	18	3
1244	2024-10-25 18:19:58.333916+00	176	ZuleikaGonzalesFonda	2	[{"changed": {"fields": ["Label"]}}]	25	3
1245	2024-10-25 18:20:11.943259+00	135	ArisGonzales	2	[{"changed": {"fields": ["Label"]}}]	25	3
1246	2024-10-25 18:21:10.073023+00	22	Odontologo	1	[{"added": {}}]	18	3
1247	2024-10-25 18:21:19.726251+00	33	CesarHernandez	2	[{"changed": {"fields": ["Label", "Reference 1"]}}]	25	3
1248	2024-10-25 18:21:47.420287+00	23	Familia Mendoza	1	[{"added": {}}]	18	3
1249	2024-10-25 18:25:27.930066+00	52	LucianoMendoza	2	[{"changed": {"fields": ["Label"]}}]	25	3
1250	2024-10-25 18:25:56.236535+00	160	AleidaMendoza	2	[{"changed": {"fields": ["Label"]}}]	25	3
1251	2024-10-25 18:26:06.731611+00	145	JulianMendoza	2	[{"changed": {"fields": ["Label"]}}]	25	3
1252	2024-10-25 18:26:16.231225+00	86	DalvisMendoza	2	[{"changed": {"fields": ["Label"]}}]	25	3
1253	2024-10-25 18:26:22.847867+00	52	LucianoMendoza	2	[]	25	3
1254	2024-10-25 18:26:31.435052+00	23	JuanMendoza	2	[{"changed": {"fields": ["Label"]}}]	25	3
1255	2024-10-25 18:27:12.319022+00	22	JoseLuciano	2	[{"changed": {"fields": ["Label"]}}]	25	3
1256	2024-10-25 18:30:22.442228+00	125	MariaKarlaRivera	2	[{"changed": {"fields": ["Username", "Last name", "Label"]}}]	25	3
1257	2024-10-25 18:31:01.128227+00	23	JuanMendoza	2	[]	25	3
1258	2024-10-25 18:38:58.42234+00	206	FranciscoMendoza	1	[{"added": {}}]	25	3
1259	2024-10-25 18:39:26.820716+00	336	FranciscoMendoza - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
1260	2024-10-25 18:40:01.628538+00	767	Transaction object (767)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1261	2024-10-25 18:40:30.150374+00	768	Transaction object (768)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1262	2024-10-25 18:40:56.224401+00	769	Transaction object (769)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1263	2024-10-25 18:44:09.946668+00	113	AdbasadierAbisalMatatan	2	[{"changed": {"fields": ["Username", "First name", "Last name", "Label"]}}]	25	3
1264	2024-10-25 18:44:40.726717+00	171	AlvaroGonzalezGomez	2	[{"changed": {"fields": ["Username", "Label"]}}]	25	3
1265	2024-10-25 18:45:24.422326+00	110	BelisarioRodriguez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1266	2024-10-25 18:49:17.94085+00	144	DiegoAbdielMeneses	2	[{"changed": {"fields": ["Label"]}}]	25	3
1267	2024-10-25 18:49:32.621004+00	191	EdgarSoto	2	[{"changed": {"fields": ["Username"]}}]	25	3
1268	2024-10-25 18:50:20.426046+00	196	EvangelistoRojas	2	[{"changed": {"fields": ["Username", "Last name"]}}]	25	3
1269	2024-10-25 18:50:59.442422+00	60	JeisonOviedo	2	[{"changed": {"fields": ["Label"]}}]	25	3
1270	2024-10-25 18:51:43.348904+00	114	LeydiamSilveraPanaderia	2	[{"changed": {"fields": ["Username", "Last name", "Label"]}}]	25	3
1271	2024-10-25 18:52:37.932582+00	7	RamiroGuerra	2	[{"changed": {"fields": ["Label"]}}]	25	3
1272	2024-10-25 18:52:47.737893+00	129	YanCarlos	2	[]	25	3
1273	2024-10-25 18:53:47.138845+00	60	YeisonOvidio	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	3
1274	2024-10-25 18:55:42.84009+00	60	JeisonOvidioGonzalez	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	3
1275	2024-10-25 19:02:11.937419+00	21	Magdaxtra	2	[{"changed": {"fields": ["Label"]}}]	25	3
1276	2024-10-25 19:02:42.924374+00	87	JhonatanAguilar	2	[{"changed": {"fields": ["Label"]}}]	25	3
1277	2024-10-25 19:03:03.93189+00	120	VictorExtar	2	[{"changed": {"fields": ["Label"]}}]	25	3
1278	2024-10-25 19:03:34.22409+00	6	SeleneIbarra	2	[{"changed": {"fields": ["Label"]}}]	25	3
1279	2024-10-25 19:03:41.123729+00	5	SeleneNovio	2	[{"changed": {"fields": ["Label"]}}]	25	3
1280	2024-10-25 19:04:21.741609+00	78	JoséSamuelQuiroz	2	[{"changed": {"fields": ["Label"]}}]	25	3
1281	2024-10-25 19:04:40.135908+00	74	ElianysMora	2	[{"changed": {"fields": ["Label"]}}]	25	3
1282	2024-10-25 19:05:52.826868+00	185	JhoannaAguilar	2	[{"changed": {"fields": ["Label"]}}]	25	3
1283	2024-10-25 19:06:10.832458+00	195	EDILBERTOJOELFIGUEROA	2	[{"changed": {"fields": ["Label"]}}]	25	3
1284	2024-10-25 19:07:11.110049+00	24	Super Market Anton	1	[{"added": {}}]	18	3
1285	2024-10-25 19:07:12.836424+00	149	KisilMarketAnton	2	[{"changed": {"fields": ["Label"]}}]	25	3
1286	2024-10-25 19:07:39.326961+00	25	SuperCocle	1	[{"added": {}}]	18	3
1287	2024-10-25 19:08:03.526418+00	172	LuisGomezSupercocle	2	[{"changed": {"fields": ["Label"]}}]	25	3
1288	2024-10-25 19:10:40.595998+00	26	Super Anton	1	[{"added": {}}]	18	3
1289	2024-10-25 19:10:42.825289+00	104	ArielHernandez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1290	2024-10-26 14:20:22.268657+00	1	Inadeh	2	[{"changed": {"fields": ["Name"]}}]	18	1
1291	2024-10-26 14:20:34.722434+00	3	Hotel Buenaventura	2	[{"changed": {"fields": ["Position"]}}]	18	1
1292	2024-10-26 18:51:27.016618+00	27	DoitCenter	1	[{"added": {}}]	18	3
1293	2024-10-26 18:51:46.855633+00	203	CarlosMora	2	[{"changed": {"fields": ["Label"]}}]	25	3
1294	2024-10-26 18:53:49.720893+00	207	LuisCamargo	1	[{"added": {}}]	25	3
1295	2024-10-26 18:54:12.837792+00	337	LuisCamargo - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1296	2024-10-26 18:54:39.132321+00	202	JoaquinAgrazal	2	[{"changed": {"fields": ["Label"]}}]	25	3
1297	2024-10-26 18:55:29.642887+00	153	ANYSANADELKAGONZALEZ	2	[{"changed": {"fields": ["Label"]}}]	25	3
1298	2024-10-27 23:18:52.238315+00	208	JavierArielOsorio	1	[{"added": {}}]	25	3
1299	2024-10-27 23:20:25.344442+00	338	JavierArielOsorio - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
1300	2024-10-27 23:23:12.837952+00	209	AdanAbdielHigaldo	1	[{"added": {}}]	25	3
1301	2024-10-27 23:23:34.637358+00	339	AdanAbdielHigaldo - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1302	2024-10-27 23:30:49.237049+00	210	SebastianCervantes	1	[{"added": {}}]	25	3
1303	2024-10-27 23:31:13.740777+00	340	SebastianCervantes - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1304	2024-10-27 23:34:20.520364+00	211	StefanyFernandez	1	[{"added": {}}]	25	3
1305	2024-10-27 23:34:41.039336+00	341	StefanyFernandez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1306	2024-10-27 23:35:28.504144+00	212	OsvaldoOscarMoreno	1	[{"added": {}}]	25	3
1307	2024-10-27 23:35:50.546542+00	342	OsvaldoOscarMoreno - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1308	2024-10-27 23:37:45.715055+00	71	Gastos de actividad - Otros - 225.50	1	[{"added": {}}]	27	3
1309	2024-10-27 23:38:08.820357+00	72	Gastos de actividad - Otros - 150	1	[{"added": {}}]	27	3
1310	2024-10-27 23:39:03.036787+00	776	Transaction object (776)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 300"}}]	26	3
1311	2024-10-27 23:39:29.840175+00	777	Transaction object (777)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1312	2024-10-27 23:40:21.181725+00	778	Transaction object (778)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1313	2024-10-27 23:41:29.532299+00	73	Gastos de actividad - Viatico - 425	1	[{"added": {}}]	27	3
1314	2024-10-27 23:41:40.41494+00	74	Gastos de actividad - Transporte - 375	1	[{"added": {}}]	27	3
1315	2024-10-27 23:46:52.388824+00	213	SusanaLopez	1	[{"added": {}}]	25	3
1316	2024-10-27 23:47:20.748598+00	343	SusanaLopez - Créditos - Crédito Personal: Credit:230, pending:230	1	[{"added": {}}]	28	3
1317	2024-10-27 23:48:06.726278+00	345	MariaLuisaVillanueva - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
1318	2024-10-27 23:48:58.137658+00	214	RogerMoreno	1	[{"added": {}}]	25	3
1319	2024-10-27 23:49:23.251134+00	346	RogerMoreno - Créditos - Crédito Personal: Credit:100, pending:100	1	[{"added": {}}]	28	3
1320	2024-10-27 23:51:20.331304+00	75	Gastos de actividad - Otros - 87	1	[{"added": {}}]	27	3
1321	2024-10-27 23:51:41.119061+00	76	Gastos de actividad - Otros - 5.50	1	[{"added": {}}]	27	3
1322	2024-10-27 23:51:53.765327+00	77	Gastos de actividad - Transporte - 3.50	1	[{"added": {}}]	27	3
1323	2024-10-27 23:53:38.733307+00	783	Transaction object (783)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1324	2024-10-27 23:54:06.546234+00	784	Transaction object (784)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1325	2024-10-27 23:54:38.936047+00	785	Transaction object (785)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1326	2024-10-27 23:55:12.917335+00	786	Transaction object (786)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1327	2024-10-27 23:55:54.447025+00	787	Transaction object (787)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1328	2024-10-27 23:58:44.948981+00	788	Transaction object (788)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1329	2024-10-28 00:00:43.225364+00	215	DIXGSANIATORRES	1	[{"added": {}}]	25	3
1330	2024-10-28 00:02:29.471944+00	347	DIXGSANIATORRES - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1331	2024-10-28 00:05:11.326151+00	126	JhoannaRodriguez	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	3
1332	2024-10-28 00:05:13.947642+00	169	JhoannaRodriguez - Créditos - Crédito Personal: Credit:140.00, pending:70.00	2	[]	28	3
1333	2024-10-28 00:06:02.949556+00	790	Transaction object (790)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1334	2024-10-28 00:13:11.438368+00	791	Transaction object (791)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1335	2024-10-28 00:14:38.736827+00	348	JhoannaRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1336	2024-10-28 00:15:42.853701+00	349	ErwuinMartinez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1337	2024-10-28 00:17:24.734443+00	794	Transaction object (794)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1338	2024-10-28 00:19:35.427093+00	795	Transaction object (795)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1339	2024-10-28 00:22:54.255493+00	78	Gastos de actividad - Viatico - 6.5	1	[{"added": {}}]	27	3
1340	2024-10-28 00:23:08.631723+00	79	Créditos - Pago a Crédito Personal - 9.5	1	[{"added": {}}]	27	3
1341	2024-10-28 00:23:20.013828+00	80	Gastos de actividad - Transporte - 3.90	1	[{"added": {}}]	27	3
1342	2024-10-28 00:30:39.532252+00	350	ElianysMora - Créditos - Crédito Personal: Credit:216, pending:216	1	[{"added": {}}]	28	3
1343	2024-10-28 00:32:21.520503+00	216	TeodoroTranquilla	1	[{"added": {}}]	25	3
1344	2024-10-28 00:32:40.029406+00	351	TeodoroTranquilla - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
1345	2024-10-28 00:34:17.952343+00	217	MarietaElionorMorales	1	[{"added": {}}]	25	3
1346	2024-10-28 00:34:35.446464+00	352	MarietaElionorMorales - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1347	2024-10-28 00:35:31.445205+00	799	Transaction object (799)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1348	2024-10-28 00:36:08.495976+00	800	Transaction object (800)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1349	2024-10-28 00:36:39.026066+00	801	Transaction object (801)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1350	2024-10-28 00:40:13.827004+00	81	Gastos de actividad - Otros - 20	1	[{"added": {}}]	27	3
1351	2024-10-28 00:40:43.138905+00	82	Gastos de actividad - Otros - 5.50	1	[{"added": {}}]	27	3
1352	2024-10-28 00:41:03.714291+00	83	Gastos de actividad - Transporte - 4	1	[{"added": {}}]	27	3
1641	2024-11-12 22:47:55.216925+00	2	Unal	3		18	3
1353	2024-10-28 01:02:53.632756+00	28	Escuela Primaria el Valle de Anton	1	[{"added": {}}]	18	3
1354	2024-10-28 01:03:08.022873+00	211	StefanyFernandez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1355	2024-10-29 01:02:40.940201+00	218	MagalyMaxwell	1	[{"added": {}}]	25	3
1356	2024-10-29 01:03:09.239227+00	353	MagalyMaxwell - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
1357	2024-10-29 01:07:57.424611+00	219	AidaRamos	1	[{"added": {}}]	25	3
1358	2024-10-29 01:08:27.154148+00	354	AidaRamos - Créditos - Crédito Personal: Credit:100, pending:100	1	[{"added": {}}]	28	3
1359	2024-10-29 01:09:03.831752+00	356	Magdaxtra - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1360	2024-10-29 01:09:44.634258+00	220	EmilethGonzales	1	[{"added": {}}]	25	3
1361	2024-10-29 01:10:08.4608+00	357	EmilethGonzales - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1362	2024-10-29 01:11:12.243659+00	358	CesarHernandez - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
1363	2024-10-29 01:12:13.036963+00	808	Transaction object (808)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1364	2024-10-29 01:12:37.73508+00	809	Transaction object (809)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1365	2024-10-29 01:13:21.172476+00	810	Transaction object (810)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1366	2024-10-29 01:14:04.844208+00	811	Transaction object (811)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1367	2024-10-29 01:14:50.951683+00	812	Transaction object (812)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1368	2024-10-29 01:15:10.56423+00	812	Transaction object (812)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50", "fields": ["Amount", "Amount paid"]}}]	26	3
1369	2024-10-29 01:15:46.359586+00	813	Transaction object (813)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
1370	2024-11-01 21:31:49.843364+00	814	Transaction object (814)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1371	2024-11-01 21:32:26.765731+00	815	Transaction object (815)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1372	2024-11-01 21:32:51.939726+00	816	Transaction object (816)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 115"}}]	26	3
1373	2024-11-01 21:34:29.852798+00	817	Transaction object (817)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1374	2024-11-01 21:36:58.249346+00	818	Transaction object (818)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1375	2024-11-01 21:37:25.820935+00	814	Transaction object (814)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1376	2024-11-01 21:37:44.947234+00	815	Transaction object (815)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1377	2024-11-01 21:38:04.425291+00	816	Transaction object (816)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1378	2024-11-01 21:38:20.435386+00	817	Transaction object (817)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1379	2024-11-01 21:38:36.540867+00	818	Transaction object (818)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1380	2024-11-01 21:44:57.328285+00	157	JavierEscobarMecanico	2	[{"changed": {"fields": ["Username", "Last name", "Label", "Reference 1"]}}]	25	3
1381	2024-11-01 21:45:34.159088+00	359	JavierEscobarMecanico - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1382	2024-11-01 21:47:12.932333+00	820	Transaction object (820)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1383	2024-11-01 21:48:11.560263+00	360	MiguelOrdoñez - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
1384	2024-11-01 21:49:24.526451+00	822	Transaction object (822)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1385	2024-11-01 21:50:13.722088+00	823	Transaction object (823)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1386	2024-11-01 21:51:11.157767+00	824	Transaction object (824)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1387	2024-11-01 21:51:39.237291+00	825	Transaction object (825)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1388	2024-11-01 21:52:07.034427+00	826	Transaction object (826)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1389	2024-11-01 21:53:30.636918+00	827	Transaction object (827)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1390	2024-11-01 21:53:59.63171+00	84	Gastos de actividad - Viatico - 5	1	[{"added": {}}]	27	3
1391	2024-11-01 21:54:18.725679+00	85	Gastos de actividad - Otros - 11.50	1	[{"added": {}}]	27	3
1392	2024-11-01 22:00:03.435373+00	86	Créditos - Crédito Personal - 4.85	1	[{"added": {}}]	27	3
1393	2024-11-01 22:00:18.133231+00	87	Gastos de actividad - Transporte - 3.40	1	[{"added": {}}]	27	3
1394	2024-11-01 22:00:33.550053+00	86	Créditos - Crédito Personal - 4.85	2	[{"changed": {"fields": ["Created at"]}}]	27	3
1395	2024-11-01 22:01:21.535033+00	828	Transaction object (828)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1396	2024-11-01 22:02:38.236321+00	829	Transaction object (829)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1397	2024-11-01 22:03:19.732094+00	830	Transaction object (830)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1398	2024-11-01 22:03:58.13327+00	831	Transaction object (831)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 285"}}]	26	3
1399	2024-11-01 22:04:27.441015+00	832	Transaction object (832)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1400	2024-11-01 22:05:09.632953+00	833	Transaction object (833)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1401	2024-11-01 22:06:02.125219+00	834	Transaction object (834)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1402	2024-11-01 22:06:40.831017+00	835	Transaction object (835)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 13"}}]	26	3
1403	2024-11-01 22:07:18.613713+00	836	Transaction object (836)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1404	2024-11-01 22:08:28.495729+00	221	LeidyMassielRodriguez	1	[{"added": {}}]	25	3
1405	2024-11-01 22:08:54.54266+00	361	LeidyMassielRodriguez - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
1406	2024-11-01 22:15:21.149812+00	362	MariamTrejos - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
1407	2024-11-01 22:29:54.447073+00	839	Transaction object (839)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1408	2024-11-01 22:30:30.941292+00	840	Transaction object (840)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1409	2024-11-01 22:31:01.838589+00	841	Transaction object (841)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1410	2024-11-02 00:19:48.721882+00	169	Transaction object (169)	2	[{"changed": {"fields": ["Date"]}}]	26	3
1411	2024-11-02 00:20:14.216609+00	216	Transaction object (216)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70.00", "fields": ["Amount", "Amount paid"]}}]	26	3
1412	2024-11-02 00:23:18.837244+00	363	BelisarioRodriguez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1413	2024-11-02 00:24:22.836044+00	843	Transaction object (843)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1414	2024-11-02 00:31:08.950555+00	844	Transaction object (844)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1415	2024-11-02 00:31:40.523627+00	845	Transaction object (845)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1416	2024-11-02 00:32:12.924176+00	846	Transaction object (846)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1417	2024-11-02 00:41:06.817547+00	94	RogelioCorro - Créditos - Crédito Personal: Credit:500.00, pending:500.00	3		28	3
1418	2024-11-02 00:43:08.525061+00	847	Transaction object (847)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 300"}}]	26	3
1419	2024-11-02 00:45:13.64553+00	848	Transaction object (848)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 500"}}]	26	3
1420	2024-11-02 00:46:26.322095+00	849	Transaction object (849)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 400"}}]	26	3
1421	2024-11-02 00:46:56.037008+00	364	RogelioCorro - Créditos - Crédito Personal: Credit:800, pending:800	1	[{"added": {}}]	28	3
1422	2024-11-02 00:49:03.535542+00	851	Transaction object (851)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
1423	2024-11-02 00:56:40.856407+00	852	Transaction object (852)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1424	2024-11-02 00:57:34.12687+00	132	ArianaMares - Créditos - Crédito Personal: Credit:660.00, pending:160.00	2	[{"changed": {"fields": ["Price"]}}]	28	3
1425	2024-11-02 00:57:51.216451+00	853	Transaction object (853)	1	[{"added": {}}]	26	3
1426	2024-11-02 00:58:35.439337+00	853	Transaction object (853)	2	[{"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1427	2024-11-05 21:40:04.836017+00	854	Transaction object (854)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1428	2024-11-05 21:41:57.71996+00	222	LizdeMora	1	[{"added": {}}]	25	3
1429	2024-11-05 21:42:21.338618+00	365	LizdeMora - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1430	2024-11-05 21:45:50.112999+00	223	JoséAdrianoPérez	1	[{"added": {}}]	25	3
1431	2024-11-05 21:46:20.761535+00	366	JoséAdrianoPérez - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
1432	2024-11-05 21:54:16.029913+00	857	Transaction object (857)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1433	2024-11-05 21:56:10.018873+00	151	YarisnethCárdenas - Créditos - Crédito Personal: Credit:140.00, pending:70.00	3		28	3
1434	2024-11-05 21:59:41.141268+00	224	AlbaCeciliaAyalaHerrera	1	[{"added": {}}]	25	3
1435	2024-11-05 22:00:10.04248+00	367	AlbaCeciliaAyalaHerrera - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1436	2024-11-05 22:02:36.625225+00	225	Hernal	1	[{"added": {}}]	25	3
1437	2024-11-05 22:06:07.02968+00	368	Hernal - Créditos - Crédito Personal: Credit:810, pending:810	1	[{"added": {}}]	28	3
1438	2024-11-05 22:06:57.353203+00	860	Transaction object (860)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1439	2024-11-05 22:07:20.530107+00	861	Transaction object (861)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1440	2024-11-05 22:18:01.337524+00	119	JoseSanchez - Créditos - Crédito Personal: Credit:330, pending:30.00	2	[{"changed": {"fields": ["Cost", "Price"]}}]	28	3
1441	2024-11-05 22:18:55.627875+00	862	Transaction object (862)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1442	2024-11-05 22:20:17.267882+00	369	JoseSanchez - Créditos - Crédito Personal: Credit:1025, pending:1025	1	[{"added": {}}]	28	3
1443	2024-11-07 01:36:04.128423+00	226	BenjaminFerreteria	1	[{"added": {}}]	25	3
1444	2024-11-07 01:36:34.946818+00	370	BenjaminFerreteria - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
1445	2024-11-08 22:49:52.847069+00	865	Transaction object (865)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
1446	2024-11-08 22:53:11.73953+00	371	JoséSamuelQuiroz - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1447	2024-11-08 22:54:19.728299+00	373	CarlosKike - Créditos - Crédito Personal: Credit:25, pending:25	1	[{"added": {}}]	28	3
1448	2024-11-08 23:01:17.018644+00	227	CarlosIvanOvalle	1	[{"added": {}}]	25	3
1449	2024-11-08 23:01:35.446911+00	374	CarlosIvanOvalle - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
1450	2024-11-08 23:02:19.137766+00	870	Transaction object (870)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1451	2024-11-08 23:03:02.250555+00	871	Transaction object (871)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1452	2024-11-08 23:03:46.555612+00	872	Transaction object (872)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1453	2024-11-08 23:04:19.635118+00	873	Transaction object (873)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1454	2024-11-08 23:05:59.234474+00	874	Transaction object (874)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1455	2024-11-08 23:09:07.518889+00	199	JoseDavidPanaderia	2	[{"changed": {"fields": ["Username"]}}]	25	3
1456	2024-11-08 23:09:49.220769+00	875	Transaction object (875)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Yappy - Amount Paid: 70"}}]	26	3
1457	2024-11-08 23:10:31.822025+00	75	AnnaMares	2	[{"changed": {"fields": ["Username", "First name"]}}]	25	3
1458	2024-11-08 23:11:18.925701+00	375	AnnaMares - Créditos - Crédito Personal: Credit:840, pending:840	1	[{"added": {}}]	28	3
1459	2024-11-08 23:19:21.324518+00	877	Transaction object (877)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1460	2024-11-08 23:19:59.842031+00	878	Transaction object (878)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1461	2024-11-08 23:20:47.434126+00	879	Transaction object (879)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1462	2024-11-08 23:33:49.529027+00	880	Transaction object (880)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1463	2024-11-08 23:34:27.621499+00	881	Transaction object (881)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1464	2024-11-08 23:35:26.827711+00	882	Transaction object (882)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1465	2024-11-08 23:36:33.365942+00	883	Transaction object (883)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1466	2024-11-08 23:37:03.920124+00	884	Transaction object (884)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1467	2024-11-08 23:37:52.03706+00	885	Transaction object (885)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1468	2024-11-08 23:40:47.926857+00	886	Transaction object (886)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1469	2024-11-08 23:41:28.328205+00	887	Transaction object (887)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1470	2024-11-08 23:42:13.826797+00	888	Transaction object (888)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1471	2024-11-08 23:43:03.822576+00	889	Transaction object (889)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1472	2024-11-08 23:59:46.556751+00	890	Transaction object (890)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
1473	2024-11-09 00:01:09.011801+00	29	Mundo Magico	1	[{"added": {}}]	18	3
1474	2024-11-09 00:01:11.701979+00	228	CristianJoelMendoza	1	[{"added": {}}]	25	3
1475	2024-11-09 00:01:32.614519+00	376	CristianJoelMendoza - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
1476	2024-11-09 00:04:54.024876+00	892	Transaction object (892)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1477	2024-11-09 00:06:48.743677+00	893	Transaction object (893)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1478	2024-11-09 00:08:04.842429+00	894	Transaction object (894)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1479	2024-11-09 00:09:37.120354+00	895	Transaction object (895)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1480	2024-11-09 00:12:04.944604+00	896	Transaction object (896)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1481	2024-11-09 00:12:37.739929+00	897	Transaction object (897)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1482	2024-11-09 00:20:58.738946+00	88	Gastos de actividad - Viatico - 13	1	[{"added": {}}]	27	3
1483	2024-11-09 00:21:58.240085+00	89	Gastos de actividad - Viatico - 13.50	1	[{"added": {}}]	27	3
1484	2024-11-09 00:22:13.238355+00	90	Gastos de actividad - Transporte - 1.50	1	[{"added": {}}]	27	3
1485	2024-11-09 00:23:20.025261+00	898	Transaction object (898)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1486	2024-11-09 00:24:19.646382+00	899	Transaction object (899)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1487	2024-11-09 00:24:45.124325+00	900	Transaction object (900)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1488	2024-11-09 00:25:01.628208+00	900	Transaction object (900)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50.00", "fields": ["Currency"]}}]	26	3
1489	2024-11-09 00:25:37.450033+00	901	Transaction object (901)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1490	2024-11-09 00:27:35.125558+00	902	Transaction object (902)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
1491	2024-11-09 00:28:07.927528+00	903	Transaction object (903)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1643	2024-11-14 19:25:28.185845+00	173	ArmandoRodriguezGonzales	2	[{"changed": {"fields": ["Label"]}}]	25	3
1492	2024-11-09 00:28:43.335722+00	904	Transaction object (904)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1493	2024-11-09 00:30:19.534859+00	377	IrisdelCarmen - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1494	2024-11-09 00:31:29.827778+00	906	Transaction object (906)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1495	2024-11-09 00:32:16.828321+00	907	Transaction object (907)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1496	2024-11-09 00:33:38.226393+00	908	Transaction object (908)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1497	2024-11-09 00:46:22.819287+00	909	Transaction object (909)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
1498	2024-11-09 00:46:50.914418+00	910	Transaction object (910)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1499	2024-11-09 00:47:23.535297+00	911	Transaction object (911)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 33"}}]	26	3
1500	2024-11-09 00:49:26.524526+00	912	Transaction object (912)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 175"}}]	26	3
1501	2024-11-09 00:57:10.128256+00	370	BenjaminFerreteria - Créditos - Crédito Personal: Credit:330.00, pending:330.00	2	[{"changed": {"fields": ["Created at"]}}]	28	3
1502	2024-11-09 00:58:53.130309+00	913	Transaction object (913)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1503	2024-11-09 00:59:24.13066+00	914	Transaction object (914)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1504	2024-11-09 00:59:47.53822+00	915	Transaction object (915)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1505	2024-11-09 01:00:47.668242+00	378	BenjaminFerreteria - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
1506	2024-11-09 01:01:29.634486+00	917	Transaction object (917)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 167"}}]	26	3
1507	2024-11-09 01:02:26.32896+00	918	Transaction object (918)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1508	2024-11-09 01:03:34.617679+00	918	Transaction object (918)	3		26	3
1509	2024-11-09 01:09:51.731973+00	919	Transaction object (919)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1510	2024-11-09 01:13:33.939339+00	379	JorgeCordoba - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
1511	2024-11-09 01:19:32.620373+00	921	Transaction object (921)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1512	2024-11-09 01:20:20.829292+00	921	Transaction object (921)	2	[{"changed": {"fields": ["User"]}}, {"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220", "fields": ["Amount", "Amount paid", "Credit"]}}]	26	3
1513	2024-11-09 01:21:37.036945+00	380	JuanAguilar - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1514	2024-11-09 01:22:07.523057+00	381	ManuelSanchez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1515	2024-11-09 01:23:02.330155+00	383	EdgarSoto - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
1516	2024-11-09 01:23:45.330524+00	926	Transaction object (926)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1517	2024-11-09 01:24:37.021087+00	927	Transaction object (927)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1518	2024-11-09 01:26:07.927056+00	928	Transaction object (928)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1519	2024-11-09 01:28:53.924199+00	384	AlvaroGonzalezGomez - Créditos - Crédito Personal: Credit:270, pending:270	1	[{"added": {}}]	28	3
1520	2024-11-09 01:29:31.527719+00	91	Gastos de actividad - Otros - 274	1	[{"added": {}}]	27	3
1521	2024-11-09 01:30:18.23543+00	930	Transaction object (930)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1522	2024-11-09 01:33:34.930458+00	931	Transaction object (931)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1523	2024-11-09 01:34:33.233146+00	385	MereidaRodriguez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1524	2024-11-09 01:35:36.259742+00	229	AbdelDeleon	1	[{"added": {}}]	25	3
1525	2024-11-09 01:35:54.21477+00	386	AbdelDeleon - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1526	2024-11-09 01:39:42.330812+00	934	Transaction object (934)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1527	2024-11-09 01:40:32.932706+00	935	Transaction object (935)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1528	2024-11-09 01:41:30.429388+00	936	Transaction object (936)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1529	2024-11-09 01:42:25.330185+00	937	Transaction object (937)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1530	2024-11-09 01:43:31.728478+00	92	Créditos - Pago a Crédito de Consumo - 23	1	[{"added": {}}]	27	3
1531	2024-11-10 20:02:53.833513+00	938	Transaction object (938)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 33"}}]	26	3
1532	2024-11-10 20:16:40.038052+00	387	GenaroRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1533	2024-11-10 20:18:06.537386+00	940	Transaction object (940)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 64"}}]	26	3
1534	2024-11-10 20:18:40.922939+00	941	Transaction object (941)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1535	2024-11-10 20:19:37.6187+00	230	PabloZyZ	1	[{"added": {}}]	25	3
1536	2024-11-10 20:19:55.931224+00	388	PabloZyZ - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1537	2024-11-10 20:20:50.338788+00	943	Transaction object (943)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1538	2024-11-10 20:21:32.24103+00	944	Transaction object (944)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1539	2024-11-10 20:23:19.416919+00	945	Transaction object (945)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1540	2024-11-10 20:23:45.723648+00	946	Transaction object (946)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1541	2024-11-10 20:24:19.12287+00	947	Transaction object (947)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Banesco - Amount Paid: 100"}}]	26	3
1542	2024-11-10 20:25:22.147158+00	389	enriquefritos - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1543	2024-11-10 20:26:00.658372+00	390	FranciscoMendoza - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1544	2024-11-10 20:27:25.73316+00	397	JorgeCamel - Créditos - Crédito Personal: Credit:260, pending:260	1	[{"added": {}}]	28	3
1545	2024-11-10 20:27:53.907433+00	93	Gastos de actividad - Viatico - 64	1	[{"added": {}}]	27	3
1546	2024-11-10 20:28:08.33247+00	94	Gastos de actividad - Otros - 80	1	[{"added": {}}]	27	3
1547	2024-11-10 20:28:30.629766+00	95	Gastos de actividad - Viatico - 40	1	[{"added": {}}]	27	3
1548	2024-11-10 20:28:45.740284+00	96	Gastos de actividad - Gasolina - 32	1	[{"added": {}}]	27	3
1549	2024-11-10 20:31:45.020259+00	231	SaulHumbertoSaens	1	[{"added": {}}]	25	3
1550	2024-11-10 20:32:13.627554+00	398	SaulHumbertoSaens - Créditos - Crédito Personal: Credit:110, pending:110	1	[{"added": {}}]	28	3
1551	2024-11-10 20:34:35.833483+00	958	Transaction object (958)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 320"}}]	26	3
1552	2024-11-10 20:35:11.146769+00	959	Transaction object (959)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1553	2024-11-10 20:35:46.864899+00	960	Transaction object (960)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1554	2024-11-10 20:36:16.435448+00	961	Transaction object (961)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1555	2024-11-10 20:36:50.870787+00	97	Gastos de actividad - Viatico - 15	1	[{"added": {}}]	27	3
1556	2024-11-10 20:37:10.82243+00	98	Gastos de actividad - Viatico - 7	1	[{"added": {}}]	27	3
1557	2024-11-10 20:37:46.036907+00	399	CatalinaMartinez - Créditos - Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
1558	2024-11-10 20:38:26.131969+00	400	BiancaCoronado - Créditos - Crédito Personal: Credit:480, pending:480	1	[{"added": {}}]	28	3
1559	2024-11-10 20:39:19.420528+00	964	Transaction object (964)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1560	2024-11-10 20:41:09.716153+00	210	RicardoPerez - Créditos - Crédito Personal: Credit:140.00, pending:90.00	3		28	3
1561	2024-11-10 20:41:39.628696+00	418	Transaction object (418)	3		26	3
1562	2024-11-10 20:41:50.919559+00	599	Transaction object (599)	3		26	3
1563	2024-11-10 20:42:02.312329+00	541	Transaction object (541)	3		26	3
1564	2024-11-10 20:42:55.632548+00	965	Transaction object (965)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1565	2024-11-10 20:43:22.94653+00	966	Transaction object (966)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1566	2024-11-10 20:45:00.321157+00	99	Créditos - Pago a Crédito Personal - 30	1	[{"added": {}}]	27	3
1567	2024-11-10 20:45:39.239912+00	401	RicardoPerez - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
1568	2024-11-10 20:46:06.033378+00	402	CarlosRangel - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1569	2024-11-10 20:47:01.355577+00	408	Lazaro - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1570	2024-11-10 20:48:39.952648+00	975	Transaction object (975)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1571	2024-11-10 20:49:06.750792+00	976	Transaction object (976)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1572	2024-11-10 20:49:46.03051+00	409	leonardovaldez - Créditos - Crédito Personal: Credit:2500, pending:2500	1	[{"added": {}}]	28	3
1573	2024-11-10 20:50:15.117846+00	100	Gastos de actividad - Viatico - 11.50	1	[{"added": {}}]	27	3
1574	2024-11-10 20:50:33.7302+00	101	Gastos de actividad - Viatico - 13.50	1	[{"added": {}}]	27	3
1575	2024-11-10 20:50:49.722876+00	102	Gastos de actividad - Otros - 300	1	[{"added": {}}]	27	3
1576	2024-11-10 20:51:22.323261+00	103	Gastos de actividad - Viatico - 15.8	1	[{"added": {}}]	27	3
1577	2024-11-10 20:52:28.837999+00	978	Transaction object (978)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1578	2024-11-10 20:53:39.935417+00	979	Transaction object (979)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1579	2024-11-10 20:54:31.856518+00	980	Transaction object (980)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
1580	2024-11-10 20:55:42.026898+00	981	Transaction object (981)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 58"}}]	26	3
1581	2024-11-10 20:56:22.825354+00	982	Transaction object (982)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1582	2024-11-10 20:56:56.856076+00	983	Transaction object (983)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1583	2024-11-10 20:58:40.143842+00	410	IsisRodriguez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1584	2024-11-10 20:59:06.761033+00	411	DiegoAbdielMeneses - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1585	2024-11-10 21:00:01.45308+00	417	YennyGonzalesPerez - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
1586	2024-11-10 23:11:54.432317+00	241	MiguelOrdoñez - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[{"changed": {"fields": ["State"]}}]	28	1
1587	2024-11-12 17:59:52.438319+00	418	CarlosIvanOvalle - Créditos - Crédito Personal: Credit:380, pending:380	1	[{"added": {}}]	28	3
1840	2024-11-22 00:58:42.680396+00	246	ArmandoDicarena	1	[{"added": {}}]	25	3
1588	2024-11-12 18:04:46.740035+00	870	Transaction object (870)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50.00", "fields": ["Credit"]}}]	26	3
1589	2024-11-12 18:05:22.83582+00	993	Transaction object (993)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1590	2024-11-12 18:12:09.825352+00	192	MiguelOrdoñez - Créditos - Crédito Personal: Credit:70.00, pending:70.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1591	2024-11-12 18:21:53.935365+00	225	JavierEscobarMecanico - Créditos - Crédito Personal: Credit:150.00, pending:0.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1592	2024-11-12 18:26:23.031244+00	282	AlvaroAlexis - Créditos - Crédito Personal: Credit:150.00, pending:-10.00	2	[{"changed": {"fields": ["Price"]}}]	28	3
1593	2024-11-12 18:26:36.233765+00	282	AlvaroAlexis - Créditos - Crédito Personal: Credit:140.00, pending:-10.00	2	[{"changed": {"fields": ["Price"]}}]	28	3
1594	2024-11-12 18:29:11.231077+00	95	AndysMartinez - Créditos - Crédito Personal: Credit:140.00, pending:140.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1595	2024-11-12 18:33:34.829059+00	31	JavierEscobarMecanico - Créditos - Crédito de Consumo: Credit:100, pending:50.00	2	[{"changed": {"fields": ["User", "Cost", "Price"]}}]	28	3
1596	2024-11-12 18:34:37.922+00	31	JavierEscobarMecanico - Créditos - Crédito de Consumo: Credit:50, pending:50.00	2	[{"changed": {"fields": ["Cost", "Price"]}}]	28	3
1597	2024-11-12 21:17:27.329397+00	994	Transaction object (994)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 115"}}]	26	3
1598	2024-11-12 21:19:21.031201+00	158	Transaction object (158)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90.00", "fields": ["Credit"]}}]	26	3
1599	2024-11-12 21:19:58.945279+00	93	GladysMontero - Créditos - Crédito Personal: Credit:140.00, pending:50.00	2	[]	28	3
1600	2024-11-12 21:22:55.321803+00	419	MorrisProfesor - Créditos - Crédito Personal: Credit:1000, pending:1000	1	[{"added": {}}]	28	3
1601	2024-11-12 21:23:23.721915+00	98	MariaTuñon	2	[{"changed": {"fields": ["Label"]}}]	25	3
1602	2024-11-12 21:23:51.329237+00	143	MariaTuñon - Créditos - Crédito Personal: Credit:115.00, pending:115.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1603	2024-11-12 21:24:33.143955+00	257	MariaTuñon - Créditos - Crédito Personal: Credit:50.00, pending:50.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1604	2024-11-12 21:25:34.636267+00	420	MariaTuñon - Créditos - Crédito Personal: Credit:1200, pending:1200	1	[{"added": {}}]	28	3
1605	2024-11-12 21:32:35.220253+00	421	PublioProfe - Créditos - Crédito Personal: Credit:800, pending:800	1	[{"added": {}}]	28	3
1606	2024-11-12 21:45:35.056012+00	164	JorgeCordoba	2	[{"changed": {"fields": ["Label"]}}]	25	3
1607	2024-11-12 21:49:45.447722+00	29	LuisGonzales - Créditos - Crédito de Consumo: Credit:50.00, pending:40.00	2	[{"changed": {"fields": ["Description"]}}]	28	3
1608	2024-11-12 21:51:13.452178+00	422	LuisGonzales - Créditos - Crédito Personal: Credit:570, pending:570	1	[{"added": {}}]	28	3
1609	2024-11-12 21:51:57.524091+00	232	LuisGonzalesHermano	1	[{"added": {}}]	25	3
1610	2024-11-12 21:52:00.639112+00	103	LuisGonzalesHermano - Créditos - Crédito Personal: Credit:270.00, pending:270.00	2	[{"changed": {"fields": ["User"]}}]	28	3
1611	2024-11-12 21:52:34.639229+00	69	Ubaldo - Créditos - Crédito Personal: Credit:90.00, pending:-10.00	2	[{"changed": {"fields": ["Price"]}}]	28	3
1612	2024-11-12 21:52:52.933937+00	217	AnaIsabelFernandez - Créditos - Pago a Crédito de Consumo: Credit:115.00, pending:65.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1613	2024-11-12 21:57:35.136761+00	604	Transaction object (604)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110.00", "fields": ["Amount", "Amount paid"]}}]	26	3
1614	2024-11-12 21:58:54.940478+00	131	Transaction object (131)	3		26	3
1615	2024-11-12 21:59:14.931386+00	57	JoseLuisFernandez - Créditos - Crédito Personal: Credit:90.00, pending:90.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1616	2024-11-12 22:01:02.242908+00	423	JoseLuisFernandez - Créditos - Crédito Personal: Credit:300, pending:300	1	[{"added": {}}]	28	3
1617	2024-11-12 22:02:06.429965+00	1000	Transaction object (1000)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1618	2024-11-12 22:02:43.647005+00	1001	Transaction object (1001)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1619	2024-11-12 22:02:56.614075+00	57	JoseLuisFernandez - Créditos - Crédito Personal: Credit:90.00, pending:90.00	3		28	3
1620	2024-11-12 22:05:19.547805+00	249	Transaction object (249)	2	[{"changed": {"fields": ["Date"]}}, {"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20.00", "fields": ["Payment code"]}}]	26	3
1621	2024-11-12 22:10:17.220293+00	233	ReinaldoPérez	1	[{"added": {}}]	25	3
1622	2024-11-12 22:11:26.42355+00	424	ReinaldoPérez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1623	2024-11-12 22:13:05.44031+00	425	ReinaldoPérez - Créditos - Pago a Crédito de Consumo: Credit:50, pending:50	1	[{"added": {}}]	28	3
1624	2024-11-12 22:14:29.638276+00	426	ReinaldoPérez - Créditos - Crédito Personal: Credit:35, pending:35	1	[{"added": {}}]	28	3
1625	2024-11-12 22:16:53.134957+00	1005	Transaction object (1005)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1626	2024-11-12 22:21:09.914034+00	40	Lazaro	2	[{"changed": {"fields": ["Label"]}}]	25	3
1627	2024-11-12 22:25:21.010595+00	14	Salomon Ponce	3		18	3
1628	2024-11-12 22:25:54.349294+00	83	ErickMagallon - Créditos - Crédito Personal: Credit:630.00, pending:10.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1629	2024-11-12 22:26:16.649281+00	353	MagalyMaxwell - Créditos - Crédito Personal: Credit:80.00, pending:0.00	2	[{"changed": {"fields": ["Price"]}}]	28	3
1630	2024-11-12 22:44:57.92363+00	148	Trujillo	2	[{"changed": {"fields": ["Label"]}}]	25	3
1631	2024-11-12 22:45:16.744323+00	178	AlcidesOrtegaFlorez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1632	2024-11-12 22:45:40.038824+00	18	MaximinoMartinez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1633	2024-11-12 22:45:57.526574+00	73	ArianaItzel	2	[]	25	3
1634	2024-11-12 22:46:06.728562+00	31	EnockGuerra	2	[]	25	3
1635	2024-11-12 22:46:16.132725+00	29	TomasAlbertoMartinez	2	[]	25	3
1636	2024-11-12 22:46:38.627471+00	24	LuisGonzales	2	[]	25	3
1637	2024-11-12 22:46:51.728611+00	233	ReinaldoPérez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1638	2024-11-12 22:47:02.82231+00	205	MaicolIbarra	2	[]	25	3
1639	2024-11-12 22:47:23.125322+00	227	CarlosIvanOvalle	2	[{"changed": {"fields": ["Label"]}}]	25	3
1640	2024-11-12 22:47:39.028517+00	145	JulianMendoza	2	[{"changed": {"fields": ["Label"]}}]	25	3
1642	2024-11-14 19:24:51.670847+00	30	Hotel Playa Blanca	1	[{"added": {}}]	18	3
1644	2024-11-14 19:27:20.182964+00	94	JoseSanchez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1645	2024-11-14 19:27:47.184551+00	142	DianaEstherPerez	2	[]	25	3
1646	2024-11-14 19:28:00.88257+00	143	JhonatanMartinez	2	[]	25	3
1647	2024-11-14 19:28:12.587602+00	39	MichelAntonio	2	[]	25	3
1648	2024-11-14 19:28:28.071109+00	53	JoseOrmelisArauz	2	[{"changed": {"fields": ["Label"]}}]	25	3
1649	2024-11-14 19:29:10.971104+00	224	AlbaCeciliaAyalaHerrera	2	[{"changed": {"fields": ["Label"]}}]	25	3
1650	2024-11-14 22:03:12.972221+00	183	YarisnethCardenasBijao	2	[{"changed": {"fields": ["Label"]}}]	25	3
1651	2024-11-14 22:03:25.677631+00	133	EdgardoMurillo	2	[{"changed": {"fields": ["Label"]}}]	25	3
1652	2024-11-14 22:03:38.773722+00	15	LeopoldoRamos	2	[{"changed": {"fields": ["Label"]}}]	25	3
1653	2024-11-14 22:05:15.664567+00	234	JoseAdrianoPerez	1	[{"added": {}}]	25	3
1654	2024-11-14 22:05:44.673463+00	427	JoseAdrianoPerez - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
1655	2024-11-14 22:07:47.864516+00	31	Hotel Decameron	1	[{"added": {}}]	18	3
1656	2024-11-14 22:07:56.076479+00	22	JoseLucianoMendoza	2	[{"changed": {"fields": ["Username", "Label"]}}]	25	3
1657	2024-11-16 21:11:55.085402+00	166	LuisArmandoDominguez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1658	2024-11-16 21:12:08.299213+00	168	GustavoErisnelGonzalesLorenzo	2	[{"changed": {"fields": ["Label"]}}]	25	3
1659	2024-11-16 21:13:55.466793+00	249	LuisArmandoDominguezPerez - Créditos - Crédito Personal: Credit:150.00, pending:75.00	3		28	3
1660	2024-11-16 21:14:26.670445+00	533	Transaction object (533)	3		26	3
1661	2024-11-16 21:14:57.381637+00	699	Transaction object (699)	2	[{"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1662	2024-11-20 21:09:58.584416+00	428	MagalyMaxwell - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
1663	2024-11-20 21:11:16.791631+00	429	ANYSANADELKAGONZALEZ - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1664	2024-11-20 21:11:56.97472+00	104	Gastos de actividad - Otros - 20	1	[{"added": {}}]	27	3
1665	2024-11-20 21:23:53.403432+00	1009	Transaction object (1009)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1666	2024-11-20 21:24:21.087075+00	1010	Transaction object (1010)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1667	2024-11-20 21:24:50.679562+00	1011	Transaction object (1011)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1668	2024-11-20 21:25:26.671813+00	1012	Transaction object (1012)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1669	2024-11-20 21:25:55.293899+00	1013	Transaction object (1013)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1670	2024-11-20 21:26:27.773275+00	1014	Transaction object (1014)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1671	2024-11-20 21:26:51.985476+00	105	Gastos de actividad - Otros - 12.50	1	[{"added": {}}]	27	3
1672	2024-11-20 21:27:09.872842+00	106	Gastos de actividad - Viatico - 15	1	[{"added": {}}]	27	3
1673	2024-11-20 21:28:03.481364+00	235	OmarGarcia	1	[{"added": {}}]	25	3
1674	2024-11-20 21:28:22.8683+00	430	OmarGarcia - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
1675	2024-11-20 21:35:45.490788+00	431	AidaProfesora - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1676	2024-11-20 21:37:04.080813+00	330	AidaProfesora - Créditos - Crédito Personal: Credit:150.00, pending:150.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1677	2024-11-20 21:37:14.074913+00	431	AidaProfesora - Créditos - Crédito Personal: Credit:280.00, pending:280.00	2	[{"changed": {"fields": ["Description"]}}]	28	3
1678	2024-11-20 21:40:52.480911+00	1017	Transaction object (1017)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 108"}}]	26	3
1679	2024-11-20 21:41:21.668485+00	1018	Transaction object (1018)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1680	2024-11-20 21:48:54.584208+00	432	JulianMendoza - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
1681	2024-11-20 21:49:22.970284+00	574	Transaction object (574)	3		26	3
1682	2024-11-20 21:49:49.996597+00	432	JulianMendoza - Créditos - Crédito Personal: Credit:360.00, pending:360.00	2	[{"changed": {"fields": ["Description"]}}]	28	3
1683	2024-11-20 21:50:07.496648+00	202	JulianMendoza - Créditos - Crédito Personal: Credit:160.00, pending:160.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1684	2024-11-20 21:52:47.979005+00	1020	Transaction object (1020)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1685	2024-11-20 21:53:20.46718+00	1021	Transaction object (1021)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1686	2024-11-20 21:53:47.377381+00	1022	Transaction object (1022)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1687	2024-11-20 21:54:27.090289+00	433	JulianMendoza - Créditos - Crédito Personal: Credit:330, pending:330	1	[{"added": {}}]	28	3
1688	2024-11-20 21:56:07.889845+00	1024	Transaction object (1024)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
1689	2024-11-20 21:56:39.470778+00	1025	Transaction object (1025)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1690	2024-11-20 21:57:09.673153+00	107	Gastos de actividad - Otros - 24	1	[{"added": {}}]	27	3
1691	2024-11-20 21:57:27.977785+00	108	Gastos de actividad - Viatico - 5.50	1	[{"added": {}}]	27	3
1692	2024-11-20 21:57:41.265513+00	109	Gastos de actividad - Otros - 20	1	[{"added": {}}]	27	3
1693	2024-11-20 21:58:35.985516+00	1026	Transaction object (1026)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1694	2024-11-20 21:59:13.67603+00	1027	Transaction object (1027)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1695	2024-11-20 21:59:47.283716+00	1028	Transaction object (1028)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1696	2024-11-20 22:00:26.09444+00	1029	Transaction object (1029)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1937	2024-11-27 00:28:05.967146+00	125	Gastos de actividad - Otros - 433.8	1	[{"added": {}}]	27	3
1697	2024-11-20 22:01:12.385178+00	1030	Transaction object (1030)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 52"}}]	26	3
1698	2024-11-20 22:01:51.585928+00	1031	Transaction object (1031)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1699	2024-11-20 22:02:19.388386+00	1032	Transaction object (1032)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1700	2024-11-20 22:02:36.084563+00	1031	Transaction object (1031)	2	[{"changed": {"fields": ["Category"]}}]	26	3
1701	2024-11-20 22:04:00.290505+00	434	carlosdelgado - Créditos - Crédito Personal: Credit:132, pending:132	1	[{"added": {}}]	28	3
1702	2024-11-20 22:05:02.093342+00	435	VictoriaCastroRojo - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1703	2024-11-20 22:05:53.191289+00	236	YARELIS	1	[{"added": {}}]	25	3
1704	2024-11-20 22:06:14.385869+00	436	YARELIS - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
1705	2024-11-20 22:07:28.101811+00	437	AlvaroAlexis - Créditos - Crédito Personal: Credit:186, pending:186	1	[{"added": {}}]	28	3
1706	2024-11-20 22:08:28.187484+00	1037	Transaction object (1037)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1707	2024-11-20 22:09:06.181513+00	1038	Transaction object (1038)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
1708	2024-11-20 22:46:53.667805+00	237	GeronimoPerez	1	[{"added": {}}]	25	3
1709	2024-11-20 22:47:11.70142+00	438	GeronimoPerez - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
1710	2024-11-20 22:47:57.566356+00	238	MariaGonzález	1	[{"added": {}}]	25	3
1711	2024-11-20 22:48:24.302894+00	439	MariaGonzález - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1712	2024-11-20 22:48:57.477433+00	110	Gastos de actividad - Viatico - 1.50	1	[{"added": {}}]	27	3
1713	2024-11-20 22:49:14.668911+00	111	Gastos de actividad - Viatico - 50	1	[{"added": {}}]	27	3
1714	2024-11-20 22:52:10.37751+00	1041	Transaction object (1041)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1715	2024-11-20 22:52:45.367578+00	1042	Transaction object (1042)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
1716	2024-11-20 22:53:19.498318+00	440	MiguelOrdoñez - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
1717	2024-11-20 22:54:23.685435+00	1044	Transaction object (1044)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1718	2024-11-20 22:54:52.567635+00	1045	Transaction object (1045)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1719	2024-11-20 22:55:19.382446+00	1046	Transaction object (1046)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1720	2024-11-20 22:55:45.49003+00	1047	Transaction object (1047)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1721	2024-11-20 22:56:26.765767+00	1048	Transaction object (1048)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 180"}}]	26	3
1722	2024-11-20 22:56:57.667509+00	1049	Transaction object (1049)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1723	2024-11-20 22:57:44.801297+00	1050	Transaction object (1050)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 270"}}]	26	3
1724	2024-11-20 22:58:17.894208+00	1051	Transaction object (1051)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1725	2024-11-20 22:58:54.493147+00	1052	Transaction object (1052)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1726	2024-11-20 23:04:18.591697+00	1053	Transaction object (1053)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1727	2024-11-20 23:05:30.991064+00	1054	Transaction object (1054)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1728	2024-11-20 23:06:16.189298+00	1055	Transaction object (1055)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1729	2024-11-20 23:06:54.967398+00	1056	Transaction object (1056)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1730	2024-11-20 23:07:30.277205+00	1057	Transaction object (1057)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1731	2024-11-20 23:08:21.574469+00	441	ErickMartinez - Créditos - Crédito Personal: Credit:1400, pending:1400	1	[{"added": {}}]	28	3
1732	2024-11-20 23:09:13.395412+00	112	Gastos de actividad - Otros - 238	1	[{"added": {}}]	27	3
1733	2024-11-20 23:09:28.280803+00	113	Gastos de actividad - Viatico - 9.80	1	[{"added": {}}]	27	3
1734	2024-11-20 23:09:49.580311+00	114	Gastos de actividad - Otros - 28	1	[{"added": {}}]	27	3
1735	2024-11-20 23:10:53.78888+00	1059	Transaction object (1059)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1736	2024-11-20 23:11:28.582318+00	1060	Transaction object (1060)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
1737	2024-11-20 23:12:47.283774+00	1061	Transaction object (1061)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1738	2024-11-20 23:13:48.268461+00	1062	Transaction object (1062)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 115"}}]	26	3
1739	2024-11-20 23:14:23.475886+00	1063	Transaction object (1063)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1740	2024-11-20 23:16:01.788827+00	442	MiguelOrdoñez - Créditos - Crédito Personal: Credit:85, pending:85	1	[{"added": {}}]	28	3
1741	2024-11-20 23:17:03.480683+00	448	IgnacioVega - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1742	2024-11-20 23:18:07.695364+00	456	KisilMarketAnton - Créditos - Crédito Personal: Credit:40, pending:40	1	[{"added": {}}]	28	3
1743	2024-11-20 23:19:39.065472+00	457	MiguelArquiñez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1744	2024-11-20 23:21:10.581991+00	1080	Transaction object (1080)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 285"}}]	26	3
1745	2024-11-20 23:21:48.779758+00	1081	Transaction object (1081)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 280"}}]	26	3
1746	2024-11-20 23:26:10.389329+00	458	OmairaCuava - Créditos - Pago a Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1747	2024-11-20 23:27:36.167873+00	1083	Transaction object (1083)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 500"}}]	26	3
1748	2024-11-20 23:35:59.592276+00	459	StefanyFernandez - Créditos - Crédito Personal: Credit:460, pending:460	1	[{"added": {}}]	28	3
1749	2024-11-20 23:37:23.39132+00	1085	Transaction object (1085)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1750	2024-11-20 23:41:37.687977+00	32	Banco Banesco	1	[{"added": {}}]	18	3
1751	2024-11-20 23:41:43.08297+00	239	JoseVillaverde	1	[{"added": {}}]	25	3
1752	2024-11-20 23:41:58.78271+00	460	JoseVillaverde - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1753	2024-11-20 23:43:13.492954+00	1087	Transaction object (1087)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1754	2024-11-20 23:44:11.182719+00	1088	Transaction object (1088)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1755	2024-11-20 23:44:47.668657+00	1089	Transaction object (1089)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1756	2024-11-20 23:46:09.17001+00	240	BelkisErickMartinez	1	[{"added": {}}]	25	3
1757	2024-11-20 23:46:13.695072+00	441	BelkisErickMartinez - Créditos - Crédito Personal: Credit:1400.00, pending:1400.00	2	[{"changed": {"fields": ["User"]}}]	28	3
1758	2024-11-20 23:46:48.350062+00	1090	Transaction object (1090)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1759	2024-11-20 23:47:24.888246+00	1091	Transaction object (1091)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1760	2024-11-20 23:48:08.677626+00	1092	Transaction object (1092)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1761	2024-11-20 23:54:45.08086+00	1093	Transaction object (1093)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 285"}}]	26	3
1762	2024-11-20 23:59:47.291051+00	1094	Transaction object (1094)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1763	2024-11-21 00:00:33.767221+00	1095	Transaction object (1095)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
1764	2024-11-21 00:07:57.885683+00	88	OscarAlbertoArauz	2	[{"changed": {"fields": ["Username", "First name", "Last name"]}}]	25	3
1765	2024-11-21 00:13:40.779421+00	189	OscarAlbertSuegro	2	[{"changed": {"fields": ["Username"]}}]	25	3
1766	2024-11-21 00:27:45.391815+00	654	Transaction object (654)	2	[{"changed": {"fields": ["Date"]}}, {"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80", "fields": ["Payment code", "Amount", "Amount paid"]}}]	26	3
1767	2024-11-21 00:30:58.286241+00	306	OscarAlbertoArauz - Créditos - Crédito Personal: Credit:150.00, pending:75.00	2	[{"changed": {"fields": ["Subcategory"]}}]	28	3
1768	2024-11-21 00:31:47.079772+00	691	Transaction object (691)	2	[{"changed": {"fields": ["Category"]}}]	26	3
1769	2024-11-21 00:34:12.176362+00	461	OscarAlbertoArauz - Créditos - Crédito Personal: Credit:240, pending:240	1	[{"added": {}}]	28	3
1770	2024-11-21 00:35:23.272636+00	1097	Transaction object (1097)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1771	2024-11-21 00:38:06.780028+00	1098	Transaction object (1098)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
1772	2024-11-21 00:44:01.787238+00	462	AndysBarrera - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1773	2024-11-21 00:44:30.491021+00	830	Transaction object (830)	2	[{"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20.00", "fields": ["Credit"]}}]	26	3
1774	2024-11-21 00:45:26.994401+00	1100	Transaction object (1100)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1775	2024-11-21 00:46:11.900782+00	1101	Transaction object (1101)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1776	2024-11-21 00:46:53.364548+00	283	AndysBarrera - Créditos - Crédito Personal: Credit:140.00, pending:120.00	3		28	3
1777	2024-11-21 00:47:14.869036+00	616	Transaction object (616)	3		26	3
1778	2024-11-21 00:47:56.686218+00	463	AndysBarrera - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1779	2024-11-21 00:48:34.591338+00	1103	Transaction object (1103)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1780	2024-11-21 00:49:15.984742+00	464	AndysBarrera - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1781	2024-11-21 00:50:20.497928+00	1105	Transaction object (1105)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 15"}}]	26	3
1782	2024-11-21 00:50:46.189234+00	1106	Transaction object (1106)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 280"}}]	26	3
1783	2024-11-21 00:51:14.509999+00	1107	Transaction object (1107)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 800"}}]	26	3
1784	2024-11-21 00:51:54.478332+00	465	PublioProfe - Créditos - Crédito Personal: Credit:750, pending:750	1	[{"added": {}}]	28	3
1785	2024-11-21 19:01:51.695762+00	1109	Transaction object (1109)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
1786	2024-11-21 19:03:38.868351+00	1110	Transaction object (1110)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 700"}}]	26	3
1787	2024-11-21 19:05:37.694501+00	466	CarlosKike - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
1788	2024-11-21 19:06:27.172418+00	467	MariaTuñon - Créditos - Crédito Personal: Credit:800, pending:800	1	[{"added": {}}]	28	3
1789	2024-11-21 19:07:19.409981+00	1113	Transaction object (1113)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1790	2024-11-21 19:08:32.693014+00	1114	Transaction object (1114)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1791	2024-11-21 19:09:07.67337+00	1115	Transaction object (1115)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1792	2024-11-21 19:09:41.670081+00	1116	Transaction object (1116)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1793	2024-11-21 19:10:53.371396+00	1117	Transaction object (1117)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1794	2024-11-21 19:12:10.180567+00	115	Gastos de actividad - Otros - 20	1	[{"added": {}}]	27	3
1795	2024-11-21 19:12:50.579173+00	116	Gastos de actividad - Viatico - 15	1	[{"added": {}}]	27	3
1796	2024-11-21 19:13:04.448362+00	117	Gastos de actividad - Viatico - 25	1	[{"added": {}}]	27	3
1797	2024-11-21 19:13:22.78648+00	118	Gastos de actividad - Otros - 8	1	[{"added": {}}]	27	3
1798	2024-11-21 19:15:38.992461+00	1118	Transaction object (1118)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1799	2024-11-21 19:22:36.888928+00	468	AidaProfesora - Créditos - Crédito Personal: Credit:550, pending:550	1	[{"added": {}}]	28	3
1800	2024-11-21 19:23:49.468637+00	33	Mega Xpress	1	[{"added": {}}]	18	3
1801	2024-11-21 19:23:51.471792+00	241	AuraTorres	1	[{"added": {}}]	25	3
1802	2024-11-21 19:24:18.690969+00	469	AuraTorres - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1803	2024-11-21 21:45:26.270906+00	421	PublioProfe - Créditos - Crédito Personal: Credit:800.00, pending:800.00	3		28	3
1804	2024-11-21 21:45:42.165409+00	150	PublioProfe - Créditos - Crédito Personal: Credit:800.00, pending:0.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1805	2024-11-21 21:45:51.596547+00	118	PublioProfe - Créditos - Crédito Personal: Credit:450.00, pending:0.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1806	2024-11-22 00:07:33.168304+00	1121	Transaction object (1121)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1807	2024-11-22 00:07:58.583384+00	1122	Transaction object (1122)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1808	2024-11-22 00:09:08.586574+00	306	OscarAlbertSuegro - Créditos - Crédito Personal: Credit:150.00, pending:75.00	2	[{"changed": {"fields": ["User"]}}]	28	3
1809	2024-11-22 00:09:55.382934+00	1123	Transaction object (1123)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1810	2024-11-22 00:11:07.672372+00	470	OscarAlbertSuegro - Créditos - Crédito Personal: Credit:135, pending:135	1	[{"added": {}}]	28	3
1811	2024-11-22 00:12:23.582611+00	1125	Transaction object (1125)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1812	2024-11-22 00:12:47.096828+00	1126	Transaction object (1126)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1813	2024-11-22 00:13:12.591501+00	1127	Transaction object (1127)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1814	2024-11-22 00:14:47.27376+00	242	ClaribelTenorio	1	[{"added": {}}]	25	3
1815	2024-11-22 00:15:12.770247+00	471	ClaribelTenorio - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1816	2024-11-22 00:16:50.083979+00	1129	Transaction object (1129)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1817	2024-11-22 00:17:13.688144+00	1130	Transaction object (1130)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1818	2024-11-22 00:17:37.189473+00	1131	Transaction object (1131)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1819	2024-11-22 00:18:35.084764+00	1132	Transaction object (1132)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
1820	2024-11-22 00:33:39.387305+00	243	GustavoBijao	1	[{"added": {}}]	25	3
1821	2024-11-22 00:34:01.872122+00	472	GustavoBijao - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1822	2024-11-22 00:35:06.293937+00	479	MagalyMaxwell - Créditos - Crédito Personal: Credit:35, pending:35	1	[{"added": {}}]	28	3
1823	2024-11-22 00:35:53.186154+00	1141	Transaction object (1141)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1824	2024-11-22 00:36:41.59475+00	1142	Transaction object (1142)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1825	2024-11-22 00:37:07.787938+00	1143	Transaction object (1143)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1826	2024-11-22 00:38:41.981923+00	480	ChristianDomínguez - Créditos - Crédito Personal: Credit:380, pending:380	1	[{"added": {}}]	28	3
1827	2024-11-22 00:41:08.570247+00	244	LicethChavez	1	[{"added": {}}]	25	3
1828	2024-11-22 00:41:31.681384+00	481	LicethChavez - Créditos - Crédito Personal: Credit:60, pending:60	1	[{"added": {}}]	28	3
1829	2024-11-22 00:42:13.382148+00	245	PascualaMartinez	1	[{"added": {}}]	25	3
1830	2024-11-22 00:42:30.891687+00	482	PascualaMartinez - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
1831	2024-11-22 00:43:00.271781+00	119	Gastos de actividad - Viatico - 15.50	1	[{"added": {}}]	27	3
1832	2024-11-22 00:43:15.072747+00	120	Gastos de actividad - Otros - 50	1	[{"added": {}}]	27	3
1833	2024-11-22 00:45:45.490775+00	1147	Transaction object (1147)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1834	2024-11-22 00:46:13.185652+00	1148	Transaction object (1148)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1835	2024-11-22 00:47:10.176751+00	265	ZuleikaGonzalesFonda - Créditos - Crédito Personal: Credit:700.00, pending:400.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1836	2024-11-22 00:48:09.386927+00	483	ZuleikaGonzalesFonda - Créditos - Crédito Personal: Credit:1050, pending:1050	1	[{"added": {}}]	28	3
1837	2024-11-22 00:52:57.485482+00	485	JhonatanSegundo - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1838	2024-11-22 00:53:05.576281+00	486	JhonatanSegundo - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1839	2024-11-22 00:53:17.781475+00	486	JhonatanSegundo - Créditos - Crédito Personal: Credit:140.00, pending:140.00	3		28	3
1841	2024-11-22 00:59:04.196162+00	487	ArmandoDicarena - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
1842	2024-11-22 00:59:54.089734+00	1154	Transaction object (1154)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1843	2024-11-22 01:00:26.485266+00	1155	Transaction object (1155)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1844	2024-11-22 01:00:53.276363+00	1156	Transaction object (1156)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1845	2024-11-22 01:01:42.371626+00	1157	Transaction object (1157)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1846	2024-11-22 01:02:13.279845+00	121	Gastos de actividad - Otros - 338	1	[{"added": {}}]	27	3
1847	2024-11-22 01:02:26.067932+00	122	Gastos de actividad - Viatico - 14	1	[{"added": {}}]	27	3
1848	2024-11-22 01:02:39.372199+00	123	Gastos de actividad - Gasolina - 30.50	1	[{"added": {}}]	27	3
1849	2024-11-22 01:02:57.878666+00	124	Gastos de actividad - Viatico - 12	1	[{"added": {}}]	27	3
1850	2024-11-23 18:06:52.472856+00	1158	Transaction object (1158)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1851	2024-11-23 18:18:26.079775+00	1159	Transaction object (1159)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1852	2024-11-23 19:11:40.988163+00	1160	Transaction object (1160)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1853	2024-11-25 01:47:49.285584+00	27	Do it Center	2	[{"changed": {"fields": ["Name"]}}]	18	1
1854	2024-11-25 01:48:17.559219+00	25	Super Cocle	2	[{"changed": {"fields": ["Name"]}}]	18	1
1855	2024-11-25 01:48:52.111382+00	21	Fonda Familion	2	[{"changed": {"fields": ["Name"]}}]	18	1
1856	2024-11-26 18:54:23.803004+00	1161	Transaction object (1161)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1857	2024-11-26 18:55:13.383617+00	1162	Transaction object (1162)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1858	2024-11-26 19:11:26.980495+00	247	KrizelBetancurt	1	[{"added": {}}]	25	3
1859	2024-11-26 19:11:49.474408+00	488	KrizelBetancurt - Créditos - Crédito Personal: Credit:280, pending:280	1	[{"added": {}}]	28	3
1860	2024-11-26 19:19:53.379917+00	1164	Transaction object (1164)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1861	2024-11-26 19:29:36.990727+00	1165	Transaction object (1165)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1862	2024-11-26 19:31:37.236854+00	1166	Transaction object (1166)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1863	2024-11-26 19:36:05.980852+00	1167	Transaction object (1167)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 167"}}]	26	3
1864	2024-11-26 19:41:18.173541+00	489	MaricelEsther - Créditos - Crédito Personal: Credit:501, pending:501	1	[{"added": {}}]	28	3
1865	2024-11-26 19:41:58.883958+00	1169	Transaction object (1169)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 150"}}]	26	3
1866	2024-11-26 19:44:19.386562+00	490	BelisarioRodriguez - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
1867	2024-11-26 19:45:25.594234+00	1171	Transaction object (1171)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1868	2024-11-26 19:45:55.476668+00	1172	Transaction object (1172)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1869	2024-11-26 19:47:06.179457+00	1173	Transaction object (1173)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1870	2024-11-26 19:48:19.36792+00	1174	Transaction object (1174)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1871	2024-11-26 19:54:24.478453+00	1175	Transaction object (1175)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1872	2024-11-26 20:57:26.095488+00	1176	Transaction object (1176)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1873	2024-11-26 20:58:06.092662+00	1177	Transaction object (1177)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 200"}}]	26	3
1874	2024-11-26 20:58:41.669633+00	1178	Transaction object (1178)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
1875	2024-11-26 21:02:16.172518+00	1179	Transaction object (1179)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1876	2024-11-26 21:06:05.174696+00	1180	Transaction object (1180)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1877	2024-11-26 21:09:24.06719+00	491	SeleneIbarra - Créditos - Crédito Personal: Credit:1140, pending:1140	1	[{"added": {}}]	28	3
1878	2024-11-26 21:10:29.592274+00	1182	Transaction object (1182)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
1879	2024-11-26 21:11:18.686385+00	1183	Transaction object (1183)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 125"}}]	26	3
1880	2024-11-26 21:13:00.283548+00	1184	Transaction object (1184)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 280"}}]	26	3
1881	2024-11-26 21:13:38.269421+00	1185	Transaction object (1185)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 550"}}]	26	3
1882	2024-11-26 21:43:46.904557+00	1186	Transaction object (1186)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
1883	2024-11-26 21:44:25.381016+00	1187	Transaction object (1187)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1884	2024-11-26 21:45:04.603385+00	492	VictorMorales - Créditos - Crédito Personal: Credit:550, pending:550	1	[{"added": {}}]	28	3
1885	2024-11-26 21:47:12.189006+00	1189	Transaction object (1189)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1886	2024-11-26 21:47:38.48274+00	1190	Transaction object (1190)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 110"}}]	26	3
1887	2024-11-26 21:48:23.184991+00	1191	Transaction object (1191)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1888	2024-11-26 21:51:05.681346+00	1192	Transaction object (1192)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1889	2024-11-26 21:53:29.677523+00	493	WuendyRangel - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1890	2024-11-26 22:01:30.068872+00	248	ElvisRojas	1	[{"added": {}}]	25	3
1891	2024-11-26 22:01:53.281407+00	494	ElvisRojas - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
1892	2024-11-26 22:03:02.995147+00	1195	Transaction object (1195)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 500"}}]	26	3
1893	2024-11-26 22:05:53.295205+00	1196	Transaction object (1196)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
1894	2024-11-26 22:21:32.186558+00	1196	Transaction object (1196)	2	[{"changed": {"fields": ["Category"]}}]	26	3
1895	2024-11-26 22:22:06.790471+00	1197	Transaction object (1197)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1896	2024-11-26 22:24:25.291342+00	17	ZoilaOrtega - Créditos - Crédito Personal: Credit:300.00, pending:0.00	2	[{"changed": {"fields": ["State"]}}]	28	3
1897	2024-11-26 22:26:41.026019+00	172	ZoilaOrtega - Créditos - Crédito Personal: Credit:360.00, pending:-160.00	3		28	3
1898	2024-11-26 22:26:58.76535+00	921	Transaction object (921)	3		26	3
1899	2024-11-26 22:27:11.768792+00	663	Transaction object (663)	3		26	3
1900	2024-11-26 22:27:26.124961+00	316	Transaction object (316)	3		26	3
1901	2024-11-26 22:28:09.470699+00	495	ZoilaOrtega - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
1902	2024-11-26 22:34:54.891629+00	1199	Transaction object (1199)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1903	2024-11-26 22:35:26.48112+00	1200	Transaction object (1200)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 220"}}]	26	3
1904	2024-11-26 22:39:57.881321+00	249	CarlosArquiñezKike	1	[{"added": {}}]	25	3
1905	2024-11-26 22:40:00.187753+00	466	CarlosArquiñezKike - Créditos - Crédito Personal: Credit:130.00, pending:130.00	2	[{"changed": {"fields": ["User"]}}]	28	3
1906	2024-11-26 23:04:40.183257+00	1201	Transaction object (1201)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 25"}}]	26	3
1907	2024-11-26 23:05:16.58476+00	1202	Transaction object (1202)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
1908	2024-11-26 23:05:47.783368+00	1203	Transaction object (1203)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
1909	2024-11-26 23:07:11.897355+00	1204	Transaction object (1204)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1910	2024-11-26 23:09:11.401527+00	34	Delta	1	[{"added": {}}]	18	3
1911	2024-11-26 23:09:13.970259+00	250	Jesus	1	[{"added": {}}]	25	3
1912	2024-11-26 23:09:38.181359+00	496	Jesus - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1913	2024-11-26 23:10:14.790659+00	251	YamarisMedina	1	[{"added": {}}]	25	3
1914	2024-11-26 23:10:36.087387+00	497	YamarisMedina - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1915	2024-11-26 23:13:30.290505+00	1207	Transaction object (1207)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
1916	2024-11-26 23:14:39.784682+00	1208	Transaction object (1208)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1917	2024-11-26 23:15:17.566528+00	1209	Transaction object (1209)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1918	2024-11-26 23:18:33.978836+00	1210	Transaction object (1210)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
1919	2024-11-26 23:20:03.387296+00	498	RafaelGonzalez - Créditos - Pago a Crédito Personal: Credit:165, pending:165	1	[{"added": {}}]	28	3
1920	2024-11-26 23:21:06.284276+00	504	CristianAlexanderGonzales - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1921	2024-11-26 23:22:34.904549+00	505	AdanAbdielHigaldo - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1922	2024-11-26 23:59:25.481956+00	1219	Transaction object (1219)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 8"}}]	26	3
1923	2024-11-27 00:03:05.68297+00	1220	Transaction object (1220)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 480"}}]	26	3
1924	2024-11-27 00:03:39.467745+00	1221	Transaction object (1221)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1925	2024-11-27 00:05:11.804921+00	506	ErickMartinez - Créditos - Crédito Personal: Credit:5600, pending:5600	1	[{"added": {}}]	28	3
1926	2024-11-27 00:05:51.403752+00	252	InocenteRojas	1	[{"added": {}}]	25	3
1927	2024-11-27 00:06:10.385801+00	507	InocenteRojas - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
1928	2024-11-27 00:13:25.27114+00	509	MaximinoMartinez - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
1929	2024-11-27 00:14:12.478918+00	253	GregorioSoto	1	[{"added": {}}]	25	3
1930	2024-11-27 00:14:37.581135+00	510	GregorioSoto - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1931	2024-11-27 00:17:04.080807+00	1227	Transaction object (1227)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1932	2024-11-27 00:23:00.789083+00	511	ClementinaPerez - Créditos - Crédito Personal: Credit:400, pending:400	1	[{"added": {}}]	28	3
1933	2024-11-27 00:25:01.970787+00	254	RaulDominguez	1	[{"added": {}}]	25	3
1934	2024-11-27 00:25:25.790584+00	512	RaulDominguez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1935	2024-11-27 00:26:21.055373+00	255	RobertoAguilarRangel	1	[{"added": {}}]	25	3
1936	2024-11-27 00:26:38.593169+00	513	RobertoAguilarRangel - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
1938	2024-11-27 00:28:22.476113+00	126	Gastos de actividad - Otros - 250	1	[{"added": {}}]	27	3
1939	2024-11-27 00:28:46.170446+00	127	Gastos de actividad - Otros - 1000	1	[{"added": {}}]	27	3
1940	2024-11-27 00:29:01.687508+00	128	Gastos de actividad - Otros - 338	1	[{"added": {}}]	27	3
1941	2024-11-27 00:29:17.177881+00	129	Gastos de actividad - Viatico - 7.5	1	[{"added": {}}]	27	3
1942	2024-11-27 00:29:58.868828+00	35	Bomba Delta	1	[{"added": {}}]	18	3
1943	2024-11-27 00:30:04.075554+00	237	GeronimoPerez	2	[{"changed": {"fields": ["Label"]}}]	25	3
1944	2024-11-27 00:30:18.673566+00	250	Jesus	2	[{"changed": {"fields": ["Label"]}}]	25	3
1945	2024-11-27 00:49:52.292857+00	514	PublioProfe - Créditos - Crédito Personal: Credit:1050, pending:1050	1	[{"added": {}}]	28	3
1946	2024-11-27 00:50:31.864951+00	515	ArianaItzel - Créditos - Crédito Personal: Credit:180, pending:180	1	[{"added": {}}]	28	3
1947	2024-11-27 00:51:32.275195+00	487	ArmandoDicarena - Créditos - Crédito Personal: Credit:180, pending:80.00	2	[{"changed": {"fields": ["Cost", "Price", "Description", "Created at"]}}]	28	3
1948	2024-11-27 00:56:51.572038+00	1233	Transaction object (1233)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1949	2024-11-27 00:57:31.582635+00	1234	Transaction object (1234)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1950	2024-11-27 00:58:02.491656+00	1235	Transaction object (1235)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1951	2024-11-27 00:58:56.476218+00	1236	Transaction object (1236)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
1952	2024-11-27 00:59:41.681971+00	1237	Transaction object (1237)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1953	2024-11-27 01:00:25.1918+00	130	Gastos de actividad - Otros - 375	1	[{"added": {}}]	27	3
1954	2024-11-27 01:00:42.696348+00	131	Gastos de actividad - Otros - 20	1	[{"added": {}}]	27	3
1955	2024-11-27 01:01:00.779823+00	132	Gastos de actividad - Viatico - 8.70	1	[{"added": {}}]	27	3
1956	2024-11-27 01:01:33.175193+00	133	Gastos de actividad - Viatico - 12.5	1	[{"added": {}}]	27	3
1957	2024-11-27 01:10:32.868289+00	1238	Transaction object (1238)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1958	2024-11-27 01:12:20.289418+00	1239	Transaction object (1239)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 6"}}]	26	3
1959	2024-11-27 01:14:10.965717+00	256	JoseAgrazal	1	[{"added": {}}]	25	3
1960	2024-11-27 01:14:34.200494+00	516	JoseAgrazal - Créditos - Crédito Personal: Credit:60, pending:60	1	[{"added": {}}]	28	3
1961	2024-11-27 01:15:35.666146+00	257	LuisAlbertoMora	1	[{"added": {}}]	25	3
1962	2024-11-27 01:16:03.883171+00	517	LuisAlbertoMora - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
1963	2024-11-27 01:17:39.275195+00	518	Ubaldo - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
1964	2024-11-27 01:18:11.084595+00	519	MagalyMaxwell - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1965	2024-11-27 01:19:03.967513+00	523	PascualaMartinez - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
1966	2024-11-27 01:19:48.582119+00	1248	Transaction object (1248)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
1967	2024-11-27 01:20:23.586818+00	1249	Transaction object (1249)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1968	2024-11-27 01:20:49.397595+00	1250	Transaction object (1250)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1969	2024-11-27 01:21:17.880743+00	1251	Transaction object (1251)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1970	2024-11-27 01:22:23.197455+00	1252	Transaction object (1252)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1971	2024-11-27 01:22:46.380048+00	1253	Transaction object (1253)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1972	2024-11-27 21:28:14.47838+00	524	MariaTuñon - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
1973	2024-11-27 21:28:43.466998+00	258	LeoColon	1	[{"added": {}}]	25	3
1974	2024-11-27 21:29:05.900155+00	525	LeoColon - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1975	2024-11-27 21:29:52.782002+00	1256	Transaction object (1256)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 52"}}]	26	3
1976	2024-11-27 21:30:21.069574+00	1257	Transaction object (1257)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1977	2024-11-27 21:30:46.390836+00	1258	Transaction object (1258)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1978	2024-11-27 21:31:15.685624+00	1259	Transaction object (1259)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1979	2024-11-27 21:31:38.976961+00	1260	Transaction object (1260)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1980	2024-11-27 21:32:04.995063+00	1261	Transaction object (1261)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
1981	2024-11-27 21:32:57.175232+00	1262	Transaction object (1262)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1982	2024-11-27 21:34:24.803614+00	134	Gastos de actividad - Viatico - 20	1	[{"added": {}}]	27	3
1983	2024-11-27 21:34:40.577317+00	135	Gastos de actividad - Otros - 10	1	[{"added": {}}]	27	3
1984	2024-11-27 21:34:56.07935+00	136	Gastos de actividad - Otros - 10	1	[{"added": {}}]	27	3
1985	2024-11-27 21:37:37.184444+00	526	LuisAlbertoMora - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
1986	2024-11-27 21:38:23.715374+00	1264	Transaction object (1264)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1987	2024-11-27 21:38:48.390616+00	1265	Transaction object (1265)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1988	2024-11-27 21:42:10.571903+00	1266	Transaction object (1266)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
1989	2024-11-27 21:42:48.684063+00	1267	Transaction object (1267)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
1990	2024-11-27 21:44:20.994269+00	527	JorgeCordoba - Créditos - Crédito Personal: Credit:135, pending:135	1	[{"added": {}}]	28	3
1991	2024-11-27 21:45:17.583562+00	528	Lazaro - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
1992	2024-11-27 21:46:39.385668+00	1270	Transaction object (1270)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
1993	2024-11-27 21:55:39.898977+00	1271	Transaction object (1271)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1994	2024-11-27 21:56:02.40468+00	1272	Transaction object (1272)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
1995	2024-11-27 21:56:37.375391+00	1273	Transaction object (1273)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
1996	2024-11-27 22:05:23.892985+00	1274	Transaction object (1274)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
1997	2024-11-27 22:06:43.267882+00	1275	Transaction object (1275)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 6"}}]	26	3
1998	2024-11-27 22:08:53.49176+00	529	ElianysMora - Créditos - Crédito Personal: Credit:500, pending:500	1	[{"added": {}}]	28	3
1999	2024-11-27 22:09:38.386288+00	530	LicethChavez - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2000	2024-11-27 22:10:28.268745+00	259	FatimaHerrera	1	[{"added": {}}]	25	3
2001	2024-11-27 22:11:06.495719+00	531	FatimaHerrera - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2002	2024-11-27 22:12:44.487691+00	260	YarelisArrocha	1	[{"added": {}}]	25	3
2003	2024-11-27 22:13:14.999824+00	532	YarelisArrocha - Créditos - Crédito Personal: Credit:25, pending:25	1	[{"added": {}}]	28	3
2004	2024-11-27 22:13:57.87014+00	261	MarlinMora	1	[{"added": {}}]	25	3
2005	2024-11-27 22:14:18.187508+00	533	MarlinMora - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2006	2024-11-27 22:16:13.286991+00	262	IrinaHernandez	1	[{"added": {}}]	25	3
2007	2024-11-27 22:16:32.566815+00	534	IrinaHernandez - Créditos - Crédito Personal: Credit:60, pending:60	1	[{"added": {}}]	28	3
2008	2024-11-27 22:20:36.891026+00	263	JoaquinMelgar	1	[{"added": {}}]	25	3
2009	2024-11-27 22:21:09.492992+00	535	JoaquinMelgar - Créditos - Crédito Personal: Credit:60, pending:60	1	[{"added": {}}]	28	3
2010	2024-11-27 22:22:03.700275+00	540	ANYSANADELKAGONZALEZ - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2011	2024-11-27 22:22:55.867772+00	137	Gastos de actividad - Viatico - 5.5	1	[{"added": {}}]	27	3
2012	2024-11-27 22:23:15.069886+00	138	Gastos de actividad - Viatico - 13.50	1	[{"added": {}}]	27	3
2013	2024-12-02 23:57:40.093418+00	541	EdgardoMurillo - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2014	2024-12-02 23:58:10.593479+00	542	RogerMoreno - Créditos - Crédito Personal: Credit:100, pending:100	1	[{"added": {}}]	28	3
2015	2024-12-03 00:16:01.089398+00	1290	Transaction object (1290)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
2016	2024-12-03 00:17:04.898936+00	1291	Transaction object (1291)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2017	2024-12-03 00:17:47.214819+00	1292	Transaction object (1292)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2018	2024-12-03 00:18:12.182425+00	1293	Transaction object (1293)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2019	2024-12-03 00:18:38.089162+00	1294	Transaction object (1294)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2020	2024-12-03 00:20:36.680819+00	264	BolivarMedina	1	[{"added": {}}]	25	3
2021	2024-12-03 00:21:55.683042+00	543	BolivarMedina - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
2022	2024-12-03 00:25:58.286578+00	1296	Transaction object (1296)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2023	2024-12-03 00:26:35.677147+00	1297	Transaction object (1297)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2024	2024-12-03 00:27:28.487601+00	1298	Transaction object (1298)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2025	2024-12-03 00:30:33.705112+00	1299	Transaction object (1299)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
2026	2024-12-03 00:31:43.28279+00	1300	Transaction object (1300)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
2027	2024-12-03 00:32:21.684206+00	1301	Transaction object (1301)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 130"}}]	26	3
2028	2024-12-03 00:36:27.887694+00	544	MiguelOrdoñez - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
2029	2024-12-03 00:37:01.475352+00	545	MiguelOrdoñez - Créditos - Crédito Personal: Credit:75, pending:75	1	[{"added": {}}]	28	3
2030	2024-12-03 00:41:26.07797+00	547	MiguelOrdoñez - Créditos - Crédito Personal: Credit:230, pending:230	1	[{"added": {}}]	28	3
2031	2024-12-03 00:42:36.370426+00	1306	Transaction object (1306)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
2032	2024-12-03 00:43:18.947264+00	139	Gastos de actividad - Otros - 1000	1	[{"added": {}}]	27	3
2033	2024-12-03 00:43:35.572443+00	140	Gastos de actividad - Otros - 200	1	[{"added": {}}]	27	3
2034	2024-12-03 00:43:53.466722+00	141	Gastos de actividad - Otros - 120	1	[{"added": {}}]	27	3
2035	2024-12-03 00:48:09.390981+00	1307	Transaction object (1307)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2036	2024-12-03 00:48:41.397489+00	142	Gastos de actividad - Otros - 270	1	[{"added": {}}]	27	3
2037	2024-12-03 00:49:31.872783+00	1308	Transaction object (1308)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2038	2024-12-03 00:49:59.384291+00	1309	Transaction object (1309)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2039	2024-12-03 00:50:36.791663+00	1310	Transaction object (1310)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2040	2024-12-03 00:51:15.278373+00	1311	Transaction object (1311)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
2041	2024-12-03 00:53:05.172399+00	1312	Transaction object (1312)	1	[{"added": {}}]	26	3
2042	2024-12-03 00:53:52.267933+00	1312	Transaction object (1312)	2	[{"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 380"}}]	26	3
2043	2024-12-03 00:54:33.378681+00	1313	Transaction object (1313)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 6"}}]	26	3
2044	2024-12-03 00:55:17.793654+00	1314	Transaction object (1314)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
2045	2024-12-03 00:56:27.482136+00	1315	Transaction object (1315)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2046	2024-12-03 00:56:58.971468+00	1316	Transaction object (1316)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2047	2024-12-03 00:57:43.594162+00	1317	Transaction object (1317)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
2048	2024-12-03 00:58:18.887483+00	1318	Transaction object (1318)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 290"}}]	26	3
2049	2024-12-03 00:59:44.466324+00	143	Gastos de actividad - Viatico - 5.5	1	[{"added": {}}]	27	3
2050	2024-12-03 01:00:23.674889+00	265	JaimeTrejos	1	[{"added": {}}]	25	3
2051	2024-12-03 01:01:05.494713+00	548	JaimeTrejos - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2052	2024-12-04 21:29:29.575768+00	1320	Transaction object (1320)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2053	2024-12-04 21:30:25.894258+00	549	JavierEscobarMecanico - Créditos - Crédito Personal: Credit:250, pending:250	1	[{"added": {}}]	28	3
2054	2024-12-04 21:31:00.891367+00	553	JoseLuisFernandez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
2055	2024-12-04 21:32:44.689662+00	1326	Transaction object (1326)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
2056	2024-12-04 21:33:14.891256+00	1327	Transaction object (1327)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
2057	2024-12-04 21:34:26.284048+00	1328	Transaction object (1328)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2058	2024-12-04 21:39:49.56806+00	1329	Transaction object (1329)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2059	2024-12-04 21:40:17.983206+00	1330	Transaction object (1330)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2060	2024-12-04 21:41:29.373924+00	1331	Transaction object (1331)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 65"}}]	26	3
2061	2024-12-04 21:42:22.190438+00	1332	Transaction object (1332)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
2062	2024-12-04 21:45:06.168489+00	144	Gastos de actividad - Gasolina - 30.80	1	[{"added": {}}]	27	3
2063	2024-12-04 21:45:21.371567+00	145	Gastos de actividad - Otros - 5.50	1	[{"added": {}}]	27	3
2064	2024-12-04 21:48:07.093911+00	1333	Transaction object (1333)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
2065	2024-12-04 21:49:04.689629+00	554	MaximinoMartinez - Créditos - Crédito Personal: Credit:80, pending:80	1	[{"added": {}}]	28	3
2066	2024-12-04 21:54:39.589192+00	1335	Transaction object (1335)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 140"}}]	26	3
2067	2024-12-04 21:55:08.980478+00	1336	Transaction object (1336)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
2068	2024-12-04 21:55:46.789618+00	1337	Transaction object (1337)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 167"}}]	26	3
2069	2024-12-04 21:56:15.36833+00	1338	Transaction object (1338)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
2070	2024-12-04 21:56:49.397521+00	1339	Transaction object (1339)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
2071	2024-12-04 21:57:27.490684+00	1340	Transaction object (1340)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
2072	2024-12-04 21:58:03.793629+00	1341	Transaction object (1341)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
2073	2024-12-04 22:00:58.671133+00	555	MagalyMaxwell - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2074	2024-12-04 22:01:27.19243+00	556	YolandaArosemena - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2075	2024-12-04 22:03:28.778543+00	1344	Transaction object (1344)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
2076	2024-12-04 22:04:09.689203+00	1345	Transaction object (1345)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2077	2024-12-04 22:08:37.189665+00	557	FranciscoMendoza - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
2078	2024-12-04 22:10:21.871953+00	558	JaiberBusito - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2079	2024-12-04 22:12:35.989037+00	1348	Transaction object (1348)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
2080	2024-12-04 22:13:27.471523+00	1349	Transaction object (1349)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2081	2024-12-04 22:14:44.288626+00	1350	Transaction object (1350)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2082	2024-12-04 22:35:12.186798+00	1351	Transaction object (1351)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 93"}}]	26	3
2083	2024-12-04 22:35:49.465569+00	1352	Transaction object (1352)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
2084	2024-12-04 22:40:15.892702+00	266	OmarBaneso	1	[{"added": {}}]	25	3
2085	2024-12-04 22:40:47.003774+00	559	OmarBaneso - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
2086	2024-12-04 22:41:37.976174+00	560	JhoannaRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2087	2024-12-04 22:42:05.082739+00	561	NoelRodriguez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2088	2024-12-04 22:44:58.693497+00	1356	Transaction object (1356)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
2089	2024-12-04 22:45:35.581129+00	1357	Transaction object (1357)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2090	2024-12-04 22:46:03.479153+00	1358	Transaction object (1358)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 180"}}]	26	3
2091	2024-12-04 22:49:18.671372+00	1359	Transaction object (1359)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2092	2024-12-04 22:49:44.785208+00	1360	Transaction object (1360)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2093	2024-12-04 22:50:42.188548+00	1361	Transaction object (1361)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
2094	2024-12-04 22:51:14.587935+00	1362	Transaction object (1362)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 6"}}]	26	3
2095	2024-12-04 22:52:25.99365+00	562	EfrainMora - Créditos - Crédito Personal: Credit:35, pending:35	1	[{"added": {}}]	28	3
2096	2024-12-04 22:53:06.992708+00	563	Lazaro - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
2097	2024-12-04 22:54:33.574241+00	1365	Transaction object (1365)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2098	2024-12-04 23:03:44.587646+00	1366	Transaction object (1366)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2099	2024-12-04 23:05:30.271324+00	1367	Transaction object (1367)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2100	2024-12-04 23:05:56.401889+00	1368	Transaction object (1368)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2101	2024-12-04 23:06:49.577826+00	146	Gastos de actividad - Otros - 15	1	[{"added": {}}]	27	3
2102	2024-12-04 23:07:12.181359+00	147	Gastos de actividad - Otros - 13.50	1	[{"added": {}}]	27	3
2103	2024-12-04 23:07:25.981832+00	148	Gastos de actividad - Otros - 14	1	[{"added": {}}]	27	3
2104	2024-12-05 23:15:40.28098+00	564	EdgardoMurillo - Créditos - Crédito Personal: Credit:2600, pending:2600	1	[{"added": {}}]	28	3
2105	2024-12-05 23:16:46.082065+00	1370	Transaction object (1370)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2106	2024-12-05 23:17:24.992293+00	1371	Transaction object (1371)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2107	2024-12-05 23:18:03.585698+00	1372	Transaction object (1372)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2108	2024-12-05 23:18:29.707621+00	1373	Transaction object (1373)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2109	2024-12-05 23:19:03.087724+00	1374	Transaction object (1374)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2110	2024-12-05 23:19:36.488413+00	1375	Transaction object (1375)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2111	2024-12-05 23:20:04.991075+00	1376	Transaction object (1376)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2112	2024-12-05 23:20:45.614652+00	1377	Transaction object (1377)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
2113	2024-12-05 23:21:29.473957+00	1378	Transaction object (1378)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 45"}}]	26	3
2114	2024-12-05 23:22:40.264666+00	1379	Transaction object (1379)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2115	2024-12-05 23:23:23.810374+00	1380	Transaction object (1380)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 10"}}]	26	3
2116	2024-12-05 23:24:08.388531+00	1381	Transaction object (1381)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2117	2024-12-05 23:25:02.867524+00	565	ReinaldoVasquez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
2118	2024-12-05 23:26:01.181428+00	573	GeidyDominguez - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
2119	2024-12-05 23:27:23.28371+00	267	SadiaNavarro	1	[{"added": {}}]	25	3
2120	2024-12-05 23:27:45.682368+00	574	SadiaNavarro - Créditos - Crédito Personal: Credit:800, pending:800	1	[{"added": {}}]	28	3
2121	2024-12-05 23:29:21.384212+00	1392	Transaction object (1392)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2122	2024-12-05 23:31:22.399857+00	1393	Transaction object (1393)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 125"}}]	26	3
2123	2024-12-05 23:31:55.893363+00	1394	Transaction object (1394)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2124	2024-12-05 23:32:17.588604+00	1395	Transaction object (1395)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2125	2024-12-05 23:33:17.387574+00	1396	Transaction object (1396)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2126	2024-12-05 23:34:05.276846+00	1397	Transaction object (1397)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 125"}}]	26	3
2127	2024-12-05 23:34:46.971396+00	149	Gastos de actividad - Otros - 200	1	[{"added": {}}]	27	3
2128	2024-12-05 23:36:26.092209+00	1398	Transaction object (1398)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 55"}}]	26	3
2129	2024-12-05 23:37:03.089137+00	575	ArielHernandez - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
2130	2024-12-05 23:37:51.573971+00	268	MariaDelosReyes	1	[{"added": {}}]	25	3
2131	2024-12-05 23:38:05.797863+00	576	MariaDelosReyes - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2132	2024-12-05 23:39:19.590366+00	1401	Transaction object (1401)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2133	2024-12-05 23:40:11.88999+00	1402	Transaction object (1402)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2134	2024-12-05 23:40:43.184397+00	1403	Transaction object (1403)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2135	2024-12-05 23:41:11.506481+00	1404	Transaction object (1404)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
2136	2024-12-05 23:56:04.979372+00	1405	Transaction object (1405)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2137	2024-12-05 23:57:02.786969+00	1406	Transaction object (1406)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2138	2024-12-05 23:58:12.770903+00	1407	Transaction object (1407)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2139	2024-12-05 23:58:45.89046+00	1408	Transaction object (1408)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 340"}}]	26	3
2140	2024-12-06 00:15:00.993526+00	577	BiancaCoronado - Créditos - Crédito Personal: Credit:240, pending:240	1	[{"added": {}}]	28	3
2141	2024-12-06 00:20:58.977126+00	1410	Transaction object (1410)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2142	2024-12-06 00:21:32.987708+00	1411	Transaction object (1411)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 20"}}]	26	3
2143	2024-12-06 00:22:04.281895+00	1412	Transaction object (1412)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2144	2024-12-06 00:22:57.497785+00	1413	Transaction object (1413)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 53"}}]	26	3
2145	2024-12-06 00:23:42.498228+00	1414	Transaction object (1414)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2146	2024-12-06 00:24:31.377119+00	1415	Transaction object (1415)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 6"}}]	26	3
2147	2024-12-06 00:25:08.09853+00	1416	Transaction object (1416)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 60"}}]	26	3
2148	2024-12-06 00:26:03.17831+00	578	JorgeReyes - Créditos - Crédito Personal: Credit:360, pending:360	1	[{"added": {}}]	28	3
2149	2024-12-06 00:27:01.586505+00	584	enriquefritos - Créditos - Crédito Personal: Credit:130, pending:130	1	[{"added": {}}]	28	3
2150	2024-12-06 00:27:31.067299+00	150	Gastos de actividad - Otros - 2000	1	[{"added": {}}]	27	3
2151	2024-12-06 00:27:45.369553+00	151	Gastos de actividad - Otros - 125	1	[{"added": {}}]	27	3
2152	2024-12-06 00:28:00.273273+00	152	Gastos de actividad - Otros - 25	1	[{"added": {}}]	27	3
2153	2024-12-06 00:28:22.674761+00	153	Gastos de actividad - Viatico - 29	1	[{"added": {}}]	27	3
2154	2024-12-06 00:39:13.070744+00	585	LucianoMendoza - Créditos - Crédito de Consumo: Credit:280, pending:280	1	[{"added": {}}]	28	3
2155	2024-12-06 00:40:02.198225+00	589	LucianoMendoza - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
2156	2024-12-06 00:41:01.89799+00	604	LucianoMendoza - Créditos - Crédito Personal: Credit:160, pending:160	1	[{"added": {}}]	28	3
2157	2024-12-06 00:41:56.189462+00	1446	Transaction object (1446)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2158	2024-12-06 00:42:51.522664+00	607	PabloZyZ - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
2159	2024-12-06 00:43:33.094711+00	608	MagalyMaxwell - Créditos - Crédito Personal: Credit:70, pending:70	1	[{"added": {}}]	28	3
2160	2024-12-06 00:44:12.57117+00	609	LeydiamSilveraPanaderia - Créditos - Crédito Personal: Credit:510, pending:510	1	[{"added": {}}]	28	3
2161	2024-12-06 00:45:00.997715+00	610	AlvaroGonzalezGomez - Créditos - Crédito Personal: Credit:1000, pending:1000	1	[{"added": {}}]	28	3
2162	2024-12-06 00:45:46.798945+00	1451	Transaction object (1451)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 90"}}]	26	3
2163	2024-12-06 00:46:28.170767+00	1452	Transaction object (1452)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 120"}}]	26	3
2164	2024-12-06 00:46:59.572112+00	1453	Transaction object (1453)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 80"}}]	26	3
2165	2024-12-06 00:47:30.838062+00	1454	Transaction object (1454)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 75"}}]	26	3
2166	2024-12-06 00:48:53.274028+00	1455	Transaction object (1455)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 54"}}]	26	3
2167	2024-12-06 00:49:24.394555+00	1456	Transaction object (1456)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2168	2024-12-06 00:49:51.868235+00	1457	Transaction object (1457)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2169	2024-12-06 00:50:34.782019+00	154	Gastos de actividad - Gasolina - 31	1	[{"added": {}}]	27	3
2170	2024-12-06 00:52:09.476638+00	1458	Transaction object (1458)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2171	2024-12-06 00:53:49.387319+00	1459	Transaction object (1459)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 5"}}]	26	3
2172	2024-12-06 00:54:23.675994+00	1460	Transaction object (1460)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 100"}}]	26	3
2173	2024-12-06 00:54:50.089846+00	1461	Transaction object (1461)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 145"}}]	26	3
2174	2024-12-06 00:56:05.185136+00	1462	Transaction object (1462)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 70"}}]	26	3
2175	2024-12-06 00:56:44.984941+00	1463	Transaction object (1463)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 50"}}]	26	3
2176	2024-12-06 00:57:14.891501+00	1464	Transaction object (1464)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 30"}}]	26	3
2177	2024-12-06 00:57:50.282066+00	1465	Transaction object (1465)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 160"}}]	26	3
2178	2024-12-06 00:58:14.579918+00	1466	Transaction object (1466)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2179	2024-12-06 00:59:09.480869+00	269	BombaDelta	1	[{"added": {}}]	25	3
2180	2024-12-06 00:59:24.486509+00	611	BombaDelta - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2181	2024-12-06 01:00:06.069555+00	615	MorrisProfesor - Créditos - Crédito Personal: Credit:60, pending:60	1	[{"added": {}}]	28	3
2182	2024-12-06 01:01:06.282951+00	620	ZoilaOrtega - Créditos - Crédito Personal: Credit:90, pending:90	1	[{"added": {}}]	28	3
2183	2024-12-06 01:03:10.786171+00	621	AlbertoArocemena - Créditos - Crédito Personal: Credit:50, pending:50	1	[{"added": {}}]	28	3
2184	2024-12-06 01:04:58.980757+00	270	JavierGonzales	1	[{"added": {}}]	25	3
2185	2024-12-06 01:05:15.274513+00	622	JavierGonzales - Créditos - Crédito Personal: Credit:150, pending:150	1	[{"added": {}}]	28	3
2186	2024-12-06 01:06:03.792447+00	625	DarioDominguez - Créditos - Crédito Personal: Credit:152, pending:152	1	[{"added": {}}]	28	3
2187	2024-12-06 01:07:17.988068+00	626	JorgeCamel - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2188	2024-12-06 01:08:11.235437+00	1483	Transaction object (1483)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 35"}}]	26	3
2189	2024-12-06 01:09:00.273528+00	1484	Transaction object (1484)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85"}}]	26	3
2190	2024-12-06 01:09:27.101931+00	1484	Transaction object (1484)	2	[{"changed": {"fields": ["User"]}}, {"changed": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 85.00", "fields": ["Credit"]}}]	26	3
2191	2024-12-06 01:09:54.283501+00	1485	Transaction object (1485)	1	[{"added": {}}, {"added": {"name": "account method amount", "object": "Payment method Efectivo - Amount Paid: 40"}}]	26	3
2192	2024-12-06 01:11:05.082596+00	271	ElizabertMartinez	1	[{"added": {}}]	25	3
2193	2024-12-06 01:11:31.679129+00	627	ElizabertMartinez - Créditos - Crédito Personal: Credit:140, pending:140	1	[{"added": {}}]	28	3
2194	2024-12-06 01:12:11.07738+00	272	AntonioCamargo	1	[{"added": {}}]	25	3
2195	2024-12-06 01:12:30.782998+00	628	AntonioCamargo - Créditos - Crédito Personal: Credit:120, pending:120	1	[{"added": {}}]	28	3
2196	2024-12-06 01:13:08.869892+00	629	OmairaCuava - Créditos - Crédito Personal: Credit:510, pending:510	1	[{"added": {}}]	28	3
2197	2024-12-06 01:13:46.38407+00	155	Gastos de actividad - Viatico - 11.60	1	[{"added": {}}]	27	3
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."django_content_type" ("id", "app_label", "model") FROM stdin;
1	authtoken	token
2	authtoken	tokenproxy
3	token_blacklist	blacklistedtoken
4	token_blacklist	outstandingtoken
5	admin	logentry
6	auth	permission
7	auth	group
8	auth	user
9	contenttypes	contenttype
10	sessions	session
11	fintech	account
12	fintech	category
13	fintech	categorytype
14	fintech	country
15	fintech	currency
16	fintech	documenttype
17	fintech	identifier
18	fintech	label
19	fintech	language
20	fintech	paramslocation
21	fintech	periodicity
22	fintech	phonenumber
23	fintech	role
24	fintech	subcategory
25	fintech	user
26	fintech	transaction
27	fintech	expense
28	fintech	credit
29	fintech	address
30	fintech	accountmethodamount
31	fintech	seller
32	oauth2_provider	application
33	oauth2_provider	accesstoken
34	oauth2_provider	grant
35	oauth2_provider	refreshtoken
36	oauth2_provider	idtoken
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."django_migrations" ("id", "app", "name", "applied") FROM stdin;
1	contenttypes	0001_initial	2024-09-11 01:46:00.936859+00
2	auth	0001_initial	2024-09-11 01:46:01.213588+00
3	admin	0001_initial	2024-09-11 01:46:01.24287+00
4	admin	0002_logentry_remove_auto_add	2024-09-11 01:46:01.25159+00
5	admin	0003_logentry_add_action_flag_choices	2024-09-11 01:46:01.311044+00
6	contenttypes	0002_remove_content_type_name	2024-09-11 01:46:01.336231+00
7	auth	0002_alter_permission_name_max_length	2024-09-11 01:46:01.347558+00
8	auth	0003_alter_user_email_max_length	2024-09-11 01:46:01.359499+00
9	auth	0004_alter_user_username_opts	2024-09-11 01:46:01.369421+00
10	auth	0005_alter_user_last_login_null	2024-09-11 01:46:01.381895+00
11	auth	0006_require_contenttypes_0002	2024-09-11 01:46:01.386246+00
12	auth	0007_alter_validators_add_error_messages	2024-09-11 01:46:01.395531+00
13	auth	0008_alter_user_username_max_length	2024-09-11 01:46:01.410956+00
14	auth	0009_alter_user_last_name_max_length	2024-09-11 01:46:01.421982+00
15	auth	0010_alter_group_name_max_length	2024-09-11 01:46:01.435896+00
16	auth	0011_update_proxy_permissions	2024-09-11 01:46:01.44857+00
17	auth	0012_alter_user_first_name_max_length	2024-09-11 01:46:01.461965+00
18	authtoken	0001_initial	2024-09-11 01:46:01.51489+00
19	authtoken	0002_auto_20160226_1747	2024-09-11 01:46:01.539237+00
20	authtoken	0003_tokenproxy	2024-09-11 01:46:01.550788+00
21	fintech	0001_initial	2024-09-11 01:46:02.408532+00
22	fintech	0002_remove_role_group_alter_credit_created_at_and_more	2024-09-11 01:46:02.525167+00
23	sessions	0001_initial	2024-09-11 01:46:02.560061+00
24	token_blacklist	0001_initial	2024-09-11 01:46:02.631081+00
25	token_blacklist	0002_outstandingtoken_jti_hex	2024-09-11 01:46:02.647022+00
26	token_blacklist	0003_auto_20171017_2007	2024-09-11 01:46:02.67771+00
27	token_blacklist	0004_auto_20171017_2013	2024-09-11 01:46:02.706361+00
28	token_blacklist	0005_remove_outstandingtoken_jti	2024-09-11 01:46:02.723577+00
29	token_blacklist	0006_auto_20171017_2113	2024-09-11 01:46:02.741174+00
30	token_blacklist	0007_auto_20171017_2214	2024-09-11 01:46:02.838425+00
31	token_blacklist	0008_migrate_to_bigautofield	2024-09-11 01:46:02.990085+00
32	token_blacklist	0010_fix_migrate_to_bigautofield	2024-09-11 01:46:03.026029+00
33	token_blacklist	0011_linearizes_history	2024-09-11 01:46:03.034392+00
34	token_blacklist	0012_alter_outstandingtoken_user	2024-09-11 01:46:03.057228+00
35	fintech	0003_alter_expense_category	2024-09-11 04:20:28.7631+00
36	fintech	0004_rename_category_expense_subcategory	2024-09-11 04:45:33.156218+00
37	fintech	0005_auto_20240911_2039	2024-09-12 01:42:11.951784+00
38	fintech	0006_expense_user	2024-09-12 02:20:33.168282+00
39	oauth2_provider	0001_initial	2024-09-20 01:52:48.919976+00
40	oauth2_provider	0002_auto_20190406_1805	2024-09-20 01:52:48.949554+00
41	oauth2_provider	0003_auto_20201211_1314	2024-09-20 01:52:48.965048+00
42	oauth2_provider	0004_auto_20200902_2022	2024-09-20 01:52:49.088161+00
43	oauth2_provider	0005_auto_20211222_2352	2024-09-20 01:52:49.181221+00
44	oauth2_provider	0006_alter_application_client_secret	2024-09-20 01:52:49.213389+00
45	oauth2_provider	0007_application_post_logout_redirect_uris	2024-09-20 01:52:49.233043+00
46	oauth2_provider	0008_alter_accesstoken_token	2024-09-20 01:52:49.30107+00
47	oauth2_provider	0009_add_hash_client_secret	2024-09-20 01:52:49.31964+00
48	oauth2_provider	0010_application_allowed_origins	2024-09-20 01:52:49.341293+00
49	oauth2_provider	0011_refreshtoken_token_family	2024-09-20 01:52:49.358607+00
50	oauth2_provider	0012_add_token_checksum	2024-09-20 01:52:49.434063+00
51	fintech	0007_expense_created_at_expense_updated_at	2024-09-21 05:06:29.833062+00
52	fintech	0008_alter_expense_user	2024-09-27 17:13:20.008842+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."django_session" ("session_key", "session_data", "expire_date") FROM stdin;
w49vtpworlax5tosfqdxvk851tt982lh	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1soCTf:Mkm5r9fsrlH3Opt37YZFCElGxWBIKP-0lA0iPEezJ04	2024-09-25 01:49:03.886298+00
c6owrjsrubyfc5kbzh20zalwyzrqh7if	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1soRkG:1AklccrpWttPJ1oQN5cLPW_CRcmwAPhVZk295Zeb_T0	2024-09-25 18:07:12.394818+00
x16fecam2huzkubfutkmw7up6whkru47	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1soRkq:9O4oGqENriz2okGlMxol4nZpjVfN8lNJ1OQjv-jRMGI	2024-09-25 18:07:48.800429+00
oqy6ur8rsd9vznqbtp70oyyd3hau6e9z	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1sowBk:rbHuv8RWvlfsujOdGdRlUj0DNSHoHDculpNNE17_n64	2024-09-27 02:37:36.522284+00
rsyybw9a0lamve3vipbvdsbwp2umt0xa	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1stWek:enbNvPn0GmyZlzfCetXWlsaf5dHoUOmfd1K7o_Vnfxg	2024-10-09 18:22:30.23832+00
u9js51s93yb08ybie6kn3wmgi7mugp4j	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1stbHZ:Ja8jNT2CvGAxAsxqm0bBRmdwO0uibTFrHPTs-KjUwsw	2024-10-09 23:18:53.759788+00
9nxv2mz4l15rj4lyepdbnm5oworo9drj	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1suEi4:V_1Y0yWUZaS1WrC1EXmVGzv_472Z-9Aha9WsP_VVGxk	2024-10-11 17:24:52.870977+00
id5w79zh3ncnh0zqo1j2orsb4mvn6led	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1suZ6s:SDLRcXEx8T-34fCFo6lT9FCLl7OmaXKZj1Ix9kUmAO4	2024-10-12 15:11:50.653238+00
2bkcv4ivubt5efz1aerb8x3jfjhu9nby	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1syfxe:p3ZAW-wmfilqQe5vdCoXvDRzxoTtSeaZpkPlpccUg8g	2024-10-23 23:19:18.76771+00
hhax7ch1b29ulhingmbh461yy2d1szez	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1syfxg:0vZiP5FmrI9cN2gtG6JZaQMY0XLglHYoCgyNq98fYAE	2024-10-23 23:19:20.663185+00
j7fnfwl45bxcmf2ybat95vvp7scyhw4a	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1t03Tw:yKjc3uJXzjsbnkuc5ymc6Zu2hS2dPkbE_p-1mZ6G8kI	2024-10-27 18:38:20.318671+00
zkweyyxyn94unkp8foxfvljrn6owvj1s	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1t1aPG:8fKXB9_ts4EfvajlplAmtiJKW4VZ7cyzb7n7fn4EkWg	2024-10-31 23:59:50.352685+00
eh9iruzgnke7i1f2ih8r7vh04487rurf	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1t3mJK:ePgaooCnrjBvSMuDYA5SmxmMGjSQNxw27i1dOGR7KGU	2024-11-07 01:06:46.973286+00
fpbwpvyrgsh6ptlk0z3muev22eyzyrtn	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1t6zEc:TGMUjKy2pnbPsmR30jUtnt6dJX2oq5R9A3ODtvO3ViU	2024-11-15 21:31:10.380501+00
etdqlurilu8c6epordeudngvs7fhyyax	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1t71H9:QaT1DAFlpt_Q6pBI2KQp6cUE-g5E1LKb11e1FWxfn6g	2024-11-15 23:41:55.590296+00
ekqj7gsd38vkj7dc4wk36tzgeo0383ep	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1t9xIh:2NbCjoAXjsWzJxD6Vr_VGC7ZkfDZ8KdrwwDzoY0pyPs	2024-11-24 02:03:39.812339+00
4q2yc6whhtoxo3eh2s5bfqe5xkyladit	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1tC5jh:bdEmVmrM9C4xsURDAt6cTkzwwwCacw9qNNAeOFBsPKw	2024-11-29 23:28:21.730008+00
azhwb8iyjtk7bhc6rtfpwu634kqyvfg6	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1tCJDE:Q6k6wGYIoId_iTv2PxWFaIe2MiU_ErEykE3kAmHOi9w	2024-11-30 13:51:44.451233+00
hkwce83go6r3tdpyhylj5ua08wmpekrv	.eJxVjEsOAiEQBe_C2hCg-bp07xkI3aCMGkiGmZXx7oZkFrp9VfXeLKZ9q3EfZY1LZmcm2el3w0TP0ibIj9TunVNv27ognwo_6ODXnsvrcrh_BzWNOussg0Ugo7MDQaiMBKeElYg-IZQU_I2cFh4MCaOkL6BdthqCllSMYJ8v0eA3Aw:1tFOCJ:QcrXgeE0H6rZhaxZCVx58NLtdhdJP8Hnx02pq8R_uYc	2024-12-09 01:47:31.040754+00
kzvgn6lum6znpd0k0a479xplzr5k9ony	.eJxVjMsOwiAQRf-FtSHAyMule7-BDDBI1UBS2pXx322TLnR7zzn3zQKuSw3roDlMmV0YsNPvFjE9qe0gP7DdO0-9LfMU-a7wgw5-65le18P9O6g46larhKgItHWgSyGQJseijRFe5CTRJKk9xgICkkLr5dlaLRwpsSkEwrHPF-TsNzY:1tIGHh:Lc1mlaSh1YEKaxuplrJBJ7nUYXA4ZScRa-gasMiElSo	2024-12-16 23:56:57.464958+00
\.


--
-- Data for Name: fintech_account; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_account" ("id_payment_method", "name", "account_number", "balance", "eletronic_software_id", "currency_id") FROM stdin;
1	Yappy	0928329	30000.00	\N	1
2	Banco General	09283223	30000.00	\N	1
3	Banesco	092832943	30000.00	\N	1
4	Efectivo	092830001	40000.00	\N	1
\.


--
-- Data for Name: fintech_accountmethodamount; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_accountmethodamount" ("id", "payment_code", "amount", "amount_paid", "credit_id", "currency_id", "payment_method_id", "transaction_id") FROM stdin;
1	280820241109	275.00	275.00	3	1	4	4
2	290820241615	275.00	275.00	3	1	4	7
3	010920241615	90.00	90.00	4	1	4	8
1207	CP261120241822	150.00	150.00	505	1	4	1218
1220	CP261120241949	1050.00	1050.00	514	1	4	1231
11	CP120920241038	1200.00	1200.00	16	1	4	23
12	050920241039	40.00	40.00	16	1	4	24
13	06092024	40.00	40.00	16	1	4	25
14	07092024	40.00	40.00	16	1	4	26
15	09092014	40.00	40.00	16	1	4	27
16	CP120920241855	300.00	300.00	17	1	4	28
17	CP120920241859	525.00	525.00	18	1	4	29
18	030820241900	80.00	80.00	17	1	4	30
19	160820241905	175.00	175.00	18	1	4	31
20	010920241905	100.00	100.00	18	1	4	32
21	CP120920241913	80.00	80.00	19	1	4	33
22	CP120920241915	300.00	300.00	20	1	4	34
23	150820241918	100.00	100.00	20	1	4	35
24	040920241918	50.00	50.00	20	1	4	36
25	CP120920241924	300.00	300.00	21	1	4	37
26	CP120920241925	510.00	510.00	22	1	4	38
27	150820241926	100.00	100.00	21	1	4	39
28	020920241926	25.00	25.00	22	1	4	40
29	CP120920241929	150.00	150.00	23	1	4	41
30	CP120920241932	510.00	510.00	24	1	4	42
31	150820242005	167.00	167.00	24	1	4	43
32	300820242005	167.00	167.00	24	1	4	44
33	CP120920242012	600.00	600.00	25	1	4	45
34	CP120920242014	165.00	165.00	26	1	4	46
35	100820242015	55.00	55.00	26	1	4	47
36	240820242016	55.00	55.00	26	1	4	48
37	CP120920242018	165.00	165.00	27	1	4	49
38	CP120920242022	140.00	140.00	28	1	4	50
39	CP130920241351	50.00	50.00	29	1	4	51
40	CP130920241352	100.00	100.00	30	1	4	52
41	CP130920241454	50.00	50.00	31	1	4	53
42	CP130920241607	50.00	50.00	32	1	4	54
43	CP130920241609	50.00	50.00	33	1	4	55
44	CP130920241610	50.00	50.00	34	1	4	56
45	CP130920241611	150.00	150.00	35	1	4	57
46	CP130920241616	70.00	70.00	36	1	4	58
47	CP130920241620	140.00	140.00	37	1	4	59
48	CP130920241621	140.00	140.00	38	1	4	60
49	CP130920241622	750.00	750.00	39	1	4	61
50	CP130920241625	90.00	90.00	40	1	4	62
51	CP130920241627	80.00	80.00	41	1	4	63
52	CP130920241628	140.00	140.00	42	1	4	64
53	CP130920241630	140.00	140.00	43	1	4	65
54	CP130920241743	200.00	200.00	44	1	4	66
55	CP130920241745	90.00	90.00	45	1	4	67
56	CP130920241748	140.00	140.00	46	1	4	68
57	CP130920241753	150.00	150.00	47	1	4	69
58	CP130920241755	80.00	80.00	48	1	4	70
59	CP130920241757	140.00	140.00	49	1	4	71
60	CP130920241758	65.00	65.00	50	1	4	72
61	CP130920241759	300.00	300.00	51	1	4	73
62	CP130920241806	150.00	150.00	52	1	4	74
63	CP130920241807	80.00	80.00	53	1	4	75
64	CP130920241809	130.00	130.00	54	1	4	76
65	CP130920241835	4200.00	4200.00	55	1	4	77
66	CP130920241839	360.00	360.00	56	1	4	78
67	150820241840	120.00	120.00	56	1	4	79
68	090920241843	375.00	375.00	39	1	4	80
70	CP130920241948	50.00	50.00	58	1	4	82
71	CP130920241957	100.00	100.00	59	1	4	83
72	CP130920242001	480.00	480.00	60	1	4	84
73	CP130920242002	150.00	150.00	61	1	4	85
74	CP130920242003	140.00	140.00	62	1	4	86
75	CP130920242018	260.00	260.00	63	1	4	87
76	CP130920242019	360.00	360.00	64	1	4	88
77	CP130920242021	600.00	600.00	65	1	4	89
78	CP130920242022	300.00	300.00	66	1	4	90
79	CP130920242023	165.00	165.00	67	1	4	91
80	CP130920242026	300.00	300.00	68	1	4	92
81	CP130920242027	80.00	80.00	69	1	4	93
83	CP130920242028	90.00	90.00	71	1	4	95
84	CP130920242029	255.00	255.00	72	1	4	96
85	CP130920242030	140.00	140.00	73	1	4	97
86	CP130920242032	165.00	165.00	74	1	4	98
87	CP130920242034	255.00	255.00	75	1	4	99
88	CP130920242035	300.00	300.00	76	1	4	100
89	CP130920242037	150.00	150.00	77	1	4	101
90	050920241245	40.00	40.00	16	1	4	102
91	060920241245	40.00	40.00	16	1	4	103
92	070920241249	40.00	40.00	16	1	4	104
93	090920241449	40.00	40.00	16	1	4	105
94	100920241250	40.00	40.00	16	1	4	106
95	CP140920241256	315.00	315.00	78	1	4	107
96	CP140920241300	345.00	345.00	79	1	4	108
97	CP140920241301	270.00	270.00	80	1	4	109
98	CP140920241314	150.00	150.00	81	1	4	110
99	240820241315	37.50	37.50	81	1	4	111
100	070920241316	37.50	37.50	81	1	4	112
101	080920241317	35.00	35.00	81	1	4	113
102	170820241355	37.50	37.50	81	1	4	114
103	CP140920241453	220.00	220.00	82	1	4	115
104	CP140920241458	630.00	630.00	83	1	4	116
105	020920241502	200.00	200.00	83	1	4	117
106	CP140920241503	600.00	600.00	84	1	4	118
107	CP140920241504	560.00	560.00	85	1	4	119
108	240820241612	50.00	50.00	84	1	4	120
109	080920241612	50.00	50.00	84	1	4	121
110	270820241613	140.00	140.00	85	1	4	122
111	CP140920241621	140.00	140.00	86	1	4	123
112	CP140920241625	380.00	380.00	87	1	4	124
113	CP140920241627	330.00	330.00	88	1	4	125
114	100920241634	20.00	20.00	86	1	4	126
115	240820241635	95.00	95.00	87	1	4	127
116	100920241636	95.00	95.00	87	1	4	128
117	270820241637	110.00	110.00	88	1	4	129
118	120920241638	110.00	110.00	88	1	4	130
1208	201120241858	8.00	8.00	269	1	4	1219
120	CP140920241700	330.00	330.00	89	1	4	132
121	020920241701	110.00	110.00	89	1	4	133
122	130920241702	110.00	110.00	89	1	4	134
123	CP140920241709	740.00	740.00	90	1	4	135
124	CP140920241750	300.00	300.00	91	1	4	136
125	CP140920241751	140.00	140.00	92	1	4	137
126	300820241752	70.00	70.00	92	1	4	138
127	CP140920241839	140.00	140.00	93	1	4	139
1221	CP261120241950	180.00	180.00	515	1	4	1232
129	CP140920241845	140.00	140.00	95	1	4	141
132	CP140920241846	5600.00	5600.00	98	1	4	144
137	CP140920241847	270.00	270.00	103	1	4	149
138	CP140920241849	375.00	375.00	104	1	4	150
139	CP140920241850	130.00	130.00	105	1	4	151
140	CP140920241851	500.00	500.00	106	1	4	152
141	130820241852	2.50	2.50	19	1	4	153
142	CP140920241902	225.00	225.00	107	1	4	154
143	CP140920241905	330.00	330.00	108	1	4	155
144	310820241913	110.00	110.00	107	1	4	156
145	310820241914	110.00	110.00	108	1	4	157
147	CP140920241923	130.00	130.00	109	1	4	159
148	CP140920241924	540.00	540.00	110	1	4	160
149	020920241931	65.00	65.00	109	1	4	161
150	020920241932	130.00	130.00	110	1	4	162
151	CP140920241935	165.00	165.00	111	1	4	163
152	CP140920241940	150.00	150.00	112	1	4	164
153	CP140920241942	150.00	150.00	113	1	4	165
154	CP140920241946	255.00	255.00	114	1	4	166
155	CP140920241947	255.00	255.00	115	1	4	167
156	020920241948	140.00	140.00	115	1	4	168
157	070920241949	40.00	40.00	114	1	4	169
158	CP140920241957	140.00	140.00	116	1	4	170
159	030920241958	70.00	70.00	116	1	4	171
160	110920242009	100.00	100.00	85	1	4	172
161	CP140920242012	120.00	120.00	117	1	4	173
162	300820242015	30.00	30.00	117	1	4	174
163	CP140920242018	450.00	450.00	118	1	4	175
164	CP140920242020	140.00	140.00	119	1	4	176
165	CP140920242022	140.00	140.00	120	1	4	177
166	CP140920242042	120.00	120.00	121	1	4	178
167	CP140920242044	140.00	140.00	122	1	4	179
168	CP140920242048	500.00	500.00	123	1	4	180
169	CP140920242049	600.00	600.00	124	1	4	181
170	CP140920242050	110.00	110.00	125	1	4	182
171	CP140920242052	140.00	140.00	126	1	4	183
172	CP170920241707	140.00	140.00	127	1	4	184
173	140920241709	70.00	70.00	92	1	4	185
174	CP170920241710	140.00	140.00	128	1	4	186
175	CP170920241712	280.00	280.00	129	1	4	187
176	140920241717	70.00	70.00	113	1	4	188
177	CP170920241726	240.00	240.00	130	1	4	189
178	140920241738	50.00	50.00	81	1	4	190
179	140920241729	32.50	32.50	50	1	4	191
146	300820241914	90.00	90.00	93	1	4	158
180	CP170920241730	140.00	140.00	131	1	4	192
181	1409202417	90.00	90.00	45	1	4	193
182	140920241733	80.00	80.00	16	1	4	194
183	140920241734	200.00	200.00	65	1	4	195
184	140920241735	110.00	110.00	88	1	4	196
185	CP170920241802	600.00	600.00	132	1	4	197
187	CP170920241803	250.00	250.00	134	1	4	199
188	150920241821	110.00	110.00	108	1	4	200
189	CP170920241824	150.00	150.00	135	1	4	201
190	CP170920241825	315.00	315.00	136	1	4	202
191	150920241830	70.00	70.00	135	1	4	203
192	150920241831	167.00	167.00	24	1	4	204
193	150920241832	50.00	50.00	84	1	4	205
194	150920241833	40.00	40.00	1	1	4	206
195	150920241834	100.00	100.00	91	1	4	207
196	CP170920241842	500.00	500.00	137	1	4	208
197	310820241843	70.00	70.00	137	1	4	209
198	020820241843	250.00	250.00	137	1	4	210
199	150920241844	50.00	50.00	137	1	4	211
200	150920241849	50.00	50.00	74	1	4	212
201	160920241854	70.00	70.00	62	1	4	213
202	160920241855	100.00	100.00	122	1	4	214
203	CP170920241857	90.00	90.00	138	1	4	215
1209	201120241412	480.00	480.00	98	1	4	1220
205	160920241900	70.00	70.00	75	1	4	217
206	160920241901	40.00	40.00	115	1	4	218
207	CP170920241903	150.00	150.00	139	1	4	219
208	CP170920241904	180.00	180.00	140	1	4	220
209	CP170920241906	150.00	150.00	141	1	4	221
210	CP170920241907	270.00	270.00	142	1	4	222
211	CP170920241908	115.00	115.00	143	1	4	223
212	CP170920241909	65.00	65.00	144	1	4	224
213	160920241910	180.00	180.00	64	1	4	225
214	160920241917	110.00	110.00	119	1	4	226
215	160920241919	40.00	40.00	16	1	4	227
216	160920241920	65.00	65.00	42	1	4	228
217	160920241921	20.00	20.00	10	1	4	229
218	160920241922	60.00	60.00	107	1	4	230
219	CP170920241926	150.00	150.00	145	1	4	231
220	160920241927	140.00	140.00	145	1	4	232
221	CP170920241930	250.00	250.00	146	1	4	233
222	060920241931	60.00	60.00	146	1	4	234
223	160920241933	60.00	60.00	146	1	4	235
224	170920241356	75.00	75.00	77	1	4	236
225	170920241358	110.00	110.00	56	1	4	237
226	170920241400	15.00	15.00	107	1	4	238
227	190920241402	30.00	30.00	27	1	4	239
228	CP190920241408	501.00	501.00	147	1	4	240
229	170920241410	65.00	65.00	42	1	4	241
230	CP190920241411	200.00	200.00	148	1	4	242
231	CP190920241412	300.00	300.00	149	1	4	243
232	170920241413	450.00	450.00	118	1	4	244
233	CP190920241416	800.00	800.00	150	1	4	245
1222	221120241702	60.00	60.00	279	1	4	1233
235	170920241419	160.00	130.00	63	1	4	247
236	170920241420	70.00	70.00	7	1	4	248
238	170920241432	75.00	75.00	47	1	4	250
239	170920241436	30.00	30.00	111	1	4	251
240	190920241439	500.00	500.00	123	1	4	252
241	170920241440	40.00	40.00	48	1	4	253
242	190920241441	40.00	40.00	16	1	4	254
243	190920241442	160.00	160.00	55	1	4	255
244	CP190920241445	140.00	140.00	152	1	4	256
245	CP190920241446	400.00	400.00	153	1	4	257
246	CP190920241447	150.00	150.00	154	1	4	258
247	CP190920241448	800.00	800.00	155	1	4	259
248	CP190920241449	345.00	345.00	156	1	4	260
249	190920241450	40.00	40.00	40	1	4	261
250	170920241451	15.00	15.00	10	1	4	262
251	180720241453	20.00	20.00	156	1	4	263
252	020820241453	35.00	35.00	156	1	4	264
253	160820241454	20.00	20.00	156	1	4	265
254	160920241454	20.00	20.00	156	1	4	266
255	CP190920241843	408.00	408.00	157	1	4	267
256	182420231846	30.00	30.00	157	1	4	268
257	160320241848	20.00	20.00	157	1	4	269
258	010420241848	20.00	20.00	157	1	4	270
259	020520241849	20.00	20.00	157	1	4	271
260	160520241852	20.00	20.00	157	1	4	272
261	170620241853	20.00	20.00	157	1	4	273
262	160720241854	20.00	20.00	157	1	4	274
263	050820241854	10.00	10.00	157	1	4	275
264	090820241855	10.00	10.00	157	1	4	276
265	020920241856	20.00	20.00	157	1	4	277
266	190820241859	20.00	20.00	157	1	3	278
237	200920241431	20.00	20.00	85	1	4	249
267	160920241700	20.00	20.00	157	1	4	279
268	CP190920241952	360.00	360.00	158	1	4	280
269	180620241953	120.00	120.00	158	1	4	281
270	170920241954	120.00	120.00	158	1	4	282
271	CP200920241330	300.00	300.00	159	1	4	283
272	110720241349	60.00	60.00	159	1	4	284
273	150720241350	90.00	90.00	159	1	4	285
274	CP200920241400	90.00	90.00	160	1	4	286
275	CP200920241511	1200.00	1200.00	161	1	4	287
276	180920241512	300.00	300.00	161	1	4	288
277	CP200920241514	300.00	300.00	162	1	4	289
278	180720241523	80.00	80.00	162	1	4	290
279	050820241523	100.00	100.00	162	1	4	291
280	180520241525	25.00	25.00	162	1	4	292
281	CP200920241527	150.00	150.00	163	1	4	293
282	CP200920241529	180.00	180.00	164	1	4	294
283	030920241530	100.00	100.00	163	1	4	295
284	CP200920241538	90.00	90.00	165	1	4	296
285	050920241539	45.00	45.00	160	1	4	297
286	CP200920241540	480.00	480.00	166	1	4	298
287	110720241541	60.00	60.00	166	1	4	299
288	120820241542	20.00	20.00	166	1	4	300
289	110920241542	20.00	20.00	166	1	4	301
290	CP200920241727	360.00	360.00	167	1	4	302
291	180920241828	15.00	15.00	8	1	4	303
292	180920241729	30.00	30.00	117	1	4	304
293	180920241730	300.00	300.00	161	1	4	305
294	CP200920241732	165.00	165.00	168	1	4	306
295	CP200920241734	140.00	140.00	169	1	4	307
296	180920241736	55.00	55.00	28	1	4	308
297	180920241738	50.00	50.00	22	1	4	309
298	180920241739	30.00	30.00	43	1	4	310
299	CP200920241746	140.00	140.00	170	1	4	311
300	220720241747	35.00	35.00	170	1	4	312
301	050820241748	35.00	35.00	170	1	4	313
302	180920241748	30.00	30.00	170	1	4	314
303	CP200920241753	90.00	90.00	171	1	4	315
1210	201120241859	40.00	40.00	441	1	4	1221
305	180920241754	40.00	40.00	25	1	4	317
306	180920241755	40.00	40.00	16	1	4	318
307	180920241756	160.00	160.00	55	1	4	319
308	110920241600	45.00	45.00	165	1	4	320
309	200920241601	90.00	90.00	166	1	4	321
310	CP210920241602	300.00	300.00	173	1	4	322
311	200920241603	50.00	50.00	34	1	4	323
312	CP210920241606	160.00	160.00	174	1	4	324
313	200920241608	30.00	30.00	107	1	4	325
314	CP210920241609	180.00	180.00	175	1	4	326
315	200920241610	40.00	40.00	16	1	4	327
316	200920241611	160.00	160.00	55	1	4	328
317	CP210920241613	250.00	250.00	176	1	4	329
318	CP230920241334	140.00	140.00	177	1	4	330
319	120820241338	25.00	25.00	177	1	4	331
320	090920241339	80.00	80.00	177	1	4	332
321	210320241339	25.00	25.00	177	1	4	333
322	210920241349	32.50	32.50	50	1	4	334
323	210920241350	40.00	40.00	16	1	4	335
324	210320241351	160.00	160.00	55	1	4	336
325	CP230920241352	140.00	140.00	178	1	4	337
326	CP230920241353	70.00	70.00	179	1	4	338
327	210320241356	40.00	40.00	44	1	4	339
328	210920241357	30.00	30.00	131	1	4	340
329	220320241422	160.00	160.00	55	1	4	341
330	CP230920241424	30.00	30.00	180	1	4	342
331	CP230920241425	160.00	160.00	181	1	4	343
332	CP230920241435	90.00	90.00	182	1	4	344
333	CP230920241916	600.00	600.00	183	1	4	345
334	200720241917	100.00	100.00	183	1	4	346
335	230920241918	200.00	200.00	183	1	3	347
336	290720241918	15.00	15.00	183	1	4	348
337	210920241919	20.00	20.00	183	1	4	349
338	CP230920241928	500.00	500.00	184	1	4	350
339	260720241729	23.00	23.00	184	1	4	351
340	290720241730	43.00	43.00	184	1	4	352
341	180820241930	5.00	5.00	184	1	4	353
342	240820241931	25.00	25.00	184	1	4	354
343	070920241931	20.00	20.00	184	1	4	355
344	180920241932	20.00	20.00	184	1	4	356
345	210920241932	10.00	10.00	184	1	4	357
346	CP250920241323	132.00	132.00	185	1	4	358
347	230920241328	300.00	300.00	79	1	4	359
348	230420241330	15.00	15.00	8	1	4	360
349	230920241331	40.00	40.00	25	1	4	361
350	230920241332	210.00	210.00	83	1	4	362
351	23092024133	40.00	40.00	16	1	4	363
352	230920241333	160.00	160.00	55	1	4	364
353	CP250920241359	150.00	150.00	186	1	4	365
1211	CP261120241905	5600.00	5600.00	506	1	4	1222
355	CP250920241400	500.00	500.00	188	1	4	367
356	CP250920241401	255.00	255.00	189	1	4	368
357	240920241402	33.00	33.00	10	1	4	369
358	240920241403	40.00	40.00	16	1	4	370
359	240920241404	160.00	160.00	55	1	4	371
360	240920241405	150.00	150.00	20	1	4	372
361	CP250920241407	375.00	375.00	190	1	4	373
362	CP270920241401	450.00	450.00	191	1	4	374
363	120920241410	225.00	225.00	191	1	4	375
364	260920241410	225.00	225.00	191	1	4	376
365	260920241726	20.00	20.00	33	1	4	377
366	CP270920241730	70.00	70.00	192	1	4	378
1223	211120241512	160.00	160.00	98	1	4	1234
368	CP270920241731	90.00	90.00	194	1	4	380
369	26092024	130.00	130.00	54	1	4	381
370	260920241739	40.00	40.00	16	1	4	382
371	260920241740	160.00	160.00	55	1	4	383
372	260920241741	50.00	50.00	40	1	4	384
373	CP270920241826	140.00	140.00	195	1	4	385
374	120820241827	70.00	70.00	195	1	4	386
375	260920241827	70.00	70.00	195	1	4	387
376	CP270920241839	250.00	250.00	196	1	4	388
377	CP270920241841	90.00	90.00	197	1	4	389
378	CP270920241843	130.00	130.00	198	1	4	390
379	250920241850	90.00	90.00	87	1	4	391
380	250920241851	150.00	150.00	112	1	4	392
381	CP270920241855	300.00	300.00	199	1	4	393
382	100820241903	100.00	100.00	199	1	4	394
383	280820241903	80.00	80.00	199	1	4	395
384	250920241904	130.00	130.00	199	1	4	396
385	CP270920241908	140.00	140.00	200	1	4	397
1231	CP261120242017	80.00	80.00	518	1	4	1242
387	CP270920241909	160.00	160.00	202	1	4	399
388	CP270920241941	150.00	150.00	203	1	4	400
389	CP270920241942	300.00	300.00	204	1	4	401
390	250920241946	30.00	30.00	43	1	4	402
391	250920241947	50.00	50.00	84	1	4	403
392	250920241948	40.00	40.00	16	1	4	404
393	250920241949	160.00	160.00	55	1	4	405
394	CP270920242011	1100.00	1100.00	205	1	4	406
395	CP270920242012	150.00	150.00	206	1	4	407
396	CP031020242110	140.00	140.00	207	1	4	408
397	CP031020242111	50.00	50.00	208	1	4	409
398	270920242112	40.00	40.00	16	1	4	410
399	290720242113	10.00	10.00	29	1	4	411
1239	221120241703	60.00	60.00	279	1	4	1250
401	270920242115	17.00	17.00	10	1	4	413
402	270920242116	20.00	20.00	69	1	4	414
403	280920242117	10.00	10.00	184	1	4	415
404	280920272119	35.00	35.00	170	1	4	416
405	CP031020242123	140.00	140.00	209	1	4	417
1247	231120241524	60.00	60.00	279	1	4	1258
407	CP031020242125	150.00	150.00	211	1	4	419
408	CP031020242126	60.00	60.00	212	1	4	420
409	290920242127	125.00	125.00	176	1	4	421
410	290920242128	160.00	160.00	55	1	4	422
411	290920242129	35.00	35.00	85	1	4	423
412	290920242130	100.00	100.00	21	1	4	424
413	300920242132	33.00	33.00	185	1	4	425
414	330920242133	18.00	18.00	10	1	4	426
415	CP031020242135	150.00	150.00	213	1	4	427
416	300920242137	70.00	70.00	62	1	4	428
417	300920242138	285.00	285.00	5	1	4	429
418	CP031020242140	280.00	280.00	214	1	4	430
419	300920242140	400.00	400.00	155	1	4	431
420	300920242141	38.00	38.00	1	1	4	432
421	300920242142	140.00	140.00	152	1	4	433
422	300920242143	220.00	220.00	132	1	4	434
423	300920242144	50.00	50.00	91	1	4	435
424	300920242145	60.00	60.00	175	1	4	436
425	300920242146	70.00	70.00	141	1	4	437
426	300920242147	70.00	70.00	49	1	4	438
427	300920242148	40.00	40.00	16	1	4	439
428	300920242149	160.00	160.00	55	1	4	440
429	300920242150	50.00	50.00	140	1	4	441
430	CP031020242150	360.00	360.00	215	1	4	442
431	CP031020242153	150.00	150.00	216	1	4	443
432	300920242153	65.00	65.00	105	1	4	444
433	300920242152	110.00	110.00	78	1	4	445
434	30092022155	70.00	70.00	92	1	4	446
435	300920212156	50.00	50.00	139	1	4	447
436	CP031020242200	115.00	115.00	217	1	4	448
437	CP031020242201	360.00	360.00	218	1	4	449
1254	241120241413	40.00	40.00	441	1	4	1265
438	CP031020242202	150.00	150.00	219	1	4	450
439	CP031020242203	140.00	140.00	220	1	4	451
440	CP031020242204	140.00	140.00	221	1	4	452
441	300920242205	110.00	110.00	108	1	4	453
442	CP031020242207	300.00	300.00	222	1	4	454
443	300920242207	100.00	100.00	222	1	4	455
444	011020247159	50.00	50.00	85	1	4	456
445	011020241804	70.00	70.00	169	1	4	457
446	0110202471807	90.00	90.00	75	1	4	458
447	CP081020241811	501.00	501.00	223	1	4	459
448	CP081020241812	120.00	120.00	224	1	4	460
449	CP081020241814	150.00	150.00	225	1	4	461
450	CP081020241815	250.00	250.00	226	1	4	462
451	CP081020241820	165.00	165.00	227	1	4	463
452	CP081020241821	80.00	80.00	228	1	4	464
453	CP081020241822	140.00	140.00	229	1	4	465
454	011020241831	40.00	40.00	183	1	4	466
455	011020241836	30.00	30.00	9	1	4	467
456	011020241843	175.00	175.00	2	1	4	468
457	011020241844	80.00	80.00	16	1	4	469
458	011020241847	200.00	200.00	65	1	4	470
459	011020241850	180.00	180.00	64	1	4	471
460	011020241853	40.00	40.00	48	1	4	472
461	011020241858	40.00	40.00	115	1	4	473
462	011020241900	70.00	70.00	178	1	4	474
463	011020241902	160.00	160.00	55	1	4	475
464	011020241905	80.00	80.00	137	1	4	476
465	011020241911	20.00	20.00	8	1	4	477
466	CP081020241919	270.00	270.00	230	1	4	478
467	011020241921	70.00	70.00	66	1	4	479
468	011020241926	210.00	210.00	83	1	4	480
469	011020241929	50.00	50.00	84	1	4	481
470	011020241936	80.00	80.00	113	1	4	482
471	011020241938	50.00	50.00	22	1	4	483
472	011020241940	30.00	30.00	43	1	4	484
473	021020241731	10.00	10.00	144	1	4	485
474	031020241632	35.00	35.00	10	1	4	486
475	021020241634	40.00	40.00	16	1	4	487
476	021020241636	40.00	40.00	25	1	4	488
477	021024241637	160.00	160.00	55	1	4	489
478	021020241639	75.00	75.00	47	1	4	490
479	021020241646	55.00	55.00	168	1	4	491
480	021020241649	95.00	95.00	111	1	4	492
481	031020241652	10.00	10.00	184	1	4	493
482	021020241657	30.00	30.00	131	1	4	494
483	CP091020241706	270.00	270.00	231	1	4	495
484	CP091020241708	165.00	165.00	232	1	4	496
485	021020241716	375.00	375.00	39	1	4	497
486	0210220241717	50.00	50.00	63	1	4	498
487	021020241723	65.00	65.00	178	1	4	499
488	CP091020241735	400.00	400.00	233	1	4	500
489	160920241796	55.00	55.00	233	1	4	501
490	021020241737	40.00	40.00	233	1	4	502
491	021020241740	55.00	55.00	218	1	4	503
492	031020241602	70.00	70.00	186	1	4	504
493	031020241805	80.00	80.00	53	1	4	505
494	CP091020241807	330.00	330.00	234	1	4	506
495	CP091020241808	150.00	150.00	235	1	4	507
496	CP091020241810	80.00	80.00	236	1	4	508
497	031020241813	50.00	50.00	181	1	4	509
498	031020241815	150.00	150.00	214	1	4	510
499	031020241817	160.00	160.00	110	1	4	511
500	CP091020241823	150.00	150.00	237	1	4	512
501	CP091020241825	80.00	80.00	238	1	4	513
502	CP091020241827	255.00	255.00	239	1	4	514
503	CP111020241054	540.00	540.00	240	1	4	515
504	041020241056	130.00	130.00	18	1	4	516
505	041020241058	160.00	160.00	55	1	4	517
506	041020241059	30.00	30.00	122	1	4	518
507	CP111020241110	90.00	90.00	241	1	4	519
508	CP111020241111	130.00	130.00	242	1	4	520
509	CP111020241126	270.00	270.00	243	1	4	521
510	040820241127	90.00	90.00	243	1	4	522
511	041020241128	50.00	50.00	243	1	4	523
512	041020241131	100.00	100.00	166	1	4	524
513	041020241133	85.00	85.00	189	1	4	525
514	051020241900	65.00	65.00	198	1	4	526
515	051020241901	10.00	10.00	184	1	4	527
516	CP171020241904	90.00	90.00	244	1	4	528
517	CP171020241905	150.00	150.00	245	1	4	529
518	CP171020241906	140.00	140.00	246	1	4	530
519	CP171020241907	90.00	90.00	247	1	4	531
520	CP171020241908	150.00	150.00	248	1	4	532
522	CP171020241913	150.00	150.00	250	1	4	534
523	061020241913q	160.00	160.00	55	1	4	535
524	CP171020241917	150.00	150.00	251	1	4	536
1212	CP261120241906	70.00	70.00	507	1	4	1223
1224	211120241513	40.00	40.00	441	1	4	1235
527	CP171020241918	80.00	80.00	254	1	4	539
528	051020241913	30.00	30.00	131	1	4	540
1232	CP261120242018	140.00	140.00	519	1	4	1243
530	051020241920	160.00	160.00	55	1	4	542
531	051020241921	30.00	30.00	81	1	4	543
532	051020241922	30.00	30.00	203	1	4	544
533	071020241927	68.00	68.00	235	1	4	545
534	CP171020241933	220.00	220.00	255	1	4	546
535	071020241933	150.00	150.00	255	1	4	547
536	CP171020241936	150.00	150.00	256	1	4	548
537	071020241936	80.00	80.00	25	1	4	549
538	CP171020241938	50.00	50.00	257	1	4	550
539	CP171020241939	1200.00	1200.00	258	1	4	551
540	CP171020241940	50.00	50.00	259	1	4	552
541	CP171020241943	150.00	150.00	260	1	4	553
542	071020241943	40.00	40.00	16	1	4	554
543	071020241944	160.00	160.00	55	1	4	555
544	CP171020241949	140.00	140.00	261	1	4	556
545	071120241949	30.00	30.00	261	1	4	557
546	CP171020241951	90.00	90.00	262	1	4	558
547	CP171020241952	160.00	160.00	263	1	4	559
548	CP171020241953	90.00	90.00	264	1	4	560
549	081020241701	50.00	50.00	84	1	4	561
550	081020241751	80.00	80.00	190	1	4	562
551	081020241556	160.00	160.00	55	1	4	563
552	CP171020242001	700.00	700.00	265	1	4	564
553	160920242002	20.00	20.00	265	1	4	565
554	210920242003	20.00	20.00	265	1	4	566
555	021020242003	80.00	80.00	265	1	4	567
556	081020242004	80.00	80.00	265	1	4	568
557	091020242007	10.00	10.00	184	1	4	569
558	091020242008	160.00	160.00	55	1	4	570
559	101020241731	120.00	120.00	87	1	4	571
560	101020241732	45.00	45.00	244	1	4	572
561	101020241733	150.00	150.00	200	1	4	573
1240	221120241536	30.00	30.00	483	1	4	1251
563	101020241737	120.00	120.00	158	1	4	575
564	CP191020241741	600.00	600.00	266	1	4	576
1248	231120241525	160.00	160.00	98	1	4	1259
1255	251120241412	120.00	120.00	433	1	4	1266
567	CP191020241742	150.00	150.00	269	1	4	579
1261	251120241416	60.00	60.00	279	1	4	1272
1265	CP271120241708	500.00	500.00	529	1	4	1276
1268	CP271120241713	25.00	25.00	532	1	4	1279
571	CP191020241743	150.00	150.00	273	1	4	583
572	101020241742	30.00	30.00	43	1	4	584
573	101020241743	160.00	160.00	55	1	4	585
574	111020241745	35.00	35.00	44	1	4	586
575	111020241748	130.00	130.00	166	1	4	587
576	111020241749	60.00	60.00	37	1	4	588
577	111020241750	45.00	45.00	255	1	4	589
578	111020241751	50.00	50.00	154	1	4	590
579	CP191020241753	150.00	150.00	274	1	4	591
1271	CP271120241721	60.00	60.00	535	1	4	1282
581	CP191020241754	260.00	260.00	276	1	4	593
582	CP191020241755	130.00	130.00	277	1	4	594
583	121020241759	70.00	70.00	221	1	4	595
584	CP191020241805	330.00	330.00	278	1	4	596
585	CP191020241806	3600.00	3600.00	279	1	4	597
586	121020241806	30.00	30.00	131	1	4	598
588	121020241808	160.00	160.00	55	1	4	600
589	131020241810	160.00	160.00	55	1	4	601
590	131020241811	60.00	60.00	85	1	4	602
591	141020241813	20.00	20.00	8	1	4	603
593	141020241815	40.00	40.00	30	1	4	605
594	141020241816	50.00	50.00	217	1	4	606
595	141020241817	20.00	20.00	69	1	4	607
596	141020241818	150.00	150.00	250	1	4	608
597	CP191020241820	180.00	180.00	280	1	4	609
598	CP191020241821	90.00	90.00	281	1	4	610
599	141020241821	285.00	285.00	205	1	4	611
600	141020241823	350.00	350.00	106	1	4	612
601	141020241824	20.00	20.00	58	1	4	613
602	141020241825	7.00	7.00	184	1	4	614
400	290720242114	140.00	140.00	73	1	4	412
603	CP191020241830	140.00	140.00	282	1	4	615
1277	CP021220241857	140.00	140.00	541	1	4	1288
605	CP191020241832	80.00	80.00	284	1	4	617
606	141020241832	100.00	100.00	188	1	4	618
607	141020241833	160.00	160.00	55	1	4	619
592	141020241714	110.00	110.00	89	1	4	604
608	141020241836	100.00	100.00	258	1	4	620
609	141020241837	430.00	430.00	124	1	4	621
610	CP201020242015	150.00	150.00	285	1	4	622
611	CP201020242016	360.00	360.00	286	1	4	623
612	CP201020242018	140.00	140.00	287	1	4	624
613	310820242019	50.00	50.00	285	1	4	625
614	021020242019	50.00	50.00	285	1	4	626
615	011020242020	100.00	100.00	286	1	4	627
617	CP231020241649	150.00	150.00	288	1	4	629
1225	211120241543	85.00	85.00	189	1	4	1236
619	CP231020241816	280.00	280.00	290	1	4	631
620	CP231020241817	90.00	90.00	291	1	4	632
621	CP231020241841	30.00	30.00	292	1	4	633
622	151020242038	75.00	75.00	135	1	4	634
623	151020242039	20.00	20.00	117	1	4	635
624	151020242030	76.00	74.00	1	1	4	636
625	151020242035	50.00	50.00	214	1	4	637
626	151020242036	100.00	100.00	149	1	4	638
627	151020242024	45.00	45.00	198	1	4	639
628	151020241524	70.00	70.00	246	1	4	640
629	151020242048	80.00	80.00	226	1	4	641
630	151020242045	100.00	100.00	222	1	4	642
631	1510202412051	120.00	120.00	175	1	4	643
632	151020242050	157.00	157.00	147	1	4	644
633	151020242053	70.00	70.00	128	1	4	645
634	151020242054	50.00	50.00	238	1	4	646
635	231020242057	50.00	50.00	84	1	4	647
636	151020242056	30.00	30.00	86	1	4	648
637	231020242059	100.00	100.00	279	1	4	649
638	231020242058	55.00	55.00	227	1	4	650
639	151020242101	160.00	160.00	55	1	4	651
640	151020242102	75.00	75.00	141	1	4	652
641	151020242103	65.00	65.00	269	1	4	653
643	151020241324	80.00	80.00	63	1	4	655
644	CP241020241325	280.00	280.00	293	1	4	656
1241	221120241625	160.00	160.00	98	1	4	1252
646	CP241020241327	300.00	300.00	295	1	4	658
647	151020241327	85.00	85.00	75	1	4	659
648	161020241336	55.00	55.00	168	1	4	660
649	170820241344	100.00	100.00	17	1	4	661
650	160920241344	120.00	120.00	17	1	4	662
652	CP241020241347	160.00	160.00	296	1	4	664
653	CP241020241349	150.00	150.00	297	1	4	665
654	CP241020241402	300.00	300.00	298	1	4	666
655	140920241402	110.00	110.00	298	1	4	667
656	161020241413	220.00	220.00	298	1	4	668
657	161020241414	80.00	80.00	167	1	4	669
658	161020241412	80.00	80.00	146	1	4	670
659	161020241416	130.00	130.00	110	1	4	671
660	161020241417	140.00	140.00	206	1	4	672
661	161020241418	60.00	60.00	224	1	4	673
662	161020241719	75.00	75.00	248	1	4	674
663	CP241020241420	140.00	140.00	299	1	4	675
664	CP241020241421	525.00	525.00	300	1	4	676
665	CP241020241423	315.00	315.00	301	1	4	677
666	CP241020241425	270.00	270.00	302	1	4	678
667	CP241020241427	330.00	330.00	303	1	4	679
668	CP241020241428	180.00	180.00	304	1	4	680
669	161020241435	65.00	65.00	105	1	4	681
670	161020241438	50.00	50.00	259	1	4	682
671	161020241439	50.00	50.00	91	1	4	683
672	CP241020241439	80.00	80.00	305	1	4	684
673	161020241440	50.00	50.00	139	1	4	685
674	161020241443	100.00	100.00	279	1	4	686
675	241020241445	65.00	65.00	235	1	4	687
676	161020241445	50.00	50.00	69	1	4	688
677	161020241446	40.00	40.00	36	1	4	689
678	161020241448	80.00	80.00	130	1	4	690
679	CP241020241449	150.00	150.00	306	1	4	691
680	CP241020241450	130.00	130.00	307	1	4	692
681	161020241751	200.00	200.00	65	1	4	693
682	CP241020241452	510.00	510.00	308	1	4	694
683	CP241020241453	150.00	150.00	309	1	4	695
684	161020241454	160.00	160.00	55	1	4	696
685	161020241455	150.00	150.00	12	1	4	697
686	CP241020241611	540.00	540.00	310	1	4	698
688	171020241612	75.00	75.00	213	1	4	700
689	171020241602	90.00	90.00	231	1	4	701
690	171020241605	50.00	50.00	154	1	4	702
691	CP241020241625	400.00	400.00	311	1	4	703
693	CP241020241626	300.00	300.00	313	1	4	705
694	171020241633	130.00	130.00	242	1	4	706
695	CP241020241652	600.00	600.00	314	1	4	707
642	301020241320	80.00	80.00	254	1	4	654
696	CP241020241658	550.00	550.00	315	1	4	708
697	CP241020241659	880.00	880.00	316	1	4	709
698	CP241020241700	150.00	150.00	317	1	4	710
1214	CP261120241913	70.00	70.00	509	1	4	1225
1226	211120241515	30.00	30.00	185	1	4	1237
701	CP241020241701	150.00	150.00	320	1	4	713
702	171020241702	100.00	100.00	279	1	4	714
703	171020241701	160.00	160.00	55	1	4	715
704	171020241704	20.00	20.00	212	\N	4	716
705	181020241710	40.00	40.00	228	1	4	717
706	181020241713	80.00	80.00	286	1	4	718
707	181020241714	150.00	150.00	282	1	4	719
708	CP241020241732	900.00	900.00	321	1	4	720
709	181020241735	50.00	50.00	74	1	4	721
710	181020241736	100.00	100.00	279	1	4	722
711	181020241738	140.00	140.00	215	1	4	723
712	181020241725	40.00	40.00	247	1	4	724
713	191020241514	70.00	70.00	287	1	4	725
714	191020241517	25.00	25.00	114	1	4	726
715	191020241745	30.00	30.00	86	1	4	727
716	CP241020241753	70.00	70.00	322	1	4	728
717	180720241753	10.00	10.00	322	1	4	729
718	220720241754	10.00	10.00	322	1	4	730
719	240720241755	5.00	5.00	322	1	4	731
720	260720241756	10.00	10.00	322	1	4	732
721	310720241756	20.00	20.00	322	1	4	733
722	191020241757	30.00	30.00	111	1	4	734
723	191020241759	30.00	30.00	183	1	4	735
724	191020241800	40.00	40.00	265	1	4	736
725	191020241705	10.00	10.00	184	1	4	737
726	1910202418045	30.00	30.00	203	1	4	738
727	CP241020241807	140.00	140.00	323	1	4	739
728	CP241020241808	140.00	140.00	324	1	4	740
729	191020241809	160.00	160.00	98	1	4	741
730	CP241020241812	140.00	140.00	325	1	4	742
1242	221120241525	40.00	40.00	441	1	4	1253
733	CP241020241813	150.00	150.00	328	1	4	745
734	201020241814	20.00	20.00	8	1	4	746
735	201020241714	160.00	160.00	98	1	4	747
736	CP241020241817	150.00	150.00	329	1	4	748
737	211020241822	375.00	375.00	39	1	4	749
738	241020241820	180.00	180.00	266	1	4	750
739	211020241823	170.00	170.00	240	1	4	751
740	211020241725	300.00	300.00	161	1	4	752
741	CP241020241826	150.00	150.00	330	1	4	753
742	CP241020241827	50.00	50.00	331	1	4	754
743	CP241020241828	150.00	150.00	332	1	4	755
744	211020241829	150.00	150.00	127	1	4	756
745	211020241729	160.00	160.00	98	1	4	757
746	CP241020241912	200.00	200.00	333	1	4	758
747	270720241913	50.00	50.00	333	1	4	759
748	300820241913	50.00	50.00	333	1	4	760
749	270920241914	50.00	50.00	333	1	4	761
750	CP241020241918	90.00	90.00	334	1	4	762
751	260720241918	90.00	90.00	334	1	4	763
752	CP241020241920	140.00	140.00	335	1	4	764
753	110920241920	45.00	45.00	335	1	4	765
754	CP251020241339	165.00	165.00	336	1	4	766
755	170820241339	55.00	55.00	336	1	4	767
756	300820241340	55.00	55.00	336	1	4	768
757	140920241340	55.00	55.00	336	1	4	769
758	CP261020241354	90.00	90.00	337	1	4	770
759	CP271020241820	250.00	250.00	338	1	4	771
760	CP271020241823	150.00	150.00	339	1	4	772
761	CP271020241831	280.00	280.00	340	1	4	773
762	CP271020241834	150.00	150.00	341	1	4	774
763	CP271020241835	150.00	150.00	342	1	4	775
764	221020241838	300.00	300.00	204	1	4	776
765	221020241835	160.00	160.00	98	1	4	777
766	221020271836	100.00	100.00	279	1	4	778
767	CP271020241847	230.00	230.00	343	1	4	779
1249	231120241526	40.00	40.00	441	1	4	1260
769	CP271020241848	50.00	50.00	345	1	4	781
770	CP271020241849	100.00	100.00	346	1	4	782
771	231020241853	100.00	100.00	279	1	4	783
772	231020241856	160.00	160.00	98	1	4	784
773	231020241855	30.00	30.00	117	1	4	785
774	231020241852	55.00	55.00	44	1	4	786
775	231020241845	50.00	50.00	86	1	4	787
776	241020241758	30.00	30.00	265	1	4	788
777	CP271020241902	90.00	90.00	347	1	4	789
778	241020241825	10.00	10.00	169	1	4	790
779	151020241712	70.00	70.00	169	1	4	791
780	CP271020241914	140.00	140.00	348	1	4	792
1256	251120241413	30.00	30.00	483	1	4	1267
781	CP271020241915	150.00	150.00	349	1	4	793
782	241020241717	60.00	60.00	279	1	4	794
783	241020241919	160.00	160.00	98	1	4	795
784	CP271020241930	216.00	216.00	350	1	4	796
785	CP271020241932	160.00	160.00	351	1	4	797
786	CP271020241934	140.00	140.00	352	1	4	798
787	251020241935	45.00	45.00	244	1	4	799
788	251020241725	60.00	60.00	279	1	4	800
789	251020241736	160.00	160.00	98	1	4	801
790	CP281020242003	70.00	70.00	353	1	4	802
791	CP281020242008	100.00	100.00	354	1	4	803
1215	CP261120241914	150.00	150.00	510	1	4	1226
793	CP281020242009	140.00	140.00	356	1	4	805
794	CP281020242010	300.00	300.00	357	1	4	806
795	CP281020242011	500.00	500.00	358	1	4	807
796	261020242012	50.00	50.00	44	1	4	808
797	261020242011	80.00	80.00	279	1	4	809
798	261020242013	160.00	160.00	98	1	4	810
799	261020242010	40.00	40.00	207	1	4	811
800	261020242014	50.00	50.00	85	1	4	812
801	261020242015	5.00	5.00	184	1	4	813
802	271020241631	160.00	160.00	98	1	4	814
803	281120241632	70.00	70.00	353	1	4	815
804	281120241631	115.00	115.00	343	1	4	816
805	281020241634	40.00	40.00	281	1	4	817
806	281020241636	150.00	150.00	225	1	4	818
807	CP011120241645	150.00	150.00	359	1	4	819
808	281020241637	150.00	150.00	321	1	4	820
809	CP011120241648	130.00	130.00	360	1	4	821
810	281020241638	40.00	40.00	90	1	4	822
811	281020241639	50.00	50.00	18	1	4	823
812	281020241640	75.00	75.00	341	1	4	824
813	281020241651	60.00	60.00	25	1	4	825
814	281020241652	160.00	160.00	98	1	4	826
815	281020241653	50.00	50.00	84	1	4	827
816	291020241700	55.00	55.00	168	1	4	828
817	291020241701	70.00	70.00	311	1	4	829
819	291020241703	285.00	285.00	3	1	4	831
820	291020241704	160.00	160.00	98	1	4	832
821	291020241705	60.00	60.00	279	1	4	833
822	291020241706	10.00	10.00	170	1	4	834
823	291020241707	13.00	13.00	184	1	4	835
824	291020241708	50.00	50.00	333	1	4	836
825	CP011120241708	360.00	360.00	361	1	4	837
826	CP011120241715	80.00	80.00	362	1	4	838
827	301020241729	75.00	75.00	309	1	4	839
828	301020241730	75.00	75.00	339	1	4	840
829	301020241731	100.00	100.00	21	1	4	841
204	160920241859	70.00	70.00	114	1	4	216
830	CP011120241923	150.00	150.00	363	1	4	842
831	301020241924	150.00	150.00	190	1	4	843
832	301020241930	70.00	70.00	287	1	4	844
833	301020241926	60.00	60.00	224	1	4	845
834	301020241906	160.00	160.00	98	1	4	846
835	130920241942	300.00	300.00	76	1	4	847
836	151020241944	500.00	500.00	155	1	4	848
837	301020241946	400.00	400.00	313	1	4	849
838	CP011120241946	800.00	800.00	364	1	4	850
839	281020241948	130.00	130.00	277	1	4	851
840	151020241956	220.00	220.00	132	1	4	852
841	281020241958	220.00	220.00	132	1	4	853
842	171020241639	75.00	75.00	220	1	4	854
843	CP051120241642	150.00	150.00	365	1	4	855
844	CP051120241646	250.00	250.00	366	1	4	856
845	130720241653	75.00	75.00	366	1	4	857
846	CP051120241700	90.00	90.00	367	1	4	858
847	CP051120241706	810.00	810.00	368	1	4	859
848	160520241706	120.00	120.00	368	1	4	860
849	150820241707	80.00	80.00	368	1	4	861
850	290920241718	220.00	220.00	119	1	4	862
851	CP051120241720	1025.00	1025.00	369	1	4	863
852	CP061120242036	330.00	330.00	370	1	4	864
853	301020241748	25.00	25.00	144	1	4	865
854	CP081120241753	150.00	150.00	371	1	4	866
856	CP081120241754	25.00	25.00	373	1	4	868
857	CP081120241801	70.00	70.00	374	1	4	869
859	301020241803	60.00	60.00	279	1	4	871
860	301020241705	50.00	50.00	84	1	4	872
861	301020241703	70.00	70.00	246	1	4	873
862	301020241804	220.00	220.00	303	1	4	874
863	31020241705	70.00	70.00	324	1	1	875
864	CP081120241811	840.00	840.00	375	1	4	876
865	311020241819	85.00	85.00	239	1	4	877
866	311020241818	160.00	160.00	98	1	4	878
867	311020241820	70.00	70.00	325	1	4	879
818	291020241702	20.00	20.00	462	1	4	830
868	311020241833	75.00	75.00	328	1	4	880
869	311020241832	80.00	80.00	181	1	4	881
870	31102024185	75.00	75.00	248	1	4	882
871	311020241702	60.00	60.00	307	1	4	883
872	311020241706	90.00	90.00	262	1	4	884
873	311020241725	70.00	70.00	220	1	4	885
874	311020241605	70.00	70.00	299	1	4	886
875	3110202471302	75.00	75.00	256	1	4	887
876	311020241803	55.00	55.00	227	1	4	888
877	311020241843	40.00	40.00	8	1	4	889
878	311020241859	25.00	25.00	142	1	4	890
879	CP081120241901	360.00	360.00	376	1	4	891
880	3110202418904	80.00	80.00	351	1	4	892
881	311020241903	100.00	100.00	222	1	4	893
882	311020241608	50.00	50.00	139	\N	4	894
883	311020241909	160.00	160.00	98	1	4	895
884	311020241911	75.00	75.00	251	1	4	896
885	311020241305	75.00	75.00	306	1	4	897
886	011120241802	80.00	80.00	302	1	4	898
887	011120241807	60.00	60.00	307	\N	4	899
1216	201120241817	30.00	30.00	483	1	4	1227
888	011120241808	50.00	50.00	285	1	4	900
889	011120241805	70.00	70.00	221	1	4	901
890	0111202418010	25.00	25.00	115	1	4	902
891	0111202418011	60.00	60.00	273	1	4	903
892	0111202418012	50.00	50.00	137	1	4	904
893	CP081120241930	300.00	300.00	377	1	4	905
894	0111202418013	70.00	70.00	279	1	4	906
895	0111202418016	40.00	40.00	323	1	4	907
896	011120241913	220.00	220.00	215	1	4	908
897	0111202418018	110.00	110.00	78	1	4	909
898	0111202418019	100.00	100.00	188	1	4	910
899	011020241910	33.00	33.00	185	1	4	911
900	011120241942	175.00	175.00	300	1	4	912
901	230920241958	80.00	80.00	370	1	4	913
902	310820241959	80.00	80.00	370	1	4	914
903	011120241914	70.00	70.00	370	1	4	915
904	CP081120242000	360.00	360.00	378	1	4	916
905	011120241943	167.00	167.00	223	1	4	917
1227	211120241526	30.00	30.00	483	1	4	1238
907	0111202419458	50.00	50.00	166	1	4	919
908	CP081120242013	130.00	130.00	379	1	4	920
1243	CP271120241628	500.00	500.00	524	1	4	1254
910	CP081120242021	150.00	150.00	380	1	4	922
911	CP081120242022	150.00	150.00	381	1	4	923
1250	231120241421	20.00	20.00	183	1	4	1261
913	CP081120242023	270.00	270.00	383	1	4	925
914	011120241904	150.00	150.00	297	1	4	926
915	011120241908	20.00	20.00	72	1	4	927
916	011120241945	50.00	50.00	346	1	4	928
917	CP081120242028	270.00	270.00	384	1	4	929
918	011120241949	20.00	20.00	314	1	4	930
919	011120241825	75.00	75.00	260	1	4	931
920	CP081120242034	300.00	300.00	385	1	4	932
921	CP081120242035	150.00	150.00	386	1	4	933
922	011120241827	40.00	40.00	296	1	4	934
923	01112024154	75.00	75.00	245	1	4	935
924	011120241782	70.00	70.00	325	1	4	936
925	011120241535	80.00	80.00	236	1	4	937
926	081020241502	33.00	33.00	185	1	4	938
927	CP101120241516	140.00	140.00	387	1	4	939
928	021120241414	64.00	64.00	213	1	4	940
929	021120241412	90.00	90.00	231	1	4	941
930	CP101120241519	90.00	90.00	388	1	4	942
931	021120241410	140.00	140.00	263	1	4	943
932	021120241408	30.00	30.00	278	1	4	944
933	021120241421	30.00	30.00	265	1	4	945
934	021120241212	100.00	100.00	279	1	4	946
935	021120241435	100.00	100.00	286	1	3	947
936	CP101120241525	140.00	140.00	389	1	4	948
937	CP101120241526	150.00	150.00	390	1	4	949
1257	CP271120241644	135.00	135.00	527	1	4	1268
944	CP101120241527	260.00	260.00	397	1	4	956
945	CP101120241532	110.00	110.00	398	1	4	957
946	031120241502	320.00	320.00	98	1	4	958
947	031120241503	140.00	140.00	310	1	4	959
948	031120241504	50.00	50.00	237	1	4	960
949	031120241506	10.00	10.00	180	1	4	961
950	CP101120241537	165.00	165.00	399	1	4	962
951	CP101120241538	480.00	480.00	400	1	4	963
952	041120241436	50.00	50.00	207	1	4	964
953	051020241301	30.00	30.00	207	1	4	965
954	121020241502	20.00	20.00	207	1	4	966
955	CP101120241545	120.00	120.00	401	1	4	967
956	CP101120241546	150.00	150.00	402	1	4	968
962	CP101120241547	140.00	140.00	408	1	4	974
963	051120241448	30.00	30.00	203	1	4	975
964	051120241425	160.00	160.00	98	1	4	976
965	CP101120241549	2500.00	2500.00	409	1	4	977
966	061120241552	100.00	100.00	23	1	4	978
967	061120241423	20.00	20.00	115	1	4	979
968	061120241554	15.00	15.00	212	1	4	980
969	061120241555	58.00	58.00	269	1	4	981
970	061120241556	85.00	85.00	409	1	4	982
971	061120241736	160.00	160.00	98	1	4	983
972	CP101120241558	300.00	300.00	410	1	4	984
973	CP101120241559	90.00	90.00	411	1	4	985
1217	CP261120241923	400.00	400.00	511	1	4	1228
1228	211120241503	6.00	6.00	8	1	4	1239
1236	CP261120242019	120.00	120.00	523	1	4	1247
1244	CP271120241629	140.00	140.00	525	1	4	1255
1251	231120241422	40.00	40.00	280	1	4	1262
979	CP101120241600	90.00	90.00	417	1	4	991
980	CP121120241259	380.00	380.00	418	1	4	992
858	301020241802	50.00	50.00	418	1	4	870
981	250720241305	140.00	140.00	418	1	4	993
982	110920241416	115.00	115.00	125	1	4	994
983	CP121120241622	1000.00	1000.00	419	1	4	995
984	CP121120241625	1200.00	1200.00	420	1	4	996
1258	CP271120241645	140.00	140.00	528	1	4	1269
986	CP121120241651	570.00	570.00	422	1	4	998
987	CP121120241701	300.00	300.00	423	1	4	999
988	141020241701	80.00	80.00	423	1	4	1000
989	301020241402	80.00	80.00	423	1	4	1001
990	CP121120241711	150.00	150.00	424	1	4	1002
991	CP121120241713	50.00	50.00	425	1	4	1003
992	CP121120241714	35.00	35.00	426	1	4	1004
993	110920241716	60.00	60.00	424	1	4	1005
994	CP141120241705	250.00	250.00	427	1	4	1006
995	171020241614	75.00	75.00	245	1	4	699
996	CP201120241609	80.00	80.00	428	1	4	1007
997	CP201120241611	150.00	150.00	429	1	4	1008
998	081120241623	10.00	10.00	184	1	4	1009
999	081120241232	80.00	80.00	226	1	4	1010
1000	0811202414412	60.00	60.00	279	1	4	1011
1001	081120241523	160.00	160.00	98	1	4	1012
1002	081120241223	85.00	85.00	16	1	4	1013
1003	081120241312	20.00	20.00	8	1	4	1014
1004	CP201120241628	130.00	130.00	430	1	4	1015
1005	CP201120241635	280.00	280.00	431	1	4	1016
1006	091120241203	108.00	108.00	280	1	4	1017
1007	091120241204	40.00	40.00	26	1	4	1018
1008	CP201120241648	360.00	360.00	432	1	4	1019
1009	101020241523	120.00	120.00	432	1	4	1020
1010	251020241423	120.00	120.00	432	1	4	1021
1011	09112024142	120.00	120.00	432	1	4	1022
1012	CP201120241654	330.00	330.00	433	1	4	1023
1013	091120241256	5.00	5.00	184	1	4	1024
1014	0911202422	60.00	60.00	279	1	4	1025
1015	091120241236	85.00	85.00	409	1	4	1026
1016	091120241239	160.00	160.00	98	1	4	1027
1017	091120241536	30.00	30.00	278	1	4	1028
1018	091120241345	30.00	30.00	203	1	4	1029
1019	091120241348	52.00	52.00	397	1	4	1030
1020	091120241303	20.00	20.00	232	1	4	1031
1021	091120241329	30.00	30.00	233	1	4	1032
1022	CP201120241704	132.00	132.00	434	1	4	1033
1023	CP201120241705	140.00	140.00	435	1	4	1034
1024	CP201120241706	70.00	70.00	436	1	4	1035
1025	CP201120241707	186.00	186.00	437	1	4	1036
1026	101120241705	160.00	160.00	98	1	4	1037
1027	101120241406	130.00	130.00	311	1	4	1038
1028	CP201120241747	50.00	50.00	438	1	4	1039
1029	CP201120241748	150.00	150.00	439	1	4	1040
1030	121120241412	120.00	120.00	361	1	4	1041
1031	121120241413	130.00	130.00	360	1	4	1042
1032	CP201120241753	130.00	130.00	440	1	4	1043
1033	121120241415	100.00	100.00	321	1	4	1044
1034	12112021132	60.00	60.00	35	1	4	1045
1035	121120241419	40.00	40.00	281	1	4	1046
1036	121120241512	30.00	30.00	389	1	4	1047
1037	121120241121	180.00	180.00	240	1	4	1048
1038	121120241414	10.00	10.00	335	1	4	1049
1039	1211202412010	270.00	270.00	375	1	4	1050
1040	121120241010	100.00	100.00	90	1	4	1051
1041	1211202141003	75.00	75.00	341	1	4	1052
1042	121120241054	70.00	70.00	279	1	4	1053
1043	121120241213	160.00	160.00	98	1	4	1054
1044	12112021806	85.00	85.00	409	1	4	1055
1045	12112021807	80.00	80.00	428	1	4	1056
1262	251120241417	160.00	160.00	98	1	4	1273
1046	12112021808	20.00	20.00	401	1	4	1057
1047	CP201120241808	1400.00	1400.00	441	1	4	1058
1048	131120241810	70.00	70.00	46	1	4	1059
1049	131120241811	110.00	110.00	423	1	4	1060
1050	131120241813	60.00	60.00	279	1	4	1061
1051	131120241412	115.00	115.00	343	1	4	1062
1052	131120241236	20.00	20.00	43	1	4	1063
1053	CP201120241816	85.00	85.00	442	1	4	1064
1218	CP261120241925	150.00	150.00	512	1	4	1229
1229	CP261120242014	60.00	60.00	516	1	4	1240
1237	221120241522	5.00	5.00	184	1	4	1248
1245	231120241522	52.00	52.00	397	1	4	1256
1252	CP271120241637	120.00	120.00	526	1	4	1263
1059	CP201120241817	280.00	280.00	448	1	4	1070
1259	251120241414	50.00	50.00	510	1	4	1270
1263	251120241418	40.00	40.00	441	1	4	1274
1266	CP271120241709	120.00	120.00	530	1	4	1277
1269	CP271120241714	120.00	120.00	533	1	4	1280
1278	CP021220241858	100.00	100.00	542	1	4	1289
1067	CP201120241818	40.00	40.00	456	1	4	1078
1068	CP201120241819	140.00	140.00	457	1	4	1079
1069	141120241201	285.00	285.00	205	1	4	1080
1070	141120241202	280.00	280.00	129	1	4	1081
1071	CP201120241826	280.00	280.00	458	1	4	1082
1072	141120241206	500.00	500.00	364	1	4	1083
1073	CP201120241835	460.00	460.00	459	1	4	1084
1074	141120241715	80.00	80.00	323	1	4	1085
1075	CP201120241841	140.00	140.00	460	1	4	1086
1076	141120241742	80.00	80.00	279	1	4	1087
1077	141120241750	85.00	85.00	409	1	4	1088
1078	141120241301	160.00	160.00	98	1	4	1089
1079	141120241410	40.00	40.00	441	1	4	1090
1080	141120241413	80.00	80.00	320	1	4	1091
1081	141120241847	40.00	40.00	41	1	4	1092
1082	141020241002	285.00	285.00	205	1	4	1093
1083	141120241003	30.00	30.00	261	1	4	1094
1084	14112024136	5.00	5.00	184	1	4	1095
1085	CP201120241934	240.00	240.00	461	1	4	1096
1086	141120241419	220.00	220.00	461	1	4	1097
1087	151120241010	10.00	10.00	389	1	4	1098
1088	CP201120241944	140.00	140.00	462	1	4	1099
1089	270920241715	60.00	60.00	462	1	4	1100
1090	141020241412	70.00	70.00	462	1	4	1101
1091	CP201120241947	140.00	140.00	463	1	4	1102
1092	151120241011	140.00	140.00	463	1	4	1103
1093	CP201120241949	140.00	140.00	464	1	4	1104
1094	151120241013	15.00	15.00	31	1	4	1105
1095	151120241014	280.00	280.00	340	1	4	1106
1096	151120241412	800.00	800.00	150	1	4	1107
1097	CP201120241951	750.00	750.00	465	1	4	1108
1098	171120241001	80.00	80.00	362	1	4	1109
1099	171120241002	700.00	700.00	420	1	4	1110
1100	CP211120241405	130.00	130.00	466	1	4	1111
1101	CP211120241406	800.00	800.00	467	1	4	1112
1102	171120241003	100.00	100.00	149	1	4	1113
1103	171120241005	70.00	70.00	386	1	4	1114
1104	171120241701	70.00	70.00	231	1	4	1115
1105	171120241402	30.00	30.00	233	1	4	1116
1106	171120241406	55.00	55.00	399	1	4	1117
1107	171120241202	220.00	220.00	234	1	4	1118
1108	CP211120241422	550.00	550.00	468	1	4	1119
1109	CP211120241424	150.00	150.00	469	1	4	1120
1110	1811202401202	150.00	150.00	338	1	4	1121
1111	1811202401203	150.00	150.00	56	1	4	1122
1112	181120241206	75.00	75.00	306	1	4	1123
1113	CP211120241911	135.00	135.00	470	1	4	1124
1114	181120241513	40.00	40.00	435	1	4	1125
1115	1811202401209	50.00	50.00	18	1	4	1126
1116	181120241208	50.00	50.00	346	1	4	1127
1117	CP211120241915	280.00	280.00	471	1	4	1128
1118	18102024178	50.00	50.00	167	1	4	1129
1119	181120241202	70.00	70.00	279	1	4	1130
1120	181120241503	75.00	75.00	400	1	4	1131
1121	181120241402	65.00	65.00	114	1	4	1132
1122	CP211120241934	140.00	140.00	472	1	4	1133
1280	261120241413	30.00	30.00	483	1	4	1291
1282	261120241415	40.00	40.00	441	1	4	1293
1284	CP021220241921	150.00	150.00	543	1	4	1295
1286	271120241413	50.00	50.00	321	1	4	1297
1288	271120241415	20.00	20.00	515	1	4	1299
1290	271120241417	130.00	130.00	440	1	4	1301
1129	CP211120241935	35.00	35.00	479	1	4	1140
1130	181120241508	85.00	85.00	409	1	4	1141
1291	CP021220241936	130.00	130.00	544	1	4	1302
1131	181120241605	160.00	160.00	98	1	4	1142
1132	181120241207	40.00	40.00	441	1	4	1143
1133	CP211120241938	380.00	380.00	480	1	4	1144
1134	CP211120241941	60.00	60.00	481	1	4	1145
1135	CP211120241942	120.00	120.00	482	1	4	1146
1136	191120240102	120.00	120.00	288	1	4	1147
1137	191120240103	30.00	30.00	142	1	4	1148
1138	CP211120241948	1050.00	1050.00	483	1	4	1149
1219	CP261120241926	150.00	150.00	513	1	4	1230
1140	CP211120241952	140.00	140.00	485	1	4	1151
1230	CP261120242016	120.00	120.00	517	1	4	1241
1142	CP211120241959	80.00	80.00	487	1	4	1153
1143	191120240114	60.00	60.00	279	1	4	1154
1144	191120241502	160.00	160.00	98	1	4	1155
1145	19112024035	20.00	20.00	401	1	4	1156
1146	191120241603	100.00	100.00	338	1	4	1157
1147	081020241306	20.00	20.00	183	1	4	1158
1148	110920241318	20.00	20.00	183	1	4	1159
1149	110920241411	70.00	70.00	46	1	4	1160
1150	151120241354	45.00	45.00	417	1	4	1161
1151	151120241355	50.00	50.00	380	1	4	1162
1152	CP261120241411	280.00	280.00	488	1	4	1163
1153	1511202413561	70.00	70.00	299	1	4	1164
1154	151120241358	100.00	100.00	295	1	4	1165
1155	151120241359	70.00	70.00	348	1	4	1166
1156	151120241401	167.00	167.00	223	1	4	1167
1157	CP261120241441	501.00	501.00	489	1	4	1168
1158	151120241402	150.00	150.00	363	1	4	1169
1159	CP261120241444	250.00	250.00	490	1	4	1170
1160	151120241404	160.00	160.00	98	1	4	1171
1161	151120241405	40.00	40.00	441	1	4	1172
1162	151120241406	85.00	85.00	409	1	4	1173
1163	151120241407	75.00	75.00	339	1	4	1174
1164	151120241419	45.00	45.00	411	1	4	1175
1165	151120241410	45.00	45.00	347	1	4	1176
1166	151120241411	200.00	200.00	188	1	4	1177
1167	151120241413	45.00	45.00	140	1	4	1178
1168	151120241414	75.00	75.00	390	1	4	1179
1169	70	70.00	70.00	324	1	4	1180
1170	CP261120241609	1140.00	1140.00	491	1	4	1181
1171	151120241418	75.00	75.00	309	1	4	1182
1172	151120241420	125.00	125.00	376	1	4	1183
1173	151120242010	280.00	280.00	431	1	4	1184
1174	151120241423	550.00	550.00	315	1	4	1185
1175	151120241424	55.00	55.00	227	1	4	1186
1176	151120241426	85.00	85.00	239	1	4	1187
1177	CP261120241645	550.00	550.00	492	1	4	1188
1178	151120241428	40.00	40.00	302	1	4	1189
1179	151120241429	110.00	110.00	303	1	4	1190
1180	151120241430	40.00	40.00	91	1	4	1191
1181	151120241431	90.00	90.00	383	1	4	1192
1182	CP261120241653	140.00	140.00	493	1	4	1193
1183	CP261120241701	250.00	250.00	494	1	4	1194
1184	151120241433	500.00	500.00	420	1	4	1195
1185	151120241435	90.00	90.00	384	1	4	1196
1186	151120241436	20.00	20.00	314	1	4	1197
1187	CP261120241728	360.00	360.00	495	1	4	1198
1188	161020241732	120.00	120.00	495	1	4	1199
1189	011120241735	220.00	220.00	495	1	4	1200
1190	161120241413	25.00	25.00	466	1	4	1201
1191	161120241414	65.00	65.00	429	1	4	1202
1192	161120241415	70.00	70.00	279	1	4	1203
1193	161120241416	100.00	100.00	410	1	4	1204
1194	CP261120241809	140.00	140.00	496	1	4	1205
1195	CP261120241810	150.00	150.00	497	1	4	1206
1196	161120241412	100.00	100.00	61	1	4	1207
1197	161120241536	50.00	50.00	278	1	4	1208
1198	161120241510	40.00	40.00	388	1	4	1209
1199	161120241814	140.00	140.00	310	1	4	1210
1200	CP261120241820	165.00	165.00	498	1	4	1211
1238	22112024153	50.00	50.00	79	1	4	1249
1246	231120241523	50.00	50.00	278	1	4	1257
1253	241120241412	160.00	160.00	98	1	4	1264
1260	251120241415	60.00	60.00	26	1	4	1271
1264	251120241301	6.00	6.00	434	1	4	1275
1206	CP261120241821	150.00	150.00	504	1	4	1217
1267	CP271120241711	120.00	120.00	531	1	4	1278
1270	CP271120241716	60.00	60.00	534	1	4	1281
1276	CP271120241722	120.00	120.00	540	1	4	1287
1279	261120241412	5.00	5.00	184	1	4	1290
1281	261120241414	160.00	160.00	98	1	4	1292
1283	261120241416	60.00	60.00	279	1	4	1294
1285	271120241412	50.00	50.00	194	1	4	1296
1287	271120241414	30.00	30.00	389	1	4	1298
1289	271120241416	10.00	10.00	335	1	4	1300
1292	CP021220241937	75.00	75.00	545	1	4	1303
1294	CP021220241941	230.00	230.00	547	1	4	1305
1295	271120241418	75.00	75.00	371	1	4	1306
1296	271120241301	60.00	60.00	279	1	4	1307
1297	271120241302	30.00	30.00	483	1	4	1308
1298	271120241304	160.00	160.00	506	1	4	1309
1299	271120241702	40.00	40.00	441	1	4	1310
1300	271120241502	100.00	100.00	311	1	4	1311
1301	271120241506	380.00	380.00	480	1	4	1312
1302	271120241325	6.00	6.00	434	1	4	1313
1303	271120241656	140.00	140.00	528	1	4	1314
1304	2811202412	160.00	160.00	506	1	4	1315
1305	281120241639	40.00	40.00	441	1	4	1316
1306	281120241640	140.00	140.00	519	1	4	1317
1307	281120241642	290.00	290.00	375	1	4	1318
1308	CP021220242001	140.00	140.00	548	1	4	1319
1309	291120241413	50.00	50.00	359	1	4	1320
1310	CP041220241630	250.00	250.00	549	1	4	1321
1314	CP041220241631	150.00	150.00	553	1	4	1325
1315	291120241412	20.00	20.00	423	1	4	1326
1316	291120241414	70.00	70.00	525	1	4	1327
1317	291120241416	60.00	60.00	279	1	4	1328
1318	291120241417	160.00	160.00	506	1	4	1329
1319	291120241315	40.00	40.00	441	1	4	1330
1320	291120241602	65.00	65.00	429	1	4	1331
1321	291120241503	5.00	5.00	184	1	4	1332
1322	291120241508	45.00	45.00	417	1	4	1333
1323	CP041220241649	80.00	80.00	554	1	4	1334
1324	301120241412	140.00	140.00	488	1	4	1335
1325	301120241413	75.00	75.00	390	1	4	1336
1326	301120241414	167.00	167.00	223	\N	4	1337
1327	301120241416	100.00	100.00	295	1	4	1338
1328	301120241417	70.00	70.00	348	1	4	1339
1329	301120241402	45.00	45.00	411	1	4	1340
1330	301120241203	100.00	100.00	149	1	4	1341
1331	CP041220241700	140.00	140.00	555	1	4	1342
1332	CP041220241701	140.00	140.00	556	1	4	1343
1333	301120241301	90.00	90.00	230	1	4	1344
1334	301120241302	50.00	50.00	347	1	4	1345
1335	CP041220241708	360.00	360.00	557	1	4	1346
1336	CP041220241710	120.00	120.00	558	1	4	1347
1337	301120241304	10.00	10.00	281	1	4	1348
1338	301120241306	50.00	50.00	91	1	4	1349
1339	301120241309	50.00	50.00	61	1	4	1350
1340	301120241419	93.00	93.00	471	1	4	1351
1341	301120211203	75.00	75.00	513	1	4	1352
1342	CP041220241740	130.00	130.00	559	1	4	1353
1343	CP041220241741	140.00	140.00	560	1	4	1354
1344	CP041220241742	140.00	140.00	561	1	4	1355
1345	301120241308	70.00	70.00	497	1	4	1356
1346	301120241310	30.00	30.00	483	1	4	1357
1347	301120211312	180.00	180.00	279	1	4	1358
1348	301120241314	50.00	50.00	469	1	4	1359
1349	301120241315	50.00	50.00	278	1	4	1360
1350	301120241206	75.00	75.00	512	1	4	1361
1351	301120241207	6.00	6.00	434	1	4	1362
1352	CP041220241752	35.00	35.00	562	1	4	1363
1353	CP041220241753	70.00	70.00	563	1	4	1364
1354	301120241506	60.00	60.00	540	1	4	1365
1355	301120241803	30.00	30.00	534	1	4	1366
1356	301120241509	60.00	60.00	533	1	4	1367
1357	301120241806	60.00	60.00	531	1	4	1368
1358	CP051220241815	2600.00	2600.00	564	1	4	1369
1359	060620241521	50.00	50.00	564	1	4	1370
1360	190620241412	50.00	50.00	564	1	4	1371
1361	170720241545	50.00	50.00	564	1	4	1372
1362	030820241415	50.00	50.00	564	1	4	1373
1363	170920241836	50.00	50.00	564	1	4	1374
1364	081120241440	50.00	50.00	564	1	4	1375
1365	241120241756	50.00	50.00	564	1	4	1376
1366	01120241412	120.00	120.00	376	1	4	1377
1367	01120241413	45.00	45.00	380	1	4	1378
1368	01120241411	50.00	50.00	84	1	4	1379
1369	01120241414	10.00	10.00	278	1	4	1380
1370	01120241415	40.00	40.00	41	1	4	1381
1371	CP051220241825	150.00	150.00	565	1	4	1382
1379	CP051220241826	360.00	360.00	573	1	4	1390
1380	CP051220241827	800.00	800.00	574	1	4	1391
1381	01120241416	50.00	50.00	320	1	4	1392
1382	011220241503	125.00	125.00	490	1	4	1393
1383	01120241503	160.00	160.00	506	1	4	1394
1384	011220241703	40.00	40.00	441	1	4	1395
1385	011220241736	40.00	40.00	72	1	4	1396
1386	01120241536	125.00	125.00	302	1	4	1397
1387	021220241415	55.00	55.00	399	1	4	1398
1388	CP051220241837	150.00	150.00	575	1	4	1399
1389	CP051220241838	140.00	140.00	576	1	4	1400
1390	021220241201	40.00	40.00	296	1	4	1401
1391	021220241402	50.00	50.00	542	1	4	1402
1392	021220241206	30.00	30.00	483	1	4	1403
1393	021220241413	5.00	5.00	184	1	4	1404
1394	021220241805	160.00	160.00	506	1	4	1405
1395	021220241830	40.00	40.00	441	1	4	1406
1396	021220241703	50.00	50.00	279	1	4	1407
1397	021220241512	340.00	340.00	400	1	4	1408
1398	CP051220241915	240.00	240.00	577	1	4	1409
1399	021220241021	50.00	50.00	84	1	4	1410
1400	021220241003	20.00	20.00	401	1	4	1411
1401	021120241004	30.00	30.00	237	1	4	1412
1402	021220241005	53.00	53.00	397	1	4	1413
1403	021220241008	50.00	50.00	389	1	4	1414
1404	021220241004	6.00	6.00	434	1	4	1415
1405	021220241411	60.00	60.00	494	1	4	1416
1406	CP051220241926	360.00	360.00	578	1	4	1417
1412	CP051220241927	130.00	130.00	584	1	4	1423
1413	CP051220241939	280.00	280.00	585	1	4	1424
1417	CP051220241940	160.00	160.00	589	1	4	1428
1432	CP051220241941	160.00	160.00	604	1	4	1443
1435	031220241010	160.00	160.00	589	1	4	1446
1436	CP051220241942	150.00	150.00	607	1	4	1447
1437	CP051220241943	70.00	70.00	608	1	4	1448
1438	CP051220241944	510.00	510.00	609	1	4	1449
1439	CP051220241945	1000.00	1000.00	610	1	4	1450
1440	031220241011	90.00	90.00	383	1	4	1451
1441	031220241013	120.00	120.00	317	1	4	1452
1442	031220241014	80.00	80.00	226	1	4	1453
1443	031220241016	75.00	75.00	138	1	4	1454
1444	031220242012	54.00	54.00	504	1	4	1455
1445	031220241403	160.00	160.00	506	1	4	1456
1446	031220241503	40.00	40.00	441	1	4	1457
1447	041220241010	40.00	40.00	435	1	4	1458
1448	041220241011	5.00	5.00	184	1	4	1459
1449	041220241012	100.00	100.00	459	1	4	1460
1450	041220241013	145.00	145.00	301	1	4	1461
1451	041220241014	70.00	70.00	496	1	4	1462
1452	041220241015	50.00	50.00	279	1	4	1463
1453	041220241016	30.00	30.00	483	1	4	1464
1454	041220241017	160.00	160.00	506	1	4	1465
1455	041220241413	40.00	40.00	441	1	4	1466
1456	CP051220241959	140.00	140.00	611	1	4	1467
1460	CP051220242000	60.00	60.00	615	1	4	1471
1465	CP051220242001	90.00	90.00	620	1	4	1476
1466	CP051220242003	50.00	50.00	621	1	4	1477
1467	CP051220242005	150.00	150.00	622	1	4	1478
1470	CP051220242006	152.00	152.00	625	1	4	1481
1471	CP051220242007	120.00	120.00	626	1	4	1482
1472	041220241020	35.00	35.00	561	1	4	1483
1473	041220241410	85.00	85.00	189	1	4	1484
1474	041220241105	40.00	40.00	127	1	4	1485
1475	CP051220242011	140.00	140.00	627	1	4	1486
1476	CP051220242012	120.00	120.00	628	1	4	1487
1477	CP051220242013	510.00	510.00	629	1	4	1488
\.


--
-- Data for Name: fintech_address; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_address" ("id", "address_type", "address", "city", "country_id", "user_id") FROM stdin;
\.


--
-- Data for Name: fintech_category; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_category" ("id", "uid", "name", "created_at", "updated_at", "category_type_id") FROM stdin;
1	3c812b7e-5cfd-46dc-b86e-da80c294d12d	Ventas	2024-09-11 02:54:04.060948+00	2024-09-11 02:54:04.06096+00	4
2	9170ab22-19d9-4fb6-800f-e27512851d1e	Créditos	2024-09-11 02:54:16.131838+00	2024-09-11 02:54:16.131848+00	4
3	44236322-b067-4efb-88c4-d8ef18242a71	Servicios	2024-09-11 02:54:32.961984+00	2024-09-11 02:54:32.962019+00	4
4	44ce9c3c-552c-42e4-a288-a66a489a9bfd	Otros ingresos operativos	2024-09-11 02:54:54.271003+00	2024-09-11 02:54:54.271018+00	4
5	1e0642c5-1c4e-4207-af81-1025efe2475d	Costo de ventas	2024-09-11 02:55:22.085592+00	2024-09-11 02:55:22.085607+00	5
6	ce737ba3-ad9e-4351-9e3e-ce1ba8130659	Gastos de ventas	2024-09-11 02:55:36.690601+00	2024-09-11 02:55:36.690615+00	5
7	def41880-32ef-43a2-a3c3-d65a510ff465	Gastos administrativos	2024-09-11 02:56:02.93995+00	2024-09-11 02:56:02.939965+00	5
8	58b89dff-478c-4231-91ec-14e93ebc1dcb	Depreciación	2024-09-11 02:56:17.404972+00	2024-09-11 02:56:17.404987+00	5
9	6df52bec-89b0-4677-bc7f-b7aae785e808	Amortización	2024-09-11 02:56:31.040722+00	2024-09-11 02:56:31.040736+00	5
10	e8e6b990-5d68-405a-a33f-4c7669651718	Ingresos financieros	2024-09-11 02:57:14.091508+00	2024-09-11 02:57:14.091527+00	6
11	483d42ac-6b6c-40c8-a961-33fcd3e7835c	Ganancias en venta de activos	2024-09-11 02:57:34.952289+00	2024-09-11 02:57:34.952301+00	6
12	c3be591c-9193-462c-b133-e03fbc7dc814	Gastos de actividad	2024-09-11 05:43:53.086258+00	2024-09-11 05:44:08.733753+00	5
\.


--
-- Data for Name: fintech_categorytype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_categorytype" ("id", "uid", "name", "description") FROM stdin;
1	b39d9d0b-ad5b-4933-b521-449de4716080	Activos	
2	b935243e-e87f-46f9-8a0b-fd8e895b5cbe	Pasivos	
3	8fe9cd5a-eb93-4831-bb20-48c6d202dd9b	Patrimonio Neto	
4	26c4e693-361a-4964-a5a5-54a9234372ff	Ingresos Operativos	
5	17f1ad39-eec9-400e-ab03-8a47cd7f68d9	Gastos Operativos	
6	dbc2cd2e-1de2-4584-aed7-b11426d50876	Ingresos no Operativos	
\.


--
-- Data for Name: fintech_country; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_country" ("id", "name", "utc_offset") FROM stdin;
1	Colombia	-5
\.


--
-- Data for Name: fintech_credit; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_credit" ("id", "uid", "state", "cost", "price", "earnings", "first_date_payment", "second_date_payment", "credit_days", "description", "interest", "refinancing", "total_abonos", "pending_amount", "installment_number", "installment_value", "is_in_default", "created_at", "updated_at", "morosidad_level", "currency_id", "payment_id", "periodicity_id", "registered_by_id", "subcategory_id", "user_id", "seller_id") FROM stdin;
21	621107a6-ad90-4449-a12b-0bda9936235b	pending	200.00	300.00	100.00	2024-08-15	2024-08-31	45		0.33	\N	300.00	0.00	3	100.00	t	2024-08-02 00:21:08+00	2024-11-01 22:31:01.836495+00	recurrent_default	1	4	3	3	2	16	\N
4	bad624e3-3f2f-4d8b-a103-fcc2fa5e1a8e	pending	100.00	140.00	40.00	2024-09-01	2024-09-15	30		0.40	\N	90.00	50.00	2	70.00	f	2024-08-02 21:03:14+00	2024-09-11 21:16:15.141292+00	on_time	1	4	3	3	2	7	\N
505	5168f062-5253-4304-a1ca-da54f734047b	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-11-16 23:21:06+00	2024-11-26 23:22:34.900268+00	on_time	1	4	3	3	2	209	1
2	1ce6b026-3e2f-42c1-8422-b1406dfced3f	pending	150.00	270.00	120.00	2024-09-15	2024-09-30	30		0.80	\N	175.00	95.00	2	135.00	f	2024-09-11 19:43:24+00	2024-10-08 23:43:25.098216+00	moderate_default	1	4	3	3	2	5	\N
28	2eb60fb9-a7cc-4c01-ad7c-6e53fe82b4d8	pending	100.00	140.00	40.00	2024-08-16	2024-08-31	30		0.40	\N	55.00	85.00	2	70.00	t	2024-08-03 01:19:45+00	2024-09-20 22:36:40.449164+00	mild_default	1	4	3	3	2	23	\N
17	e1930381-c923-4478-9317-50baa0888f73	completed	225.00	300.00	75.00	2024-08-03	2024-08-30	45		0.22	\N	300.00	0.00	3	100.00	t	2024-07-31 23:53:24+00	2024-11-26 22:24:25.288086+00	recurrent_default	1	4	3	3	2	12	\N
8	7fd45bb2-f7cd-418c-b952-a5cdca4964bc	pending	100.00	160.00	60.00	2024-09-15	2024-09-30	60		0.30	\N	156.00	4.00	4	40.00	t	2024-09-09 23:35:35+00	2024-11-27 01:12:20.287779+00	mild_default	1	4	3	1	2	1	\N
30	480748d0-c275-4cd8-a0af-90e2cdfaa853	pending	60.00	100.00	40.00	2024-09-30	2024-10-15	30		0.67	\N	40.00	60.00	2	50.00	t	2024-09-12 18:51:19+00	2024-10-19 23:16:41.425059+00	mild_default	1	4	3	3	2	18	\N
9	b0806c7b-8326-4aa3-bb51-67ba15ed3eb8	pending	50.00	90.00	40.00	2024-09-15	2024-09-30	30		0.80	\N	30.00	60.00	2	45.00	t	2024-09-09 23:36:25+00	2024-10-08 23:38:55.886536+00	mild_default	1	4	3	1	2	2	\N
18	b865d0fc-b262-46cb-b636-49bf33475460	pending	300.00	525.00	225.00	2024-08-16	2024-09-01	45		0.50	\N	505.00	20.00	3	175.00	t	2024-07-31 23:55:44+00	2024-11-22 00:12:47.094868+00	recurrent_default	1	4	3	3	2	13	\N
38	ab6eeb84-5ba8-4649-b075-a8c3bba65c48	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	90.00	50.00	2	70.00	f	2024-09-11 21:20:51+00	2024-09-15 00:15:01.924294+00	on_time	1	4	3	3	2	32	1
516	799f2c48-23b3-4b78-aff9-80784871d5e3	pending	50.00	60.00	10.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	60.00	2	30.00	f	2024-11-22 01:13:26+00	2024-11-27 01:14:34.196227+00	on_time	1	4	3	3	2	256	1
19	d138852f-9401-42a4-841d-04245731a37c	pending	50.00	80.00	30.00	2024-08-31	2024-09-30	60		0.30	\N	2.50	77.50	2	40.00	f	2024-08-01 00:07:08+00	2024-09-14 23:53:04.912924+00	on_time	1	4	4	3	2	14	\N
3	9e4f312f-f96d-4a85-a7f3-1f4fbd003efa	pending	600.00	1100.00	500.00	2024-08-28	2024-08-29	60		0.42	\N	835.00	265.00	4	275.00	t	2024-08-15 19:45:52+00	2024-11-01 22:03:58.130961+00	mild_default	1	4	3	3	2	6	\N
35	1b8afdb8-e915-4246-adcf-6336fa7126ad	pending	100.00	150.00	50.00	2024-09-15	2024-09-30	30		0.50	\N	60.00	90.00	2	75.00	t	2024-09-12 21:10:53+00	2024-11-20 22:54:52.565552+00	recurrent_default	1	4	3	3	2	29	1
41	7b11691f-ebc2-416a-a143-4ef4df35b1ba	pending	50.00	80.00	30.00	2024-09-15	2024-09-30	30		0.60	\N	80.00	0.00	2	40.00	t	2024-09-10 21:26:06+00	2024-12-05 23:24:08.386887+00	recurrent_default	1	4	3	3	2	35	1
29	527bf700-b14a-41c3-bef8-a5a909ef86ff	pending	50.00	50.00	0.00	2024-09-30	2024-10-15	75	Camiseta	0.00	\N	10.00	40.00	5	10.00	f	2024-09-12 18:47:15+00	2024-11-12 21:49:45.443911+00	on_time	1	4	3	3	1	24	\N
42	cb31876b-c804-49ba-a618-be877199d34d	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	130.00	10.00	2	70.00	f	2024-09-10 21:28:03+00	2024-09-19 19:10:35.503852+00	on_time	1	4	3	3	2	36	1
37	1cb943d3-e630-49b6-be04-45ae0e9af190	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	60.00	80.00	2	70.00	t	2024-09-11 21:19:47+00	2024-10-19 22:49:47.415044+00	mild_default	1	4	3	3	2	31	1
5	d3149dd6-568a-4526-9c24-1283932500d7	pending	150.00	255.00	105.00	2024-09-15	2024-09-30	30		0.70	\N	285.00	-30.00	2	127.50	f	2024-09-01 21:06:56+00	2024-10-04 02:39:09.242407+00	moderate_default	1	4	3	3	2	7	\N
24	54ebbe0f-b9ea-436a-85b6-9fc0a5859357	pending	300.00	510.00	210.00	2024-08-15	2024-08-30	45		0.47	\N	501.00	9.00	3	170.00	t	2024-08-02 00:30:56+00	2024-09-17 23:31:20.122487+00	moderate_default	1	4	3	3	2	19	\N
7	f7c7954a-08d1-4fe7-b84e-bae229d5eaba	pending	200.00	300.00	100.00	2024-09-15	2024-09-30	45		0.33	\N	70.00	230.00	3	100.00	f	2024-09-02 21:18:08+00	2024-09-19 19:21:07.227134+00	on_time	1	4	3	3	2	9	\N
43	1bab7ed5-0299-44bb-bdb2-5464e5de61f2	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	60		0.20	\N	140.00	0.00	4	35.00	f	2024-09-10 21:29:20+00	2024-11-20 23:14:23.474213+00	moderate_default	1	4	3	3	2	37	1
12	166ae913-e9df-469d-a48b-08c4aebf5930	pending	200.00	300.00	100.00	2024-09-11	2024-09-25	30		0.50	\N	150.00	150.00	2	150.00	t	2024-08-21 23:57:11+00	2024-10-24 19:54:45.826763+00	mild_default	1	4	3	3	2	11	\N
39	f991994b-efce-4b0e-95f2-57a84206c5a4	pending	500.00	750.00	250.00	2024-09-15	2024-09-30	30		0.50	\N	750.00	0.00	2	375.00	f	2024-09-10 21:21:39+00	2024-10-24 23:22:18.137272+00	moderate_default	1	4	3	3	2	33	1
10	1cdb6d4a-8153-4166-9a1b-0b28736b1584	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	138.00	2.00	2	70.00	f	2024-09-09 23:37:26+00	2024-10-09 21:33:04.743628+00	moderate_default	1	4	3	1	2	3	\N
32	06de66c5-8ee5-40f3-aaa1-dab8e8da39d0	pending	10.00	50.00	40.00	2024-09-15	2024-09-30	75	Camiseta	1.60	\N	0.00	50.00	5	10.00	f	2024-09-12 21:05:53+00	2024-09-13 21:07:38.428652+00	on_time	1	4	3	3	1	26	1
40	303ade5a-8093-4883-9eda-1f75363f242a	pending	50.00	90.00	40.00	2024-09-15	2024-09-30	30		0.80	\N	90.00	0.00	2	45.00	f	2024-09-10 21:24:41+00	2024-09-27 22:41:00.42854+00	on_time	1	4	3	3	2	34	1
20	8cab9fa6-90b9-40b0-995b-9acd79d7eae5	pending	200.00	300.00	100.00	2024-08-15	2024-09-30	30		0.50	\N	300.00	0.00	2	150.00	t	2024-08-01 00:13:53+00	2024-09-25 19:04:29.339262+00	moderate_default	1	4	3	3	2	15	\N
25	49065c31-0087-4fb6-9241-cb85355dc35d	pending	500.00	600.00	100.00	2024-08-05	2024-08-07	24		0.25	\N	260.00	340.00	4	150.00	t	2024-08-03 01:08:31+00	2024-11-01 21:51:39.234827+00	recurrent_default	1	4	2	3	2	20	\N
27	0ed38888-b5d8-472a-a8f1-518e0462b4f9	pending	100.00	165.00	65.00	2024-09-04	2024-09-25	45		0.43	\N	30.00	135.00	3	55.00	t	2024-08-03 01:17:23+00	2024-09-19 19:02:59.671638+00	mild_default	1	4	3	3	2	22	\N
22	ba2b3baa-7ed0-4080-824c-3dcd1bd17f41	pending	300.00	510.00	210.00	2024-09-02	2024-09-23	45		0.47	\N	125.00	385.00	3	170.00	t	2024-08-02 00:24:34+00	2024-10-09 00:39:11.009907+00	mild_default	1	4	3	3	2	17	\N
36	e401ce66-d175-41b5-8d20-5c415427512b	pending	50.00	70.00	20.00	2024-09-15	2024-09-30	30		0.40	\N	40.00	30.00	2	35.00	t	2024-09-12 21:11:59+00	2024-10-24 19:46:29.447361+00	mild_default	1	4	3	3	2	30	1
1	8109c785-5648-4858-8a83-bafa0b9a8110	pending	100.00	152.00	52.00	2024-09-15	2024-09-30	60		0.26	\N	152.00	0.00	4	38.00	f	2024-08-31 19:32:56+00	2024-10-24 01:39:37.627373+00	moderate_default	1	4	3	3	2	4	\N
23	a4d4f05c-a78b-4e02-bedb-561f597e26a6	pending	100.00	150.00	50.00	2024-08-15	2024-09-30	30		0.50	\N	100.00	50.00	2	75.00	t	2024-08-02 00:28:50+00	2024-11-10 20:52:28.835501+00	recurrent_default	1	4	3	3	2	18	\N
16	4c242242-f1ab-491d-be1b-770d7336b250	pending	1000.00	1200.00	200.00	2024-09-05	2024-09-06	30		0.20	\N	1165.00	35.00	30	40.00	t	2024-09-04 15:37:57+00	2024-11-20 21:25:55.2922+00	recurrent_default	1	4	1	1	2	10	1
69	0103d180-687a-43a2-b011-8f18c785dd1a	pending	50.00	90.00	40.00	2024-09-15	2024-09-30	30		0.80	\N	90.00	-10.00	2	45.00	t	2024-09-03 01:26:21+00	2024-11-12 21:52:34.635548+00	moderate_default	1	4	3	3	2	59	1
47	594c2810-7b2e-4c23-9fd7-3f64471cd535	pending	100.00	150.00	50.00	2024-09-15	2024-09-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-09-06 22:52:07+00	2024-10-09 21:40:10.428192+00	moderate_default	1	4	3	3	2	41	1
34	638d612b-fd90-487c-8127-ef04bbcc76bd	pending	10.00	50.00	40.00	2024-09-15	2024-09-30	75	Camiseta	1.60	\N	50.00	0.00	5	10.00	f	2024-09-12 21:09:22+00	2024-09-21 21:03:49.811845+00	on_time	1	4	3	3	1	28	1
66	f5707845-29b9-4f5f-a7b0-2a39c9b86eff	pending	200.00	300.00	100.00	2024-09-15	2024-09-30	30		0.50	\N	70.00	230.00	2	150.00	t	2024-09-04 01:22:01+00	2024-10-09 00:22:29.790214+00	mild_default	1	4	3	3	2	58	1
64	add4d36c-c314-492d-81e8-3e65678ce691	pending	300.00	360.00	60.00	2024-09-15	2024-09-30	30		0.20	\N	360.00	0.00	2	180.00	f	2024-09-04 01:19:05+00	2024-10-08 23:50:55.103038+00	moderate_default	1	4	3	3	2	56	1
51	3ba6317a-3339-44fe-a249-0fa181991c14	pending	200.00	300.00	100.00	2024-09-15	2024-09-30	30		0.50	\N	0.00	300.00	2	150.00	f	2024-09-06 22:58:38+00	2024-09-13 22:59:31.012476+00	on_time	1	4	3	3	2	45	1
52	f7293000-7160-466a-a5f6-36daf61da284	pending	100.00	150.00	50.00	2024-09-15	2024-09-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-09-05 23:05:53+00	2024-09-13 23:06:54.422131+00	on_time	1	4	3	3	2	46	1
55	09075212-b7d2-46c4-9c91-62a66f6c9de5	pending	3000.00	4200.00	1200.00	2024-08-05	2024-08-07	35		0.34	\N	4160.00	40.00	35	120.00	t	2024-08-04 23:29:45+00	2024-10-24 22:02:56.528862+00	recurrent_default	1	4	1	3	2	49	1
63	d77b722d-2189-4bfc-b10a-d97de42b0c42	pending	200.00	260.00	60.00	2024-09-15	2024-09-30	30		0.30	\N	260.00	0.00	2	130.00	f	2024-09-04 01:17:15+00	2024-10-24 18:24:23.029296+00	moderate_default	1	4	3	3	2	55	1
44	fb8b27e8-19b7-4f0e-bd6c-587d5a273d93	pending	100.00	200.00	100.00	2024-09-15	2024-09-30	60		0.50	\N	180.00	20.00	4	50.00	t	2024-09-08 22:42:39+00	2024-10-29 01:12:13.034703+00	moderate_default	1	4	3	3	2	38	1
517	d98ded6c-41b9-4190-8414-b54ffd005a48	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	120.00	2	60.00	f	2024-11-22 01:14:34+00	2024-11-27 01:16:03.879696+00	on_time	1	4	3	3	2	257	1
45	6ce1de70-f2f8-4c11-83f8-96721af72b8f	pending	50.00	90.00	40.00	2024-09-15	2024-09-30	30		0.80	\N	90.00	0.00	2	45.00	f	2024-09-08 22:43:45+00	2024-09-17 22:32:50.599541+00	on_time	1	4	3	3	2	39	1
59	ebc215b6-6ae2-4641-bc67-2ab66417aec0	pending	50.00	100.00	50.00	2024-09-15	2024-09-30	30		1.00	\N	0.00	100.00	2	50.00	f	2024-09-05 00:56:41+00	2024-09-14 00:57:56.796553+00	on_time	1	4	3	3	2	52	1
60	f28671dc-0e0d-4b24-a3be-43103c06ae1d	pending	300.00	480.00	180.00	2024-09-15	2024-09-30	30		0.60	\N	0.00	480.00	2	240.00	f	2024-09-05 00:58:43+00	2024-09-14 01:01:44.938553+00	on_time	1	4	3	3	2	53	1
529	6fe86f39-dfd2-4275-9d71-76c9a3be40ff	pending	300.00	500.00	200.00	2024-11-30	2024-12-15	60		0.33	\N	0.00	500.00	4	125.00	f	2024-11-25 22:07:18+00	2024-11-27 22:08:53.487806+00	on_time	1	4	3	3	2	74	1
74	30869f9f-1022-4576-a67f-b615e82e0249	pending	100.00	165.00	65.00	2024-09-15	2024-09-30	45		0.43	\N	100.00	65.00	3	55.00	t	2024-09-03 01:31:40+00	2024-10-24 22:36:00.649758+00	mild_default	1	4	3	3	2	62	1
75	d8090277-80df-45fa-b35e-5238c48f307c	pending	150.00	255.00	105.00	2024-09-15	2024-09-30	45		0.47	\N	245.00	10.00	3	85.00	f	2024-09-03 01:32:48+00	2024-10-24 18:27:52.232101+00	moderate_default	1	4	3	3	2	63	1
77	f37d398b-3a10-440d-9eca-6792e793c93c	pending	100.00	150.00	50.00	2024-09-15	2024-09-30	30		0.50	\N	75.00	75.00	2	75.00	f	2024-09-03 01:36:14+00	2024-09-19 18:58:08.340436+00	on_time	1	4	3	3	2	65	1
76	63c0c41a-0cc5-462e-b760-c56cd708135a	pending	200.00	300.00	100.00	2024-09-15	2024-09-30	30		0.50	\N	300.00	0.00	2	150.00	t	2024-09-03 01:34:19+00	2024-11-02 00:43:08.522922+00	mild_default	1	4	3	3	2	64	1
65	13b9987c-6493-4138-b465-55c0cdb73959	pending	400.00	600.00	200.00	2024-09-15	2024-09-30	30		0.50	\N	600.00	0.00	2	300.00	f	2024-09-04 01:21:09+00	2024-10-24 19:51:20.823495+00	moderate_default	1	4	3	3	2	57	1
67	8a690d96-cfb8-4a15-b6a5-f57ad78db5b5	pending	100.00	165.00	65.00	2024-09-15	2024-09-30	45		0.43	\N	0.00	165.00	3	55.00	f	2024-09-04 01:23:03+00	2024-09-14 01:23:53.715263+00	on_time	1	4	3	3	2	23	1
68	42411f60-e441-47d0-9ae5-c4658b1d404c	pending	200.00	300.00	100.00	2024-09-15	2024-09-30	45		0.33	\N	0.00	300.00	3	100.00	f	2024-09-03 01:25:41+00	2024-09-14 01:26:10.121524+00	on_time	1	4	3	3	2	9	1
71	0e94f246-a90c-4573-97db-246f1705abce	pending	50.00	90.00	40.00	2024-09-15	2024-09-30	30		0.80	\N	0.00	90.00	2	45.00	f	2024-09-03 01:28:10+00	2024-09-14 01:28:36.335786+00	on_time	1	4	3	3	2	29	1
56	9d896651-30ee-45ba-ac4b-726abb6cd91b	pending	200.00	360.00	160.00	2024-08-15	2024-09-30	45		0.53	\N	260.00	100.00	3	120.00	t	2024-08-06 23:37:59+00	2024-11-22 00:07:58.581671+00	recurrent_default	1	4	3	3	2	50	1
61	439f2a00-53ac-493e-9de7-624dd3750bef	pending	100.00	150.00	50.00	2024-09-15	2024-09-30	30		0.50	\N	150.00	0.00	2	75.00	t	2024-09-05 01:02:08+00	2024-12-04 22:14:44.286784+00	recurrent_default	1	4	3	3	2	15	1
58	79b7b804-be56-4e06-b8d3-94927472b460	pending	10.00	50.00	40.00	2024-09-15	2024-09-30	75	Camiseta	1.60	\N	20.00	30.00	5	10.00	f	2024-09-03 00:47:50+00	2024-10-19 23:25:04.519545+00	moderate_default	1	4	3	3	1	29	1
49	0577fdb9-8094-467d-8ff1-cdad7f08d212	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	70.00	70.00	2	70.00	f	2024-09-06 22:56:24+00	2024-10-04 02:47:30.745848+00	moderate_default	1	4	3	3	2	43	1
48	90102a8d-67d9-4ec4-8b15-dced14800db1	pending	50.00	80.00	30.00	2024-09-15	2024-09-30	30		0.60	\N	80.00	0.00	2	40.00	f	2024-09-06 22:53:58+00	2024-10-08 23:54:11.304913+00	moderate_default	1	4	3	3	2	42	1
78	da74c3f2-5386-4ced-b2ae-dd15945431bb	pending	200.00	315.00	115.00	2024-09-15	2024-09-30	45		0.38	\N	220.00	95.00	3	105.00	t	2024-09-13 17:55:26+00	2024-11-09 00:46:22.817085+00	mild_default	1	4	3	3	2	66	1
46	cc199d5a-4a52-4625-b535-b4d85b79e2cc	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	140.00	0.00	2	70.00	t	2024-09-07 22:47:04+00	2024-11-23 19:11:40.9863+00	recurrent_default	1	4	3	3	2	40	1
72	f83adecf-a681-409f-88a7-8d008b8c93f3	pending	150.00	255.00	105.00	2024-09-15	2024-09-30	45		0.47	\N	60.00	195.00	3	85.00	t	2024-09-03 01:28:40+00	2024-12-05 23:33:17.384982+00	recurrent_default	1	4	3	3	2	60	1
33	695d9fa8-ca0b-4a53-99f5-423528c6b515	pending	10.00	50.00	40.00	2024-09-15	2024-09-30	75	Camiseta	1.60	\N	20.00	30.00	5	10.00	f	2024-09-12 21:08:15+00	2024-09-27 22:27:31.743415+00	on_time	1	4	3	3	1	27	1
80	fde25c2d-3701-469c-aed3-46c013dd01d1	pending	150.00	270.00	120.00	2024-08-15	2024-08-30	45		0.53	\N	0.00	270.00	3	90.00	t	2024-08-09 18:00:50+00	2024-09-14 18:01:54.314256+00	severe_default	1	4	3	3	2	68	1
62	18c67617-43df-4daa-8d5e-ccbd3d62edf7	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	140.00	0.00	2	70.00	f	2024-09-05 01:02:49+00	2024-10-04 02:38:15.950169+00	moderate_default	1	4	3	3	2	54	1
54	dc3f2c31-4756-4a50-9d43-0fb838beb574	pending	100.00	130.00	30.00	2024-09-15	2024-09-30	30		0.30	\N	130.00	0.00	2	65.00	f	2024-09-05 23:08:41+00	2024-09-27 22:35:36.440124+00	on_time	1	4	3	3	2	48	1
93	fa0252e9-05ea-4580-9fbc-5ceae707d36b	pending	100.00	140.00	40.00	2024-08-30	2024-09-15	30		0.40	\N	90.00	50.00	2	70.00	t	2024-08-16 23:38:46+00	2024-11-12 21:19:58.941158+00	recurrent_default	1	4	3	3	2	32	1
95	e70477f3-b1df-4dab-b4f2-4afd2d2c912e	to_solve	100.00	140.00	40.00	2024-09-30	2024-10-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-09-13 23:44:28+00	2024-11-12 18:29:11.226672+00	on_time	1	4	3	3	2	79	1
103	0fc64db7-491a-4f0c-9d75-4374c2b3d507	pending	150.00	270.00	120.00	2024-09-30	2024-10-15	45		0.53	\N	0.00	270.00	7	38.57	f	2024-09-13 23:46:54+00	2024-11-12 21:52:00.635038+00	on_time	1	4	2	3	2	232	1
507	a8b8382d-a753-461b-a3bc-35ade781a6b4	pending	50.00	70.00	20.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	70.00	1	70.00	f	2024-11-21 00:05:12+00	2024-11-27 00:06:10.381546+00	on_time	1	4	4	3	2	252	1
112	f711f78e-9773-47bd-b84b-d8e7da72cde3	pending	100.00	150.00	50.00	2024-08-30	2024-09-15	30		0.50	\N	150.00	0.00	2	75.00	t	2024-08-18 00:38:03+00	2024-09-27 23:51:54.773934+00	moderate_default	1	4	3	3	2	87	1
83	1ddfb20c-9dba-4ff2-947e-1d99d1bec716	to_solve	400.00	630.00	230.00	2024-09-02	2024-09-15	45		0.38	\N	620.00	10.00	3	210.00	f	2024-08-12 19:57:36+00	2024-11-12 22:25:54.345837+00	moderate_default	1	4	3	3	2	71	1
82	ee474bce-5b66-4992-a956-ed36cd566826	pending	150.00	220.00	70.00	2024-08-15	2024-09-30	30		0.47	\N	0.00	220.00	2	110.00	t	2024-08-12 19:31:52+00	2024-09-14 19:53:12.813222+00	severe_default	1	4	3	3	2	70	1
518	d27e0cfb-1c86-455b-a7dd-78cdb0005f81	pending	50.00	80.00	30.00	2024-11-30	2024-12-15	30		0.60	\N	0.00	80.00	1	80.00	f	2024-11-23 01:16:58+00	2024-11-27 01:17:39.271252+00	on_time	1	4	4	3	2	59	1
118	d161d15b-38f5-4952-bede-a3b45bdcf7b6	completed	300.00	450.00	150.00	2024-08-30	2024-09-15	30		0.50	\N	450.00	0.00	2	225.00	t	2024-08-20 01:16:36+00	2024-11-21 21:45:51.592656+00	moderate_default	1	4	3	3	2	93	1
119	6fe4c01e-705f-48a1-86dc-8f271337991f	pending	130.00	330.00	200.00	2024-09-15	2024-09-30	30		1.54	\N	330.00	0.00	2	165.00	t	2024-08-21 01:19:20+00	2024-11-05 22:18:55.625741+00	mild_default	1	4	3	3	2	94	1
526	c309ee82-1f13-4eca-9a77-2ec473eece15	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	120.00	2	60.00	f	2024-11-24 21:35:36+00	2024-11-27 21:37:37.179868+00	on_time	1	4	3	3	2	257	1
117	dbb41bd0-ab1b-41e3-bc55-53a895817a92	pending	100.00	120.00	20.00	2024-08-30	2024-09-15	30		0.20	\N	110.00	10.00	5	24.00	t	2024-08-20 01:11:12+00	2024-10-27 23:54:38.933589+00	recurrent_default	1	4	2	3	2	92	1
530	b40a541e-f574-4d25-b178-d03abcc9faa5	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	120.00	2	60.00	f	2024-11-25 22:08:54+00	2024-11-27 22:09:38.382324+00	on_time	1	4	3	3	2	244	1
106	0b2ca385-9888-4767-a603-3e90e6c79935	pending	300.00	500.00	200.00	2024-09-30	2024-10-15	45		0.44	\N	350.00	150.00	3	166.67	f	2024-09-13 23:50:56+00	2024-10-19 23:24:08.030715+00	moderate_default	1	4	3	3	2	5	1
90	1869643c-8f17-4e1b-a675-4fdde8a3573a	pending	500.00	740.00	240.00	2024-08-30	2024-09-15	60		0.24	\N	140.00	600.00	4	185.00	t	2024-08-14 22:08:35+00	2024-11-20 22:58:17.891929+00	recurrent_default	1	4	3	3	9	76	1
91	5aa8143e-f6de-40ac-a7d0-3b48a03b4d4b	pending	200.00	300.00	100.00	2024-09-30	2024-09-15	30		0.50	\N	290.00	10.00	2	150.00	t	2024-08-15 22:49:29+00	2024-12-04 22:13:27.469417+00	recurrent_default	1	4	3	3	2	77	1
110	030db4e6-f749-40da-9df4-b7c07ced81af	pending	300.00	540.00	240.00	2024-09-03	2024-09-15	60		0.40	\N	485.00	55.00	4	135.00	f	2024-08-17 00:23:27+00	2024-10-24 19:16:09.759248+00	moderate_default	1	4	3	3	2	85	1
81	a333bbfc-c873-4066-88ad-bc3fa73dd4fd	pending	100.00	150.00	50.00	2024-08-24	2024-09-07	60		0.25	\N	227.50	-77.50	4	37.50	t	2024-08-11 18:04:00+00	2024-10-18 00:21:20.753222+00	moderate_default	1	4	3	3	2	69	1
88	5d1dff01-f3c2-4641-855d-7d65fa96c27e	pending	200.00	330.00	130.00	2024-08-27	2024-09-12	45		0.43	\N	330.00	0.00	3	110.00	t	2024-08-13 21:26:05+00	2024-09-17 22:36:14.027196+00	moderate_default	1	4	3	3	2	75	1
104	2ac095fa-9be5-4a2e-ba41-65f2cf961d25	pending	200.00	375.00	175.00	2024-09-30	2024-10-15	45		0.58	\N	0.00	375.00	3	125.00	f	2024-09-13 23:47:12+00	2024-09-14 23:49:59.091715+00	on_time	1	4	3	3	2	80	1
108	1a73d4e0-656a-412b-b577-e9fdf4b7a99d	pending	200.00	330.00	130.00	2024-08-31	2024-09-15	45		0.43	\N	330.00	0.00	3	110.00	f	2024-08-17 00:04:56+00	2024-10-04 03:05:27.049227+00	moderate_default	1	4	3	3	2	83	1
86	ccd65dc9-d2a1-4dfe-8e22-a0f058b29a30	pending	100.00	140.00	40.00	2024-08-10	2024-08-30	30		0.40	\N	130.00	10.00	2	70.00	t	2024-08-13 21:21:02+00	2024-10-27 23:55:54.444714+00	recurrent_default	1	4	3	3	2	37	1
115	14770993-86eb-4aa3-b1f9-6ed89b73e0aa	pending	150.00	255.00	105.00	2024-09-02	2024-09-15	45		0.47	\N	265.00	-10.00	3	85.00	t	2024-08-18 00:47:01+00	2024-11-10 20:53:39.933464+00	mild_default	1	4	3	3	2	89	1
109	230c6b8b-61bf-4ce1-95e6-fcc73506937e	pending	100.00	130.00	30.00	2024-09-02	2024-09-15	30		0.30	\N	130.00	0.00	2	65.00	f	2024-08-17 00:21:01+00	2024-09-15 00:31:39.321789+00	on_time	1	4	3	3	2	84	1
113	733c5447-0fbb-4f61-b71b-9cde6b86cb06	pending	100.00	150.00	50.00	2024-08-30	2024-09-15	30		0.50	\N	150.00	0.00	2	75.00	t	2024-08-18 00:41:24+00	2024-10-09 00:37:54.3977+00	moderate_default	1	4	3	3	2	88	1
87	742e3937-9054-4bf5-bcce-9a2afdf25c0f	pending	200.00	380.00	180.00	2024-08-24	2024-09-10	60		0.45	\N	400.00	-20.00	4	95.00	t	2024-08-13 21:21:55+00	2024-10-19 22:32:39.817244+00	moderate_default	1	4	3	3	2	74	1
114	6bb6272c-0bdf-49c0-a0ab-7a6b8d33402d	pending	150.00	255.00	105.00	2024-09-07	2024-09-21	45		0.47	\N	270.00	-15.00	3	85.00	t	2024-08-18 00:43:18+00	2024-11-22 00:18:35.082822+00	mild_default	1	4	3	3	2	90	1
105	0acefdb3-f31d-40d5-bddf-7ed432d5a065	pending	100.00	130.00	30.00	2024-09-30	2024-10-15	30		0.30	\N	130.00	0.00	2	65.00	f	2024-09-13 23:50:06+00	2024-10-24 19:35:54.423425+00	moderate_default	1	4	3	3	2	81	1
122	51771098-1cf7-4025-a1c3-bf6398ced53d	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	130.00	10.00	2	70.00	f	2024-08-22 01:43:10+00	2024-10-11 16:00:20.127211+00	moderate_default	1	4	3	3	2	97	1
111	94aae993-7752-48b5-b556-8eca021de91d	pending	100.00	165.00	65.00	2024-08-30	2024-09-15	45		0.43	\N	155.00	10.00	3	55.00	t	2024-08-18 00:34:12+00	2024-10-24 22:57:28.047406+00	mild_default	1	4	3	3	2	86	1
116	f17e01a5-5f51-4dbe-98be-953948a317dc	pending	100.00	140.00	40.00	2024-09-03	2024-09-17	30		0.40	\N	70.00	70.00	2	70.00	f	2024-08-18 00:52:23+00	2024-09-15 00:58:56.2951+00	on_time	1	4	3	3	2	91	1
89	06c0c029-c7e6-4e53-a6e1-9f7a28c64186	pending	200.00	330.00	130.00	2024-09-02	2024-09-13	45		0.43	\N	440.00	-110.00	3	110.00	t	2024-08-14 21:59:12+00	2024-11-12 21:57:35.134684+00	moderate_default	1	4	3	3	2	51	1
107	55292100-f398-492f-948a-fdaede2d2387	pending	150.00	225.00	75.00	2024-08-31	2024-09-15	30		0.50	\N	215.00	10.00	2	112.50	f	2024-09-14 00:01:09+00	2024-09-21 21:08:19.961231+00	moderate_default	1	4	3	3	2	82	1
120	fbf34961-a5f5-42d9-9baa-63a6d2d350c2	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-08-21 01:21:21+00	2024-09-15 01:22:28.43008+00	on_time	1	4	3	3	2	95	1
121	af981313-0a86-48b8-878c-54b9b98c9a8f	pending	100.00	120.00	20.00	2024-09-15	2024-09-30	30		0.20	\N	0.00	120.00	2	60.00	f	2024-08-21 01:22:50+00	2024-09-15 01:42:48.022436+00	on_time	1	4	3	3	2	96	1
143	961cd14f-1440-421c-8cd0-d5c63e8c881c	to_solve	100.00	115.00	15.00	2024-09-30	2024-10-01	15		0.30	\N	0.00	115.00	1	115.00	f	2024-09-17 00:07:54+00	2024-11-12 21:23:51.325295+00	on_time	1	4	3	3	2	98	1
150	a8f2c2a5-5674-4a19-b3a5-a4a5517c9b84	completed	500.00	800.00	300.00	2024-09-30	2024-10-15	15		1.20	\N	800.00	0.00	1	800.00	t	2024-09-17 19:15:34+00	2024-11-21 21:45:42.086133+00	recurrent_default	1	4	3	3	2	93	1
126	e16958e4-f8e3-438f-84d2-52214b84d7d4	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-08-24 01:51:31+00	2024-09-15 01:52:19.630052+00	on_time	1	4	3	3	2	101	1
146	0f683c91-b98a-4fd4-96f7-d5c0750fd051	pending	150.00	250.00	100.00	2024-09-06	2024-09-16	30		0.67	\N	200.00	50.00	2	125.00	t	2024-07-17 00:28:30+00	2024-10-24 19:15:12.916911+00	mild_default	1	4	3	3	2	113	1
140	88b16d82-41c0-45b6-970c-7819cfc3eec1	pending	100.00	180.00	80.00	2024-09-30	2024-10-15	45		0.53	\N	95.00	85.00	3	60.00	t	2024-09-17 00:03:18+00	2024-11-26 20:58:41.667881+00	mild_default	1	4	3	3	2	109	1
154	d55af1e0-1068-42de-bcf0-09ca58a113d9	pending	100.00	150.00	50.00	2024-09-30	2024-10-15	45		0.33	\N	100.00	50.00	3	50.00	f	2024-09-17 19:46:59+00	2024-10-24 21:18:02.931055+00	moderate_default	1	4	3	3	2	34	1
144	f6188f6b-0d31-4050-b6d7-1d6a98a4321e	pending	50.00	65.00	15.00	2024-09-30	2024-10-01	15		0.60	\N	35.00	30.00	1	65.00	t	2024-09-17 00:08:48+00	2024-11-08 22:49:52.844827+00	mild_default	1	4	3	3	2	111	1
155	0be6f227-3258-4330-a71e-70fb7fa1327d	pending	500.00	800.00	300.00	2024-09-30	2024-10-15	30		0.60	\N	900.00	-100.00	2	400.00	f	2024-09-17 19:47:42+00	2024-11-02 00:45:13.642958+00	moderate_default	1	4	3	3	2	64	1
127	712da1ab-6a34-49bd-aff4-2248b9c1c46c	pending	400.00	600.00	200.00	2024-09-30	2024-10-15	45		0.33	\N	190.00	410.00	3	200.00	t	2024-09-14 22:06:56+00	2024-12-06 01:09:54.28173+00	recurrent_default	1	4	3	3	2	13	1
134	1c639c41-84b4-40d8-830e-e17c5b50a341	pending	150.00	250.00	100.00	2024-09-30	2024-10-15	30		0.67	\N	0.00	250.00	2	125.00	f	2024-09-14 23:03:20+00	2024-09-17 23:03:27.103124+00	on_time	1	4	3	3	2	39	1
136	6307e3ae-c39e-4d50-aea4-63bf7b66ac05	pending	200.00	315.00	115.00	2024-09-30	2024-10-15	45		0.38	\N	0.00	315.00	3	105.00	f	2024-09-15 23:24:46+00	2024-09-17 23:25:52.784871+00	on_time	1	4	3	3	2	105	1
128	c8c865e1-853d-478a-957f-1979dae5b233	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	30		0.40	\N	70.00	70.00	2	70.00	f	2024-09-14 22:10:03+00	2024-10-24 01:53:40.735275+00	moderate_default	1	4	3	3	2	78	1
142	75ea91a3-0669-4a91-864f-a4242e5ea376	pending	150.00	270.00	120.00	2024-09-30	2024-10-15	45		0.53	\N	55.00	215.00	3	90.00	t	2024-09-17 00:06:43+00	2024-11-22 00:46:13.184064+00	recurrent_default	1	4	3	3	2	97	1
145	f61497e2-3578-4c5f-b136-a90d5346e955	pending	100.00	150.00	50.00	2024-09-16	2024-09-30	30		0.50	\N	140.00	10.00	2	75.00	f	2024-08-31 00:24:55+00	2024-09-18 00:27:31.308499+00	on_time	1	4	3	3	2	112	1
141	d8b2310a-6950-459f-9eec-02b4cf5dcd9f	pending	100.00	150.00	50.00	2024-09-30	2024-10-15	30		0.50	\N	145.00	5.00	2	75.00	f	2024-09-17 00:05:42+00	2024-10-24 01:59:55.451525+00	moderate_default	1	4	3	3	2	110	1
125	5541ba95-e71b-4414-a59b-7c4cc57e5fd1	pending	80.00	110.00	30.00	2024-09-15	2024-09-30	30		0.38	\N	115.00	-5.00	2	55.00	t	2024-08-24 01:49:16+00	2024-11-12 21:17:27.326945+00	mild_default	1	4	3	3	2	100	1
92	e58d2335-313f-4baa-bf9d-c9a67c458520	pending	90.00	140.00	50.00	2024-08-30	2024-09-15	30		0.56	\N	210.00	-70.00	2	70.00	f	2024-08-15 22:51:00+00	2024-10-04 02:55:31.746083+00	moderate_default	1	4	3	3	2	78	1
139	41e5b87d-6d6d-4c4b-9fbe-30c38784e693	pending	100.00	150.00	50.00	2024-09-30	2024-10-15	45		0.33	\N	150.00	0.00	3	50.00	f	2024-09-17 00:01:49+00	2024-11-09 00:08:04.840315+00	moderate_default	1	4	3	3	2	108	1
129	772d9c52-378a-42fe-b7aa-34ec7864f5aa	pending	200.00	280.00	80.00	2024-09-30	2024-09-30	15		0.80	\N	280.00	0.00	1	280.00	t	2024-09-14 22:11:39+00	2024-11-20 23:21:48.777913+00	recurrent_default	1	4	3	3	2	102	1
148	94f2f3ec-0d9d-4e85-b99c-28c8805c70cc	pending	150.00	200.00	50.00	2024-09-30	2024-10-15	30		0.33	\N	0.00	200.00	2	100.00	f	2024-09-17 19:11:07+00	2024-09-19 19:11:48.025701+00	on_time	1	4	3	3	2	36	1
147	076c1dfc-6831-40f7-85fa-bd0443cd1e6a	pending	300.00	501.00	201.00	2024-09-30	2024-10-15	45		0.45	\N	157.00	344.00	3	167.00	t	2024-09-17 19:04:52+00	2024-10-24 01:52:14.833631+00	mild_default	1	4	3	3	2	114	1
137	e987b6ba-e9e1-41aa-a162-30bd26155960	pending	300.00	500.00	200.00	2024-08-02	2024-09-15	45		0.44	\N	500.00	0.00	3	166.67	t	2024-08-15 23:40:30+00	2024-11-09 00:28:43.333341+00	recurrent_default	1	4	3	3	2	106	1
531	4ebc2179-a00b-4b79-9740-e1fa9de0596c	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	60.00	60.00	2	60.00	f	2024-11-25 22:09:38+00	2024-12-04 23:05:56.39993+00	on_time	1	4	3	3	2	259	1
135	0f859ffb-ff29-4254-bb30-e04e09c9f4e9	pending	100.00	150.00	50.00	2024-09-15	2024-09-30	30		0.50	\N	145.00	5.00	2	75.00	t	2024-08-26 23:21:50+00	2024-10-24 01:38:26.083504+00	mild_default	1	4	3	3	2	104	1
123	e6dfe011-60b2-4bee-84a2-ff1f743ec058	pending	300.00	500.00	200.00	2024-09-15	2024-09-30	30		0.67	\N	500.00	0.00	2	250.00	f	2024-08-23 01:46:30+00	2024-09-19 19:39:41.149516+00	on_time	1	4	3	3	2	98	1
84	6d2b6dbc-3a68-4e09-8d86-b38596a55856	pending	300.00	600.00	300.00	2024-08-24	2024-09-08	12		2.50	\N	550.00	50.00	2	300.00	t	2024-08-13 20:02:29+00	2024-12-06 00:20:58.975348+00	recurrent_default	1	4	2	3	2	72	1
153	f01532a5-42f4-4d8e-8e02-8112d8779965	pending	200.00	400.00	200.00	2024-09-30	2024-10-15	60		0.50	\N	0.00	400.00	4	100.00	f	2024-09-17 19:45:52+00	2024-09-19 19:46:44.724981+00	on_time	1	4	3	3	2	29	1
131	08f186ae-31bb-4ed4-b6ca-e49ae8d12e3b	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	60		0.20	\N	120.00	20.00	4	35.00	f	2024-09-14 22:29:53+00	2024-10-19 23:07:17.644759+00	moderate_default	1	4	3	3	2	103	1
152	75d1ec0d-705d-4a55-83e4-d347bb40765c	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	30		0.40	\N	140.00	0.00	2	70.00	f	2024-09-17 19:43:40+00	2024-10-04 02:43:06.064424+00	on_time	1	4	3	3	2	116	1
156	3a040d1e-704d-4809-ab9a-63501204a10b	pending	200.00	345.00	145.00	2024-07-18	2024-08-04	60		0.36	\N	95.00	250.00	4	86.25	t	2024-07-03 19:48:45+00	2024-09-19 19:55:03.935017+00	recurrent_default	1	4	3	3	2	117	1
149	ff2ff194-bbb1-4261-9411-98d201bc0431	pending	200.00	300.00	100.00	2024-09-30	2024-10-15	45		0.33	\N	300.00	0.00	3	100.00	t	2024-09-17 19:11:56+00	2024-12-04 21:58:03.791872+00	mild_default	1	4	3	3	2	16	1
50	5663b25d-6152-4e07-9ed0-03fae0b566ef	pending	50.00	65.00	15.00	2024-09-15	2024-09-30	30		0.30	\N	65.00	0.00	2	32.50	f	2024-09-06 22:57:37+00	2024-09-23 18:49:59.549867+00	on_time	1	4	3	3	2	44	1
124	7a8f020b-e678-451c-9bb9-6cc1a7c72754	pending	300.00	600.00	300.00	2024-09-15	2024-09-30	60		0.50	\N	430.00	170.00	4	150.00	f	2024-08-23 01:48:19+00	2024-10-19 23:35:34.546152+00	moderate_default	1	4	3	3	2	99	1
132	12f888fd-25b8-427e-8b63-f987406f28fb	pending	400.00	660.00	260.00	2024-09-30	2024-10-15	45		0.43	\N	660.00	0.00	3	220.00	f	2024-09-14 22:56:54+00	2024-11-02 00:58:35.436933+00	moderate_default	1	4	3	3	2	75	1
159	46e62bc0-66c4-4fd1-bc48-f6413480e590	pending	300.00	300.00	0.00	2024-07-11	2024-07-16	60		0.00	\N	150.00	150.00	4	75.00	t	2024-04-11 18:28:26+00	2024-09-20 18:50:27.523134+00	recurrent_default	1	4	3	3	2	120	1
192	1cf3b6ae-f365-4fba-8230-6ace7e20ad86	to_solve	50.00	70.00	20.00	2024-09-30	2024-10-15	30		0.40	\N	0.00	70.00	2	35.00	f	2024-09-26 22:29:47+00	2024-11-12 18:12:09.821054+00	on_time	1	4	3	3	2	84	1
165	941f2c40-fd41-47a9-87f7-6c92cfc2d298	pending	50.00	90.00	40.00	2024-09-05	2024-09-30	30	Credito #3	0.80	\N	45.00	45.00	2	45.00	t	2024-08-21 20:37:35+00	2024-09-21 21:00:42.744836+00	moderate_default	1	4	3	3	2	27	1
509	f57092c6-52fc-48be-9405-72d2fc5fb681	pending	50.00	70.00	20.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	70.00	2	35.00	f	2024-11-21 00:06:10+00	2024-11-27 00:13:25.264579+00	on_time	1	4	3	3	2	18	1
177	77f5fe31-a9c4-4d72-8fec-7fc796dc9d80	pending	100.00	140.00	40.00	2024-07-30	2024-10-15	30		0.40	\N	130.00	10.00	2	70.00	t	2024-07-19 18:33:00+00	2024-09-23 18:40:04.149261+00	mild_default	1	4	3	3	2	131	1
169	6bf98106-efed-409a-afc4-1472482c0a5c	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	30		0.40	\N	150.00	-10.00	2	70.00	f	2024-09-18 22:32:54+00	2024-10-28 00:13:11.436147+00	moderate_default	1	4	3	3	2	126	1
162	dc5e22ea-2e09-499f-ac1e-6da656366d96	pending	200.00	300.00	100.00	2024-07-18	2024-08-05	45		0.33	\N	205.00	95.00	3	100.00	t	2024-06-03 20:13:06+00	2024-09-20 20:25:43.6102+00	mild_default	1	4	3	3	2	122	1
164	8ec7e2b6-6f39-424e-9e45-8f35d13278d9	pending	180.00	180.00	0.00	2024-07-30	2024-08-15	30		0.00	\N	0.00	180.00	2	90.00	t	2024-07-01 20:28:01+00	2024-09-20 20:29:39.324471+00	critical_default	1	4	3	3	2	124	1
181	2eb70213-5d0e-40e1-8fdc-ec2256d46eca	pending	80.00	160.00	80.00	2024-09-30	2024-10-15	30		1.00	\N	130.00	30.00	2	80.00	t	2024-09-22 19:24:34+00	2024-11-08 23:34:27.619345+00	mild_default	1	4	3	3	2	133	1
163	5d5f1347-e7d5-4d47-b068-9486125eb828	pending	100.00	150.00	50.00	2024-09-03	2024-09-30	30		0.50	\N	100.00	50.00	2	75.00	t	2024-08-17 20:26:15+00	2024-09-20 20:30:38.514628+00	moderate_default	1	4	3	3	2	123	1
157	7ac1bac5-d5d0-4f85-a1c0-d54266ad396e	pending	105.00	408.00	303.00	2023-09-18	2024-03-16	180	Celular	0.48	\N	230.00	178.00	12	34.00	t	2023-12-18 23:35:30+00	2024-09-20 00:14:42.449888+00	recurrent_default	1	4	3	3	2	118	1
160	2f5e24c0-e891-4ab2-8cef-0cf19c013b86	pending	50.00	90.00	40.00	2024-09-11	2024-09-30	30		0.80	\N	45.00	45.00	2	45.00	f	2024-09-10 19:00:07+00	2024-09-20 20:39:26.869044+00	on_time	1	4	3	3	2	27	1
171	402b135e-e2c2-433b-b6e1-60930eccdfc3	pending	50.00	90.00	40.00	2024-09-30	2024-10-15	30		0.80	\N	0.00	90.00	2	45.00	f	2024-09-19 22:51:51+00	2024-10-23 23:09:05.125721+00	on_time	1	4	3	3	2	128	1
173	943449ec-99f9-4446-9460-05df59f684de	pending	150.00	300.00	150.00	2024-09-30	2024-10-15	45		0.67	\N	0.00	300.00	3	100.00	f	2024-09-20 21:01:43+00	2024-09-21 21:02:14.653558+00	on_time	1	4	3	3	2	27	1
174	b2f90600-dd02-473e-bc90-101543f18d7c	pending	160.00	160.00	0.00	2024-09-30	2024-10-15	30		0.00	\N	0.00	160.00	2	80.00	f	2024-09-20 21:04:00+00	2024-09-21 21:06:57.438523+00	on_time	1	4	3	3	2	28	1
168	94c4fe43-bfb5-4b72-896b-fc5624ea0fa5	pending	100.00	165.00	65.00	2024-09-30	2024-10-15	45		0.43	\N	165.00	0.00	3	55.00	f	2024-09-18 22:31:47+00	2024-11-01 22:01:21.532769+00	moderate_default	1	4	3	3	2	125	1
190	100a82f7-d34e-4598-8daf-e96a3bd69541	pending	300.00	375.00	75.00	2024-09-30	2024-10-15	30		0.25	\N	230.00	145.00	2	187.50	t	2024-09-24 19:07:18+00	2024-11-02 00:24:22.833834+00	mild_default	1	4	3	3	2	15	1
166	053bc6fc-8068-449e-9d0c-3756ec075603	pending	100.00	480.00	380.00	2024-07-11	2024-08-12	60		1.90	\N	470.00	10.00	4	120.00	t	2024-07-03 20:39:39+00	2024-11-09 01:09:51.729957+00	recurrent_default	1	4	3	3	2	27	1
527	36cbf852-1f65-49fc-a1f1-5caa5bb296b1	pending	100.00	135.00	35.00	2024-11-30	2024-12-15	30		0.35	\N	0.00	135.00	1	135.00	f	2024-11-25 21:43:36+00	2024-11-27 21:44:20.990401+00	on_time	1	4	4	3	2	164	1
161	b04e6cc0-fdd8-4d83-af9f-940f2e27aa2b	pending	530.00	1200.00	670.00	2024-09-18	2024-09-30	60		0.63	\N	900.00	300.00	4	300.00	f	2024-08-19 20:10:04+00	2024-10-24 23:24:11.525239+00	moderate_default	1	4	3	3	2	121	1
186	1ba9412d-969b-4c42-ae60-c268c9848f29	pending	100.00	150.00	50.00	2024-09-30	2024-10-15	30		0.50	\N	70.00	80.00	2	75.00	f	2024-09-24 18:38:23+00	2024-10-09 23:03:45.074222+00	on_time	1	4	3	3	2	137	1
179	00f4c7f1-94a9-4062-ad68-64d6969a5956	pending	50.00	70.00	20.00	2024-09-30	2024-10-15	30		0.40	\N	0.00	70.00	2	35.00	f	2024-09-21 18:52:13+00	2024-09-23 18:53:04.055145+00	on_time	1	4	3	3	2	111	1
188	c9b24b6b-d3a9-459c-97dc-d49f26d4144d	pending	300.00	500.00	200.00	2024-09-30	2024-10-15	75		0.27	\N	400.00	100.00	5	100.00	f	2024-09-24 18:59:11+00	2024-11-26 20:58:06.090773+00	moderate_default	1	4	3	3	2	138	1
170	b9a6fb57-f99b-46d8-9e09-b4c40edcf54d	pending	100.00	140.00	40.00	2024-07-22	2024-08-05	60		0.20	\N	145.00	-5.00	4	35.00	t	2024-07-16 22:41:41+00	2024-11-01 22:06:02.122742+00	mild_default	1	4	3	3	2	127	1
182	bc895841-9613-4ee9-9e1a-6d4220ba745f	pending	50.00	90.00	40.00	2024-09-30	2024-10-15	30		0.80	\N	0.00	90.00	2	45.00	f	2024-09-22 19:33:16+00	2024-09-23 19:35:06.30732+00	on_time	1	4	3	3	2	134	1
176	b3d78375-6368-4f92-87d3-c5db12e4e626	pending	150.00	250.00	100.00	2024-09-30	2024-10-15	30		0.67	\N	125.00	125.00	2	125.00	f	2024-09-20 21:12:08+00	2024-10-04 02:28:00.338376+00	on_time	1	4	3	3	2	130	1
185	9a550dda-ced6-40ad-a078-70f04d6b91d0	pending	100.00	132.00	32.00	2024-09-30	2024-10-15	60		0.16	\N	129.00	3.00	4	33.00	f	2024-09-23 18:23:28+00	2024-11-27 00:59:41.680173+00	moderate_default	1	4	3	3	2	44	1
180	e8de2e0b-e0e8-4c2a-a14c-b3907b645de3	pending	20.00	30.00	10.00	2024-09-30	2024-10-15	30		0.50	\N	10.00	20.00	2	15.00	t	2024-09-22 19:23:23+00	2024-11-10 20:36:16.433295+00	mild_default	1	4	3	3	2	132	1
158	0fc64909-cc31-4bcf-83f7-a2581b891b2f	pending	200.00	360.00	160.00	2024-05-18	2024-09-17	60		0.40	\N	360.00	0.00	2	180.00	t	2024-05-02 00:51:17+00	2024-10-19 22:38:13.017524+00	recurrent_default	1	4	4	3	2	119	1
175	f4a253c4-08c6-4457-9565-87593256c8e4	pending	100.00	180.00	80.00	2024-09-30	2024-10-15	45		0.53	\N	180.00	0.00	3	60.00	f	2024-09-20 21:08:58+00	2024-10-24 01:51:30.730901+00	moderate_default	1	4	3	3	2	129	1
183	4a2c3674-6f76-44b4-8aaa-9c6ad07b91ff	pending	400.00	600.00	200.00	2024-07-20	2024-07-23	45		0.33	\N	465.00	135.00	3	200.00	t	2024-07-04 00:15:11+00	2024-11-27 21:32:04.992993+00	recurrent_default	1	4	3	3	2	135	1
191	0053f991-eed7-486c-8111-752d3e7751ed	pending	300.00	450.00	150.00	2024-09-15	2024-09-30	30		0.50	\N	450.00	0.00	2	225.00	f	2024-08-29 19:00:18+00	2024-09-27 19:10:44.946067+00	on_time	1	4	3	3	2	140	1
532	8f09ec40-e175-4fe1-9331-e7e5cc73ad45	pending	20.00	25.00	5.00	2024-11-30	2024-12-15	30		0.25	\N	0.00	25.00	1	25.00	f	2024-11-25 22:11:07+00	2024-11-27 22:13:14.995772+00	on_time	1	4	4	3	2	260	1
167	a128fa11-ef11-4d72-9a79-59453d28b2ba	pending	200.00	360.00	160.00	2024-09-30	2024-10-15	45		0.53	\N	215.00	145.00	3	120.00	t	2024-09-18 22:25:55+00	2024-12-06 01:09:00.271793+00	recurrent_default	1	4	3	3	2	106	1
178	92f38a85-d564-479d-9fbb-94f03a404c9d	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	30		0.40	\N	135.00	5.00	2	70.00	f	2024-09-21 18:51:36+00	2024-10-09 22:24:03.342355+00	on_time	1	4	3	3	2	82	1
195	23e0ba81-6920-4b42-961b-e5f3246948ed	pending	100.00	140.00	40.00	2024-08-12	2024-09-26	30		0.40	\N	140.00	0.00	2	70.00	t	2024-07-28 23:20:20+00	2024-09-27 23:27:44.766155+00	mild_default	1	4	3	3	2	141	1
196	6c6c181a-95e7-436f-9191-e24862c86b23	pending	150.00	250.00	100.00	2024-09-30	2024-10-15	30		0.67	\N	0.00	250.00	2	125.00	f	2024-09-26 23:37:37+00	2024-09-27 23:39:03.616952+00	on_time	1	4	3	3	2	142	1
225	099444da-55d3-4a0e-abd3-97241c9b807b	to_solve	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-01 23:12:46+00	2024-11-12 18:21:53.931082+00	moderate_default	1	4	3	3	2	157	1
212	2f9d6107-f547-42da-8eca-6ecdbc345664	pending	30.00	60.00	30.00	2024-09-30	2024-10-15	45		0.67	\N	35.00	25.00	3	20.00	t	2024-09-29 02:25:15+00	2024-11-10 20:54:31.843638+00	mild_default	1	4	3	3	2	149	1
204	ab46b9ef-7fc0-4e2e-81a0-beb249260648	pending	250.00	300.00	50.00	2024-09-30	2024-10-15	30		0.20	\N	300.00	0.00	2	150.00	f	2024-09-26 00:41:22+00	2024-10-27 23:39:03.034417+00	moderate_default	1	4	3	3	2	67	1
211	d6676550-5eca-4c39-85f2-ec62a7883a36	pending	100.00	150.00	50.00	2024-09-30	2024-10-02	30		0.50	\N	0.00	150.00	2	75.00	f	2024-09-29 02:24:26+00	2024-10-04 02:25:03.340717+00	on_time	1	4	3	3	2	15	1
228	75b60fef-55c7-4ced-8b73-05b09f0ea83c	pending	50.00	80.00	30.00	2024-10-15	2024-10-30	30		0.60	\N	40.00	40.00	2	40.00	f	2024-10-01 23:20:22+00	2024-10-24 22:12:14.01517+00	on_time	1	4	3	3	2	42	1
199	897ab697-1d12-4942-a1f5-bd466c1b5757	pending	150.00	300.00	150.00	2024-08-10	2024-08-28	45		0.67	\N	310.00	-10.00	3	100.00	t	2024-07-25 23:53:21+00	2024-09-28 00:04:53.298479+00	moderate_default	1	4	3	3	2	145	1
202	940d52dc-6610-4074-abb1-c6cbd34117f4	to_solve	100.00	160.00	60.00	2024-09-30	2024-10-15	30		0.60	\N	0.00	160.00	2	80.00	f	2024-09-26 00:08:32+00	2024-11-20 21:50:07.489284+00	moderate_default	1	4	3	3	2	145	1
215	3baeeeb7-6911-4996-8e8e-85815a48d70b	pending	200.00	360.00	160.00	2024-10-15	2024-10-30	45		0.53	\N	360.00	0.00	3	120.00	f	2024-10-01 02:49:49+00	2024-11-09 00:33:38.224265+00	moderate_default	1	4	3	3	2	43	1
200	54aa683d-c124-4432-af2a-25f32ddd8007	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	30		0.40	\N	150.00	-10.00	2	70.00	f	2024-09-26 00:05:11+00	2024-10-19 22:35:08.92564+00	moderate_default	1	4	3	3	2	87	1
197	8d34c902-d499-473a-a118-3c6f87312f3a	pending	50.00	90.00	40.00	2024-09-30	2024-10-15	30		0.80	\N	0.00	90.00	2	45.00	f	2024-09-26 23:39:09+00	2024-10-24 16:29:28.716392+00	on_time	1	4	3	3	2	143	1
223	f84be3ce-74b1-478f-8083-502f335c1473	pending	300.00	501.00	201.00	2024-10-15	2024-10-31	48		0.42	\N	501.00	0.00	4	125.25	f	2024-10-01 23:10:11+00	2024-12-04 21:55:46.787265+00	moderate_default	1	4	3	3	2	19	1
217	325f4d00-08c0-459d-8d8f-653c01bdc87f	to_solve	90.00	115.00	25.00	2024-09-30	2024-10-15	60		0.14	\N	50.00	65.00	4	28.75	f	2024-08-31 02:59:03+00	2024-11-12 21:52:52.929639+00	moderate_default	1	4	3	3	10	152	1
208	d9e8d7d8-5f78-4eea-992a-770234186cf6	pending	50.00	50.00	0.00	2024-09-30	2024-10-15	30		0.00	\N	0.00	50.00	2	25.00	f	2024-09-28 02:10:49+00	2024-10-04 02:11:47.121978+00	on_time	1	4	3	3	2	148	1
209	2c467e7a-761f-4f96-bce6-4cb3dbfb0600	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	45		0.27	\N	0.00	140.00	3	46.67	f	2024-09-29 02:22:18+00	2024-10-04 02:23:42.060012+00	on_time	1	4	3	3	2	92	1
207	bc8f85fb-9b95-4cbd-a47a-951842fb7b72	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	60		0.20	\N	140.00	0.00	4	35.00	f	2024-09-28 02:09:36+00	2024-11-10 20:43:22.9442+00	moderate_default	1	4	3	3	2	147	1
232	7f80a031-2ed1-4eea-bf29-63e7d061980a	pending	100.00	165.00	65.00	2024-10-15	2024-10-30	45		0.43	\N	20.00	145.00	3	55.00	t	2024-10-02 22:06:25+00	2024-11-20 22:01:51.583849+00	mild_default	1	4	3	3	2	86	1
214	c3b4ba88-21fa-413e-8338-d66c644185cf	pending	160.00	280.00	120.00	2024-10-15	2024-10-30	30		0.75	\N	200.00	80.00	2	140.00	f	2024-10-01 02:39:20+00	2024-10-24 01:40:56.342508+00	on_time	1	4	3	3	2	54	1
216	0457fc72-de91-4355-bc7f-4e331a25c783	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	45		0.33	\N	0.00	150.00	3	50.00	f	2024-10-01 02:52:10+00	2024-10-04 02:53:08.045885+00	on_time	1	4	3	3	2	151	1
205	600a6285-8742-4ca4-9e52-4700cf476e4f	pending	600.00	1100.00	500.00	2024-09-30	2024-10-15	60		0.42	\N	855.00	245.00	4	275.00	t	2024-09-26 01:11:06+00	2024-11-20 23:54:45.079219+00	moderate_default	1	4	3	3	2	6	1
203	6288252c-7912-4947-bd03-07e03d34fb71	pending	100.00	150.00	50.00	2024-09-30	2024-10-15	75		0.20	\N	120.00	30.00	5	30.00	f	2024-09-26 00:10:07+00	2024-11-20 22:00:26.092311+00	moderate_default	1	4	3	3	2	146	1
219	781f66d3-95bc-42ed-82dc-f8dd3084dac0	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-10-01 03:01:41+00	2024-10-04 03:02:24.052565+00	on_time	1	4	3	3	2	123	1
230	53189764-f548-4b89-9ebb-5cc5ba3cb0e8	pending	150.00	270.00	120.00	2024-10-15	2024-10-31	45		0.53	\N	90.00	180.00	3	90.00	t	2024-10-02 00:17:48+00	2024-12-04 22:03:28.776282+00	recurrent_default	1	4	3	3	2	7	1
222	17eaae4b-ec81-4922-843e-6f6183c631f8	pending	200.00	300.00	100.00	2024-08-30	2024-09-15	45		0.33	\N	300.00	0.00	3	100.00	t	2024-08-26 03:06:24+00	2024-11-09 00:06:48.741357+00	mild_default	1	4	3	3	2	155	1
198	bb5814b7-df7a-40c3-86fb-8e26c8d89da4	pending	80.00	130.00	50.00	2024-09-30	2024-10-15	30		0.63	\N	110.00	20.00	2	65.00	f	2024-09-26 23:41:55+00	2024-10-24 01:47:51.831004+00	moderate_default	1	4	3	3	2	144	1
224	23a848f4-cf1b-4f37-8505-78d135b3cfea	pending	100.00	120.00	20.00	2024-10-15	2024-10-30	30		0.20	\N	120.00	0.00	2	60.00	f	2024-10-01 23:11:03+00	2024-11-02 00:31:40.521548+00	moderate_default	1	4	3	3	2	156	1
221	59c609b5-23e9-458e-a8ba-3b57c77653d7	pending	100.00	140.00	40.00	2024-10-15	2024-10-30	30		0.40	\N	140.00	0.00	2	70.00	f	2024-10-01 03:03:30+00	2024-11-09 00:25:37.447895+00	moderate_default	1	4	3	3	2	154	1
213	2a3484ee-58b1-4e8b-8bfc-7b2136dd4646	pending	100.00	150.00	50.00	2024-10-17	2024-11-02	60		0.25	\N	139.00	11.00	4	37.50	f	2024-10-01 02:33:51+00	2024-11-10 20:18:06.535006+00	moderate_default	1	4	3	3	2	150	1
226	0eb63745-45d0-401e-aa9a-016b57a32a47	pending	150.00	250.00	100.00	2024-10-15	2024-10-30	30		0.67	\N	240.00	10.00	2	125.00	t	2024-10-01 23:14:19+00	2024-12-06 00:46:59.569633+00	mild_default	1	4	3	3	2	116	1
227	cfa4f217-3946-4f35-8698-bb9056d7e5f9	pending	100.00	165.00	65.00	2024-10-15	2024-10-30	45		0.43	\N	165.00	0.00	3	55.00	f	2024-10-01 23:18:59+00	2024-11-26 21:43:46.901001+00	moderate_default	1	4	3	3	2	158	1
206	0e90f26c-6b3a-4936-b37f-7ca45ee0ef2c	pending	100.00	150.00	50.00	2024-09-30	2024-10-15	30		0.50	\N	140.00	10.00	2	75.00	f	2024-09-26 01:11:39+00	2024-10-24 19:17:01.544012+00	moderate_default	1	4	3	3	2	112	1
229	bb8ea621-96ba-4f2a-997a-153b0646dee8	pending	100.00	140.00	40.00	2024-10-15	2024-10-31	30		0.40	\N	0.00	140.00	2	70.00	f	2024-10-01 23:21:27+00	2024-10-08 23:22:44.093995+00	on_time	1	4	3	3	2	159	1
231	8bd9cdc4-28cd-430b-a3cd-9dc2b6de8bd2	pending	150.00	270.00	120.00	2024-10-15	2024-10-30	30		0.80	\N	250.00	20.00	2	135.00	t	2024-10-02 22:05:15+00	2024-11-21 19:09:07.671066+00	mild_default	1	4	3	3	2	41	1
218	32a70ae1-6ec4-4409-ac3d-5ff5be0abb9c	pending	200.00	360.00	160.00	2024-10-15	2024-10-30	45		0.53	\N	55.00	305.00	3	120.00	f	2024-10-01 03:00:38+00	2024-10-09 22:42:29.314961+00	on_time	1	4	3	3	2	23	1
265	3603a933-0f9e-4dbf-91e6-9ec2a522d3e9	to_solve	500.00	700.00	200.00	2024-08-30	2024-09-15	30		0.40	\N	300.00	400.00	2	350.00	t	2024-08-14 01:00:03+00	2024-11-22 00:47:10.173082+00	recurrent_default	1	4	3	3	2	176	1
53	34a4c460-f2f9-47c5-98fa-a58649bbef39	pending	50.00	80.00	30.00	2024-09-15	2024-09-15	15		1.20	\N	80.00	0.00	1	80.00	f	2024-09-05 23:07:01+00	2024-10-09 23:05:35.363071+00	moderate_default	1	4	3	3	2	47	1
269	dc2e9b3c-cdc1-4e0b-bbe9-2e5d024cd979	pending	80.00	150.00	70.00	2024-10-15	2024-10-30	30		0.88	\N	131.00	19.00	2	75.00	t	2024-10-10 22:41:56+00	2024-11-26 23:59:25.479985+00	mild_default	1	4	3	3	2	2	1
241	f7b97530-6d7d-4d92-9019-eaf559932cb7	to_solve	20.00	90.00	70.00	2024-10-15	2024-10-30	30		3.50	\N	0.00	90.00	1	90.00	f	2024-10-04 16:08:39+00	2024-11-10 23:11:54.427736+00	on_time	1	4	4	3	2	84	1
263	60db50db-74dd-4451-bcfd-145009311d20	pending	100.00	160.00	60.00	2024-10-15	2024-10-30	30		0.60	\N	140.00	20.00	2	80.00	f	2024-10-09 00:51:36+00	2024-11-10 20:20:50.336583+00	moderate_default	1	4	3	3	2	47	1
248	fae2e563-f532-4d43-a9de-6ce3d63abf11	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-07 00:07:14+00	2024-11-08 23:35:26.8256+00	moderate_default	1	4	3	3	2	168	1
257	38414f22-58ed-4cad-98ea-f3bb3038e0aa	to_solve	30.00	50.00	20.00	2024-10-15	2024-10-30	15		1.33	\N	0.00	50.00	1	50.00	f	2024-10-08 00:38:14+00	2024-11-12 21:24:33.139954+00	on_time	1	4	3	3	2	98	1
247	6bcd996d-2054-4e3f-a3a5-c4a9e9d9eea4	pending	50.00	90.00	40.00	2024-10-15	2024-10-30	30		0.80	\N	40.00	50.00	2	45.00	f	2024-10-07 00:06:45+00	2024-10-24 22:39:06.239157+00	on_time	1	4	3	3	2	184	1
240	fae4329c-de90-4fcc-8fde-ddafe32add01	pending	300.00	540.00	240.00	2024-10-15	2024-10-30	45		0.53	\N	350.00	190.00	3	180.00	t	2024-10-04 15:53:31+00	2024-11-20 22:56:26.696836+00	mild_default	1	4	3	3	2	71	1
242	d9878776-7428-46a3-a0f1-c6581f3c687e	pending	100.00	130.00	30.00	2024-10-15	2024-10-30	30		0.30	\N	130.00	0.00	2	65.00	f	2024-10-04 16:10:45+00	2024-10-24 21:33:34.436775+00	on_time	1	4	3	3	2	164	1
243	27b5e02f-745a-4d1f-bb1b-1bf1bcb69daa	pending	150.00	270.00	120.00	2024-08-04	2024-10-04	45		0.53	\N	140.00	130.00	3	90.00	t	2024-07-05 16:24:39+00	2024-10-11 16:28:17.437848+00	recurrent_default	1	4	3	3	2	165	1
236	751b711d-c2de-4fe0-af04-aad42809cb16	pending	50.00	80.00	30.00	2024-10-15	2024-10-30	30		0.60	\N	80.00	0.00	1	80.00	f	2024-10-03 23:08:26+00	2024-11-09 01:42:25.328149+00	on_time	1	4	4	3	2	133	1
235	426a7c66-c205-4f0b-91a1-fa80463d0a6f	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	133.00	17.00	2	75.00	f	2024-10-03 23:07:10+00	2024-10-24 19:44:48.12867+00	on_time	1	4	3	3	2	82	1
234	d9a02c18-7de3-4e99-bbb1-e373a7e816b7	pending	200.00	330.00	130.00	2024-10-15	2024-10-30	45		0.43	\N	220.00	110.00	3	110.00	f	2024-10-03 23:06:04+00	2024-11-21 19:15:38.990555+00	moderate_default	1	4	3	3	2	65	1
238	4de7b723-a52a-4e67-90e6-4685dd625b02	pending	50.00	80.00	30.00	2024-10-15	2024-10-30	30		0.60	\N	50.00	30.00	2	40.00	f	2024-10-03 23:23:54+00	2024-10-24 01:54:12.840007+00	on_time	1	4	3	3	2	162	1
260	b51cd0ec-670d-42ec-adf0-d70c5ea8377b	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	75.00	75.00	2	75.00	f	2024-10-08 00:42:05+00	2024-11-09 01:33:34.928417+00	moderate_default	1	4	3	3	2	173	1
533	2c50d019-0d5c-439b-9c1d-4ebc07d08289	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	60.00	60.00	2	60.00	f	2024-11-25 22:13:15+00	2024-12-04 23:05:30.268592+00	on_time	1	4	3	3	2	261	1
237	30e36ebd-774d-43be-b496-283050db341c	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	80.00	70.00	2	75.00	t	2024-10-03 23:22:16+00	2024-12-06 00:22:04.280276+00	mild_default	1	4	3	3	2	161	1
259	4a43c2e6-34ef-4b6d-8291-4f0c3b647b16	pending	30.00	50.00	20.00	2024-10-15	2024-10-30	15		1.33	\N	50.00	0.00	1	50.00	f	2024-10-08 00:39:28+00	2024-10-24 19:37:51.64787+00	on_time	1	4	3	3	2	77	1
528	b52b4bf5-5c6e-41fd-b476-3bc3ee08cebe	pending	100.00	140.00	40.00	2024-12-13	2024-12-27	45		0.27	\N	140.00	0.00	3	46.67	f	2024-11-26 21:44:21+00	2024-12-03 00:55:17.79188+00	on_time	1	4	3	3	2	40	1
245	80082d9e-0620-48aa-928a-6b056cf3f745	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-06 00:04:04+00	2024-11-16 21:14:57.379721+00	moderate_default	1	4	3	3	2	166	1
251	8f89406e-a449-4931-98b4-1107213989e3	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	75.00	75.00	2	75.00	f	2024-10-06 00:15:15+00	2024-11-09 00:12:04.942341+00	moderate_default	1	4	3	3	2	171	1
261	a546bdd0-e362-4b02-8168-20afd645de95	pending	100.00	140.00	40.00	2024-10-15	2024-10-30	60		0.20	\N	60.00	80.00	2	70.00	t	2024-07-27 00:47:54+00	2024-11-20 23:59:47.289146+00	mild_default	1	4	4	3	2	174	1
239	beda4a45-1e16-418a-ba3b-5371cf08b011	pending	150.00	255.00	105.00	2024-10-15	2024-10-30	45		0.47	\N	170.00	85.00	3	85.00	f	2024-10-03 23:25:39+00	2024-11-26 21:44:25.379201+00	moderate_default	1	4	3	3	2	163	1
233	a50e2a69-5cb1-4a73-a8cf-c0902bfebcea	pending	200.00	400.00	200.00	2024-08-30	2024-09-15	60		0.50	\N	155.00	245.00	4	100.00	t	2024-08-24 22:34:30+00	2024-11-21 19:09:41.667805+00	recurrent_default	1	4	3	3	2	160	1
256	be110709-c475-48dc-ab18-bab08fda3c05	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	75.00	75.00	2	75.00	f	2024-10-08 00:35:34+00	2024-11-08 23:41:28.32627+00	moderate_default	1	4	3	3	2	104	1
264	d4c9aaba-66f5-4c1c-8bc6-20f2be299d35	pending	40.00	90.00	50.00	2024-10-15	2024-10-30	30		1.25	\N	0.00	90.00	2	45.00	f	2024-10-09 00:52:18+00	2024-10-18 00:53:14.415334+00	on_time	1	4	3	3	2	175	1
254	bb8480bd-f5de-4c28-8a1b-4ef4ed2ea62f	pending	50.00	80.00	30.00	2024-10-15	2024-10-30	30		0.60	\N	160.00	-80.00	2	40.00	f	2024-10-06 00:17:58+00	2024-11-21 00:27:45.390231+00	moderate_default	1	4	3	3	2	189	1
266	d3052858-b8e5-4cdb-b305-d19e91aa7b9e	pending	300.00	600.00	300.00	2024-10-15	2024-10-30	45		0.67	\N	180.00	420.00	3	200.00	f	2024-10-10 22:40:29+00	2024-10-24 23:22:59.129727+00	on_time	1	4	3	3	2	119	1
246	0541cf1a-4b97-438e-bf1f-686498ff1c38	pending	100.00	140.00	40.00	2024-10-15	2024-10-30	30		0.40	\N	140.00	0.00	2	70.00	f	2024-10-07 00:05:15+00	2024-11-08 23:04:19.632945+00	moderate_default	1	4	3	3	2	167	1
258	1ce873b1-0628-4b90-abcf-2e185701d234	pending	1000.00	1200.00	200.00	2024-10-15	2024-10-30	30		0.20	\N	100.00	1100.00	30	40.00	t	2024-10-08 00:38:51+00	2024-10-19 23:34:15.235264+00	mild_default	1	4	1	3	2	20	1
255	f626d77d-81e2-43e5-a00a-64a06423f6d9	pending	90.00	220.00	130.00	2024-09-15	2024-09-30	30		1.44	\N	195.00	25.00	2	110.00	t	2024-09-03 00:31:14+00	2024-10-19 22:50:36.928567+00	mild_default	1	4	3	3	2	172	1
250	308b2a4d-45d1-45d7-96f4-0c3f59dacc14	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-07 00:11:51+00	2024-10-19 23:18:51.319667+00	on_time	1	4	3	3	2	170	1
262	44dccc06-3bbc-4565-abf9-76aa1793fc11	pending	50.00	90.00	40.00	2024-10-15	2024-10-30	30		0.80	\N	90.00	0.00	2	45.00	f	2024-10-09 00:50:53+00	2024-11-08 23:37:03.917816+00	moderate_default	1	4	3	3	2	144	1
244	d5b6bada-4dd4-4ca2-8d93-8f0d35df1940	pending	50.00	90.00	40.00	2024-10-15	2024-10-30	30		0.80	\N	90.00	0.00	2	45.00	f	2024-10-06 00:03:30+00	2024-10-28 00:35:31.442906+00	on_time	1	4	3	3	2	21	1
511	f4434faa-829d-4500-b711-fcb2dfbfdd97	pending	250.00	400.00	150.00	2024-11-30	2024-12-15	30		0.60	\N	0.00	400.00	2	200.00	f	2024-11-21 00:22:26+00	2024-11-27 00:23:00.785425+00	on_time	1	4	3	3	2	43	1
274	9dfe7250-9f21-4483-b6ce-d4b331b4045e	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	0.00	150.00	1	150.00	f	2024-10-11 22:52:56+00	2024-10-19 22:53:22.124646+00	on_time	1	4	4	3	2	27	1
523	e3fee0eb-4871-4f49-8f0f-c65ce8d868bb	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	120.00	2	60.00	f	2024-11-22 01:19:01+00	2024-11-27 01:19:03.963844+00	on_time	1	4	3	3	2	245	1
276	6b69a9cd-d47a-4712-89e5-a14e8d24ba5b	pending	150.00	260.00	110.00	2024-10-15	2024-10-30	30		0.73	\N	0.00	260.00	2	130.00	f	2024-10-11 22:53:22+00	2024-10-19 22:54:14.443057+00	on_time	1	4	3	3	2	172	1
286	b01b4b02-34c0-4ccb-8a8d-484f3b2a3232	pending	200.00	360.00	160.00	2024-09-15	2024-09-30	45		0.53	\N	280.00	80.00	3	120.00	t	2024-08-31 01:15:33+00	2024-11-10 20:24:19.120033+00	mild_default	1	4	3	3	2	182	1
280	bf8dac48-6d58-4402-ae42-39b7504619a0	pending	100.00	180.00	80.00	2024-10-15	2024-10-30	30		0.80	\N	148.00	32.00	2	90.00	t	2024-10-14 23:20:16+00	2024-11-27 21:32:57.173564+00	mild_default	1	4	3	3	2	74	1
510	fb13b7d3-7057-4b8a-9da0-ce2ffe1daeb3	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	45		0.33	\N	50.00	100.00	3	50.00	f	2024-11-21 00:13:25+00	2024-11-27 21:46:39.382908+00	on_time	1	4	3	3	2	253	1
73	c5f8748f-16c8-4913-97f1-de3250c6f5e7	pending	100.00	140.00	40.00	2024-09-15	2024-09-30	30		0.40	\N	280.00	-140.00	2	70.00	t	2024-09-03 01:29:49+00	2024-10-19 23:28:42.920431+00	moderate_default	1	4	3	3	2	61	1
281	7cc8612b-6d2e-4338-8c87-c88873607378	pending	50.00	90.00	40.00	2024-10-15	2024-10-30	30		0.80	\N	90.00	0.00	2	45.00	t	2024-10-14 23:20:44+00	2024-12-04 22:12:35.987312+00	mild_default	1	4	3	3	2	178	1
296	4ac42aa2-dcd7-4595-8cba-03e4ac90aec4	pending	100.00	160.00	60.00	2024-10-30	2024-11-15	60		0.30	\N	80.00	80.00	4	40.00	f	2024-10-16 18:46:47+00	2024-12-05 23:39:19.588704+00	moderate_default	1	4	3	3	2	190	1
284	434e8c0d-680b-49f4-a843-bdfe0bf8e71b	pending	50.00	80.00	30.00	2024-10-15	2024-10-30	30		0.60	\N	0.00	80.00	2	40.00	f	2024-10-14 23:31:28+00	2024-10-19 23:32:13.527919+00	on_time	1	4	3	3	2	180	1
277	554eafce-9de3-4169-bb03-b595e62bdbd1	pending	100.00	130.00	30.00	2024-10-15	2024-10-30	30		0.30	\N	130.00	0.00	2	65.00	f	2024-10-11 22:54:26+00	2024-11-02 00:49:03.53333+00	moderate_default	1	4	3	3	2	177	1
309	8e321b15-7477-42e4-b5ec-d5a38b2bdb5f	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-16 19:52:29+00	2024-11-26 21:10:29.590509+00	moderate_default	1	4	3	3	2	195	1
299	9fddcb53-a416-4a3b-9a07-3c02fcef54bb	pending	100.00	140.00	40.00	2024-10-30	2024-11-15	30		0.40	\N	140.00	0.00	2	70.00	f	2024-10-16 19:19:54+00	2024-11-26 19:19:53.377579+00	moderate_default	1	4	3	3	2	55	1
285	6cff7d30-08f0-4f84-b719-ecbc15383db9	pending	100.00	150.00	50.00	2024-07-15	2024-07-30	30		0.50	\N	200.00	-50.00	2	75.00	t	2024-07-04 01:13:48+00	2024-11-09 00:25:01.626055+00	recurrent_default	1	4	3	3	2	181	1
302	1a5b888f-4dd1-4061-be67-b0b07c70dc9b	pending	150.00	270.00	120.00	2024-10-30	2024-11-15	45		0.53	\N	245.00	25.00	3	90.00	f	2024-10-16 19:23:41+00	2024-12-05 23:34:05.27496+00	moderate_default	1	4	3	3	2	63	1
301	ecf27223-9acb-4710-bc7e-b4aee8611e2f	pending	200.00	315.00	115.00	2024-10-30	2024-11-15	45		0.38	\N	145.00	170.00	3	105.00	t	2024-10-16 19:21:28+00	2024-12-06 00:54:50.088243+00	mild_default	1	4	3	3	2	193	1
290	557e87ba-d937-41eb-8a6a-e04b7ce0ba8a	pending	200.00	280.00	80.00	2024-09-30	2024-10-15	30		0.40	\N	0.00	280.00	1	280.00	f	2024-09-14 23:15:46+00	2024-10-23 23:16:24.885591+00	on_time	1	4	4	3	2	99	1
291	b7eb7b2a-93e8-44f1-99f4-a93d82765491	pending	50.00	90.00	40.00	2024-09-30	2024-10-15	30		0.80	\N	0.00	90.00	2	45.00	t	2024-09-16 23:17:10+00	2024-10-23 23:17:39.527936+00	severe_default	1	4	3	3	2	107	1
292	63cb527a-0710-4853-bd4e-b37a565a43dd	pending	20.00	30.00	10.00	2024-09-15	2024-09-30	30		0.50	\N	0.00	30.00	1	30.00	t	2024-09-09 23:40:22+00	2024-10-23 23:41:24.020208+00	severe_default	1	4	4	3	2	188	1
293	ef4b446b-e0dc-482b-a198-8f4f35741a0f	pending	200.00	280.00	80.00	2024-10-30	2024-11-15	30		0.40	\N	0.00	280.00	2	140.00	f	2024-10-16 18:24:37+00	2024-10-24 18:25:09.82608+00	on_time	1	4	3	3	2	99	1
297	c6c219d1-1610-41cd-9567-f14d6216dc14	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-16 18:48:21+00	2024-11-09 01:23:45.328541+00	on_time	1	4	3	3	2	191	1
298	6f2795d3-bdcf-43c2-9cff-b2f1d3019f77	pending	200.00	300.00	100.00	2024-09-15	2024-09-30	30		0.50	\N	330.00	-30.00	2	150.00	t	2024-08-31 19:01:19+00	2024-10-24 19:13:38.032078+00	moderate_default	1	4	3	3	2	192	1
306	a5f2fea3-114d-49ef-94d2-611c996b8354	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-16 19:48:17+00	2024-11-22 00:09:55.381175+00	moderate_default	1	4	3	3	2	189	1
307	d1dcd47e-0752-4ceb-a12b-814349eb6dcd	pending	75.00	130.00	55.00	2024-10-30	2024-11-15	30		0.73	\N	120.00	10.00	2	65.00	f	2024-10-16 19:49:14+00	2024-11-09 00:24:19.644333+00	on_time	1	4	3	3	2	194	1
273	5432e997-9640-4f66-92ad-3668b8622df4	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	60.00	90.00	2	75.00	t	2024-10-10 22:42:57+00	2024-11-09 00:28:07.925389+00	mild_default	1	4	3	3	2	185	1
304	cc2b1432-1d20-46fe-a130-d0c2f140db83	pending	100.00	180.00	80.00	2024-10-30	2024-11-15	45		0.53	\N	0.00	180.00	3	60.00	f	2024-10-16 19:27:24+00	2024-10-24 19:28:00.851558+00	on_time	1	4	3	3	2	129	1
305	5d0bd54c-833f-494d-bede-76b5f6232ec2	pending	50.00	80.00	30.00	2024-10-30	2024-11-15	30		0.60	\N	0.00	80.00	1	80.00	f	2024-10-16 19:39:04+00	2024-10-24 19:39:27.934765+00	on_time	1	4	4	3	2	77	1
303	349ebbfa-5218-4fd6-a61c-cb3d6b95f290	pending	200.00	330.00	130.00	2024-10-30	2024-11-15	45		0.43	\N	330.00	0.00	3	110.00	f	2024-10-16 19:25:58+00	2024-11-26 21:47:38.481056+00	moderate_default	1	4	3	3	2	192	1
282	b912dc59-f830-4d5a-8771-f0a3a77ad07a	pending	100.00	140.00	40.00	2024-10-15	2024-10-30	30		0.40	\N	150.00	-10.00	2	70.00	f	2024-10-14 23:29:44+00	2024-11-12 18:26:36.229935+00	on_time	1	4	3	3	2	61	1
130	1e5fc3af-2074-4981-b8e1-2e4b14e437d1	pending	150.00	240.00	90.00	2024-09-30	2024-10-15	45		0.40	\N	160.00	80.00	3	80.00	t	2024-09-14 22:26:20+00	2024-10-24 19:47:16.137235+00	moderate_default	1	4	3	3	2	88	1
308	8de2cec2-c532-4a41-b61b-a6ab4135e980	pending	250.00	510.00	260.00	2024-10-30	2024-11-15	45		0.69	\N	0.00	510.00	3	170.00	f	2024-10-16 19:51:42+00	2024-10-24 19:52:29.432123+00	on_time	1	4	3	3	2	57	1
287	f406a054-9d7c-48f6-8eb9-06538303d704	pending	100.00	140.00	40.00	2024-09-30	2024-10-15	20		0.60	\N	140.00	0.00	2	70.00	t	2024-09-18 01:17:15+00	2024-11-02 00:31:08.946997+00	moderate_default	1	4	3	3	2	183	1
300	54c13ffa-cea7-4c7c-90d2-36dcae11691f	pending	300.00	525.00	225.00	2024-10-30	2024-11-15	45		0.50	\N	175.00	350.00	3	175.00	f	2024-10-16 19:20:43+00	2024-11-09 00:49:26.522442+00	on_time	1	4	3	3	2	5	1
288	a96dc139-e4f9-46e1-a195-9902ad3ebc04	pending	100.00	150.00	50.00	2024-10-15	2024-10-30	30		0.50	\N	120.00	30.00	2	75.00	t	2024-10-03 21:47:18+00	2024-11-22 00:45:45.487221+00	mild_default	1	4	3	3	2	54	1
330	8526a464-c194-4cfa-a943-70363650163e	to_solve	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	0.00	150.00	1	150.00	f	2024-10-21 23:25:07+00	2024-11-20 21:37:04.077314+00	on_time	1	4	4	3	2	201	1
325	bf5c8180-800b-41d5-98c5-dd4d17debf9f	pending	100.00	140.00	40.00	2024-10-30	2024-11-15	30		0.40	\N	140.00	0.00	2	70.00	f	2024-10-20 23:11:55+00	2024-11-09 01:41:30.42699+00	on_time	1	4	3	3	2	183	1
314	695ae4fd-cfc3-440d-acf1-db3f0b73e4df	pending	400.00	600.00	200.00	2024-10-30	2024-11-15	90		0.17	\N	40.00	560.00	6	100.00	t	2024-10-17 21:46:55+00	2024-11-26 22:22:06.788298+00	mild_default	1	4	3	3	2	196	1
316	58f2ec33-d1f9-4bc2-9357-b7c4d6d4fc08	pending	500.00	880.00	380.00	2024-10-30	2024-11-15	30		0.76	\N	0.00	880.00	1	880.00	f	2024-10-17 21:58:46+00	2024-10-24 21:59:12.845057+00	on_time	1	4	4	3	2	93	1
320	119496d8-3485-4034-90ac-144c4111f1f6	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	130.00	20.00	2	75.00	t	2024-10-17 22:00:33+00	2024-12-05 23:29:21.382539+00	mild_default	1	4	3	3	2	82	1
315	1f7b1fcf-446a-4cb1-a7c6-85f131563f34	pending	300.00	550.00	250.00	2024-10-30	2024-11-15	30		0.83	\N	550.00	0.00	2	275.00	f	2024-10-17 21:57:34+00	2024-11-26 21:13:38.266968+00	moderate_default	1	4	3	3	2	197	1
335	3760b9ab-0d20-495b-bcae-a27eb41b194b	pending	100.00	140.00	40.00	2024-08-15	2024-08-30	30		0.40	\N	65.00	75.00	2	70.00	t	2024-07-27 00:19:31+00	2024-12-03 00:31:43.281142+00	recurrent_default	1	4	3	3	9	205	1
333	97209164-5e99-4d83-9989-a595d9258585	pending	100.00	200.00	100.00	2024-07-30	2024-08-15	60		0.50	\N	200.00	0.00	4	50.00	t	2024-07-15 00:10:33+00	2024-11-01 22:07:18.558534+00	recurrent_default	1	4	3	3	2	204	1
345	f5e62cbf-5410-40e0-90d4-33e5ea50395f	pending	25.00	50.00	25.00	2024-10-30	2024-11-15	30		1.00	\N	0.00	50.00	1	50.00	f	2024-10-23 23:48:03+00	2024-10-27 23:48:06.720665+00	on_time	1	4	4	3	2	54	1
340	2b58876c-2c36-43ba-9414-b1b9bc732380	pending	200.00	280.00	80.00	2024-10-30	2024-11-15	30		0.40	\N	280.00	0.00	1	280.00	f	2024-10-22 23:23:35+00	2024-11-21 00:50:46.187533+00	on_time	1	4	4	3	2	210	1
311	e9473563-d447-43a9-9b91-0523e9427ef7	pending	200.00	400.00	200.00	2024-10-30	2024-11-15	60		0.50	\N	300.00	100.00	4	100.00	f	2024-10-17 21:24:31+00	2024-12-03 00:51:15.276707+00	moderate_default	1	4	3	3	2	34	1
348	47da994d-a94d-485e-a0e9-5b4130d8556a	pending	100.00	140.00	40.00	2024-11-15	2024-11-30	30		0.40	\N	140.00	0.00	2	70.00	f	2024-10-25 00:13:41+00	2024-12-04 21:56:49.395276+00	moderate_default	1	4	3	3	2	126	1
328	f576cf94-db76-44bb-87af-01f08b560b37	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	75.00	75.00	2	75.00	f	2024-10-20 23:12:23+00	2024-11-08 23:33:49.527045+00	on_time	1	4	3	3	2	30	1
347	52ea78c1-1e93-40be-b5dc-7ea1eb838a81	pending	50.00	90.00	40.00	2024-10-30	2024-11-15	30		0.80	\N	95.00	-5.00	2	45.00	f	2024-10-24 23:59:17+00	2024-12-04 22:04:09.687362+00	moderate_default	1	4	3	3	2	215	1
512	0ffdac21-aafe-4c3b-884e-47d3fdcc5cb9	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	30		0.50	\N	75.00	75.00	2	75.00	f	2024-11-21 00:23:31+00	2024-12-04 22:50:42.186482+00	on_time	1	4	3	3	2	254	1
317	44e367ec-ac16-4a78-af6e-02b67f3568f8	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	120.00	30.00	2	75.00	t	2024-10-17 21:59:13+00	2024-12-06 00:46:28.167752+00	mild_default	1	4	3	3	2	113	1
322	9fdab794-7a72-4432-ac8a-207314fa31fb	pending	50.00	70.00	20.00	2024-07-30	2024-08-15	12		1.00	\N	55.00	15.00	12	5.83	t	2024-07-16 22:48:44+00	2024-10-24 22:56:37.743701+00	recurrent_default	1	4	1	3	2	198	1
351	5006961e-8869-40bd-b503-61781cc36193	pending	100.00	160.00	60.00	2024-10-30	2024-11-15	30		0.60	\N	80.00	80.00	2	80.00	f	2024-10-26 00:30:39+00	2024-11-09 00:04:54.022616+00	on_time	1	4	3	3	2	216	1
329	8beab437-9621-4d50-b09e-85e303a6bc52	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-10-20 23:15:47+00	2024-10-24 23:17:14.063386+00	on_time	1	4	3	3	2	200	1
331	f36dbc00-a86f-4d89-b256-50553564c490	pending	30.00	50.00	20.00	2024-10-30	2024-11-15	30		0.67	\N	0.00	50.00	2	25.00	f	2024-10-21 23:26:08+00	2024-10-24 23:27:26.335067+00	on_time	1	4	3	3	2	202	1
332	9059f499-7d55-4b07-b194-2f3160f2f1b0	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-10-21 23:27:26+00	2024-10-24 23:28:24.628202+00	on_time	1	4	3	3	2	203	1
336	70ad6642-54d6-4c67-be07-5c51f51f4d0f	pending	100.00	165.00	65.00	2024-08-17	2024-08-30	45		0.43	\N	165.00	0.00	3	55.00	t	2024-07-24 18:37:58+00	2024-10-25 18:40:56.221906+00	mild_default	1	4	3	3	2	206	1
334	9babb45d-6096-41e9-90c9-384748a9c94c	pending	50.00	90.00	40.00	2024-07-30	2024-08-15	30		0.80	\N	90.00	0.00	2	45.00	t	2024-07-16 00:16:19+00	2024-10-25 00:19:05.236938+00	recurrent_default	1	4	3	3	2	205	1
337	71132042-6400-40e2-9ac6-d596e5457ca7	pending	50.00	90.00	40.00	2024-10-30	2024-11-15	30		0.80	\N	0.00	90.00	2	45.00	f	2024-10-21 18:53:01+00	2024-10-26 18:54:12.826146+00	on_time	1	4	3	3	2	207	1
341	e5dc3c14-b7c8-4792-a4e4-5320149559dd	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-22 23:31:14+00	2024-11-20 22:58:54.487475+00	moderate_default	1	4	3	3	2	211	1
342	19b6a438-7634-4062-909c-308979f5cc4e	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-10-22 23:34:41+00	2024-10-27 23:35:50.541966+00	on_time	1	4	3	3	2	212	1
346	81d58f52-4c46-4e1f-b038-ce81917bafb4	pending	60.00	100.00	40.00	2024-10-30	2024-11-15	30		0.67	\N	100.00	0.00	2	50.00	f	2024-10-22 23:48:07+00	2024-11-22 00:13:12.589532+00	moderate_default	1	4	3	3	2	214	1
313	06ad985d-293c-4d9a-8e38-80568fb40abf	pending	200.00	300.00	100.00	2024-10-30	2024-11-15	30		0.50	\N	400.00	-100.00	1	300.00	f	2024-10-17 21:25:15+00	2024-11-02 00:46:26.319785+00	on_time	1	4	4	3	2	64	1
310	495ce78c-ee62-4ce3-8992-6ee779bd848b	pending	300.00	540.00	240.00	2024-10-30	2024-11-15	60		0.40	\N	280.00	260.00	4	135.00	f	2024-10-17 21:07:20+00	2024-11-26 23:18:33.977129+00	moderate_default	1	4	3	3	2	85	1
343	6208971b-23e9-4e3e-a94b-a0efd367afab	pending	150.00	230.00	80.00	2024-10-30	2024-11-15	30		0.53	\N	230.00	0.00	2	115.00	f	2024-10-23 23:45:47+00	2024-11-20 23:13:48.266249+00	moderate_default	1	4	3	3	2	213	1
339	93bd9fcb-c40d-4cbf-bb76-bb1f1dfe2ef7	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-22 23:20:25+00	2024-11-26 19:48:19.365638+00	moderate_default	1	4	3	3	2	209	1
349	35287a17-2b4a-4855-a34b-38c32a056afd	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-10-25 00:14:39+00	2024-10-28 00:15:42.84791+00	on_time	1	4	3	3	2	112	1
350	96df5046-94c0-4e23-b0fe-9568b689b074	pending	180.00	216.00	36.00	2024-11-15	2024-11-30	45		0.13	\N	0.00	216.00	3	72.00	f	2024-10-26 00:29:50+00	2024-10-28 00:30:39.474899+00	on_time	1	4	3	3	2	74	1
338	243848f2-5824-45a9-badd-70b814d6ab58	pending	150.00	250.00	100.00	2024-10-30	2024-11-15	30		0.67	\N	250.00	0.00	2	125.00	f	2024-10-21 23:16:10+00	2024-11-22 01:01:42.369575+00	moderate_default	1	4	3	3	2	208	1
323	b8ea1218-db63-4e31-8aa9-3a81863e8fdb	pending	100.00	140.00	40.00	2024-10-30	2024-11-15	30		0.40	\N	160.00	-20.00	2	70.00	f	2024-10-19 23:06:27+00	2024-11-20 23:37:23.38975+00	moderate_default	1	4	3	3	2	131	1
352	de5920e9-dca2-433f-b994-a5a0ff531eef	pending	100.00	140.00	40.00	2024-10-30	2024-11-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-10-26 00:32:40+00	2024-10-28 00:34:35.441957+00	on_time	1	4	3	3	2	217	1
373	ef98a469-4464-4b6c-a890-174d666488b6	pending	20.00	25.00	5.00	2024-11-15	2024-11-30	8		0.94	\N	0.00	25.00	8	3.13	f	2024-10-30 22:54:17+00	2024-11-08 22:54:19.723838+00	on_time	1	4	1	3	2	111	1
354	85f74dcf-d786-42c5-b2a9-96ec582f358a	pending	60.00	100.00	40.00	2024-10-31	2024-11-15	30		0.67	\N	0.00	100.00	2	50.00	f	2024-10-27 01:03:09+00	2024-10-29 01:08:27.134929+00	on_time	1	4	3	3	2	219	1
356	7e1c8fc1-4985-46db-a410-e7602690880e	pending	100.00	140.00	40.00	2024-10-31	2024-11-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-10-27 01:09:02+00	2024-10-29 01:09:03.826831+00	on_time	1	4	3	3	2	21	1
357	881cfef8-6d4a-4188-9ddd-313aa2caa69b	pending	200.00	300.00	100.00	2024-10-31	2024-11-15	30		0.50	\N	0.00	300.00	2	150.00	f	2024-10-27 01:09:04+00	2024-10-29 01:10:08.455674+00	on_time	1	4	3	3	2	220	1
358	9fbc46c4-06f3-484b-9050-e37701337579	pending	300.00	500.00	200.00	2024-10-31	2024-11-15	30		0.67	\N	0.00	500.00	2	250.00	f	2024-10-27 01:10:08+00	2024-10-29 01:11:12.23848+00	on_time	1	4	3	3	2	33	1
366	b9152fc1-571b-4c52-9227-1d8c5bca7238	pending	150.00	250.00	100.00	2024-03-15	2024-03-30	90		0.22	\N	75.00	175.00	3	83.33	t	2024-03-02 21:42:21+00	2024-11-05 21:54:16.027664+00	recurrent_default	1	4	4	3	2	223	1
79	b1695778-b71b-4e4e-9167-4146d5db1664	pending	200.00	345.00	145.00	2024-08-15	2024-09-30	45		0.48	\N	350.00	-5.00	3	115.00	t	2024-08-09 17:58:59+00	2024-11-27 01:20:23.584667+00	recurrent_default	1	4	3	3	2	67	1
376	fe2fa3a1-97c0-4cce-a818-00a5ea0a2e5f	pending	200.00	360.00	160.00	2024-11-15	2024-11-30	45		0.53	\N	245.00	115.00	3	120.00	f	2024-11-01 00:00:24+00	2024-12-05 23:20:45.61288+00	moderate_default	1	4	3	3	2	228	1
513	43f2b1d9-be0e-4979-a14c-47ae831f310a	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	30		0.50	\N	75.00	75.00	2	75.00	f	2024-11-21 00:25:26+00	2024-12-04 22:35:49.370192+00	on_time	1	4	3	3	2	255	1
367	ce443cad-1edc-4f10-aa3a-d0b359890d60	pending	50.00	90.00	40.00	2024-08-15	2024-08-30	30		0.80	\N	0.00	90.00	2	45.00	t	2024-07-31 21:58:00+00	2024-11-05 22:00:10.038005+00	critical_default	1	4	3	3	2	224	1
377	fa7ba87d-ec64-47ef-98ad-15b2ffae4fff	pending	200.00	300.00	100.00	2024-11-15	2024-11-30	30		0.50	\N	0.00	300.00	2	150.00	f	2024-11-02 00:29:52+00	2024-11-09 00:30:19.529262+00	on_time	1	4	3	3	2	50	1
360	c86b515d-fa80-473e-abb6-43b3f2f69ce2	pending	100.00	130.00	30.00	2024-11-15	2024-11-30	30		0.30	\N	130.00	0.00	1	130.00	f	2024-10-28 21:47:37+00	2024-11-20 22:52:45.36537+00	on_time	1	4	4	3	2	84	1
386	be853fcd-a900-4006-b7ad-3cfd0a5ed01a	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	70.00	80.00	2	75.00	f	2024-11-02 01:34:33+00	2024-11-21 19:08:32.689801+00	on_time	1	4	3	3	2	229	1
380	307f6d29-a888-4fcc-a1be-558ae5d49e91	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	45		0.33	\N	95.00	55.00	3	50.00	f	2024-11-02 01:21:08+00	2024-12-05 23:21:29.472105+00	moderate_default	1	4	3	3	2	108	1
362	0080dcf7-78a4-40e0-ae20-f5670a2a0691	pending	50.00	80.00	30.00	2024-11-15	2024-11-30	30		0.60	\N	80.00	0.00	1	80.00	f	2024-10-30 22:12:53+00	2024-11-21 19:01:51.693778+00	on_time	1	4	4	3	2	42	1
365	b9491821-6781-418c-a87b-cf98bf8ebd0d	pending	100.00	150.00	50.00	2024-10-30	2024-11-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-10-18 21:40:33+00	2024-11-05 21:42:21.333249+00	on_time	1	4	3	3	2	222	1
353	a463eea0-0b0d-428a-b86e-fa0bb23c04a2	pending	50.00	80.00	30.00	2024-10-30	2024-11-15	30		0.60	\N	70.00	0.00	2	40.00	f	2024-10-27 01:01:47+00	2024-11-12 22:26:16.645167+00	on_time	1	4	3	3	2	218	1
374	ea53bc46-372e-4083-931e-5de03b69b039	pending	50.00	70.00	20.00	2024-07-31	2024-08-15	30		0.40	\N	50.00	20.00	2	35.00	t	2024-07-26 23:00:01+00	2024-11-08 23:02:19.135371+00	recurrent_default	1	4	3	3	2	227	1
370	38366152-2fe2-440a-9800-0cd2c7858eeb	pending	200.00	330.00	130.00	2024-08-31	2024-09-23	45		0.43	\N	230.00	100.00	3	110.00	t	2024-07-16 01:35:31+00	2024-11-09 00:59:47.535964+00	mild_default	1	4	3	3	2	226	1
368	1ba9dac1-9b9e-4d70-9aae-edd924ccb227	pending	500.00	810.00	310.00	2024-05-15	2024-05-30	75		0.25	\N	200.00	610.00	5	162.00	t	2024-04-30 22:00:10+00	2024-11-05 22:07:20.528078+00	recurrent_default	1	4	3	3	2	225	1
369	cced3a38-5cb4-4989-892b-24b50a296402	pending	475.00	1025.00	550.00	2024-10-15	2024-10-30	60		0.58	\N	0.00	1025.00	4	256.25	t	2024-09-29 22:19:36+00	2024-11-05 22:20:17.257562+00	severe_default	1	4	3	3	2	94	1
359	8b9f8c0e-361c-4c03-b122-c9345f0088e4	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	50.00	100.00	1	150.00	f	2024-10-28 21:44:16+00	2024-12-04 21:29:29.573899+00	on_time	1	4	4	3	2	157	1
375	e904b26c-ee17-4ec6-a726-14208d32fafd	pending	500.00	840.00	340.00	2024-11-15	2024-11-30	45		0.45	\N	560.00	280.00	3	280.00	f	2024-10-31 23:10:35+00	2024-12-03 00:58:18.88499+00	moderate_default	1	4	3	3	2	75	1
378	80fdf081-5755-4f68-aa62-a139fd64dddd	pending	200.00	360.00	160.00	2024-11-15	2024-11-30	45		0.53	\N	0.00	360.00	3	120.00	f	2024-11-02 01:00:08+00	2024-11-09 01:00:47.658551+00	on_time	1	4	3	3	2	226	1
364	f37bd805-4972-40a9-a853-55536c27fa9e	pending	400.00	800.00	400.00	2024-11-15	2024-11-30	30		1.00	\N	500.00	300.00	2	400.00	f	2024-10-31 00:46:37+00	2024-11-20 23:27:36.164919+00	on_time	1	4	3	3	2	64	1
220	6843660f-14f7-4a8c-82d2-49e862f6bc48	pending	100.00	140.00	40.00	2024-10-15	2024-10-30	30		0.40	\N	145.00	-5.00	2	70.00	f	2024-10-01 03:02:24+00	2024-11-08 23:37:52.034934+00	moderate_default	1	4	3	3	2	153	1
363	0b09a462-eeca-42cc-8cb1-7a9272ef7fb0	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-10-31 00:22:42+00	2024-11-26 19:41:58.882217+00	on_time	1	4	3	3	2	110	1
379	677f294b-50b5-4e04-ad70-c12ce4ea08c5	pending	100.00	130.00	30.00	2024-11-15	2024-11-30	30		0.30	\N	0.00	130.00	2	65.00	f	2024-11-02 01:11:33+00	2024-11-09 01:13:33.93476+00	on_time	1	4	3	3	2	164	1
381	5bd21819-ae9b-4b6d-a1fd-ee82ff2aadc1	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-11-02 01:21:37+00	2024-11-09 01:22:07.518453+00	on_time	1	4	3	3	2	82	1
383	6ff98075-543d-467b-87ad-ea6906619901	pending	150.00	270.00	120.00	2024-11-15	2024-11-30	45		0.53	\N	180.00	90.00	3	90.00	f	2024-11-02 01:23:00+00	2024-12-06 00:45:46.795901+00	moderate_default	1	4	3	3	2	191	1
384	e1811631-f3ec-42e6-a6b0-09ede4eacf1e	pending	150.00	270.00	120.00	2024-11-15	2024-11-30	45		0.53	\N	90.00	180.00	3	90.00	f	2024-11-02 01:27:47+00	2024-11-26 22:05:53.291903+00	on_time	1	4	3	3	2	171	1
385	7fe1d3ae-6110-48f3-adf8-0830caf5eebd	pending	200.00	300.00	100.00	2024-11-15	2024-11-30	45		0.33	\N	0.00	300.00	3	100.00	f	2024-11-02 01:33:53+00	2024-11-09 01:34:33.228719+00	on_time	1	4	3	3	2	16	1
387	4d04c479-8c70-49e5-9677-5aa662675f15	pending	100.00	140.00	40.00	2024-11-15	2024-11-30	60		0.20	\N	0.00	140.00	4	35.00	f	2024-11-02 20:16:09+00	2024-11-10 20:16:40.033662+00	on_time	1	4	3	3	2	44	1
85	fc91f872-219a-4d5f-bdad-f2d25ae769a2	pending	400.00	560.00	160.00	2024-08-27	2024-09-30	60		0.20	\N	525.00	35.00	4	140.00	t	2024-08-13 20:03:47+00	2024-11-12 22:05:19.545462+00	mild_default	1	4	3	3	2	73	1
361	7f0e37d8-9400-4d47-81b5-79c673c9c257	pending	200.00	360.00	160.00	2024-11-15	2024-11-30	45		0.53	\N	120.00	240.00	3	120.00	f	2024-10-29 22:07:26+00	2024-11-20 22:52:10.375241+00	on_time	1	4	3	3	2	221	1
514	9b1640b0-9c95-4cb1-af15-53909e7e2940	pending	750.00	1050.00	300.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	1050.00	1	1050.00	f	2024-11-22 00:45:03+00	2024-11-27 00:49:52.288538+00	on_time	1	4	4	3	2	93	1
431	cd624cc3-e78e-40f7-8ed1-25480c88f9cd	pending	100.00	280.00	180.00	2024-11-15	2024-11-30	30	Se añadió el saldo pendiente del crédito del 21 de Octubre	1.80	\N	280.00	0.00	2	140.00	f	2024-11-08 21:34:29+00	2024-11-26 21:13:00.281773+00	on_time	1	4	3	3	2	201	1
524	a6a0a424-9457-4d35-aba3-31e89f599bd8	pending	300.00	500.00	200.00	2024-11-30	2024-12-15	30		0.67	\N	0.00	500.00	2	250.00	f	2024-11-23 21:27:04+00	2024-11-27 21:28:14.473204+00	on_time	1	4	3	3	2	98	1
26	263cbb62-598d-4013-ae6c-30bde1713f3d	pending	100.00	165.00	65.00	2024-08-24	2024-09-03	30		0.65	\N	155.00	10.00	2	82.50	t	2024-08-03 01:13:17+00	2024-11-27 21:55:39.897279+00	recurrent_default	1	4	3	3	2	21	\N
433	e57cdb40-5258-4fd7-b29a-6ad82dc956e4	pending	150.00	330.00	180.00	2024-11-15	2024-11-30	45		0.80	\N	120.00	210.00	3	110.00	f	2024-11-09 21:53:56+00	2024-11-27 21:42:10.569942+00	on_time	1	4	3	3	2	145	1
398	71c669d4-9afa-428e-ae70-d8ccd756da0f	pending	80.00	110.00	30.00	2024-11-15	2024-11-30	30		0.38	\N	0.00	110.00	2	55.00	f	2024-11-02 20:30:00+00	2024-11-10 20:32:13.62324+00	on_time	1	4	3	3	2	231	1
534	de7d6cd8-8323-45df-aa7a-c2a6f132da71	pending	50.00	60.00	10.00	2024-11-30	2024-12-15	30		0.20	\N	30.00	30.00	1	60.00	f	2024-11-25 22:14:18+00	2024-12-04 23:03:44.585718+00	on_time	1	4	4	3	2	262	1
423	5a9611f1-b41d-463d-b603-7b7536323d2c	pending	200.00	300.00	100.00	2024-09-30	2024-10-15	45		0.33	\N	290.00	10.00	3	100.00	t	2024-09-26 22:00:08+00	2024-12-04 21:32:44.688064+00	mild_default	1	4	3	3	2	51	1
429	3ac3a34f-5c3b-4502-a889-1e4da6c8d9c4	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	130.00	20.00	2	75.00	f	2024-11-08 21:10:44+00	2024-12-04 21:41:29.371825+00	moderate_default	1	4	3	3	2	153	1
402	9493d435-7e26-4656-9d57-5a3735bc5a45	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-11-04 20:45:39+00	2024-11-10 20:46:06.029222+00	on_time	1	4	3	3	2	181	1
417	65d076df-d3a4-442f-8b76-07e0c04d7f0a	pending	50.00	90.00	40.00	2024-11-15	2024-11-30	30		0.80	\N	90.00	0.00	2	45.00	f	2024-11-06 21:00:00+00	2024-12-04 21:48:07.092078+00	moderate_default	1	4	3	3	2	167	1
390	04193e8e-14f0-4f65-aeb8-023fa7267fc5	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	150.00	0.00	2	75.00	f	2024-11-02 20:25:22+00	2024-12-04 21:55:08.978804+00	moderate_default	1	4	3	3	2	206	1
411	0a4f26c6-e4e4-4242-a5a0-74b637231e6f	pending	50.00	90.00	40.00	2024-11-15	2024-11-30	30		0.80	\N	90.00	0.00	2	45.00	f	2024-11-06 20:58:40+00	2024-12-04 21:57:27.489179+00	moderate_default	1	4	3	3	2	144	1
399	9e8ca5da-0814-4e7d-98a9-de03f9dc9c25	pending	100.00	165.00	65.00	2024-11-15	2024-11-30	45		0.43	\N	110.00	55.00	3	55.00	f	2024-11-03 20:37:14+00	2024-12-05 23:36:26.087971+00	moderate_default	1	4	3	3	2	150	1
400	0cb1c152-cdfb-43a1-aa4d-382ea08472dc	pending	400.00	480.00	80.00	2024-11-15	2024-11-30	30		0.20	\N	415.00	65.00	2	240.00	f	2024-11-04 20:37:59+00	2024-12-05 23:58:45.888681+00	moderate_default	1	4	3	3	2	56	1
408	88fd5569-04a1-4af5-80c1-0bf0435612f1	pending	100.00	140.00	40.00	2024-11-15	2024-11-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-04 20:47:00+00	2024-11-10 20:47:01.350631+00	on_time	1	4	3	3	2	40	1
435	ba68783b-0359-4042-bce6-ea9cad12fd0e	pending	100.00	140.00	40.00	2024-11-15	2024-11-16	30		0.40	\N	80.00	60.00	1	140.00	f	2024-11-10 22:04:00+00	2024-12-06 00:52:09.474739+00	on_time	1	4	4	3	2	170	1
401	53f41b0e-f303-44b0-ac28-d0d2677cc3a7	pending	100.00	120.00	20.00	2024-11-15	2024-11-30	60		0.10	\N	60.00	60.00	4	30.00	f	2024-11-04 20:45:07+00	2024-12-06 00:21:32.98624+00	moderate_default	1	4	3	3	2	147	1
388	ddbb5eb5-5fe4-413c-a158-75ccf6acd619	pending	50.00	90.00	40.00	2024-11-15	2024-11-30	30		0.80	\N	40.00	50.00	2	45.00	f	2024-11-02 20:19:08+00	2024-11-26 23:15:17.493475+00	on_time	1	4	3	3	2	230	1
409	9493a2f7-5213-48ea-8048-8f8b002c0147	pending	2000.00	2500.00	500.00	2024-11-15	2024-11-30	30		0.25	\N	510.00	1990.00	30	83.33	t	2024-11-05 20:49:19+00	2024-11-26 19:47:06.177635+00	recurrent_default	1	4	1	3	2	10	1
422	57b9a910-5265-4745-b5b5-23415bbc9858	pending	300.00	570.00	270.00	2024-08-30	2024-09-15	90		0.30	\N	0.00	570.00	6	95.00	t	2024-08-13 21:50:35+00	2024-11-12 21:51:13.423406+00	critical_default	1	4	3	3	2	24	1
424	066664cd-c57a-408a-a8c3-79260ace4481	pending	100.00	150.00	50.00	2024-07-30	2024-08-15	30		0.50	\N	60.00	90.00	2	75.00	t	2024-07-25 22:06:20+00	2024-11-12 22:16:53.132857+00	recurrent_default	1	4	3	3	2	233	1
418	d58aa23a-d553-4408-9cb1-e125d9470007	pending	200.00	380.00	180.00	2024-07-25	2024-07-31	60		0.45	\N	190.00	190.00	4	95.00	t	2024-06-28 17:59:03+00	2024-11-12 18:05:22.833757+00	recurrent_default	1	4	3	3	2	227	1
419	be3aa325-2dac-493f-a29e-e9df03eac9c9	pending	500.00	1000.00	500.00	2024-11-15	2024-11-30	45		0.67	\N	0.00	1000.00	3	333.33	f	2024-10-30 21:22:14+00	2024-11-12 21:22:55.316925+00	on_time	1	4	3	3	2	121	1
427	4b03f32e-36b4-4e61-98f6-682796634a8d	pending	150.00	250.00	100.00	2024-03-15	2024-03-30	60		0.33	\N	0.00	250.00	2	125.00	t	2024-03-02 22:04:23+00	2024-11-14 22:05:44.668587+00	critical_default	1	4	4	3	2	234	1
410	b32ce1c3-c13b-4532-809f-bb6b4d54afc5	pending	150.00	300.00	150.00	2024-11-15	2024-11-30	30		1.00	\N	100.00	200.00	2	150.00	f	2024-11-06 20:58:03+00	2024-11-26 23:07:11.895443+00	on_time	1	4	3	3	2	182	1
430	7a560535-c84d-4ef4-94a4-c4c9091b795e	pending	100.00	130.00	30.00	2024-11-15	2024-11-30	30		0.30	\N	0.00	130.00	1	130.00	f	2024-11-08 21:27:21+00	2024-11-20 21:28:22.791211+00	on_time	1	4	4	3	2	235	1
425	bbeb3c70-be59-49c0-92c7-0393ab27a62f	pending	10.00	50.00	40.00	2024-09-15	2024-09-30	75	Camiseta	1.60	\N	0.00	50.00	5	10.00	t	2024-08-30 22:12:06+00	2024-11-12 22:13:05.436133+00	critical_default	1	4	3	3	10	233	1
426	b080c4a0-172a-450c-b7f1-a490e24bc47a	pending	20.00	35.00	15.00	2024-09-15	2024-09-30	30		0.75	\N	0.00	35.00	2	17.50	t	2024-08-30 22:13:16+00	2024-11-12 22:14:29.63346+00	critical_default	1	4	3	3	2	233	1
428	644f590a-15a2-4f95-940d-b8877ebd4d89	pending	50.00	80.00	30.00	2024-11-15	2024-11-30	30		0.60	\N	80.00	0.00	2	40.00	f	2024-11-08 21:09:32+00	2024-11-20 23:06:54.965017+00	on_time	1	4	3	3	2	218	1
420	f26c692f-9659-4097-8baa-b573c67baa8c	pending	360.00	1200.00	840.00	2024-11-15	2024-11-30	60		1.17	\N	1200.00	0.00	4	300.00	f	2024-11-01 21:24:50+00	2024-11-26 22:03:02.993062+00	on_time	1	4	3	3	2	98	1
432	d8c2d6de-e13c-458d-a750-5eb24b12ae1a	pending	200.00	360.00	160.00	2024-10-15	2024-10-30	45	Reajustado del crédito del 25 de Sept	0.53	\N	360.00	0.00	3	120.00	t	2024-09-30 21:47:30+00	2024-11-20 21:53:47.375644+00	moderate_default	1	4	3	3	2	145	1
436	503ae055-cbc8-437b-a69e-045995d5cd38	pending	40.00	70.00	30.00	2024-11-15	2024-11-30	30		0.75	\N	0.00	70.00	2	35.00	f	2024-11-10 22:05:02+00	2024-11-20 22:06:14.381953+00	on_time	1	4	3	3	2	236	1
437	d42207dd-c26b-49f1-a516-1d7456978ec6	pending	186.00	186.00	0.00	2024-11-15	2024-12-05	30		0.00	\N	0.00	186.00	1	186.00	f	2024-11-10 22:07:04+00	2024-11-20 22:07:28.097535+00	on_time	1	4	4	3	2	61	1
438	abadb788-5e7c-4ad9-ba09-30b0547c4075	pending	30.00	50.00	20.00	2024-11-15	2024-11-30	30		0.67	\N	0.00	50.00	2	25.00	f	2024-11-11 22:40:07+00	2024-11-20 22:47:11.697053+00	on_time	1	4	3	3	2	237	1
439	9069ddef-2382-4ccf-a4c0-24a57a14be83	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	0.00	150.00	1	150.00	f	2024-11-11 22:47:12+00	2024-11-20 22:48:24.298017+00	on_time	1	4	4	3	2	238	1
442	ca032487-c5a2-4963-b911-c6910e668c9e	pending	60.00	85.00	25.00	2024-12-07	2024-12-07	30		0.42	\N	0.00	85.00	1	85.00	f	2024-11-13 23:15:31+00	2024-11-20 23:16:01.784525+00	on_time	1	4	4	3	2	84	1
480	6c03c301-a5b9-4961-857c-838a0af90c58	pending	300.00	380.00	80.00	2024-11-25	2024-11-30	30		0.27	\N	380.00	0.00	1	380.00	f	2024-11-19 00:37:34+00	2024-12-03 00:53:52.265626+00	on_time	1	4	4	3	2	99	1
487	0d12e67a-b7ee-49da-84e4-c3e49c68e922	pending	100.00	180.00	80.00	2024-11-30	2024-12-15	30	Ajustado del crédito del 19 de Nov.	0.80	\N	0.00	80.00	2	90.00	f	2024-11-22 00:57:59+00	2024-11-27 00:51:32.271111+00	on_time	1	4	3	3	2	246	1
488	5a442138-9381-46a6-b42d-2db6d7490957	pending	200.00	280.00	80.00	2024-11-30	2024-12-15	30		0.40	\N	140.00	140.00	2	140.00	f	2024-11-15 18:56:12+00	2024-12-04 21:54:39.587323+00	on_time	1	4	3	3	2	247	1
448	bad5a759-def6-4159-a740-c2630f9c57af	pending	200.00	280.00	80.00	2024-11-15	2024-11-30	30		0.40	\N	0.00	280.00	2	140.00	f	2024-11-13 23:17:01+00	2024-11-20 23:17:03.47678+00	on_time	1	4	3	3	2	66	1
440	cd391410-cbc5-4f90-a162-8bc80bf1003d	pending	100.00	130.00	30.00	2024-11-15	2024-11-30	30		0.30	\N	130.00	0.00	1	130.00	f	2024-11-12 22:52:56+00	2024-12-03 00:32:21.682187+00	on_time	1	4	4	3	2	84	1
459	56ca6b5e-46c3-4a4f-8f6e-79be96312fc5	pending	250.00	460.00	210.00	2024-11-15	2024-11-30	30		0.84	\N	100.00	360.00	2	230.00	t	2024-11-14 23:34:47+00	2024-12-06 00:54:23.673926+00	mild_default	1	4	3	3	2	211	1
515	6037007d-cc4f-43b4-ba93-020ea6f048e7	pending	100.00	180.00	80.00	2024-11-30	2024-12-15	45		0.53	\N	20.00	160.00	3	60.00	f	2024-11-22 00:49:52+00	2024-12-03 00:30:33.70281+00	on_time	1	4	3	3	2	73	1
525	b187e423-52f3-406d-8128-156e1593f09f	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	70.00	70.00	2	70.00	f	2024-11-23 21:28:14+00	2024-12-04 21:33:14.889234+00	on_time	1	4	3	3	2	258	1
471	4807b9c7-675a-4203-ab0a-668489618dbb	pending	200.00	280.00	80.00	2024-11-30	2024-12-15	45		0.27	\N	93.00	187.00	3	93.33	f	2024-11-19 00:14:13+00	2024-12-04 22:35:12.18523+00	on_time	1	4	3	3	2	242	1
469	160cafc7-255d-40d3-8ce4-d864b6b838d7	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	45		0.33	\N	50.00	100.00	3	50.00	f	2024-11-17 19:22:37+00	2024-12-04 22:49:18.669524+00	on_time	1	4	3	3	2	241	1
456	dd3cdb51-38e3-44c2-b747-f54dd87da85a	pending	25.00	40.00	15.00	2024-11-15	2024-11-30	30		0.60	\N	0.00	40.00	2	20.00	f	2024-11-13 23:17:55+00	2024-11-20 23:18:07.691205+00	on_time	1	4	3	3	2	149	1
457	4cf6c9aa-64e7-4a41-8017-c1ace89b938c	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	140.00	1	140.00	f	2024-11-14 23:18:57+00	2024-11-20 23:19:38.994116+00	on_time	1	4	4	3	2	159	1
458	46d14379-4fbe-4914-ac37-7d99c2ca1c93	pending	200.00	280.00	80.00	2024-11-15	2024-11-30	30		0.40	\N	0.00	280.00	2	140.00	f	2024-11-14 23:25:47+00	2024-11-20 23:26:10.382989+00	on_time	1	4	3	3	9	83	1
460	2c264f3b-3f6e-4021-ae9a-a7ac3fcf78b9	pending	100.00	140.00	40.00	2024-11-15	2024-11-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-14 23:40:37+00	2024-11-20 23:41:58.779154+00	on_time	1	4	3	3	2	239	1
465	2e88e3b2-e3b9-4794-9748-cc1de9a0647f	pending	500.00	750.00	250.00	2024-11-30	2024-12-15	30		0.50	\N	0.00	750.00	1	750.00	f	2024-11-16 00:51:29+00	2024-11-21 00:51:54.4747+00	on_time	1	4	4	3	2	93	1
490	df6624a2-b6b4-4ef7-a5e4-ccb19822fa85	pending	150.00	250.00	100.00	2024-11-30	2024-12-15	30		0.67	\N	125.00	125.00	2	125.00	f	2024-11-15 19:43:53+00	2024-12-05 23:31:22.397049+00	on_time	1	4	3	3	2	110	1
389	66ac24e2-13dd-402e-be21-5f2c9bdb39ef	pending	100.00	140.00	40.00	2024-11-15	2024-11-30	75		0.16	\N	120.00	20.00	5	28.00	f	2024-11-02 20:24:40+00	2024-12-06 00:23:42.496222+00	moderate_default	1	4	3	3	2	3	1
461	fe3ac10d-1219-4e32-b76f-9228a9bd4aa4	pending	150.00	240.00	90.00	2024-11-15	2024-11-30	30		0.60	\N	220.00	20.00	2	120.00	f	2024-11-01 00:33:32+00	2024-11-21 00:35:23.270565+00	on_time	1	4	3	3	2	88	1
467	4291f0d3-98c1-41d9-9fb2-b0bf940e1fbf	pending	500.00	800.00	300.00	2024-11-30	2024-12-15	30		0.60	\N	0.00	800.00	1	800.00	f	2024-11-17 19:05:38+00	2024-11-21 19:06:27.168233+00	on_time	1	4	4	3	2	98	1
468	878763be-b576-4ae9-bb61-0161a8f3abba	pending	300.00	550.00	250.00	2024-11-30	2024-12-15	30		0.83	\N	0.00	550.00	1	550.00	f	2024-11-17 19:22:07+00	2024-11-21 19:22:36.885193+00	on_time	1	4	4	3	2	201	1
462	79565a4c-7c09-4e19-9a64-3a94748be310	pending	100.00	140.00	40.00	2024-08-15	2024-08-30	30		0.40	\N	150.00	-10.00	2	70.00	t	2024-07-28 00:42:55+00	2024-11-21 00:46:11.8987+00	recurrent_default	1	4	3	3	2	179	1
470	47886fcb-c43d-4b9f-9ca1-83befa1f787a	pending	75.00	135.00	60.00	2024-11-30	2024-12-15	30		0.80	\N	0.00	135.00	2	67.50	f	2024-11-19 00:10:24+00	2024-11-22 00:11:07.667595+00	on_time	1	4	3	3	2	189	1
463	d32a64c5-ecca-428a-bdb4-19428458b0fe	pending	100.00	140.00	40.00	2024-10-15	2024-11-30	30		0.40	\N	140.00	0.00	2	70.00	t	2024-11-15 00:47:18+00	2024-11-21 00:48:34.589386+00	moderate_default	1	4	3	3	2	179	1
464	dd9c3133-004e-4f01-aaf0-8fddc24f0e1d	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-16 00:48:48+00	2024-11-21 00:49:15.981135+00	on_time	1	4	3	3	2	179	1
31	ee0620fe-2c96-457e-a31b-c014f301a669	pending	10.00	50.00	40.00	2024-09-15	2024-09-30	75	Camiseta	1.60	\N	15.00	35.00	5	10.00	t	2024-09-12 19:51:04+00	2024-11-21 00:50:20.495616+00	recurrent_default	1	4	3	1	1	157	1
472	39f1d941-13a6-4445-af05-5a320b6b465f	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-19 00:32:29+00	2024-11-22 00:34:01.868311+00	on_time	1	4	3	3	2	243	1
479	13b1d3da-6593-4e43-92a5-2a1832b520bd	pending	20.00	35.00	15.00	2024-11-30	2024-12-15	30		0.75	\N	0.00	35.00	2	17.50	f	2024-11-19 00:35:00+00	2024-11-22 00:35:06.289769+00	on_time	1	4	3	3	2	218	1
324	942c44cb-169e-4ad4-a2ce-e2d3ad095f30	pending	100.00	140.00	40.00	2024-10-30	2024-11-15	30		0.40	\N	140.00	0.00	2	70.00	f	2024-10-19 23:07:20+00	2024-11-26 21:06:05.172532+00	moderate_default	1	4	3	3	2	199	1
481	4f67135b-04ef-484b-8eeb-58948238f952	pending	50.00	60.00	10.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	60.00	1	60.00	f	2024-11-19 00:39:07+00	2024-11-22 00:41:31.676983+00	on_time	1	4	4	3	2	244	1
482	97ca4819-a0e2-4a60-b8b1-890067c5be67	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	120.00	2	60.00	f	2024-11-19 00:41:32+00	2024-11-22 00:42:30.888187+00	on_time	1	4	3	3	2	245	1
485	3b48d416-ed4f-40d2-be72-9738340ee73f	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-20 00:48:17+00	2024-11-22 00:52:57.481973+00	on_time	1	4	3	3	2	81	1
489	ad9ca78c-318f-4f59-944d-4e71724d8344	pending	300.00	501.00	201.00	2024-11-30	2024-12-15	45		0.45	\N	0.00	501.00	3	167.00	f	2024-11-15 19:39:45+00	2024-11-26 19:41:18.104017+00	on_time	1	4	3	3	2	19	1
491	f2552fb8-2a0a-4160-9137-e1e77b9341f7	pending	600.00	1140.00	540.00	2024-11-30	2024-12-15	60		0.45	\N	0.00	1140.00	4	285.00	f	2024-11-15 21:08:26+00	2024-11-26 21:09:23.99205+00	on_time	1	4	3	3	2	6	1
492	5225696c-e378-488b-87d2-3f1bc6286f92	pending	300.00	550.00	250.00	2024-11-30	2024-12-15	30		0.83	\N	0.00	550.00	1	550.00	f	2024-11-15 21:44:38+00	2024-11-26 21:45:04.599427+00	on_time	1	4	4	3	2	197	1
493	dfc68032-c122-4348-87f1-c4d4982e3779	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-15 21:52:52+00	2024-11-26 21:53:29.673377+00	on_time	1	4	3	3	2	55	1
535	a7462840-b2d2-4f8a-bc3b-6ab51f3eb8a5	pending	50.00	60.00	10.00	2024-11-30	2024-12-15	30		0.20	\N	0.00	60.00	2	30.00	f	2024-11-25 22:16:33+00	2024-11-27 22:21:09.488936+00	on_time	1	4	3	3	2	263	1
495	be3c8550-60c9-4fcd-8589-62d132593266	pending	200.00	360.00	160.00	2024-09-30	2024-10-15	45		0.53	\N	340.00	20.00	3	120.00	t	2024-09-19 22:27:29+00	2024-11-26 22:35:26.4794+00	mild_default	1	4	3	3	2	12	1
466	960225b8-a612-48eb-a6c1-0b5afa22e8a2	pending	100.00	130.00	30.00	2024-11-30	2024-12-15	30		0.30	\N	25.00	105.00	2	65.00	f	2024-11-17 19:05:07+00	2024-11-26 23:04:40.181281+00	on_time	1	4	3	3	2	249	1
279	671c01c9-f3c2-43d5-b4e9-4a2184a5ddb5	pending	3000.00	3600.00	600.00	2024-10-15	2024-10-30	36		0.17	\N	2320.00	1280.00	36	100.00	t	2024-10-12 23:05:39+00	2024-12-06 00:56:44.983226+00	recurrent_default	1	4	1	3	2	186	1
504	f3adab08-1bfb-46e7-a9c3-e487560b8143	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	30		0.50	\N	54.00	96.00	2	75.00	f	2024-11-16 23:20:52+00	2024-12-06 00:48:53.2725+00	on_time	1	4	3	3	2	162	1
498	d12fe820-ac34-4d59-8db5-7e129a9d7eae	pending	100.00	165.00	65.00	2024-11-30	2024-12-15	45		0.43	\N	0.00	165.00	3	55.00	f	2024-11-16 23:19:32+00	2024-11-26 23:20:03.383315+00	on_time	1	4	3	3	9	158	1
184	5a4608b6-c7a1-499b-881b-ef9d3432e8c9	pending	400.00	500.00	100.00	2024-07-31	2024-08-15	45		0.17	\N	266.00	234.00	7	71.43	t	2024-07-25 00:27:20+00	2024-12-06 00:53:49.38478+00	recurrent_default	1	4	2	3	2	136	1
541	cf18458e-a3dd-40e2-88e2-1a089b0697cd	pending	70.00	140.00	70.00	2024-11-30	2024-12-15	30		1.00	\N	0.00	140.00	2	70.00	f	2024-11-26 23:57:00+00	2024-12-02 23:57:40.08893+00	on_time	1	4	3	3	2	133	1
441	b3957f7f-9b49-4faa-ad3d-a1442c663833	pending	1000.00	1400.00	400.00	2024-11-15	2024-11-30	40		0.30	\N	680.00	720.00	40	35.00	t	2024-11-12 23:07:41+00	2024-12-06 00:58:14.578084+00	mild_default	1	4	1	3	2	240	1
506	02d33097-8401-4297-9fc3-d2b8d8c5891e	pending	4000.00	5600.00	1600.00	2024-11-30	2024-12-15	36		0.33	\N	1120.00	4480.00	36	155.56	f	2024-11-21 00:04:39+00	2024-12-06 00:57:50.280495+00	on_time	1	4	1	3	2	49	1
554	f8102967-9317-41bf-9a6c-26fe06df8661	pending	50.00	80.00	30.00	2024-11-30	2024-12-15	30		0.60	\N	0.00	80.00	1	80.00	f	2024-11-29 21:48:21+00	2024-12-04 21:49:04.684978+00	on_time	1	4	4	3	2	18	1
98	cafb4547-67ec-454c-b95a-6331c06fb685	pending	4000.00	5600.00	1600.00	2024-09-15	2024-09-17	35		0.34	\N	5600.00	0.00	35	160.00	t	2024-09-13 23:45:55+00	2024-12-03 00:17:47.212614+00	recurrent_default	1	4	1	3	2	49	1
547	f12d628e-4934-4958-b64c-b76afb3f454a	pending	150.00	230.00	80.00	2024-12-01	2024-12-20	30		0.53	\N	0.00	230.00	1	230.00	f	2024-11-28 00:37:01+00	2024-12-03 00:41:26.074399+00	on_time	1	4	4	3	2	84	1
519	75c64571-1e5c-4891-8cc8-79e3d5788556	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	140.00	0.00	1	140.00	f	2024-11-23 01:17:39+00	2024-12-03 00:57:43.592249+00	on_time	1	4	4	3	2	218	1
543	64cae424-a009-4271-b60c-61ffd4d2aa54	pending	80.00	150.00	70.00	2024-11-30	2024-12-15	30		0.88	\N	0.00	150.00	2	75.00	f	2024-11-27 00:19:59+00	2024-12-03 00:21:55.679445+00	on_time	1	4	3	3	2	264	1
194	fa83b659-9e5e-4c66-871b-d6cf0a362fd6	pending	50.00	90.00	40.00	2024-09-30	2024-10-15	30		0.80	\N	50.00	40.00	2	45.00	t	2024-09-26 22:31:29+00	2024-12-03 00:25:58.284769+00	recurrent_default	1	4	3	3	9	27	1
321	202d6f82-a2ba-4123-a9d4-070c2e1af93d	pending	500.00	900.00	400.00	2024-10-30	2024-11-15	60		0.40	\N	300.00	600.00	4	225.00	t	2024-10-18 22:31:38+00	2024-12-03 00:26:35.675259+00	mild_default	1	4	3	3	2	61	1
544	d5b53456-5929-460f-86e0-f6d036e68bb2	pending	100.00	130.00	30.00	2024-11-30	2024-12-15	30		0.30	\N	0.00	130.00	1	130.00	f	2024-11-28 00:35:09+00	2024-12-03 00:36:27.883841+00	on_time	1	4	4	3	2	84	1
545	45e12afe-d9a9-4de6-83e8-9ef3014ca7f5	pending	50.00	75.00	25.00	2024-11-30	2024-12-15	30		0.50	\N	0.00	75.00	1	75.00	f	2024-11-28 00:36:28+00	2024-12-03 00:37:01.470426+00	on_time	1	4	4	3	2	84	1
371	09f9f675-e009-41ed-9eb8-64fb553f04b3	pending	100.00	150.00	50.00	2024-11-15	2024-11-30	30		0.50	\N	75.00	75.00	2	75.00	f	2024-10-30 22:52:46+00	2024-12-03 00:42:36.368442+00	moderate_default	1	4	3	3	2	78	1
483	56b4e332-0e61-4cb4-9129-4ea7570f3c4b	pending	280.00	1050.00	770.00	2024-11-30	2024-12-15	35	Reajustado 400 del crédito anterior	2.36	\N	270.00	780.00	35	30.00	f	2024-11-20 00:47:12+00	2024-12-06 00:57:14.889446+00	on_time	1	4	1	3	2	176	1
540	f572cb8b-03a5-47db-8833-ef0e0938df7e	pending	100.00	120.00	20.00	2024-11-30	2024-12-15	30		0.20	\N	60.00	60.00	2	60.00	f	2024-11-25 22:21:58+00	2024-12-04 22:54:33.572665+00	on_time	1	4	3	3	2	153	1
397	99bf7a5c-b56e-4301-8fad-edafb899391d	pending	200.00	260.00	60.00	2024-11-15	2024-11-30	75		0.12	\N	157.00	103.00	5	52.00	f	2024-11-02 20:27:03+00	2024-12-06 00:22:57.496275+00	moderate_default	1	4	3	3	2	103	1
548	cc78efec-57ae-427e-b673-aa69efe6fb34	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	60		0.20	\N	0.00	140.00	4	35.00	f	2024-11-29 01:00:36+00	2024-12-03 01:01:05.490354+00	on_time	1	4	3	3	2	265	1
542	4f8fd115-12fb-4784-bb0f-f9cbe3ab36b5	pending	60.00	100.00	40.00	2024-11-30	2024-12-15	30		0.67	\N	50.00	50.00	2	50.00	f	2024-12-26 23:57:40+00	2024-12-05 23:40:11.888294+00	on_time	1	4	3	3	2	214	1
189	03608076-efc5-4c6c-aa78-af77dfb8760a	pending	150.00	255.00	105.00	2024-09-30	2024-10-15	45		0.47	\N	255.00	0.00	3	85.00	t	2024-09-24 19:00:11+00	2024-12-06 01:09:27.099883+00	mild_default	1	4	3	3	2	139	1
549	ce5bd984-2127-4729-a8bc-7ad3cb07c1b0	pending	150.00	250.00	100.00	2024-11-30	2024-12-15	30		0.67	\N	0.00	250.00	1	250.00	f	2024-11-29 21:29:55+00	2024-12-04 21:30:25.883701+00	on_time	1	4	4	3	2	157	1
553	e19a111f-ce1e-4a01-9f85-64fbb36d4369	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	30		0.50	\N	0.00	150.00	2	75.00	f	2024-11-29 21:30:56+00	2024-12-04 21:31:00.88819+00	on_time	1	4	3	3	2	51	1
494	11a022d0-5dc5-40f1-9257-cd689a35e120	pending	150.00	250.00	100.00	2024-11-30	2024-12-15	30		0.67	\N	60.00	190.00	2	125.00	f	2024-11-15 22:00:52+00	2024-12-06 00:25:08.096514+00	on_time	1	4	3	3	2	248	1
295	7ee01fdc-76bc-45c3-96c7-57bd8606744f	pending	200.00	300.00	100.00	2024-10-30	2024-11-15	45		0.33	\N	200.00	100.00	3	100.00	f	2024-10-16 18:25:10+00	2024-12-04 21:56:15.36528+00	moderate_default	1	4	3	3	2	155	1
555	d78461f4-1d85-4526-8b99-2d6856846ac3	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	140.00	1	140.00	f	2024-11-30 22:00:34+00	2024-12-04 22:00:58.666312+00	on_time	1	4	4	3	2	218	1
556	c8a60d20-6cb6-46a4-8b34-6f17d72955e6	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-30 22:00:59+00	2024-12-04 22:01:27.188004+00	on_time	1	4	3	3	2	154	1
557	5ad0912e-c2ab-491d-ba7f-e52b575acc24	pending	200.00	360.00	160.00	2024-12-15	2024-12-30	60		0.40	\N	0.00	360.00	4	90.00	f	2024-11-30 22:08:06+00	2024-12-04 22:08:37.186106+00	on_time	1	4	3	3	2	206	1
496	24947edd-c0da-4dd5-9d3d-378d2d058a52	pending	100.00	140.00	40.00	2024-11-30	2024-12-15	30		0.40	\N	70.00	70.00	2	70.00	f	2024-11-16 23:08:37+00	2024-12-06 00:56:05.182297+00	on_time	1	4	3	3	2	250	1
434	f340fa4c-17ee-4934-a1d6-848124b7c0a4	pending	100.00	132.00	32.00	2024-11-15	2024-11-30	30		0.32	\N	24.00	108.00	30	4.40	t	2024-11-09 22:03:32+00	2024-12-06 00:24:31.375476+00	recurrent_default	1	4	1	3	2	1	1
558	c8792c64-a181-49d9-8ec1-2fc91f6b4303	pending	100.00	120.00	20.00	2024-12-15	2024-12-30	60		0.10	\N	0.00	120.00	4	30.00	f	2024-11-30 22:08:37+00	2024-12-04 22:10:21.793751+00	on_time	1	4	3	3	2	92	1
559	b57962e8-103e-4561-a723-3ddac70adee6	pending	100.00	130.00	30.00	2024-12-15	2024-12-30	30		0.30	\N	0.00	130.00	1	130.00	f	2024-11-30 22:39:25+00	2024-12-04 22:40:46.993656+00	on_time	1	4	4	3	2	266	1
560	88d90b38-8a81-42a0-a9a0-121bd2af3caa	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-11-30 22:40:47+00	2024-12-04 22:41:37.972599+00	on_time	1	4	3	3	2	126	1
497	d8754735-e929-4566-b60e-88230ca64dbf	pending	100.00	150.00	50.00	2024-11-30	2024-12-15	30		0.50	\N	70.00	80.00	2	75.00	f	2024-11-16 23:09:38+00	2024-12-04 22:44:58.691444+00	on_time	1	4	3	3	2	251	1
562	64294388-28aa-4b46-812a-dfa0e8cbdf7c	pending	20.00	35.00	15.00	2024-12-15	2024-12-30	30		0.75	\N	0.00	35.00	1	35.00	f	2024-11-30 22:52:00+00	2024-12-04 22:52:25.989864+00	on_time	1	4	4	3	2	77	1
563	085b5bbf-805f-4b94-8ed9-c2201a508236	pending	50.00	70.00	20.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	70.00	1	70.00	f	2024-11-30 22:52:26+00	2024-12-04 22:53:06.988824+00	on_time	1	4	4	3	2	40	1
561	9c9195a1-3832-4be4-a17d-3cadaf54f10a	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	60		0.20	\N	35.00	105.00	4	35.00	f	2024-11-30 22:41:38+00	2024-12-06 01:08:11.233455+00	on_time	1	4	3	3	2	37	1
564	a3751df6-524f-4982-aeb3-03b9ece316db	pending	2000.00	2600.00	600.00	2024-06-15	2024-06-30	90		0.10	\N	350.00	2250.00	6	433.33	t	2024-06-06 23:14:50+00	2024-12-05 23:20:04.988701+00	recurrent_default	1	4	3	3	2	133	1
278	05233fe0-9ba5-4163-aa1d-cce0051f0609	pending	200.00	330.00	130.00	2024-10-15	2024-10-30	90		0.22	\N	220.00	110.00	6	55.00	t	2024-10-12 23:03:47+00	2024-12-05 23:23:23.808645+00	moderate_default	1	4	3	3	2	38	1
565	eaa83f32-12ce-4e03-8589-c8a8e694ab84	pending	100.00	150.00	50.00	2024-12-15	2024-12-30	60		0.25	\N	0.00	150.00	4	37.50	f	2024-12-01 23:24:32+00	2024-12-05 23:25:02.798275+00	on_time	1	4	3	3	2	38	1
573	47bd5de9-da13-4abf-aa0e-903f313d8c9d	pending	200.00	360.00	160.00	2024-12-15	2024-12-30	60		0.40	\N	0.00	360.00	4	90.00	f	2024-12-01 23:26:00+00	2024-12-05 23:26:01.177787+00	on_time	1	4	3	3	2	90	1
574	dbff921b-eca1-4db9-ac36-7c6f1146776d	pending	800.00	800.00	0.00	2024-12-15	2024-12-30	30		0.00	\N	0.00	800.00	2	400.00	f	2024-12-01 23:26:01+00	2024-12-05 23:27:45.679022+00	on_time	1	4	3	3	2	267	1
575	4c8500e3-b103-406b-8757-cbae1cbd8028	pending	100.00	150.00	50.00	2024-12-15	2024-12-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-12-02 23:36:40+00	2024-12-05 23:37:03.085254+00	on_time	1	4	3	3	2	104	1
576	4b7f33b1-69eb-4459-923a-901362580f4f	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-12-02 23:37:03+00	2024-12-05 23:38:05.79376+00	on_time	1	4	3	3	2	268	1
577	73059550-bcb5-420e-9c9c-426733cb088c	pending	200.00	240.00	40.00	2024-12-15	2024-12-30	30		0.20	\N	0.00	240.00	2	120.00	f	2024-12-03 00:14:18+00	2024-12-06 00:15:00.989337+00	on_time	1	4	3	3	2	56	1
578	c146e4e7-38d5-4e3a-91eb-45bcf00e56e1	pending	200.00	360.00	160.00	2024-12-15	2024-12-30	45		0.53	\N	0.00	360.00	3	120.00	f	2024-12-03 00:25:28+00	2024-12-06 00:26:03.174825+00	on_time	1	4	3	3	2	63	1
584	82ae263a-45f9-47a1-8b59-465cbfa52b22	pending	100.00	130.00	30.00	2024-12-15	2024-12-30	60		0.15	\N	0.00	130.00	4	32.50	f	2024-12-03 00:26:54+00	2024-12-06 00:27:01.580236+00	on_time	1	4	3	3	2	3	1
585	1da74431-6e5a-4e68-ae4f-618925f9c0a6	pending	280.00	280.00	0.00	2024-09-15	2024-09-30	90	Libros	0.00	\N	0.00	280.00	3	93.33	t	2024-09-08 00:38:25+00	2024-12-06 00:39:12.988966+00	critical_default	1	4	4	3	1	52	1
589	34561f6e-0f11-40e2-abf1-879b7637819b	pending	100.00	160.00	60.00	2024-09-15	2024-09-30	30		0.60	\N	160.00	0.00	1	160.00	t	2024-09-08 00:39:58+00	2024-12-06 00:41:56.187742+00	mild_default	1	4	4	3	2	52	1
604	821d6263-869c-4461-9568-7d6eee94bfb5	pending	100.00	160.00	60.00	2024-09-15	2024-09-30	30		0.60	\N	0.00	160.00	1	160.00	t	2024-09-08 00:40:58+00	2024-12-06 00:41:01.893936+00	critical_default	1	4	4	3	2	52	1
607	47199484-15a4-4ea7-a982-cacaab5dc5f0	pending	100.00	150.00	50.00	2024-12-15	2024-12-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-12-04 00:42:17+00	2024-12-06 00:42:51.518469+00	on_time	1	4	3	3	2	230	1
608	2c4c9691-0042-4614-80f4-79833de56c91	pending	40.00	70.00	30.00	2024-12-07	2024-12-24	30		0.75	\N	0.00	70.00	2	35.00	f	2024-12-04 00:42:51+00	2024-12-06 00:43:33.09093+00	on_time	1	4	3	3	2	218	1
609	85740a98-7bab-4f4c-9685-ae945d019d70	pending	300.00	510.00	210.00	2024-12-15	2024-12-30	45		0.47	\N	0.00	510.00	3	170.00	f	2024-12-04 00:43:33+00	2024-12-06 00:44:12.567307+00	on_time	1	4	3	3	2	114	1
610	02ce8c64-22c7-4377-8c9e-f7c8359ae8bc	pending	500.00	1000.00	500.00	2024-12-15	2024-12-30	120		0.25	\N	0.00	1000.00	8	125.00	f	2024-12-04 00:44:13+00	2024-12-06 00:45:00.994493+00	on_time	1	4	3	3	2	171	1
138	182a1322-9508-43fe-89cd-b676242aaafc	pending	90.00	150.00	60.00	2024-09-30	2024-10-15	30	Ajustado con el crédito del 16 de Septiembre	0.67	\N	75.00	75.00	2	75.00	t	2024-10-05 23:56:30+00	2024-12-06 00:47:30.836268+00	recurrent_default	1	4	3	3	2	107	1
611	312ba2e4-c8a3-4886-b7e7-9b06b68c331a	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-12-05 00:58:24+00	2024-12-06 00:59:24.482892+00	on_time	1	4	3	3	2	269	1
615	d3ebc62c-0a4f-42b1-a3a7-99d32dcca130	pending	15.00	60.00	45.00	2024-12-15	2024-12-30	30		3.00	\N	0.00	60.00	1	60.00	f	2024-12-05 01:00:00+00	2024-12-06 01:00:06.065219+00	on_time	1	4	4	3	2	121	1
620	da8d8de2-4a81-4e36-a6b4-62b1b5f1d131	pending	50.00	90.00	40.00	2024-12-15	2024-12-30	30		0.80	\N	0.00	90.00	2	45.00	f	2024-12-05 01:00:59+00	2024-12-06 01:01:06.279422+00	on_time	1	4	3	3	2	12	1
621	a1649d18-9041-4b94-ad16-367c44960611	pending	30.00	50.00	20.00	2024-12-15	2024-12-30	30		0.67	\N	0.00	50.00	2	25.00	f	2024-12-05 01:01:06+00	2024-12-06 01:03:10.782282+00	on_time	1	4	3	3	2	30	1
622	b6f6e0ce-2010-47fe-b9fa-8d9a8631cc75	pending	100.00	150.00	50.00	2024-12-15	2024-12-30	30		0.50	\N	0.00	150.00	2	75.00	f	2024-12-05 01:03:11+00	2024-12-06 01:05:15.2708+00	on_time	1	4	3	3	2	270	1
625	e709ad46-2476-4951-b554-cd6a0f034589	pending	100.00	152.00	52.00	2024-12-15	2024-12-30	60		0.26	\N	0.00	152.00	4	38.00	f	2024-12-05 01:06:01+00	2024-12-06 01:06:03.787062+00	on_time	1	4	3	3	2	4	1
626	049b7da8-037a-4cd4-b64a-2c9ece02d955	pending	100.00	120.00	20.00	2024-12-06	2024-12-08	30		0.20	\N	0.00	120.00	30	4.00	f	2024-12-05 01:06:29+00	2024-12-06 01:07:17.984789+00	on_time	1	4	1	3	2	103	1
627	c71ac1ca-53db-44ce-82d6-cdd954591105	pending	100.00	140.00	40.00	2024-12-15	2024-12-30	30		0.40	\N	0.00	140.00	2	70.00	f	2024-12-05 01:10:16+00	2024-12-06 01:11:31.675844+00	on_time	1	4	3	3	2	271	1
628	b40c1797-e588-4aad-bc08-2262d2b8a562	pending	100.00	120.00	20.00	2024-12-15	2024-12-30	30		0.20	\N	0.00	120.00	2	60.00	f	2024-12-05 01:11:32+00	2024-12-06 01:12:30.779556+00	on_time	1	4	3	3	2	272	1
629	8f48425d-8238-4eb4-bf55-31fd8a960cad	pending	300.00	510.00	210.00	2024-12-15	2024-12-30	45		0.47	\N	0.00	510.00	3	170.00	f	2024-12-05 01:12:31+00	2024-12-06 01:13:08.866302+00	on_time	1	4	3	3	2	83	1
\.


--
-- Data for Name: fintech_currency; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_currency" ("id", "asset_type", "id_currency", "currency", "exchange_rate") FROM stdin;
1	FIAT	USD	Dólar	1.0000
2	FIAT	EUR	Euro	1.1200
3	FIAT	COP	Peso colombiano	0.0020
\.


--
-- Data for Name: fintech_documenttype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_documenttype" ("id", "code", "description", "country_id_id") FROM stdin;
1	CC	Cédula de ciudadanía	1
\.


--
-- Data for Name: fintech_expense; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_expense" ("id", "uid", "amount", "description", "date", "account_id", "subcategory_id", "registered_by_id", "user_id", "created_at", "updated_at") FROM stdin;
5	13cd745f-209c-4af6-8b91-1f1dfd933ba5	420.00	Deposito al Banesco	2024-09-20 21:05:25.411608+00	4	8	3	2	2024-09-21 05:06:28.891114+00	2024-09-21 05:06:29.38088+00
6	8488fcf3-2723-4219-aee4-5c8279ffd3a0	11.00	Almuerzo	2024-09-23 18:58:58.226615+00	4	7	3	3	2024-09-21 18:58:15+00	2024-09-23 18:58:58.2266+00
7	6d3d42ef-e0ae-41bf-bab7-35d1fb8922fb	40.00	Pago para la licencia	2024-09-27 22:39:10.064214+00	4	6	3	2	2024-09-26 22:37:52+00	2024-09-27 22:39:10.064203+00
8	f59337a5-a3e8-4dd3-ac19-e784febc33f9	28.00	Comida	2024-09-27 23:29:24.37766+00	4	8	3	3	2024-09-26 23:28:53+00	2024-09-27 23:29:24.377647+00
9	351920b2-8957-46b8-a872-a0b097a00c2e	1.60		2024-09-27 23:30:08.104942+00	4	4	3	2	2024-09-26 23:29:24+00	2024-09-27 23:30:08.104932+00
10	b83eae7d-17ea-49a0-ab24-b9c45888a1eb	25.00	Comida	2024-09-27 23:49:26.721026+00	4	8	3	2	2024-09-26 23:49:08+00	2024-09-27 23:49:26.721012+00
11	11f252d0-12a6-42db-aad7-0628579d2143	1.85		2024-09-27 23:49:46.019234+00	4	4	3	2	2024-09-26 23:49:27+00	2024-09-27 23:49:46.019219+00
12	48ee588d-e0a5-45ce-b591-b1cc309e5fd3	17.50	Comida	2024-09-28 01:12:32.107473+00	4	8	3	2	2024-09-26 01:12:10+00	2024-09-28 01:12:32.107462+00
13	b81d52d6-7938-4b43-a68f-6150044ca991	1.50		2024-09-28 01:12:45.524449+00	4	4	3	2	2024-09-26 01:12:32+00	2024-09-28 01:12:45.52444+00
14	75fe2af1-d9ee-4d2c-bb16-fdfef7908e1a	20.00	Enseñanza licencia	2024-09-28 01:13:02.293342+00	4	7	3	2	2024-09-26 01:12:46+00	2024-09-28 01:13:02.293327+00
15	f551769f-025c-47cb-a8c8-537667e01927	38.00	Mercado	2024-10-04 02:30:36.917317+00	4	8	3	2	2024-09-30 02:30:12+00	2024-10-04 02:30:36.917307+00
16	fcca5d53-e0a7-4a8d-a1fb-6e7a065d7536	1.50		2024-10-04 02:30:52.01811+00	4	4	3	2	2024-09-30 02:30:37+00	2024-10-04 02:30:52.018095+00
17	e7a2b738-acc4-421b-bea3-42d7989852e8	9.00	Comidas	2024-10-04 02:31:12.739771+00	4	8	3	3	2024-09-28 02:30:52+00	2024-10-04 02:31:12.73976+00
18	38380f09-2835-476f-9591-13248b53d2d1	1.60		2024-10-04 02:31:33.520321+00	4	4	3	2	2024-09-28 02:31:13+00	2024-10-04 02:31:33.520305+00
19	b8c61510-51ac-49c8-a43e-ee46a1e0b28b	1.65		2024-10-04 03:08:52.93731+00	4	4	3	2	2024-10-01 03:08:24+00	2024-10-04 03:08:52.937299+00
20	6fe24cf3-df13-4d92-a27c-6b7df0d3279b	6.90	Comidas	2024-10-04 03:09:12.11548+00	4	8	3	3	2024-10-01 03:08:53+00	2024-10-04 03:09:12.115461+00
21	0e690c7e-8c96-4ab9-b25e-52cc6287ab62	55.00	Pago a la DGI.	2024-10-04 03:09:37.454175+00	4	12	3	2	2024-10-04 03:09:12+00	2024-10-04 03:09:37.454165+00
23	351d3840-6f97-44cb-892d-6fc405f6ad20	30.00		2024-10-09 00:46:55.087185+00	4	8	3	2	2024-10-02 00:46:15+00	2024-10-09 00:46:55.087169+00
24	78fa19f1-9626-4c1b-974c-712badf35d1a	5.00	Mercado	2024-10-09 00:47:40.693462+00	4	8	3	2	2024-10-02 00:46:55+00	2024-10-09 00:47:40.693453+00
22	79fa0898-2c3e-42d3-816a-03b2fc690b0b	138.70	Alquiler de carro	2024-10-09 00:46:08.118036+00	4	6	3	2	2024-10-02 00:45:19+00	2024-10-09 00:48:20.899391+00
25	116fb7f3-54c1-4aa9-bd86-0063d87bde28	22.50	Comida	2024-10-09 22:25:00.815084+00	4	8	3	2	2024-10-02 22:24:34+00	2024-10-09 22:25:00.815073+00
26	bc056b35-e668-43a7-9f15-2c842be15868	52.00	Mercado	2024-10-09 22:25:24.415161+00	4	8	3	2	2024-10-02 22:25:01+00	2024-10-09 22:25:24.415147+00
27	57bc3990-bd71-4106-94a7-602781e30e8c	276.00	Pago Banesco	2024-10-09 23:29:29.922206+00	4	8	3	2	2024-10-03 23:28:44+00	2024-10-09 23:29:29.922194+00
28	099aa8e5-2c0b-43cf-8334-c80262788083	42.00	Comida	2024-10-09 23:29:56.926868+00	4	8	3	2	2024-10-03 23:29:30+00	2024-10-09 23:29:56.926858+00
29	ef8f89ce-bd3f-497a-b303-ec9a311d03a7	20.00		2024-10-09 23:30:24.745579+00	4	5	3	2	2024-10-03 23:29:57+00	2024-10-09 23:30:24.745567+00
30	878afc4f-318b-461f-bcb7-0d6de64fb8ea	28.00	Almuerzos	2024-10-11 16:34:46.231659+00	4	8	3	2	2024-10-04 16:34:22+00	2024-10-11 16:34:46.231644+00
31	9834fd8e-c965-44fb-b931-2ef52cb057d4	17.00	Comidas	2024-10-11 16:35:08.116568+00	4	8	3	2	2024-10-04 16:34:46+00	2024-10-11 16:35:08.116552+00
32	a15be939-c18b-4401-bb37-e21c7224ced5	7.50		2024-10-18 00:46:12.920282+00	4	8	3	2	2024-10-08 00:45:52+00	2024-10-18 00:46:12.920271+00
33	6f71b728-8023-49cb-bcf3-95816ae95316	1.95		2024-10-18 00:46:25.615615+00	4	4	3	3	2024-10-08 00:46:13+00	2024-10-18 00:46:25.615598+00
34	937bb882-624c-4624-8acc-f911b5ea082e	3.50		2024-10-18 00:56:36.541315+00	4	8	3	2	2024-10-09 00:56:20+00	2024-10-18 00:56:36.5413+00
35	97a3f3d4-5828-4e4e-8dc7-19fd8c60931f	1.50		2024-10-18 00:56:49.829959+00	4	4	3	2	2024-10-09 00:56:36+00	2024-10-18 00:56:49.829946+00
36	74275818-332b-4f4b-8e57-97740df87e88	15.00	Legumbres	2024-10-18 00:57:04.024092+00	4	2	3	2	2024-10-09 00:56:50+00	2024-10-18 00:57:04.024081+00
37	3c070751-5fed-40d5-9663-7ed9813eb920	105.00	Compra de celular	2024-10-18 01:10:08.720589+00	4	7	3	2	2024-10-10 01:09:48+00	2024-10-18 01:10:08.720577+00
38	f35edb76-6758-4a52-ae32-70adcd12d0a2	3.75		2024-10-18 01:10:24.227814+00	4	4	3	2	2024-10-10 01:10:09+00	2024-10-18 01:10:24.227802+00
39	ebc6ed56-0552-4d3f-9d07-b99b20174f0e	5.00	Almuerzo	2024-10-18 01:10:45.225337+00	4	8	3	2	2024-10-10 01:10:24+00	2024-10-18 01:10:45.225328+00
40	8ef7b692-3958-4c29-a491-ec1894e92330	11.00	Almuerzo y comidas	2024-10-19 22:44:54.838052+00	4	8	3	2	2024-10-10 22:44:35+00	2024-10-19 22:44:54.838043+00
41	f1421dae-3c1f-48f8-9a35-0afa122c72c3	75.00		2024-10-19 22:45:09.315789+00	4	4	3	2	2024-10-10 22:44:55+00	2024-10-19 22:45:09.315773+00
42	0462a34e-08b5-4a40-a088-c7033cb614ef	64.60	Casa ofic. Pago servicios	2024-10-19 22:52:09.222978+00	4	7	3	2	2024-10-11 22:51:51+00	2024-10-19 22:52:09.22297+00
43	e536b0bf-2df8-4878-95b1-5b4c16523ed2	5.60		2024-10-19 22:52:22.81974+00	4	8	3	2	2024-10-11 22:52:09+00	2024-10-19 22:52:22.819725+00
44	5d6c299b-3388-499e-a7e9-78a624f0debf	1.70		2024-10-19 22:52:38.016233+00	4	4	3	2	2024-10-11 22:52:23+00	2024-10-19 22:52:38.01622+00
45	713bd9cc-ba8e-4007-b59f-daf341f7f5e6	100.00	Naturgy se abono a serv	2024-10-19 22:57:56.217266+00	4	7	3	2	2024-10-11 22:57:38+00	2024-10-19 22:57:56.217258+00
46	3e150143-3cbf-4951-adf3-6f3c19d12a03	13.00	Almuerzos y comidas	2024-10-19 23:09:16.414941+00	4	8	3	2	2024-10-12 23:08:56+00	2024-10-19 23:09:16.41493+00
47	40a676d3-bc3c-49af-8fab-665c49e3317e	170.00		2024-10-19 23:09:30.844252+00	4	4	3	2	2024-10-12 23:09:16+00	2024-10-19 23:09:30.844238+00
48	9540700f-e96c-4673-815c-f85818cd4515	4.50	Agua y frescos	2024-10-19 23:09:46.819397+00	4	8	3	2	2024-10-12 23:09:31+00	2024-10-19 23:09:46.819386+00
49	f7fe3910-700d-49cf-94ae-c59b7b1e7043	76.00	Mercado	2024-10-19 23:10:14.334455+00	4	8	3	2	2024-10-13 23:09:47+00	2024-10-19 23:10:14.334445+00
50	ab708416-a342-4f80-baa1-0bf2486f30c9	10.50	Almuerzos	2024-10-19 23:10:30.115314+00	4	8	3	2	2024-10-13 23:10:14+00	2024-10-19 23:10:30.115299+00
51	714b9610-c345-4040-b56b-75d458b1d3e1	10.00	El lince gastos  representac	2024-10-19 23:10:48.965984+00	4	7	3	2	2024-10-13 23:10:30+00	2024-10-19 23:10:48.965971+00
52	256f839b-5799-4896-b7dc-6136b7bcf0d2	5.00	Almuerzo	2024-10-19 23:36:08.953159+00	4	8	3	2	2024-10-14 23:35:54+00	2024-10-19 23:36:08.95315+00
53	688157e3-5d21-4c83-a7f1-b4ed13e90cd9	1.90		2024-10-19 23:36:21.530438+00	4	4	3	2	2024-10-14 23:36:09+00	2024-10-19 23:36:21.530425+00
54	a465f5e7-78d1-4647-9af4-92656f27c263	20.25	Comidas	2024-10-19 23:36:36.618016+00	4	8	3	2	2024-10-14 23:36:22+00	2024-10-19 23:36:36.618003+00
55	e81088c0-2adf-488a-800b-1485407c5c19	10.00	Invitacion  representacion.	2024-10-19 23:36:50.62+00	4	7	3	2	2024-10-14 23:36:37+00	2024-10-19 23:36:50.61999+00
56	bf98b42e-dd58-4e33-8b45-45504e620e9a	40.00	Abono de servicios	2024-10-19 23:37:09.927539+00	4	7	3	2	2024-10-14 23:36:51+00	2024-10-19 23:37:09.927527+00
57	c610685b-b1b7-4f4d-8ceb-edcdb9d4967e	1.50		2024-10-24 19:55:28.769719+00	4	4	3	2	2024-10-16 19:55:05+00	2024-10-24 19:55:28.769704+00
58	136474e6-501f-4fca-ac75-e37f98690948	54.00	Carro Arrendado	2024-10-24 19:55:47.528903+00	4	6	3	2	2024-10-16 19:55:29+00	2024-10-24 19:55:47.528889+00
59	611dfa7b-a12a-4c75-bdd2-c66d428a0f6b	6.00	Desayuno	2024-10-24 19:56:02.225955+00	4	8	3	2	2024-10-16 19:55:47+00	2024-10-24 19:56:02.225942+00
60	15285370-6578-4d56-813a-56a011c13cae	14.50	Almuerzos	2024-10-24 19:56:23.222974+00	4	8	3	2	2024-10-16 19:56:02+00	2024-10-24 19:56:23.222963+00
61	a082a9b6-68c7-4f7a-91fb-7bcd2af03a42	11.50	Comidas	2024-10-24 19:56:38.526823+00	4	8	3	2	2024-10-16 19:56:23+00	2024-10-24 19:56:38.526807+00
62	bdc1c15d-d37e-4cbf-8686-43049aa946b7	6.50	Frutas	2024-10-24 19:56:54.726701+00	4	8	3	2	2024-10-16 19:56:38+00	2024-10-24 19:56:54.726688+00
63	ac910bbb-c4c9-4fb2-ad1c-2431fd2e0017	22.00	Compra de detergentes	2024-10-24 22:05:25.227239+00	4	8	3	2	2024-10-17 22:05:05+00	2024-10-24 22:05:25.227228+00
64	7a438b03-e765-4797-890a-0bfb4cc44dc8	400.00	Deposito a banescoLexus	2024-10-24 22:57:56.123254+00	4	7	3	3	2024-10-19 22:57:40+00	2024-10-24 22:57:56.12324+00
65	6b4c3dee-ed8f-4cd3-8e1f-4942ddd94eb6	55.00	Mercado	2024-10-24 23:10:24.518238+00	4	8	3	2	2024-10-19 23:10:01+00	2024-10-24 23:10:24.518228+00
66	9275d940-3e6a-467b-bae2-ffa790d131ea	7.00	Desayumo y almuerzo.	2024-10-24 23:10:39.115838+00	4	8	3	2	2024-10-19 23:10:24+00	2024-10-24 23:10:39.115826+00
67	d4b4b3fd-2cce-44be-9f43-8b403987ea58	1.20		2024-10-24 23:15:23.243242+00	4	4	3	2	2024-10-20 23:15:13+00	2024-10-24 23:15:23.243232+00
68	63b20df1-a01c-4779-96c1-00b8cec73dcf	10.50	omida gato y otros	2024-10-24 23:15:40.34206+00	4	8	3	2	2024-10-20 23:15:23+00	2024-10-24 23:15:40.342045+00
69	f3affad6-03ff-4767-93e0-fa6c6f7d4fa7	9.50	Comida	2024-10-24 23:30:23.32088+00	4	8	3	2	2024-10-21 23:30:03+00	2024-10-24 23:30:23.320869+00
70	becf56e3-1900-418c-a95f-9b4a0cb63c84	3.70		2024-10-24 23:30:50.426149+00	4	4	3	2	2024-10-21 23:30:23+00	2024-10-24 23:30:50.426139+00
71	69996f07-c9d8-42ae-856d-d5b6f0005147	225.50	Pagos de placa	2024-10-27 23:37:45.676393+00	4	7	3	2	2024-10-22 23:37:24+00	2024-10-27 23:37:45.676385+00
72	41b8f697-b0b5-4795-a1ed-e30927aaadcb	150.00	papel ahumado del carro	2024-10-27 23:38:08.817528+00	4	7	3	2	2024-10-22 23:37:46+00	2024-10-27 23:38:08.817518+00
73	92a66c3d-c036-4423-89e8-f4d2ba918dcf	425.00	Almuerzo	2024-10-27 23:41:29.529699+00	4	8	3	2	2024-10-22 23:41:08+00	2024-10-27 23:41:29.529689+00
74	456e4a00-fd10-43de-be48-6400281d5018	375.00		2024-10-27 23:41:40.400543+00	4	4	3	2	2024-10-22 23:41:30+00	2024-10-27 23:41:40.400531+00
75	975a795d-d531-4879-a203-2ca07ae96253	87.00	Daniel Ojeda Tenis	2024-10-27 23:51:20.328036+00	4	7	3	2	2024-10-23 23:50:49+00	2024-10-27 23:51:20.32802+00
76	e85eb09d-d7ff-4efd-98e8-d99b976e39ac	5.50	Almuerzo	2024-10-27 23:51:41.115982+00	4	7	3	2	2024-10-23 23:51:20+00	2024-10-27 23:51:41.115966+00
77	9b824ffa-7840-4d1c-909d-226f88414192	3.50		2024-10-27 23:51:53.762727+00	4	4	3	2	2024-10-23 23:51:41+00	2024-10-27 23:51:53.762717+00
78	1544f5a0-3b19-4ea6-a2dd-b1a1166c97ae	6.50	Almuerzo	2024-10-28 00:22:54.252244+00	4	8	3	2	2024-10-25 00:22:36+00	2024-10-28 00:22:54.25223+00
79	a46160cd-8121-4cf0-a049-5768e9ea7bc1	9.50	Mercado	2024-10-28 00:23:08.628774+00	4	9	3	2	2024-10-25 00:22:54+00	2024-10-28 00:23:08.628762+00
80	58418f4f-e8ea-4797-9ae3-6b7fd84e5d96	3.90		2024-10-28 00:23:19.98283+00	4	4	3	2	2024-10-25 00:23:08+00	2024-10-28 00:23:19.982822+00
81	07c1aabc-0ee0-4eda-af12-a35251289569	20.00	Gastos personales.	2024-10-28 00:40:13.824094+00	4	7	3	2	2024-10-26 00:39:58+00	2024-10-28 00:40:13.82408+00
82	33e05589-59b2-45f2-a41f-eb72b350648f	5.50	Almuerzo	2024-10-28 00:40:43.13067+00	4	7	3	2	2024-10-26 00:40:14+00	2024-10-28 00:40:43.130652+00
83	7ea2b008-0c62-48cc-a0b2-3048d7142cf3	4.00		2024-10-28 00:41:03.643653+00	4	4	3	2	2024-10-26 00:40:43+00	2024-10-28 00:41:03.643646+00
84	8dccbc0a-10be-41c2-bcf9-dad1d933c944	5.00	Almuerzo	2024-11-01 21:53:59.628618+00	4	8	3	2	2024-10-28 21:53:42+00	2024-11-01 21:53:59.628602+00
85	4a4d12a4-7e76-4eee-8513-23cce090257f	11.50	Detergentes	2024-11-01 21:54:18.722163+00	4	7	3	2	2024-10-28 21:53:59+00	2024-11-01 21:54:18.722149+00
87	2f4db9af-97d4-4448-bab2-538e494ecdee	3.40		2024-11-01 22:00:18.129402+00	4	4	3	2	2024-10-29 22:00:03+00	2024-11-01 22:00:18.129384+00
86	5e0773f7-d213-4123-a362-16e660524c39	4.85	Almuerzo	2024-11-01 22:00:03.431407+00	4	2	3	2	2024-10-29 21:55:42+00	2024-11-01 22:00:33.546042+00
88	aaf18ee3-a22f-4974-ab38-807e81ee4b36	13.00	Almuerzo	2024-11-09 00:20:58.736473+00	4	8	3	2	2024-11-01 00:20:33+00	2024-11-09 00:20:58.736464+00
89	f52cc54d-67b7-4016-8f64-8f06e4b66b6d	13.50	Comida	2024-11-09 00:21:58.2324+00	4	8	3	2	2024-10-31 00:21:37+00	2024-11-09 00:21:58.232384+00
90	f09b997d-90e6-4bd3-be76-5db5caba2b2a	1.50		2024-11-09 00:22:13.234548+00	4	4	3	2	2024-10-31 00:21:58+00	2024-11-09 00:22:13.23453+00
91	5451407f-4774-4c0b-8c1c-7fd2d9fc5e03	274.00	Pago prestamo banesco.	2024-11-09 01:29:31.52492+00	4	7	2	3	2024-11-02 01:29:16+00	2024-11-09 01:29:31.524911+00
92	9f56f464-1924-42dc-82c0-2ff1f93c37c4	23.00	Comida	2024-11-09 01:43:31.725516+00	4	10	3	2	2024-11-02 01:43:16+00	2024-11-09 01:43:31.725508+00
93	464484b8-1021-446a-859d-f5a80f57e05d	64.00	Mercado	2024-11-10 20:27:53.904548+00	4	8	3	2	2024-11-02 20:27:37+00	2024-11-10 20:27:53.904536+00
94	0462dd6c-b60b-44ed-b0dc-439c03bdeac4	80.00		2024-11-10 20:28:08.329957+00	4	7	3	2	2024-11-02 20:27:54+00	2024-11-10 20:28:08.329948+00
95	4cc6ec99-e231-4bf2-af09-6ed1cc5eb479	40.00	Desayunos almuerzos y comida	2024-11-10 20:28:30.626936+00	4	8	2	3	2024-11-02 20:28:08+00	2024-11-10 20:28:30.626924+00
96	7b898533-2749-475f-9200-c07e0c7caa3a	32.00		2024-11-10 20:28:45.737512+00	4	5	3	2	2024-11-02 20:28:30+00	2024-11-10 20:28:45.737503+00
97	5183becd-3277-48b5-b7f2-de648bc2ff33	15.00	Mercado	2024-11-10 20:36:50.868263+00	4	8	3	2	2024-11-03 20:36:32+00	2024-11-10 20:36:50.868255+00
98	015601f5-289c-4fdc-ba5c-1db31e056deb	7.00	Mercadito	2024-11-10 20:37:10.819831+00	4	8	3	2	2024-11-03 20:36:51+00	2024-11-10 20:37:10.81982+00
99	60c5ad6b-2910-4a4d-83c6-5ab243afb853	30.00		2024-11-10 20:45:00.318468+00	4	9	3	2	2024-11-04 20:43:52+00	2024-11-10 20:45:00.318459+00
100	b7046fc7-78da-40a2-a483-28b0836438b4	11.50	Almuerzo	2024-11-10 20:50:15.114993+00	4	8	3	2	2024-11-05 20:49:56+00	2024-11-10 20:50:15.114981+00
101	487699ba-3ea0-4869-8005-85f60abfd2d4	13.50	Comidas	2024-11-10 20:50:33.727183+00	4	8	3	2	2024-11-05 20:50:15+00	2024-11-10 20:50:33.727174+00
102	2c51e380-6910-41b5-8970-59c1df6aba82	300.00	Daniel ojeda	2024-11-10 20:50:49.719904+00	4	7	3	2	2024-11-05 20:50:34+00	2024-11-10 20:50:49.719893+00
103	0da6eb15-c40a-4e92-8018-129b292bec52	15.80	Comidas	2024-11-10 20:51:22.320592+00	4	8	3	2	2024-11-06 20:51:06+00	2024-11-10 20:51:22.320579+00
104	1c029799-c668-4d5f-ae82-3d935a11fc4d	20.00	Pago de enseñanza conducción	2024-11-20 21:11:56.916443+00	4	7	3	2	2024-11-08 21:11:30+00	2024-11-20 21:11:56.916435+00
105	f8b5296c-6e68-4222-b471-6de1882ed490	12.50	Almuerzos	2024-11-20 21:26:51.982505+00	4	7	3	2	2024-11-08 21:26:37+00	2024-11-20 21:26:51.982496+00
106	8d7ec454-6331-4225-a396-d1e02a5bd2a7	15.00	Comida	2024-11-20 21:27:09.870427+00	4	8	3	2	2024-11-08 21:26:52+00	2024-11-20 21:27:09.870414+00
107	169bd836-8508-4f86-a356-cfd6e632a314	24.00	Marcos instructor	2024-11-20 21:57:09.670834+00	4	7	3	2	2024-11-09 21:56:51+00	2024-11-20 21:57:09.670823+00
108	e415a069-1fd6-4054-a1f4-1976a62e1e66	5.50	Almuerzo	2024-11-20 21:57:27.975611+00	4	8	2	3	2024-11-09 21:57:09+00	2024-11-20 21:57:27.975602+00
109	26a3e3d5-fe30-4597-aa1d-3903222784d4	20.00	Lince	2024-11-20 21:57:41.198894+00	4	7	2	3	2024-11-09 21:57:28+00	2024-11-20 21:57:41.198884+00
110	a82f27b4-de8d-4831-9c0d-bae812d6dab1	1.50	Almuerzo	2024-11-20 22:48:57.475126+00	4	8	3	2	2024-11-11 22:48:39+00	2024-11-20 22:48:57.475116+00
111	14cae1b4-7102-4e5d-97d0-8041ee9e6024	50.00	Cafe	2024-11-20 22:49:14.666276+00	4	8	3	2	2024-11-11 22:48:57+00	2024-11-20 22:49:14.666265+00
112	8de8cc5c-ea9f-4150-b52c-6d98d3aaf6ef	238.00	Daniel Ojeda envió a mamá	2024-11-20 23:09:13.39284+00	4	7	2	2	2024-11-12 23:08:45+00	2024-11-20 23:09:13.39283+00
113	36a487eb-176c-4fdc-8fdf-3ea3c4e02a9b	9.80	Comida pio pio.	2024-11-20 23:09:28.278596+00	4	8	3	2	2024-11-12 23:09:13+00	2024-11-20 23:09:28.278588+00
114	ed105983-d09c-400c-bb77-f5c4685960ed	28.00	Mercado	2024-11-20 23:09:49.577917+00	4	7	3	2	2024-11-12 23:09:28+00	2024-11-20 23:09:49.577908+00
115	fcc9afa3-d72d-4abd-ad4d-9416256a01bc	20.00	Cama	2024-11-21 19:12:10.177672+00	4	7	3	2	2024-11-17 19:11:53+00	2024-11-21 19:12:10.177659+00
116	19119fdb-98ff-4cb8-bf21-2043cf45c41c	15.00	Almuerzo	2024-11-21 19:12:50.576391+00	4	8	2	3	2024-11-17 19:12:20+00	2024-11-21 19:12:50.576381+00
117	9adcbd1a-d3b1-49dd-a7c6-ea45e9e423a6	25.00	Almuerzo	2024-11-21 19:13:04.446108+00	4	8	3	2	2024-11-17 19:12:50+00	2024-11-21 19:13:04.446079+00
118	c00f3877-f4b9-4912-806f-dfab8240bb80	8.00	Mecatos y lavada de auto	2024-11-21 19:13:22.783999+00	4	7	3	2	2024-11-21 19:13:04+00	2024-11-21 19:13:22.783987+00
119	414e1141-8e50-4c7e-b94e-ac37fbf36fbf	15.50	Almuerzo	2024-11-22 00:43:00.269512+00	4	8	3	2	2024-11-19 00:42:47+00	2024-11-22 00:43:00.269501+00
120	e0ebbc55-3f05-4af6-9321-d589dfb96910	50.00	Mercado	2024-11-22 00:43:15.07018+00	4	7	3	2	2024-11-19 00:43:00+00	2024-11-22 00:43:15.070167+00
121	04c1d776-817a-4064-8eb7-0e30a897d58d	338.00	Compra de. Apple	2024-11-22 01:02:13.277382+00	4	7	3	2	2024-11-20 01:01:55+00	2024-11-22 01:02:13.277373+00
122	c1c4a066-054e-4a03-bacd-f3693ef02a33	14.00	Comida	2024-11-22 01:02:26.065787+00	4	8	3	2	2024-11-20 01:02:13+00	2024-11-22 01:02:26.065777+00
123	39b98901-f848-48b7-a38a-04a11496d8da	30.50		2024-11-22 01:02:39.369438+00	4	5	3	2	2024-11-20 01:02:26+00	2024-11-22 01:02:39.369427+00
124	8d33cfd7-e2ff-435d-b267-cf8fcf7cf9db	12.00	Almuerzos	2024-11-22 01:02:57.87632+00	4	8	3	2	2024-11-20 01:02:39+00	2024-11-22 01:02:57.876311+00
125	3c338255-eb31-4a10-b346-bb0a90d1640f	433.80	Pagos... 1er abono Carro	2024-11-27 00:28:05.923248+00	4	7	3	2	2024-11-21 00:27:42+00	2024-11-27 00:28:05.923236+00
126	05c066cb-bfa9-4a7e-b90e-27bd1185a369	250.00	Casa don villa	2024-11-27 00:28:22.473804+00	4	7	3	2	2024-11-21 00:28:06+00	2024-11-27 00:28:22.473791+00
127	22e39086-b4d3-4f9b-83c4-36ca6ae5476a	1000.00	Sueldo Jose	2024-11-27 00:28:46.16776+00	4	7	2	2	2024-11-21 00:28:22+00	2024-11-27 00:28:46.167747+00
128	4388567e-ab5a-4073-9f03-88f0a95471c0	338.00	Compra.. Abono a  Apple	2024-11-27 00:29:01.683434+00	4	7	2	3	2024-11-21 00:28:46+00	2024-11-27 00:29:01.683423+00
129	d21fe80c-17ab-4882-9de7-0ccf863d40c3	7.50	Almuerzo	2024-11-27 00:29:17.175621+00	4	8	2	3	2024-11-21 00:29:02+00	2024-11-27 00:29:17.175611+00
130	16a212eb-a724-48b7-b1bd-e1b519a752c8	375.00	Copmra de impresora.        375	2024-11-27 01:00:25.188273+00	4	7	3	2	2024-11-22 01:00:08+00	2024-11-27 01:00:25.188261+00
131	4bb44f24-04ec-49d5-8d90-3bd12c0e1971	20.00	Resma de papel	2024-11-27 01:00:42.693292+00	4	7	3	2	2024-11-22 01:00:25+00	2024-11-27 01:00:42.693278+00
132	c06e74b8-1494-4034-a0c3-0d7c3d537251	8.70	Comidas	2024-11-27 01:01:00.7773+00	4	8	3	2	2024-11-22 01:00:43+00	2024-11-27 01:01:00.77729+00
133	0bc1e0f0-4a3a-4bac-9d8e-36f8597bd7a4	12.50	Mercado	2024-11-27 01:01:33.171906+00	4	8	3	2	2024-11-22 01:01:07+00	2024-11-27 01:01:33.17189+00
134	2ca21144-d678-4e0f-a7b6-03d316253d65	20.00	Almuerzos.	2024-11-27 21:34:24.796604+00	4	8	3	2	2024-11-23 21:34:03+00	2024-11-27 21:34:24.796589+00
135	887096d0-cba6-4068-aed1-da8ca6039a30	10.00	Lava auto.	2024-11-27 21:34:40.574311+00	4	7	3	2	2024-11-23 21:34:25+00	2024-11-27 21:34:40.574298+00
136	1f32dec6-1797-41bf-8578-737dd1e7cbe1	10.00	Gastos cortesia	2024-11-27 21:34:56.076319+00	4	7	3	2	2024-11-23 21:34:40+00	2024-11-27 21:34:56.076303+00
137	9a4f13d8-dfa6-42d1-aac5-2fdb35c691a5	5.50	Almuerzo.	2024-11-27 22:22:55.821638+00	4	8	3	2	2024-11-25 22:22:40+00	2024-11-27 22:22:55.821598+00
138	46d46986-dd42-4142-8614-408512c8b422	13.50	Comidas tarde	2024-11-27 22:23:15.064971+00	4	8	3	2	2024-11-25 22:22:56+00	2024-11-27 22:23:15.064952+00
139	834ff3bf-e611-4d65-9519-152af0574d28	1000.00	Jose Daniel	2024-12-03 00:43:18.944843+00	4	7	3	2	2024-11-28 00:42:52+00	2024-12-03 00:43:18.944833+00
140	ce68ccd9-730e-48df-a0c1-b7f989718cd6	200.00	hon Mario. Medellin.	2024-12-03 00:43:35.569996+00	4	7	3	2	2024-11-28 00:43:19+00	2024-12-03 00:43:35.569986+00
141	f3059c85-497c-42f1-a2b2-5799203fecce	120.00	Iris  mi esposa	2024-12-03 00:43:53.407901+00	4	7	3	2	2024-11-28 00:43:35+00	2024-12-03 00:43:53.407887+00
142	1dd07267-a9d0-45b7-a412-aff9d69a7c36	270.00	Pago Banesco	2024-12-03 00:48:41.387587+00	4	7	3	2	2024-11-28 00:48:24+00	2024-12-03 00:48:41.387571+00
143	b17dd43b-bfa3-46bf-976f-149fefdf8631	5.50	Legumbres.	2024-12-03 00:59:44.448988+00	4	8	3	2	2024-11-29 00:59:19+00	2024-12-03 00:59:44.448974+00
144	4404d1c8-bc38-4864-9512-32fca87276b4	30.80	Gasolina Camioneta	2024-12-04 21:45:06.166082+00	4	5	3	2	2024-11-29 21:44:47+00	2024-12-04 21:45:06.166073+00
145	531262e5-3528-4bfb-a4e2-93cd811de763	5.50	Almuerzo.	2024-12-04 21:45:21.369179+00	4	7	3	2	2024-11-29 21:45:06+00	2024-12-04 21:45:21.369168+00
146	6db209c8-12d5-4939-93cb-3158217f564d	15.00	Legumbres	2024-12-04 23:06:49.575412+00	4	7	3	2	2024-11-30 23:06:35+00	2024-12-04 23:06:49.575403+00
147	5fb78d3c-e362-4d58-97c6-7d295ef45407	13.50	Comidas.	2024-12-04 23:07:12.17723+00	4	7	3	2	2024-11-30 23:06:49+00	2024-12-04 23:07:12.177217+00
148	356704cb-1af8-4960-afda-0a30bd271f82	14.00	Almuerzo.	2024-12-04 23:07:25.979323+00	4	7	3	2	2024-11-30 23:07:12+00	2024-12-04 23:07:25.979313+00
149	8a09b5c4-82a3-4c9f-84aa-ad1ed8e9c868	200.00	Pago a Frank. Natiyera	2024-12-05 23:34:46.963486+00	4	7	3	2	2024-12-01 23:34:32+00	2024-12-05 23:34:46.96347+00
150	e2cea662-6d6d-491b-b69a-de61332f2c11	2000.00	jhon Mario Ojeda. Univ	2024-12-06 00:27:31.016049+00	4	7	2	3	2024-12-03 00:27:08+00	2024-12-06 00:27:31.016039+00
151	0d0f5ada-7e52-449a-ab8a-dee588b98aad	125.00	Mi mama.	2024-12-06 00:27:45.366452+00	4	7	3	2	2024-12-03 00:27:31+00	2024-12-06 00:27:45.366437+00
152	82c0ead2-1b1a-4a17-898f-f873cf74c0a8	25.00	Envioss.	2024-12-06 00:28:00.270611+00	4	7	3	2	2024-12-03 00:27:45+00	2024-12-06 00:28:00.2706+00
153	b2ab261d-adc0-4097-bed2-09f0f3c877f2	29.00	Almuwezo y comidas.	2024-12-06 00:28:22.672318+00	4	8	3	2	2024-12-03 00:28:00+00	2024-12-06 00:28:22.672306+00
154	64793cc7-ecdd-46d3-8953-fc803f35727b	31.00	Gasolona del carro	2024-12-06 00:50:34.779233+00	4	5	3	2	2024-12-06 00:50:10+00	2024-12-06 00:50:34.77922+00
155	69fdbd56-8fd4-4419-9bae-db6f9b047ded	11.60	Almuerzos.	2024-12-06 01:13:46.381371+00	4	8	3	2	2024-12-05 01:13:29+00	2024-12-06 01:13:46.381359+00
\.


--
-- Data for Name: fintech_identifier; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_identifier" ("id", "document_number", "country_id", "document_type_id") FROM stdin;
1	1214724312	1	1
\.


--
-- Data for Name: fintech_label; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_label" ("id", "uid", "name", "position") FROM stdin;
4	60574d9a-e72b-43a4-8d8f-40ec63c512d4	Hotel Bijao	\N
5	09afb313-bc47-493b-8271-120959ab3354	Panaderia Sabores	\N
6	365426b0-89f8-41a9-be73-832990bb9c0a	Super Extra	\N
7	d68922ef-a498-4d21-968b-4b83130a11a0	Colegio San Francisco Penonome	\N
8	5ccdbb79-c83d-4787-a062-667fd053a417	Escuela Chorrera	\N
9	d7fde171-a6e9-44b7-a36b-74306d45d29c	Escuela de las guabas	\N
10	b6ccc614-1af1-4392-82db-e315fe824b30	Escuela Dominicana	\N
11	226f5fa5-2df3-46bf-a3ef-d99067ed9678	Escuela Manuel Patiño	\N
12	ceb71cb0-62d0-4fb4-9207-f33d8716fe02	IPEHE Antón	\N
13	53743801-0c07-4200-ba7c-05779112bbce	IPEHE Penonome	\N
15	184ffc10-44d5-45be-a952-0ce1fd82b70c	Salomon Ponce Aguilera	\N
16	de1f7b43-fa50-4a2e-86e7-4ad9da89e79c	SPA	\N
17	c960feb0-2a3c-4a45-9da1-14ecf0e79657	Universidad Nacional de Panamá	\N
18	1a7c7ddd-3fbd-4261-9c5d-8217167f36cf	Universidad Tecnologica de Panamá	\N
19	ecd76440-4b95-4ca9-a001-5ee93886604e	Universidad UDELAS	\N
20	b6fbbe52-ada3-4067-9dc7-e9245c60d4e8	Colegio de la madera	\N
22	d2870554-e48d-4d4a-93d4-60b1f5f982f3	Odontologo	\N
23	f85a36ad-88be-47da-a996-10fcacb0af50	Familia Mendoza	\N
24	d270b324-cf72-4eb9-8fdc-c0825b501d84	Super Market Anton	\N
26	a23cd55c-6cfa-4233-860a-448a762751d5	Super Anton	\N
1	4ffbf554-7d10-477b-8c17-e847716c17fa	Inadeh	\N
3	4c862bda-1d93-4549-856a-90263d004899	Hotel Buenaventura	\N
28	0c04d6fc-2142-4c8b-87e4-74d43032651e	Escuela Primaria el Valle de Anton	\N
29	47811187-e424-4f57-a9ac-1a2d0776b9c6	Mundo Magico	\N
30	41fdd4c6-5503-4287-8697-7fb5de2deeaf	Hotel Playa Blanca	\N
31	3321d000-86c9-423b-98ea-c213492fd4a1	Hotel Decameron	\N
32	03461b5d-2057-41e2-9d35-903a07f53785	Banco Banesco	\N
33	b0475b6e-2571-4ed8-9750-263b67e6cf9c	Mega Xpress	\N
27	71c62f2e-2d4d-4fb4-a2b5-4126c9a63dd6	Do it Center	\N
25	63ae349d-d4f9-4c6f-a4cc-7826e9e6d77b	Super Cocle	\N
21	acadf812-84a0-403c-b52f-1f50382e5e34	Fonda Familion	\N
34	2dc9a332-864e-4e82-9887-4c21ae1daa62	Delta	\N
35	4cdc3ba0-e8c3-40ee-bf5b-d448814a9b90	Bomba Delta	\N
\.


--
-- Data for Name: fintech_language; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_language" ("id", "name", "region_of_use") FROM stdin;
\.


--
-- Data for Name: fintech_paramslocation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_paramslocation" ("id", "city_code", "city_name", "state_code", "state_name", "country_code", "country_name") FROM stdin;
\.


--
-- Data for Name: fintech_periodicity; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_periodicity" ("id", "name", "days") FROM stdin;
1	Daily	1
2	Weekly	7
3	Beweekly	15
4	Monthly	30
\.


--
-- Data for Name: fintech_phonenumber; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_phonenumber" ("id", "country_code", "phone_number", "country_related_id") FROM stdin;
\.


--
-- Data for Name: fintech_role; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_role" ("id", "name", "is_staff_role") FROM stdin;
1	User	f
2	Controller	t
\.


--
-- Data for Name: fintech_seller; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_seller" ("id", "total_sales", "commissions", "returns", "role_id", "user_id") FROM stdin;
1	0.00	0.00	0	2	4
\.


--
-- Data for Name: fintech_subcategory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_subcategory" ("id", "uid", "name", "description", "created_at", "updated_at", "category_id") FROM stdin;
2	d52dd0d0-3d37-4d5d-a154-01049b8e802c	Crédito Personal		2024-09-11 02:58:46.278271+00	2024-09-11 02:58:46.278281+00	2
1	13183c33-9780-4a02-99a6-418f1bf54974	Crédito de Consumo		2024-09-11 02:58:26.789907+00	2024-09-11 02:58:58.352391+00	2
3	30ed0c5c-df6e-47bd-a5c9-574df819daec	Crédito Hipotecario		2024-09-11 02:59:13.422696+00	2024-09-11 03:00:12.602083+00	2
4	4dbf0c32-0242-4ff4-8c38-7ec0e92ad7de	Transporte		2024-09-11 05:39:37.675142+00	2024-09-11 05:44:40.848521+00	12
5	6acb9bbb-16c7-4230-965e-333e1bc78015	Gasolina		2024-09-11 05:45:07.396242+00	2024-09-11 05:45:07.396261+00	12
6	a3e499d3-14f0-4ae8-a084-309c008d6ade	Rent a car		2024-09-11 05:46:41.910874+00	2024-09-11 05:46:41.910893+00	12
9	e65011f7-aa02-4319-bc02-afee1120e33a	Pago a Crédito Personal		2024-09-11 21:22:50.851644+00	2024-09-11 21:22:50.851664+00	2
11	81744af1-f7cd-4581-b419-1b1628326a9e	Pago a Crédito Hipotecario		2024-09-11 21:24:18.548488+00	2024-09-11 21:24:18.548502+00	2
10	68073612-81f5-44dd-827c-bf36d7e3bd51	Pago a Crédito de Consumo		2024-09-11 21:23:39.122606+00	2024-09-27 17:35:59.368031+00	2
8	1a24aa98-8e13-4196-894f-35f883e5e8dc	Viatico	Comida	2024-09-11 15:12:38.298353+00	2024-09-27 17:45:32.331455+00	12
7	571d7251-bee2-40b7-9afa-f2e4f633b712	Otros		2024-09-11 15:10:05.707895+00	2024-09-27 17:45:48.724608+00	12
12	a0a2030b-7994-4b8b-81dd-e39a5841cf45	Movimiento		2024-09-27 17:46:40.126028+00	2024-09-27 17:46:40.126046+00	7
\.


--
-- Data for Name: fintech_transaction; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_transaction" ("id", "uid", "transaction_type", "date", "description", "category_id", "user_id") FROM stdin;
4	3124c05f-5643-4b5b-a769-af86ddeaaae9	income	2024-08-28 20:52:45+00		2	6
6	f428a133-8b0f-4509-9e04-80cfa79ded6b	income	2024-09-01 21:06:56+00	Crédito creado con monto de 255	2	7
7	7799f484-28a3-4a00-9978-b1c26fd2da1d	income	2024-08-29 21:14:46+00		2	6
8	d0967809-5b8b-418f-b85d-8acd27a05312	income	2024-09-11 21:15:37+00		2	7
9	3c87dfc8-16cc-4531-8326-0fc9acdfb07f	income	2024-09-11 21:14:03+00	Crédito creado con monto de 1200	2	8
10	5f8b5b58-0c24-4b01-a90d-185fdef58eb9	income	2024-09-02 21:18:08+00	Crédito creado con monto de 300	2	9
56	9a6a6ddd-4297-464d-b49d-b2db798e56d6	expense	2024-09-12 21:09:22+00	Crédito de $50.00 registrado.	1	28
57	bb322580-1cf6-45a0-92f2-7af1bf913d94	expense	2024-09-12 21:10:53+00	Crédito de $150.00 registrado.	2	29
1	87887c5e-b16b-49ae-981c-555138939869	expense	2024-08-31 19:32:56+00	Crédito creado por valor de $152.00	2	4
2	8af749bb-e342-4a2f-bc72-dbb526165c06	expense	2024-09-11 19:43:24+00	Crédito creado por  valor de $270.00	2	5
3	619a3a83-b3d5-4028-901d-7c6e1bb461d4	expense	2024-08-15 19:45:52+00	Crédito creado con monto de 1100	2	6
5	a67429f5-9a2c-4d20-a47d-75f0572ff7ee	expense	2024-08-02 21:03:14+00	Crédito creado por valor de $140.00	2	7
13	a3c0647c-4b46-4275-af61-dac6a622a976	expense	2024-09-09 23:37:26+00	Crédito creado por valor de $140.00	2	3
12	d57c8962-2dd2-4ea0-a396-d39706cc081b	expense	2024-09-09 23:36:25+00	Crédito creado por valor de $90.00	2	2
11	65557758-50cd-42a3-afeb-d9502ae2febd	expense	2024-09-09 23:35:35+00	Crédito creado por valor de $160.00	2	1
1220	fb88ede9-fbf7-4167-9eac-a7e123956ef7	income	2024-11-20 23:59:25+00		9	49
58	f6f5b758-35f5-4dfe-8faf-040af65233d4	expense	2024-09-12 21:11:59+00	Crédito de $70.00 registrado.	2	30
59	96d8feff-2551-4879-b54f-225b0013a82e	expense	2024-09-11 21:19:47+00	Crédito de $140.00 registrado.	2	31
19	ca8c23e8-8508-42c7-bf96-ce321ac42f98	expense	2024-08-21 23:57:11+00	Crédito creado por valor de $300.00	2	11
23	055aba76-9479-4e27-a814-74f353c5ca29	expense	2024-09-04 15:37:57+00	Crédito de $1200.00 registrado.	2	10
24	0643287e-c184-4dad-b9cb-9fa6551bdb52	income	2024-09-05 15:39:11+00		9	10
60	9bf4b237-8cdf-4ea8-a2be-c1ec597203aa	expense	2024-09-11 21:20:51+00	Crédito de $140.00 registrado.	2	32
25	969547cc-7f7d-4bd4-ab9c-aad7f41ba324	income	2024-09-06 15:45:10+00		9	10
27	872cb688-3215-422e-9dfd-b22387e043c4	income	2024-09-09 15:51:46+00		9	10
26	9128174b-2d27-486b-ab9c-eda96cc0a100	income	2024-09-07 15:48:13+00		9	10
28	401a3783-1dc3-4216-9db0-ba679d0306bc	expense	2024-07-31 23:53:24+00	Crédito de $300.00 registrado.	2	12
29	48c46617-1473-4552-b005-7515e25b8d9a	expense	2024-07-31 23:55:44+00	Crédito de $525.00 registrado.	2	13
31	60469042-352b-45b4-88b7-d40dfc86e839	income	2024-08-17 00:01:02+00		9	13
32	1e5457fb-0ed6-488c-a574-70c6e689b785	income	2024-09-02 00:05:26+00		9	13
33	4be218b2-0260-4512-9515-45c0e7bb782a	expense	2024-08-01 00:07:08+00	Crédito de $80.00 registrado.	2	14
34	a69d3835-301b-4d0e-bd1a-1e51bfa7e47d	expense	2024-08-01 00:13:53+00	Crédito de $300.00 registrado.	2	15
35	71f34f99-caaf-450f-8b33-fdc246074a1c	income	2024-08-16 00:17:47+00		9	15
36	375f6ebe-add8-46ca-9c03-59e12dff8094	income	2024-09-05 00:18:21+00		9	15
37	c0a28813-db2f-4e98-bed3-3b8f0144795d	expense	2024-08-02 00:21:08+00	Crédito de $300.00 registrado.	2	16
38	6fa004bd-181a-4998-adbe-202f954a9611	expense	2024-08-02 00:24:34+00	Crédito de $510.00 registrado.	2	17
39	ce011ea2-8278-4b54-bb5b-954e1fbb91af	income	2024-08-16 00:26:03+00		9	16
40	5dd781f1-9250-4abc-ab79-00ebb14a0f7d	income	2024-09-03 00:26:41+00		9	17
41	aa071d07-79fd-411e-a6c7-a2480a43a473	expense	2024-08-02 00:28:50+00	Crédito de $150.00 registrado.	2	18
42	d6e3ead3-d242-487d-a6a4-1e37cfdeefe0	expense	2024-08-02 00:30:56+00	Crédito de $510.00 registrado.	2	19
43	c9d7c9aa-4b6a-488d-9280-edcafcaa3e5f	income	2024-08-16 01:04:21+00		9	19
44	1a3daf50-77bc-458a-aef9-f267ae160a18	income	2024-08-31 01:05:29+00		9	19
45	94170a50-1f2d-4f17-892d-b4d462759b51	expense	2024-08-03 01:08:31+00	Crédito de $600.00 registrado.	2	20
46	33783945-cfd7-409a-8143-098b5b90b799	expense	2024-08-03 01:13:17+00	Crédito de $165.00 registrado.	2	21
47	fce9eb07-cf6c-4790-8338-7accf2aba8d1	income	2024-08-11 01:15:10+00		9	21
48	8f9358d5-2624-473f-9f38-0ebd260d5808	expense	2024-08-25 01:16:03+00		9	21
49	b1e5a337-d829-41c2-bd51-7db50ff47cdd	expense	2024-08-03 01:17:23+00	Crédito de $165.00 registrado.	2	22
50	21b8b09a-b238-4db7-a0bd-536d0bc78c02	expense	2024-08-03 01:19:45+00	Crédito de $140.00 registrado.	2	23
51	1d35d6c8-3870-4880-b1d6-67b70d9a5539	expense	2024-09-13 18:47:15+00	Crédito de $50.00 registrado.	2	24
52	a2c2b381-8f38-4491-92ff-09ab9137a5ef	expense	2024-09-12 18:51:19+00	Crédito de $100.00 registrado.	2	18
53	6ce94bb8-6efd-4f35-86da-0c559924c5f1	expense	2024-09-12 19:51:04+00	Crédito de $50.00 registrado.	1	25
54	2fa8a8d1-4b7a-499d-9aa6-138737bb8e62	expense	2024-09-12 21:05:53+00	Crédito de $50.00 registrado.	1	26
55	0ddd3ea1-ddcd-4ffc-9d4f-2ec6604967fa	expense	2024-09-12 21:08:15+00	Crédito de $50.00 registrado.	1	27
61	13bd666b-a19f-4916-af34-1786c2d07882	expense	2024-09-10 21:21:39+00	Crédito de $750.00 registrado.	2	33
62	cf34790e-ec47-4ca4-91b0-42604779119e	expense	2024-09-10 21:24:41+00	Crédito de $90.00 registrado.	2	34
63	f0d43ae6-484a-4283-978b-16a3254571e5	expense	2024-09-10 21:26:06+00	Crédito de $80.00 registrado.	2	35
64	1c119387-0c16-44cc-b3b8-ca9d45d2b044	expense	2024-09-10 21:28:03+00	Crédito de $140.00 registrado.	2	36
65	ab662f71-514d-485e-98d6-7398e6a73e27	expense	2024-09-10 21:29:20+00	Crédito de $140.00 registrado.	2	37
66	dd04fa05-b62d-46cc-b7b4-a3a4b96c2e76	expense	2024-09-08 22:42:39+00	Crédito de $200.00 registrado.	2	38
67	60126ff2-c819-4a45-8223-80e58c8e77e0	expense	2024-09-08 22:43:45+00	Crédito de $90.00 registrado.	2	39
68	7e849e0b-e6c9-4706-94fe-32d8334733a1	expense	2024-09-07 22:47:04+00	Crédito de $140.00 registrado.	2	40
69	2cdeab3d-883f-4caa-a7de-4653b392016a	expense	2024-09-06 22:52:07+00	Crédito de $150.00 registrado.	2	41
70	0c6dc1b4-a43b-46fa-9133-4e287f79c74b	expense	2024-09-06 22:53:58+00	Crédito de $80.00 registrado.	2	42
71	9d68e664-526f-4994-a4d8-8ad7d16bd034	expense	2024-09-06 22:56:24+00	Crédito de $140.00 registrado.	2	43
72	21c4f796-22d7-4202-ac45-665c624b29cc	expense	2024-09-06 22:57:37+00	Crédito de $65.00 registrado.	2	44
73	1e021797-e5a3-4731-a13b-f8d04b31251b	expense	2024-09-06 22:58:38+00	Crédito de $300.00 registrado.	2	45
74	0c799820-b735-415d-8e6b-a8dd743210eb	expense	2024-09-05 23:05:53+00	Crédito de $150.00 registrado.	2	46
75	761ccbdf-4ac2-4ec7-9876-cbc78361179b	expense	2024-09-05 23:07:01+00	Crédito de $80.00 registrado.	2	47
76	82cb50f8-ce4c-4306-9ba5-826ceda9fcc0	expense	2024-09-05 23:08:41+00	Crédito de $130.00 registrado.	2	48
77	9774ad22-ae2f-4f8a-a6fb-7d939cde6164	expense	2024-08-04 23:29:45+00	Crédito de $4200.00 registrado.	2	49
78	b3f10def-5cd6-4275-ae27-4447a5f5223c	expense	2024-08-06 23:37:59+00	Crédito de $360.00 registrado.	2	50
79	908d5955-88f0-4a56-9519-514db8f12369	expense	2024-09-13 23:39:50+00		9	50
80	4c04a092-d62d-4737-afee-39925ef4e3c2	expense	2024-09-09 23:43:08+00		9	33
81	7b9975a6-75db-4a19-9134-dd15c51621f3	expense	2024-08-10 00:09:41+00	Crédito de $90.00 registrado.	2	51
82	48e7a547-aeba-4c71-9bd9-966c35a54e34	expense	2024-09-03 00:47:50+00	Crédito de $50.00 registrado.	1	29
83	01074af7-8d76-4723-a50c-2e90088ae301	expense	2024-09-05 00:56:41+00	Crédito de $100.00 registrado.	2	52
84	4353a6e7-f682-4342-b31d-ebdc1877ded6	expense	2024-09-05 00:58:43+00	Crédito de $480.00 registrado.	2	53
85	9ac89b03-8cd5-4236-8b50-e028218c8086	expense	2024-09-05 01:02:08+00	Crédito de $150.00 registrado.	2	15
86	4a9b6d54-b540-4248-9a9b-e196e5c57c04	expense	2024-09-05 01:02:49+00	Crédito de $140.00 registrado.	2	54
87	196827e4-b545-4f63-a0bb-fe9e4358a59b	expense	2024-09-04 01:17:15+00	Crédito de $260.00 registrado.	2	55
88	bf10ecc5-16e4-48d7-8684-323364c9091c	expense	2024-09-04 01:19:05+00	Crédito de $360.00 registrado.	2	56
89	ad7447da-ff45-4a18-9ea5-9b3a7ff3e383	expense	2024-09-04 01:21:09+00	Crédito de $600.00 registrado.	2	57
90	039d087a-08ab-4408-b182-4caf41245802	expense	2024-09-04 01:22:01+00	Crédito de $300.00 registrado.	2	58
91	922fbf5a-d91e-4d54-a67f-cbe45a184e63	expense	2024-09-04 01:23:03+00	Crédito de $165.00 registrado.	2	23
92	79ca5edf-bfc6-452c-a86e-5d2661e5483e	expense	2024-09-03 01:25:41+00	Crédito de $300.00 registrado.	2	9
93	ce19b632-68c7-4c23-a782-16ee9ae29a80	expense	2024-09-03 01:26:21+00	Crédito de $80.00 registrado.	2	59
1221	3001c4cc-8e70-4614-b917-c5e87423eef6	income	2024-11-21 00:03:06+00		9	240
95	fdc5c849-c531-480b-92b8-82bf15376419	expense	2024-09-03 01:28:10+00	Crédito de $90.00 registrado.	2	29
96	9a9c43af-e65c-4443-a0d5-aec5f27e7bd4	expense	2024-09-03 01:28:40+00	Crédito de $255.00 registrado.	2	60
97	e2626f22-5509-44e6-9c67-b3cd27618ccf	expense	2024-09-03 01:29:49+00	Crédito de $140.00 registrado.	2	61
98	e7d491f1-fdbf-4f08-bdba-23d9e8bf847f	expense	2024-09-03 01:31:40+00	Crédito de $165.00 registrado.	2	62
99	63aa662f-a930-4540-9e29-deac2fc55ded	expense	2024-09-03 01:32:48+00	Crédito de $255.00 registrado.	2	63
100	a95a0b8a-74c8-4b7d-92bd-62406fe39fe7	expense	2024-09-03 01:34:19+00	Crédito de $300.00 registrado.	2	64
101	5c59d0e6-0225-4739-8729-854a3fd85ef9	expense	2024-09-03 01:36:14+00	Crédito de $150.00 registrado.	2	65
102	844385c2-54b8-477d-aff2-3e1946d93287	income	2024-09-05 17:44:26+00		9	10
103	89fa3305-d591-436b-9dbd-e7df3afbe201	income	2024-09-06 17:45:36+00		9	10
104	3d3996df-3b87-4f90-9ae1-9dfb76bde09e	income	2024-09-07 17:46:49+00		9	10
105	ac2a4ab7-83ef-47cb-b31c-a8df6022de11	income	2024-09-09 17:49:28+00		9	10
106	e7f35051-71de-4c61-bd85-5cf2ba896950	income	2024-09-10 17:50:14+00		9	10
107	30c8289c-9c28-4fe8-8b4f-08b7990ef8a5	expense	2024-09-13 17:55:26+00	Crédito de $315.00 registrado.	2	66
108	4e218b9a-a935-4f4f-8d95-70a4a688c9a2	expense	2024-08-09 17:58:59+00	Crédito de $345.00 registrado.	2	67
109	a0fc149a-27b8-484c-a439-9300c5c5123b	expense	2024-08-09 18:00:50+00	Crédito de $270.00 registrado.	2	68
110	dbde94b7-1de2-44cf-99f8-91083b24b883	expense	2024-08-11 18:04:00+00	Crédito de $150.00 registrado.	2	69
111	3a691784-4679-4231-8943-8959d6a23908	income	2024-08-24 18:15:10+00		9	69
112	de6a9779-75e4-484c-bd6b-3e025dbdd0f7	income	2024-09-07 18:16:24+00		9	69
113	5bfd0426-f78a-4f5a-b967-a1ac9510079f	income	2024-09-08 18:17:08+00		9	69
114	163ef31a-1f40-4990-9870-6e4790870969	income	2024-08-17 18:54:58+00		9	69
115	592b2473-93a1-4a32-b1d3-a3fb68a27043	expense	2024-08-12 19:31:52+00	Crédito de $220.00 registrado.	2	70
116	c03ddcf3-90c0-458b-a9cf-e0481abee4be	expense	2024-08-12 19:57:36+00	Crédito de $630.00 registrado.	2	71
117	65b91460-de60-416c-afb4-0b67f1f417b0	income	2024-09-02 20:01:46+00		9	71
118	7ae237f5-1f5f-48a1-85f3-2d296f070966	expense	2024-08-13 20:02:29+00	Crédito de $600.00 registrado.	2	72
119	69f4631e-aea6-48f3-a3cc-c9a330e75b69	expense	2024-08-13 20:03:47+00	Crédito de $560.00 registrado.	2	73
120	11315f4d-fcea-48f7-9a12-e3e7e06a9e11	income	2024-08-24 21:12:00+00		9	72
121	ffd6701b-b5e0-4138-8176-600a4c32a6b9	income	2024-09-08 21:12:42+00		9	72
122	8370bac0-60b3-48d9-8421-3c7c552f4fae	income	2024-08-27 21:13:18+00		9	73
123	23ee3115-3c44-4327-9242-40b2f6cb8693	expense	2024-08-18 21:21:02+00	Crédito de $140.00 registrado.	2	37
124	54ec985a-bc92-4fa9-8b5c-f3aff23a5cea	expense	2024-08-13 21:21:55+00	Crédito de $380.00 registrado.	2	74
125	c3d61b44-efa4-4c4f-a99a-83a48f959015	expense	2024-08-13 21:26:05+00	Crédito de $330.00 registrado.	2	75
126	5ceaf034-bbc7-4220-a34e-43e05faffb7a	income	2024-09-10 21:33:20+00		9	37
127	8490cfad-9aec-49ec-b983-7ca0d0d32538	income	2024-08-24 21:34:44+00		9	74
128	c80b1f5f-a275-47cf-a386-5911a36f65c2	income	2024-09-10 21:36:10+00		9	74
129	2c262841-81fc-4708-ad7e-b8897398800e	income	2024-08-27 21:37:04+00		9	75
130	4a451cd6-e86a-44f6-bb4a-65f36ae0f866	income	2024-09-12 21:38:14+00		9	75
1234	83f88d5a-d5bd-45d5-8958-634f62f79957	income	2024-11-22 00:56:51+00		9	49
132	8ce47862-322c-4dd0-a3fd-5a4d82e62329	expense	2024-08-14 21:59:12+00	Crédito de $330.00 registrado.	2	51
133	115ecb9c-40e8-49e7-9832-88ced5ac241c	income	2024-09-02 22:00:56+00		9	51
134	950fc649-2690-4efe-a875-49cefd665fb0	income	2024-09-13 22:02:02+00		9	51
135	4e44fa7d-8aea-4581-bfaf-681a0ad4b2bd	expense	2024-08-14 22:08:35+00	Crédito de $740.00 registrado.	9	76
136	db313b2e-989d-4c0b-9f35-706da9e037b9	expense	2024-08-15 22:49:29+00	Crédito de $300.00 registrado.	2	77
137	77cb7a93-08bd-4495-b8f7-f23351d5e401	expense	2024-08-15 22:51:00+00	Crédito de $140.00 registrado.	2	78
138	4d8b84b7-d27f-4815-b107-472febf27837	income	2024-08-30 22:52:28+00		9	78
139	91247791-87ac-4400-875c-b5cbef28a296	expense	2024-08-16 23:38:46+00	Crédito de $140.00 registrado.	2	32
140	63df3737-89bb-48c8-b8a2-57b8114683ce	expense	2024-09-13 23:43:45+00	Crédito de $500.00 registrado.	2	64
141	4df86820-ff9d-4ef4-91e2-ac9720a9e894	expense	2024-09-13 23:44:28+00	Crédito de $140.00 registrado.	2	79
1251	a2be617a-852b-4652-aa09-40b53430a3c2	income	2024-11-23 01:20:50+00		9	176
144	3fc73133-3c1a-4515-a5f1-a9ff35cb5020	expense	2024-09-13 23:45:55+00	Crédito de $5600.00 registrado.	2	49
1256	568dc3ef-1c99-4654-a6f6-ae4e91345b52	income	2024-11-23 21:29:14+00		9	103
1261	c1225e7e-e0c4-4032-b809-87d2c0ae313b	income	2024-11-23 21:31:39+00		9	135
1265	59925bf6-5db9-49fa-9d26-1148eba64155	income	2024-11-24 21:38:24+00		9	240
1269	66b9a963-ad97-44d9-be17-30fb4bf1d2a9	expense	2024-11-26 21:44:21+00	Crédito de $140.00 registrado.	2	40
149	821840bd-d835-43e6-baaf-ebd0778b2e34	expense	2024-09-13 23:46:54+00	Crédito de $270.00 registrado.	2	24
150	1ebdee98-1046-4219-b0cd-89f348d0062e	expense	2024-09-13 23:47:12+00	Crédito de $375.00 registrado.	2	80
151	8cf97c82-8e15-490b-9b55-5d2dc3a5d21b	expense	2024-09-13 23:50:06+00	Crédito de $130.00 registrado.	2	81
152	b1829659-15ff-438e-8e1c-43b2718f8c82	expense	2024-09-13 23:50:56+00	Crédito de $500.00 registrado.	2	5
153	b1a78f9a-506a-4162-82ff-f1ee7e5d6cc2	income	2024-09-13 23:51:40+00		4	8
154	aac264ed-5f17-4552-b853-bf73faa7aeb7	expense	2024-09-14 00:01:09+00	Crédito de $225.00 registrado.	2	82
155	55ac118d-039d-4390-9a52-941d6f6b174a	expense	2024-08-17 00:04:56+00	Crédito de $330.00 registrado.	2	83
156	fe5bab33-e12e-4645-bfa2-4269de352712	income	2024-09-01 00:10:38+00		9	82
1272	168bba37-06b4-4ac3-90e6-b4ca36a57823	income	2024-11-25 21:55:40+00		9	186
157	e83e0ed2-5422-4fef-a9f9-685de6a4aa3e	income	2024-09-01 00:13:19+00		9	83
159	0b0fa4a0-d6c1-415f-a8c6-57236a4d2d24	expense	2024-08-17 00:21:01+00	Crédito de $130.00 registrado.	2	84
160	e2ae4ffc-000d-4c2f-8cd7-9dacabacdcaa	expense	2024-08-17 00:23:27+00	Crédito de $540.00 registrado.	2	85
161	9a8b1d31-697f-4bd7-af88-6e061a910db1	income	2024-09-03 00:28:37+00		9	84
1222	8e66e640-8e86-407e-82f5-72aa58cfb357	expense	2024-11-21 00:04:39+00	Crédito de $5600.00 registrado.	2	49
162	0114cfbd-6e2a-42af-bbc0-162278f945ab	income	2024-09-03 00:28:37+00		9	85
163	95f36887-d2c2-4fb6-806e-7ba29bf92939	expense	2024-08-18 00:34:12+00	Crédito de $165.00 registrado.	2	86
164	a1b74a04-89bf-4575-afd1-ae13b2c5598f	expense	2024-08-18 00:38:03+00	Crédito de $150.00 registrado.	2	87
165	a48a4b1d-7c82-46cc-b68b-7a84cb25e90d	expense	2024-08-18 00:41:24+00	Crédito de $150.00 registrado.	2	88
166	2cd06eb0-6458-49f5-aab5-a4e1277c464f	expense	2024-08-18 00:43:18+00	Crédito de $255.00 registrado.	2	90
167	4b6507ce-d8fa-4e9a-9333-2a93338243e7	expense	2024-08-18 00:47:01+00	Crédito de $255.00 registrado.	2	89
168	85c2d85b-c759-43ec-94d2-bdee0a60192d	income	2024-09-15 00:48:08+00		9	89
170	f1dcffb6-52a6-4c04-9a99-a7b9a886cc00	expense	2024-08-18 00:52:23+00	Crédito de $140.00 registrado.	2	91
171	f25a8da1-0532-4d50-bc18-a4899066baf9	income	2024-09-04 00:58:16+00		9	91
172	0201998f-a564-403f-a734-0fef444afef5	income	2024-09-12 01:01:43+00		9	73
173	2d483622-79cc-4c03-ac43-1a31aa42dec7	expense	2024-08-20 01:11:12+00	Crédito de $120.00 registrado.	2	92
174	0bf271e7-4a1a-4f3e-bfb4-e5b2797a964d	income	2024-08-31 01:14:54+00		9	92
175	de17067e-7af4-432f-bcba-8056de49694a	expense	2024-08-20 01:16:36+00	Crédito de $450.00 registrado.	2	93
176	94719727-f0f1-4bc8-bdcc-6a5fa27cef1e	expense	2024-08-21 01:19:20+00	Crédito de $140.00 registrado.	2	94
177	53bdc8fa-eed0-450e-99dd-e35e0744d0db	expense	2024-08-21 01:21:21+00	Crédito de $140.00 registrado.	2	95
178	7beed4a2-09dd-46d1-aabe-e99d0b130ddf	expense	2024-08-21 01:22:50+00	Crédito de $120.00 registrado.	2	96
179	9f14445a-2cc5-4a02-8aba-93ba489a7b5f	expense	2024-08-22 01:43:10+00	Crédito de $140.00 registrado.	2	97
180	22ba87a2-b6a8-441d-aab2-6683a569c1e4	expense	2024-08-23 01:46:30+00	Crédito de $500.00 registrado.	2	98
181	29a9c689-6e8e-42fd-98f9-2fca68a830ec	expense	2024-08-23 01:48:19+00	Crédito de $600.00 registrado.	2	99
182	298b4545-204b-4227-8ff9-02aafcc3463c	expense	2024-08-24 01:49:16+00	Crédito de $110.00 registrado.	2	100
183	11c4c6cb-40c5-4257-afd3-7e232b1e4ee5	expense	2024-08-24 01:51:31+00	Crédito de $140.00 registrado.	2	101
184	7dbc64db-6094-4974-8937-b20d951fcd81	expense	2024-09-14 22:06:56+00	Crédito de $140.00 registrado.	2	13
185	b34f5912-dbfe-485c-b6de-71bacad5315c	income	2024-09-14 22:08:29+00		9	78
186	a39b3472-003a-4f52-b94f-1fa366b48106	expense	2024-09-14 22:10:03+00	Crédito de $140.00 registrado.	2	78
187	c62e086c-a860-4b64-97fd-a971bd3a8af4	expense	2024-09-14 22:11:39+00	Crédito de $280.00 registrado.	2	102
188	b768b335-a099-4359-a679-523b1671783b	income	2024-09-14 22:16:25+00		9	88
189	6027d7de-fb07-4850-95ae-89f363d2818d	expense	2024-09-14 22:26:20+00	Crédito de $240.00 registrado.	2	88
190	b1b7d839-0952-4b8c-b3ac-b976e148d2c6	income	2024-09-14 22:27:42+00		9	69
191	486b833e-6eaa-44b9-a7d5-3c747806735e	income	2024-09-14 22:28:31+00		9	44
192	1fc68da8-d6f3-4090-822a-1a5a53a1b852	expense	2024-09-14 22:29:53+00	Crédito de $140.00 registrado.	2	103
193	e125ea1a-e1a2-4e79-8982-a70748702df9	income	2024-09-14 22:31:49+00		9	39
194	ef959bd0-9ee3-4c28-9823-9157e2c760a8	income	2024-09-14 22:32:58+00		9	10
195	45912bf0-f0e2-4146-9463-83c377a04090	income	2024-09-14 22:33:53+00		9	57
196	07cd3c52-59a3-40e6-81ae-7c54b124d0c3	income	2024-09-14 22:35:01+00		9	75
197	1c0c7324-64b7-4694-974d-f31441961a6c	expense	2024-09-14 22:56:54+00	Crédito de $600.00 registrado.	2	75
199	c474416e-7d34-4a1c-8d7e-2dceb581a7c3	expense	2024-09-14 23:03:20+00	Crédito de $250.00 registrado.	2	39
200	a57ae3cc-dd48-497e-ab61-f91e92cd2102	income	2024-09-15 23:21:00+00		9	83
201	a0a72cd7-8375-4084-bfee-b2d8766e9753	expense	2024-08-26 23:21:50+00	Crédito de $150.00 registrado.	2	104
202	4d98ce65-c0b7-4d59-9e8a-70f282fb776a	expense	2024-09-15 23:24:46+00	Crédito de $315.00 registrado.	2	105
203	7000b335-dc92-4f3c-927b-e6a90d787214	income	2024-09-15 23:29:54+00		9	104
204	8a41e4b4-ba8c-4fbd-bdbd-1ac41b44762c	income	2024-09-15 23:30:45+00		9	19
205	4bf0da32-4055-4ea3-ad97-d8302807e196	income	2024-09-15 23:31:29+00		9	72
206	023ef0b5-5fc2-4a85-9bf4-8a0554c51d7f	income	2024-09-15 23:32:16+00		9	4
207	0af31b4b-b55c-48d3-a66f-aa28e0f77ed6	income	2024-09-15 23:33:41+00		9	77
208	738b5192-bfd7-47b6-bff2-4489126847cd	expense	2024-08-15 23:40:30+00	Crédito de $500.00 registrado.	2	106
209	c2275bab-19bd-4af5-b41a-3bcece3919ce	income	2024-08-30 23:42:28+00		9	106
210	6345aa6e-51f5-4281-8f7a-1a96fbe3faea	income	2024-09-02 23:43:36+00		9	106
211	cf7f2e76-6890-496b-b0bc-84384777a757	income	2024-09-15 23:44:18+00		9	106
212	36ba0fac-105b-4c87-bf58-ffc41ba3d263	income	2024-09-15 23:48:44+00		9	62
214	f1258c9a-7701-4580-80b0-b0d2a9bf0162	income	2024-09-16 23:55:13+00		9	97
213	b3e58839-478f-41f2-8219-689e1b1e87ef	income	2024-09-16 23:53:26+00		9	54
215	304f97f4-bd12-4d4f-93f9-ffd8f9c95916	expense	2024-09-16 23:56:30+00	Crédito de $90.00 registrado.	2	107
217	5a1a456d-2a77-4400-81e2-23d7b16831a1	income	2024-09-16 23:59:29+00		9	63
218	9718ed05-b0a3-42bf-8eb8-f1fac08338b9	income	2024-09-17 00:00:23+00		9	89
219	d71c4dd7-8f75-46d6-af1e-a5af481ec405	expense	2024-09-17 00:01:49+00	Crédito de $150.00 registrado.	2	108
220	49c8c795-e7f3-4273-958f-cee5045f062c	expense	2024-09-17 00:03:18+00	Crédito de $180.00 registrado.	2	109
221	be65d89b-8fea-4df2-a2b1-767d5cbfd17d	expense	2024-09-18 00:05:42+00	Crédito de $150.00 registrado.	2	110
222	78c73cb7-721f-4c28-a7e5-bb814be8aeec	expense	2024-09-17 00:06:43+00	Crédito de $270.00 registrado.	2	97
223	06156257-22c2-4c9d-9a8a-f57eaf184a40	expense	2024-09-17 00:07:54+00	Crédito de $115.00 registrado.	2	98
224	1afb681c-f427-4d8b-a60e-86c5a2dd3948	expense	2024-09-17 00:08:48+00	Crédito de $65.00 registrado.	2	111
225	5a2b6155-062b-43ec-95b7-5f7b2b215675	income	2024-09-17 00:10:25+00		9	56
226	22024a56-d8bb-4a47-b042-e045bd84af67	income	2024-09-17 00:11:06+00		9	94
227	94ccb418-1d48-4beb-b542-21432cff0089	income	2024-09-17 00:18:51+00		9	10
228	053d046c-2314-4991-875a-f25ac349292a	income	2024-09-17 00:19:54+00		9	36
229	a85a85be-d00e-4494-9765-d83e4b47d4c3	income	2024-09-17 00:21:01+00		9	3
230	a58c099f-f423-4f31-ab17-4dce211ffb5a	income	2024-09-17 00:22:08+00		9	82
231	2fb0600f-1ffe-4deb-afae-3e88d14b7e1f	expense	2024-08-31 00:24:55+00	Crédito de $150.00 registrado.	2	112
232	b8c748a7-1533-4ad3-a2c7-4e2584c552d0	income	2024-09-17 00:26:40+00		9	112
233	150aae7c-58bc-4491-a3d9-739362fd6c3f	expense	2024-07-17 00:28:30+00	Crédito de $250.00 registrado.	2	113
234	329cd935-52ae-49a6-8cb8-2a6c2aecae04	income	2024-09-07 00:30:56+00		9	113
235	f9cbfff3-7525-4999-b54a-2e56b28ae3f4	income	2024-09-17 00:31:43+00		9	113
236	f40314f8-aea7-4a71-abbd-2a0bf702c63c	income	2024-09-17 18:56:04+00		9	65
158	c94d8802-0c35-413d-9f97-a29aea756ea3	income	2024-08-31 00:14:25+00		9	32
237	0910d25c-9921-4e78-8665-64a80b2385a0	income	2024-09-17 18:58:19+00		9	50
238	1cd123f0-6ad5-4bc2-aa41-65259be2b46c	income	2024-09-17 18:59:58+00		9	82
239	397bdcdd-c947-44da-934c-5c2072a2c23c	income	2024-09-17 19:02:11+00		9	22
240	8b70c5aa-44be-471e-945b-445b9fa0ec60	expense	2024-09-17 19:04:52+00	Crédito de $501.00 registrado.	2	114
241	91dc437e-0f47-40d0-a1c0-e1c08eff64ad	income	2024-09-17 19:09:56+00		9	36
242	bd62a8eb-9c8d-4125-8ea2-ec1a59c63ca0	expense	2024-09-17 19:11:07+00	Crédito de $200.00 registrado.	2	36
243	ef75676c-ef63-4b9a-8e8c-4223776e71c6	expense	2024-09-17 19:11:56+00	Crédito de $300.00 registrado.	2	16
244	42da29d6-3254-430e-a43b-b09677153c00	income	2024-09-17 19:13:00+00		9	93
245	2177d4e2-4ae6-4539-9d5e-1d364c19a19c	expense	2024-09-17 19:15:34+00	Crédito de $800.00 registrado.	2	93
246	0faf3403-a833-445b-a109-a73ba2a0598e	expense	2024-09-17 19:16:46+00	Crédito de $140.00 registrado.	2	115
1223	ae7b6b13-8921-4835-8819-22d70373fa7b	expense	2024-11-21 00:05:12+00	Crédito de $70.00 registrado.	2	252
248	94092513-c155-456b-99b8-d156e731cc4c	income	2024-09-17 19:20:21+00		9	9
247	afaabf59-5a81-4b46-a83f-8fc5f4491335	income	2024-09-17 19:18:09+00		9	55
1235	0a6d94e7-872e-4e82-8088-f1a4c0d4db3b	income	2024-11-22 00:57:31+00		9	240
250	1d6aa4d7-dc70-4955-ac27-0c71b524ab2d	income	2024-09-17 19:32:32+00		9	41
251	6fab5289-7a6f-43bb-9ff3-6caf3810c0ce	income	2024-09-17 19:35:59+00		9	86
252	1a0ec2a0-f262-4bb5-a46b-57206b1f1167	income	2024-09-17 19:38:47+00		9	98
253	b0710f74-0fb1-499e-b135-e93da62e830b	income	2024-09-17 19:39:51+00		9	42
254	81fb52ce-64b6-4529-b865-20dd98685c9d	income	2024-09-17 19:41:27+00		9	10
255	f058612a-a86d-42da-9d05-2a165408add7	income	2024-09-17 19:42:22+00		9	49
256	6de3bc12-d19e-4a2d-81f0-465e7a4feeb5	expense	2024-09-17 19:43:40+00	Crédito de $140.00 registrado.	2	116
257	9f605d0c-bb17-4c59-bcac-716440ae6be9	expense	2024-09-17 19:45:52+00	Crédito de $400.00 registrado.	2	29
258	ea3585a6-7b19-4d17-beda-a73ec0c97922	expense	2024-09-17 19:46:59+00	Crédito de $150.00 registrado.	2	34
259	3ca2c978-c5c8-44f0-8a1d-75b419c9068b	expense	2024-09-17 19:47:42+00	Crédito de $800.00 registrado.	2	64
260	63f7873f-d510-4128-9bbf-20e879e3524d	expense	2024-07-03 19:48:45+00	Crédito de $345.00 registrado.	2	117
261	730639df-95f1-4be4-a51d-708f8690b4b4	income	2024-09-17 19:50:10+00		9	34
262	579e4908-d0d2-40d4-8a01-841051bfdb5e	income	2024-09-17 19:50:51+00		9	3
263	c30c98bc-dc2a-4c50-84c6-5ea19ea8fbff	income	2024-07-18 19:52:22+00		9	117
264	1fdd439e-4efb-446c-afd3-201c71446e1f	income	2024-09-19 19:53:19+00		9	117
265	41bee8b1-0d4a-4c1d-8cff-dc44023fb57f	income	2024-08-16 19:53:53+00		9	117
266	e6d26f0b-2058-4038-b260-9ab774edf811	income	2024-09-16 19:54:29+00		9	117
271	f9940920-c369-491a-970c-22ec66985fc8	income	2024-05-02 23:49:10+00		10	118
270	5069aacc-13eb-4f72-a537-448baf167ac2	income	2024-04-01 23:48:26+00		10	118
269	0bc2fce4-7420-4961-a843-83f6e17ff4f0	income	2024-03-16 23:47:42+00		10	118
268	feda8475-80bc-425e-bbce-d637182eebf4	income	2023-12-18 23:46:16+00		10	118
267	02682731-cc0e-468f-b141-075fbc9ec2e1	expense	2023-12-18 23:35:30+00	Crédito de $408.00 registrado.	1	118
272	b9870c8b-6e11-49ed-a29e-ab14f556a8b9	income	2024-05-16 23:51:58+00		10	118
273	9dc916da-fc73-4ee4-b04f-39827104f35c	income	2024-06-17 23:52:50+00		10	118
274	35734f6c-2152-4eb6-b7f5-dccb393b0a3a	income	2024-07-16 23:53:39+00		10	118
275	023caa48-e799-4311-b661-0b57e2ffeda0	income	2024-08-05 23:54:23+00		10	118
276	687940f3-4e84-4206-807d-0b9110244b2d	income	2024-08-09 23:55:03+00		10	118
277	ab8687ee-bc4e-4fd2-81cc-e4cf4e798ebd	income	2024-09-02 23:55:46+00		10	118
278	e4f6056f-5f84-4aa0-81b5-03472eba86b5	income	2024-08-19 23:57:20+00		10	118
279	166569f4-0f6e-419a-87ef-e5f4ad6f54bf	income	2024-09-16 23:59:49+00		10	118
280	5de8897c-cd39-40bf-90f3-1191d177c636	expense	2024-05-02 00:51:17+00	Crédito de $360.00 registrado.	2	119
281	cb76bd65-b60a-4f0a-b572-727aa6a3e7e9	income	2024-06-19 00:52:59+00		9	119
282	1fbc0896-cac4-4268-86f6-4f405eb9de7f	income	2024-09-18 00:53:49+00		9	119
283	a1911a82-1e45-45a2-9592-2a6a96bd8ce6	expense	2024-04-11 18:28:26+00	Crédito de $300.00 registrado.	2	120
284	7c9b7c38-5fa5-422a-969f-d1ad00310b23	income	2024-07-11 18:30:46+00		9	120
285	2f2ee2b1-00d3-4c05-9299-12b722fde9ae	income	2024-07-15 18:49:48+00		9	120
286	cb27eaf5-9a0b-4290-b093-115ccc57466d	expense	2024-09-10 19:00:07+00	Crédito de $90.00 registrado.	2	27
287	386a44e7-4ac5-40cb-bfd5-19b91b922d16	expense	2024-08-19 20:10:04+00	Crédito de $1200.00 registrado.	2	121
288	66b3bc19-1b2b-4af9-b221-56ba43e238f9	income	2024-09-18 20:11:49+00		9	121
289	64d0616e-9328-46de-908f-7ca5bc177a3b	expense	2024-06-03 20:13:06+00	Crédito de $300.00 registrado.	2	122
290	b87c0e42-443e-4592-b5c0-a75262081b19	income	2024-07-18 20:22:12+00		9	122
291	0c1c3bd9-4b68-4f37-8ed1-7f507f8503a1	income	2024-08-05 20:23:27+00		9	122
292	494abc56-9cc5-4edf-af37-0bea685f4b45	income	2024-08-18 20:24:47+00		9	122
293	9a4b75e6-f78e-4d85-97e2-4751174b2af2	expense	2024-08-17 20:26:15+00	Crédito de $150.00 registrado.	2	123
294	824dd594-12fa-451d-a037-1bf302d04653	expense	2024-07-01 20:28:01+00	Crédito de $180.00 registrado.	2	124
295	e52e2f22-6cdc-436f-94de-bb7edeb11b60	income	2024-09-03 20:30:01+00		9	123
296	6841a051-cb39-414d-906a-99a69209f097	expense	2024-08-21 20:37:35+00	Crédito de $90.00 registrado.	2	27
297	54667010-6235-4ab7-80db-c29a39c97a30	income	2024-09-05 20:38:48+00		9	27
298	03296c71-1351-4ac8-937d-33527db98ffc	expense	2024-07-03 20:39:39+00	Crédito de $480.00 registrado.	2	27
299	a833786f-472d-4ecf-b0d6-b343cfc09753	income	2024-07-11 20:41:03+00		9	27
300	c16e1d30-8e4d-425f-bec6-b9ce81583e46	income	2024-08-12 20:41:44+00		9	27
301	da5d84a3-159c-4ffe-8cb9-d054cdf60bea	income	2024-09-11 20:42:34+00		9	27
302	cbd0a46d-130c-4679-9b27-5828f54bedc0	expense	2024-09-18 22:25:55+00	Crédito de $360.00 registrado.	2	106
303	50c6dd61-df4f-4876-8002-e791f514f28c	income	2024-09-18 22:28:17+00		9	1
304	c519357c-339c-4820-9fd3-504c39dcb43d	income	2024-09-18 22:29:00+00		9	92
305	6a7ddc18-615f-4e71-b92a-98558723537b	income	2024-09-18 22:29:53+00		9	121
306	00125397-e063-44c8-8de0-817e5184e4df	expense	2024-09-18 22:31:47+00	Crédito de $165.00 registrado.	2	125
307	711ff5aa-8f9c-4b8f-a1a5-55cee3a83b63	expense	2024-09-18 22:32:54+00	Crédito de $140.00 registrado.	2	126
308	9d093094-de20-4a73-b54f-274140aaf6d1	income	2024-09-18 22:36:05+00		9	23
309	2584a3ad-ba65-45af-9ac6-911009db4cb9	income	2024-09-20 22:36:47+00		9	17
310	635ff49b-e1b8-45b2-b934-9ec904e5a396	income	2024-09-20 22:38:25+00		9	37
311	4f9497c3-fdcc-493f-970f-a0988095556f	expense	2024-07-16 22:41:41+00	Crédito de $140.00 registrado.	2	127
312	1cf2a0d8-9ea8-4f0a-b539-25dd6d7996b6	income	2024-07-22 22:47:21+00		9	127
313	1460db54-a0eb-422e-a0ea-b27c4e72e6d1	income	2024-08-05 22:48:04+00		9	127
314	609f1372-2977-43c8-9942-0c75cab1ab26	income	2024-09-18 22:48:42+00		9	127
315	add5608a-2cf2-436b-b1b7-671c93629259	expense	2024-09-18 22:51:51+00	Crédito de $90.00 registrado.	2	128
317	b5b9db74-b094-4ca7-941e-59bc21512eff	income	2024-09-18 22:54:35+00		9	20
318	a0bf65be-6f9c-4265-bd3d-91868b959214	income	2024-09-18 22:55:12+00		9	10
319	0e0e5493-2ecb-4a2e-bd35-928a5d90cd29	income	2024-09-18 22:56:01+00		9	49
320	220f3082-d2eb-4b46-aabf-a873f974c447	income	2024-09-11 21:00:01+00		9	27
321	8f9b1bc2-c623-4750-b122-65b75ed48f3c	income	2024-09-20 21:01:02+00		9	27
322	076f9cb7-1784-4dab-9200-f0d2efdd9f6a	expense	2024-09-20 21:01:43+00	Crédito de $300.00 registrado.	2	27
323	d684502e-2304-4a79-a153-ca087948b48f	income	2024-09-20 21:03:10+00		10	28
324	ff0a6568-777b-4869-9c11-2a04d8432e0e	expense	2024-09-20 21:04:00+00	Crédito de $160.00 registrado.	2	28
325	23660d42-4c7b-4c8f-8dc1-bb6ba36ee84c	income	2024-09-20 21:07:43+00		2	82
326	46e14b3f-b2c9-4325-a7fe-c76f4f94b451	expense	2024-09-20 21:08:58+00	Crédito de $180.00 registrado.	2	129
327	66cc895e-a9c8-4dc8-8e9c-a28b34df9a91	income	2024-09-20 21:10:04+00		9	10
328	1b678bc1-09ae-474e-b546-667d2f941201	income	2024-09-20 21:10:46+00		9	49
329	cd2b0f36-e35d-4e87-a9e6-8d5267371370	expense	2024-09-20 21:12:08+00	Crédito de $250.00 registrado.	2	130
330	7fe73849-8a9a-42a6-8204-44397fbcf144	expense	2024-07-19 18:33:00+00	Crédito de $140.00 registrado.	2	131
331	10f4bce3-741f-4660-a3fa-801477b695dc	income	2024-08-12 18:34:56+00		9	131
332	4ba958e1-d4c6-40c5-8f9d-5518a93a7849	income	2024-09-09 18:38:36+00		9	131
333	ece97a48-a94a-411f-8114-8d629ee5ed7f	income	2024-09-22 18:39:27+00		9	131
334	36bef6fa-7d90-4a51-bc88-2f6ec4a6b0f7	income	2024-09-21 18:49:21+00		9	44
335	026d1de1-cf93-4c56-a76b-62a560e7ff78	income	2024-09-21 18:50:07+00		9	10
336	90369464-d47a-47b1-9c5f-32bdb5a5811a	income	2024-09-21 18:50:51+00		9	49
337	12d185b6-2e9b-45a3-ac81-080d817a6112	expense	2024-09-21 18:51:36+00	Crédito de $140.00 registrado.	2	82
338	d1c21fd4-5f44-4630-b62e-87836d313b03	expense	2024-09-21 18:52:13+00	Crédito de $70.00 registrado.	2	111
339	0248c203-f334-4d5b-b99d-3e397ba90c25	income	2024-09-21 18:56:27+00		9	38
340	78ce8e82-7285-472d-8b6b-59dee1216b1b	income	2024-09-21 18:57:16+00		9	103
341	1bc8ffa9-7fff-4dff-88c1-ec46bc5d671c	income	2024-09-22 19:22:35+00		9	49
342	22084911-5ebd-482f-a78c-11a3fdfabfbe	expense	2024-09-22 19:23:23+00	Crédito de $30.00 registrado.	2	132
343	67196260-0c33-458b-885a-8bafdbd344c1	expense	2024-09-22 19:24:34+00	Crédito de $160.00 registrado.	2	133
344	094639f0-fc47-4a27-9c96-bfe92ce85e42	expense	2024-09-22 19:33:16+00	Crédito de $90.00 registrado.	2	134
345	f10c29a7-4ee7-4534-b88a-d74029e6b4e5	expense	2024-07-04 00:15:11+00	Crédito de $600.00 registrado.	2	135
346	dedd9772-82f1-47d4-8c93-4859508ae142	income	2024-07-21 00:16:44+00		9	135
347	de18d7df-97df-4398-b067-3250b8bfbbb9	income	2024-07-24 00:17:38+00		9	135
348	e8fba291-3872-4ded-bcc5-ab5ddb2fe80e	income	2024-07-30 00:18:21+00		9	135
349	014f9f86-40b7-41f1-acfc-69bccaec906b	income	2024-09-22 00:19:01+00		9	135
350	2f18c44e-d14e-4242-8d28-fe351c2cd9f5	expense	2024-07-25 00:27:20+00	Crédito de $500.00 registrado.	2	136
351	9df4d569-07d8-47e8-b15a-b3c2960d325b	income	2024-07-27 00:29:03+00		9	136
352	55748a19-fad0-4dfd-a777-7db8bee0f23e	income	2024-07-30 00:29:38+00		9	136
353	ff9582fe-bef4-4b95-bc63-7dcb38506e36	income	2024-08-19 00:30:08+00		9	136
354	68af0233-2044-4bff-bebb-3cce84fa5d22	income	2024-08-25 00:30:41+00		9	136
355	c83bcb4a-61f8-4056-b1ce-34ba0a931815	income	2024-09-08 00:31:12+00		9	136
356	c7aaa9b5-b51c-48bb-baee-cba70ee68b95	income	2024-09-19 00:32:00+00		9	136
357	c21362ca-ea5a-4309-a0ba-25319195d647	income	2024-09-22 00:32:33+00		9	136
358	509d6402-856f-48a9-97e5-8f612f6699e4	expense	2024-09-23 18:23:28+00	Crédito de $132.00 registrado.	2	44
359	5537538d-dd9b-4eeb-8074-a5d2e1a9b58b	income	2024-09-23 18:27:03+00		9	67
360	9fa9104e-1df9-401c-a538-b4883f171edc	income	2024-09-23 18:30:16+00		9	1
361	b3c86aa4-cf7b-4a5e-b420-8b306dcb722d	income	2024-09-23 18:30:58+00		9	20
362	f6cecaeb-a127-4ea4-af9c-a238418af4bf	income	2024-09-23 18:32:00+00		9	71
363	98f3fdbf-6829-4301-a499-63fbdf793edd	income	2024-09-23 18:32:46+00		9	10
364	fbeba6ae-c736-49d8-bef0-50ce960bf558	income	2024-09-23 18:33:29+00		9	49
365	682dcc5f-9fda-4b61-b6be-df8c726b1005	expense	2024-09-24 18:38:23+00	Crédito de $150.00 registrado.	2	137
1236	b8d89297-1293-4585-8bd9-f2fbf19494c7	income	2024-11-22 00:58:02+00		9	139
367	44524436-33ec-4c4f-9613-cc81b2937092	expense	2024-09-24 18:59:11+00	Crédito de $500.00 registrado.	2	138
368	f167b878-f648-4c51-af75-3fb09c962359	expense	2024-09-24 19:00:11+00	Crédito de $255.00 registrado.	2	139
369	a854d641-77e9-440f-82ea-30a6884d7265	income	2024-09-24 19:02:15+00		9	3
370	6a32187e-fbbd-464d-97da-b579610924a1	income	2024-09-24 19:02:48+00		9	10
371	998740f3-c0db-4cd1-8831-e7735b8a1a32	income	2024-09-24 19:03:17+00		9	49
372	cc7c9ba4-d3ce-4b09-bba7-cf876b1d3b2a	income	2024-09-24 19:03:56+00		9	15
373	8452745a-e221-4a5d-a74b-b41d011bb9fb	expense	2024-09-24 19:07:18+00	Crédito de $375.00 registrado.	2	15
374	ed3cfb04-5e4a-47df-902c-c16655c5c791	expense	2024-08-29 19:00:18+00	Crédito de $450.00 registrado.	2	140
375	fe37bf11-3d14-4aa0-ae77-6456a3fdfc3c	income	2024-09-12 19:01:44+00		9	140
376	7fb0ec1e-957a-4bbb-bc6f-946883b8f09b	income	2024-09-26 19:10:15+00		9	140
377	8ec3ede7-19e3-41a6-bd44-a0c63c4852bd	income	2024-09-26 22:26:33+00		10	27
378	f789a5cc-8b5c-4b02-a963-e72196af3911	expense	2024-09-26 22:29:47+00	Crédito de $70.00 registrado.	2	84
380	a8ae0616-22b4-48a7-b90a-44da3297c4d1	expense	2024-09-26 22:31:29+00	Crédito de $90.00 registrado.	9	27
381	f68da646-f13a-4ccc-af75-aa7f820b51b9	income	2024-09-26 22:32:24+00		9	48
382	f62711d9-eb79-4390-99ee-b7bde2e15355	income	2024-09-26 22:39:23+00		9	10
383	d785c39a-a267-440f-895d-9eb3d148d5c0	income	2024-09-26 22:40:03+00		9	49
384	b672344e-6143-4432-bb13-e97cb3b7eb36	income	2024-09-26 22:40:28+00		9	34
385	10d60f10-716c-487d-b807-d31b3365bbd8	expense	2024-07-28 23:20:20+00	Crédito de $140.00 registrado.	2	141
386	255caebb-0011-4216-b11f-40737dec1529	income	2024-08-12 23:26:41+00		9	141
387	32491599-38fa-4ef0-ac3e-db9ecce0a9eb	income	2024-09-26 23:27:14+00		9	141
388	cf985811-c93c-4717-9e16-1d449b364ff7	expense	2024-09-26 23:37:37+00	Crédito de $250.00 registrado.	2	142
389	72afd4ad-2b99-42bc-ab4c-765e0b240bae	expense	2024-09-26 23:39:09+00	Crédito de $90.00 registrado.	2	143
390	f5db602b-d22b-4269-8e86-23a6aed39f68	expense	2024-09-26 23:41:55+00	Crédito de $130.00 registrado.	2	144
391	31005fc6-ad49-4313-84a7-7dc11f3c2241	income	2024-09-25 23:50:30+00		9	74
392	b0379790-17e6-4f2c-b827-34f48b8ee7c3	income	2024-09-25 23:51:19+00		9	87
393	9fad53e4-d1d6-4a72-ba12-b1fe904bc912	expense	2024-07-25 23:53:21+00	Crédito de $300.00 registrado.	2	145
395	6180b68a-3ed0-44d5-aa48-f2f8a219fe08	income	2024-08-29 00:03:19+00		9	145
394	e00a2499-b339-4562-a032-34250c55b5ee	income	2024-08-11 00:02:31+00		9	145
396	a0821769-8514-4188-9dce-a3c0c52f5322	income	2024-09-26 00:04:27+00		9	145
397	2d432b47-c8c9-46b1-a21a-2eb9acfab462	expense	2024-09-26 00:05:11+00	Crédito de $140.00 registrado.	2	87
399	0c3d0051-2815-4a10-9104-4a8ee40ca02e	expense	2024-09-26 00:08:32+00	Crédito de $160.00 registrado.	2	145
400	fcb83987-ad5c-45eb-86a2-2ab97b8ca668	expense	2024-09-26 00:10:07+00	Crédito de $150.00 registrado.	2	146
401	ce5dcf38-078b-4d20-9fd1-d4e1eb86885c	expense	2024-09-26 00:41:22+00	Crédito de $300.00 registrado.	2	67
402	de80534e-d124-427f-a41c-9436f76dc999	income	2024-09-26 00:45:49+00		9	37
403	65114329-e1ad-4eb9-bee9-4ae00abec963	income	2024-09-26 00:46:45+00		9	72
404	cd40d149-6d5b-46d3-b810-574dac55b4c1	income	2024-09-26 00:47:22+00		9	10
405	7f174fb3-625e-4281-8f17-295de5f14b36	income	2024-09-26 00:48:09+00		9	49
406	306c2ae6-5efe-4afc-906a-c38ac7910231	expense	2024-09-26 01:11:06+00	Crédito de $1100.00 registrado.	2	6
407	0d482fc0-59c7-4737-9ee9-f45a1cd13f9c	expense	2024-09-26 01:11:39+00	Crédito de $150.00 registrado.	2	112
408	b6b7d723-aa28-485c-9fdf-9383a7c05337	expense	2024-09-28 02:09:36+00	Crédito de $140.00 registrado.	2	147
409	e67a3b22-cad9-4581-bc0b-9471462127eb	expense	2024-09-28 02:10:49+00	Crédito de $50.00 registrado.	2	148
410	7a19ede6-baa7-4dde-8c60-80c0198e92f2	income	2024-09-28 02:11:59+00		9	10
411	443c3b75-8199-448a-8b1b-89958bb9c74f	income	2024-09-28 02:13:36+00	Camiseta	10	24
413	a189ec4b-72bb-4fd1-9d33-28f9c4465b41	income	2024-09-28 02:15:01+00		9	3
414	32b568ab-eae5-452c-a5c1-42b3608bc6ad	income	2024-09-28 02:15:53+00		9	59
415	2cb577f3-3586-4795-bc18-dda76e9d4152	income	2024-09-29 02:17:05+00		9	136
416	2d1388d8-cd86-474b-a3bd-a56fa0df9f42	income	2024-09-29 02:19:05+00		9	127
417	d50925c0-703b-4bf4-8500-d6f8d383920a	expense	2024-09-29 02:22:18+00	Crédito de $140.00 registrado.	2	92
1237	21654491-6609-4110-9757-07afd0b7f607	income	2024-11-22 00:58:56+00		9	44
419	a39a0417-03b6-42ce-80b1-33a6d8963f71	expense	2024-09-29 02:24:26+00	Crédito de $150.00 registrado.	2	15
420	7df10c0a-dc06-4c4d-86ba-f4c0e79a668e	expense	2024-09-29 02:25:15+00	Crédito de $60.00 registrado.	2	149
421	a12b5fe8-1e3d-4105-b12c-af258ffb0c33	income	2024-09-30 02:27:24+00		9	130
422	f7ee8d6f-cf52-4f8e-9631-9af578373b04	income	2024-09-30 02:28:00+00		9	49
423	7d7a3f65-370e-4925-84fc-418d210b72de	income	2024-09-30 02:28:46+00		9	73
424	3a7fbd58-f366-48c3-a40b-2074415e97bf	income	2024-09-30 02:29:17+00		9	16
425	5fd24871-246b-4a56-86c7-5c8ca34c91c6	income	2024-10-01 02:32:02+00		9	44
426	0643958e-19be-4d33-a754-0f16d14f7e9a	income	2024-10-01 02:32:57+00		9	3
427	90cfec9e-6c90-4ab3-a75b-9b1a4adebe08	expense	2024-10-01 02:33:51+00	Crédito de $150.00 registrado.	2	150
428	490cc369-1e91-4016-b699-d7cdbec1d2cf	income	2024-10-01 02:36:59+00		9	54
429	19b99f97-7982-4e41-9aa9-803e0e996ba6	income	2024-10-01 02:38:16+00		9	7
430	436391a3-5dfd-4c24-9c9c-91b24b53bab5	expense	2024-10-01 02:39:20+00	Crédito de $280.00 registrado.	2	54
431	82ea38ce-9f6b-4dce-bccb-7b9a558b2def	income	2024-10-01 02:40:16+00		9	64
432	d7e5c949-b2db-4b22-8b9d-822746e3e087	income	2024-10-01 02:41:37+00		9	4
433	7aea1c37-c0fd-455e-ad87-a849e8cc7c2a	income	2024-10-01 02:42:09+00		11	116
434	f964df2a-c1a4-4720-8c07-28f93fade319	income	2024-10-01 02:43:06+00		10	75
435	0c45ff18-366d-4e9c-b6be-d7b86a19f7ef	income	2024-10-01 02:44:11+00		9	77
436	f86cbfe6-ee10-497a-8a4a-3226d9505aa4	income	2024-10-01 02:45:00+00		9	129
437	c609e04f-6b0e-4c0d-ab73-80d6a25c1b67	income	2024-10-01 02:45:53+00		9	110
438	988fe660-4d44-4ee7-aa00-33f10b8acfa1	income	2024-10-01 02:46:39+00		9	43
439	233d89b1-3b6f-48c6-99e2-e620f68a52db	income	2024-10-01 02:47:44+00		9	10
440	663c82f0-c965-44a8-abba-ed9a789f22da	income	2024-10-01 02:48:19+00		9	49
441	d823c529-02ac-463c-9198-61590fe59b17	income	2024-10-01 02:48:54+00		9	109
442	f5c375bf-b99d-4fed-b2f0-a96933fd7e0f	expense	2024-10-01 02:49:49+00	Crédito de $360.00 registrado.	2	43
443	96c92f5a-97a8-47d8-876d-3da65a67bdbe	expense	2024-10-01 02:52:10+00	Crédito de $150.00 registrado.	2	151
444	e17e4e82-1f0b-4482-8520-eaf2ab157349	income	2024-10-01 02:53:23+00		9	81
445	837b1321-59a5-4e83-9c78-09aee088e046	income	2024-10-01 02:53:58+00		9	66
446	5b1acc01-c1b7-44b1-b225-c124ba5225a8	income	2024-10-01 02:54:38+00		9	78
447	540d0c97-c42f-408f-999e-7da23ce81137	income	2024-10-01 02:55:32+00		9	108
448	7de5c625-29ce-4293-ac88-4f0d36c560af	expense	2024-08-31 02:59:03+00	Crédito de $115.00 registrado.	10	152
449	e0cc23ca-4e6a-44bf-844b-178075dde8c5	expense	2024-10-01 03:00:38+00	Crédito de $360.00 registrado.	2	23
450	d747241d-004b-44a0-a224-b547ac87f94d	expense	2024-10-01 03:01:41+00	Crédito de $150.00 registrado.	2	123
451	96658083-f298-4574-b7dd-0b6f97527240	expense	2024-10-01 03:02:24+00	Crédito de $140.00 registrado.	2	153
452	d10e9e76-0f13-4d28-bce0-40792c94d867	expense	2024-10-01 03:03:30+00	Crédito de $140.00 registrado.	2	154
453	8a84015c-9b13-4319-9589-c508283f062f	income	2024-10-01 03:04:52+00		9	83
454	7ff584d0-0b83-4661-9696-7daa57fdfd52	expense	2024-08-26 03:06:24+00	Crédito de $300.00 registrado.	2	155
455	27367add-a160-456c-9397-2dd062d77af7	income	2024-10-01 03:07:39+00		9	155
456	b0707067-719f-4edb-bba0-80e067260a80	income	2024-10-01 22:58:30+00		9	73
457	f0e12cb8-6ffe-428b-90cd-b7c4c544a624	income	2024-10-01 23:03:19+00		9	126
458	2c3c8dff-f6a4-4f31-bd35-3de5e1a2ad2e	income	2024-10-01 23:06:04+00		9	63
459	0808fe17-3ba9-455e-8cb7-eabcc8cdfdcb	expense	2024-10-01 23:10:11+00	Crédito de $501.00 registrado.	2	19
460	b1c96334-0675-4c50-8512-c4c7a74bc635	expense	2024-10-01 23:11:03+00	Crédito de $120.00 registrado.	2	156
461	046c1347-ceb6-441d-b99c-efaecd533f8b	expense	2024-10-01 23:12:46+00	Crédito de $150.00 registrado.	2	157
462	8615aa45-e541-4e7c-9938-f5c217d97eea	expense	2024-10-01 23:14:19+00	Crédito de $250.00 registrado.	2	116
463	9cef4643-b8d9-4c13-90b7-31ffeda657e4	expense	2024-10-01 23:18:59+00	Crédito de $165.00 registrado.	2	158
464	62635843-fbc0-4dc3-b4e8-997a8311b201	expense	2024-10-01 23:20:22+00	Crédito de $80.00 registrado.	2	42
465	9bb67276-59e9-43b7-b94c-475ea828ce8b	expense	2024-10-01 23:21:27+00	Crédito de $140.00 registrado.	2	159
466	919f0014-1f2d-4fae-8878-f147745323f1	income	2024-10-01 23:31:19+00		9	135
467	952dde0a-1666-4d47-8011-63b8da958679	income	2024-10-01 23:35:08+00		9	2
468	303cc98c-d092-4106-bb78-130b5084500a	income	2024-10-01 23:42:10+00		9	5
469	85c1daa8-c926-42a4-9562-e421b0014da6	income	2024-10-01 23:43:25+00		9	10
470	27e74384-d2ce-46a9-b8dd-8e8710a17d40	income	2024-10-01 23:45:02+00		9	57
471	16e1fb00-2dcf-4718-9597-f3d0ea91450b	income	2024-10-01 23:49:07+00		9	56
472	79a246d7-f412-4560-9c49-2a822c758afa	income	2024-10-01 23:52:08+00		9	42
473	60b15b84-d47b-4dd5-91a8-9d9f11e8c858	income	2024-10-01 23:54:50+00		9	89
474	6bd6438b-dc3c-408e-bce5-6b8b6f5a8582	income	2024-10-01 23:59:06+00		9	82
475	ad117af1-352a-485c-8b8a-57201ffd79da	income	2024-10-02 00:01:21+00		9	49
476	95359733-fb09-474e-b215-b14e425e957b	income	2024-10-02 00:03:09+00		9	106
477	9912f401-0d55-45de-b799-1affc73b2e35	income	2024-10-02 00:06:12+00		9	1
478	3abf654f-d691-4d54-a322-164443085105	expense	2024-10-02 00:17:48+00	Crédito de $270.00 registrado.	2	7
479	41319876-3584-4e7e-8743-9f993a8898b5	income	2024-10-02 00:20:45+00		9	58
480	5bba28b9-c4ce-4d4b-b40c-4d675b924449	income	2024-10-02 00:22:37+00		9	71
481	4566e247-b685-4aac-ab60-368ace2fd10c	income	2024-10-02 00:26:54+00		9	72
482	cb1f970f-7d14-49e1-8827-7f74a81b9d28	income	2024-10-02 00:35:39+00		9	88
483	cd34d21e-fd58-4849-873d-2d36b860ceff	income	2024-10-02 00:38:01+00		9	17
484	d6a691c3-ef45-4bb1-a785-4abbc1a96c3d	income	2024-10-02 00:39:17+00		9	37
485	dcb8e1e3-bb99-413c-8d9c-a9d4a79110e7	income	2024-10-02 21:29:22+00		9	111
486	47604ec1-f44a-4719-88e1-e68f90c03e38	income	2024-10-03 21:31:35+00		9	3
487	04d72e01-77c7-4439-b857-57966b6b938e	income	2024-10-02 21:33:05+00		9	10
488	30be43da-abb0-4d60-959b-2e5a8ca0f837	income	2024-10-03 21:35:01+00		9	20
489	1a2a829c-34a5-4680-b29a-bab14777b3df	income	2024-10-02 21:36:54+00		9	49
490	ddbcdcb7-49fc-4e58-a5bf-c0e9977bad09	income	2024-10-02 21:38:35+00		9	41
491	4281c825-4b1c-44b6-934f-0152ab41ee4b	income	2024-10-02 21:43:47+00		9	125
492	d6d3ceb3-91e4-4b37-be87-221ecb2e4c63	income	2024-10-02 21:48:24+00		9	86
493	b4927819-158f-45d1-b314-09b7cca111b3	income	2024-10-03 21:50:36+00		9	136
494	8f0feb95-7a19-4152-a275-974cc6456970	income	2024-10-02 21:53:15+00		9	103
495	9a31f6b0-be0d-4ac8-9439-99b5d0cade19	expense	2024-10-02 22:05:15+00	Crédito de $270.00 registrado.	2	41
496	09011647-7b1e-4c76-8afc-ec12b67cd8ab	expense	2024-10-02 22:06:25+00	Crédito de $165.00 registrado.	2	86
497	3dc7ac21-161d-4623-944d-a3f645388c09	income	2024-10-02 22:15:39+00		9	33
498	d0dabe5b-dfed-4d35-b79f-20733c0df5f3	income	2024-10-02 22:16:51+00		9	55
499	9812a5c9-f153-43bb-b0db-2ce5e0e01607	income	2024-10-02 22:21:25+00		9	82
500	eb0a0d12-11ba-4989-9737-955d93da5fd7	expense	2024-08-24 22:34:30+00	Crédito de $400.00 registrado.	2	160
501	242be8ec-00be-453d-81c9-c0f0f4a772d5	income	2024-09-16 22:35:44+00		9	160
502	d957c28a-dbaf-45d3-9795-205f8a5464c7	income	2024-10-02 22:37:02+00		9	160
503	92a5d9be-ba34-418d-b069-db1f57ac8f08	income	2024-10-02 22:39:37+00		9	23
504	decfd24a-ba6e-41f7-a671-939cf374cecc	income	2024-10-03 23:00:41+00		9	137
505	b5aabd0f-5984-41f9-8c55-7d0d4fdba838	income	2024-10-03 23:03:46+00		9	47
506	bdde4125-7a38-4d17-aef1-6e184d0cf44d	expense	2024-10-03 23:06:04+00	Crédito de $330.00 registrado.	2	65
507	23e497e0-03ed-4db3-b281-63fc04115683	expense	2024-10-03 23:07:10+00	Crédito de $150.00 registrado.	2	82
508	9ee9ec9c-5336-4dbb-a460-4495dd45518a	expense	2024-10-03 23:08:26+00	Crédito de $80.00 registrado.	2	133
509	0b108ecc-000e-4b9c-adf7-8faad496e406	income	2024-10-03 23:10:51+00		9	133
510	dc8e2a32-1d57-4fa9-8656-4ea298cad773	income	2024-10-03 23:14:24+00		9	54
511	e0465338-0b97-4486-9ba4-0f9213d33bd0	income	2024-10-03 23:16:04+00		9	85
512	aed89e47-4266-4375-8890-3c547294f484	expense	2024-10-03 23:22:16+00	Crédito de $150.00 registrado.	2	161
513	bf41ec06-f1c0-4cee-86d5-60d5e11579c2	expense	2024-10-03 23:23:54+00	Crédito de $80.00 registrado.	2	162
514	758b9475-401a-45bd-9e61-1fcf6814913d	expense	2024-10-03 23:25:39+00	Crédito de $255.00 registrado.	2	163
515	aa154c74-d143-44ac-8133-6d9402ad12f5	expense	2024-10-04 15:53:31+00	Crédito de $540.00 registrado.	2	71
516	6028ce50-39f0-40c3-aaef-f0edda030bf8	income	2024-10-04 15:54:58+00		9	13
518	8cfefebb-96cb-4b10-a93e-db0ee4bde8b7	income	2024-10-04 15:58:35+00		9	97
517	78ea345a-d360-4973-92d7-24142e2ad3cd	income	2024-10-04 15:56:44+00		9	49
519	a38dbaa9-dde9-4f0e-ba62-4a30cf52aa30	expense	2024-10-04 16:08:39+00	Crédito de $90.00 registrado.	2	84
520	a1293a26-f78a-4b54-8f94-be3e4072fb43	expense	2024-10-04 16:10:45+00	Crédito de $130.00 registrado.	2	164
521	2e8d510b-f0a0-47ba-ba36-937739bd697b	expense	2024-07-05 16:24:39+00	Crédito de $270.00 registrado.	2	165
522	be3d9c36-3407-4866-bb16-6dbdd2b92b39	income	2024-08-04 16:26:39+00		2	165
523	705c526a-f6a6-42f6-8243-9af5d40df011	income	2024-10-04 16:27:33+00		9	165
524	3d49a323-f1d6-4286-9b4a-388c48da9815	income	2024-10-04 16:28:18+00		9	27
525	d86794ab-68b0-410d-b146-4a227f10dd8f	income	2024-10-04 16:32:14+00		9	139
526	b9f0f429-faa4-481d-8173-c5dbc30fe2d6	income	2024-10-06 00:00:58+00		9	144
527	0bf81268-8f0c-48c2-908b-89befff012a7	income	2024-10-06 00:01:38+00		9	136
528	3cb58f4a-3622-4a3c-81d6-76b1c10bdf36	expense	2024-10-06 00:03:30+00	Crédito de $90.00 registrado.	2	21
529	600dff67-2da0-4f02-b2e9-c7de8de3e0bd	expense	2024-10-06 00:04:04+00	Crédito de $150.00 registrado.	2	166
530	713e186e-d054-4b47-b1a3-73c74c4b68b4	expense	2024-10-06 00:05:15+00	Crédito de $140.00 registrado.	2	167
531	2b1b5f90-2cb0-484f-b632-d3ae905506e5	expense	2024-10-06 00:06:45+00	Crédito de $90.00 registrado.	2	42
532	5ce9716b-c891-42ea-a7e6-7397ca04659f	expense	2024-10-06 00:07:14+00	Crédito de $150.00 registrado.	2	168
1225	f1dbcadb-1e74-43d9-b521-90241926661d	expense	2024-11-21 00:06:10+00	Crédito de $70.00 registrado.	2	18
534	0c35ee80-6a71-4f4d-a8ed-ac98c561a1da	expense	2024-10-07 00:11:51+00	Crédito de $150.00 registrado.	2	170
535	4cf3fd6e-f458-4d7e-a63a-2ec2406c5742	income	2024-10-07 00:13:22+00		9	49
536	93eaa8e5-51c0-422d-83d7-8f45858794c2	expense	2024-10-06 00:15:15+00	Crédito de $150.00 registrado.	2	171
1238	49926ae5-3f1c-4748-aad9-680450e0afa7	income	2024-11-22 01:07:10+00		9	176
539	e3eef56a-8524-4ece-9945-8df86513392a	expense	2024-10-06 00:17:58+00	Crédito de $80.00 registrado.	2	88
540	9201c231-fff5-4981-ad78-cb2094a2edba	income	2024-10-06 00:18:39+00		9	103
542	8e6c6855-a044-4d63-9385-e0a6828cee1f	income	2024-10-06 00:20:03+00		9	49
543	180864bb-1c1f-43de-83c1-58d19b39c872	income	2024-10-06 00:20:30+00		9	69
544	9d6fd5d6-e874-4c1d-8642-2ac1ae1b25cd	income	2024-10-06 00:21:21+00		9	146
545	cc6cb93b-46ed-4da4-b037-ad89f6f79931	income	2024-10-08 00:27:31+00		9	82
546	afdd9a4a-4a31-40ba-9591-5b92bb696cbe	expense	2024-09-03 00:31:14+00	Crédito de $220.00 registrado.	\N	172
547	1b46896c-8ab6-4eca-894e-77844356e1ac	income	2024-10-08 00:34:04+00		9	172
548	151829a4-4299-4bad-8477-13222fe427af	expense	2024-10-08 00:35:34+00	Crédito de $150.00 registrado.	2	104
549	5016b9e3-c4da-417f-bdfc-e61ddea93a3c	income	2024-10-08 00:36:25+00		9	20
550	7d79018d-c6f7-422a-87c1-bbefd2b36cbe	expense	2024-10-08 00:38:14+00	Crédito de $50.00 registrado.	2	98
551	bf0f1d97-8bd6-4ba8-b3a9-7c2bf3a58cd2	expense	2024-10-08 00:38:51+00	Crédito de $1200.00 registrado.	2	20
552	23d28ef2-3018-4bcf-b6e3-1f2ce09a4356	expense	2024-10-08 00:39:28+00	Crédito de $50.00 registrado.	2	77
553	265247a9-4453-4f2a-b936-74aae00f63d9	expense	2024-10-08 00:42:05+00	Crédito de $150.00 registrado.	2	173
554	49252f0f-e6e2-408d-9554-3c773e44ec75	income	2024-10-08 00:43:45+00		9	10
555	735c7fd4-412e-47e3-9fe6-117795716f24	income	2024-10-08 00:44:23+00		9	49
556	fc9daebf-e3bb-43af-9457-0a288b4f5b4d	expense	2024-07-27 00:47:54+00	Crédito de $140.00 registrado.	2	174
557	07603a09-bbdd-4054-a0f5-c693cbd72db3	income	2024-10-08 00:49:33+00		9	174
558	851146be-c124-4144-9596-501b45bbb922	expense	2024-10-09 00:50:53+00	Crédito de $90.00 registrado.	2	144
559	86b4ee84-88e2-4e02-a4f4-ae01ce06d1fa	expense	2024-10-09 00:51:36+00	Crédito de $160.00 registrado.	2	47
560	07036879-ea34-4942-acb8-ac81c1fd5e19	expense	2024-10-09 00:52:18+00	Crédito de $90.00 registrado.	2	175
561	cd97a433-736d-417e-b5eb-be92dd5d86d2	income	2024-10-09 00:53:40+00		9	72
562	2fa8f49a-7e11-4866-aa62-0be030da8b54	income	2024-10-09 00:54:14+00		9	10
563	6bb0cc43-d4c5-4bf8-9741-130bc3552389	income	2024-10-09 00:55:36+00		9	49
564	eaa41a93-7f07-48c3-ba54-0b7d76bca5e3	expense	2024-08-14 01:00:03+00	Crédito de $700.00 registrado.	2	176
565	e0f45e88-de76-4f71-95ae-f62c0a564b34	income	2024-09-17 01:03:09+00		9	176
566	7d09c44c-b375-4cf8-a051-d6885dda0e8f	income	2024-09-22 01:03:43+00		9	176
567	d56fe766-dfd3-4209-842b-874460500054	income	2024-10-03 01:04:19+00		9	176
568	31641732-fef8-4550-8119-b278ec90e909	income	2024-10-09 01:04:47+00		9	176
569	3f4abd2b-a2f4-4dc7-82f0-0aea0e78acfb	income	2024-10-10 01:07:33+00		9	136
570	a4462c58-b83d-4769-8af4-2b15ca644753	income	2024-10-10 01:08:45+00		9	49
571	177c6568-7e50-4cc0-903c-7940d1a51daf	income	2024-10-10 22:30:39+00		9	74
572	f30b9145-6733-4aa4-9c5c-04af4c943942	income	2024-10-10 22:32:40+00		9	21
573	1c8509a9-a71b-4fee-911f-6a9a17d7ed9c	income	2024-10-10 22:34:12+00		9	87
1226	8e1d3c45-6971-4a16-a0f4-323099e05e6f	expense	2024-11-21 00:13:25+00	Crédito de $150.00 registrado.	2	253
575	791bfd43-89dd-489e-9865-b0011c62925e	income	2024-10-10 22:36:11+00		9	119
576	6d9b2e79-3e84-415a-a935-8ffad3de0756	expense	2024-10-10 22:40:29+00	Crédito de $600.00 registrado.	2	119
1239	0eda7c0a-029d-452d-bcc8-3f244acb3e81	income	2024-11-22 01:10:33+00		9	1
579	074446a2-d1df-4aa5-b231-c0d35e0baf68	expense	2024-10-10 22:41:56+00	Crédito de $150.00 registrado.	2	2
583	9192dbb2-e008-40c3-9af7-a87f4c04b51c	expense	2024-10-10 22:42:57+00	Crédito de $150.00 registrado.	2	87
584	88375e52-e13d-45b6-87bf-a516dfbc04ec	income	2024-10-10 22:43:22+00		9	37
585	2368c319-6296-4b05-96b4-3b490adc2436	income	2024-10-10 22:43:56+00		9	49
586	a00c02c0-498f-42c9-b3f1-6e67957628d0	income	2024-10-11 22:45:48+00		9	38
587	f8eff83b-949d-4c03-afca-eed403a695bb	income	2024-10-11 22:46:44+00		9	27
588	e7226bd6-3c78-4c6f-92b1-17c4e9367868	income	2024-10-11 22:49:10+00		9	31
589	a57644a5-0c28-469b-a7da-9c91c0789fc3	income	2024-10-11 22:49:48+00		9	172
590	adbd11ff-abf3-4734-9298-3db1614e06bf	income	2024-10-11 22:50:37+00		9	34
591	2201d075-8cf9-4ae0-a134-4fe89ff85f11	expense	2024-10-11 22:52:56+00	Crédito de $150.00 registrado.	2	27
593	65c8cd76-cba4-448e-9c53-3e1fc6bae0e8	expense	2024-10-11 22:53:22+00	Crédito de $260.00 registrado.	2	172
594	8d6d3a62-985e-4596-949f-c1753e3de291	expense	2024-10-11 22:54:26+00	Crédito de $130.00 registrado.	2	177
595	645419af-27f8-4e51-af25-9f3492aad55b	income	2024-10-12 23:00:09+00		9	154
596	24a7d17e-7478-496f-8615-4a778cd97487	expense	2024-10-12 23:03:47+00	Crédito de $330.00 registrado.	2	38
597	0d14ebb4-c3bd-4fac-9d53-1d5129af45b2	expense	2024-10-12 23:05:39+00	Crédito de $3600.00 registrado.	2	20
598	071a053d-d88a-47bf-998d-4d093967a8d7	income	2024-10-12 23:06:33+00		9	103
600	0ef8184a-4368-4744-bda0-37227df6e3cb	income	2024-10-12 23:08:09+00		9	49
601	d0f83367-ad48-4c75-a9e6-7c14746b1d5b	income	2024-10-13 23:11:14+00		9	49
602	a7ab5330-46a4-4d60-994d-81263af09b7e	income	2024-10-13 23:11:43+00		9	73
603	783a219f-b931-4943-b1b7-914c46992e6c	income	2024-10-14 23:12:44+00		9	1
605	b90f845b-0b43-42ec-8d0c-0f67fbfd1ae9	income	2024-10-14 23:16:02+00		9	18
606	ef7318e0-7443-4be7-9c48-9a370e9819ba	income	2024-10-14 23:16:42+00		9	152
607	f3a090c8-dcaf-4319-9cbc-d09afcfc3dec	income	2024-10-14 23:17:18+00		9	59
608	a111e662-cb5a-4016-bfc7-0830df938852	income	2024-10-14 23:17:49+00		9	170
609	4f0a79bf-1df2-4119-9a9c-372cc79d0c03	expense	2024-10-14 23:20:16+00	Crédito de $180.00 registrado.	2	74
610	2179b23c-dae8-43af-b85c-c4f5ef0c8802	expense	2024-10-14 23:20:44+00	Crédito de $90.00 registrado.	2	178
611	0cb7b1f1-fa60-4b0f-964e-f102ad2edd9d	income	2024-10-14 23:22:00+00		9	6
612	8245f34a-b610-4b67-a389-89cdbd867bb0	income	2024-10-14 23:23:26+00		9	5
613	28538551-31c9-4650-a40d-b711a32576bd	income	2024-10-14 23:24:08+00		10	29
614	f66989ef-3c47-45cd-93fb-920b7b5bdff9	income	2024-10-19 23:25:11+00		9	136
412	16cc8e50-8bc5-4522-8047-716296739bd6	income	2024-10-15 02:14:29+00		9	61
615	511f5270-90cd-423c-a202-d27685388c5d	expense	2024-10-14 23:29:44+00	Crédito de $140.00 registrado.	2	61
617	7a335c8a-bba3-487d-8c2f-c02359490dc1	expense	2024-10-14 23:31:28+00	Crédito de $80.00 registrado.	2	180
618	7f560202-2095-4a49-b4cc-3eb1c1084fd2	income	2024-10-14 23:32:36+00		9	138
619	5a6b5f0b-05f3-4cd5-b8b9-596b957372fb	income	2024-10-14 23:33:10+00		9	49
620	e7920f07-11b7-4416-8080-7c0af629d186	income	2024-10-14 23:33:37+00		9	20
621	cc659f09-258f-456d-880f-c0732a4d6390	income	2024-10-14 23:35:01+00		9	99
622	e01c3250-2660-49d3-8fa4-5fe53f439e3a	expense	2024-07-04 01:13:48+00	Crédito de $150.00 registrado.	2	181
623	9f3f1ac8-1367-482b-9bc6-acfa1cb316af	expense	2024-08-31 01:15:33+00	Crédito de $360.00 registrado.	2	182
624	b5f92b0b-ca27-4826-b835-1b7e5273abc3	expense	2024-09-18 01:17:15+00	Crédito de $140.00 registrado.	2	183
625	df264f7a-47b0-4e92-98ef-5e62f3d9bcb1	income	2024-09-01 01:18:40+00		9	181
626	16797463-bf83-4109-8214-8242734a1235	income	2024-10-03 01:19:27+00		9	181
627	790dee66-3638-4c78-a844-9fff948cc12c	income	2024-10-02 01:20:09+00		9	182
628	f351c5db-adbb-41a6-9344-cbad7a6d6f7e	income	2024-10-04 01:20:43+00		9	115
629	73a49576-16b5-4678-8fc3-9c8be2b5a588	expense	2024-10-03 21:47:18+00	Crédito de $150.00 registrado.	2	54
630	7de92956-4c50-4f70-a6b2-d05705f9eb4a	expense	2024-09-17 23:10:54+00	Crédito de $200.00 registrado.	2	187
631	139f9ea3-192e-4bd1-848a-505e86fa330e	expense	2024-09-14 23:15:46+00	Crédito de $280.00 registrado.	2	99
632	33b5b44a-0388-4405-98e3-e383d86cfe79	expense	2024-09-16 23:17:10+00	Crédito de $90.00 registrado.	2	107
633	95a97397-eefc-4563-9b63-fa09fe658b82	expense	2024-09-09 23:40:22+00	Crédito de $30.00 registrado.	2	188
634	b6da06fb-e667-4357-bcb9-b1f4647ae1f7	income	2024-10-16 01:38:00+00		9	104
635	51a1a85f-5fc5-46b2-afc8-412bcfe58d45	income	2024-10-16 01:38:26+00		9	92
636	c7ac7b5a-6ac3-4b7e-81cd-e23d368d75f4	income	2024-10-16 01:39:07+00		9	4
637	7f2819e7-4bed-4404-b46b-5ad962b01d55	income	2024-10-16 01:39:38+00		9	54
638	a39cb94d-e317-48a8-9f59-3b084baf975b	income	2024-10-16 01:40:56+00		9	16
639	931490a3-3608-419c-8090-36df2a6f0240	income	2024-10-16 01:47:27+00		9	144
640	fa03aadb-a92e-44d8-adbe-f9104c7b2c46	income	2024-10-16 01:47:52+00		9	167
641	06f039e2-a391-4c24-a277-0716541cf4ed	income	2024-10-16 01:48:24+00		9	116
642	6e328c7b-b44d-49e0-9f7a-c27dbf2f5687	income	2024-10-16 01:49:03+00		9	155
643	1f6f23ed-3afb-4e6c-b5e8-b04a1a252ffd	income	2024-10-16 01:50:01+00		9	129
644	f2772ab0-8ea6-461b-8ab2-304b5cbb31ce	income	2024-10-16 01:51:31+00		9	114
645	17b5ff1f-ace8-4c9f-8b2a-c5b0475265a9	income	2024-10-16 01:52:44+00		9	78
646	64900e0d-899b-433b-82b6-9ab575ba4c2f	income	2024-10-16 01:53:41+00		9	162
647	996ed009-c126-44f9-88cb-fb2815d55872	income	2024-10-16 01:54:20+00		9	72
648	a03a2bec-48d2-46da-9188-4a9ea3d06caa	income	2024-10-16 01:55:14+00		9	37
649	3fda937d-bdbe-43ac-a515-d0851fa9344d	income	2024-10-16 01:57:13+00		9	186
650	82de8352-75f3-4741-9783-4221271dea41	income	2024-10-16 01:58:07+00		9	158
604	e5cb5700-cb5c-4dd6-bcc8-6c10d0dbddca	income	2024-10-14 23:14:56+00		9	51
651	abb7f9e5-fdc6-4111-8ae0-29f3a2464085	income	2024-10-16 01:58:56+00		9	49
652	c0d75988-1618-489a-ae3e-30604ade4cdb	income	2024-10-16 01:59:19+00		9	110
653	495f62a9-138d-4714-80af-95efa337fe68	income	2024-10-16 01:59:55+00		9	2
655	ab1d5426-d949-4f78-9e06-0dae01a8f635	income	2024-10-16 18:21:13+00		9	55
656	0d4762b1-c72d-427d-b38a-1be1a41a81f3	expense	2024-10-16 18:24:37+00	Crédito de $280.00 registrado.	2	99
1227	84a67b69-67cd-4244-94dd-712bd1e4813e	income	2024-11-21 00:14:47+00		9	176
658	c814522a-32d0-4348-977a-4dbf123cb103	expense	2024-10-16 18:25:10+00	Crédito de $300.00 registrado.	2	155
659	c6f0d7a2-7f14-43c3-889a-e9d33ac981c2	income	2024-10-16 18:27:21+00		9	63
660	cb49f4e4-bac5-4dd6-b5f4-5ca2ba246ecc	income	2024-10-16 18:35:24+00		9	125
661	916c9112-dca7-40e6-a344-6e4c45ae2acd	income	2024-08-17 18:43:43+00		9	12
662	6d313c21-590a-4177-928c-a8d14466d3f8	income	2024-09-16 18:44:17+00		9	12
30	9ecc79d7-6ab3-4703-9d11-9d3ef1a989be	income	2024-08-31 23:59:59+00		9	12
1240	7628cd8a-f998-4bb0-bf5f-630d53c1492e	expense	2024-11-22 01:13:26+00	Crédito de $60.00 registrado.	2	256
664	7ada813e-eb6a-4c17-a0dc-4f839a6b31ec	expense	2024-10-16 18:46:47+00	Crédito de $160.00 registrado.	2	190
665	f89f98e0-1623-4321-ad72-d9130ca6e34a	expense	2024-10-16 18:48:21+00	Crédito de $150.00 registrado.	2	191
666	b963b552-1392-4ed5-829a-8493693f1fa5	expense	2024-08-31 19:01:19+00	Crédito de $300.00 registrado.	2	192
667	2be9c45c-6626-41f0-b50f-410853d9c70b	income	2024-09-14 19:02:18+00		9	192
668	dd9c18fe-74a4-40b0-ab9c-768fbc1b06ce	income	2024-10-16 19:11:54+00		9	192
669	fd68c115-03ee-4b8e-a2ab-705e28ba970c	income	2024-10-16 19:13:38+00		9	106
670	6cdf34db-0379-401b-9218-5ec9d80406f5	income	2024-10-16 19:14:41+00		9	113
671	dbf2a3dc-11eb-4be1-9cfd-67b7eabcd3de	income	2024-10-16 19:15:13+00		9	85
672	f018548f-64b9-4681-9542-4f4cee31facc	income	2024-10-16 19:16:10+00		9	112
673	21374988-de24-4b98-951a-8ea5b42ae1b5	income	2024-10-16 19:17:01+00		9	156
674	2a655ad5-9be9-46ef-8707-4cf8fc8c6e37	income	2024-10-16 19:17:37+00		9	168
675	900fd989-bb8b-46c2-a58e-51fc7c8478e2	expense	2024-10-16 19:19:54+00	Crédito de $140.00 registrado.	2	55
676	6c025f58-6b8f-41c9-b8ba-2e6dd7e97e42	expense	2024-10-16 19:20:43+00	Crédito de $525.00 registrado.	2	5
677	09a528ad-376e-4adb-9744-f67c99978983	expense	2024-10-16 19:21:28+00	Crédito de $315.00 registrado.	2	193
678	e642d570-917c-414d-99ae-b6071f771385	expense	2024-10-16 19:23:41+00	Crédito de $270.00 registrado.	2	63
679	aafaf90d-7e89-4f94-8e3d-62e8333bb3f8	expense	2024-10-16 19:25:58+00	Crédito de $330.00 registrado.	2	192
680	074a109e-53ac-4c92-98b3-c857c6de8839	expense	2024-10-16 19:27:24+00	Crédito de $180.00 registrado.	2	129
681	be418b8c-87ff-4620-a2b3-ef62e2161c4b	income	2024-10-16 19:35:06+00		9	81
682	687e933a-e069-4cf5-aca7-dd3162571bbc	income	2024-10-16 19:37:11+00		9	77
683	62158dad-46a8-49b5-a096-45c9f8b6f719	income	2024-10-16 19:37:52+00		9	77
684	778decff-f58e-420d-b136-117247fa2a8a	expense	2024-10-16 19:39:04+00	Crédito de $80.00 registrado.	2	77
685	13d4f99d-d519-48c6-8eba-fc56b61a7ed3	income	2024-10-16 19:39:50+00		9	108
686	a1126218-b51c-4634-9d38-7b3aecf32e58	income	2024-10-16 19:43:37+00		9	186
687	6385068f-7a1a-48ed-b84a-9b35351cfe7d	income	2024-10-16 19:44:15+00		9	82
688	1c4aa0b0-f9a1-4e0b-8389-59a31c30337a	income	2024-10-16 19:44:48+00		9	59
689	894fa199-1cdb-4d3f-8d27-c1370ee64bd3	income	2024-10-16 19:45:31+00		9	30
690	2a0b58f9-2b15-4df9-9083-bcc27778c6db	income	2024-10-16 19:46:29+00		9	88
692	8d7a8d4f-199d-44aa-bf2a-35c153ec5f44	expense	2024-10-16 19:49:14+00	Crédito de $130.00 registrado.	2	194
693	119c4a26-59c0-4b88-b6e6-5b02736f532e	income	2024-10-16 19:50:51+00		9	57
694	d7bafe54-c9d8-4874-b630-c25b38610c85	expense	2024-10-16 19:51:42+00	Crédito de $510.00 registrado.	2	57
695	8bd8c874-9e63-453e-8ac1-c7893061d975	expense	2024-10-16 19:52:29+00	Crédito de $150.00 registrado.	2	195
696	d39b14c4-67ed-464d-a1db-df9b2ca12369	income	2024-10-16 19:53:49+00		9	49
697	4c01aee9-05c4-422b-a0ba-2b51681b69eb	income	2024-10-16 19:54:15+00		9	11
698	5d40450f-171b-457a-82c8-73e63c9bf4ee	expense	2024-10-17 21:07:20+00	Crédito de $540.00 registrado.	2	85
700	6cb73482-14e7-4d22-a893-a2f4f8be17d5	income	2024-10-17 21:16:33+00		9	150
701	aabb5bb5-5053-4478-bf99-c02301c07801	income	2024-10-17 21:17:05+00		9	41
702	dc3fe64c-e54d-4fd8-8087-0aa294aac698	income	2024-10-17 21:17:34+00		9	34
703	8a5c1eb6-b926-4938-a780-be370f49d30c	expense	2024-10-17 21:24:31+00	Crédito de $400.00 registrado.	2	34
705	909fde52-a942-43cb-9461-9aeae9e5ac28	expense	2024-10-17 21:25:15+00	Crédito de $300.00 registrado.	2	64
706	77ba9586-a2f7-41fa-b5c6-0378d2e5c4ab	income	2024-10-17 21:30:09+00		9	164
707	f1c7445f-7691-4167-8656-463412b5d6b5	expense	2024-10-17 21:46:55+00	Crédito de $600.00 registrado.	2	196
708	c658de9f-d211-4680-827b-bf7ed086e387	expense	2024-10-17 21:57:34+00	Crédito de $550.00 registrado.	2	197
709	f56c2b23-99bb-4ea2-bb49-5d2bd12467ce	expense	2024-10-17 21:58:46+00	Crédito de $880.00 registrado.	2	93
710	d7ae3e8b-6834-48dd-9b21-36d1e1b54b59	expense	2024-10-17 21:59:13+00	Crédito de $150.00 registrado.	2	113
713	28be85a2-2434-4ae8-88f9-460ab9b44748	expense	2024-10-17 22:00:33+00	Crédito de $150.00 registrado.	2	82
714	65bb28d3-d519-49a9-a819-0f30b31421d9	income	2024-10-17 22:01:52+00		9	186
715	e0065e2c-60c8-443f-a66a-b3e449c97504	income	2024-10-17 22:02:38+00		9	49
716	f50515db-5d20-40fb-ba9e-f2b4f50655b5	income	2024-10-17 22:02:56+00		9	149
717	03359413-4149-40e6-973a-f595426385d2	income	2024-10-18 22:10:42+00		9	42
718	05569aa0-64c0-4622-8446-ef5a9259dfd3	income	2024-10-17 22:12:14+00		9	182
719	b3666f77-8e01-44c1-89ed-e90a7a654fae	income	2024-10-17 22:13:17+00		9	61
720	8f466474-f778-4b46-a99f-2c360f05c713	expense	2024-10-18 22:31:38+00	Crédito de $900.00 registrado.	2	61
721	93fd6152-e87c-44b7-b939-e0beea0c57f0	income	2024-10-24 22:35:08+00		9	62
722	b858e64e-9b61-46c0-8662-f6dfeb006fa9	income	2024-10-18 22:36:01+00		9	186
723	348a6dcc-97bd-4bd5-a4db-aafa47b5bc5a	income	2024-10-18 22:36:37+00		9	43
724	63908dc6-41dd-415e-b86a-732eebf8d221	income	2024-10-18 22:37:21+00		9	184
725	ec3cd3b8-df97-4036-b8b3-3150dacb6a67	income	2024-10-19 22:45:18+00		9	183
726	012239ee-7328-4913-abd3-105a06bc7314	income	2024-10-19 22:45:59+00		9	90
727	61c4dc42-453f-4c69-b9a4-2233123ae4af	income	2024-10-19 22:46:57+00		9	37
728	25e10e99-b6ce-4881-a5c9-cefd561aacc0	expense	2024-07-16 22:48:44+00	Crédito de $70.00 registrado.	2	198
729	afb2cb0d-8b46-4f35-9a44-d5ddd95e98aa	income	2024-07-18 22:53:31+00		9	198
730	f6f8d401-6200-4039-a541-e5cee4080218	income	2024-07-22 22:54:06+00		9	198
731	3ba9efe5-17da-45f9-b032-065f1b603e0d	income	2024-07-24 22:54:37+00		9	198
732	6143d744-fef1-4efc-be13-caa88c1d57d1	income	2024-07-26 22:55:21+00		9	198
733	7a034e48-e747-4989-824f-f3fdae56be26	income	2024-08-31 22:56:06+00		9	198
734	b4a5b869-6dbb-4ff7-8dcf-8f0ea4197443	income	2024-10-19 22:57:05+00		9	86
654	629b4319-6b92-4d64-992f-466e764bea72	income	2024-10-30 18:20:12+00		9	189
691	89f58c21-e5c4-4528-8f5e-d022b56039be	expense	2024-10-16 19:48:17+00	Crédito de $150.00 registrado.	2	88
735	5a6f74df-d36c-417f-b829-0be4fef007c0	income	2024-10-19 22:59:01+00		9	135
736	0d5e78f0-f308-4edc-92dc-bf59e75b7a2c	income	2024-10-19 22:59:33+00		9	176
737	227db834-1e7e-4321-9aa8-4c75adb33a52	income	2024-10-19 23:00:03+00		9	136
738	7ca772a9-4b77-4dea-a7f7-d49a381930c2	income	2024-10-19 23:01:04+00		9	146
739	407bf340-5ea3-4496-8fab-7fce1334b1ca	expense	2024-10-19 23:06:27+00	Crédito de $140.00 registrado.	2	131
740	b13e0843-ead7-48ac-b61b-979d3c7934d4	expense	2024-10-19 23:07:20+00	Crédito de $140.00 registrado.	2	199
741	0b5e677d-0ed1-4b51-85cf-69c8c8061241	income	2024-10-19 23:08:52+00		9	49
742	62417c89-b7b5-48eb-babe-2d2b78b69216	expense	2024-10-20 23:11:55+00	Crédito de $140.00 registrado.	2	183
1228	469f8460-d844-4618-a41f-2f4c1fab4e16	expense	2024-11-21 00:22:26+00	Crédito de $400.00 registrado.	2	43
1241	8e148c70-c3ca-454e-b3d1-993da08fbe71	expense	2024-11-22 01:14:34+00	Crédito de $120.00 registrado.	2	257
745	a375f4dc-178c-4025-a850-866f89f0f75d	expense	2024-10-20 23:12:23+00	Crédito de $150.00 registrado.	2	30
746	eb3a89b5-bde1-4a13-b37d-02587f82cd6a	income	2024-10-20 23:13:32+00		9	1
747	e155d1bf-f7a3-443e-887f-a167726ab67c	income	2024-10-20 23:14:15+00		9	49
748	7769028f-799c-4e7e-8f32-1626c23b4ed1	expense	2024-10-20 23:15:47+00	Crédito de $150.00 registrado.	2	200
749	99fd6ad6-fe47-4f31-a623-8e1b0b35a13a	income	2024-10-21 23:21:53+00		9	33
750	f2ab4895-2623-4db9-afa9-ce765224463e	income	2024-10-21 23:22:18+00		9	119
751	f3357aee-36e2-46ba-a370-589a1bf0d68f	income	2024-10-21 23:22:59+00		9	71
752	876a37ce-6a19-4ad6-b76f-116163f23015	income	2024-10-21 23:23:35+00		9	121
753	0219691e-230a-481a-a3cf-4344195fbd36	expense	2024-10-21 23:25:07+00	Crédito de $150.00 registrado.	2	201
754	e55d1c7c-b40b-451d-ab54-307c6c6a7eb1	expense	2024-10-21 23:26:08+00	Crédito de $50.00 registrado.	2	202
755	d8782dc3-90a8-4ec2-a743-5db58b120499	expense	2024-10-21 23:27:26+00	Crédito de $150.00 registrado.	2	203
756	092ad126-d1d4-478f-9444-648483c09d54	income	2024-10-21 23:28:46+00		9	13
757	e523c44a-5a1f-40e3-b5e4-2f6a36e32f6a	income	2024-10-21 23:29:18+00		9	49
758	2be4f732-5838-484b-a926-d5efed1d7d37	expense	2024-07-15 00:10:33+00	Crédito de $200.00 registrado.	2	204
759	f6e0dcba-4894-47e3-bfa0-280b99d50c6c	income	2024-07-28 00:12:33+00		9	204
760	516dbec3-e157-438d-8c1d-0e98d1721f17	income	2024-08-31 00:13:13+00		9	204
761	79a9f3ab-ad94-4e90-a74f-8034334755fc	income	2024-09-28 00:13:52+00		9	204
762	08e40072-c416-4a53-be66-ee013caa4a72	expense	2024-07-16 00:16:19+00	Crédito de $90.00 registrado.	2	205
763	0ee01b93-8b24-4222-ba26-6f3539225fcb	income	2024-07-27 00:18:36+00		9	205
764	de6b83e1-d9be-4d81-a340-515b0aa74896	expense	2024-07-27 00:19:31+00	Crédito de $140.00 registrado.	9	205
765	8cd66519-a727-47b5-9339-9bb8d61798f3	income	2024-09-12 00:20:42+00		9	205
766	f7d98dc6-ea1f-43d2-9adb-a09621c053d5	expense	2024-07-24 18:37:58+00	Crédito de $165.00 registrado.	2	206
767	bfcf8d7a-83fa-4b51-add6-7a1b4b7741d0	income	2024-08-17 18:39:34+00		9	206
768	efdd076f-53fc-4edd-a340-9ff6d71ae00b	income	2024-08-30 18:40:02+00		9	206
769	bd786d7e-5f85-417f-900c-8b6b5cdd09d2	income	2024-09-14 18:40:30+00		9	206
770	28d0e53b-7df1-4479-9718-d052e3f2d652	expense	2024-10-21 18:53:01+00	Crédito de $90.00 registrado.	2	207
771	13c0d048-a335-4f6e-be48-b1fbe1648a7b	expense	2024-10-21 23:16:10+00	Crédito de $250.00 registrado.	2	208
772	f980b2b9-4c1d-43f2-9889-8173df6cb3ca	expense	2024-10-22 23:20:25+00	Crédito de $150.00 registrado.	2	209
773	afc80ab5-0b36-40c1-87c4-80bfed95d9e1	expense	2024-10-22 23:23:35+00	Crédito de $280.00 registrado.	2	210
774	05a8fee0-04fc-4755-9e2a-8e8165e44695	expense	2024-10-22 23:31:14+00	Crédito de $150.00 registrado.	2	211
775	a32bd5d8-4925-478a-ab24-edb61532be60	expense	2024-10-22 23:34:41+00	Crédito de $150.00 registrado.	2	212
776	682c222b-f2b0-4579-beca-f1238ed60003	income	2024-10-22 23:38:36+00		9	67
777	7adb0f31-8e56-4d3c-a0bf-18e3e4f6e41d	income	2024-10-22 23:39:03+00		9	49
778	b0ef5697-482d-4619-80de-02f6cc3a9115	income	2024-10-22 23:39:30+00		9	186
779	d191cd7c-53f8-44e6-9be0-d469cb5f32a2	expense	2024-10-23 23:45:47+00	Crédito de $230.00 registrado.	2	213
1247	e2773811-0aaf-47de-91ca-a0aa03240430	expense	2024-11-22 01:19:01+00	Crédito de $120.00 registrado.	2	245
781	be8a4268-a53c-4110-b89b-2c7a8a61c34b	expense	2024-10-23 23:48:03+00	Crédito de $50.00 registrado.	2	54
782	0eac4442-3ce2-4c09-9159-57de4aa0768b	expense	2024-10-22 23:48:07+00	Crédito de $100.00 registrado.	2	214
783	619b9d16-03c6-4560-ad5e-22f1a11a7e6d	income	2024-10-23 23:53:12+00		9	186
784	6858d295-43b6-4e41-bf28-09e0bcb16400	income	2024-10-23 23:53:39+00		9	49
785	f63d30ea-444e-48c0-842d-ac2def53cb18	income	2024-10-23 23:54:07+00		9	92
786	b2e95e7e-8c38-4a03-ac7d-02724d47e070	income	2024-10-23 23:54:39+00		9	38
787	c3d0d768-2c6b-47fc-992c-f59f2f3f2ef7	income	2024-10-23 23:55:17+00		9	37
788	80979e36-c994-4df1-973e-160ed65157de	income	2024-10-24 23:55:54+00		9	176
789	97b87921-f651-40d1-b871-3bdcf581383f	expense	2024-10-24 23:59:17+00	Crédito de $90.00 registrado.	2	215
790	e69015ce-1731-4e37-805a-f2dbe5a482f0	income	2024-10-25 00:05:25+00		9	126
791	c0a6aa00-9d68-46b6-b6da-86312282c2ba	income	2024-10-16 00:12:29+00		9	126
792	bf8e4f1c-716a-4cda-bb36-bf6a1bea5ef6	expense	2024-10-25 00:13:41+00	Crédito de $140.00 registrado.	2	126
793	5c355114-a05e-4bfa-acae-6b796788e52f	expense	2024-10-25 00:14:39+00	Crédito de $150.00 registrado.	2	112
794	cac52482-e645-46ac-bad5-dbdb411750c0	income	2024-10-25 00:16:45+00		9	186
795	562088ff-c8d4-4da3-b1df-9741c1b65705	income	2024-10-25 00:17:25+00		9	49
796	38d1ba8a-60c5-4e13-ac9d-e30d0649fbd1	expense	2024-10-26 00:29:50+00	Crédito de $216.00 registrado.	2	74
797	0fbaa7f2-46d1-4f5e-ab34-803ca36b1277	expense	2024-10-26 00:30:39+00	Crédito de $160.00 registrado.	2	216
798	1560e094-94b8-4403-a43a-fc86945e6b40	expense	2024-10-26 00:32:40+00	Crédito de $140.00 registrado.	2	217
799	8b482032-d996-428e-a56f-ccb7acb53d59	income	2024-10-26 00:34:48+00		9	21
800	f7794c70-1c59-46e6-95f5-96f98f9d0989	income	2024-10-26 00:35:31+00		9	186
801	5b04ef1f-83b7-424e-8822-edd435ae8014	income	2024-10-26 00:36:08+00		9	49
802	bd481b89-81b7-40e0-a381-24db3fdc70a2	expense	2024-10-27 01:01:47+00	Crédito de $70.00 registrado.	2	218
803	2b6aa11a-8035-43c5-8e95-abd906de0a04	expense	2024-10-27 01:03:09+00	Crédito de $100.00 registrado.	2	219
1252	ebf5abe9-bfc9-43b0-bc7b-fe8b4b758802	income	2024-11-23 01:21:18+00		9	49
805	bc84b463-c76b-4d00-8bca-825072e334b1	expense	2024-10-27 01:09:02+00	Crédito de $140.00 registrado.	2	21
806	6c00bc5c-4d0a-4f76-8883-ac33a19d4464	expense	2024-10-27 01:09:04+00	Crédito de $300.00 registrado.	2	220
807	e26dc9ad-6f3b-408c-8910-22086ff7be2b	expense	2024-10-27 01:10:08+00	Crédito de $500.00 registrado.	2	33
808	da9d95f0-fb37-4494-a6c5-198c6aa999a6	income	2024-10-27 01:11:49+00		9	38
809	076671fc-a1fd-4209-a3a0-f7c39c8d996c	income	2024-10-27 01:12:13+00		9	186
810	b7b4ab61-4975-4e23-9119-1d772e472339	income	2024-10-27 01:12:39+00		9	49
811	f4843dcb-1dd8-4a3d-8fa5-3a3f81d7b1c1	income	2024-10-27 01:13:21+00		9	147
812	902352f6-e6c7-4896-8109-369f1f36ebf9	income	2024-10-27 01:14:05+00		9	73
1257	c2d7cb0d-c893-48ab-bb12-ff45d5b5b866	income	2024-11-23 21:29:53+00		9	38
813	ffa47e10-752d-44dc-a164-099126890905	income	2024-10-27 01:15:10+00		9	136
814	476e4ea7-92d6-4595-af0a-3ee390f359c9	income	2024-10-27 21:31:16+00		9	49
815	585f8760-7150-44d3-9285-ee5cb26193ae	income	2024-10-28 21:31:50+00		9	218
816	785f3622-b327-4601-8ceb-81e72a44a72c	income	2024-10-28 21:32:27+00		9	213
817	0a6ca455-6434-4f4f-a137-7e082ac412c5	income	2024-10-28 21:32:52+00		9	178
818	6b74f318-15c5-4792-8ac6-67afb3e15a43	income	2024-10-28 21:34:30+00		9	157
819	18ebdd13-411e-426c-b7ee-2c88a793125f	expense	2024-10-28 21:44:16+00	Crédito de $150.00 registrado.	2	157
820	5cf354aa-2b79-415a-8d05-0fa43a509b45	income	2024-10-28 21:45:43+00		9	61
821	236d0cf7-e621-400d-98c3-5f8bfdd72a7a	expense	2024-10-28 21:47:37+00	Crédito de $130.00 registrado.	2	84
822	d03c4680-1a8f-4796-b84c-9cbe3fa992b6	income	2024-10-28 21:48:40+00		9	76
823	17d36fcd-2be0-4173-ad63-d6e0c5d66f89	income	2024-10-28 21:49:24+00		9	13
824	bb3a669e-dc5b-49f3-a693-4add93d3e73d	income	2024-10-28 21:50:14+00		9	211
825	089051a4-fef5-4ab0-8c0d-737c6f4c2d67	income	2024-10-28 21:51:11+00		9	20
826	67a43eb6-c634-4390-868c-0ab9412eb906	income	2024-10-28 21:51:39+00		9	49
827	a052e31d-135a-4c2f-801b-490e497e0430	income	2024-10-28 21:52:07+00		9	72
828	ee63dc4a-0d8b-4673-8229-92cdd0483a7a	income	2024-10-29 22:00:45+00		9	125
829	33a2d674-4b65-415c-8ea6-f17181027dee	income	2024-10-29 22:01:22+00		9	34
831	229df037-eda4-46e1-9c2a-19a7d893ea74	income	2024-10-29 22:03:20+00		9	6
832	788f142b-b531-4a6b-b022-3fa76aa462c7	income	2024-10-29 22:03:58+00		9	49
833	7378e3a9-b9c3-459b-818d-8d30a2386e0d	income	2024-10-29 22:04:27+00		9	186
834	33d0412d-2746-4c52-a2d1-dcd063f15f87	income	2024-10-29 22:05:14+00		9	127
835	99cd5834-f10c-40f5-b0d1-434c63bed06f	income	2024-10-29 22:06:02+00		9	136
836	8840d97b-fade-4fc9-ac4f-821801336cc2	income	2024-10-29 22:06:41+00		9	204
837	d8f695ad-0607-4158-8aac-2af50ccc06e4	expense	2024-10-29 22:07:26+00	Crédito de $360.00 registrado.	2	221
838	67b890a6-326c-41ec-9aff-73dd9807437e	expense	2024-10-30 22:12:53+00	Crédito de $80.00 registrado.	2	42
839	ebe27828-286f-42e4-a370-243f87109fa9	income	2024-10-30 22:29:19+00		9	195
840	b185d18d-deaa-43dd-b00a-9b5fdc113e2c	income	2024-10-30 22:29:54+00		9	209
841	f5dc56c1-fa89-43b9-b363-ac2a94b6a80c	income	2024-10-30 22:30:31+00		9	16
169	1a89aede-acc7-444d-b2ee-2d1119a09f0c	income	2024-09-08 00:49:11+00		9	90
216	a931a374-de89-4065-a260-5b76436558cc	income	2024-09-16 23:58:23+00		9	90
842	d51590fd-71e9-4f2d-9f71-e065ecb6a243	expense	2024-10-31 00:22:42+00	Crédito de $150.00 registrado.	2	110
843	e8d239b9-87fa-46bc-854b-2f62e861effb	income	2024-10-31 00:23:36+00		9	15
844	c5cf4275-924c-4e52-a03a-bb0316191ca7	income	2024-10-31 00:24:23+00		9	183
845	3b1713a1-7b2f-463d-a8f9-8d676a69a2c7	income	2024-10-31 00:31:09+00		9	156
846	d16d84ac-6a45-4b67-a58e-b8b8f8afc3f2	income	2024-10-31 00:31:40+00		9	49
847	5103fe8d-089e-40d8-9ce9-c90a7c6b51ab	income	2024-09-14 00:42:33+00		9	64
848	1d72a1d1-39fa-41ae-952b-3ceaf76efcd6	income	2024-10-16 00:44:12+00		9	64
849	c9373728-31dd-41ff-99d9-f725e180d408	income	2024-10-31 00:45:51+00		9	64
850	c05335fb-9de4-4292-8399-5755a720a5f0	expense	2024-10-31 00:46:37+00	Crédito de $800.00 registrado.	2	64
851	281da25f-59ed-46d2-a3ef-f4d0ac890ea0	income	2024-10-29 00:48:29+00		9	177
852	15aa977e-7d7a-4846-a27d-6a4df0dde4cd	income	2024-10-16 00:55:51+00		9	75
853	2b48ce48-ba72-4898-851c-1f1878e85d77	income	2024-10-29 00:57:39+00		9	75
854	c952e397-8c6c-4e0e-9c29-51d87ab6d649	income	2024-10-17 21:39:39+00		9	153
855	f159f339-8680-412e-b545-66d484358253	expense	2024-10-18 21:40:33+00	Crédito de $150.00 registrado.	2	222
856	ee8aa576-89ab-4b31-8a00-b8067d27731d	expense	2024-03-02 21:42:21+00	Crédito de $250.00 registrado.	2	223
857	83332949-6c38-4e9e-a87f-5189cf4738b2	income	2024-07-13 21:53:22+00		9	223
858	7399c0d6-65eb-41a4-b838-61a732659434	expense	2024-07-31 21:58:00+00	Crédito de $90.00 registrado.	2	224
859	11a9730b-684c-4164-8d85-a287028c627c	expense	2024-04-30 22:00:10+00	Crédito de $810.00 registrado.	2	225
860	76a98426-2c72-4f53-94ed-76193a08fc51	income	2024-05-16 22:06:22+00		9	225
861	1b3bcdd5-8db0-4f9f-9500-3fe29216a96e	income	2024-08-15 22:06:57+00		9	225
862	8093f7dc-7217-4ce8-a11f-84856695747a	income	2024-09-29 22:18:07+00		9	94
863	afcd82d6-947c-469d-af67-f62faf0ed55d	expense	2024-09-29 22:19:36+00	Crédito de $1025.00 registrado.	2	94
864	67d10fdf-088b-45b1-afd2-f7d3e8781ee1	expense	2024-08-01 01:35:31+00	Crédito de $330.00 registrado.	2	226
865	164e0b48-285f-45ec-8731-f219ec731203	income	2024-10-30 22:48:06+00		9	111
866	fc399e1f-ce25-458e-bda6-51cce1276f5f	expense	2024-10-30 22:52:46+00	Crédito de $150.00 registrado.	2	78
1229	891ef75e-91e8-468e-8dea-bd95082b6bcf	expense	2024-11-21 00:23:31+00	Crédito de $150.00 registrado.	2	254
868	ba269c94-57b1-4461-85bb-534534f0bb6e	expense	2024-10-30 22:54:17+00	Crédito de $25.00 registrado.	2	111
869	7ae1b2e7-d63e-4f7c-8c67-426c6316cfc1	expense	2024-07-26 23:00:01+00	Crédito de $70.00 registrado.	2	227
871	b57bf572-dd3d-4fb0-9b15-3d0d57c23970	income	2024-10-30 23:02:19+00		9	186
872	d6b67253-e30c-4b53-b9c6-685f3a2919db	income	2024-10-30 23:03:02+00		9	72
873	bd7d003c-9c0e-434e-8b08-e347bb4a7b8a	income	2024-10-30 23:03:46+00		9	167
874	f6d1fedc-be28-4283-85a0-04cb5546a00f	income	2024-10-30 23:04:19+00		9	192
875	a13587b2-4f3a-4ad1-9ef6-9cc9a3b3fcaf	income	2024-10-31 23:09:20+00		9	199
876	fbdf4ecd-c9cd-4ccb-9be8-8ae569847bb8	expense	2024-10-31 23:10:35+00	Crédito de $840.00 registrado.	2	75
877	70d41913-3da2-4b43-a52c-fde5ea4006fa	income	2024-11-08 23:15:18+00		9	163
878	229a5388-08b7-460e-9095-151640f35753	income	2024-10-31 23:19:21+00		9	49
879	a4b14787-0afe-41f3-8ab7-597de2de8421	income	2024-10-31 23:20:00+00		9	183
880	233f6c24-96a4-4371-a7b4-d7832f74b45a	income	2024-10-31 23:33:05+00		9	30
881	426be3f3-22c0-4166-af7c-f193cdac2886	income	2024-10-31 23:33:50+00		9	133
882	8425d795-00e0-4757-9bd4-d928643985e0	income	2024-10-31 23:34:27+00		11	168
883	d69acd67-e46e-4f35-b075-1347f73a253d	income	2024-10-31 23:35:57+00		9	194
884	7267bf4e-1b83-46b5-8181-5f1c117fe30b	income	2024-10-31 23:36:33+00		9	144
885	6c2c470d-402f-4aa7-8b15-faea7d5364d7	income	2024-10-31 23:37:04+00		9	153
886	a47366ac-afb4-4da2-b051-616e6a28d2ee	income	2024-10-31 23:38:27+00		9	55
887	117ce39a-a087-4e68-9985-df776b03ea8a	income	2024-10-31 23:40:48+00		9	104
888	bbe38601-6e3d-4633-b108-e74371a932ac	income	2024-10-31 23:41:28+00		9	158
889	7e7e7ccb-acc3-4410-b3c1-ca1b4a59eee1	income	2024-10-31 23:42:14+00		9	1
890	fb5c8ae3-0d4c-430f-94be-8f63d6c56ca0	income	2024-10-31 23:58:43+00		9	97
891	30fb8768-ef87-49f7-9b36-207cddad7f80	expense	2024-11-01 00:00:24+00	Crédito de $360.00 registrado.	2	228
892	ee9cfc6f-237a-42e6-814b-3154b114df4f	income	2024-11-01 00:04:23+00		9	216
893	f409955b-e13e-46fc-844d-5ccd7766811c	income	2024-11-01 00:04:54+00		9	155
894	8a11b074-14b3-40b4-9690-4276bce977ec	income	2024-11-01 00:06:49+00		9	108
830	90dd874f-3b99-4ae6-98e5-3625267d0b20	income	2024-10-29 22:02:38+00		9	179
895	12e792fc-55b2-4102-a331-8904a6b41da1	income	2024-11-01 00:08:05+00		9	49
896	eb3b3a6c-3630-47ae-af61-d784c4b3be87	income	2024-11-01 00:11:34+00		9	171
897	8dc3613e-0156-4fe8-81df-2acc85c2e899	income	2024-11-01 00:12:05+00		9	88
898	23d9c6e8-66d4-4df0-9d4f-0ea8ac1702cf	income	2024-11-02 00:22:27+00		9	63
899	4516524b-4bb4-4168-b63e-cc2733db90e8	income	2024-11-02 00:23:20+00		9	194
900	3548fbde-6848-48a5-bdb1-f3276ad9bfc6	income	2024-11-02 00:24:20+00		9	181
901	0db5a34a-f8a2-4715-b1a1-3617c07c305c	income	2024-11-02 00:25:02+00		9	154
902	46b066f4-7291-45ac-94b0-e9b2b6383591	income	2024-11-02 00:25:37+00		9	89
903	9ee7b294-4ca3-444c-a53d-26ce695db066	income	2024-11-02 00:27:35+00		9	129
904	cd967312-1c90-457c-ad64-9af8baffc7e7	income	2024-11-02 00:28:08+00		9	106
905	5b882670-ab1e-4a7f-98d7-af5dbc9aa427	expense	2024-11-02 00:29:52+00	Crédito de $300.00 registrado.	2	50
906	d46525a6-cc46-4ce2-bf46-2ccec6219b6a	income	2024-11-02 00:30:35+00		9	186
907	ed7d41f2-5754-488d-b309-305b7e462525	income	2024-11-02 00:31:30+00		9	131
908	8eb52be4-2c5a-46b7-b311-06441adeae4c	income	2024-11-09 00:32:17+00		9	43
909	d32e2112-f3b9-45a2-ac08-8ea846965e6e	income	2024-11-02 00:45:55+00		9	66
910	2a35e2c8-d77b-4573-b347-004ca8340a05	income	2024-11-02 00:46:23+00		9	138
911	688578ce-73f1-4edd-be3b-6d6636d520f7	income	2024-11-02 00:46:51+00		9	44
912	8b88b6a2-a297-405c-8d92-60553e92c5c1	income	2024-11-02 00:47:23+00		9	5
913	8c00cdd9-ec00-4a3e-9826-503e05a0db02	income	2024-08-24 00:57:50+00		9	226
914	5ddbbb25-6467-4fc0-bf93-1d143eceea42	income	2024-09-01 00:58:53+00		9	226
915	fab139e1-6aef-4a56-9fd9-ff3bacadfaa9	income	2024-11-02 00:59:24+00		9	226
916	2509d680-34fd-43cb-aec4-af4e88629969	expense	2024-11-02 01:00:08+00	Crédito de $360.00 registrado.	2	226
917	92d9689f-64ad-47c9-885d-2547c8c98f2b	income	2024-11-02 01:00:55+00		9	19
1230	6faec512-e4cc-4176-b41f-13a130a3c946	expense	2024-11-21 00:25:26+00	Crédito de $150.00 registrado.	2	255
919	8a7fac9d-0392-4fc4-bb00-cb73c0d9c37c	income	2024-11-02 01:08:48+00		9	27
920	7e31d8d3-15f8-40bd-b598-7cd846475e7e	expense	2024-11-02 01:11:33+00	Crédito de $130.00 registrado.	2	164
1242	f769414b-7897-456f-a1c7-897ea706dd29	expense	2024-11-23 01:16:58+00	Crédito de $80.00 registrado.	2	59
1248	7a48b4e5-5475-4dd6-9569-b40a5e9b66b8	income	2024-11-23 01:19:20+00		9	136
922	e4215c04-0054-46b6-8234-102c4409df48	expense	2024-11-02 01:21:08+00	Crédito de $150.00 registrado.	2	108
923	41c8926b-1de3-49c6-bfba-db1cce7794a8	expense	2024-11-02 01:21:37+00	Crédito de $150.00 registrado.	2	82
1253	5bed01f7-171f-4df0-875d-3eeb8e6c064e	income	2024-11-23 01:22:23+00		9	240
925	480c1d9e-8905-4b33-a395-27c3f1ce7162	expense	2024-11-02 01:23:00+00	Crédito de $270.00 registrado.	2	191
926	5b571fe9-5678-457f-9643-591bcee855c9	income	2024-11-02 01:23:09+00		9	191
927	3f6b1998-b1bd-4376-85ea-70bb55481a49	income	2024-11-02 01:23:45+00		9	60
928	19d97d4f-59d7-45cb-bf84-1de5ce7a6eae	income	2024-11-02 01:24:37+00		9	214
929	2ee18444-ee4c-4494-af3f-a2aa3f39f937	expense	2024-11-02 01:27:47+00	Crédito de $270.00 registrado.	2	171
930	ba40bb38-fe61-42dc-96bc-db84c019168b	income	2024-11-02 01:29:38+00		9	196
931	04df7eaf-35b4-4284-b7dc-08a72b662bef	income	2024-11-02 01:33:01+00		9	173
932	faf9dc98-bcde-45e2-9a66-abcb3f97efb1	expense	2024-11-02 01:33:53+00	Crédito de $300.00 registrado.	2	16
933	f97e4e3d-c50d-4271-b4dc-84ca060a5508	expense	2024-11-02 01:34:33+00	Crédito de $150.00 registrado.	2	229
934	12c75b25-b5df-4b3f-8206-a9c1191b2d63	income	2024-11-02 01:36:52+00		9	190
935	5e57cf6d-2e91-42a7-b3df-82f6dc2c36ef	income	2024-11-02 01:39:42+00		9	166
936	1592dd8f-9366-4f39-b484-8536eef42433	income	2024-11-02 01:40:33+00		9	183
937	9a0332e5-4fd5-4520-b262-89cd5a54dbf0	income	2024-11-02 01:41:30+00		9	133
938	2b00306c-9e81-4ccc-bace-dc919287eea5	income	2024-10-08 20:01:59+00		9	44
939	63ff65c8-3cc6-4be5-ac47-fc5c1571d09a	expense	2024-11-02 20:16:09+00	Crédito de $140.00 registrado.	2	44
940	ab834a10-a373-4664-92df-c7e6e6fd7b38	income	2024-11-10 20:17:35+00		9	150
941	36ca87d9-c42b-403e-964f-ed1a59fd9b71	income	2024-11-02 20:18:06+00		9	41
942	02241920-899a-4de2-888e-16b3d74c7964	expense	2024-11-02 20:19:08+00	Crédito de $90.00 registrado.	2	230
943	c55e9367-33e4-40ac-be29-ee04f4995945	income	2024-11-02 20:20:07+00		9	47
944	06b9fd93-0a75-4cf8-81bb-2684831804dc	income	2024-11-02 20:20:50+00		9	38
945	f21afe06-b94f-4947-bd1c-281d602bd26b	income	2024-11-02 20:21:32+00		9	176
946	87fceef0-7138-4391-8045-96621b895646	income	2024-11-02 20:23:19+00		9	186
947	99e311e9-7f6f-474e-adb2-0c4d10c43a67	income	2024-11-02 20:23:46+00		9	182
948	6760d8c4-152d-4e2c-93e5-0009a92778c0	expense	2024-11-02 20:24:40+00	Crédito de $140.00 registrado.	2	3
949	d163127d-3da5-401c-aaef-8f56bfd21338	expense	2024-11-02 20:25:22+00	Crédito de $150.00 registrado.	2	206
1258	90cbdc67-6edd-411e-b96c-ff7f75088c85	income	2024-11-23 21:30:21+00		9	186
1262	9861b704-0cfa-4aaa-ad0c-962625a4c68e	income	2024-11-23 21:32:05+00		9	74
1266	5ba4907b-98a6-4ae5-a9e9-bbb62eecc21b	income	2024-11-25 21:38:48+00		9	145
956	79880eff-f8db-4b7d-8bcb-3147a94c7393	expense	2024-11-02 20:27:03+00	Crédito de $260.00 registrado.	2	103
957	2d896ede-de37-4889-a601-34b284e34c3c	expense	2024-11-02 20:30:00+00	Crédito de $110.00 registrado.	2	231
958	0eb2e8e9-9530-4685-b2cd-7b8f0e962ece	income	2024-11-03 20:34:03+00		9	49
959	5b4c94b0-8693-47e4-a00c-22ac512c6422	income	2024-11-10 20:34:36+00		9	85
960	c07626f1-3c66-4b13-8c54-058d6db22d92	income	2024-11-03 20:35:11+00		9	161
961	7ff912eb-19e1-4af8-8ceb-dea526d133ec	income	2024-11-03 20:35:47+00		9	132
962	ca932a67-3b29-4c12-b4ed-64e1d3060580	expense	2024-11-03 20:37:14+00	Crédito de $165.00 registrado.	2	150
963	dc1f9013-53dc-4e03-b239-a172ed8bfb17	expense	2024-11-04 20:37:59+00	Crédito de $480.00 registrado.	2	56
964	01fbb7b9-f5bd-4935-8f0a-7dd609350a68	income	2024-11-04 20:38:41+00		9	147
965	17c468a5-13c9-48fa-a9e4-88de69e6d274	income	2024-10-05 20:42:04+00		9	147
966	9d0b6b45-17f2-4865-8e28-f68dd10fc170	income	2024-10-12 20:42:55+00		9	147
967	1dae42ad-ba8b-47f4-b0fa-20fb4adb8afd	expense	2024-11-04 20:45:07+00	Crédito de $120.00 registrado.	2	147
968	f9e01610-3c8c-42c6-9437-dc415b734013	expense	2024-11-04 20:45:39+00	Crédito de $150.00 registrado.	2	181
974	09af96a1-cfbf-4cf5-a075-8b3fff67e046	expense	2024-11-04 20:47:00+00	Crédito de $140.00 registrado.	2	40
975	98a944da-ca8d-4036-beea-f8093bb7b629	income	2024-11-05 20:48:14+00		9	146
976	b0b38309-9590-4e98-9b44-a0db8c128ae8	income	2024-11-05 20:48:40+00		9	49
977	11d13136-05d9-4a54-ae7d-37e24cbfc13c	expense	2024-11-05 20:49:19+00	Crédito de $2500.00 registrado.	2	10
978	3da449af-fc17-402a-adc8-807b5ccd7731	income	2024-11-06 20:51:45+00		9	18
979	6cec3a1d-39fa-4619-9e26-be1d4a68386d	income	2024-11-06 20:52:29+00		9	89
980	a8288cd8-cf3f-4644-b193-60ac105f2788	income	2024-11-06 20:53:40+00		9	149
981	1af9c588-8779-44eb-b488-faee5470e7c4	income	2024-11-06 20:54:32+00		9	2
982	e1995924-c5e5-4974-8f0d-fd937b21c9c7	income	2024-11-06 20:55:42+00		9	10
983	9253e185-89d7-4fd7-ad93-e8a2365e4bea	income	2024-11-06 20:56:23+00		9	49
984	6d06d60e-1db5-443d-873a-8b23afcfd011	expense	2024-11-06 20:58:03+00	Crédito de $300.00 registrado.	2	182
985	8e2a5f32-2193-4ce3-b840-607b2b0bdb0e	expense	2024-11-06 20:58:40+00	Crédito de $90.00 registrado.	2	144
1231	f13d222b-67c4-4119-81a7-0a4d8468979d	expense	2024-11-22 00:45:03+00	Crédito de $1050.00 registrado.	2	93
991	4e1c7a88-a3d4-41ab-8b27-fc383c4b951a	expense	2024-11-06 21:00:00+00	Crédito de $90.00 registrado.	2	167
992	d2ec2116-9e18-4419-aaaa-e09567a95efd	expense	2024-06-28 17:59:03+00	Crédito de $380.00 registrado.	2	227
870	ff150b48-87e7-4d69-b06e-654cb463fd94	income	2024-10-30 23:01:51+00		9	227
993	4040602b-05d6-462f-a39c-ebcba86aab41	income	2024-07-25 18:04:47+00		9	227
994	4406f122-e5c8-436d-9744-57e395f967f8	income	2024-09-11 21:16:37+00		9	32
995	c48df17f-5d40-40cf-8fd2-6e00323ceb9b	expense	2024-10-30 21:22:14+00	Crédito de $1000.00 registrado.	2	121
996	c25d3c2a-8eeb-48e2-9f44-f0f0b7bcd0d7	expense	2024-11-01 21:24:50+00	Crédito de $1200.00 registrado.	2	98
997	01b7f56b-e5c5-47c5-acd2-a16a53c267a7	expense	2024-10-17 21:25:53+00	Crédito de $800.00 registrado.	2	93
998	02d5d428-e987-43e6-b989-c0d9d7300289	expense	2024-08-13 21:50:35+00	Crédito de $570.00 registrado.	2	24
999	eabf4d07-2537-4321-90bd-607772f30c45	expense	2024-09-26 22:00:08+00	Crédito de $300.00 registrado.	2	51
1000	54def6af-7476-4875-8f7f-f2832db157a9	income	2024-10-14 22:01:12+00		9	51
1001	b491525d-e3fb-4131-ab66-1b89682e85a6	income	2024-10-30 22:02:06+00		9	51
249	610e67e5-fb3b-4f42-bb5b-172919aa894c	income	2024-09-20 19:31:19+00		9	73
1002	abfd72cc-1d9f-48a5-8a05-ac586573f335	expense	2024-07-25 22:06:20+00	Crédito de $150.00 registrado.	2	233
1003	f71412e8-dc6f-4d9b-917e-0665c2fe5224	expense	2024-08-30 22:12:06+00	Crédito de $50.00 registrado.	10	233
1004	aa7f9fd9-2a70-4f15-9ae1-491b04d7dfb7	expense	2024-08-30 22:13:16+00	Crédito de $35.00 registrado.	2	233
1005	568c8dc5-a16c-4e3c-a0ad-a7690e094757	income	2024-09-11 22:16:10+00		9	233
1006	9ce9a4a5-289f-438e-808f-6e9018a09d67	expense	2024-03-02 22:04:23+00	Crédito de $250.00 registrado.	2	234
699	2476d069-f855-4051-a5cd-94776ec9bc9c	income	2024-10-17 21:16:02+00		9	166
1007	0896dcea-9852-40d8-9c42-44cfc8155460	expense	2024-11-08 21:09:32+00	Crédito de $80.00 registrado.	2	218
1008	34488aa5-0d67-468c-ae67-b1c8d6310218	expense	2024-11-08 21:10:44+00	Crédito de $150.00 registrado.	2	153
1009	faaed7d3-ce14-4081-b92a-4ec3bf34050b	income	2024-11-08 21:23:23+00		9	136
1010	926b4584-5257-46c2-88c8-80fe889f1096	income	2024-11-08 21:23:53+00		9	116
1011	0132aaf3-219c-4cc9-b730-0a6388e9080f	income	2024-11-08 21:24:21+00		9	186
1012	b57076c2-4fbb-43d2-b4b9-121bfeddbd8a	income	2024-11-08 21:24:51+00		9	49
1013	cd423bfa-1082-413c-b2c1-7c9e5a3553db	income	2024-11-08 21:25:27+00		9	10
1014	d7e67ff4-b8ff-4601-822f-d35776ad96d2	income	2024-11-08 21:25:55+00		9	1
1015	347784a1-e4d3-45c1-a694-0ccf4cf84320	expense	2024-11-08 21:27:21+00	Crédito de $130.00 registrado.	2	235
1016	ee7b21d3-67e4-4360-853c-666d8c65e1d4	expense	2024-11-08 21:34:29+00	Crédito de $280.00 registrado.	2	201
1017	2bb243ec-aae8-4caf-8ff8-1f3ec59737da	income	2024-11-09 21:40:08+00		9	74
1018	a1fc6c67-445f-46a6-95fa-57ba742aea8c	income	2024-11-09 21:40:52+00		9	21
1019	413a37cd-c89f-492f-934d-bfd53c50d75c	expense	2024-09-30 21:47:30+00	Crédito de $360.00 registrado.	2	145
1020	b34f420a-541d-4b29-869c-dc229649ccc6	income	2024-10-10 21:51:01+00		9	145
1021	6796cd35-bc20-45b3-a0a9-b3fd54d0b9d0	income	2024-10-25 21:52:48+00		9	145
1022	e20c2b8f-4797-437b-a6f2-541b21092a44	income	2024-11-09 21:53:20+00		9	145
1023	69dba6aa-3de0-45f5-b903-3c657b14b148	expense	2024-11-09 21:53:56+00	Crédito de $330.00 registrado.	2	145
1024	ac00d9eb-ce38-493b-af4b-33b1a58965a1	income	2024-11-20 21:55:18+00		9	136
1025	92e052a1-255b-427d-ad22-ab3c07752cb0	income	2024-11-09 21:56:08+00		9	186
1026	6717c02a-4421-40f9-92c3-16351c4b06ee	income	2024-11-09 21:57:59+00		9	10
1027	d3cbb8f5-7bb9-4283-a80a-cafd919fdd5c	income	2024-11-09 21:58:36+00		9	49
1028	e98fdd7b-7073-41b2-ad17-1b1d75a63c70	income	2024-11-09 21:59:13+00		9	38
1029	6726ecbd-cc6c-4e26-ad5a-2c4eef88cb3a	income	2024-11-09 21:59:47+00		9	146
1030	0fc2b1c9-8c15-4bb2-bd5e-3f042ca77c93	income	2024-11-09 22:00:26+00		9	103
1032	177c1ed2-5a69-4afc-8228-65962bb89aff	income	2024-11-09 22:01:51+00		9	160
1031	b13e2626-4e5b-4dd6-839e-5f815f5d8f8c	income	2024-11-09 22:01:23+00		9	86
1033	a769ca96-1a81-41b5-99d5-047a6026636f	expense	2024-11-09 22:03:32+00	Crédito de $132.00 registrado.	2	1
1034	68ce3e48-0576-4bf3-a572-c93e7029b8d6	expense	2024-11-10 22:04:00+00	Crédito de $140.00 registrado.	2	170
1035	c69f14a8-9520-4f28-8d60-3a2e13232b2a	expense	2024-11-10 22:05:02+00	Crédito de $70.00 registrado.	2	236
1036	18554a52-6709-4f35-9f26-9aa9b31972a6	expense	2024-11-10 22:07:04+00	Crédito de $186.00 registrado.	2	61
1037	48fbefae-bb0c-43e3-bcad-5851e3fbc11c	income	2024-11-10 22:07:53+00		6	49
1038	88815ef5-5854-41fd-b40e-6ab931723ffb	income	2024-11-10 22:08:28+00		9	34
1039	ae55e7c3-faee-4373-822f-004af5902412	expense	2024-11-11 22:40:07+00	Crédito de $50.00 registrado.	2	237
1040	dbea526a-47ff-48e4-9dec-fa49538d04c5	expense	2024-11-11 22:47:12+00	Crédito de $150.00 registrado.	2	238
1041	00480849-f8df-4fa2-bbb5-03b06ba6dec2	income	2024-11-12 22:51:31+00		9	221
1042	966c2be5-89ff-436e-97b7-971b6b02f014	income	2024-11-12 22:52:10+00		9	84
1043	4355b181-86b8-4761-b593-2d11bc0fa331	expense	2024-11-12 22:52:56+00	Crédito de $130.00 registrado.	2	84
1044	111ebdd6-83a9-483b-acba-cd5947f318e3	income	2024-11-12 22:53:28+00		9	61
1045	176804a1-a953-4ef3-99e7-a92ff4c1cee1	income	2024-11-12 22:54:24+00		9	29
1046	b3a3d09d-63fe-4635-9df3-261a9b369def	income	2024-11-12 22:54:53+00		9	178
1047	ab1e23b8-93ce-4f09-ab99-57d2490d7f3c	income	2024-11-12 22:55:19+00		9	3
1048	7d0578fc-ac37-4cb9-bb69-54cd4090c2a0	income	2024-11-12 22:55:45+00		9	71
1049	0549c78e-4f24-4022-bf87-d2f10a2e3607	income	2024-11-12 22:56:27+00		9	205
1050	5b5bddff-3cf4-4760-8eea-0aad148fb09b	income	2024-11-12 22:56:58+00		9	75
1051	046b241e-43ce-4dae-a1a0-fc02ddae2f4b	income	2024-11-12 22:57:49+00		9	76
1052	85244e31-ed5e-4c66-a9af-2412ca8b3e91	income	2024-11-12 22:58:18+00		9	211
1053	7493769f-65bf-4814-81c6-1916a31539cc	income	2024-11-12 23:03:41+00		9	186
1054	f41d4476-46a1-440b-83cf-b107342554a6	income	2024-11-12 23:04:18+00		9	49
1055	5fc95ad7-00d2-4a5e-bb0c-9bc5e7fcf76d	income	2024-11-20 23:05:31+00		9	10
1056	9c03652b-ae6c-4966-9fd4-d4f30879a634	income	2024-11-12 23:06:16+00		9	218
1057	8211db87-880e-4a2d-9a3d-9e6c8ceac1a4	income	2024-11-12 23:06:55+00		9	147
1058	2030b0ff-8997-4b43-951d-d37b27709229	expense	2024-11-12 23:07:41+00	Crédito de $1400.00 registrado.	2	49
1059	fe4998d0-968d-4b92-a249-af1b75c350f4	income	2024-11-13 23:10:26+00		9	40
1060	d9618cdc-dabc-4b6c-ba43-c101856dfd9f	income	2024-11-13 23:10:54+00		9	51
1061	5556a614-e877-4b7f-9f56-a27cfd5553ba	income	2024-11-20 23:11:28+00		9	186
1062	89b098f5-0e43-4544-85a6-99ce4c80419d	income	2024-11-13 23:12:47+00		9	213
1063	c28759db-9893-4752-a880-94b121ac3ec4	income	2024-11-13 23:13:52+00		9	37
1064	adc82c9c-8f3e-41e4-ae11-66b3a1213fd3	expense	2024-11-13 23:15:31+00	Crédito de $85.00 registrado.	2	84
1232	e53eefad-b9f9-4037-a2f8-cc39a5600762	expense	2024-11-22 00:49:52+00	Crédito de $180.00 registrado.	2	73
1243	f80a3366-d2b2-43af-b33c-4ce12ecc946a	expense	2024-11-23 01:17:39+00	Crédito de $140.00 registrado.	2	218
1249	8751d604-4a3e-4b40-9224-5504743b08b8	income	2024-11-23 01:19:48+00		9	67
1254	5578d325-cc87-433c-bb5b-cf085a050872	expense	2024-11-23 21:27:04+00	Crédito de $500.00 registrado.	2	98
1070	44fe2396-701e-4bb9-bb26-5c3b2a5abf00	expense	2024-11-13 23:17:01+00	Crédito de $280.00 registrado.	2	66
1259	8e6ae324-916f-417a-9085-59c1f91713b5	income	2024-11-23 21:30:47+00		9	49
1263	045c2494-95f6-44fb-a2b9-36f284cc2f81	expense	2024-11-24 21:35:36+00	Crédito de $120.00 registrado.	2	257
1267	0bf86fb5-eaf4-440c-817f-db063306229d	income	2024-11-25 21:42:10+00		9	176
1270	320b2bf6-787f-45f8-b915-66e76cfb42d8	income	2024-11-25 21:45:26+00		9	253
1273	c6b0188a-d748-411f-8d45-27e7bed36fe2	income	2024-11-25 21:56:02+00		9	49
1275	674fc5a2-3b16-4dd1-bb88-92c1a479641f	income	2024-11-25 22:05:24+00		9	1
1277	200b087f-6518-42a8-b359-af01f3b28535	expense	2024-11-25 22:08:54+00	Crédito de $120.00 registrado.	2	244
1078	fa1b3ba7-8eb7-4e25-8ca7-3ea36378e04e	expense	2024-11-13 23:17:55+00	Crédito de $40.00 registrado.	2	149
1079	c1b93e7c-df88-4dd4-8be2-67426cf7561a	expense	2024-11-14 23:18:57+00	Crédito de $140.00 registrado.	2	159
1080	6f943bcf-5f44-49f0-a443-70d0a7fabc05	income	2024-11-14 23:19:58+00		9	6
1081	048d9df0-af0e-4cdb-8138-4ee2fe3d4213	income	2024-11-14 23:21:11+00		9	99
1082	b12adb85-3a29-4274-baa6-34f897fc95cd	expense	2024-11-14 23:25:47+00	Crédito de $280.00 registrado.	9	83
1083	e6523d08-8210-48ca-827f-a3a527137c8e	income	2024-11-20 23:26:56+00		9	64
1084	7733b41a-6238-4c3a-8eb8-0deaabc27502	expense	2024-11-14 23:34:47+00	Crédito de $460.00 registrado.	2	211
1085	9e47b54a-e8c8-418b-a06d-516cdb7685ed	income	2024-11-14 23:36:41+00		9	131
1086	b2bbd311-9e0e-4dc2-81ad-39eee4ae00f2	expense	2024-11-14 23:40:37+00	Crédito de $140.00 registrado.	2	239
1087	15db8d93-9506-4f8d-9913-472ffbde74aa	income	2024-11-14 23:42:33+00		9	186
1088	374a5cb1-f7bd-4c81-9084-d6f7dd0c571b	income	2024-11-14 23:43:13+00		9	10
1089	f2680e22-dc0c-4274-b8ae-c4e0fa3c2cdd	income	2024-11-14 23:44:11+00		9	49
1090	f8a2b2e0-6bc8-45a2-9763-14ace8bbeacc	income	2024-11-14 23:46:20+00		9	240
1091	bdfe4aa8-9025-40b5-bef0-338a327cc6ed	income	2024-11-14 23:46:48+00		9	82
1092	187c6630-84ba-4740-b104-0cc86a1244f0	income	2024-11-14 23:47:34+00		9	35
1093	3d282a0b-76e9-466c-b196-1e23f37b74f5	income	2024-11-14 23:48:09+00		9	6
1094	75a75d3e-0af8-422d-97ea-67ebdc69b20a	income	2024-11-14 23:59:11+00		9	174
1095	e100134e-57a0-4fbb-808d-7bf140c920f3	income	2024-11-14 23:59:47+00		9	136
1096	c6db20da-13af-440c-b20c-c30d0e1cc63a	expense	2024-11-01 00:33:32+00	Crédito de $240.00 registrado.	2	88
1097	d7fae91e-24a7-4de7-9551-de779cb2ce5b	income	2024-11-15 00:34:42+00		9	88
1098	f9dca37a-749d-454b-86e9-cc02e6cd52c7	income	2024-11-16 00:37:23+00		9	3
1099	a818b324-e1c0-4976-a675-a298e8e7fccc	expense	2024-07-28 00:42:55+00	Crédito de $140.00 registrado.	2	179
1100	c822aeff-ff5f-4bdc-9493-3fcf0d884da0	income	2024-09-28 00:44:32+00		9	179
1101	e68439e1-4426-429f-b13e-8400aaaeea19	income	2024-10-15 00:45:27+00		9	179
1102	d3132dc5-cb02-4b0f-acbd-089443a7e6cf	expense	2024-11-15 00:47:18+00	Crédito de $140.00 registrado.	2	179
1103	22c7b52d-fb71-4391-8ec6-0fdb47750159	income	2024-11-16 00:48:06+00		9	179
1104	32342315-86a0-4302-a97e-995221723e05	expense	2024-11-16 00:48:48+00	Crédito de $140.00 registrado.	2	179
1105	75d1ac57-1f04-4014-b594-3b928037a1f8	income	2024-11-16 00:49:44+00		9	157
1106	fc380b92-d87e-4601-bcad-ffeec19e2e53	income	2024-11-16 00:50:20+00		9	210
1107	dc66d2c6-a8ac-4f56-9099-fd9fb10c5e3b	income	2024-11-16 00:50:46+00		9	93
1108	3a18f8f5-222e-48b2-9eaf-26b30a500935	expense	2024-11-16 00:51:29+00	Crédito de $750.00 registrado.	2	93
1109	5dbb89a2-9e98-4ce5-a4f0-95d4f992419f	income	2024-11-17 19:00:22+00		9	42
1110	b93f98a3-8e02-4c10-bf4a-04461871d63b	income	2024-11-17 19:01:52+00		9	98
1111	801fe2c4-a327-4b69-92b7-5f594cdde33e	expense	2024-11-17 19:05:07+00	Crédito de $130.00 registrado.	2	111
1112	0e1a6ec4-f4bd-40fd-929f-b7fa88bf84ec	expense	2024-11-17 19:05:38+00	Crédito de $800.00 registrado.	2	98
1113	b1ccad4a-aecc-442b-bafd-9e304411e167	income	2024-11-17 19:06:39+00		9	16
1114	16694232-a0ee-4999-a75d-62dc5374ed44	income	2024-11-17 19:07:19+00		9	229
1115	4f70a6d6-79b7-4955-adc6-aafb82fa5955	income	2024-11-17 19:08:33+00		9	41
1116	d12da402-a2a6-43b4-87ce-2de99749fba7	income	2024-11-17 19:09:08+00		9	160
1117	5e733293-afd7-434f-b71d-6e7d75e84d15	income	2024-11-17 19:09:42+00		9	150
1118	e18739e8-130b-488f-aa79-191526531aba	income	2024-11-17 19:13:33+00		9	65
1119	8372deed-f250-4dda-b354-ecd9eda684dc	expense	2024-11-17 19:22:07+00	Crédito de $550.00 registrado.	2	201
1120	5c0b7bd3-f9b7-445f-9798-6fb4b1978d1a	expense	2024-11-17 19:22:37+00	Crédito de $150.00 registrado.	2	241
1121	0063dba9-3f26-4006-8131-58847141ebd6	income	2024-11-19 00:06:31+00		9	208
1122	c0ee99e9-6a6b-4249-add3-340728a08dbc	income	2024-11-19 00:07:33+00		9	50
1123	071e044e-fb89-40c1-b9f1-875fac0cb584	income	2024-11-19 00:09:17+00		9	189
1124	dba8579f-d54b-49cb-803f-dfbb061e9be3	expense	2024-11-19 00:10:24+00	Crédito de $135.00 registrado.	2	189
1125	69975e0d-9848-40f3-a17f-4fafd7de8502	income	2024-11-19 00:11:56+00		9	170
1126	f044bff2-c92e-4804-a9f6-15367a6402eb	income	2024-11-19 00:12:24+00		9	13
1127	fb134b89-9ce9-44aa-80e0-5dbc952a0677	income	2024-11-19 00:12:47+00		9	214
1128	f7f8e2c7-1fdd-4f86-820e-5f4ae095b230	expense	2024-11-19 00:14:13+00	Crédito de $280.00 registrado.	2	242
1129	a222a02a-1678-474d-a3b8-65b06f247bbb	income	2024-11-19 00:16:13+00		9	106
1130	4a083a11-15c5-4019-b177-7d105912d091	income	2024-11-19 00:16:50+00		9	186
1131	594504a6-0bda-4851-a55b-8b222a17d15a	income	2024-11-19 00:17:14+00		9	56
1132	bd24efbb-a331-460f-a4ca-a8f853a1e89d	income	2024-11-19 00:17:37+00		9	90
1133	62b1061e-45b2-4778-a4d7-dbf84df3476b	expense	2024-11-19 00:32:29+00	Crédito de $140.00 registrado.	2	243
1279	b97bf4f3-cca4-45b4-aff1-0b3506460b7d	expense	2024-11-25 22:11:07+00	Crédito de $25.00 registrado.	2	260
1281	c87a91d6-86b4-43f8-9b26-4dc218cb553a	expense	2024-11-25 22:14:18+00	Crédito de $60.00 registrado.	2	262
1282	d0a86011-8199-4f59-a235-52de108ebdb8	expense	2024-11-25 22:16:33+00	Crédito de $60.00 registrado.	2	263
1140	1e5ad25c-3309-4e1a-b9ac-1a9e877cf001	expense	2024-11-19 00:35:00+00	Crédito de $35.00 registrado.	2	218
1141	8813629c-bedf-4c53-9aa1-85309fdbaa89	income	2024-11-19 00:35:16+00		9	10
1142	a86d66c4-51de-42b0-9884-9d0f7be6b525	income	2024-11-19 00:35:53+00		9	49
1143	5616e7fc-e3cf-4bbb-a80a-67b5d1f83a21	income	2024-11-19 00:36:42+00		9	240
1144	c93e11e0-1dcd-4b83-9145-3ed88d965056	expense	2024-11-19 00:37:34+00	Crédito de $380.00 registrado.	2	99
1145	79e2bfd9-38bf-48c8-ab02-a38cba341504	expense	2024-11-19 00:39:07+00	Crédito de $60.00 registrado.	2	244
1146	3521db29-9d5c-47d7-a0f1-f7bb7cf929e8	expense	2024-11-19 00:41:32+00	Crédito de $120.00 registrado.	2	245
1147	ad134cd5-83dc-4068-a808-9d1835c9423c	income	2024-11-20 00:43:23+00		9	54
1148	9a902392-57bf-4a1f-99a5-c3d9bdfe6df5	income	2024-11-20 00:45:46+00		9	97
1149	4989821b-6347-4acb-b3bd-c46ecd98a3e3	expense	2024-11-20 00:47:12+00	Crédito de $1050.00 registrado.	2	176
1233	d9df4b9c-2054-41f2-b158-57d978322541	income	2024-11-22 00:52:15+00		9	186
1151	12f083d5-3bee-4146-b6f3-2f7c51480f48	expense	2024-11-20 00:48:17+00	Crédito de $140.00 registrado.	2	81
1152	be3bc1c8-7452-4e96-9fa4-f606bb8d29f4	expense	2024-11-20 00:52:58+00	Crédito de $140.00 registrado.	2	81
1153	34fe4ed8-49df-43eb-9758-e83240cb7b4d	expense	2024-11-20 00:57:59+00	Crédito de $80.00 registrado.	2	246
1154	1f81ef26-1abd-4999-802c-2707a1d8f7ed	income	2024-11-20 00:59:15+00		9	186
1155	363a88aa-94cb-44ff-bad1-c63ee4a1aa80	income	2024-11-20 00:59:54+00		9	49
1156	ef4d6433-2321-4455-ae2d-a63efb43f19a	income	2024-11-20 01:00:26+00		9	147
1157	9b0d70e8-348c-4d80-a569-fcb0ba48635f	income	2024-11-20 01:00:53+00		9	208
1158	7f89f691-c85a-438b-b11e-19e20e2c2977	income	2024-10-08 18:06:11+00		9	135
1159	e59f70a6-05b1-4330-b189-8e5e4a80f8a1	income	2024-09-11 18:06:52+00		9	135
1160	a2b0715e-8b92-440b-8f9f-ff4a2ccff173	income	2024-09-11 19:11:12+00		9	40
1161	c85bea68-8d7c-45dd-a9e2-c8675bd37853	income	2024-11-15 18:53:05+00		9	167
1162	1b99bf1a-2c76-4ccd-9c25-f8816709fe13	income	2024-11-15 18:54:24+00		9	108
1163	28499010-6ae0-4890-8741-5cecfc41dfa2	expense	2024-11-15 18:56:12+00	Crédito de $280.00 registrado.	2	247
1164	e8e043a3-fafd-449f-bee7-643bbd16364c	income	2024-11-15 19:18:55+00		9	55
1165	50b5ea7c-a9f2-4ee2-84b1-9a800c148493	income	2024-11-15 19:27:41+00		9	155
1166	4951f931-ad4f-4ffe-94b6-6531170909dd	income	2024-11-15 19:29:37+00		9	126
1167	1c825f36-d90d-42c6-8668-b675b936f065	income	2024-11-15 19:31:37+00		9	19
1168	9bb5c410-e376-40c2-b639-7458391da5a3	expense	2024-11-15 19:39:45+00	Crédito de $501.00 registrado.	2	19
1169	130e2e6f-af99-4dc1-bca5-238eb884532e	income	2024-11-15 19:41:25+00		9	110
1170	630266b0-7389-443d-a44c-2d762bc04fdc	expense	2024-11-15 19:43:53+00	Crédito de $250.00 registrado.	2	110
1171	94090924-485e-4009-808b-1772d908e13e	income	2024-11-15 19:44:46+00		9	49
1172	ffd512a4-338f-450c-9aa5-8d29ef6fa845	income	2024-11-15 19:45:26+00		9	240
1173	ad102ce1-e38e-443d-9d8b-d93bc70b3add	income	2024-11-15 19:45:55+00		9	10
1174	4847d06d-310c-41f0-8076-0c66147d2ff0	income	2024-11-15 19:47:42+00		9	209
1175	9a5e6b69-7f1b-4012-92e5-6ff8231aa269	income	2024-11-15 19:53:06+00		9	144
1176	6755f142-6fe2-46dc-ad22-95161f5f145f	income	2024-11-15 20:56:28+00		9	215
1177	6ceadc78-04ac-4894-971f-24eb079107c5	income	2024-11-15 20:57:26+00		9	138
1178	22527016-c64e-4980-a146-f8b2240f7788	income	2024-11-15 20:58:06+00		9	109
1179	7026f744-7204-4c48-9f7e-a41168be1224	income	2024-11-15 20:58:42+00		9	206
1180	f1de7c19-ab7d-4d5b-8a04-56fc943de1ea	income	2024-11-15 21:02:21+00		9	199
1181	91fbe13a-cf46-4188-88a9-53d009feb06d	expense	2024-11-15 21:08:26+00	Crédito de $1140.00 registrado.	2	6
1182	7123d219-1d22-4eec-8b94-c21c14d1371b	income	2024-11-15 21:09:57+00		9	195
1183	639b0909-8a34-4378-9f47-591755fe434f	income	2024-11-15 21:10:30+00		9	228
1184	fd9c4742-3d03-4dae-85c2-5d69ddc063ce	income	2024-11-15 21:11:19+00		9	201
1185	2bbee863-4c5b-4559-9d27-267096b064ec	income	2024-11-26 21:13:00+00		9	197
1186	5bd0441c-adba-4cc7-9605-5f0ec53fae09	income	2024-11-15 21:43:09+00		9	158
1187	df9b4462-3ac1-4995-9985-26d72914dfd8	income	2024-11-15 21:43:47+00		9	163
1188	394fcdd5-547b-4527-bd58-278caf3b3e0c	expense	2024-11-15 21:44:38+00	Crédito de $550.00 registrado.	2	197
1189	3f82af83-6bb6-4349-aab6-2b0caed034ed	income	2024-11-15 21:45:46+00		9	63
1190	0def36f9-a176-4af1-a3ac-a582990eed4a	income	2024-11-15 21:47:12+00		9	192
1191	b758c98f-ebf0-422b-aacd-7e8614cfa5f0	income	2024-11-15 21:47:38+00		9	77
1192	984be26e-56d5-41de-b9f4-2c479246e50b	income	2024-11-15 21:48:23+00		9	191
1193	146cf8ac-bdac-4006-ba9a-e9d33da49efe	expense	2024-11-15 21:52:52+00	Crédito de $140.00 registrado.	2	55
1194	707a4e8f-3753-492e-9708-97dbbf6da2f6	expense	2024-11-15 22:00:52+00	Crédito de $250.00 registrado.	2	248
1195	91d877ba-70d1-4bd5-84b6-2f166133240d	income	2024-11-15 22:02:22+00		9	98
1196	bd3c97c8-3e41-4414-8e32-165032bba922	income	2024-11-15 22:03:03+00		9	171
1197	084827e1-dce2-4889-994b-3c347d268d51	income	2024-11-15 22:21:37+00		9	196
1198	0e371b70-589d-46b9-b0ab-79c8f0172e5f	expense	2024-09-19 22:27:29+00	Crédito de $360.00 registrado.	2	12
1199	1f0fed5b-2c01-48bf-a7df-1506c593da08	income	2024-10-16 22:34:19+00		9	12
1200	00d1ddde-974b-45ec-8284-4574739f325c	income	2024-11-01 22:34:55+00		9	12
1201	48815ae3-75d2-4746-b8d0-dfa37d984d0e	income	2024-11-16 23:04:00+00		9	249
1202	0728643d-1504-46d3-a3af-9743a9826150	income	2024-11-26 23:04:40+00		9	153
1203	62977c6f-452c-41bb-ac01-e247c90a622b	income	2024-11-16 23:05:17+00		9	186
1204	e5253552-6a14-489b-a85d-7e647a2f0148	income	2024-11-26 23:05:48+00		9	182
1205	292b1032-c0f3-427b-a268-f4dd88a7dc84	expense	2024-11-16 23:08:37+00	Crédito de $140.00 registrado.	2	250
1206	f1628984-9d4b-4f7c-b868-2fc88d3c4be2	expense	2024-11-16 23:09:38+00	Crédito de $150.00 registrado.	2	251
1207	d4618aef-a6a4-48ff-8a69-faee613af81b	income	2024-11-16 23:12:50+00		9	15
1208	f65f60ec-9d83-41c6-8d48-6974aeb7f443	income	2024-11-26 23:13:30+00		9	38
1209	9bc37bbb-c763-4588-b7c9-71cba228b895	income	2024-11-16 23:14:40+00		9	230
1210	76826bf2-5d2c-44f5-8d01-3b5c281e80e5	income	2024-11-16 23:18:01+00		9	85
1211	2d4a56c1-a4c5-4c2d-a362-56cc2b08e3ee	expense	2024-11-16 23:19:32+00	Crédito de $165.00 registrado.	9	158
1250	5908d018-f320-42f0-affa-83e2ec44be7b	income	2024-11-23 01:20:24+00		9	186
1255	db1fe5cd-13e1-453b-83b5-f36a7291fa46	expense	2024-11-23 21:28:14+00	Crédito de $140.00 registrado.	2	258
1260	ec5a1749-1758-4d4b-9322-41d4c4c98d2d	income	2024-11-23 21:31:16+00		9	240
1264	234d1108-c12a-4da6-aa57-51c9971f1e20	income	2024-11-24 21:37:44+00		9	49
1268	f2402f8e-f51d-4ff8-afcc-41c37f9e2014	expense	2024-11-25 21:43:36+00	Crédito de $135.00 registrado.	2	164
1217	27267850-bd67-4aee-9bb8-f3ab8753de20	expense	2024-11-16 23:20:52+00	Crédito de $150.00 registrado.	2	162
1218	17dbc665-09a6-4f66-9df9-3d8d1e756447	expense	2024-11-16 23:21:06+00	Crédito de $150.00 registrado.	2	209
1219	fdad5ca1-46d6-42e8-ab3e-c494c28686ba	income	2024-11-20 23:58:12+00		9	2
1271	0fe2f205-db28-43f5-9bc7-495294f30374	income	2024-11-25 21:54:46+00		9	21
1274	1fc0c48a-ce1e-4b5c-ba34-82c15e4339ed	income	2024-11-25 22:04:59+00		9	240
1276	9ff25b40-6539-4665-bbdb-3e88cdf20b62	expense	2024-11-25 22:07:18+00	Crédito de $500.00 registrado.	2	74
1278	9f1b0e59-72e0-419b-a767-86330cc55e5c	expense	2024-11-25 22:09:38+00	Crédito de $120.00 registrado.	2	259
1280	dd06afb0-10d0-4be4-b9c2-470fda329c9c	expense	2024-11-25 22:13:15+00	Crédito de $120.00 registrado.	2	261
1290	5472bb60-2c66-4196-84eb-6aa303646ec4	income	2024-11-27 00:15:29+00		9	136
1287	02d559f3-13a6-4913-9edf-70eebd362cee	expense	2024-11-25 22:21:58+00	Crédito de $120.00 registrado.	2	153
1288	94331f02-20ef-4d16-9da5-a621c29bfd8d	expense	2024-11-26 23:57:00+00	Crédito de $140.00 registrado.	2	133
1289	8afd3257-d704-493b-8ecb-6fd9a5535333	expense	2024-12-26 23:57:40+00	Crédito de $100.00 registrado.	2	214
1291	e84dd8a0-b37b-4f8d-ac67-383262b03359	income	2024-11-27 00:16:01+00		9	176
1292	c77688ae-4c85-4578-b8b4-fd8e9a3b5f21	income	2024-11-27 00:17:05+00		9	49
1293	16aabca3-a3d1-456b-baf9-954b65f90c65	income	2024-11-27 00:17:47+00		9	240
1294	31c5758e-1ef9-4707-8bbd-4eb4cb0a51b4	income	2024-11-27 00:18:12+00		9	186
1295	e57f44ae-3b2f-4f4c-83ce-ca6aeca97e1f	expense	2024-11-27 00:19:59+00	Crédito de $150.00 registrado.	2	264
1296	49f5b328-7928-4f68-9600-6d551cbfd333	income	2024-11-28 00:22:03+00		9	27
1297	0b34ff05-a6da-4671-8b0b-762e09cf9d14	income	2024-11-28 00:25:58+00		9	61
1298	6421a7a4-cd95-45dd-923d-530b18aa2987	income	2024-11-28 00:26:36+00		9	3
1299	6ba716d6-1863-459f-96b6-98f2c29824cd	income	2024-11-28 00:27:28+00		9	73
1300	f1ea328a-6f7f-429f-a26e-cb0d3ef600a8	income	2024-11-28 00:30:34+00		9	205
1301	3ff16dc0-d8d9-4783-96ad-e824b893d351	income	2024-11-28 00:31:43+00		9	84
1302	250f7247-69d7-4660-ad4e-b122783002ae	expense	2024-11-28 00:35:09+00	Crédito de $130.00 registrado.	2	84
1303	e534cb64-a6fe-4bb5-be4e-0a32c050e1c9	expense	2024-11-28 00:36:28+00	Crédito de $75.00 registrado.	2	84
1305	a3837832-96eb-46dd-9aca-45d124b94d1d	expense	2024-11-28 00:37:01+00	Crédito de $230.00 registrado.	2	84
1306	0a20996e-6135-499c-abf4-88cfaa84c36d	income	2024-11-28 00:41:44+00		9	78
1307	55c54272-81e5-4fc4-aa81-b78d2a7afb41	income	2024-11-28 00:46:16+00		9	186
1308	02f4429b-c067-440d-a9bc-23797be59e2c	income	2024-11-28 00:48:53+00		9	176
1309	15c75c47-9edf-4850-b145-634c9be40d30	income	2024-11-28 00:49:32+00		9	49
1310	bbf3e22b-143c-4bb8-abe5-b32915fdaa48	income	2024-11-28 00:49:59+00		9	240
1311	beacb4e1-4bcc-4765-8566-ddc5e822ce2d	income	2024-11-28 00:50:37+00		9	34
1312	61be4edd-55e9-480e-9347-f22094aefb7a	income	2024-11-28 00:51:15+00		9	102
1313	ff1d6f97-0746-4848-81b5-603bc560b88e	income	2024-11-28 00:53:52+00		9	1
1314	9668a489-bf6f-4026-9268-67abe7db059c	income	2024-11-28 00:54:33+00		9	40
1315	4cc44514-0381-42b5-b210-dad4fdaa99ef	income	2024-11-29 00:55:18+00		9	49
1316	bdd7c5fc-380f-475d-87ad-45c04900351d	income	2024-11-29 00:56:27+00		9	240
1317	731870a8-59e3-4477-8076-987ebb2eec14	income	2024-11-29 00:56:59+00		9	218
1318	3e5c3df1-a387-4fbc-9699-4fedce107cab	income	2024-11-29 00:57:44+00		9	75
1319	dc383388-179d-4172-966f-e96f5b7c5253	expense	2024-11-29 01:00:36+00	Crédito de $140.00 registrado.	2	265
1320	30029527-7d47-4b21-b8bf-d873c778d485	income	2024-11-29 21:28:50+00		9	157
1321	9612ac89-c2e2-4f42-bbc9-88be0bb87077	expense	2024-11-29 21:29:55+00	Crédito de $250.00 registrado.	2	157
1325	85bda70a-3fc7-4509-bf7e-6590c0bc160c	expense	2024-11-29 21:30:56+00	Crédito de $150.00 registrado.	2	51
1326	bc8b57f8-ed11-446c-9893-a5ef083cb3e1	income	2024-11-29 21:31:46+00		9	51
1327	f2ad0007-2f9d-48ba-81ec-f409958dd350	income	2024-11-29 21:32:45+00		9	258
1328	11d36c1a-87df-4ca7-9c9c-dadfb32ff620	income	2024-11-29 21:33:15+00		9	186
1329	5741a621-2235-4787-a2dc-ee5834c98d64	income	2024-11-29 21:34:26+00		9	49
1330	6fca2080-97bd-44e7-afa5-0d2cb3916a8b	income	2024-11-29 21:39:50+00		9	240
1331	45e54e69-a1a2-419c-83bd-184ff7143a0a	income	2024-11-29 21:40:18+00		9	153
1332	5d070325-e470-4c59-b1fe-fb72769bea0b	income	2024-11-29 21:41:29+00		9	136
1333	ff07f44e-4a42-4162-8f26-fb9cb6c33fc4	income	2024-11-29 21:47:23+00		9	167
1334	1e2544e6-816a-4390-a887-a8e034ac4606	expense	2024-11-29 21:48:21+00	Crédito de $80.00 registrado.	2	18
1335	ea67d5bc-8247-4d72-a6b9-87c14bcaad49	income	2024-11-30 21:54:07+00		9	247
1336	68ed1a63-ef2b-4fe7-a038-d6d68ff6568c	income	2024-11-30 21:54:40+00		9	206
1337	31f30487-653c-4104-be88-33ad4418267e	income	2024-11-30 21:55:09+00		9	19
1338	3e8db0cb-9bfe-4ad6-8d71-ba93de3de42e	income	2024-11-30 21:55:47+00		9	155
1339	85f1d950-60a2-4ca9-8379-ef7774dfe26c	income	2024-11-30 21:56:15+00		9	126
1340	7b18fdd7-86e7-40e5-8b4d-f3e5a8bfec5f	income	2024-11-30 21:56:49+00		9	144
1341	134c0bfb-b384-47be-96c0-cfa6808c6a73	income	2024-11-30 21:57:28+00		9	16
1342	9648689e-68c2-4222-b3f2-64ba28a4de6f	expense	2024-11-30 22:00:34+00	Crédito de $140.00 registrado.	2	218
1343	95aa160d-aac1-4304-b17d-341c3e0cebf2	expense	2024-11-30 22:00:59+00	Crédito de $140.00 registrado.	2	154
1344	9929f083-c37b-4dab-b3f2-3921c5686d72	income	2024-11-30 22:02:08+00		9	7
1345	ae724a21-a017-4970-8aa7-791534e37f11	income	2024-11-30 22:03:29+00		9	215
1346	5fac6922-eb79-4f8f-bd88-29270b505804	expense	2024-11-30 22:08:06+00	Crédito de $360.00 registrado.	2	206
1347	02933825-6c8b-46f3-87ee-9b2d0f15950d	expense	2024-11-30 22:08:37+00	Crédito de $120.00 registrado.	2	92
1348	0da53a96-5d64-4f5c-88b0-8ecba908a713	income	2024-11-30 22:10:31+00		9	178
1349	3c862df1-f645-45c3-8ce9-dc307e1e8fc8	income	2024-11-30 22:12:44+00		9	77
1350	b4e2d0c8-34ef-4ff8-8314-f3934702c60a	income	2024-11-30 22:13:27+00		9	15
1351	67b89904-3244-4908-9a05-8cc2e1ca398a	income	2024-11-30 22:34:30+00		9	242
1352	2ee522db-6d9d-46ab-a01c-3feb5af3fa95	income	2024-11-30 22:35:12+00		9	255
1353	cc4027c9-0a75-4e0b-8cb7-96c9aaf3872a	expense	2024-11-30 22:39:25+00	Crédito de $130.00 registrado.	2	266
1354	f65e1d9b-c00d-4ca5-b2d4-4e78ef724764	expense	2024-11-30 22:40:47+00	Crédito de $140.00 registrado.	2	126
1355	a79e2c8a-41ab-421f-aefe-099257ee477c	expense	2024-11-30 22:41:38+00	Crédito de $140.00 registrado.	2	37
1356	90b85243-04b1-4cb4-a6ff-777912743d7e	income	2024-11-30 22:42:23+00		9	251
1357	f958fb42-8903-4f00-b64b-a2e63a50c4d5	income	2024-11-30 22:44:59+00		9	176
1358	a5bc144b-1257-48e7-80c0-b9b5bdef4b02	income	2024-11-30 22:45:35+00		9	186
1359	ac8ea4f3-9c7b-4f55-af73-0702c9eefed2	income	2024-11-30 22:46:04+00		9	241
1360	e77a1ba4-bcec-4d4b-88bc-3279355b6524	income	2024-11-30 22:49:19+00		9	38
1361	faaea4c4-5054-4461-b67b-06fee09ea0bd	income	2024-11-30 22:49:45+00		9	254
1362	e58a5837-f606-4a93-82cf-caa863996184	income	2024-11-30 22:50:42+00		9	1
1363	23801c02-703e-434b-a1da-53508ff1d96d	expense	2024-11-30 22:52:00+00	Crédito de $35.00 registrado.	2	77
1364	c08135ae-b19a-4d5b-ae3b-9d5b6a1b8d7c	expense	2024-11-30 22:52:26+00	Crédito de $70.00 registrado.	2	40
1365	3fe693cb-a8d7-453a-a526-d4063eb814fd	income	2024-11-30 22:54:02+00		9	153
1366	8281f261-7f1b-4b34-b57c-3a70b737126e	income	2024-11-30 23:03:07+00		9	262
1367	dbd012ad-8f89-4e5b-b345-6d957a1494e4	income	2024-11-30 23:03:45+00		9	261
1368	835cfb06-c0a7-4ac1-8908-a224ef421fc0	income	2024-11-30 23:05:30+00		9	259
1369	0e440e31-b574-42f1-9a8a-298daf6e9311	expense	2024-06-06 23:14:50+00	Crédito de $2600.00 registrado.	2	133
1370	93a768c2-5aa8-4248-af91-6137b0b7edb0	income	2024-06-06 23:15:56+00		9	133
1371	9c2687b0-787c-4159-9d5a-65e0b6f2a841	income	2024-06-19 23:16:46+00		9	133
1372	a128594a-0468-47f2-b17f-499fbeb77643	income	2024-07-17 23:17:25+00		9	133
1373	cd6a6dd3-f16c-4b6e-9b51-1683b7b39474	income	2024-08-03 23:18:03+00		9	133
1374	efccdd1d-5a23-4a42-92f9-16f43676fc57	income	2024-09-17 23:18:30+00		9	133
1375	7ae20ada-c974-4c01-b490-b45d9853faff	income	2024-11-08 23:19:03+00		9	133
1376	81b75738-6f05-4d5f-9c73-905785a69d65	income	2024-11-24 23:19:37+00		9	133
1377	3e5fbc25-8353-459f-b036-5162d2f3211f	income	2024-12-01 23:20:05+00		9	228
1378	12cce4d4-baab-4a58-80fc-92f85e5d5a22	income	2024-12-01 23:20:45+00		9	108
1379	e384b643-b37e-4a20-befe-0af564b086b9	income	2024-12-01 23:21:29+00		9	72
1380	7b278e21-4fb6-4afa-a9fc-628193a047f0	income	2024-12-01 23:22:40+00		9	38
1381	4edbd182-0d9d-4f4c-a7b1-ac824f980334	income	2024-12-01 23:23:24+00		9	35
1382	72c3aaef-e1a2-495b-a04d-d3a745dc5c8f	expense	2024-12-01 23:24:32+00	Crédito de $150.00 registrado.	2	38
1390	0dae2e21-500f-43c3-9991-322688426ec5	expense	2024-12-01 23:26:00+00	Crédito de $360.00 registrado.	2	90
1391	1acfa870-865f-4dae-aeab-c8e962afe469	expense	2024-12-01 23:26:01+00	Crédito de $800.00 registrado.	2	267
1392	490d6a68-ae0f-43e8-b2bd-869ea2d40cb0	income	2024-12-01 23:27:57+00		9	82
1393	2610b204-5a3a-46f2-ac46-6b7bd45cfd47	income	2024-12-01 23:29:21+00		9	110
1394	7e871c2b-1603-407d-ab36-0a47613414c0	income	2024-12-01 23:31:22+00		9	49
1395	43340af6-d673-4bf2-b794-366ca2262cfe	income	2024-12-01 23:31:56+00		9	240
1396	075322b4-b381-4fb2-8160-b48fc61aa482	income	2024-12-01 23:32:18+00		9	60
1397	0916c40a-95ce-43a2-89db-ff3d9f4f34b2	income	2024-12-01 23:33:17+00		9	63
1398	23d667f4-60cd-4931-8bcd-3e2a3715f286	income	2024-12-02 23:36:02+00		9	150
1399	7a80c0af-5cc6-4fb6-8bc8-49696a52c763	expense	2024-12-02 23:36:40+00	Crédito de $150.00 registrado.	2	104
1400	c98281c3-ec08-4a93-87c3-e7c3be49c742	expense	2024-12-02 23:37:03+00	Crédito de $140.00 registrado.	2	268
1401	39d63546-ba6a-4b44-81df-0abbaa44be67	income	2024-12-02 23:38:55+00		9	190
1402	4bbf6605-e8fe-4ccd-b601-c89325dae970	income	2024-12-02 23:39:20+00		9	214
1403	3c4389d1-ab09-4483-afd7-b95ac23c2f69	income	2024-12-02 23:40:12+00		9	176
1404	1cd4ad07-9f4b-45ac-9169-e5044e6d61d8	income	2024-12-02 23:40:43+00		9	136
1405	a16f17c4-daaa-4906-9894-ea1bad8e7a96	income	2024-12-02 23:54:54+00		9	49
1406	7a0d3b91-1829-4d3a-af94-97230a0bc4ed	income	2024-12-02 23:56:05+00		9	240
1407	c0bdc903-7e42-4e80-b8d2-6de00ef029fd	income	2024-12-02 23:57:03+00		9	186
1408	77132c8c-07af-4cf5-9f18-6f63508a9b71	income	2024-12-02 23:58:13+00		9	56
1409	ff17bff7-5fe6-4009-979e-ec5a3d04dac5	expense	2024-12-03 00:14:18+00	Crédito de $240.00 registrado.	2	56
1410	8680bd4e-8eee-4324-8c86-661ef252c30b	income	2024-12-03 00:19:00+00		9	72
1411	88616970-65bd-46a6-9b7d-89b1217f7d8b	income	2024-12-03 00:20:59+00		9	147
1412	678a8de3-97a8-4f5c-b305-634e5b9c4386	income	2024-12-06 00:21:33+00		9	161
1413	e076851e-e305-4645-a897-96e71d7f24c2	income	2024-12-03 00:22:04+00		9	103
1414	054438cd-a398-4047-b42b-14b2ae4ff064	income	2024-12-03 00:22:58+00		9	3
1415	2229e24a-df34-4731-8bb5-8bcd6a123107	income	2024-12-03 00:23:43+00		9	1
1416	077ef088-a0b6-4478-85a4-971090651c48	income	2024-12-03 00:24:31+00		9	248
1417	47ec7d35-86b7-41a2-8ab4-49296a2016a2	expense	2024-12-03 00:25:28+00	Crédito de $360.00 registrado.	2	63
1423	899ff735-a33e-4b6d-8226-07b8fec79853	expense	2024-12-03 00:26:54+00	Crédito de $130.00 registrado.	2	3
1424	0f062231-af72-4cf9-b049-00547c6adcaf	expense	2024-09-08 00:38:25+00	Crédito de $280.00 registrado.	1	52
1428	d4c5497b-8d22-45cc-85a4-80e10e0b1b78	expense	2024-09-08 00:39:58+00	Crédito de $160.00 registrado.	2	52
1443	8e8ee797-a42e-4810-b751-52927591a7e7	expense	2024-09-08 00:40:58+00	Crédito de $160.00 registrado.	2	52
1446	e5808f08-880a-48e0-b206-4b777027debc	income	2024-12-04 00:41:24+00		9	52
1447	8be7117c-882b-4d04-b7bf-89ca98bf3671	expense	2024-12-04 00:42:17+00	Crédito de $150.00 registrado.	2	230
1448	e606457d-96e7-4088-bd57-54685fae5af2	expense	2024-12-04 00:42:51+00	Crédito de $70.00 registrado.	2	218
1449	5d798d39-0fc8-40ff-a3f8-055edd9db6f4	expense	2024-12-04 00:43:33+00	Crédito de $510.00 registrado.	2	114
1450	e4bbea5e-983f-46d7-94a6-40625f10e353	expense	2024-12-04 00:44:13+00	Crédito de $1000.00 registrado.	2	171
1451	f609e5ac-eb5b-4840-b7c1-89506a935d93	income	2024-12-04 00:45:08+00		9	191
1452	5ad23246-30e3-45a1-80d1-60a186581945	income	2024-12-04 00:45:47+00		9	113
1453	fd5ad0fb-bd6b-4276-b456-9babc30fadbf	income	2024-12-04 00:46:28+00		9	116
1454	73ef0714-642d-46d3-8ac8-ac829db8f299	income	2024-12-04 00:47:00+00		9	107
1455	490fd0af-025b-47e8-8985-371b8f9229aa	income	2024-12-04 00:47:31+00		9	162
1456	6f9c43e5-8882-43d8-baea-36f61d23264e	income	2024-12-04 00:48:53+00		9	49
1457	778768c0-9dd3-4bee-8eae-b9929ff4fc6b	income	2024-12-04 00:49:24+00		9	240
1458	02ed909d-da4b-49a3-814a-f50810a07ff9	income	2024-12-05 00:51:31+00		9	170
1459	2b50fb0f-c570-4b95-a12d-b19d41946862	income	2024-12-05 00:52:09+00		9	136
1460	05e07828-221e-45fb-b67d-d5cc3d124fbf	income	2024-12-05 00:53:49+00		9	211
1461	a7c864b9-6fdb-420e-a565-30201469656e	income	2024-12-05 00:54:24+00		9	193
1462	8d36d2b9-41a1-40d2-8952-c66e116c834e	income	2024-12-05 00:54:50+00		9	250
1463	704c6000-7949-4798-9a21-f9b1783350c9	income	2024-12-05 00:56:05+00		9	186
1464	affe6c52-cc93-42ed-94bc-8164b4e34d79	income	2024-12-05 00:56:45+00		9	176
1465	33bdb8d5-d3af-4beb-bf10-09cf6b19b114	income	2024-12-05 00:57:15+00		9	49
1466	d7d2f149-a533-4201-b424-47494483e729	income	2024-12-05 00:57:50+00		9	240
1467	01d8e650-415c-451f-93a1-0c571ae2e037	expense	2024-12-05 00:58:24+00	Crédito de $140.00 registrado.	2	269
1471	9c7cf031-3d52-42aa-a62a-e1767fce9f9d	expense	2024-12-05 01:00:00+00	Crédito de $60.00 registrado.	2	121
1476	294e018c-6cb7-4db6-8718-af90fb448ad5	expense	2024-12-05 01:00:59+00	Crédito de $90.00 registrado.	2	12
1477	a3105248-3b24-4406-a6ba-511edceb9d00	expense	2024-12-05 01:01:06+00	Crédito de $50.00 registrado.	2	30
1478	6142f748-f813-4e71-8ffd-315934c43f0c	expense	2024-12-05 01:03:11+00	Crédito de $150.00 registrado.	2	270
1481	736f3f33-53d2-4675-97a0-83d6fcd35894	expense	2024-12-05 01:06:01+00	Crédito de $152.00 registrado.	2	4
1482	9a8ad2b6-f296-456f-8dca-9e5b618fd8cf	expense	2024-12-05 01:06:29+00	Crédito de $120.00 registrado.	2	103
1483	02e95ad2-cb52-46bc-891d-5859f760bf1c	income	2024-12-05 01:07:28+00		9	37
1484	0d68d968-69ac-47b7-909e-17054c35fb09	income	2024-12-05 01:08:11+00		9	139
1485	8632c6e0-7ecb-4bb3-bb0e-c6520897627a	income	2024-12-05 01:09:27+00		9	13
1486	832f2298-b393-4428-a26f-00a50080a937	expense	2024-12-05 01:10:16+00	Crédito de $140.00 registrado.	2	271
1487	3b7e957f-5d34-4640-9f49-b80016d6c240	expense	2024-12-05 01:11:32+00	Crédito de $120.00 registrado.	2	272
1488	36c2379f-58a0-44eb-874b-85d8a9dbb636	expense	2024-12-05 01:12:31+00	Crédito de $510.00 registrado.	2	83
\.


--
-- Data for Name: fintech_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_user" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "id_user", "billing_address", "address_shipping", "reference_1", "reference_2", "electronic_id", "city_id", "country_id", "document_id", "label_id", "phone_1_id", "role_id") FROM stdin;
206	Fintech123*	2024-07-24 18:38:20+00	f	FranciscoMendoza	Francisco	Mendoza		f	t	2024-07-24 18:38:08+00	24f28324-92d1-4c20-a7d6-d2b881127fac	N/A	N/A	\N	\N	\N	\N	\N	\N	23	\N	\N
2	*Finance123*	\N	f	colonvelasquez	Colon	Velasquez		f	t	2024-09-11 02:39:09+00	ad1c6270-7745-4cda-9477-902ddda4d406	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	1
1	*Finance123*	\N	f	carlosdelgado	Carlos	Delgado		f	t	2024-09-11 02:38:13+00	4011ca93-837b-42a9-9cae-77d0017f9b2a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	1
7	Fintech123*	2024-08-02 21:03:39+00	f	RamiroGuerra	Guerra			f	t	2024-08-02 21:03:19+00	d2d245cd-3ad0-422c-8484-84a0b5391a74	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
6	Fintech123*	2024-08-15 19:46:09+00	f	SeleneIbarra	Selene	Ibarra		f	t	2024-08-15 19:45:56+00	bc2d93bc-ae5c-410f-adf7-4a6d156a215d	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
244	Fintech123*	2024-11-19 00:40:46+00	f	LicethChavez	Liceth	chavez		f	t	2024-11-19 00:40:36+00	07605ccc-7a44-4eb5-9916-bb0bc2352da5	villa karola, después de super  En la ppal, casa53D	villa karola, después de super  En la ppal, casa53D	\N	\N	\N	\N	\N	\N	27	\N	\N
8	Jose360*	\N	f	JoseOjeda	José	Ojeda	joseojedagarizao@outlook.com	f	t	2024-09-11 21:14:35+00	7acf084e-0077-41c7-a98e-0bbfe1c433a7	N/A	N/A	\N	\N	\N	\N	\N	1	\N	\N	1
10	jose360+	\N	f	leonardovaldez	Leonardo	Valdez		f	t	2024-09-11 23:44:05+00	639d830b-66e4-490a-91cf-1430870131e3	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
5	Fintech123*	2024-08-31 19:44:05+00	f	SeleneNovio	Selene Ibarra			f	t	2024-09-11 19:43:31+00	a060bddf-dfff-4cdc-a3bf-1c2ebb88431e	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
207	Fintech123*	2024-10-21 18:53:30+00	f	LuisCamargo	Luis	Camargo		f	t	2024-10-21 18:53:22+00	b6557225-e7e1-4bd3-80bc-e1369adbbd16	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
209	Fintech123*	2024-10-22 23:22:03+00	f	AdanAbdielHigaldo	Adan Abdiel	Higaldo		f	t	2024-10-22 23:21:54+00	26ea96c8-ab33-46c9-ae32-0cc6560136ab	Miraflores a un costado del mini superPaloAlto	Miraflores a un costado del mini superPaloAlto	\N	\N	\N	\N	\N	\N	6	\N	\N
213	Fintech123*	2024-10-23 23:46:14+00	f	SusanaLopez	Susana	Lopez		f	t	2024-10-22 23:45:53+00	5fe9b953-d207-4202-855d-7290a9dcbda6	Santiago de Veraguas	Santiago de Veraguas	\N	\N	\N	\N	\N	\N	10	\N	\N
216	Fintech123*	2024-10-26 00:32:03+00	f	TeodoroTranquilla	Teodoro	Tranquilla		f	t	2024-10-26 00:31:55+00	475c762c-f378-4f73-9447-4e9f65955363	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
211	Fintech123*	2024-10-22 23:32:05+00	f	StefanyFernandez	Stefany	Fernandez		f	t	2024-10-22 23:31:59+00	086a3482-b02b-4c4a-8f78-f0b1dc19aceb	:Alto de la Estancia. Nuevo Mexico	:Alto de la Estancia. Nuevo Mexico	\N	\N	\N	\N	\N	\N	28	\N	\N
220	Fintech123*	2024-10-27 01:09:20+00	f	EmilethGonzales	Emileth	Gonzales		f	t	2024-10-29 01:09:15+00	0622aa75-c423-40b3-aac8-bf4a2ce116ee	N/A	N/A	\N	\N	\N	\N	\N	\N	21	\N	\N
222	Fintech123*	2024-10-18 21:41:30+00	f	LizdeMora	Liz	Mora		f	t	2024-10-18 21:41:18+00	e5bdb68a-e7ce-4373-abde-1b51f2548330	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
228	Fintech123*	2024-11-01 00:00:38+00	f	CristianJoelMendoza	Cristian joel	Mendoza		f	t	2024-11-01 00:00:31+00	2c1ba289-5ba9-4fa3-8897-319613d492da	N/A	N/A	\N	\N	\N	\N	\N	\N	29	\N	\N
230	Fintech123*	2024-11-02 20:19:20+00	f	PabloZyZ	Pablo			f	t	2024-11-02 20:19:14+00	b942e514-4754-4625-b06e-d75013fbe09c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
98	Fintech123*	2024-07-23 01:47:01+00	f	MariaTuñon	Maria	Tuñon		f	t	2024-08-23 01:46:47+00	46506b14-4669-462c-bba9-fce2fe0c0c4d	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
148	Fintech123*	2024-09-28 02:10:59+00	f	Trujillo		Trujillo		f	t	2024-09-28 02:10:58+00	8f165a9f-208e-409a-a045-d180ff5e2d46	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
227	Fintech123*	2024-07-26 23:00:40+00	f	CarlosIvanOvalle	Carlos Ivan	Ovalle		f	t	2024-07-26 23:00:29+00	ffd7f279-7e26-4279-a2b1-5e9507230fd7	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
143	Fintech123*	2024-09-26 23:41:01+00	f	JhonatanMartinez	Jhonatan	Martinez		f	t	2024-09-26 23:40:55+00	4b7ce3fc-a6c3-4f06-8c40-72572e22ee3b	B//paseo del bosque.,2da calle al final.. 2do cruce a mano iquierda/2 casa#212	B//paseo del bosque.,2da calle al final.. 2do cruce a mano iquierda/2 casa#212	\N	\N	\N	\N	\N	\N	3	\N	\N
53	Fintech123*	2024-09-05 00:59:44+00	f	JoseOrmelisArauz	Jose	Ormelis Arauz		f	t	2024-09-05 00:58:50+00	d6840af1-2c84-4a13-abfb-fb7a6cd1a1ad	N/A	N/A	\N	\N	\N	\N	\N	\N	3	\N	\N
224	Fintech123*	2024-07-31 21:59:02+00	f	AlbaCeciliaAyalaHerrera	Alba cecilia	Ayala Herrera		f	t	2024-07-31 21:58:53+00	e1f912e3-f917-4eae-bb11-b9464a8fbde2	Anton al final de la calle tercera, El Bajito	Anton al final de la calle tercera, El Bajito	\N	\N	\N	\N	\N	\N	30	\N	\N
15	Fintech123*	2024-08-01 00:15:19+00	f	LeopoldoRamos	Leopoldo	Ramos		f	t	2024-08-01 00:14:55+00	b1526115-cfad-43c5-94c3-a282cdbe901c	N/A	N/A	\N	\N	\N	\N	\N	\N	4	\N	\N
235	Fintech123*	2024-11-08 21:27:27+00	f	OmarGarcia	Omar	Garcia		f	t	2024-11-08 21:27:26+00	549b685c-9aef-4d63-8c76-40a278eaec29	juan Diaz.. Despues de la escuela. primera kta  mano derecha casa Rosada	juan Diaz.. Despues de la escuela. primera kta  mano derecha casa Rosada	\N	\N	\N	\N	\N	\N	\N	\N	\N
238	Fintech123*	2024-11-11 22:47:25+00	f	MariaGonzález	Maria	González		f	t	2024-11-20 22:47:20+00	b4acd2b2-ec36-4cf4-8290-37b335bc2291	B el ecologico 2da entrada final casa  a mano izquierda	B el ecologico 2da entrada final casa  a mano izquierda	\N	\N	\N	\N	\N	\N	\N	\N	\N
240	Fintech123*	\N	f	BelkisErickMartinez	Belkis			f	t	2024-11-20 23:45:43+00	55abbe7e-2c32-4cea-9ecb-ff2804d125d6	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
242	Fintech123*	2024-11-19 00:14:26+00	f	ClaribelTenorio	Claribel	Tenorio		f	t	2024-11-19 00:14:20+00	6dd914a7-3626-49d9-bc41-67ef8014b9d2	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
246	Fintech123*	2024-11-20 00:58:21+00	f	ArmandoDicarena	Armando	Dicarena		f	t	2024-11-22 00:58:16+00	16e83ff2-bf7b-452c-adc4-522ccbc204c0	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
248	Fintech123*	2024-11-15 22:01:27+00	f	ElvisRojas	Elvis	Rojas		f	t	2024-11-15 22:00:59+00	e85e23be-b7f4-4054-9bb9-af4dac909111	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
252	Fintech123*	2024-11-21 00:05:48+00	f	InocenteRojas	Inocente	Rojas		f	t	2024-11-27 00:05:18+00	735aaa7b-7884-452e-a187-9d49d84e6e98	Calle de la Cárcel de mujeres.. 4 casa	Calle de la Cárcel de mujeres.. 4 casa	\N	\N	\N	\N	\N	\N	\N	\N	\N
254	Fintech123*	2024-11-21 00:23:45+00	f	RaulDominguez	Raul	Dominguez		f	t	2024-11-21 00:23:41+00	0b346db6-1571-4900-a67d-4a51fa596899	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
255	Fintech123*	2024-11-21 00:25:38+00	f	RobertoAguilarRangel	Roberto	Aguilar Rangel		f	t	2024-11-27 00:25:33+00	27860942-fe55-4cb4-9911-0faa1e5a290e	En Guabas abajo av 9.sur. donde venden gas casa 1225	En Guabas abajo av 9.sur. donde venden gas casa 1225	\N	\N	\N	\N	\N	\N	\N	\N	\N
250	Fintech123*	2024-11-16 23:08:50+00	f	Jesus	Jesus			f	t	2024-11-16 23:08:46+00	9d090b8f-8d0d-473c-9420-917a699c57ec	N/A	N/A	\N	\N	\N	\N	\N	\N	35	\N	\N
256	Fintech123*	2024-11-22 01:13:36+00	f	JoseAgrazal	Jose	Agrazal		f	t	2024-11-27 01:13:30+00	02ccdf95-a300-44c9-8038-abb3401c883c	Ciruelito pnme entrando pir la iglesia casa blanca al fondo.	Ciruelito pnme entrando pir la iglesia casa blanca al fondo.	\N	\N	\N	\N	\N	\N	27	\N	\N
257	Fintech123*	2024-11-18 01:14:48+00	f	LuisAlbertoMora	Luis Alberto	Mora Castellon		f	t	2024-11-27 01:14:44+00	11b96cad-7019-4b94-87b4-33b11901ef37	sta Rosa. Barriada PuebloHetmoso	sta Rosa. Barriada PuebloHetmoso	\N	\N	\N	\N	\N	\N	27	\N	\N
9	Fintech123*	2024-09-02 21:18:45+00	f	MariaMartinez	Maria	Martinez		f	t	2024-09-02 21:18:14+00	f8b2052b-59b8-4eb5-ac19-36aaaa1ab293	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
54	Fintech123*	2024-09-05 01:03:07+00	f	MariaLuisaVillanueva	Maria Luisa	Villanueva Morales		f	t	2024-09-05 01:02:59+00	1db321c5-907d-40dd-8694-bd526591d99e	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
11	Fintech123*	2024-08-22 00:47:50+00	f	JessicaSanchez	Jessica	Sánchez		f	t	2024-09-12 00:47:23+00	f0298372-07bb-4446-b46f-d6148b2bd12b	N/A	N/A	Profesor	\N	\N	\N	\N	\N	7	\N	\N
25	Fintech123*	2024-09-12 18:52:52+00	f	JavierInadeh	Taller Mecanica			f	t	2024-09-12 18:52:48+00	2d6ed48c-f8fd-4bcd-a5de-d6ef2f0dbc66	N/A	N/A	Mecanico	\N	\N	\N	\N	\N	1	\N	\N
3	*Finance123*	\N	f	enriquefritos	Enrique			f	t	2024-09-11 02:40:40+00	935b8160-c3d0-4e4f-a0f8-45314cb619a9	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	1
52	Fintech123*	2024-09-05 00:57:23+00	f	LucianoMendoza	Luciano	Mendoza		f	t	2024-09-05 00:57:12+00	6fcbedeb-be12-4d53-a3a9-8ab2289891d1	N/A	N/A	\N	\N	\N	\N	\N	\N	23	\N	\N
4	Fintech123*	2024-09-11 19:34:07+00	f	DarioDominguez	Dario	Dominguez		f	t	2024-08-31 19:33:01+00	7a509261-cbde-4d18-b975-397a4e2d2929	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
12	Fintech123*	2024-08-31 23:53:49+00	f	ZoilaOrtega	Zoila	Ortega		f	t	2024-08-31 23:53:37+00	5083ddc3-666d-4e1d-a12d-212abfec1e66	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
13	Fintech123*	2024-07-31 23:58:51+00	f	LisbethSoto	Lisbeth	Soto		f	t	2024-07-31 23:58:42+00	fe5c2f2b-3c55-47d2-be14-1da77a65685a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
14	Fintech123*	\N	f	JorgeGonzales	Jorge	Gonzales		f	t	2024-08-01 00:08:12+00	826fb131-868f-44bb-9e95-f5549ccae58a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
16	Fintech123*	2024-08-02 00:23:32+00	f	MereidaRodriguez	Mereida	Rodríguez		f	t	2024-08-02 00:21:14+00	be861fb4-3a0c-45d1-8f26-0ce571515013	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
17	Fintech123*	2024-08-02 00:25:04+00	f	EliaRosa	Elia	Gordon		f	t	2024-08-02 00:24:43+00	06963e29-a015-417a-8748-c0d3c5043475	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
23	Fintech123*	2024-08-03 01:20:46+00	f	JuanMendoza	Juan	Mendoza		f	t	2024-08-03 01:19:51+00	747c2f45-f9a4-410e-87ef-63b55fb23400	N/A	N/A	\N	\N	\N	\N	\N	\N	23	\N	\N
19	Fintech123*	2024-08-02 00:31:28+00	f	MaricelEsther	Maricel	Pinzón		f	t	2024-08-02 00:31:16+00	5f84e22a-959c-4590-8d87-3978d2fc4c34	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
20	Fintech123*	2024-08-03 01:08:47+00	f	OscarIvanMojica	Oscar	Mojica		f	t	2024-08-03 01:08:39+00	75195b95-52e8-478c-9290-c8d982a69463	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
60	Fintech123*	2024-09-03 01:28:50+00	f	JeisonOvidioGonzalez	Jeison	Oviedo Gonzales		f	t	2024-09-03 01:28:45+00	d964bf93-8d00-4f48-897f-0b7f17da992d	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
26	Fintech123*	2024-09-12 21:06:30+00	f	MaxMoreno	Max	Moreno		f	t	2024-09-12 21:06:03+00	142ff179-bc06-4eed-935f-c6bd98ca818e	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
21	Fintech123*	2024-08-03 01:14:13+00	f	Magdaxtra	Magda			f	t	2024-08-03 01:13:38+00	af60439b-47c7-4b89-b239-d5a9203674f4	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
78	Fintech123*	2024-08-15 22:51:17+00	f	JoséSamuelQuiroz	José Samue	Quiroz		f	t	2024-08-15 22:51:05+00	4cf85d6a-f339-4290-ad6c-b1dd25d7e533	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
74	Fintech123*	2024-08-13 21:22:39+00	f	ElianysMora	Elianys	Mora		f	t	2024-08-13 21:22:14+00	a9a8404e-4f94-40c6-ac33-9f9a945b98e7	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
30	Fintech123*	2024-09-12 21:12:43+00	f	AlbertoArocemena	Alberto	Arosemena		f	t	2024-09-12 21:12:04+00	86ac7107-2968-4730-9e77-cdfce43a1381	sector del Machetazo	sector del Machetazo	\N	\N	\N	\N	\N	\N	\N	\N	\N
210	Fintech123*	2024-10-22 23:29:37+00	f	SebastianCervantes	Sebastian	Cervantes Pinzon		f	t	2024-10-22 23:29:10+00	94a8b133-3976-4337-ad86-bb0e98d56a36	Aguadulce calle Veragua	Aguadulce calle Veragua	Profesor	\N	\N	\N	\N	\N	1	\N	\N
40	Fintech123*	2024-09-07 22:47:41+00	f	Lazaro	Lazaro	Profesor		f	t	2024-09-07 22:47:34+00	62548815-8550-47cb-b616-cdb1d5b9207f	N/A	N/A	Profesor	\N	\N	\N	\N	\N	15	\N	\N
18	Fintech123*	2024-08-02 00:29:02+00	f	MaximinoMartinez	Maximinio	Martinez		f	t	2024-08-02 00:28:59+00	aeb391e6-e778-4de1-bd60-33ada3374259	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
31	Fintech123*	2024-09-11 21:19:58+00	f	EnockGuerra	Enock	Guerra		f	t	2024-09-11 21:19:52+00	4e6c2e70-b345-4570-97fa-892b7d133a85	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
36	Fintech123*	2024-09-10 21:28:12+00	f	EdnaZulema	Edna	Moreno		f	t	2024-09-10 21:28:11+00	7d9e9b60-66b4-4c71-982f-68245dd8166c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
37	Fintech123*	2024-09-10 21:29:29+00	f	NoelRodriguez	Noel	Rodriguez		f	t	2024-09-10 21:29:25+00	802427c1-1563-4b8e-af81-2684f0fa6de5	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
38	Fintech123*	2024-09-08 22:42:53+00	f	ReinaldoVasquez	Reinaldo	Vasquez		f	t	2024-09-08 22:42:46+00	5e197660-27a9-4a1b-8e6c-44589f2b9365	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
29	Fintech123*	2024-09-12 21:11:09+00	f	TomasAlbertoMartinez	Tomas	Martinez		f	t	2024-09-12 21:11:04+00	e22989e8-1fb1-452c-ba4b-874977dea421	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
24	Fintech123*	2024-09-12 18:49:57+00	f	LuisGonzales	Luis	Gonzales		f	t	2024-09-12 18:49:36+00	98b18289-ca45-4d26-bccf-6d53a3b74751	N/A	N/A	Trabajos varios	\N	\N	\N	\N	\N	17	\N	\N
41	Fintech123*	2024-09-06 22:52:53+00	f	LiceidaMartinez	Liceida	Martinez		f	t	2024-09-06 22:52:49+00	5daf1e46-235e-4a2f-b2cc-4770871f3652	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
42	Fintech123*	2024-09-06 22:54:27+00	f	MariamTrejos	Mariam	Trejos		f	t	2024-09-06 22:54:22+00	001e8131-b3b3-452c-a46a-eaf6e54f3b7b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
39	Fintech123*	2024-09-08 22:44:36+00	f	MichelAntonio	Michael	Sánchez		f	t	2024-09-08 22:44:29+00	95008006-e450-40de-9ca5-8fbe599e7b9f	N/A	N/A	\N	\N	\N	\N	\N	\N	4	\N	\N
44	Fintech123*	2024-09-06 22:57:51+00	f	GenaroRodriguez	Genaro	Rodríguez		f	t	2024-09-06 22:57:46+00	19068da1-dbd4-4bcf-b640-44e667d05ec2	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
45	Fintech123*	2024-09-06 22:58:52+00	f	OlmedoAlexy	Olmedo	Alex		f	t	2024-09-06 22:58:43+00	decdf27f-3973-44f1-875b-0a1a417305a4	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
46	Fintech123*	2024-09-05 23:06:08+00	f	JosephTrujillo	Joseph	Trujillo		f	t	2024-09-05 23:05:58+00	233c4243-dbc7-4100-9840-db2614e3421e	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
47	Fintech123*	2024-09-05 23:07:09+00	f	NildaSanchez	Nilda	Sánchez		f	t	2024-09-05 23:07:06+00	775cbbb7-6002-4fe8-bd7a-3014eec2e1d0	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
48	Fintech123*	2024-09-05 23:09:16+00	f	JavierArosemena	Javier	Arosemena		f	t	2024-09-05 23:09:13+00	88923d73-211a-4ab7-8c36-df02c1c4ec75	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
49	Fintech123*	2024-08-09 23:30:12+00	f	ErickMartinez	Erick	Martinez		f	t	2024-08-09 23:29:52+00	4e8b180d-5a77-4ee3-9cca-431fbc8f0497	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
50	Fintech123*	2024-08-06 23:38:13+00	f	IrisdelCarmen	Iris	Del Carmen		f	t	2024-08-06 23:38:06+00	f17a0786-00e2-429f-b683-6a0d2c9481b7	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
35	Fintech123*	2024-09-10 21:27:02+00	f	IdaniaBernalRuiz	Idania	Bernal Ruiz		f	t	2024-09-10 21:26:14+00	9980b067-79fa-4028-a061-3b4c9ca45743	en las Guias	en las Guias	\N	\N	\N	\N	\N	\N	\N	\N	\N
55	Fintech123*	2024-09-04 01:18:07+00	f	WuendyRangel	Wuendy	Rangel		f	t	2024-09-04 01:18:00+00	883cbd94-3f57-48b3-bf7f-d39d2773743b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
56	Fintech123*	2024-09-04 01:19:21+00	f	BiancaCoronado	Bianca	Coronado		f	t	2024-09-04 01:19:10+00	489f5b3c-e4bf-4baa-b10e-421a2f650149	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
63	Fintech123*	2024-09-03 01:33:05+00	f	JorgeReyes	Jorge	Reyes Paquetero		f	t	2024-09-03 01:32:57+00	77f5668e-e0e2-4737-a677-f16f9c6302a6	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
64	Fintech123*	2024-09-03 01:34:33+00	f	RogelioCorro	Rogelio	Corro		f	t	2024-09-03 01:34:28+00	79bb0eec-567b-458a-8985-bac1af42c872	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
65	Fintech123*	2024-09-03 01:36:26+00	f	MariamDelosAngeles	Mariam	DelosAngeles		f	t	2024-09-03 01:36:21+00	8644c8d5-ddc8-43aa-9733-be45fc633d08	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
67	Fintech123*	2024-08-09 17:59:38+00	f	FernandoMorales	Fernando	Morales		f	t	2024-08-09 17:59:09+00	1a03d4a2-576e-4385-bffd-0b7a9965bd6e	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
68	Fintech123*	2024-08-09 18:01:00+00	f	AlejandroPinto	Alejandro	Pinto		f	t	2024-08-09 18:00:55+00	45310725-e5c1-428a-9d70-008535723865	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
69	Fintech123*	2024-08-11 18:14:04+00	f	ReinaldoAlto	Reinaldo	Alto		f	t	2024-08-11 18:07:17+00	00dbfe32-6119-4a2c-a391-c7c2132aa2e6	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
70	Fintech123*	2024-08-12 19:52:27+00	f	CarlosMeneses	Carlos	Meneses		f	t	2024-08-12 19:52:19+00	374751ac-5dad-4a3c-8d4b-eeaa8ba29ac1	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
72	Fintech123*	2024-08-13 20:02:44+00	f	JhonnyReyes	Jhonny	Reyes		f	t	2024-08-13 20:02:35+00	3767700a-398e-4390-9742-bf3bd675ee74	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
77	Fintech123*	2024-08-15 22:49:40+00	f	EfrainMora	Efrain	Mora		f	t	2024-08-15 22:49:35+00	e6ed96d1-9299-449c-8bac-e39f3f6fafc1	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
57	Fintech123*	2024-09-04 01:21:20+00	f	SantanaPanaderia	Santana	Panaderia		f	t	2024-09-04 01:21:15+00	15ea5b29-84fe-448d-9eee-2bbc60fbc990	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
62	Fintech123*	2024-09-03 01:31:53+00	f	CarlosArturoArauz	Carlos Arturo	Arauz		f	t	2024-09-03 01:31:49+00	97cc562f-ccaf-463d-88c2-ad29733e8382	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
43	Fintech123*	2024-09-06 22:56:34+00	f	ClementinaPerez	Clementina	Pérez		f	t	2024-09-06 22:56:29+00	98dd0df3-cb1e-4044-b94a-abc72dbb8fea	N/A	N/A	Profesor	\N	\N	\N	\N	\N	9	\N	\N
66	Fintech123*	2024-09-13 17:55:45+00	f	IgnacioVega	Ignacio	Vega		f	t	2024-09-13 17:55:41+00	f20b27f5-75fe-476e-8f75-751a2523acf7	N/A	N/A	Profesor	\N	\N	\N	\N	\N	10	\N	\N
28	Fintech123*	2024-09-12 21:09:31+00	f	EliecerInadeh	Eliecer			f	t	2024-09-12 21:09:27+00	79960da8-da19-44ed-8624-f73a9e00a7e9	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
61	Fintech123*	2024-09-03 01:30:05+00	f	AlvaroAlexis	Alvaro Alexis	Navas		f	t	2024-09-03 01:29:56+00	04524dd4-ab2d-4716-b93e-158586d7572a	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
32	Fintech123*	2024-09-11 21:21:00+00	f	GladysMontero	Gladys	Montero		f	t	2024-09-11 21:20:57+00	3756984f-84fe-4043-93da-370fdb46bbda	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
58	Fintech123*	2024-09-04 01:22:15+00	f	MarinaMoreno	Marina	Moreno		f	t	2024-09-04 01:22:09+00	e8ea58cc-4fb8-4f0a-bab4-c199ca415d94	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
76	Fintech123*	2024-08-14 22:08:48+00	f	YesibethIbarra	Yesibeth	Ibarra		f	t	2024-08-14 22:08:41+00	f3aedfb8-cc76-43ca-8bee-ab6a21e46fb4	N/A	N/A	\N	\N	\N	\N	\N	\N	13	\N	\N
71	Fintech123*	2024-08-13 19:57:56+00	f	ErickMagallon	Erick	Magallon		f	t	2024-08-13 19:57:42+00	6cdf3428-4952-41fb-8ced-210f67c7e473	N/A	N/A	Profesor	\N	\N	\N	\N	\N	15	\N	\N
59	Fintech123*	2024-09-03 01:26:36+00	f	Ubaldo	Ubaldo	Unal		f	t	2024-09-03 01:26:31+00	174df0b4-faf7-4f57-8c0c-27f34968a280	N/A	N/A	Gestor de aire acondicionado	\N	\N	\N	\N	\N	17	\N	\N
34	Fintech123*	2024-09-10 21:24:55+00	f	SimonaDominguez	Simona	Dominguez		f	t	2024-09-13 21:24:46+00	0b5226ad-c8fc-46c0-bed7-1516b3e19ea7	Ecologico de pnme	Ecologico de pnme	\N	\N	\N	\N	\N	\N	20	\N	\N
33	Fintech123*	2024-09-10 21:22:19+00	f	CesarHernandez	Cesar	Hernandez		f	t	2024-09-11 21:21:49+00	367e5256-ded3-4c28-9a22-de5dd3c1a45c	N/A	N/A	Odontologo	\N	\N	\N	\N	\N	22	\N	\N
125	Fintech123*	2024-09-18 22:32:05+00	f	MariaKarlaRivera	Maria Karla	Rivera		f	t	2024-09-18 22:31:53+00	366d9246-306a-4ad8-aa94-03ad10525b73	N/A	N/A	\N	\N	\N	\N	\N	\N	23	\N	\N
113	Fintech123*	2024-07-17 00:29:17+00	f	AdbasadierAbisalMatatan	Adbasadier	Abisal Aguilar		f	t	2024-08-17 00:28:35+00	da3f21b6-0cda-40f3-8eab-e4668be04af1	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
81	Fintech123*	2024-09-13 23:50:20+00	f	JhonatanSegundo	Jhonatan	Segundo		f	t	2024-09-13 23:50:18+00	93db799c-bcde-4901-a52d-2403dd5fb51b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
82	Fintech123*	2024-09-14 00:01:23+00	f	ManuelSanchez	Manuel	Sanchez		f	t	2024-09-14 00:01:17+00	491e71ce-80b2-4116-bc7b-937349f8d9d2	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
83	Fintech123*	2024-09-14 00:05:07+00	f	OmairaCuava	Omaira	Cuava		f	t	2024-09-14 00:05:06+00	a6062aea-6d3d-4a4b-9c7b-d6980b249ac7	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
110	Fintech123*	2024-09-17 00:06:02+00	f	BelisarioRodriguez	Belisario	Rodriguez		f	t	2024-09-17 00:05:55+00	bd7afdb3-5e88-4014-b545-401587a633be	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
85	Fintech123*	2024-08-17 00:23:35+00	f	DanitzaAguilar	Danitza	Aguilar		f	t	2024-08-17 00:23:32+00	76bffdcf-27c4-43ca-8cd9-dc3028b94a48	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
114	Fintech123*	2024-09-17 19:06:58+00	f	LeydiamSilveraPanaderia	Leidyam	Silvera		f	t	2024-09-17 19:05:21+00	a7df0d73-b6ad-4fd3-af05-c9e1d1b6a555	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
89	Fintech123*	2024-08-18 00:45:24+00	f	NicolasMeneses	Nicolas	Meneses		f	t	2024-08-18 00:43:31+00	9dbdda2c-6231-467e-b5e5-2cc989b2310d	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
90	Fintech123*	2024-08-18 00:46:26+00	f	GeidyDominguez	Geidy	Dominguez		f	t	2024-08-18 00:45:52+00	febcf296-c55e-44ad-ba90-ed1e4ebbe8d4	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
91	Fintech123*	2024-08-18 00:57:07+00	f	AuraSotiyo	Aura	Sotiyo		f	t	2024-08-18 00:56:57+00	0dda6a35-7dcb-4b06-9e8d-fe193ba86ce1	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
92	Fintech123*	2024-08-20 01:11:34+00	f	JaiberBusito	Jaiber	Busito		f	t	2024-08-20 01:11:26+00	4943ea1a-ef64-4771-9779-d66007249ba6	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
93	Fintech123*	2024-08-20 01:17:03+00	f	PublioProfe	Publio	Ojo		f	t	2024-08-20 01:16:53+00	33e0b9fa-27f6-44a9-a86c-119524d8b301	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
95	Fintech123*	2024-08-21 01:21:35+00	f	GabrielaGuerrero	Gabriela	Guerrero		f	t	2024-08-21 01:21:25+00	460d6de8-f004-45a1-a603-e116fbea9e69	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
96	Fintech123*	2024-08-21 01:42:05+00	f	CompañerodeNelson	CompañerodeNelson			f	t	2024-08-21 01:39:54+00	be6e3ea5-d80b-4011-8ba6-f48f12ca71a5	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
97	Fintech123*	2024-08-22 01:43:26+00	f	AristidesMartinez	Aristides	Martinez		f	t	2024-08-22 01:43:15+00	5312083f-10e2-43c2-8d44-113a73afe05a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
99	Fintech123*	2024-08-23 01:48:38+00	f	ChristianDomínguez	Christian	Domínguez		f	t	2024-08-23 01:48:23+00	7a7259a5-f726-440d-bb6d-1c620282fe33	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
100	Fintech123*	2024-08-23 01:49:28+00	f	GladysPerez	Gladys	Perez		f	t	2024-08-23 01:49:21+00	2bc46ae0-1fe3-4f3a-9265-851092445ccf	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
101	Fintech123*	2024-08-24 01:51:45+00	f	IndiraSanchez	Indira	Sanchez		f	t	2024-08-24 01:51:35+00	921fed09-e344-4e0c-8f94-9d4d9dc376cb	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
87	Fintech123*	2024-08-18 00:39:24+00	f	JhonatanAguilar	Jhonatan	Aguilar		f	t	2024-08-18 00:38:32+00	ac767a1a-09e4-4cf0-9ef7-3bfed9867ed6	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
102	Fintech123*	2024-09-14 22:07:08+00	f	ChristianDominguez	Christian	Dominguez		f	t	2024-09-14 22:07:04+00	44941f17-1e59-4839-9cbe-ece2ab7f1d5c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
103	Fintech123*	2024-09-14 22:30:02+00	f	JorgeCamel	Jorge	Camel		f	t	2024-09-14 22:29:58+00	75b904dd-da8b-456b-844d-43e41490c125	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
105	Fintech123*	2024-09-15 23:24:58+00	f	Elcutty	El cutty			f	t	2024-09-15 23:24:52+00	046cb6e3-89a7-481b-b3fe-e94e41a92811	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
106	Fintech123*	2024-08-15 23:41:10+00	f	ElizabethVayVen	Elizabeth			f	t	2024-08-15 23:41:02+00	37285fdc-7f23-471b-8c1a-5d0085776854	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
107	Fintech123*	2024-09-16 23:56:40+00	f	DelfinaReyes	Delfina	Reyes		f	t	2024-09-16 23:56:35+00	a9a7f1aa-d4a3-4c58-97de-81b40272d7f4	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
108	Fintech123*	2024-09-17 00:02:28+00	f	JuanAguilar	Juan	Aguilar		f	t	2024-09-17 00:02:22+00	7572fa72-90b5-4137-b39a-842479264d45	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
109	Fintech123*	2024-09-17 00:03:34+00	f	CesarRodriguez	Cesar	Rodriguez		f	t	2024-09-17 00:03:28+00	0e54e02a-18d4-4e11-b974-9d571293ac18	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
111	Fintech123*	2024-09-17 00:09:17+00	f	CarlosKike	Carlos	Kike		f	t	2024-09-17 00:09:12+00	4f9465d2-612e-427f-a9a1-5a67abde4c4c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
112	Fintech123*	2024-09-17 00:25:12+00	f	ErwuinMartinez	Erwuin	Martinez		f	t	2024-08-31 00:25:05+00	2803b507-0f55-4999-b8e9-0b365c34d12c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
115	Fintech123*	2024-09-17 19:16:57+00	f	YarisnethCárdenas	Yarisneth	Cárdenas		f	t	2024-09-17 19:16:53+00	260e3707-729a-4237-9b00-ce9df00cb9fe	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
116	Fintech123*	2024-09-17 19:43:59+00	f	Bernabethaguilar	Bernabeth	Aguilar Reyes		f	t	2024-09-17 19:43:54+00	005abe6e-b212-4a24-8f4d-aeeaf4b628c7	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
117	Fintech123*	2024-09-17 19:48:55+00	f	EliasPérez	Elias	Pérez		f	t	2024-09-17 19:48:50+00	90d7c700-02bc-4812-9914-b6570409d164	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
118	Fintech123*	2023-12-18 23:41:43+00	f	JamilethDominguez	Jamileth	Dominguez		f	t	2023-12-18 23:37:38+00	677932ab-1c07-4e0a-953d-81db52862c70	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
120	Fintech123*	2024-04-11 18:29:14+00	f	VictorExtar	Victor	Super Extra		f	t	2024-04-11 18:28:58+00	c228984b-075e-4d86-a25b-2968d5afbf1d	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
104	Fintech123*	2024-09-15 23:24:06+00	f	ArielHernandez	Ariel	Hernandez		f	t	2024-09-15 23:23:38+00	c10d1fdc-04ba-4cb6-b340-a7b3416a099a	N/A	N/A	\N	\N	\N	\N	\N	\N	26	\N	\N
122	Fintech123*	2024-06-03 20:13:33+00	f	Lidia	Lidia			f	t	2024-06-03 20:13:24+00	169448c4-2760-4063-804c-6be4e6932512	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
214	Fintech123*	2024-10-23 23:48:42+00	f	RogerMoreno	Roger	Moreno		f	t	2024-10-27 23:48:23+00	b4e37990-726d-4037-b7cf-43edaba99481	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
218	Fintech123*	2024-10-27 01:02:00+00	f	MagalyMaxwell	Magaly	Maxwell		f	t	2024-10-27 01:01:55+00	9df2422a-0490-4b06-88fa-a542e01c7362	N/A	N/A	\N	\N	\N	\N	\N	\N	15	\N	\N
127	Fintech123*	2024-07-16 22:42:03+00	f	MariaIsidora	Maria Isidora	Barria		f	t	2024-07-16 22:41:46+00	0ac03e32-231f-4747-b658-8b8ed6de07e4	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
128	Fintech123*	2024-09-18 22:52:25+00	f	LuisGomez	Luis	Gomez		f	t	2024-09-18 22:52:19+00	decb2db8-983e-4c89-962e-f9b3a01e39f5	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
94	Fintech123*	2024-08-21 01:19:32+00	f	JoseSanchez	Jose	Sanchez		f	t	2024-08-21 01:19:28+00	affead89-c296-4e94-ad73-f98a8589cda6	N/A	N/A	\N	\N	\N	\N	\N	\N	3	\N	\N
130	Fintech123*	2024-09-20 21:12:21+00	f	EsposaJoseSanchez	EsposaJose	Sanchez		f	t	2024-09-20 21:12:16+00	2fc79314-f10c-4eb6-a5cb-b9e895b26700	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
131	Fintech123*	2024-07-19 18:33:40+00	f	OmeidaJubilada	Omeida			f	t	2024-07-19 18:33:21+00	dd60d93b-5130-4134-92fc-5fd46f841f8a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
132	Fintech123*	2024-09-22 19:23:47+00	f	OrielBanismo	Oriel	Banismo		f	t	2024-09-22 19:23:32+00	4b637bac-7cab-42ea-a231-5d68e3063626	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
134	Fintech123*	2024-09-22 19:33:31+00	f	EdgardomurilloAmigogustavo	Edgardo	Murillo		f	t	2024-09-22 19:33:24+00	a06c4e2c-deb5-4adf-b4a7-d5e105376d18	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
133	Fintech123*	2024-09-22 19:24:51+00	f	EdgardoMurillo	Edgardo	Murillo		f	t	2024-09-22 19:24:40+00	d7166fd7-ccce-4ce1-bbd7-203a120b19b7	N/A	N/A	\N	\N	\N	\N	\N	\N	4	\N	\N
188	Fintech123*	2024-09-09 23:40:38+00	f	JuanZyZ	Juan			f	t	2024-09-09 23:40:34+00	cf1480d0-de32-48b5-ac0d-d7ed33c4fd53	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
121	Fintech123*	2024-08-19 20:10:20+00	f	MorrisProfesor	Morris			f	t	2024-08-19 20:10:09+00	9d41ccea-6e52-4a46-8648-0875e1b4d1ed	N/A	N/A	Profesor	\N	\N	\N	\N	\N	1	\N	\N
119	Fintech123*	2024-05-02 00:51:48+00	f	MaximilianoMoreno	Maximiliano	Moreno		f	t	2024-05-02 00:51:22+00	8259a4fc-ddf7-41a8-bd2e-5985f2c2a85d	N/A	N/A	Profesor	\N	\N	\N	\N	\N	1	\N	\N
84	Fintech123*	2024-08-18 00:22:21+00	f	MiguelOrdoñez	Miguel	Ordoñez		f	t	2024-08-17 00:22:14+00	34a5d7f3-3eaf-4fb0-9f54-80ab642d4541	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
79	Fintech123*	2024-09-13 23:44:37+00	f	AndysMartinez	Andys	Martinez		f	t	2024-09-13 23:44:33+00	6898ca35-7366-4005-a65c-26c6c46036ad	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
80	Fintech123*	2024-09-13 23:49:36+00	f	MarioBetancur	Mario	Betancur		f	t	2024-09-13 23:49:11+00	b6d512f3-9ae8-4cd7-b017-4d14e30855c5	N/A	N/A	Profesor	\N	\N	\N	\N	\N	15	\N	\N
123	Fintech123*	2024-08-17 20:26:38+00	f	GemaGonzález	Gema	González		f	t	2024-08-17 20:26:29+00	dd0eb228-e577-4ab1-98f4-4220eb009706	N/A	N/A	Profesor	\N	\N	\N	\N	\N	16	\N	\N
135	Fintech123*	2024-07-04 00:15:28+00	f	ArisGonzales	Aris	Gonzales		f	t	2024-07-04 00:15:17+00	cf30a287-c177-49d1-9827-19a51f71a368	N/A	N/A	\N	\N	\N	\N	\N	\N	21	\N	\N
86	Fintech123*	2024-08-18 00:34:43+00	f	DalvisMendoza	Dalvis	Mendoza		f	t	2024-08-18 00:34:19+00	3a0476da-5fc3-456d-a8f2-44c04a991a65	N/A	N/A	\N	\N	\N	\N	\N	\N	23	\N	\N
88	Fintech123*	2024-08-18 00:41:41+00	f	OscarAlbertoArauz	Oscar Alberto	Arauz		f	t	2024-08-18 00:41:36+00	08829b31-a248-43fe-982e-49da8e476978	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
136	Fintech123*	2024-07-25 00:27:40+00	f	EleuterioDelrosarioTello	Eleuterio	Delrosario Tello		f	t	2024-07-25 00:27:26+00	132fd9c9-31fb-42f4-a368-384d062dd0a2	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
137	Fintech123*	2024-09-24 18:58:10+00	f	JoseEnriqueVillanueva	Jose Enrique	Villanueva		f	t	2024-09-24 18:57:48+00	3c212e76-ff53-4a32-82b8-de6188c845a6	El ciruelito de Anton 2 casa detra de la ferreteria san juan	El ciruelito de Anton 2 casa detra de la ferreteria san juan	\N	\N	\N	\N	\N	\N	\N	\N	\N
138	Fintech123*	2024-09-24 18:59:20+00	f	MarioMoreno	Mario	Moreno		f	t	2024-09-24 18:59:17+00	bc8f79e3-2d02-4d37-85fe-3271b3e14f3c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
171	Fintech123*	2024-10-06 00:16:01+00	f	AlvaroGonzalezGomez	Alvaro	Gonzale Gomez		f	t	2024-10-06 00:15:35+00	139a8133-a024-49f5-8c6f-d4d514114c93	Vive en :B. Las Lomas. 2do super	Vive en :B. Las Lomas. 2do super	\N	\N	\N	\N	\N	\N	5	\N	\N
185	Fintech123*	2024-10-10 22:06:55+00	f	JhoannaAguilar	Jhoanna	Aguilar		f	t	2024-10-23 22:06:46+00	aa00685d-b538-4adc-ae69-7fb4262f68ae	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
141	Fintech123*	2024-07-28 23:24:57+00	f	LazaroAgustiniani	Lazaro	Agustiniani		f	t	2024-07-28 23:22:48+00	dc181281-2445-40a2-b069-616d2e938169	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
149	Fintech123*	2024-09-29 02:25:38+00	f	KisilMarketAnton	Kisil			f	t	2024-09-28 02:25:37+00	ab4996fb-beab-494c-9a62-e77ff3c3d634	N/A	N/A	\N	\N	\N	\N	\N	\N	24	\N	\N
172	Fintech123*	\N	f	LuisGomezSupercocle	Luis	Gómez		f	t	2024-09-03 00:31:18+00	5fc9b6e0-6697-45ff-bc3c-ed4660fe3d3e	N/A	N/A	\N	\N	\N	\N	\N	\N	25	\N	\N
153	Fintech123*	2024-10-01 03:02:37+00	f	ANYSANADELKAGONZALEZ	ANYS ANADELKA	ANADELKA GONZALEZ		f	t	2024-10-01 03:02:33+00	e54ea444-6c5e-4c5b-972b-2d18b6802fff	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
146	Fintech123*	2024-06-29 00:39:34+00	f	GregorioRodriguez	Gregorio	Rodriguez		f	t	2024-06-29 00:13:37+00	c81ff401-1663-4dcc-97f5-0ff01f48e9e5	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
147	Fintech123*	2024-09-28 02:09:53+00	f	RicardoPerez	Ricardo	Perez Larry		f	t	2024-10-04 02:09:44+00	a6ced73e-bae7-494b-8959-186a7c43bcae	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
150	Fintech123*	2024-10-01 02:34:06+00	f	CatalinaMartinez	Catalina	Martinez		f	t	2024-10-01 02:34:04+00	92e78805-73e7-4c13-808b-9c607c251c23	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
151	Fintech123*	2024-10-01 02:52:40+00	f	JoseRicaute	Jose	Ricaute		f	t	2024-10-01 02:52:14+00	6c96f01e-28df-4cca-ae54-b53c8ea17846	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
154	Fintech123*	2024-10-01 03:03:38+00	f	YolandaArosemena	YOLANDA	AROSEMENA		f	t	2024-10-01 03:03:37+00	decffb8c-fb57-4f4e-9283-7a9ebf2ba4ef	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
155	Fintech123*	2024-08-26 03:06:36+00	f	EvelioRodriguez	Evelio	Rodriguez		f	t	2024-08-26 03:06:28+00	2302ce71-584f-49d7-bfa0-e8866b587baa	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
156	Fintech123*	2024-10-01 23:11:37+00	f	AngelTorres	Angel	Torres		f	t	2024-10-01 23:11:22+00	c114e7b5-a5a4-49c4-9e1c-53151f0255d6	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
158	Fintech123*	2024-10-01 23:19:23+00	f	RafaelGonzalez	Rafael	Gonzales		f	t	2024-10-01 23:19:16+00	36419b32-0bc5-49a5-9e6b-055de8807e3c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
159	Fintech123*	2024-10-01 23:21:42+00	f	MiguelArquiñez	Miguel	Arquiñez		f	t	2024-10-01 23:21:35+00	870188cd-0dcd-49c0-9add-ee45c2e10cb2	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
215	Fintech123*	2024-10-25 00:00:15+00	f	DIXGSANIATORRES	DIXGSANIA	TORRES		f	t	2024-10-25 00:00:10+00	37d1698a-831b-4faa-9631-0f4e34c04492	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
161	Fintech123*	2024-10-03 23:22:31+00	f	DaniDaniel	Daniel			f	t	2024-10-03 23:22:23+00	f79cb011-058e-4179-af6a-044609051206	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
162	Fintech123*	2024-10-03 23:24:22+00	f	CristianAlexanderGonzales	Cristian Alexander	Gonzales		f	t	2024-10-03 23:24:14+00	bcb16495-4e55-49d2-90d2-7c84cfa08dfe	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
163	Fintech123*	2024-10-03 23:26:00+00	f	YamiscellyAguilar	Yamiscelly	Aguilar		f	t	2024-10-03 23:25:53+00	edf06e1d-0997-46b5-b0bc-8e5abc73da48	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
165	Fintech123*	2024-10-04 16:24:55+00	f	RogelioTuñon	Rogelio	Tuñon		f	t	2024-07-05 16:24:48+00	539d0cce-27a2-40bd-9848-d42089c9f099	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
167	Fintech123*	2024-10-06 00:04:46+00	f	YennyGonzalesPerez	YENNY	GONZALEZ PEREZ		f	t	2024-10-18 00:05:24+00	0b810d33-3cf7-433e-8248-2a447c5f74f1	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
169	Fintech123*	2024-10-06 00:08:51+00	f	LuisArmandoDominguezPerez	LUIS ARMANDO	DOMINGUEZ PEREZ		f	t	2024-10-18 00:09:27+00	1924aadc-840e-4d73-8a4f-d6503cd8568b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
170	Fintech123*	2024-10-07 00:12:06+00	f	VictoriaCastroRojo	Victoria	Castro Rojo		f	t	2024-10-18 00:12:00+00	ae5d81e1-457a-4d5e-94e6-ed1057f82463	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
174	Fintech123*	2024-07-27 00:47:56+00	f	JuanPabloPanadero	Juan Pablo			f	t	2024-10-18 00:48:12+00	364877e8-b59f-4e07-a07b-bb27c0021e1b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
175	Fintech123*	2024-10-09 00:51:47+00	f	NildaSanchezHijo	Nilda	Sanchez		f	t	2024-10-18 00:52:25+00	e350d5c5-5777-49a6-adae-80207787004d	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
157	Fintech123*	2024-10-01 23:13:13+00	f	JavierEscobarMecanico	Javier	Escobar		f	t	2024-10-01 23:13:04+00	e1b11841-020e-4129-b4ae-05ceca5bae0e	N/A	N/A	Profesor	\N	\N	\N	\N	\N	1	\N	\N
177	Fintech123*	2024-10-11 22:53:50+00	f	OrdoñezSr		Ordoñez		f	t	2024-10-11 22:54:33+00	788b7911-3209-4826-ab99-b48a46126e02	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
179	Fintech123*	2024-10-14 23:30:08+00	f	AndysBarrera	Andys	Barrera		f	t	2024-10-14 23:30:51+00	05596097-11b8-49bb-a1fd-4aefde47cfba	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
180	Fintech123*	2024-10-14 23:30:51+00	f	IdaniaBernal	Idania	Bernal		f	t	2024-10-14 23:31:35+00	1aad9695-0060-48bc-8d43-b8de404a9e02	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
181	Fintech123*	2024-07-04 01:15:01+00	f	CarlosRangel	Carlos	Rangel		f	t	2024-10-21 01:14:41+00	1fca5429-825b-4687-a021-b3a3b3b117b5	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
182	Fintech123*	2024-08-31 01:16:01+00	f	IsisRodriguez	Isis	Rodriguez		f	t	2024-08-31 01:15:50+00	85c7a239-9674-40b4-8aa2-3579dde80545	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
184	Fintech123*	2024-10-06 22:02:18+00	f	MiriamTrejos	Miriam	Trejos		f	t	2024-10-23 22:02:11+00	073aaab6-dd53-4303-9c18-ec3070debe50	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
186	Fintech123*	2024-10-12 22:10:14+00	f	OscarEmilioMojica	Oscar Emilio	Mojica		f	t	2024-10-12 22:10:00+00	e17e4e8e-03b2-4203-b9a6-a6c9117fcb43	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
139	Fintech123*	2024-09-24 19:00:30+00	f	ElizabethJubilada	Elizabeth			f	t	2024-09-24 19:00:22+00	395f712e-1b98-4704-8861-77c1433c59c3	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
187	Fintech123*	2024-09-17 23:11:46+00	f	ZulemaMoreno	Zulema	Moreno		f	t	2024-09-17 23:11:37+00	8df14f65-198d-43db-87c2-d5b1bd639180	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
183	Fintech123*	2024-09-18 01:17:29+00	f	YarisnethCardenasBijao	Yarisneth	Cardenas Bijao		f	t	2024-09-18 01:17:20+00	e444b3e6-8bf1-48d1-95bd-de021adc4505	N/A	N/A	\N	\N	\N	\N	\N	\N	4	\N	\N
140	Fintech123*	2024-08-29 19:00:42+00	f	ArianaMoreno	Ariana	Moreno Ramos		f	t	2024-08-29 19:00:33+00	42eff7df-b59e-405b-bccb-c6894633584a	N/A	N/A	\N	\N	\N	\N	\N	\N	13	\N	\N
152	Fintech123*	2024-08-31 02:59:21+00	f	AnaIsabelFernandez	Ana Isabel	Fernandez		f	t	2024-08-31 02:59:09+00	a9213df9-4d34-47a1-8010-78071cb55bd9	N/A	N/A	Profesor	\N	\N	\N	\N	\N	17	\N	\N
176	Fintech123*	2024-08-14 00:59:43+00	f	ZuleikaGonzalesFonda	Zuleika	Gonzales		f	t	2024-08-14 01:00:12+00	cd7383d5-2966-4d7d-ab08-22471b3f5905	N/A	N/A	\N	\N	\N	\N	\N	\N	21	\N	\N
160	Fintech123*	2024-08-24 22:33:34+00	f	AleidaMendoza	Aleida	Mendoza		f	t	2024-08-24 22:33:20+00	6b818546-1916-4089-ab04-9caf9ba364bc	N/A	N/A	\N	\N	\N	\N	\N	\N	23	\N	\N
225	Fintech123*	2024-04-30 22:02:10+00	f	Hernal	Hernal			f	t	2024-04-30 22:02:10+00	15934d62-9b7f-4f62-a4de-04cf6329f06a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
164	Fintech123*	2024-10-04 16:11:02+00	f	JorgeCordoba	Jorge	Córdoba		f	t	2024-10-04 16:10:55+00	c6ebd2c5-bca7-4fd4-8861-3a7b796ce9e8	N/A	N/A	\N	\N	\N	\N	\N	\N	1	\N	\N
232	Fintech123*	2024-09-12 21:51:37+00	f	LuisGonzalesHermano				f	t	2024-09-12 21:51:30+00	9f742ab8-8fae-4c2d-bc74-3f00d5c6be9c	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
145	Fintech123*	2024-07-25 23:54:42+00	f	JulianMendoza	Julian	Mendoza		f	t	2024-07-25 23:54:29+00	13b5ebfb-99f4-4883-9b1a-ddbd7a228e9d	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
173	Fintech123*	2024-10-08 00:41:51+00	f	ArmandoRodriguezGonzales	Armando	Rodriguez Gonzales		f	t	2024-10-18 00:42:28+00	feb148be-3b07-4167-91eb-c4f0fdf54934	N/A	N/A	\N	\N	\N	\N	\N	\N	3	\N	\N
166	Fintech123*	2024-10-06 00:03:45+00	f	LuisArmandoDominguez	Luis Armando	Dominguez		f	t	2024-10-06 00:04:20+00	1c8c5782-0ed9-4b77-a5fd-05fbe5a8ab0e	:Cabuya Arriba. Final. Frente a la piquera de busitos	:Cabuya Arriba. Final. Frente a la piquera de busitos	\N	\N	\N	\N	\N	\N	4	\N	\N
168	Fintech123*	2024-10-06 00:07:24+00	f	GustavoErisnelGonzalesLorenzo	GUSTAVO ERISNEL	GONZALEZ LORENZO		f	t	2024-10-18 00:07:30+00	ebce0f29-e853-4b69-bd05-39afcd153829	N/A	N/A	\N	\N	\N	\N	\N	\N	4	\N	\N
236	Fintech123*	2024-11-10 22:05:33+00	f	YARELIS	YARELIS			f	t	2024-11-10 22:05:29+00	9a508916-e94b-47de-99c8-6abbb8a7c095	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
258	Fintech123*	2024-11-23 21:28:23+00	f	LeoColon	Leo	Colon		f	t	2024-11-23 21:28:22+00	0549f61c-72c3-4920-84aa-e40eba4b71b3	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
265	Fintech123*	2024-11-29 01:00:07+00	f	JaimeTrejos	Jaime	Trejos		f	t	2024-11-29 01:00:02+00	0cc3bf93-6407-4b12-8b57-1cd67a2327b5	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
266	Fintech123*	2024-11-30 22:39:56+00	f	OmarBaneso	Omar			f	t	2024-11-30 22:39:34+00	51e2fd7f-fd2e-40b4-aa35-9552810a5a61	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
190	Fintech123*	2024-10-16 18:47:08+00	f	AlexioGonzalezGallo	Alexio Gonzalez	gallo pinto		f	t	2024-10-16 18:46:54+00	ac540c95-4339-4868-96d3-26c8d456fd6a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
192	Fintech123*	2024-08-31 19:01:28+00	f	IlkaBustos	Ilka	Bustoa		f	t	2024-08-31 19:01:23+00	552412bb-318f-4f1c-b5f8-d1afbb0a233b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
144	Fintech123*	2024-09-26 23:42:09+00	f	DiegoAbdielMeneses	Diego Abdiel	Meneses Torres		f	t	2024-09-26 23:42:02+00	7cf93684-23a6-4d70-a0c5-dbc4bd3d8243	Res. Anton B. El entradero. Calle principal al lado de la escuela.	Res. Anton B. El entradero. Calle principal al lado de la escuela.	\N	\N	\N	\N	\N	\N	5	\N	\N
194	Fintech123*	2024-10-16 19:49:29+00	f	CristianAlexanderMega	Cristian Alexander			f	t	2024-10-16 19:49:26+00	03224129-b748-47ab-bc3c-7b084f64ceb6	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
197	Fintech123*	2024-10-17 21:57:45+00	f	VictorMorales	Victor	Morales		f	t	2024-10-17 21:57:44+00	3df187cc-42d8-4719-93ab-3f2d0bf3cabb	Vive en Pnme calle uvi	Vive en Pnme calle uvi	\N	\N	\N	\N	\N	\N	1	\N	\N
198	Fintech123*	2024-07-16 22:52:13+00	f	RicauterSegundo	Ricauter	Segundo		f	t	2024-07-16 22:52:03+00	4c99ebc0-2fb7-44fe-9598-821987e4d33b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
200	Fintech123*	2024-10-20 23:16:01+00	f	MariaLuisaTercero	MariaLuisa	Villanueva		f	t	2024-10-24 23:15:56+00	94cc49dd-fdc7-4c3e-b2f1-09f2c963073a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
201	Fintech123*	2024-10-21 23:25:13+00	f	AidaProfesora	Aida			f	t	2024-10-21 23:25:11+00	bee0b98a-ca7c-49f6-a615-f499029cce9e	.Nata de los Caballeros	.Nata de los Caballeros	\N	\N	\N	\N	\N	\N	1	\N	\N
193	Fintech123*	2024-10-16 19:22:48+00	f	TrinidadJeanPorfe	Trinidad			f	t	2024-10-16 19:22:36+00	802cfeec-31f8-40af-b88e-cce006be88d5	N/A	N/A	Profesor	\N	\N	\N	\N	\N	7	\N	\N
124	Fintech123*	2024-07-01 20:29:05+00	f	DorisAguilar	Doris	Aguilar		f	t	2024-08-01 20:28:22+00	cdeb5f6e-2c33-4eb2-9b05-43e37c66b25b	N/A	N/A	Profesor	\N	\N	\N	\N	\N	11	\N	\N
27	Fintech123*	2024-09-12 21:08:37+00	f	RobertoCharles	Robert	Charles		f	t	2024-09-12 21:08:33+00	03b8b409-b92a-4754-a676-0862f98249c9	N/A	N/A	Profesor	\N	\N	\N	\N	\N	1	\N	\N
51	Fintech123*	2024-08-10 00:09:56+00	f	JoseLuisFernandez	José Luis	Fernandez		f	t	2024-08-10 00:09:46+00	4c25632b-3b9f-4bd1-87ec-f82525359299	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
204	Fintech123*	2024-07-15 00:10:59+00	f	AdolfoCorrea	Adolfo	Correa		f	t	2024-07-15 00:10:38+00	e37245c8-b4e9-47d5-b375-d0dac6328e4c	N/A	N/A	\N	\N	\N	\N	\N	\N	12	\N	\N
191	Fintech123*	2024-10-16 18:48:45+00	f	EdgarSoto	Edgar	Soto		f	t	2024-10-16 18:48:43+00	c303328b-795d-4e65-b8b9-c4d242e689a3	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
196	Fintech123*	2024-10-17 21:50:48+00	f	EvangelistoRojas	Evangelisto	Rojas		f	t	2024-10-17 21:47:10+00	7199fec1-d38a-4c57-a2c9-9aff3cc72453	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
129	Fintech123*	2024-09-20 21:09:09+00	f	YanCarlos	Carlos	Panaderia		f	t	2024-09-20 21:09:05+00	b888b4c0-c858-40f3-919e-2eabab8746d4	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
195	Fintech123*	2024-10-16 19:52:42+00	f	EDILBERTOJOELFIGUEROA	EDILBERTO JOEL	FIGUEROA		f	t	2024-10-16 19:52:34+00	03c2a856-6176-40e6-8349-31fcd20e49aa	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
203	Fintech123*	2024-10-21 23:27:37+00	f	CarlosMora	Carlos	Mora		f	t	2024-10-21 23:27:35+00	458bc02c-1aa5-4393-834e-14429964ecaf	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
202	Fintech123*	2024-10-21 23:26:41+00	f	JoaquinAgrazal	Joaquin	Agrazal		f	t	2024-10-21 23:26:39+00	1825296b-b639-4335-912e-7ba2480f816e	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
208	Fintech123*	2024-10-22 23:17:55+00	f	JavierArielOsorio	Javier Ariel	Osorio  Garcia		f	t	2024-10-22 23:17:50+00	c838c37f-92b6-4046-b421-0fb07958cf0b	Villas deArraijan Residencial. Aragon Casa. A43	Villas deArraijan Residencial. Aragon Casa. A43	Profesor	\N	\N	\N	\N	\N	1	\N	\N
212	Fintech123*	2024-10-22 23:35:01+00	f	OsvaldoOscarMoreno	Osvaldo oscar	Moreno Mitre		f	t	2024-10-22 23:34:57+00	4b580ee2-ec55-4c85-8657-09355dab37fe	calle larga	calle larga	\N	\N	\N	\N	\N	\N	\N	\N	\N
126	Fintech123*	2024-09-18 22:34:05+00	f	JhoannaRodriguez	Jhoanna	Rodriguez cabuya		f	t	2024-09-18 22:33:55+00	3d0fd4d1-cbc1-4ae5-b19c-765f423b586a	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
217	Fintech123*	2024-10-26 00:33:39+00	f	MarietaElionorMorales	Marieta Elionor	Morales		f	t	2024-10-26 00:33:35+00	d8a9d24e-a083-4a8b-89f9-ce14db6b81c5	B. Guabas Abajo	B. Guabas Abajo	\N	\N	\N	\N	\N	\N	\N	\N	\N
219	Fintech123*	2024-10-27 01:07:29+00	f	AidaRamos	Aida	Ramos		f	t	2024-10-27 01:07:16+00	c6250616-8ec7-42aa-a492-47f09e117867	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
221	Fintech123*	2024-10-29 22:07:41+00	f	LeidyMassielRodriguez	Leidy Massiel	Rodriguez		f	t	2024-10-29 22:07:36+00	d426bde7-7ec1-498c-944b-7e61c825b840	Vive en las minas. Via la la pintada	Vive en las minas. Via la la pintada	Secretaria	Secretaria	\N	\N	\N	\N	1	\N	\N
223	Fintech123*	2024-03-02 21:45:19+00	f	JoséAdrianoPérez	José Adriano	Pérez		f	t	2024-03-02 21:43:08+00	1ba14f22-2fff-4be0-846d-660e73fc1af3	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
226	Fintech123*	2024-07-16 01:35:46+00	f	BenjaminFerreteria	Benjamin			f	t	2024-07-16 01:35:38+00	fd25942a-6649-405b-b9d9-685e3268c833	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
199	Fintech123*	2024-10-19 23:07:55+00	f	JoseDavidPanaderia	David			f	t	2024-10-24 23:07:54+00	dcfb33df-ff4d-4fd6-8904-d1ed826f8e37	N/A	N/A	\N	\N	\N	\N	\N	\N	5	\N	\N
75	Fintech123*	2024-08-13 21:26:50+00	f	AnnaMares	Anna	Mares		f	t	2024-08-13 21:26:25+00	05a31b01-78fa-4bd0-9ca5-70be7212ef1c	N/A	N/A	\N	\N	\N	\N	\N	\N	13	\N	\N
229	Fintech123*	2024-11-02 01:35:33+00	f	AbdelDeleon	Abdel	De Leon		f	t	2024-11-02 01:34:50+00	33fe54fb-9e31-43f4-af07-a9f43ebaacf4	Barriada el Bosque. Al lado de la escuela la Escala	Barriada el Bosque. Al lado de la escuela la Escala	\N	\N	\N	\N	\N	\N	\N	\N	\N
231	Fintech123*	2024-11-02 20:31:07+00	f	SaulHumbertoSaens	Saul Humberto	Saens		f	t	2024-11-02 20:31:03+00	ea558d44-05be-44a0-9666-011ea884c8a7	N/A	N/A	\N	\N	\N	\N	\N	\N	27	\N	\N
178	Fintech123*	2024-10-14 23:20:09+00	f	AlcidesOrtegaFlorez	Alcides	Ortega florez		f	t	2024-10-14 23:20:51+00	ffc794e8-1923-4192-9cf7-34cdecfb4702	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
73	Fintech123*	2024-07-13 20:04:06+00	f	ArianaItzel	Ariana Itzel	Hernandez		f	t	2024-08-13 20:03:55+00	4bcb9792-7a41-423a-9c82-d9af3a4f064c	N/A	N/A	Profesor	\N	\N	\N	\N	\N	17	\N	\N
233	Fintech123*	2024-07-25 22:09:38+00	f	ReinaldoPérez	Reinaldo	Pérez		f	t	2024-07-25 22:09:35+00	eace0ff0-732e-4720-a9cb-93bff0918baf	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
205	Fintech123*	2024-07-16 00:16:37+00	f	MaicolIbarra	Maicol	Ibarra		f	t	2024-07-16 00:16:27+00	f3f57bac-0a6b-4866-be4c-795136486169	N/A	N/A	\N	\N	\N	\N	\N	\N	17	\N	\N
142	Fintech123*	2024-09-26 23:37:48+00	f	DianaEstherPerez	Diana Esther	Perez		f	t	2024-09-26 23:37:43+00	8e60911b-f19e-429e-b2e7-546af481febc	JuanDiaza frente ala iglesia evangelica roca dela eternidad	JuanDiaza frente ala iglesia evangelica roca dela eternidad	\N	\N	\N	\N	\N	\N	3	\N	\N
234	Fintech123*	2024-03-02 22:04:38+00	f	JoseAdrianoPerez	Jose Adriano	Perez		f	t	2024-03-02 22:04:27+00	0e3e1e55-bd8e-4d1b-82c3-784269b8833d	N/A	N/A	\N	\N	\N	\N	\N	\N	3	\N	\N
22	Fintech123*	2024-08-03 01:17:43+00	f	JoseLucianoMendoza	José Luciano	Mendoza		f	t	2024-08-03 01:17:33+00	3a78a5fc-26c2-4921-ba8a-b7b8ca6e28e3	N/A	N/A	\N	\N	\N	\N	\N	\N	31	\N	\N
239	Fintech123*	2024-11-14 23:40:50+00	f	JoseVillaverde	Jose	Villaverde		f	t	2024-11-14 23:40:44+00	d5c0f961-cb5d-4465-90e6-bf3335bbdc03	N/A	N/A	\N	\N	\N	\N	\N	\N	32	\N	\N
189	Fintech123*	2024-10-05 18:18:33+00	f	OscarAlbertSuegro	Oscar Alberto	Arauz		f	t	2024-10-05 18:18:29+00	85a71083-6f9b-4d75-a5dc-60de4f01468b	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
241	Fintech123*	2024-11-17 19:22:56+00	f	AuraTorres	Aura	Torres		f	t	2024-11-17 19:22:53+00	fbf6fda4-d814-47f0-b665-177cdd6fc954	Pueblo Nuevo	Pueblo Nuevo	\N	\N	\N	\N	\N	\N	33	\N	\N
243	Fintech123*	2024-11-19 00:33:16+00	f	GustavoBijao	Gustavo			f	t	2024-11-19 00:33:10+00	dd7ec831-c6af-47d8-82c6-bec5e6cf1df2	N/A	N/A	\N	\N	\N	\N	\N	\N	4	\N	\N
245	Fintech123*	2024-11-19 00:41:44+00	f	PascualaMartinez	Pascuala	Martinez		f	t	2024-11-19 00:41:40+00	2a6b418e-0116-4bb8-aa63-824fe38a8cb2	vive en pueblo hermoso, via a las delicias. Call., 3, casa 53.	vive en pueblo hermoso, via a las delicias. Call., 3, casa 53.	\N	\N	\N	\N	\N	\N	27	\N	\N
247	Fintech123*	2024-11-15 19:10:58+00	f	KrizelBetancurt	Krizel	Betancurt		f	t	2024-11-15 19:10:49+00	d8661992-cc4c-4c3c-8dca-69706bd7bda3	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
249	Fintech123*	2024-11-17 22:39:48+00	f	CarlosArquiñezKike	Carlos	sArquiñez		f	t	2024-11-17 22:39:26+00	d8b9279f-2ed9-482a-a816-07d3e87ee95f	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
251	Fintech123*	2024-11-16 23:09:55+00	f	YamarisMedina	Yamaris	Medina		f	t	2024-11-16 23:09:52+00	b7a22ec3-537c-4a55-af89-706f1416600f	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
253	Fintech123*	2024-11-21 00:13:40+00	f	GregorioSoto	Gregorio	Soto		f	t	2024-11-21 00:13:35+00	99f4d17c-2447-43e6-993d-dbdbc4b1ee43	N/A	N/A	\N	\N	\N	\N	\N	\N	6	\N	\N
237	Fintech123*	2024-11-11 22:46:24+00	f	GeronimoPerez	Geronimo	186		f	t	2024-11-20 22:40:20+00	00d3f92f-4c2b-43bf-aa88-cdb3b9a05f9d	en jn juan diaz	en jn juan diaz	\N	\N	\N	\N	\N	\N	35	\N	\N
260	Fintech123*	2024-11-25 22:11:57+00	f	YarelisArrocha	Yarelis	Arrocha		f	t	2024-11-25 22:11:52+00	eed6d306-ab9c-4392-af6b-fc9f02e7e713	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
259	Fintech123*	2024-11-25 22:09:55+00	f	FatimaHerrera	Fatima	Herrera		f	t	2024-11-25 22:09:54+00	4165f1af-da9e-4a17-b7d0-f33f26c047ed	Res. Llano hermoso. Calle13 casa 23H	Res. Llano hermoso. Calle13 casa 23H	\N	\N	\N	\N	\N	\N	27	\N	\N
261	Fintech123*	2024-11-25 22:13:29+00	f	MarlinMora	Marlin	Mora		f	t	2024-11-27 22:13:27+00	2dcf906a-0ece-427a-b4d0-0bb7adb85fe7	Vive. Cermeño. Al lado de la casa comunal.	Vive. Cermeño. Al lado de la casa comunal.	\N	\N	\N	\N	\N	\N	27	\N	\N
262	Fintech123*	2024-11-25 22:15:38+00	f	IrinaHernandez	Irina	Hernandez		f	t	2024-11-25 22:15:36+00	a7cdf285-fd71-4cd7-b640-a405dc471022	Vive en llano Marin al lado de la piscina	Vive en llano Marin al lado de la piscina	\N	\N	\N	\N	\N	\N	27	\N	\N
263	Fintech123*	2024-11-25 22:18:25+00	f	JoaquinMelgar	Joaquin	Melgar		f	t	2024-11-27 22:18:20+00	be9da87a-7a47-4e00-9b06-d6148863e3b5	Res. Vi e al lado de la iglesia. En Garicin	Res. Vi e al lado de la iglesia. En Garicin	\N	\N	\N	\N	\N	\N	27	\N	\N
264	Fintech123*	2024-11-27 00:20:34+00	f	BolivarMedina	Bolivar	Medina		f	t	2024-11-27 00:20:10+00	ae1a0d87-d7fe-40a8-97cb-977d49f7c514	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
267	Fintech123*	2024-12-01 23:27:06+00	f	SadiaNavarro	Sadia	Navarro		f	t	2024-12-05 23:27:03+00	f182ad9d-8026-45de-9915-32623525be97	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
268	Fintech123*	2024-12-02 23:37:48+00	f	MariaDelosReyes	Maria	De Los Reyes		f	t	2024-12-05 23:37:11+00	ac3176ce-ccf5-4a39-9b2a-476def6ed634	B. Ciruelito de Anton. Clle de esc. Patino Final	B. Ciruelito de Anton. Clle de esc. Patino Final	\N	\N	\N	\N	\N	\N	\N	\N	\N
269	Fintech123*	2024-12-05 00:58:54+00	f	BombaDelta				f	t	2024-12-06 00:58:35+00	a9c4041c-f48f-420d-8ec5-d33e95a40010	N/A	N/A	\N	\N	\N	\N	\N	\N	\N	\N	\N
270	Fintech123*	2024-12-05 01:04:15+00	f	JavierGonzales	Javier	Gonzales		f	t	2024-12-06 01:04:12+00	b77e9e4d-3794-47c7-9461-13f219eb56be	san Juan de Dios	san Juan de Dios	\N	\N	\N	\N	\N	\N	\N	\N	\N
271	Fintech123*	2024-12-05 01:10:35+00	f	ElizabertMartinez	Elizabert	Martinez		f	t	2024-12-06 01:10:22+00	baa5def5-61cf-4983-89a6-4cba356d6c9f	vista hermosa.  Pnme	vista hermosa.  Pnme	\N	\N	\N	\N	\N	\N	34	\N	\N
272	Fintech123*	2024-12-05 01:11:47+00	f	AntonioCamargo	Antonio	Camargo		f	t	2024-12-06 01:11:44+00	a14355d4-5327-4e9a-9348-c3e200ced891	Villa cumbrera	Villa cumbrera	\N	\N	\N	\N	\N	\N	27	\N	\N
\.


--
-- Data for Name: fintech_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_user_groups" ("id", "user_id", "group_id") FROM stdin;
1	1	1
2	2	1
3	3	1
4	8	1
5	10	1
6	18	1
\.


--
-- Data for Name: fintech_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."fintech_user_user_permissions" ("id", "user_id", "permission_id") FROM stdin;
\.


--
-- Data for Name: oauth2_provider_accesstoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."oauth2_provider_accesstoken" ("id", "token", "expires", "scope", "application_id", "user_id", "created", "updated", "source_refresh_token_id", "id_token_id", "token_checksum") FROM stdin;
\.


--
-- Data for Name: oauth2_provider_application; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."oauth2_provider_application" ("id", "client_id", "redirect_uris", "client_type", "authorization_grant_type", "client_secret", "name", "user_id", "skip_authorization", "created", "updated", "algorithm", "post_logout_redirect_uris", "hash_client_secret", "allowed_origins") FROM stdin;
\.


--
-- Data for Name: oauth2_provider_grant; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."oauth2_provider_grant" ("id", "code", "expires", "redirect_uri", "scope", "application_id", "user_id", "created", "updated", "code_challenge", "code_challenge_method", "nonce", "claims") FROM stdin;
\.


--
-- Data for Name: oauth2_provider_idtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."oauth2_provider_idtoken" ("id", "jti", "expires", "scope", "created", "updated", "application_id", "user_id") FROM stdin;
\.


--
-- Data for Name: oauth2_provider_refreshtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."oauth2_provider_refreshtoken" ("id", "token", "access_token_id", "application_id", "user_id", "created", "updated", "revoked", "token_family") FROM stdin;
\.


--
-- Data for Name: token_blacklist_blacklistedtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."token_blacklist_blacklistedtoken" ("id", "blacklisted_at", "token_id") FROM stdin;
\.


--
-- Data for Name: token_blacklist_outstandingtoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY "public"."token_blacklist_outstandingtoken" ("id", "token", "created_at", "expires_at", "user_id", "jti") FROM stdin;
1	eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyNzY2MzM3NCwiaWF0IjoxNzI3NTc2OTc0LCJqdGkiOiIxNTdhZTg1ZmNkZWM0MmYzOGY3ZDYzMDRhOGNmYWI3NiIsInVzZXJfaWQiOjF9.dRIkeQy7eRMbPGxADAoThC8wLpdb-zDnB1GqKxPXkiM	2024-09-29 02:29:34.081715+00	2024-09-30 02:29:34+00	1	157ae85fcdec42f38f7d6304a8cfab76
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."auth_group_id_seq"', 1, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."auth_group_permissions_id_seq"', 30, true);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."auth_permission_id_seq"', 144, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."auth_user_groups_id_seq"', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."auth_user_id_seq"', 4, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."auth_user_user_permissions_id_seq"', 120, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."django_admin_log_id_seq"', 2197, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."django_content_type_id_seq"', 36, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."django_migrations_id_seq"', 52, true);


--
-- Name: fintech_account_id_payment_method_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_account_id_payment_method_seq"', 4, true);


--
-- Name: fintech_accountmethodamount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_accountmethodamount_id_seq"', 1477, true);


--
-- Name: fintech_address_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_address_id_seq"', 1, false);


--
-- Name: fintech_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_category_id_seq"', 12, true);


--
-- Name: fintech_categorytype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_categorytype_id_seq"', 6, true);


--
-- Name: fintech_country_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_country_id_seq"', 1, true);


--
-- Name: fintech_credit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_credit_id_seq"', 629, true);


--
-- Name: fintech_currency_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_currency_id_seq"', 3, true);


--
-- Name: fintech_documenttype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_documenttype_id_seq"', 1, true);


--
-- Name: fintech_expense_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_expense_id_seq"', 155, true);


--
-- Name: fintech_identifier_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_identifier_id_seq"', 1, true);


--
-- Name: fintech_label_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_label_id_seq"', 35, true);


--
-- Name: fintech_language_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_language_id_seq"', 1, false);


--
-- Name: fintech_paramslocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_paramslocation_id_seq"', 1, false);


--
-- Name: fintech_periodicity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_periodicity_id_seq"', 4, true);


--
-- Name: fintech_phonenumber_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_phonenumber_id_seq"', 1, false);


--
-- Name: fintech_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_role_id_seq"', 2, true);


--
-- Name: fintech_seller_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_seller_id_seq"', 1, true);


--
-- Name: fintech_subcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_subcategory_id_seq"', 13, true);


--
-- Name: fintech_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_transaction_id_seq"', 1488, true);


--
-- Name: fintech_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_user_groups_id_seq"', 6, true);


--
-- Name: fintech_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_user_id_seq"', 272, true);


--
-- Name: fintech_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."fintech_user_user_permissions_id_seq"', 1, false);


--
-- Name: oauth2_provider_accesstoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."oauth2_provider_accesstoken_id_seq"', 1, false);


--
-- Name: oauth2_provider_application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."oauth2_provider_application_id_seq"', 1, false);


--
-- Name: oauth2_provider_grant_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."oauth2_provider_grant_id_seq"', 1, false);


--
-- Name: oauth2_provider_idtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."oauth2_provider_idtoken_id_seq"', 1, false);


--
-- Name: oauth2_provider_refreshtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."oauth2_provider_refreshtoken_id_seq"', 1, false);


--
-- Name: token_blacklist_blacklistedtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."token_blacklist_blacklistedtoken_id_seq"', 1, false);


--
-- Name: token_blacklist_outstandingtoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('"public"."token_blacklist_outstandingtoken_id_seq"', 1, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group"
    ADD CONSTRAINT "auth_group_name_key" UNIQUE ("name");


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group_permissions"
    ADD CONSTRAINT "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" UNIQUE ("group_id", "permission_id");


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group_permissions"
    ADD CONSTRAINT "auth_group_permissions_pkey" PRIMARY KEY ("id");


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group"
    ADD CONSTRAINT "auth_group_pkey" PRIMARY KEY ("id");


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_permission"
    ADD CONSTRAINT "auth_permission_content_type_id_codename_01ab375a_uniq" UNIQUE ("content_type_id", "codename");


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_permission"
    ADD CONSTRAINT "auth_permission_pkey" PRIMARY KEY ("id");


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_groups"
    ADD CONSTRAINT "auth_user_groups_pkey" PRIMARY KEY ("id");


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_groups"
    ADD CONSTRAINT "auth_user_groups_user_id_group_id_94350c0c_uniq" UNIQUE ("user_id", "group_id");


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user"
    ADD CONSTRAINT "auth_user_pkey" PRIMARY KEY ("id");


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_user_permissions"
    ADD CONSTRAINT "auth_user_user_permissions_pkey" PRIMARY KEY ("id");


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_user_permissions"
    ADD CONSTRAINT "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" UNIQUE ("user_id", "permission_id");


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user"
    ADD CONSTRAINT "auth_user_username_key" UNIQUE ("username");


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."authtoken_token"
    ADD CONSTRAINT "authtoken_token_pkey" PRIMARY KEY ("key");


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."authtoken_token"
    ADD CONSTRAINT "authtoken_token_user_id_key" UNIQUE ("user_id");


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_admin_log"
    ADD CONSTRAINT "django_admin_log_pkey" PRIMARY KEY ("id");


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_content_type"
    ADD CONSTRAINT "django_content_type_app_label_model_76bd3d3b_uniq" UNIQUE ("app_label", "model");


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_content_type"
    ADD CONSTRAINT "django_content_type_pkey" PRIMARY KEY ("id");


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_migrations"
    ADD CONSTRAINT "django_migrations_pkey" PRIMARY KEY ("id");


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_session"
    ADD CONSTRAINT "django_session_pkey" PRIMARY KEY ("session_key");


--
-- Name: fintech_account fintech_account_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_account"
    ADD CONSTRAINT "fintech_account_pkey" PRIMARY KEY ("id_payment_method");


--
-- Name: fintech_accountmethodamount fintech_accountmethodamount_payment_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount"
    ADD CONSTRAINT "fintech_accountmethodamount_payment_code_key" UNIQUE ("payment_code");


--
-- Name: fintech_accountmethodamount fintech_accountmethodamount_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount"
    ADD CONSTRAINT "fintech_accountmethodamount_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_address fintech_address_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_address"
    ADD CONSTRAINT "fintech_address_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_category fintech_category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_category"
    ADD CONSTRAINT "fintech_category_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_category fintech_category_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_category"
    ADD CONSTRAINT "fintech_category_uid_key" UNIQUE ("uid");


--
-- Name: fintech_categorytype fintech_categorytype_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_categorytype"
    ADD CONSTRAINT "fintech_categorytype_name_key" UNIQUE ("name");


--
-- Name: fintech_categorytype fintech_categorytype_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_categorytype"
    ADD CONSTRAINT "fintech_categorytype_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_categorytype fintech_categorytype_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_categorytype"
    ADD CONSTRAINT "fintech_categorytype_uid_key" UNIQUE ("uid");


--
-- Name: fintech_country fintech_country_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_country"
    ADD CONSTRAINT "fintech_country_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_credit fintech_credit_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_credit fintech_credit_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_uid_key" UNIQUE ("uid");


--
-- Name: fintech_currency fintech_currency_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_currency"
    ADD CONSTRAINT "fintech_currency_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_documenttype fintech_documenttype_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_documenttype"
    ADD CONSTRAINT "fintech_documenttype_code_key" UNIQUE ("code");


--
-- Name: fintech_documenttype fintech_documenttype_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_documenttype"
    ADD CONSTRAINT "fintech_documenttype_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_expense fintech_expense_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense"
    ADD CONSTRAINT "fintech_expense_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_expense fintech_expense_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense"
    ADD CONSTRAINT "fintech_expense_uid_key" UNIQUE ("uid");


--
-- Name: fintech_identifier fintech_identifier_document_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_identifier"
    ADD CONSTRAINT "fintech_identifier_document_number_key" UNIQUE ("document_number");


--
-- Name: fintech_identifier fintech_identifier_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_identifier"
    ADD CONSTRAINT "fintech_identifier_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_label fintech_label_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_label"
    ADD CONSTRAINT "fintech_label_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_label fintech_label_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_label"
    ADD CONSTRAINT "fintech_label_uid_key" UNIQUE ("uid");


--
-- Name: fintech_language fintech_language_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_language"
    ADD CONSTRAINT "fintech_language_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_paramslocation fintech_paramslocation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_paramslocation"
    ADD CONSTRAINT "fintech_paramslocation_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_periodicity fintech_periodicity_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_periodicity"
    ADD CONSTRAINT "fintech_periodicity_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_phonenumber fintech_phonenumber_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_phonenumber"
    ADD CONSTRAINT "fintech_phonenumber_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_role fintech_role_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_role"
    ADD CONSTRAINT "fintech_role_name_key" UNIQUE ("name");


--
-- Name: fintech_role fintech_role_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_role"
    ADD CONSTRAINT "fintech_role_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_seller fintech_seller_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_seller"
    ADD CONSTRAINT "fintech_seller_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_seller fintech_seller_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_seller"
    ADD CONSTRAINT "fintech_seller_user_id_key" UNIQUE ("user_id");


--
-- Name: fintech_subcategory fintech_subcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_subcategory"
    ADD CONSTRAINT "fintech_subcategory_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_subcategory fintech_subcategory_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_subcategory"
    ADD CONSTRAINT "fintech_subcategory_uid_key" UNIQUE ("uid");


--
-- Name: fintech_transaction fintech_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_transaction"
    ADD CONSTRAINT "fintech_transaction_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_transaction fintech_transaction_uid_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_transaction"
    ADD CONSTRAINT "fintech_transaction_uid_key" UNIQUE ("uid");


--
-- Name: fintech_user_groups fintech_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_groups"
    ADD CONSTRAINT "fintech_user_groups_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_user_groups fintech_user_groups_user_id_group_id_03e1aeef_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_groups"
    ADD CONSTRAINT "fintech_user_groups_user_id_group_id_03e1aeef_uniq" UNIQUE ("user_id", "group_id");


--
-- Name: fintech_user fintech_user_id_user_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_id_user_key" UNIQUE ("id_user");


--
-- Name: fintech_user fintech_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_user_user_permissions fintech_user_user_permis_user_id_permission_id_a21e5774_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_user_permissions"
    ADD CONSTRAINT "fintech_user_user_permis_user_id_permission_id_a21e5774_uniq" UNIQUE ("user_id", "permission_id");


--
-- Name: fintech_user_user_permissions fintech_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_user_permissions"
    ADD CONSTRAINT "fintech_user_user_permissions_pkey" PRIMARY KEY ("id");


--
-- Name: fintech_user fintech_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_username_key" UNIQUE ("username");


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_id_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_accesstoken_id_token_id_key" UNIQUE ("id_token_id");


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_accesstoken_pkey" PRIMARY KEY ("id");


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_source_refresh_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_accesstoken_source_refresh_token_id_key" UNIQUE ("source_refresh_token_id");


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_token_checksum_85319a26_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_accesstoken_token_checksum_85319a26_uniq" UNIQUE ("token_checksum");


--
-- Name: oauth2_provider_application oauth2_provider_application_client_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_application"
    ADD CONSTRAINT "oauth2_provider_application_client_id_key" UNIQUE ("client_id");


--
-- Name: oauth2_provider_application oauth2_provider_application_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_application"
    ADD CONSTRAINT "oauth2_provider_application_pkey" PRIMARY KEY ("id");


--
-- Name: oauth2_provider_grant oauth2_provider_grant_code_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_grant"
    ADD CONSTRAINT "oauth2_provider_grant_code_key" UNIQUE ("code");


--
-- Name: oauth2_provider_grant oauth2_provider_grant_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_grant"
    ADD CONSTRAINT "oauth2_provider_grant_pkey" PRIMARY KEY ("id");


--
-- Name: oauth2_provider_idtoken oauth2_provider_idtoken_jti_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_idtoken"
    ADD CONSTRAINT "oauth2_provider_idtoken_jti_key" UNIQUE ("jti");


--
-- Name: oauth2_provider_idtoken oauth2_provider_idtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_idtoken"
    ADD CONSTRAINT "oauth2_provider_idtoken_pkey" PRIMARY KEY ("id");


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_access_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_refreshtoken"
    ADD CONSTRAINT "oauth2_provider_refreshtoken_access_token_id_key" UNIQUE ("access_token_id");


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_refreshtoken"
    ADD CONSTRAINT "oauth2_provider_refreshtoken_pkey" PRIMARY KEY ("id");


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_refreshtoken"
    ADD CONSTRAINT "oauth2_provider_refreshtoken_token_revoked_af8a5134_uniq" UNIQUE ("token", "revoked");


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_blacklistedtoken"
    ADD CONSTRAINT "token_blacklist_blacklistedtoken_pkey" PRIMARY KEY ("id");


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_blacklistedtoken"
    ADD CONSTRAINT "token_blacklist_blacklistedtoken_token_id_key" UNIQUE ("token_id");


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_outstandingtoken"
    ADD CONSTRAINT "token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq" UNIQUE ("jti");


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outstandingtoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_outstandingtoken"
    ADD CONSTRAINT "token_blacklist_outstandingtoken_pkey" PRIMARY KEY ("id");


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_group_name_a6ea08ec_like" ON "public"."auth_group" USING "btree" ("name" "varchar_pattern_ops");


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "public"."auth_group_permissions" USING "btree" ("group_id");


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "public"."auth_group_permissions" USING "btree" ("permission_id");


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "public"."auth_permission" USING "btree" ("content_type_id");


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_user_groups_group_id_97559544" ON "public"."auth_user_groups" USING "btree" ("group_id");


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_user_groups_user_id_6a12ed8b" ON "public"."auth_user_groups" USING "btree" ("user_id");


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_user_user_permissions_permission_id_1fbb5f2c" ON "public"."auth_user_user_permissions" USING "btree" ("permission_id");


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_user_user_permissions_user_id_a95ead1b" ON "public"."auth_user_user_permissions" USING "btree" ("user_id");


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "auth_user_username_6821ab7c_like" ON "public"."auth_user" USING "btree" ("username" "varchar_pattern_ops");


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "authtoken_token_key_10f0b77e_like" ON "public"."authtoken_token" USING "btree" ("key" "varchar_pattern_ops");


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "public"."django_admin_log" USING "btree" ("content_type_id");


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "django_admin_log_user_id_c564eba6" ON "public"."django_admin_log" USING "btree" ("user_id");


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "django_session_expire_date_a5c62663" ON "public"."django_session" USING "btree" ("expire_date");


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "django_session_session_key_c0390e0f_like" ON "public"."django_session" USING "btree" ("session_key" "varchar_pattern_ops");


--
-- Name: fintech_account_currency_id_dcd5160a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_account_currency_id_dcd5160a" ON "public"."fintech_account" USING "btree" ("currency_id");


--
-- Name: fintech_accountmethodamount_credit_id_c52a4a9c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_accountmethodamount_credit_id_c52a4a9c" ON "public"."fintech_accountmethodamount" USING "btree" ("credit_id");


--
-- Name: fintech_accountmethodamount_currency_id_088ff444; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_accountmethodamount_currency_id_088ff444" ON "public"."fintech_accountmethodamount" USING "btree" ("currency_id");


--
-- Name: fintech_accountmethodamount_payment_code_df824755_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_accountmethodamount_payment_code_df824755_like" ON "public"."fintech_accountmethodamount" USING "btree" ("payment_code" "varchar_pattern_ops");


--
-- Name: fintech_accountmethodamount_payment_method_id_6a28ff5a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_accountmethodamount_payment_method_id_6a28ff5a" ON "public"."fintech_accountmethodamount" USING "btree" ("payment_method_id");


--
-- Name: fintech_accountmethodamount_transaction_id_962ad92f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_accountmethodamount_transaction_id_962ad92f" ON "public"."fintech_accountmethodamount" USING "btree" ("transaction_id");


--
-- Name: fintech_address_country_id_e50a90ec; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_address_country_id_e50a90ec" ON "public"."fintech_address" USING "btree" ("country_id");


--
-- Name: fintech_address_user_id_b141579e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_address_user_id_b141579e" ON "public"."fintech_address" USING "btree" ("user_id");


--
-- Name: fintech_category_category_type_id_8c2a931a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_category_category_type_id_8c2a931a" ON "public"."fintech_category" USING "btree" ("category_type_id");


--
-- Name: fintech_categorytype_name_b89ce7d3_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_categorytype_name_b89ce7d3_like" ON "public"."fintech_categorytype" USING "btree" ("name" "varchar_pattern_ops");


--
-- Name: fintech_credit_currency_id_b12e7221; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_currency_id_b12e7221" ON "public"."fintech_credit" USING "btree" ("currency_id");


--
-- Name: fintech_credit_payment_id_62803c60; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_payment_id_62803c60" ON "public"."fintech_credit" USING "btree" ("payment_id");


--
-- Name: fintech_credit_periodicity_id_6f6a311a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_periodicity_id_6f6a311a" ON "public"."fintech_credit" USING "btree" ("periodicity_id");


--
-- Name: fintech_credit_registered_by_id_5c849d88; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_registered_by_id_5c849d88" ON "public"."fintech_credit" USING "btree" ("registered_by_id");


--
-- Name: fintech_credit_seller_id_c3d4f145; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_seller_id_c3d4f145" ON "public"."fintech_credit" USING "btree" ("seller_id");


--
-- Name: fintech_credit_subcategory_id_4e4ac2ca; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_subcategory_id_4e4ac2ca" ON "public"."fintech_credit" USING "btree" ("subcategory_id");


--
-- Name: fintech_credit_user_id_8f2f3be3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_credit_user_id_8f2f3be3" ON "public"."fintech_credit" USING "btree" ("user_id");


--
-- Name: fintech_documenttype_code_d7ceaafb_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_documenttype_code_d7ceaafb_like" ON "public"."fintech_documenttype" USING "btree" ("code" "varchar_pattern_ops");


--
-- Name: fintech_documenttype_country_id_id_0b6af4b2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_documenttype_country_id_id_0b6af4b2" ON "public"."fintech_documenttype" USING "btree" ("country_id_id");


--
-- Name: fintech_expense_account_id_84b59e55; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_expense_account_id_84b59e55" ON "public"."fintech_expense" USING "btree" ("account_id");


--
-- Name: fintech_expense_category_id_8e608b51; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_expense_category_id_8e608b51" ON "public"."fintech_expense" USING "btree" ("subcategory_id");


--
-- Name: fintech_expense_registered_by_id_6cd6d3d2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_expense_registered_by_id_6cd6d3d2" ON "public"."fintech_expense" USING "btree" ("registered_by_id");


--
-- Name: fintech_expense_user_id_df173b21; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_expense_user_id_df173b21" ON "public"."fintech_expense" USING "btree" ("user_id");


--
-- Name: fintech_identifier_country_id_355176a7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_identifier_country_id_355176a7" ON "public"."fintech_identifier" USING "btree" ("country_id");


--
-- Name: fintech_identifier_document_number_d8e74d5c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_identifier_document_number_d8e74d5c_like" ON "public"."fintech_identifier" USING "btree" ("document_number" "varchar_pattern_ops");


--
-- Name: fintech_identifier_document_type_id_f348b6c7; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_identifier_document_type_id_f348b6c7" ON "public"."fintech_identifier" USING "btree" ("document_type_id");


--
-- Name: fintech_phonenumber_country_related_id_5dbe9007; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_phonenumber_country_related_id_5dbe9007" ON "public"."fintech_phonenumber" USING "btree" ("country_related_id");


--
-- Name: fintech_role_name_52d8e08d_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_role_name_52d8e08d_like" ON "public"."fintech_role" USING "btree" ("name" "varchar_pattern_ops");


--
-- Name: fintech_seller_role_id_f00a0466; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_seller_role_id_f00a0466" ON "public"."fintech_seller" USING "btree" ("role_id");


--
-- Name: fintech_subcategory_category_id_50f7bc8f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_subcategory_category_id_50f7bc8f" ON "public"."fintech_subcategory" USING "btree" ("category_id");


--
-- Name: fintech_transaction_category_id_e09c657c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_transaction_category_id_e09c657c" ON "public"."fintech_transaction" USING "btree" ("category_id");


--
-- Name: fintech_transaction_user_id_7a424d2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_transaction_user_id_7a424d2c" ON "public"."fintech_transaction" USING "btree" ("user_id");


--
-- Name: fintech_user_city_id_f6cec28d; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_city_id_f6cec28d" ON "public"."fintech_user" USING "btree" ("city_id");


--
-- Name: fintech_user_country_id_90ed5849; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_country_id_90ed5849" ON "public"."fintech_user" USING "btree" ("country_id");


--
-- Name: fintech_user_document_id_f52d8362; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_document_id_f52d8362" ON "public"."fintech_user" USING "btree" ("document_id");


--
-- Name: fintech_user_groups_group_id_18bcab92; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_groups_group_id_18bcab92" ON "public"."fintech_user_groups" USING "btree" ("group_id");


--
-- Name: fintech_user_groups_user_id_15fdbb30; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_groups_user_id_15fdbb30" ON "public"."fintech_user_groups" USING "btree" ("user_id");


--
-- Name: fintech_user_label_id_5129caf1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_label_id_5129caf1" ON "public"."fintech_user" USING "btree" ("label_id");


--
-- Name: fintech_user_phone_1_id_2077fbe4; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_phone_1_id_2077fbe4" ON "public"."fintech_user" USING "btree" ("phone_1_id");


--
-- Name: fintech_user_role_id_45d07174; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_role_id_45d07174" ON "public"."fintech_user" USING "btree" ("role_id");


--
-- Name: fintech_user_user_permissions_permission_id_ca4b8a5c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_user_permissions_permission_id_ca4b8a5c" ON "public"."fintech_user_user_permissions" USING "btree" ("permission_id");


--
-- Name: fintech_user_user_permissions_user_id_5b840db9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_user_permissions_user_id_5b840db9" ON "public"."fintech_user_user_permissions" USING "btree" ("user_id");


--
-- Name: fintech_user_username_1d15bc5f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "fintech_user_username_1d15bc5f_like" ON "public"."fintech_user" USING "btree" ("username" "varchar_pattern_ops");


--
-- Name: oauth2_provider_accesstoken_application_id_b22886e1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_accesstoken_application_id_b22886e1" ON "public"."oauth2_provider_accesstoken" USING "btree" ("application_id");


--
-- Name: oauth2_provider_accesstoken_token_checksum_85319a26_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_accesstoken_token_checksum_85319a26_like" ON "public"."oauth2_provider_accesstoken" USING "btree" ("token_checksum" "varchar_pattern_ops");


--
-- Name: oauth2_provider_accesstoken_user_id_6e4c9a65; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_accesstoken_user_id_6e4c9a65" ON "public"."oauth2_provider_accesstoken" USING "btree" ("user_id");


--
-- Name: oauth2_provider_application_client_id_03f0cc84_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_application_client_id_03f0cc84_like" ON "public"."oauth2_provider_application" USING "btree" ("client_id" "varchar_pattern_ops");


--
-- Name: oauth2_provider_application_client_secret_53133678; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_application_client_secret_53133678" ON "public"."oauth2_provider_application" USING "btree" ("client_secret");


--
-- Name: oauth2_provider_application_client_secret_53133678_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_application_client_secret_53133678_like" ON "public"."oauth2_provider_application" USING "btree" ("client_secret" "varchar_pattern_ops");


--
-- Name: oauth2_provider_application_user_id_79829054; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_application_user_id_79829054" ON "public"."oauth2_provider_application" USING "btree" ("user_id");


--
-- Name: oauth2_provider_grant_application_id_81923564; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_grant_application_id_81923564" ON "public"."oauth2_provider_grant" USING "btree" ("application_id");


--
-- Name: oauth2_provider_grant_code_49ab4ddf_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_grant_code_49ab4ddf_like" ON "public"."oauth2_provider_grant" USING "btree" ("code" "varchar_pattern_ops");


--
-- Name: oauth2_provider_grant_user_id_e8f62af8; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_grant_user_id_e8f62af8" ON "public"."oauth2_provider_grant" USING "btree" ("user_id");


--
-- Name: oauth2_provider_idtoken_application_id_08c5ff4f; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_idtoken_application_id_08c5ff4f" ON "public"."oauth2_provider_idtoken" USING "btree" ("application_id");


--
-- Name: oauth2_provider_idtoken_user_id_dd512b59; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_idtoken_user_id_dd512b59" ON "public"."oauth2_provider_idtoken" USING "btree" ("user_id");


--
-- Name: oauth2_provider_refreshtoken_application_id_2d1c311b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_refreshtoken_application_id_2d1c311b" ON "public"."oauth2_provider_refreshtoken" USING "btree" ("application_id");


--
-- Name: oauth2_provider_refreshtoken_user_id_da837fce; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "oauth2_provider_refreshtoken_user_id_da837fce" ON "public"."oauth2_provider_refreshtoken" USING "btree" ("user_id");


--
-- Name: token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_like" ON "public"."token_blacklist_outstandingtoken" USING "btree" ("jti" "varchar_pattern_ops");


--
-- Name: token_blacklist_outstandingtoken_user_id_83bc629a; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "token_blacklist_outstandingtoken_user_id_83bc629a" ON "public"."token_blacklist_outstandingtoken" USING "btree" ("user_id");


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group_permissions"
    ADD CONSTRAINT "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_group_permissions"
    ADD CONSTRAINT "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_permission"
    ADD CONSTRAINT "auth_permission_content_type_id_2f476e4b_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "public"."django_content_type"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_groups"
    ADD CONSTRAINT "auth_user_groups_group_id_97559544_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_groups"
    ADD CONSTRAINT "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_user_permissions"
    ADD CONSTRAINT "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."auth_user_user_permissions"
    ADD CONSTRAINT "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."authtoken_token"
    ADD CONSTRAINT "authtoken_token_user_id_35299eff_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_admin_log"
    ADD CONSTRAINT "django_admin_log_content_type_id_c4bce8eb_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "public"."django_content_type"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."django_admin_log"
    ADD CONSTRAINT "django_admin_log_user_id_c564eba6_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_account fintech_account_currency_id_dcd5160a_fk_fintech_currency_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_account"
    ADD CONSTRAINT "fintech_account_currency_id_dcd5160a_fk_fintech_currency_id" FOREIGN KEY ("currency_id") REFERENCES "public"."fintech_currency"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_accountmethodamount fintech_accountmetho_credit_id_c52a4a9c_fk_fintech_c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount"
    ADD CONSTRAINT "fintech_accountmetho_credit_id_c52a4a9c_fk_fintech_c" FOREIGN KEY ("credit_id") REFERENCES "public"."fintech_credit"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_accountmethodamount fintech_accountmetho_currency_id_088ff444_fk_fintech_c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount"
    ADD CONSTRAINT "fintech_accountmetho_currency_id_088ff444_fk_fintech_c" FOREIGN KEY ("currency_id") REFERENCES "public"."fintech_currency"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_accountmethodamount fintech_accountmetho_payment_method_id_6a28ff5a_fk_fintech_a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount"
    ADD CONSTRAINT "fintech_accountmetho_payment_method_id_6a28ff5a_fk_fintech_a" FOREIGN KEY ("payment_method_id") REFERENCES "public"."fintech_account"("id_payment_method") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_accountmethodamount fintech_accountmetho_transaction_id_962ad92f_fk_fintech_t; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_accountmethodamount"
    ADD CONSTRAINT "fintech_accountmetho_transaction_id_962ad92f_fk_fintech_t" FOREIGN KEY ("transaction_id") REFERENCES "public"."fintech_transaction"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_address fintech_address_country_id_e50a90ec_fk_fintech_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_address"
    ADD CONSTRAINT "fintech_address_country_id_e50a90ec_fk_fintech_country_id" FOREIGN KEY ("country_id") REFERENCES "public"."fintech_country"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_address fintech_address_user_id_b141579e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_address"
    ADD CONSTRAINT "fintech_address_user_id_b141579e_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_category fintech_category_category_type_id_8c2a931a_fk_fintech_c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_category"
    ADD CONSTRAINT "fintech_category_category_type_id_8c2a931a_fk_fintech_c" FOREIGN KEY ("category_type_id") REFERENCES "public"."fintech_categorytype"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_currency_id_b12e7221_fk_fintech_currency_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_currency_id_b12e7221_fk_fintech_currency_id" FOREIGN KEY ("currency_id") REFERENCES "public"."fintech_currency"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_payment_id_62803c60_fk_fintech_a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_payment_id_62803c60_fk_fintech_a" FOREIGN KEY ("payment_id") REFERENCES "public"."fintech_account"("id_payment_method") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_periodicity_id_6f6a311a_fk_fintech_p; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_periodicity_id_6f6a311a_fk_fintech_p" FOREIGN KEY ("periodicity_id") REFERENCES "public"."fintech_periodicity"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_registered_by_id_5c849d88_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_registered_by_id_5c849d88_fk_auth_user_id" FOREIGN KEY ("registered_by_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_seller_id_c3d4f145_fk_fintech_seller_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_seller_id_c3d4f145_fk_fintech_seller_id" FOREIGN KEY ("seller_id") REFERENCES "public"."fintech_seller"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_subcategory_id_4e4ac2ca_fk_fintech_s; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_subcategory_id_4e4ac2ca_fk_fintech_s" FOREIGN KEY ("subcategory_id") REFERENCES "public"."fintech_subcategory"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_credit fintech_credit_user_id_8f2f3be3_fk_fintech_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_credit"
    ADD CONSTRAINT "fintech_credit_user_id_8f2f3be3_fk_fintech_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."fintech_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_documenttype fintech_documenttype_country_id_id_0b6af4b2_fk_fintech_c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_documenttype"
    ADD CONSTRAINT "fintech_documenttype_country_id_id_0b6af4b2_fk_fintech_c" FOREIGN KEY ("country_id_id") REFERENCES "public"."fintech_country"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_expense fintech_expense_account_id_84b59e55_fk_fintech_a; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense"
    ADD CONSTRAINT "fintech_expense_account_id_84b59e55_fk_fintech_a" FOREIGN KEY ("account_id") REFERENCES "public"."fintech_account"("id_payment_method") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_expense fintech_expense_registered_by_id_6cd6d3d2_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense"
    ADD CONSTRAINT "fintech_expense_registered_by_id_6cd6d3d2_fk_auth_user_id" FOREIGN KEY ("registered_by_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_expense fintech_expense_subcategory_id_e6c7e1f6_fk_fintech_s; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense"
    ADD CONSTRAINT "fintech_expense_subcategory_id_e6c7e1f6_fk_fintech_s" FOREIGN KEY ("subcategory_id") REFERENCES "public"."fintech_subcategory"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_expense fintech_expense_user_id_df173b21_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_expense"
    ADD CONSTRAINT "fintech_expense_user_id_df173b21_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_identifier fintech_identifier_country_id_355176a7_fk_fintech_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_identifier"
    ADD CONSTRAINT "fintech_identifier_country_id_355176a7_fk_fintech_country_id" FOREIGN KEY ("country_id") REFERENCES "public"."fintech_country"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_identifier fintech_identifier_document_type_id_f348b6c7_fk_fintech_d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_identifier"
    ADD CONSTRAINT "fintech_identifier_document_type_id_f348b6c7_fk_fintech_d" FOREIGN KEY ("document_type_id") REFERENCES "public"."fintech_documenttype"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_phonenumber fintech_phonenumber_country_related_id_5dbe9007_fk_fintech_c; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_phonenumber"
    ADD CONSTRAINT "fintech_phonenumber_country_related_id_5dbe9007_fk_fintech_c" FOREIGN KEY ("country_related_id") REFERENCES "public"."fintech_country"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_seller fintech_seller_role_id_f00a0466_fk_fintech_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_seller"
    ADD CONSTRAINT "fintech_seller_role_id_f00a0466_fk_fintech_role_id" FOREIGN KEY ("role_id") REFERENCES "public"."fintech_role"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_seller fintech_seller_user_id_168b245a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_seller"
    ADD CONSTRAINT "fintech_seller_user_id_168b245a_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_subcategory fintech_subcategory_category_id_50f7bc8f_fk_fintech_category_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_subcategory"
    ADD CONSTRAINT "fintech_subcategory_category_id_50f7bc8f_fk_fintech_category_id" FOREIGN KEY ("category_id") REFERENCES "public"."fintech_category"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_transaction fintech_transaction_category_id_e09c657c_fk_fintech_s; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_transaction"
    ADD CONSTRAINT "fintech_transaction_category_id_e09c657c_fk_fintech_s" FOREIGN KEY ("category_id") REFERENCES "public"."fintech_subcategory"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_transaction fintech_transaction_user_id_7a424d2c_fk_fintech_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_transaction"
    ADD CONSTRAINT "fintech_transaction_user_id_7a424d2c_fk_fintech_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."fintech_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user fintech_user_city_id_f6cec28d_fk_fintech_paramslocation_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_city_id_f6cec28d_fk_fintech_paramslocation_id" FOREIGN KEY ("city_id") REFERENCES "public"."fintech_paramslocation"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user fintech_user_country_id_90ed5849_fk_fintech_country_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_country_id_90ed5849_fk_fintech_country_id" FOREIGN KEY ("country_id") REFERENCES "public"."fintech_country"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user fintech_user_document_id_f52d8362_fk_fintech_identifier_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_document_id_f52d8362_fk_fintech_identifier_id" FOREIGN KEY ("document_id") REFERENCES "public"."fintech_identifier"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user_groups fintech_user_groups_group_id_18bcab92_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_groups"
    ADD CONSTRAINT "fintech_user_groups_group_id_18bcab92_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user_groups fintech_user_groups_user_id_15fdbb30_fk_fintech_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_groups"
    ADD CONSTRAINT "fintech_user_groups_user_id_15fdbb30_fk_fintech_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."fintech_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user fintech_user_label_id_5129caf1_fk_fintech_label_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_label_id_5129caf1_fk_fintech_label_id" FOREIGN KEY ("label_id") REFERENCES "public"."fintech_label"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user fintech_user_phone_1_id_2077fbe4_fk_fintech_phonenumber_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_phone_1_id_2077fbe4_fk_fintech_phonenumber_id" FOREIGN KEY ("phone_1_id") REFERENCES "public"."fintech_phonenumber"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user fintech_user_role_id_45d07174_fk_fintech_role_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user"
    ADD CONSTRAINT "fintech_user_role_id_45d07174_fk_fintech_role_id" FOREIGN KEY ("role_id") REFERENCES "public"."fintech_role"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user_user_permissions fintech_user_user_pe_permission_id_ca4b8a5c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_user_permissions"
    ADD CONSTRAINT "fintech_user_user_pe_permission_id_ca4b8a5c_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fintech_user_user_permissions fintech_user_user_pe_user_id_5b840db9_fk_fintech_u; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."fintech_user_user_permissions"
    ADD CONSTRAINT "fintech_user_user_pe_user_id_5b840db9_fk_fintech_u" FOREIGN KEY ("user_id") REFERENCES "public"."fintech_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_acce_application_id_b22886e1_fk_oauth2_pr" FOREIGN KEY ("application_id") REFERENCES "public"."oauth2_provider_application"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_acce_id_token_id_85db651b_fk_oauth2_pr" FOREIGN KEY ("id_token_id") REFERENCES "public"."oauth2_provider_idtoken"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_acce_source_refresh_token_e66fbc72_fk_oauth2_pr" FOREIGN KEY ("source_refresh_token_id") REFERENCES "public"."oauth2_provider_refreshtoken"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_accesstoken oauth2_provider_accesstoken_user_id_6e4c9a65_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_accesstoken"
    ADD CONSTRAINT "oauth2_provider_accesstoken_user_id_6e4c9a65_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_application oauth2_provider_application_user_id_79829054_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_application"
    ADD CONSTRAINT "oauth2_provider_application_user_id_79829054_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_grant oauth2_provider_gran_application_id_81923564_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_grant"
    ADD CONSTRAINT "oauth2_provider_gran_application_id_81923564_fk_oauth2_pr" FOREIGN KEY ("application_id") REFERENCES "public"."oauth2_provider_application"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_grant oauth2_provider_grant_user_id_e8f62af8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_grant"
    ADD CONSTRAINT "oauth2_provider_grant_user_id_e8f62af8_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_idtoken oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_idtoken"
    ADD CONSTRAINT "oauth2_provider_idto_application_id_08c5ff4f_fk_oauth2_pr" FOREIGN KEY ("application_id") REFERENCES "public"."oauth2_provider_application"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_idtoken oauth2_provider_idtoken_user_id_dd512b59_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_idtoken"
    ADD CONSTRAINT "oauth2_provider_idtoken_user_id_dd512b59_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_refreshtoken"
    ADD CONSTRAINT "oauth2_provider_refr_access_token_id_775e84e8_fk_oauth2_pr" FOREIGN KEY ("access_token_id") REFERENCES "public"."oauth2_provider_accesstoken"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_refreshtoken"
    ADD CONSTRAINT "oauth2_provider_refr_application_id_2d1c311b_fk_oauth2_pr" FOREIGN KEY ("application_id") REFERENCES "public"."oauth2_provider_application"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: oauth2_provider_refreshtoken oauth2_provider_refreshtoken_user_id_da837fce_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."oauth2_provider_refreshtoken"
    ADD CONSTRAINT "oauth2_provider_refreshtoken_user_id_da837fce_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_blacklistedtoken token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_blacklistedtoken"
    ADD CONSTRAINT "token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk" FOREIGN KEY ("token_id") REFERENCES "public"."token_blacklist_outstandingtoken"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- Name: token_blacklist_outstandingtoken token_blacklist_outs_user_id_83bc629a_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "public"."token_blacklist_outstandingtoken"
    ADD CONSTRAINT "token_blacklist_outs_user_id_83bc629a_fk_auth_user" FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id") DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

