"""Schema definitions for log objects."""

from singer_sdk import typing as th

from tap_auth0.schemas import IPType

_LocationInfoObject = th.PropertiesList(
    th.Property("country_code", th.StringType),
    th.Property("country_code3", th.StringType),
    th.Property("country_name", th.StringType),
    th.Property("city_name", th.StringType),
    th.Property("latitude", th.StringType),
    th.Property("longitude", th.StringType),
    th.Property("time_zone", th.StringType),
    th.Property(
        "continent_code",
        th.StringType,
        allowed_values=[
            "AF",  # Africa
            "AN",  # Antarctica
            "AS",  # Asia
            "EU",  # Europe
            "NA",  # North America
            "OC",  # Oceania
            "SA",  # South America
        ],
    ),
)


_Auth0ClientObject = th.PropertiesList(
    th.Property("name", th.StringType),
    th.Property("version", th.StringType),
)


LogObject = th.PropertiesList(
    th.Property("date", th.DateTimeType),
    # https://auth0.com/docs/deploy-monitor/logs/log-event-type-codes
    th.Property(
        "type",
        th.StringType,
        allowed_values=[
            "admin_update_launch",
            "api_limit",
            "cls",
            "cs",
            "depnote",
            "du",
            "f",
            "fapi",
            "fc",
            "fce",
            "fco",
            "fcoa",
            "fcp",
            "fcph",
            "fcpn",
            "fcpr",
            "fcpro",
            "fcu",
            "fd",
            "fdeac",
            "fdeaz",
            "fdecc",
            "fdu",
            "feacft",
            "feccft",
            "fede",
            "fens",
            "feoobft",
            "feotpft",
            "fepft",
            "fepotpft",
            "fercft",
            "fertft",
            "ferrt",
            "fi",
            "flo",
            "fn",
            "fp",
            "fs",
            "fsa",
            "fu",
            "fui",
            "fv",
            "fvr",
            "gd_auth_failed",
            "gd_auth_rejected",
            "gd_auth_succeed",
            "gd_enrollment_complete",
            "gd_otp_rate_limit_exceed",
            "gd_recovery_failed",
            "gd_recovery_rate_limit_exceed",
            "gd_recovery_succeed",
            "gd_send_pn",
            "gd_send_sms",
            "gd_send_sms_failure",
            "gd_send_voice",
            "gd_send_voice_failure",
            "gd_start_auth",
            "gd_start_enroll",
            "gd_tenant_update",
            "gd_unenroll",
            "gd_update_device_account",
            "limit_delegation",
            "/delegation",
            "limit_mu",
            "limit_wc",
            "limit_sul",
            "mfar",
            "mgmt_api_read",
            "pla",
            "pwd_leak",
            "ip",
            "s",
            "sapi",
            "sce",
            "scoa",
            "scp",
            "scph",
            "scpn",
            "scpr",
            "scu",
            "sd",
            "sdu",
            "seacft",
            "seccft",
            "sede",
            "sens",
            "seoobft",
            "seotpft",
            "sepft",
            "sercft",
            "sertft",
            "si",
            "srrt",
            "slo",
            "ss",
            "ssa",
            "sui",
            "sv",
            "svr",
            "sys_os_update_end",
            "sys_os_update_start",
            "sys_update_end",
            "sys_update_start",
            "ublkdu",
            "w",
        ],
    ),
    th.Property("description", th.StringType),
    th.Property("connection", th.StringType),
    th.Property("connection_id", th.StringType),
    th.Property("client_id", th.StringType),
    th.Property("client_name", th.StringType),
    th.Property("ip", IPType),
    th.Property("hostname", th.StringType),
    th.Property("user_id", th.StringType),
    th.Property("user_name", th.StringType),
    th.Property("audience", th.StringType),
    th.Property("scope", th.ArrayType(th.StringType)),
    th.Property("strategy", th.StringType),
    th.Property("strategy_type", th.StringType),
    th.Property("log_id", th.StringType),
    th.Property("isMobile", th.BooleanType),
    th.Property("details", th.ObjectType()),
    th.Property("user_agent", th.StringType),
    th.Property("location_info", _LocationInfoObject),
    th.Property("auth0_client", _Auth0ClientObject),
    th.Property("_id", th.StringType),
    th.Property("session_connection", th.StringType),
    th.Property("client_ip", IPType),
)
