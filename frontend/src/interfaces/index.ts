export interface UserCreate {
  username: string;
  password: string;
}

export interface UserUpdate {
  username?: string;
  password?: string;
  is_admin?: boolean;
  is_active?: boolean;
  password_expires?: string; // Use string because dates are often returned as ISO strings in JSON
}

export interface UserResponse {
  id: number;
  username: string;
  is_admin: boolean;
  is_active: boolean;
  force_password_change: boolean;
  password_expires?: string; // Use string for optional datetime fields
}

export interface JWTAccessToken {
  access_token: string;
  token_type: string;
}

export interface PasswordChange {
  old_password: string;
  new_password: string;
}

export interface AppConfig {
  password_validation_enabled: boolean;
  password_min_length: number;
  password_require_digit: boolean;
  password_require_special: boolean;
  password_expire_days: number;
  login_attempts: number;
  session_expire_seconds: number;
}

export interface AppConfigUpdate {
  password_validation_enabled?: boolean;
  password_min_length?: number;
  password_require_digit?: boolean;
  password_require_special?: boolean;
  password_expire_days?: number;
  login_attempts? : number;
  session_expire_seconds?: number;
}


export interface LogResponse {
  id: number;
  user_id: number;
  event: "login" | "logout" | "password_change" | "user_added" | "user_updated" | "user_deleted" | "config_updated";
  status: "success" | "failure"; // Adjust to match the possible values of enums.LogStatus
  message?: string; // Optional field
  created_at: string; // ISO 8601 datetime string format
}


export interface IAccessTokenPayload {
  sub: string;
  exp: number;
}