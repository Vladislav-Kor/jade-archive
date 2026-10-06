import { personResource } from '../resource'

// Бэкенд требует person_id и в пути, и в теле запроса.
export const partnersApi = personResource('partners', { personIdInBody: true })
