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

# Adaptive Cards: messages can carry a full Adaptive Card as an attachment
# instead of plain text. 1.5 is broadly supported by Teams desktop/web/mobile
# at time of writing.
ADAPTIVE_CARD_CONTENT_TYPE = "application/vnd.microsoft.card.adaptive"
DEFAULT_ADAPTIVE_CARD_VERSION = "1.5"

SERVICE_SEND_CARD = "send_card"
ATTR_CARD = "card"
ATTR_CONFIG_ENTRY_ID = "config_entry_id"

# Graph API resiliency: retry 429/5xx with backoff, never retry 4xx
# auth/permission errors.
MAX_RETRY_ATTEMPTS = 4
RETRY_BACKOFF_BASE_SECONDS = 1.0
RETRY_BACKOFF_MAX_SECONDS = 30.0
