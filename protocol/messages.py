"""
protocol/messages.py — All known message IDs for v26.184.
Client → Server IDs are in the 10000–19999 range.
Server → Client IDs are in the 20000–29999 range.
"""

class MessageID:
    # ── Client → Server ──────────────────────────────────────────────────
    CLIENT_HELLO        = 10100   # Initial handshake
    LOGIN               = 10101   # Login with account credentials
    KEEP_ALIVE          = 10108   # Heartbeat (no payload)
    GET_HOME_DATA       = 14101   # Request main home screen data
    END_CLIENT_TURN     = 14102   # Battle tick / command
    GO_TO_BATTLE        = 14113   # Player enters matchmaking
    BATTLE_END          = 14114   # Client reports battle result
    CLUB_CHAT           = 14715   # Club chat message

    # ── Server → Client ──────────────────────────────────────────────────
    SERVER_HELLO        = 20100   # Response to CLIENT_HELLO
    LOGIN_OK            = 20104   # Login accepted
    LOGIN_FAILED        = 20103   # Login rejected
    KEEP_ALIVE_OK       = 20108   # Heartbeat ack
    HOME_DATA           = 24101   # Full home/profile payload
    BATTLE_DATA         = 24108   # Battle room data
    BATTLE_END_OK       = 24114   # Battle end acknowledged
    CLUB_CHAT_OK        = 24715   # Club chat delivery ack
    OUT_OF_SYNC         = 24115   # Sync mismatch notification

# ========== PRIME BRAWL - PIRANHAMESSAGE BASIS-KLASSE ==========
class PiranhaMessage:
    """Basis-Klasse für alle Netzwerk-Nachrichten - PRIME BRAWL"""
    
    def __init__(self):
        self.id = 0
        self.length = 0
        self.payload = b""
        self.read_pos = 0
        self.session = None
    
    def encode(self):
        """Codiert die Nachricht in Bytes"""
        return self.payload
    
    def decode(self, data):
        """Dekodiert Bytes in die Nachricht"""
        self.payload = data
        self.read_pos = 0
    
    def read_string(self):
        """Liest einen String aus dem Payload"""
        if self.read_pos >= len(self.payload):
            return ""
        length = int.from_bytes(self.payload[self.read_pos:self.read_pos+1], 'big')
        self.read_pos += 1
        if length > 0:
            value = self.payload[self.read_pos:self.read_pos+length].decode('utf-8', errors='ignore')
            self.read_pos += length
            return value
        return ""
    
    def write_string(self, value):
        """Schreibt einen String in den Payload"""
        if value is None:
            value = ""
        encoded = value.encode('utf-8')
        self.payload += len(encoded).to_bytes(1, 'big') + encoded
    
    def read_int(self):
        """Liest einen Integer (4 Bytes) aus dem Payload"""
        if self.read_pos + 4 > len(self.payload):
            return 0
        value = int.from_bytes(self.payload[self.read_pos:self.read_pos+4], 'big')
        self.read_pos += 4
        return value
    
    def write_int(self, value):
        """Schreibt einen Integer (4 Bytes) in den Payload"""
        self.payload += value.to_bytes(4, 'big', signed=False)
    
    def read_bool(self):
        """Liest einen Boolean aus dem Payload"""
        if self.read_pos >= len(self.payload):
            return False
        value = self.payload[self.read_pos] == 1
        self.read_pos += 1
        return value
    
    def write_bool(self, value):
        """Schreibt einen Boolean in den Payload"""
        self.payload += (1 if value else 0).to_bytes(1, 'big')
    
    def read_byte(self):
        """Liest ein Byte aus dem Payload"""
        if self.read_pos >= len(self.payload):
            return 0
        value = self.payload[self.read_pos]
        self.read_pos += 1
        return value
    
    def write_byte(self, value):
        """Schreibt ein Byte in den Payload"""
        self.payload += value.to_bytes(1, 'big')
    
    def read_bytes(self, length):
        """Liest eine feste Anzahl Bytes aus dem Payload"""
        if self.read_pos + length > len(self.payload):
            return b""
        value = self.payload[self.read_pos:self.read_pos+length]
        self.read_pos += length
        return value
    
    def write_bytes(self, data):
        """Schreibt Bytes in den Payload"""
        self.payload += data
    
    def send(self, session):
        """Sendet die Nachricht an den Client"""
        if session:
            session.send(self)
