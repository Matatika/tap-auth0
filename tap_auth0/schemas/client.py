"""Schema definitions for client objects."""

from singer_sdk import typing as th

from tap_auth0.schemas import CustomObject
from tap_auth0.types.client import (
    AppTypeType,
    GrantTypeType,
    OrganizationRequireBehaviourType,
    OrganizationUsageType,
    TokenEndpointAuthMethodType,
)
from tap_auth0.types.jwt_configuration import AlgType
from tap_auth0.types.refresh_token import ExpirationTypeType, RotationTypeType


class _JWTConfigurationObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("lifetime_in_seconds", th.IntegerType),
        th.Property("secret_encoded", th.BooleanType),
        th.Property("scopes", th.ObjectType()),
        th.Property("alg", AlgType),
    )


class _EncryptionKeyObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("pub", th.StringType),
        th.Property("cert", th.StringType),
        th.Property("subject", th.StringType),
    )


class _AWSObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("principal", th.StringType),
        th.Property("role", th.StringType),
        th.Property("lifetime_in_seconds", th.IntegerType),
    )


class _AzureBlobObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("accountName", th.StringType),
        th.Property("storageAccessKey", th.StringType),
        th.Property("containerName", th.StringType),
        th.Property("blobName", th.StringType),
        th.Property("expiration", th.IntegerType),
        th.Property("signedIdentifier", th.StringType),
        th.Property("blob_read", th.BooleanType),
        th.Property("blob_write", th.BooleanType),
        th.Property("blob_delete", th.BooleanType),
        th.Property("container_read", th.BooleanType),
        th.Property("container_write", th.BooleanType),
        th.Property("container_delete", th.BooleanType),
        th.Property("container_list", th.BooleanType),
    )


class _AzureSBObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("namespace", th.StringType),
        th.Property("sasKeyName", th.StringType),
        th.Property("sasKey", th.StringType),
        th.Property("entityPath", th.StringType),
        th.Property("expiration", th.IntegerType),
    )


class _RMSObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("url", th.URIType),
    )


class _MSCRMObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("url", th.URIType),
    )


class _SlackObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("team", th.StringType),
    )


class _SentryObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("org_slug", th.StringType),
        th.Property("base_url", th.URIType),
    )


class _EchoSignObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("domain", th.StringType),
    )


class _EgnyteObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("domain", th.StringType),
    )


class _FirebaseObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("secret", th.StringType),
        th.Property("private_key_id", th.StringType),
        th.Property("private_key", th.StringType),
        th.Property("client_email", th.EmailType),
        th.Property("lifetime_in_seconds", th.IntegerType),
    )


class _NewRelicObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("account", th.StringType),
    )


class _Office365Object(CustomObject):
    properties = th.PropertiesList(
        th.Property("domain", th.StringType),
        th.Property("connection", th.StringType),
    )


class _SalesforceObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("entity_id", th.URIType),
    )


class _SalesforceAPIObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("clientid", th.StringType),
        th.Property("principal", th.StringType),
        th.Property("communityName", th.StringType),
        th.Property("community_url_section", th.StringType),
    )


class _SalesforceSandboxAPIObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("clientid", th.StringType),
        th.Property("principal", th.StringType),
        th.Property("communityName", th.StringType),
        th.Property("community_url_section", th.StringType),
    )


class _SAMLPObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("mappings", th.ObjectType()),
        th.Property("audience", th.StringType),
        th.Property("recipient", th.StringType),
        th.Property("createUpnClaim", th.BooleanType),
        th.Property("mapUnknownClaimsAsIs", th.BooleanType),
        th.Property("passthroughClaimsWithNoMapping", th.BooleanType),
        th.Property("mapIdentities", th.BooleanType),
        th.Property("signatureAlgorithm", th.StringType),
        th.Property("digestAlgorithm", th.StringType),
        th.Property("issuer", th.StringType),
        th.Property("destination", th.StringType),
        th.Property("lifetimeInSeconds", th.IntegerType),
        th.Property("signResponse", th.BooleanType),
        th.Property("nameIdentifierFormat", th.StringType),
        th.Property("nameIdentifierProbes", th.ArrayType(th.StringType)),
        th.Property("authnContextClassRef", th.StringType),
    )


class _LayerObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("providerId", th.StringType),
        th.Property("keyId", th.StringType),
        th.Property("privateKey", th.StringType),
        th.Property("principal", th.StringType),
        th.Property("expiration", th.IntegerType),
    )


class _SAPAPIObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("clientId", th.StringType),
        th.Property("usernameAttribute", th.StringType),
        th.Property("tokenEndpointUrl", th.URIType),
        th.Property("scope", th.StringType),
        th.Property("servicePassword", th.StringType),
        th.Property("nameIdentifierFormat", th.StringType),
    )


class _SharePointObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("url", th.URIType),
        th.Property("external_url", th.ArrayType(th.URIType)),
    )


class _SpringCMObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("acsurl", th.URIType),
    )


class _WAMSObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("masterkey", th.StringType),
    )


class _ZendeskObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("accountName", th.StringType),
    )


class _ZoomObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("account", th.StringType),
    )


class _SSOIntegrationObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("name", th.StringType),
        th.Property("version", th.StringType),
    )


class _AddonsObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("aws", _AWSObject),
        th.Property("azure_blob", _AzureBlobObject),
        th.Property("azure_sb", _AzureSBObject),
        th.Property("rms", _RMSObject),
        th.Property("mscrm", _MSCRMObject),
        th.Property("slack", _SlackObject),
        th.Property("sentry", _SentryObject),
        th.Property("box", th.ObjectType()),
        th.Property("cloudbees", th.ObjectType()),
        th.Property("concur", th.ObjectType()),
        th.Property("dropbox", th.ObjectType()),
        th.Property("echosign", _EchoSignObject),
        th.Property("egnyte", _EgnyteObject),
        th.Property("firebase", _FirebaseObject),
        th.Property("newrelic", _NewRelicObject),
        th.Property("office365", _Office365Object),
        th.Property("salesforce", _SalesforceObject),
        th.Property("salesforce_api", _SalesforceAPIObject),
        th.Property("salesforce_sandbox_api", _SalesforceSandboxAPIObject),
        th.Property("samlp", _SAMLPObject),
        th.Property("layer", _LayerObject),
        th.Property("sap_api", _SAPAPIObject),
        th.Property("sharepoint", _SharePointObject),
        th.Property("springcm", _SpringCMObject),
        th.Property("wams", _WAMSObject),
        th.Property("wsfed", th.ObjectType()),
        th.Property("zendesk", _ZendeskObject),
        th.Property("zoom", _ZoomObject),
        th.Property("sso_integration", _SSOIntegrationObject),
    )


class _AndroidObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("app_package_name", th.StringType),
        th.Property("sha256_cert_fingerprints", th.ArrayType(th.StringType)),
    )


class _iOSObject(CustomObject):  # noqa: N801
    properties = th.PropertiesList(
        th.Property("team_id", th.StringType),
        th.Property("app_bundle_identifier", th.StringType),
    )


class _MobileObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("android", _AndroidObject),
        th.Property("ios", _iOSObject),
    )


class _AppleObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("enabled", th.BooleanType),
    )


class _FacebookObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("enabled", th.BooleanType),
    )


class _NativeSocialLoginObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("apple", _AppleObject),
        th.Property("facebook", _FacebookObject),
    )


class _RefreshTokenObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("rotation_type", RotationTypeType),
        th.Property("expiration_type", ExpirationTypeType),
        th.Property("leeway", th.IntegerType),
        th.Property("token_lifetime", th.IntegerType),
        th.Property("infinite_token_lifetime", th.BooleanType),
        th.Property("idle_token_lifetime", th.IntegerType),
        th.Property("infinite_idle_token_lifetime", th.BooleanType),
    )


class ClientObject(CustomObject):
    properties = th.PropertiesList(
        th.Property("client_id", th.StringType),
        th.Property("tenant", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("global", th.BooleanType),
        th.Property("client_secret", th.StringType),
        th.Property("app_type", AppTypeType),
        th.Property("logo_uri", th.URIType),
        th.Property("is_first_party", th.BooleanType),
        th.Property("oidc_conformant", th.BooleanType),
        th.Property("callbacks", th.ArrayType(th.URIType)),
        th.Property("allowed_origins", th.ArrayType(th.URIType)),
        th.Property("web_origins", th.ArrayType(th.URIType)),
        th.Property("client_aliases", th.ArrayType(th.StringType)),
        th.Property("allowed_clients", th.ArrayType(th.StringType)),
        th.Property("allowed_logout_urls", th.ArrayType(th.URIType)),
        th.Property("grant_types", th.ArrayType(GrantTypeType)),
        th.Property("jwt_configuration", _JWTConfigurationObject),
        th.Property("signing_keys", th.ArrayType(th.ObjectType())),
        th.Property("encryption_key", _EncryptionKeyObject),
        th.Property("sso", th.BooleanType),
        th.Property("sso_disabled", th.BooleanType),
        th.Property("cross_origin_auth", th.BooleanType),
        th.Property("cross_origin_loc", th.URIType),
        th.Property("custom_login_page_on", th.BooleanType),
        th.Property("custom_login_page", th.StringType),
        th.Property("custom_login_page_preview", th.StringType),
        th.Property("form_template", th.StringType),
        th.Property("addons", _AddonsObject),
        th.Property("token_endpoint_auth_method", TokenEndpointAuthMethodType),
        th.Property("client_metadata", th.ObjectType()),
        th.Property("mobile", _MobileObject),
        th.Property("initiate_login_uri", th.URIType),
        th.Property("native_social_login", _NativeSocialLoginObject),
        th.Property("refresh_token", _RefreshTokenObject),
        th.Property("organization_usage", OrganizationUsageType),
        th.Property("organization_require_behavior", OrganizationRequireBehaviourType),
        th.Property("is_token_endpoint_ip_header_trusted", th.BooleanType),
        th.Property("callback_url_template", th.BooleanType),
        th.Property("owners", th.ArrayType(th.StringType)),
    )
