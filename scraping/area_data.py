# Platform-specific area codes/identifiers
PLATFORM_CODES = {
    'talabat': {
        # Fujairah and East Coast
        'al_faseel': '3866',
        'kalba': '3862',
        'khorfakkan': '3863',
        'fujairah': '3864',
        'dibba': '3865',
        'al_owaid': '3867',
        'mirbah': '3868',
        'aqah': '3869',
        # ... (keep other area codes)
    },
    'noon': {
        # Standardized names for Noon
        'al_faseel': 'Al Faseel',
        'kalba': 'Kalba',
        'khorfakkan': 'Khorfakkan',
        'fujairah': 'Fujairah City',
        'dibba': 'Dibba Al Fujairah',
        'al_owaid': 'Al Owaid',
        'mirbah': 'Mirbah',
        'aqah': 'Aqah',
        # ... (keep other area names)
    }
}

# Update UAE_AREAS with correct structure
UAE_AREAS = {
    'al_faseel': {
        'alternatives': [
            'faseel',
            'al fasseel',
            'الفصيل',
            'fujairah faseel',
            'al-faseel'  # Added hyphenated version
        ],
        'talabat_code': PLATFORM_CODES['talabat']['al_faseel'],
        'noon_name': PLATFORM_CODES['noon']['al_faseel']
    },
    'kalba': {
        'alternatives': [
            'kalba city',
            'كلباء',
            'khor kalba',
            'kalba corniche'
        ],
        'talabat_code': PLATFORM_CODES['talabat']['kalba'],
        'noon_name': PLATFORM_CODES['noon']['kalba']
    },
    # ... (continue for other areas)
}

def get_area_info(area_input):
    """
    Get all information about an area including platform-specific codes.
    
    Args:
        area_input (str): User input area name
        
    Returns:
        dict: Area information including alternatives and platform codes
    """
    # Normalize input
    area_key = area_input.lower().replace('-', '_').replace(' ', '_')
    
    # Direct match
    if area_key in UAE_AREAS:
        return {
            'key': area_key,
            'alternatives': UAE_AREAS[area_key]['alternatives'],
            'talabat_code': UAE_AREAS[area_key]['talabat_code'],
            'noon_name': UAE_AREAS[area_key]['noon_name'],
            'is_valid': True
        }
    
    # Search through alternatives
    for key, data in UAE_AREAS.items():
        if any(area_input.lower() in alt.lower() for alt in data['alternatives']):
            return {
                'key': key,
                'alternatives': data['alternatives'],
                'talabat_code': data['talabat_code'],
                'noon_name': data['noon_name'],
                'is_valid': True
            }
    
    # No match found
    return {
        'key': area_key,
        'alternatives': [],
        'talabat_code': None,
        'noon_name': None,
        'is_valid': False
    }

def get_all_uae_areas():
    """Returns a structured dictionary of all UAE areas"""
    return {
        'Dubai': [
            'Dubai Marina', 'JBR', 'Palm Jumeirah', 'Downtown Dubai',
            'Business Bay', 'Dubai Silicon Oasis', 'International City',
            'Dubai Sports City', 'JLT', 'Al Barsha', 'Deira', 'Bur Dubai'
        ],
        'Abu Dhabi': [
            'Abu Dhabi City', 'Yas Island', 'Reem Island', 'Saadiyat Island',
            'Khalifa City', 'Al Raha'
        ],
        'Sharjah': [
            'Sharjah City', 'Al Nahda', 'Al Majaz', 'Al Qasimia'
        ],
        'Fujairah': [
            'Fujairah City', 'Al Faseel', 'Al Owaid', 'Mirbah', 'Qidfa',
            'Madhab', 'Sakamkam'
        ],
        'East Coast': [
            'Kalba', 'Khorfakkan', 'Dibba', 'Aqah'
        ],
        'Ajman': [
            'Ajman City', 'Al Nuaimia', 'Al Rashidiya'
        ],
        'RAK': [
            'Ras Al Khaimah', 'Al Hamra'
        ],
        'UAQ': [
            'Umm Al Quwain'
        ]
    }