# Localization and general texts for the help menu
HELP_TEXTS = {
    'th': {
        'title': "Help Me! - คำสั่งบอททั้งหมด",
        'description_header': (
            "## วิธีใช้งานคำสั่ง\n"
            "`\\` = คำสั่งแบบพิมพ์แชทแบบเดิม (Prefix)\n"
            "`/` = คำสั่งแบบพิมพ์เฉียง (Slash Command)\n"
        ),
        'category_headers': {
            'prefix': "### คำสั่งแบบปกติ (\\ Prefix)",
            'slash': "### Slash Commands (/) ที่แนะนำ",
            'context': "### เมนูแอปพลิเคชัน (คลิกขวาที่สมาชิก -> Apps)"
        },
        'note_title': "หมายเหตุ",
        'note_description': "หากเพื่อนที่คุณต้องการปลุกไม่ได้เปิดการแจ้งเตือน บอทอาจทำงานได้ไม่สมบูรณ์",
        'footer_text': "คลิกปุ่มด้านล่างเพื่อเลือกภาษา / สเปกความปลอดภัย"
    },
    'en': {
        'title': "Help Me! - Bot Commands Info",
        'description_header': (
            "## Command Usage\n"
            "`\\` = Legacy prefix command\n"
            "`/` = Modern slash command\n"
        ),
        'category_headers': {
            'prefix': "### Prefix Commands (\\)",
            'slash': "### Recommended Slash Commands (/)",
            'context': "### App / Context Menu (Right-click Member -> Apps)"
        },
        'note_title': "Note",
        'note_description': "If the target user has notifications turned off, the waking mechanism might not work perfectly.",
        'footer_text': "Click the buttons below to switch language / invite the bot"
    }
}

# Commands metadata list
COMMANDS_METADATA = [
    # Prefix Commands
    {
        'name': 'help',
        'type': 'prefix',
        'description': {
            'th': 'แสดงคำแนะนำความช่วยเหลือการใช้งานบอท',
            'en': 'Show this help instructions'
        }
    },
    {
        'name': 'stop',
        'type': 'prefix',
        'description': {
            'th': 'หยุดการสลับย้ายห้องเสียงทันที',
            'en': 'Stop poking actions immediately'
        }
    },
    
    # Slash Commands
    {
        'name': 'help',
        'type': 'slash',
        'description': {
            'th': 'เปิดหน้าต่างข้อมูลคำช่วยเหลือแบบโต้ตอบ',
            'en': 'Display interactive help information'
        }
    },
    {
        'name': 'poke',
        'type': 'slash',
        'description': {
            'th': 'ปลุกเพื่อนโดยสลับห้องเสียงไปมาตามรอบที่กำหนด (ระบุผู้ใช้ และจำนวนรอบ)',
            'en': 'Wake friends by moving them between voice channels (specify user & rounds)'
        }
    },
    {
        'name': 'stop',
        'type': 'slash',
        'description': {
            'th': 'หยุดบอทจากการเคลื่อนย้ายสมาชิก',
            'en': 'Stop moving members and clean up temporary channels'
        }
    },
    {
        'name': 'invite',
        'type': 'slash',
        'description': {
            'th': 'ดึงลิงก์คำเชิญเข้าร่วมเซิร์ฟเวอร์สำหรับบอทนี้',
            'en': 'Generate invite links for this bot'
        }
    },
    {
        'name': 'micmute',
        'type': 'slash',
        'description': {
            'th': 'ปิดไมโครโฟนของสมาชิกชั่วคราว (กำหนดเวลาและหน่วยวินาที/นาที/ชั่วโมง ได้)',
            'en': 'Mute microphone of a member temporarily (s/m/h)'
        }
    },
    {
        'name': 'earmute',
        'type': 'slash',
        'description': {
            'th': 'ปิดหูฟังเสียงของสมาชิกชั่วคราว (กำหนดเวลาและหน่วยวินาที/นาที/ชั่วโมง ได้)',
            'en': 'Deafen headphone of a member temporarily (s/m/h)'
        }
    },
    {
        'name': 'muteboth',
        'type': 'slash',
        'description': {
            'th': 'ปิดหูฟังเสียงและไมโครโฟนของสมาชิกชั่วคราว (กำหนดเวลาและหน่วยวินาที/นาที/ชั่วโมง ได้)',
            'en': 'Deafen headphone and mute microphone of a member temporarily (s/m/h)'
        }
    },
    {
        'name': 'mute',
        'type': 'slash',
        'description': {
            'th': 'เลือกปิดไมโครโฟน หูฟัง หรือทั้งสองอย่างชั่วคราว (กำหนดเวลาและหน่วยวินาที/นาที/ชั่วโมง ได้)',
            'en': 'Mute mic, deafen headphones, or both for a specific duration (s/m/h)'
        }
    },
    # Context Menu (Apps)
    {
        'name': 'Poke Until Stop',
        'type': 'context',
        'description': {
            'th': 'ย้ายสมาชิกปลุกเรื่อย ๆ อย่างต่อเนื่อง จนกว่าจะมีคนสั่งหยุด',
            'en': 'Continuously move member between channels until stopped'
        }
    },
    {
        'name': 'Stop Poke',
        'type': 'context',
        'description': {
            'th': 'หยุดการสลับห้อง/ปลุกทันทีสำหรับผู้ใช้ท่านนั้น',
            'en': 'Stop poking/moving that specific user immediately'
        }
    }
]
