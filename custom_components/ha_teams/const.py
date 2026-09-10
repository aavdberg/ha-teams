"""Constants for the Microsoft Teams integration."""

DOMAIN = "ha_teams"

# Microsoft identity platform (v2.0) endpoints.
# "common" allows both personal and work/school accounts; most users will
# want "organizations" or their tenant id for a single-tenant Azure AD app.
DEFAULT_TENANT = "common"
OAUTH2_AUTHORIZE_TEMPLATE = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize"
OAUTH2_TOKEN_TEMPLATE = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"

GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"

# Delegated Graph scopes required to list joined teams/channels and post
# messages as the signed-in user. offline_access is required to obtain a
# refresh token.
OAUTH2_SCOPES = [
    "openid",
    "profile",
    "offline_access",
    "ChannelMessage.Send",
    "Team.ReadBasic.All",
    "Channel.ReadBasic.All",
]

CONF_TENANT_ID = "tenant_id"
CONF_TEAM_ID = "team_id"
CONF_TEAM_NAME = "team_name"
CONF_CHANNEL_ID = "channel_id"
CONF_CHANNEL_NAME = "channel_name"

DEFAULT_NAME = "Microsoft Teams"
