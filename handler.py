'''
Smart TV Command Handler
========================

Centralized command table with expected argument counts + handlers.
One SmartTV instance holds state (power + channel).

Author: dotDennis
Course: IDATA2304
'''

from config import APP_NAME, APP_VERSION
from logic.tv import SmartTV

# ---------------------------------------------------------------------
#  Shared TV instance (state persists across requests)
# ---------------------------------------------------------------------
tv = SmartTV()

# ---------------------------------------------------------------------
#  User-facing static texts
# ---------------------------------------------------------------------
TEXT_EMPTY_COMMAND = 'ERROR: Unknown command \'{cmd}\'. See \'help\' for available commands.'
TEXT_UNKNOWN = 'ERROR: Unknown command \'{cmd}\'. See \'help\' for available commands.'
TEXT_TV_OFF = 'ERROR: TV is switched OFF. Turn it ON first.'
TEXT_ALREADY_ON = 'TV is already ON'
TEXT_ALREADY_OFF = 'TV is already OFF'
TEXT_ON = 'TV switched ON. Type \'help\' for available commands.'
TEXT_OFF = 'TV switched OFF'
TEXT_STATUS_ON = 'ON'
TEXT_STATUS_OFF = 'OFF'
TEXT_INVALID_NUMBER = 'ERROR: Invalid channel number (must be an integer)'
TEXT_GOODBYE = 'Goodbye!'
TEXT_WRONG_ARGS = 'ERROR: Command \'{cmd}\' expected {expected} argument(s), but received {got}.'
TEXT_OUT_OF_RANGE = 'ERROR: Channel out of range (valid: 1-{max_ch})'

HELP_TEXT = (
    '———————————————————————————————————————————————————\n'
    'Supported commands:\n'
    'help           - lists available commands.\n'
    'version        - displays current version.\n'
    'on             - turns ON the TV.\n'
    'off            - turns OFF the TV.\n'
    'status         - displays TV ON/OFF status.\n'
    'get_c          - displays number of available channels.\n'
    'get_ch         - displays current active channel.\n'
    'set_ch <n>     - sets channel to <n>.\n'
    'quit           - disconnect (handled by server).\n'
    '———————————————————————————————————————————————————\n'
)

# ---------------------------------------------------------------------
#  Helpers
# ---------------------------------------------------------------------
def err_wrong_args(cmd, expected, got):
    return TEXT_WRONG_ARGS.format(cmd=cmd, expected=expected, got=got)

# ---------------------------------------------------------------------
#  Per-command handlers (no arg-count checks here)
# ---------------------------------------------------------------------
def cmd_help(_):
    return HELP_TEXT

def cmd_version(_):
    return f'{APP_NAME}-{APP_VERSION}'

def cmd_on(_):
    if tv.is_on():
        return TEXT_ALREADY_ON
    tv.turn_on()
    return TEXT_ON

def cmd_off(_):
    if not tv.is_on():
        return TEXT_ALREADY_OFF
    tv.turn_off()
    return TEXT_OFF

def cmd_status(_):
    return TEXT_STATUS_ON if tv.is_on() else TEXT_STATUS_OFF

def cmd_get_c(_):
    return str(tv.get_channel_count())

def cmd_get_ch(_):
    return str(tv.get_channel())

def cmd_set_ch(args):
    try:
        n = int(args[0])
    except ValueError:
        return TEXT_INVALID_NUMBER
    try:
        tv.set_channel(n)
        return f'Channel set to {n}'
    except ValueError:
        return TEXT_OUT_OF_RANGE.format(max_ch=tv.get_channel_count())

def cmd_quit(_):
    return TEXT_GOODBYE

# ---------------------------------------------------------------------
#  Command spec (name → (expected_args, handler))
# ---------------------------------------------------------------------
COMMANDS = {
    'help':    (0, cmd_help),
    'version': (0, cmd_version),
    'on':      (0, cmd_on),
    'off':     (0, cmd_off),
    'status':  (0, cmd_status),
    'get_c':   (0, cmd_get_c),
    'get_ch':  (0, cmd_get_ch),
    'set_ch':  (1, cmd_set_ch),
    'quit':    (0, cmd_quit),
}

# ---------------------------------------------------------------------
#  Public entrypoint
# ---------------------------------------------------------------------
def handle_command(command):
    '''
    Parse a raw command string and return a response string.

    - Centralized argument-count validation via COMMANDS table.
    - Stateful via a shared SmartTV instance.
    '''
    parts = command.strip().lower().split()
    if not parts:
        return TEXT_EMPTY_COMMAND

    cmd, *args = parts

    # Strict OFF gate: ONLY 'on' is accepted while TV is OFF
    if not tv.is_on() and cmd != 'on':
        return TEXT_TV_OFF

    spec = COMMANDS.get(cmd)
    if spec is None:
        return TEXT_UNKNOWN.format(cmd=cmd)

    expected_args, handler = spec
    if len(args) != expected_args:
        return err_wrong_args(cmd, expected_args, len(args))

    return handler(args)