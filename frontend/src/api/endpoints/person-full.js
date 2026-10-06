import { apiClient } from '../client';
import { personsApi } from './persons';
import { relationsApi } from './relations';
import { digitalAccountsApi } from './digital-accounts';
import { realEstateApi } from './real-estate';
import { vehiclesApi } from './vehicles';
import { casesApi } from './cases';
import { medicalApi } from './medical';

export const personFullApi = {
    getFullPerson: async (id) => {
        const [person, relations, digitalAccounts, realEstate, vehicles, cases, medical] = await Promise.all([
            personsApi.getById(id).catch(() => null),
            relationsApi.getForPerson(id).catch(() => []),
            digitalAccountsApi.getForPerson(id).catch(() => []),
            realEstateApi.getForPerson(id).catch(() => []),
            vehiclesApi.getForPerson(id).catch(() => []),
            casesApi.getForPerson(id).catch(() => []),
            medicalApi.getForPerson(id).catch(() => [])
        ]);
        
        return {
            ...person,
            relations,
            digital_accounts: digitalAccounts,
            real_estate: realEstate,
            vehicles,
            cases,
            medical_records: medical
        };
    }
};