import pygame

translations = {
    "English": {
        "ACID BREAKOUT": "ACID BREAKOUT",
        "Play": "Play",
        "Options": "Options",
        "Quit": "Quit",
        "MUS": "MUS",
        "SFX": "SFX",
        "Screen Shake": "Screen Shake",
        "Fullscreen": "Fullscreen",
        "all_rights_reserved": "All rights reserved",
        "acid_breakout": "Acid Breakout",
        "English": "English",
        "Filipino": "Filipino",
        "Bahasa Indonesia": "Bahasa Indonesia",
        "English▼": "English▼",
        "◀BACK": "◀BACK",
        "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved":
            "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved"
    },
    "Bahasa Indonesia": {
        "ACID BREAKOUT": "PELARIAN ASAM",
        "Play": "Main",
        "Options": "Opsi",
        "Quit": "Keluar",
        "MUS": "MUS",
        "SFX": "SFX",
        "Screen Shake": "Guncangan Layar",
        "Fullscreen": "Layar Penuh",
        "all_rights_reserved": "Hak cipta dilindungi",
        "acid_breakout": "Ledakan Asam",
        "English": "Inggris",
        "Filipino": "Filipina",
        "Bahasa Indonesia": "Bahasa Indonesia",
        "English▼": "Inggris▼",
        "◀BACK": "◀KEMBALI",
        "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved":
            "© 2025 Acid Breakout | Dikembangkan oleh Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer dari 10.3 | Semua hak dilindungi"
    },
    "Filipino": {
        "ACID BREAKOUT": "PAGSABOG NG ASIDO",
        "Play": "Laro",
        "Options": "Mga Opsyon",
        "Quit": "Umalis",
        "MUS": "MUS",
        "SFX": "SFX",
        "Screen Shake": "Pagyanig ng Screen",
        "Fullscreen": "Buong Screen",
        "all_rights_reserved": "Lahat ng karapatan ay nakalaan",
        "acid_breakout": "Pagsabog ng Asido",
        "English": "Ingles",
        "Filipino": "Filipino",
        "Bahasa Indonesia": "Wikang Indones",
        "English▼": "Ingles▼",
        "◀BACK": "◀BUMALIK",
        "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved":
            "© 2025 Acid Breakout | Binuo nina Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer ng 10.3 | Lahat ng karapatan ay nakalaan"
    }
}

font_sizes = {
    "English": {
        "ACID BREAKOUT": 80,
        "Play": 50,
        "Options": 50,
        "Quit": 50,
        "MUS": 36,
        "SFX": 36,
        "Screen Shake": 36,
        "Fullscreen": 36,
        "all_rights_reserved": 8,
        "acid_breakout": 30,
        "English": 30,
        "Filipino": 30,
        "Bahasa Indonesia": 30,
        "English▼": 30,
        "◀BACK": 55,
        "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved": 8
    },
    "Bahasa Indonesia": {
        "ACID BREAKOUT": 75,
        "Play": 48,
        "Options": 48,
        "Quit": 48,
        "MUS": 36,
        "SFX": 36,
        "Screen Shake": 36,
        "Fullscreen": 36,
        "all_rights_reserved": 8,
        "acid_breakout": 30,
        "English": 30,
        "Filipino": 30,
        "Bahasa Indonesia": 30,
        "English▼": 30,
        "◀BACK": 35,
        "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved": 8
    },
    "Filipino": {
        "ACID BREAKOUT": 60,
        "Play": 37,
        "Options": 37,
        "Quit": 37,
        "MUS": 36,
        "SFX": 36,
        "Screen Shake": 36,
        "Fullscreen": 36,
        "all_rights_reserved": 8,
        "acid_breakout": 30,
        "English": 30,
        "Filipino": 30,
        "Bahasa Indonesia": 30,
        "English▼": 30,
        "◀BACK": 34,
        "© 2025 Acid Breakout | Developed by Allison, Chris Dillon, Danica, Della, Eliana, Jason AW, Jennifer of 10.3 | All rights reserved": 8
    }
}

current_lang = "English"

def set_language(lang):
    global current_lang
    current_lang = lang

def get_translation(key):
    return translations[current_lang].get(key, key)

def get_font_size(key):
    return font_sizes[current_lang].get(key, 30)