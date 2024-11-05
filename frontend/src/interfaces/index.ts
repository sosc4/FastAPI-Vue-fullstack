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
}

export interface AppConfigUpdate {
  password_validation_enabled?: boolean;
  password_min_length?: number;
  password_require_digit?: boolean;
  password_require_special?: boolean;
  password_expire_days?: number;
}
