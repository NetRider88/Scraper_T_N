class AreaMapping:
    # Talabat area codes mapping
    TALABAT_CODES = {
        # Fujairah and East Coast
        'kalba': '3862',
        'khorfakkan': '3863',
        'fujairah': '3864',
        'dibba': '3865',
        'al_faseel': '3866',
        'al_owaid': '3867',
        'mirbah': '3868',
        'aqah': '3869',
        'merashid': '3870',
        'bidiya': '3871',
        'dhadna': '3872',
        'qidfa': '3873',
        'sakamkam': '3874',
        'murbah': '3875',
        'ghurfah': '3876',
        'zubarah': '3877',
         # Sharjah
        'sharjah_city': '3850',
        'al_nahda_sharjah': '3851',
        'al_majaz': '3852',
        'al_qasimia': '3853',
        'al_taawun': '3854',
        'al_khan': '3855',
        'abu_shagara': '3856',
        'al_mamzar': '3857',
        
        # Ajman
        'ajman_city': '3840',
        'al_nuaimia': '3841',
        'al_rashidiya': '3842',
        'al_jurf': '3843',
        'mushairef': '3844',
        'al_zahra': '3845',
        
        # Ras Al Khaimah
        'ras_al_khaimah_city': '3830',
        'al_nakheel': '3831',
        'al_dhait': '3832',
        'al_mamourah': '3833',
        'al_rams': '3834',
        'khuzam': '3835',
        'al_hamra': '3836',
        
        # Umm Al Quwain
        'umm_al_quwain_city': '3820',
        'al_raudah': '3821',
        'al_riqqah': '3822',
        'al_salama': '3823',
        # Add more areas as needed
    }

    # Noon doesn't use codes but needs exact area names
    NOON_NAMES = {
        'kalba': 'Kalba',
        'khorfakkan': 'Khorfakkan',
        'fujairah': 'Fujairah City',
        'dibba': 'Dibba Al Fujairah',
        'al_faseel': 'Al Faseel',
        'al_owaid': 'Al Owaid',
        'mirbah': 'Mirbah',
        'aqah': 'Aqah',
        'merashid': 'Merashid',
        'bidiya': 'Bidiya',
        'dhadna': 'Dhadna',
        'qidfa': 'Qidfa',
        'sakamkam': 'Sakamkam',
        'murbah': 'Murbah',
        'ghurfah': 'Ghurfah',
        'zubarah': 'Zubarah',

        # Sharjah
        'sharjah_city': 'Sharjah City',
        'al_nahda_sharjah': 'Al Nahda Sharjah',
        'al_majaz': 'Al Majaz',
        'al_qasimia': 'Al Qasimia',
        'al_taawun': 'Al Taawun',
        'al_khan': 'Al Khan',
        'abu_shagara': 'Abu Shagara',
        'al_mamzar': 'Al Mamzar',
        
        # Ajman
        'ajman_city': 'Ajman City',
        'al_nuaimia': 'Al Nuaimia',
        'al_rashidiya': 'Al Rashidiya',
        'al_jurf': 'Al Jurf',
        'mushairef': 'Mushairef',
        'al_zahra': 'Al Zahra',
        
        # Ras Al Khaimah
        'ras_al_khaimah_city': 'Ras Al Khaimah City',
        'al_nakheel': 'Al Nakheel',
        'al_dhait': 'Al Dhait',
        'al_mamourah': 'Al Mamourah',
        'al_rams': 'Al Rams',
        'khuzam': 'Khuzam',
        'al_hamra': 'Al Hamra',
        
        # Umm Al Quwain
        'umm_al_quwain_city': 'Umm Al Quwain City',
        'al_raudah': 'Al Raudah',
        'al_riqqah': 'Al Riqqah',
        'al_salama': 'Al Salama',
    }

    @classmethod
    def get_area_info(cls, area_input):
        """
        Get standardized area information for both platforms
        """
        # Convert input to lowercase and remove special characters
        area_key = area_input.lower().replace(' ', '_').replace('-', '_')
        
        # Check if area exists in either mapping
        talabat_code = cls.TALABAT_CODES.get(area_key)
        noon_name = cls.NOON_NAMES.get(area_key)
        
        return {
            'talabat_code': talabat_code,
            'noon_name': noon_name,
            'original_input': area_input,
            'is_valid': bool(talabat_code or noon_name)
        }

    @classmethod
    def get_all_areas(cls):
        """
        Get list of all available areas for Streamlit dropdown
        """
        return sorted(set(cls.NOON_NAMES.values()))

    @classmethod
    def suggest_areas(cls, partial_input):
        """
        Suggest similar area names based on partial input
        """
        partial = partial_input.lower()
        suggestions = []
        for name in cls.NOON_NAMES.values():
            if partial in name.lower():
                suggestions.append(name)
        return suggestions