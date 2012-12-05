CREATE TABLE ga_settings(
    ga_api_key TEXT PRIMARY KEY,
    ga_url TEXT,
    oauth_scope TEXT,
    oauth_endpoint TEXT,
    oauth_token_url TEXT,
    oauth_redirect_uri TEXT,
    oauth_client_id TEXT,
    oauth_client_secret TEXT,
    oauth_refresh_token TEXT,
    oauth_access_token TEXT
);