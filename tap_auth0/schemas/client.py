from singer_sdk.typing import (
    ArrayType,
    BooleanType,
    EmailType,
    IntegerType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
    URIType,
)

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
    properties = PropertiesList(
        Property("lifetime_in_seconds", IntegerType),
        Property("secret_encoded", BooleanType),
        Property("scopes", ObjectType()),
        Property("alg", AlgType),
    )


class _EncryptionKeyObject(CustomObject):
    properties = PropertiesList(
        Property("pub", StringType),
        Property("cert", StringType),
        Property("subject", StringType),
    )


from tap_auth0.schemas import CustomObject


class _AWSObject(CustomObject):
    properties = PropertiesList(
        Property("principal", StringType),
        Property("role", StringType),
        Property("lifetime_in_seconds", IntegerType),
    )


class _AzureBlobObject(CustomObject):
    properties = PropertiesList(
        Property("accountName", StringType),
        Property("storageAccessKey", StringType),
        Property("containerName", StringType),
        Property("blobName", StringType),
        Property("expiration", IntegerType),
        Property("signedIdentifier", StringType),
        Property("blob_read", BooleanType),
        Property("blob_write", BooleanType),
        Property("blob_delete", BooleanType),
        Property("container_read", BooleanType),
        Property("container_write", BooleanType),
        Property("container_delete", BooleanType),
        Property("container_list", BooleanType),
    )


class _AzureSBObject(CustomObject):
    properties = PropertiesList(
        Property("namespace", StringType),
        Property("sasKeyName", StringType),
        Property("sasKey", StringType),
        Property("entityPath", StringType),
        Property("expiration", IntegerType),
    )


class _RMSObject(CustomObject):
    properties = PropertiesList(
        Property("url", URIType),
    )


class _MSCRMObject(CustomObject):
    properties = PropertiesList(
        Property("url", URIType),
    )


class _SlackObject(CustomObject):
    properties = PropertiesList(
        Property("team", StringType),
    )


class _SentryObject(CustomObject):
    properties = PropertiesList(
        Property("org_slug", StringType),
        Property("base_url", URIType),
    )


class _EchoSignObject(CustomObject):
    properties = PropertiesList(
        Property("domain", StringType),
    )


class _EgnyteObject(CustomObject):
    properties = PropertiesList(
        Property("domain", StringType),
    )


class _FirebaseObject(CustomObject):
    properties = PropertiesList(
        Property("secret", StringType),
        Property("private_key_id", StringType),
        Property("private_key", StringType),
        Property("client_email", EmailType),
        Property("lifetime_in_seconds", IntegerType),
    )


class _NewRelicObject(CustomObject):
    properties = PropertiesList(
        Property("account", StringType),
    )


class _Office365Object(CustomObject):
    properties = PropertiesList(
        Property("domain", StringType),
        Property("connection", StringType),
    )


class _SalesforceObject(CustomObject):
    properties = PropertiesList(
        Property("entity_id", URIType),
    )


class _SalesforceAPIObject(CustomObject):
    properties = PropertiesList(
        Property("clientid", StringType),
        Property("principal", StringType),
        Property("communityName", StringType),
        Property("community_url_section", StringType),
    )


class _SalesforceSandboxAPIObject(CustomObject):
    properties = PropertiesList(
        Property("clientid", StringType),
        Property("principal", StringType),
        Property("communityName", StringType),
        Property("community_url_section", StringType),
    )


class _SAMLPObject(CustomObject):
    properties = PropertiesList(
        Property("mappings", ObjectType()),
        Property("audience", StringType),
        Property("recipient", StringType),
        Property("createUpnClaim", BooleanType),
        Property("mapUnknownClaimsAsIs", BooleanType),
        Property("passthroughClaimsWithNoMapping", BooleanType),
        Property("mapIdentities", BooleanType),
        Property("signatureAlgorithm", StringType),
        Property("digestAlgorithm", StringType),
        Property("issuer", StringType),
        Property("destination", StringType),
        Property("lifetimeInSeconds", IntegerType),
        Property("signResponse", BooleanType),
        Property("nameIdentifierFormat", StringType),
        Property("nameIdentifierProbes", ArrayType(StringType)),
        Property("authnContextClassRef", StringType),
    )


class _LayerObject(CustomObject):
    properties = PropertiesList(
        Property("providerId", StringType),
        Property("keyId", StringType),
        Property("privateKey", StringType),
        Property("principal", StringType),
        Property("expiration", IntegerType),
    )


class _SAPAPIObject(CustomObject):
    properties = PropertiesList(
        Property("clientId", StringType),
        Property("usernameAttribute", StringType),
        Property("tokenEndpointUrl", URIType),
        Property("scope", StringType),
        Property("servicePassword", StringType),
        Property("nameIdentifierFormat", StringType),
    )


class _SharePointObject(CustomObject):
    properties = PropertiesList(
        Property("url", URIType),
        Property("external_url", ArrayType(URIType)),
    )


class _SpringCMObject(CustomObject):
    properties = PropertiesList(
        Property("acsurl", URIType),
    )


class _WAMSObject(CustomObject):
    properties = PropertiesList(
        Property("masterkey", StringType),
    )


class _ZendeskObject(CustomObject):
    properties = PropertiesList(
        Property("accountName", StringType),
    )


class _ZoomObject(CustomObject):
    properties = PropertiesList(
        Property("account", StringType),
    )


class _SSOIntegrationObject(CustomObject):
    properties = PropertiesList(
        Property("name", StringType),
        Property("version", StringType),
    )


class _AddonsObject(CustomObject):
    properties = PropertiesList(
        Property("aws", _AWSObject),
        Property("azure_blob", _AzureBlobObject),
        Property("azure_sb", _AzureSBObject),
        Property("rms", _RMSObject),
        Property("mscrm", _MSCRMObject),
        Property("slack", _SlackObject),
        Property("sentry", _SentryObject),
        Property("box", ObjectType()),
        Property("cloudbees", ObjectType()),
        Property("concur", ObjectType()),
        Property("dropbox", ObjectType()),
        Property("echosign", _EchoSignObject),
        Property("egnyte", _EgnyteObject),
        Property("firebase", _FirebaseObject),
        Property("newrelic", _NewRelicObject),
        Property("office365", _Office365Object),
        Property("salesforce", _SalesforceObject),
        Property("salesforce_api", _SalesforceAPIObject),
        Property("salesforce_sandbox_api", _SalesforceSandboxAPIObject),
        Property("samlp", _SAMLPObject),
        Property("layer", _LayerObject),
        Property("sap_api", _SAPAPIObject),
        Property("sharepoint", _SharePointObject),
        Property("springcm", _SpringCMObject),
        Property("wams", _WAMSObject),
        Property("wsfed", ObjectType()),
        Property("zendesk", _ZendeskObject),
        Property("zoom", _ZoomObject),
        Property("sso_integration", _SSOIntegrationObject),
    )


class _AndroidObject(CustomObject):
    properties = PropertiesList(
        Property("app_package_name", StringType),
        Property("sha256_cert_fingerprints", ArrayType(StringType)),
    )


class _iOSObject(CustomObject):
    properties = PropertiesList(
        Property("team_id", StringType),
        Property("app_bundle_identifier", StringType),
    )


class _MobileObject(CustomObject):
    properties = PropertiesList(
        Property("android", _AndroidObject),
        Property("ios", _iOSObject),
    )


class _AppleObject(CustomObject):
    properties = PropertiesList(
        Property("enabled", BooleanType),
    )


class _FacebookObject(CustomObject):
    properties = PropertiesList(
        Property("enabled", BooleanType),
    )


class _NativeSocialLoginObject(CustomObject):
    properties = PropertiesList(
        Property("apple", _AppleObject),
        Property("facebook", _FacebookObject),
    )


class _RefreshTokenObject(CustomObject):
    properties = PropertiesList(
        Property("rotation_type", RotationTypeType),
        Property("expiration_type", ExpirationTypeType),
        Property("leeway", IntegerType),
        Property("token_lifetime", IntegerType),
        Property("infinite_token_lifetime", BooleanType),
        Property("idle_token_lifetime", IntegerType),
        Property("infinite_idle_token_lifetime", BooleanType),
    )


class ClientObject(CustomObject):
    properties = PropertiesList(
        Property("client_id", StringType),
        Property("tenant", StringType),
        Property("name", StringType),
        Property("description", StringType),
        Property("global", BooleanType),
        Property("client_secret", StringType),
        Property("app_type", AppTypeType),
        Property("logo_uri", URIType),
        Property("is_first_party", BooleanType),
        Property("oidc_conformant", BooleanType),
        Property("callbacks", ArrayType(URIType)),
        Property("allowed_origins", ArrayType(URIType)),
        Property("web_origins", ArrayType(URIType)),
        Property("client_aliases", ArrayType(StringType)),
        Property("allowed_clients", ArrayType(StringType)),
        Property("allowed_logout_urls", ArrayType(URIType)),
        Property("grant_types", ArrayType(GrantTypeType)),
        Property("jwt_configuration", _JWTConfigurationObject),
        Property("signing_keys", ArrayType(ObjectType())),
        Property("encryption_key", _EncryptionKeyObject),
        Property("sso", BooleanType),
        Property("sso_disabled", BooleanType),
        Property("cross_origin_auth", BooleanType),
        Property("cross_origin_loc", URIType),
        Property("custom_login_page_on", BooleanType),
        Property("custom_login_page", StringType),
        Property("custom_login_page_preview", StringType),
        Property("form_template", StringType),
        Property("addons", _AddonsObject),
        Property("token_endpoint_auth_method", TokenEndpointAuthMethodType),
        Property("client_metadata", ObjectType()),
        Property("mobile", _MobileObject),
        Property("initiate_login_uri", URIType),
        Property("native_social_login", _NativeSocialLoginObject),
        Property("refresh_token", _RefreshTokenObject),
        Property("organization_usage", OrganizationUsageType),
        Property("organization_require_behavior", OrganizationRequireBehaviourType),
        Property("is_token_endpoint_ip_header_trusted", BooleanType),
    )
