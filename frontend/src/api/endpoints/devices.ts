import { personResource } from '../resource'

// Бэкенд требует person_id и в пути, и в теле запроса.
export const devicesApi = personResource('devices', { personIdInBody: true })
