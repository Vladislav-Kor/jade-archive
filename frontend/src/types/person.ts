export interface Person {
    id: number
    full_name: string
    short_name: string
    photo_path?: string
    birth_date?: string
    gender?: string
    address?: string
    phone?: string
    email?: string
    height?: number
    weight?: number
    clothing_size?: string
    shoe_size?: number
    chest_size?: number
    waist_size?: number
    hip_size?: number
    blood_type?: string
    rh_factor?: string
    allergies?: string
    chronic_diseases?: string
    medications?: string
    blood_pressure?: string
    heart_rate?: number
    passport_number?: string
    inn?: string
    snils?: string
    driver_license_category?: string
    driver_license_number?: string
    marital_status?: string
    children_count: number
    education?: string
    profession?: string
    workplace?: string
    favorite_color?: string
    favorite_flowers?: string
    favorite_food?: string
    favorite_music?: string
    favorite_movies?: string
    hobbies?: string
    importance: number
    importance_level: string
    notes?: string
    created_at?: string
    updated_at?: string
    social_media?: SocialMedia[]
    tags_prefs?: TagPreference[]
    digital_accounts?: DigitalAccount[]
    real_estate?: RealEstate[]
    vehicles?: Vehicle[]
    cases?: Case[]
    medical_records?: MedicalRecord[]
    partners?: Partner[]
    devices?: Device[]
    cross_records?: CrossRecord[]
    relations?: Relation[]
}

export interface Partner {
    id: number
    person_id: number
    partner_id: number
    relationship_type: string
    relationship_status?: string
    relationship_label?: string
    start_date?: string
    end_date?: string
    breakup_reason?: string
    emotional_connection?: string
    physical_connection?: string
    relationship_rating?: number
    relationship_notes?: string
    created_at?: string
    updated_at?: string
}

export interface Device {
    id: number
    person_id: number
    device_type: string
    brand: string
    model: string
    color?: string
    specs?: string
    imei?: string
    serial_number?: string
    purchase_date?: string
    purchase_price?: number
    purchase_place?: string
    warranty_until?: string
    accessories?: string
    condition?: string
    notes?: string
    is_active: boolean
    created_at?: string
    updated_at?: string
}

export interface Category {
    id: number
    name: string
    slug: string
    icon?: string
    color?: string
    description?: string
    parent_id?: number
    is_system: boolean
    sort_order: number
    children?: Category[]
    created_at?: string
}

export interface CrossRecord {
    id: number
    person_id: number
    title: string
    description?: string
    record_type: string
    primary_category_id: number
    secondary_categories?: number[]
    data?: any
    record_date?: string
    start_date?: string
    end_date?: string
    status: string
    importance: number
    is_private: boolean
    created_by?: number
    created_at?: string
    updated_at?: string
}

export interface SocialMedia {
    id: number
    platform: string
    link: string
    created_at?: string
    updated_at?: string
}

export interface TagPreference {
    id: number
    category: string
    value: string
}

export interface DigitalAccount {
    id: number
    platform_type: string
    platform_name: string
    username?: string
    email?: string
    phone?: string
    password?: string
    account_id?: string
    server_id?: string
    nickname?: string
    server?: string
    level?: number
    rank?: string
    guild?: string
    characters?: string
    notes?: string
    is_active: boolean
    link?: string
    created_at?: string
    updated_at?: string
}

export interface RealEstate {
    id: number
    property_type: string
    property_name?: string
    address: string
    total_area?: number
    living_area?: number
    land_area?: number
    floor?: number
    total_floors?: number
    rooms_count?: number
    bathroom_count?: number
    balcony_count?: number
    ownership_type?: string
    ownership_percent: number
    cadastral_number?: string
    registration_date?: string
    purchase_price?: number
    current_value?: number
    condition?: string
    year_built?: number
    renovation_year?: number
    notes?: string
    is_active: boolean
    created_at?: string
    updated_at?: string
}

export interface Vehicle {
    id: number
    vehicle_type: string
    brand: string
    model: string
    year?: number
    color?: string
    license_plate?: string
    vin?: string
    engine_number?: string
    engine_capacity?: number
    horsepower?: number
    mileage?: number
    transmission?: string
    drive_type?: string
    fuel_type?: string
    ownership_type?: string
    registration_date?: string
    registration_number?: string
    purchase_price?: number
    current_value?: number
    condition?: string
    notes?: string
    is_active: boolean
    created_at?: string
    updated_at?: string
}

export interface Case {
    id: number
    case_type: string
    title: string
    description?: string
    priority: string
    status: string
    due_date?: string
    created_at?: string
    updated_at?: string
}

export interface MedicalRecord {
    id: number
    record_type: string
    title: string
    description?: string
    record_date?: string
    doctor_name?: string
    attachments?: string
    created_at?: string
    updated_at?: string
}

export interface Relation {
    id: number
    parent_id: number
    child_id: number
    relation_type: string
    created_at?: string
    updated_at?: string
}
