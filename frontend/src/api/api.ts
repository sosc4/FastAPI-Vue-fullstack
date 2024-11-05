import { AppConfig, AppConfigUpdate, PasswordChange, UserCreate, UserResponse, UserUpdate } from '@/interfaces'
import { ApiCore } from './core'

export class Api extends ApiCore {
  // eslint-disable-next-line no-use-before-define
  protected static instance: Api

  static getInstance () {
    if (!Api.instance) {
      Api.instance = new Api()
    }
    return Api.instance
  }

  async readMe () {
    const response = await this.client.get<UserResponse>('/users/me')
    return response.data
  }

  async changePassword (data: PasswordChange) {
    const response = await this.client.patch<UserResponse>('/auth/password', data)
    return response.data
  }

  async createUser (data: UserCreate) {
    const response = await this.client.post<UserResponse>('/users/', data)
    return response.data
  }

  async readAllUsers () {
    const response = await this.client.get<UserResponse>('/users/all')
    return response.data
  }

  async updateUser (id: number, data: UserUpdate) {
    const response = await this.client.patch<UserResponse>(`/users/${id}`, data)
    return response.data
  }

  async deleteUser (id: number) {
    const response = await this.client.delete(`/users/${id}`)
    return response.data
  }

  async getConfig () {
    const response = await this.client.get<AppConfig>('/config')
    return response.data
  }

  async updateConfig (data: AppConfigUpdate) {
    const response = await this.client.patch<AppConfig>('/config', data)
    return response.data
  }

  async toggleConfigPasswordValidation () {
    const response = await this.client.post<AppConfig>('/config/password/validation')
    return response.data
  }
}
