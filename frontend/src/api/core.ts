import {IAccessTokenPayload, JWTAccessToken} from '@/interfaces'
import axios, { AxiosInstance } from 'axios'
import { Buffer } from 'buffer'
import { useToast } from 'vue-toastification'
import { logout } from '@/functions'
import {useUser} from "@/stores/user";

function parseToken (token: string): object {
  return JSON.parse(Buffer.from(token.split('.')[1], 'base64').toString())
}

export class ApiCore {
  static token: JWTAccessToken | null = null
  // eslint-disable-next-line no-use-before-define
  protected static instance: ApiCore
  protected client: AxiosInstance
  protected baseURL: string

  constructor () {
    this.baseURL = import.meta.env.VITE_BACKEND_URL
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    this.client.interceptors.request.use(async (config: any) => {
      const accessTokenPayload = ApiCore.accessToken as IAccessTokenPayload

      if (!accessTokenPayload) {
        return config
      }

      const token = ApiCore.token?.access_token
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }

      // expiry is UNIX timestamp in seconds. If it is about to expire (30 seconds) send a request to /refresh
      console.log(`Token expires in ${accessTokenPayload.exp - Date.now() / 1000} seconds`)

      if (token && accessTokenPayload.exp - Date.now() / 1000 <= 0) {
        const toast = useToast()
        toast.error('Wylogowano z powodu wygaśnięcia sesji')
        location.reload()

        throw new Error('Token expired')
      }

      if (token && accessTokenPayload.exp - Date.now() / 1000 < 30) {
        console.log('Refreshing token')
        try {
          const response = await axios.post<JWTAccessToken>(`${this.baseURL}/auth/refresh`, {}, {
            headers: {
              'Authorization': 'Bearer ' + token,
            }
          })

          if (response.data.access_token) {
            ApiCore.setToken(response.data)
            config.headers.Authorization = `Bearer ${response.data.access_token}`
          }
        } catch (error) {
          console.error(error)
          ApiCore.clearToken()
        }
      }
      return config
    })

    this.client.interceptors.response.use(
      response => {
        return response
      },
      error => {
        if (error.response) {
          const toast = useToast()
          let detail = error.response.data.detail

          if (Array.isArray(detail)) {
            detail = detail.join(', ')
          }
          toast.error(detail)
        }
        return Promise.reject(error)
      }
    )
  }

  static get accessToken () {
    return this.token ? parseToken(this.token.access_token) : null
  }

  static get isLoggedIn () {
    return this.token !== null
  }

  static clearToken () {
    this.token = null
  }

  static setToken (token: JWTAccessToken) {
    this.token = token
  }

  static getInstance () {
    if (!ApiCore.instance) {
      ApiCore.instance = new ApiCore()
    }
    return ApiCore.instance
  }

  async login (formData: { username: string; password: string; }) {
    const params = new URLSearchParams()
    params.append('username', formData.username)
    params.append('password', formData.password)

    const response = await this.client.post<JWTAccessToken>('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    if (response.data.access_token) {
      ApiCore.setToken(response.data)
    }

    return response.data
  }
}
